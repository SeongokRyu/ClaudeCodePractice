#!/bin/bash
#
# PreToolUse Hook: Protect sensitive files from being edited
#
# This hook runs BEFORE Edit or Write tool calls.
# Exit 0 = allow the edit
# Exit 2 = block the edit (stderr message is shown to Claude)
#
# Input: JSON on stdin with tool_name and tool_input
#

# Read the JSON input from stdin
INPUT=$(cat)

# Extract the file path from tool_input
# Works for both Edit (file_path) and Write (file_path) tools
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  # No file path found — allow (might be a different tool input format)
  exit 0
fi

# Define protected file patterns
PROTECTED_PATTERNS=(
  "*.env"
  "*.env.*"
  ".env"
  ".env.local"
  ".env.production"
  ".env.staging"
)

# Get the basename of the file
BASENAME=$(basename "$FILE_PATH")

# Check against protected patterns
for PATTERN in "${PROTECTED_PATTERNS[@]}"; do
  case "$BASENAME" in
    $PATTERN)
      echo "BLOCKED: Cannot edit '$FILE_PATH' — .env files are protected." >&2
      echo "Environment files contain secrets and should be edited manually." >&2
      exit 2
      ;;
  esac
done

# Check if file is in a protected directory
case "$FILE_PATH" in
  */generated/*)
    echo "BLOCKED: Cannot edit '$FILE_PATH' — files in generated/ are auto-generated." >&2
    exit 2
    ;;
esac

# Allow all other files
exit 0
