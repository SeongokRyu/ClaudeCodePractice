#!/usr/bin/env bash
# stuck-detector.sh — Detect if an agent is stuck in a loop
#
# Monitors agent log entries and detects:
# - Repeated identical tool calls
# - Edit-undo-edit cycles
# - No progress after N iterations
#
# Usage:
#   bash stuck-detector.sh <log-file> [--threshold <count>] [--interval <seconds>]
#
# Example:
#   bash stuck-detector.sh session.log --threshold 5 --interval 10

set -uo pipefail

# ── Defaults ──────────────────────────────────────────────────────────────
LOG_FILE="${1:-}"
REPEAT_THRESHOLD=5      # Alert after this many repeated identical calls
CYCLE_THRESHOLD=3       # Alert after this many A-B-A-B cycles
INTERVAL=10             # Check interval in seconds
NO_PROGRESS_TIMEOUT=120 # Alert if no new log entries for this many seconds

# ── Parse arguments ──────────────────────────────────────────────────────
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --threshold)
      REPEAT_THRESHOLD="$2"
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
  echo "Usage: bash stuck-detector.sh <log-file> [--threshold <count>] [--interval <seconds>]"
  exit 1
fi

echo "Stuck Detector Started"
echo "  Log file: ${LOG_FILE}"
echo "  Repeat threshold: ${REPEAT_THRESHOLD}"
echo "  Cycle threshold: ${CYCLE_THRESHOLD}"
echo "  Check interval: ${INTERVAL}s"
echo ""

# ── State ─────────────────────────────────────────────────────────────────
LAST_LINE_COUNT=0
LAST_ACTIVITY_TIME=$(date +%s)
STUCK_ALERTED=false

# ── Helper functions ──────────────────────────────────────────────────────

check_repeated_calls() {
  local log_file="$1"

  # Get last N tool calls
  local recent_calls
  recent_calls=$(grep '"tool_call_end"' "$log_file" | tail -"$REPEAT_THRESHOLD" | jq -r '.tool_name' 2>/dev/null || echo "")

  if [[ -z "$recent_calls" ]]; then
    return 1
  fi

  # Check if all recent calls are identical
  local unique_count
  unique_count=$(echo "$recent_calls" | sort -u | wc -l)

  if [[ $unique_count -eq 1 ]]; then
    local tool_name
    tool_name=$(echo "$recent_calls" | head -1)
    echo "REPEATED: Tool '${tool_name}' called ${REPEAT_THRESHOLD} times consecutively"
    return 0
  fi

  return 1
}

check_cycles() {
  local log_file="$1"

  # Get recent tool call sequence
  local recent_calls
  recent_calls=$(grep '"tool_call_end"' "$log_file" | tail -$((CYCLE_THRESHOLD * 2 + 2)) | jq -r '.tool_name' 2>/dev/null || echo "")

  if [[ -z "$recent_calls" ]]; then
    return 1
  fi

  local calls_array=()
  while IFS= read -r line; do
    calls_array+=("$line")
  done <<< "$recent_calls"

  local len=${#calls_array[@]}
  if [[ $len -lt 4 ]]; then
    return 1
  fi

  # Check for A-B-A-B pattern
  local a="${calls_array[$((len-1))]}"
  local b="${calls_array[$((len-2))]}"

  if [[ "$a" == "$b" ]]; then
    return 1
  fi

  local cycle_count=0
  for ((i=len-1; i>=1; i-=2)); do
    if [[ "${calls_array[$i]}" == "$a" && "${calls_array[$((i-1))]}" == "$b" ]]; then
      cycle_count=$((cycle_count + 1))
    else
      break
    fi
  done

  if [[ $cycle_count -ge $CYCLE_THRESHOLD ]]; then
    echo "CYCLE: ${a} <-> ${b} repeated ${cycle_count} times"
    return 0
  fi

  return 1
}

check_no_progress() {
  local log_file="$1"
  local current_time
  current_time=$(date +%s)
  local elapsed=$((current_time - LAST_ACTIVITY_TIME))

  if [[ $elapsed -ge $NO_PROGRESS_TIMEOUT ]]; then
    echo "STALLED: No new log entries for ${elapsed}s"
    return 0
  fi

  return 1
}

# ── Monitor loop ─────────────────────────────────────────────────────────

while true; do
  if [[ ! -f "$LOG_FILE" ]]; then
    sleep "$INTERVAL"
    continue
  fi

  # Check for new activity
  CURRENT_LINE_COUNT=$(wc -l < "$LOG_FILE" 2>/dev/null || echo "0")

  if [[ "$CURRENT_LINE_COUNT" -ne "$LAST_LINE_COUNT" ]]; then
    LAST_LINE_COUNT=$CURRENT_LINE_COUNT
    LAST_ACTIVITY_TIME=$(date +%s)
    STUCK_ALERTED=false
  fi

  # Run checks
  STUCK_REASON=""

  if RESULT=$(check_repeated_calls "$LOG_FILE"); then
    STUCK_REASON="$RESULT"
  elif RESULT=$(check_cycles "$LOG_FILE"); then
    STUCK_REASON="$RESULT"
  elif RESULT=$(check_no_progress "$LOG_FILE"); then
    STUCK_REASON="$RESULT"
  fi

  if [[ -n "$STUCK_REASON" && "$STUCK_ALERTED" != "true" ]]; then
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo ""
    echo "[${TIMESTAMP}] STUCK DETECTED: ${STUCK_REASON}"
    echo "  Recommendation: Consider interrupting the session and reprompting."
    echo ""

    # Desktop notification
    if command -v notify-send &>/dev/null; then
      notify-send "Agent Stuck" "${STUCK_REASON}" 2>/dev/null || true
    fi

    STUCK_ALERTED=true
  fi

  # Check for session end
  if grep -q '"session_end"' "$LOG_FILE" 2>/dev/null; then
    echo "Session ended. Stopping stuck detector."
    break
  fi

  sleep "$INTERVAL"
done
