#!/usr/bin/env bash
# session-summary.sh — Generate a session summary report from agent logs
#
# Parses structured log entries and produces a human-readable summary.
#
# Usage:
#   bash session-summary.sh <log-file>

set -uo pipefail

LOG_FILE="${1:-}"

if [[ -z "$LOG_FILE" || ! -f "$LOG_FILE" ]]; then
  echo "Usage: bash session-summary.sh <log-file>"
  exit 1
fi

# ── Parse log data ────────────────────────────────────────────────────────

# Session info
SESSION_ID=$(grep '"session_start"' "$LOG_FILE" | head -1 | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
START_TIME=$(grep '"session_start"' "$LOG_FILE" | head -1 | jq -r '.timestamp // "unknown"' 2>/dev/null || echo "unknown")
END_TIME=$(grep '"session_end"' "$LOG_FILE" | tail -1 | jq -r '.timestamp // "unknown"' 2>/dev/null || echo "unknown")

# Total entries
TOTAL_ENTRIES=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")

# Tool call counts
TOOL_CALLS=$(grep -c '"tool_call_end"' "$LOG_FILE" 2>/dev/null || echo "0")
TOOL_ERRORS=$(grep -c '"tool_call_error"' "$LOG_FILE" 2>/dev/null || echo "0")

# Token counts (from last cumulative entry)
LAST_TOKEN_ENTRY=$(grep '"cumulative_tokens"' "$LOG_FILE" | tail -1 || echo "")
INPUT_TOKENS=0
OUTPUT_TOKENS=0

if [[ -n "$LAST_TOKEN_ENTRY" ]]; then
  INPUT_TOKENS=$(echo "$LAST_TOKEN_ENTRY" | jq -r '.cumulative_tokens.input // 0' 2>/dev/null || echo "0")
  OUTPUT_TOKENS=$(echo "$LAST_TOKEN_ENTRY" | jq -r '.cumulative_tokens.output // 0' 2>/dev/null || echo "0")
fi

TOTAL_TOKENS=$((INPUT_TOKENS + OUTPUT_TOKENS))

# Cost estimate
COST=$(echo "$INPUT_TOKENS * 0.000003 + $OUTPUT_TOKENS * 0.000015" | bc -l 2>/dev/null || echo "0")
COST_FMT=$(printf "%.4f" "$COST" 2>/dev/null || echo "$COST")

# Tool usage breakdown
TOOL_BREAKDOWN=$(grep '"tool_call_end"\|"tool_call_error"' "$LOG_FILE" | jq -r '.tool_name // "unknown"' 2>/dev/null | sort | uniq -c | sort -rn || echo "")

# Error breakdown
ERROR_MESSAGES=$(grep '"tool_call_error"' "$LOG_FILE" | jq -r '.message // "unknown error"' 2>/dev/null | sort | uniq -c | sort -rn | head -10 || echo "")

# Cost alerts
COST_ALERTS=$(grep -c '"cost_alert"' "$LOG_FILE" 2>/dev/null || echo "0")

# Stuck detections
STUCK_EVENTS=$(grep -c '"stuck_detected"' "$LOG_FILE" 2>/dev/null || echo "0")

# ── Generate report ──────────────────────────────────────────────────────

echo "============================================"
echo "  Agent Session Summary Report"
echo "============================================"
echo ""
echo "Session ID:    ${SESSION_ID}"
echo "Start:         ${START_TIME}"
echo "End:           ${END_TIME}"
echo "Log entries:   ${TOTAL_ENTRIES}"
echo ""
echo "── Tool Calls ──────────────────────────────"
echo "  Total calls: ${TOOL_CALLS}"
echo "  Errors:      ${TOOL_ERRORS}"
if [[ $TOOL_CALLS -gt 0 ]]; then
  ERROR_RATE=$(echo "scale=1; $TOOL_ERRORS * 100 / $TOOL_CALLS" | bc 2>/dev/null || echo "0")
  echo "  Error rate:  ${ERROR_RATE}%"
fi
echo ""
echo "── Tool Usage Breakdown ────────────────────"
if [[ -n "$TOOL_BREAKDOWN" ]]; then
  echo "$TOOL_BREAKDOWN" | while read -r count tool; do
    printf "  %-20s %s calls\n" "$tool" "$count"
  done
else
  echo "  No tool calls recorded"
fi
echo ""
echo "── Token Usage ─────────────────────────────"
echo "  Input tokens:  ${INPUT_TOKENS}"
echo "  Output tokens: ${OUTPUT_TOKENS}"
echo "  Total tokens:  ${TOTAL_TOKENS}"
echo "  Est. cost:     \$${COST_FMT}"
echo ""
echo "── Alerts ──────────────────────────────────"
echo "  Cost alerts:       ${COST_ALERTS}"
echo "  Stuck detections:  ${STUCK_EVENTS}"
echo ""

if [[ -n "$ERROR_MESSAGES" ]]; then
  echo "── Top Errors ──────────────────────────────"
  echo "$ERROR_MESSAGES" | while read -r count msg; do
    printf "  %3s  %s\n" "$count" "$msg"
  done
  echo ""
fi

echo "============================================"
echo "  Report generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "============================================"
