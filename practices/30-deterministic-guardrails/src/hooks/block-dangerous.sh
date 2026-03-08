#!/usr/bin/env bash
# block-dangerous.sh — PreToolUse hook that blocks dangerous bash commands
#
# Exit codes:
#   0 = allow the command
#   2 = block the command (with message on stdout)
#
# Input: JSON on stdin with tool_name and tool_input fields
# Example: {"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}

set -euo pipefail

# ── Read input ────────────────────────────────────────────────────────────
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only check Bash tool calls
if [[ "$TOOL_NAME" != "Bash" ]]; then
  exit 0
fi

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [[ -z "$COMMAND" ]]; then
  exit 0
fi

# ── Dangerous patterns ───────────────────────────────────────────────────
# Each entry: pattern|description
DANGEROUS_PATTERNS=(
  'rm\s+-r[f]*\s+/|Recursive deletion from root directory'
  'rm\s+-[a-z]*f[a-z]*\s+/|Forced recursive deletion from root'
  'rm\s+-rf\s+~|Recursive deletion of home directory'
  'rm\s+-rf\s+\.\s|Recursive deletion of current directory'
  'git\s+push\s+.*--force|Force push (can destroy remote history)'
  'git\s+push\s+-f|Force push (shorthand, can destroy remote history)'
  'git\s+reset\s+--hard\s+origin|Hard reset to remote (destroys local changes)'
  'DROP\s+TABLE|SQL DROP TABLE (destructive database operation)'
  'DROP\s+DATABASE|SQL DROP DATABASE (destructive database operation)'
  'TRUNCATE\s+TABLE|SQL TRUNCATE TABLE (destructive database operation)'
  'chmod\s+777|Insecure permissions (world-writable)'
  'chmod\s+-R\s+777|Recursive insecure permissions'
  'curl\s+.*\|\s*sh|Piping remote content to shell (unsafe)'
  'curl\s+.*\|\s*bash|Piping remote content to bash (unsafe)'
  'wget\s+.*\|\s*sh|Piping remote content to shell (unsafe)'
  'wget\s+.*\|\s*bash|Piping remote content to bash (unsafe)'
  'mkfs\.|Formatting a filesystem'
  'dd\s+if=.*of=/dev/|Writing directly to a device'
  '>\s*/dev/sd|Writing directly to a block device'
  'shutdown|System shutdown command'
  'reboot|System reboot command'
  'init\s+0|System halt'
)

# ── Check command against patterns ────────────────────────────────────────
for entry in "${DANGEROUS_PATTERNS[@]}"; do
  pattern="${entry%%|*}"
  description="${entry#*|}"

  if echo "$COMMAND" | grep -qiE "$pattern"; then
    echo "BLOCKED: Dangerous command detected"
    echo ""
    echo "Pattern matched: ${description}"
    echo "Command: ${COMMAND}"
    echo ""
    echo "If you believe this is a false positive, review the command carefully"
    echo "and modify block-dangerous.sh to adjust the pattern."
    exit 2
  fi
done

# ── No dangerous patterns found — allow ───────────────────────────────────
exit 0
