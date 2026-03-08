#!/bin/bash
#
# PostToolUse Hook: Auto-format files after Edit or Write
#
# This hook runs AFTER Edit or Write tool calls complete.
# It formats the edited file using Prettier (if available).
#
# Exit code does not matter for PostToolUse hooks (they cannot block).
#
# Input: JSON on stdin with tool_name, tool_input, and tool_output
#

# Read the JSON input from stdin
INPUT=$(cat)

# Extract the file path from tool_input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

# Only format if the file exists
if [ ! -f "$FILE_PATH" ]; then
  exit 0
fi

# Determine the file extension
EXT="${FILE_PATH##*.}"

# Only format supported file types
case "$EXT" in
  ts|tsx|js|jsx|json|css|scss|html|md|yaml|yml)
    # Try Prettier first (most common formatter)
    if command -v npx &> /dev/null && [ -f "node_modules/.bin/prettier" ]; then
      npx prettier --write "$FILE_PATH" 2>/dev/null
    elif command -v prettier &> /dev/null; then
      prettier --write "$FILE_PATH" 2>/dev/null
    fi
    ;;
  py)
    # Python: try Black, then autopep8
    if command -v black &> /dev/null; then
      black --quiet "$FILE_PATH" 2>/dev/null
    elif command -v autopep8 &> /dev/null; then
      autopep8 --in-place "$FILE_PATH" 2>/dev/null
    fi
    ;;
  go)
    # Go: use gofmt
    if command -v gofmt &> /dev/null; then
      gofmt -w "$FILE_PATH" 2>/dev/null
    fi
    ;;
  rs)
    # Rust: use rustfmt
    if command -v rustfmt &> /dev/null; then
      rustfmt "$FILE_PATH" 2>/dev/null
    fi
    ;;
esac

exit 0
