#!/usr/bin/env bash
# notify-completion.sh — PostToolUse hook that sends desktop notification on task completion
#
# This hook detects when Claude signals task completion and sends a desktop
# notification so you know work is done (useful for long-running headless tasks).
#
# Always exits 0 — notifications should never block work.
#
# Input: JSON on stdin with tool_name, tool_input, and tool_output fields

set -uo pipefail

# ── Read input ────────────────────────────────────────────────────────────
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
TOOL_OUTPUT=$(echo "$INPUT" | jq -r '.tool_output // empty' 2>/dev/null || echo "")

# ── Detect completion signals ─────────────────────────────────────────────
# Look for patterns that indicate a task is done
COMPLETION_PATTERNS=(
  "task.*complete"
  "successfully.*created"
  "all.*tests.*pass"
  "build.*succeeded"
  "deployment.*complete"
  "done"
)

IS_COMPLETE=false

for pattern in "${COMPLETION_PATTERNS[@]}"; do
  if echo "$TOOL_OUTPUT" | grep -qiE "$pattern"; then
    IS_COMPLETE=true
    break
  fi
done

if [[ "$IS_COMPLETE" != "true" ]]; then
  exit 0
fi

# ── Send notification ─────────────────────────────────────────────────────
TITLE="Claude Code: Task Complete"
MESSAGE="Tool '${TOOL_NAME}' completed successfully."

# macOS
if command -v osascript &>/dev/null; then
  osascript -e "display notification \"${MESSAGE}\" with title \"${TITLE}\"" 2>/dev/null || true
fi

# Linux (notify-send)
if command -v notify-send &>/dev/null; then
  notify-send "${TITLE}" "${MESSAGE}" 2>/dev/null || true
fi

# Fallback: terminal bell
echo -ne '\a' >&2

echo "Notification sent: ${MESSAGE}" >&2

exit 0
