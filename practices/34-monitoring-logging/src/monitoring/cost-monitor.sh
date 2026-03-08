#!/usr/bin/env bash
# cost-monitor.sh — Monitor agent session cost and alert if over budget
#
# Reads structured log entries and tracks cumulative cost.
# Alerts at configurable thresholds (50%, 75%, 90%, 100%).
#
# Usage:
#   bash cost-monitor.sh <log-file> [--budget <usd>] [--interval <seconds>]
#
# Example:
#   bash cost-monitor.sh session.log --budget 1.00 --interval 5

set -uo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────
LOG_FILE="${1:-}"
BUDGET_USD="1.00"
INTERVAL=5

# ── Parse arguments ──────────────────────────────────────────────────────
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --budget)
      BUDGET_USD="$2"
      shift 2
      ;;
    --interval)
      INTERVAL="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

if [[ -z "$LOG_FILE" ]]; then
  echo "Usage: bash cost-monitor.sh <log-file> [--budget <usd>] [--interval <seconds>]"
  exit 1
fi

# ── Pricing (Claude Sonnet) ──────────────────────────────────────────────
COST_PER_INPUT_TOKEN="0.000003"    # $3 per 1M tokens
COST_PER_OUTPUT_TOKEN="0.000015"   # $15 per 1M tokens

# ── Alert state ───────────────────────────────────────────────────────────
ALERTED_50=false
ALERTED_75=false
ALERTED_90=false
ALERTED_100=false

alert() {
  local level="$1"
  local message="$2"
  local timestamp
  timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  echo "[${timestamp}] [COST ${level}] ${message}"

  # Desktop notification
  if command -v notify-send &>/dev/null; then
    notify-send "Cost ${level}" "${message}" 2>/dev/null || true
  fi
}

# ── Monitor loop ─────────────────────────────────────────────────────────
echo "Cost Monitor Started"
echo "  Log file: ${LOG_FILE}"
echo "  Budget:   \$${BUDGET_USD}"
echo "  Interval: ${INTERVAL}s"
echo "  Pricing:  \$${COST_PER_INPUT_TOKEN}/input token, \$${COST_PER_OUTPUT_TOKEN}/output token"
echo ""

LAST_LINE_COUNT=0

while true; do
  if [[ ! -f "$LOG_FILE" ]]; then
    sleep "$INTERVAL"
    continue
  fi

  # Count current lines
  CURRENT_LINE_COUNT=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")

  # Skip if no new data
  if [[ "$CURRENT_LINE_COUNT" -eq "$LAST_LINE_COUNT" ]]; then
    sleep "$INTERVAL"
    continue
  fi

  LAST_LINE_COUNT=$CURRENT_LINE_COUNT

  # Extract cumulative tokens from last entry with cumulative_tokens
  LAST_ENTRY=$(grep '"cumulative_tokens"' "$LOG_FILE" | tail -1 || echo "")

  if [[ -z "$LAST_ENTRY" ]]; then
    sleep "$INTERVAL"
    continue
  fi

  INPUT_TOKENS=$(echo "$LAST_ENTRY" | jq -r '.cumulative_tokens.input // 0' 2>/dev/null || echo "0")
  OUTPUT_TOKENS=$(echo "$LAST_ENTRY" | jq -r '.cumulative_tokens.output // 0' 2>/dev/null || echo "0")

  # Calculate cost
  COST=$(echo "$INPUT_TOKENS * $COST_PER_INPUT_TOKEN + $OUTPUT_TOKENS * $COST_PER_OUTPUT_TOKEN" | bc -l 2>/dev/null || echo "0")
  PERCENTAGE=$(echo "$COST / $BUDGET_USD * 100" | bc -l 2>/dev/null || echo "0")

  # Format for display
  COST_FMT=$(printf "%.4f" "$COST" 2>/dev/null || echo "$COST")
  PCT_FMT=$(printf "%.1f" "$PERCENTAGE" 2>/dev/null || echo "$PERCENTAGE")

  echo "[$(date -u +%H:%M:%S)] Tokens: ${INPUT_TOKENS}in/${OUTPUT_TOKENS}out | Cost: \$${COST_FMT} | Budget: ${PCT_FMT}%"

  # ── Check thresholds ────────────────────────────────────────────────
  PCT_INT=$(printf "%.0f" "$PERCENTAGE" 2>/dev/null || echo "0")

  if [[ $PCT_INT -ge 100 && "$ALERTED_100" != "true" ]]; then
    alert "CRITICAL" "Budget exceeded! \$${COST_FMT} >= \$${BUDGET_USD} (${PCT_FMT}%)"
    ALERTED_100=true
    # In production, you might want to kill the session here
    echo "WARNING: Budget exceeded. Consider stopping the session."
  elif [[ $PCT_INT -ge 90 && "$ALERTED_90" != "true" ]]; then
    alert "WARNING" "90% of budget used: \$${COST_FMT} / \$${BUDGET_USD}"
    ALERTED_90=true
  elif [[ $PCT_INT -ge 75 && "$ALERTED_75" != "true" ]]; then
    alert "WARNING" "75% of budget used: \$${COST_FMT} / \$${BUDGET_USD}"
    ALERTED_75=true
  elif [[ $PCT_INT -ge 50 && "$ALERTED_50" != "true" ]]; then
    alert "INFO" "50% of budget used: \$${COST_FMT} / \$${BUDGET_USD}"
    ALERTED_50=true
  fi

  # Check for session end
  if grep -q '"session_end"' "$LOG_FILE"; then
    echo ""
    echo "Session ended. Final cost: \$${COST_FMT} (${PCT_FMT}% of budget)"
    break
  fi

  sleep "$INTERVAL"
done
