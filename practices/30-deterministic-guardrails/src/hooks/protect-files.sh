#!/usr/bin/env bash
# protect-files.sh — PreToolUse hook that blocks edits to protected files
#
# Exit codes:
#   0 = allow the tool call
#   2 = block the tool call (with message on stdout)
#
# Input: JSON on stdin with tool_name and tool_input fields
# Example: {"tool_name":"Edit","tool_input":{"file_path":".env","old_string":"...","new_string":"..."}}

set -euo pipefail

# ── Configurable protected paths ──────────────────────────────────────────
# Add patterns here. Supports exact matches and prefix matches (directories).
PROTECTED_PATTERNS=(
  ".env"
  ".env.*"
  "package-lock.json"
  "migrations/"
  "*.pem"
  "*.key"
  "secrets/"
)

# ── Read input ────────────────────────────────────────────────────────────
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')

# If no file path found, allow (not a file operation we care about)
if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# Normalize: remove leading ./ if present
FILE_PATH="${FILE_PATH#./}"

# ── Check against protected patterns ──────────────────────────────────────
for pattern in "${PROTECTED_PATTERNS[@]}"; do
  # Directory prefix match (pattern ends with /)
  if [[ "$pattern" == */ ]]; then
    if [[ "$FILE_PATH" == ${pattern}* ]]; then
      echo "BLOCKED: Cannot edit files in protected directory '${pattern}'"
      echo "File '${FILE_PATH}' is in a protected directory."
      echo "To modify this file, remove it from the protected list in protect-files.sh."
      exit 2
    fi
  # Glob pattern match
  elif [[ "$FILE_PATH" == $pattern ]]; then
    echo "BLOCKED: Cannot edit protected file '${FILE_PATH}'"
    echo "This file matches protected pattern '${pattern}'."
    echo "To modify this file, remove it from the protected list in protect-files.sh."
    exit 2
  fi

  # Also check basename for patterns without path separators
  BASENAME=$(basename "$FILE_PATH")
  if [[ "$pattern" != */ && "$BASENAME" == $pattern ]]; then
    echo "BLOCKED: Cannot edit protected file '${FILE_PATH}'"
    echo "Basename '${BASENAME}' matches protected pattern '${pattern}'."
    exit 2
  fi
done

# ── Not protected — allow ─────────────────────────────────────────────────
exit 0
