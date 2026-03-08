#!/usr/bin/env bash
# auto-format.sh — PostToolUse hook that runs prettier after file edits
#
# This hook always exits 0 (formatting failures should not block work).
# Formatting results are logged to stderr for debugging.
#
# Input: JSON on stdin with tool_name and tool_input fields
# Example: {"tool_name":"Edit","tool_input":{"file_path":"src/app.ts",...}}

set -uo pipefail

# ── Supported file extensions ─────────────────────────────────────────────
SUPPORTED_EXTENSIONS="ts|js|tsx|jsx|json|css|scss|less|md|yaml|yml|html"

# ── Read input ────────────────────────────────────────────────────────────
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# Only run after Edit or Write tools
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
  exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

# ── Check file extension ─────────────────────────────────────────────────
EXTENSION="${FILE_PATH##*.}"

if ! echo "$EXTENSION" | grep -qiE "^($SUPPORTED_EXTENSIONS)$"; then
  echo "Skipping prettier: unsupported extension '.${EXTENSION}'" >&2
  exit 0
fi

# ── Check if file exists ─────────────────────────────────────────────────
if [[ ! -f "$FILE_PATH" ]]; then
  echo "Skipping prettier: file not found '${FILE_PATH}'" >&2
  exit 0
fi

# ── Check if prettier is available ────────────────────────────────────────
if ! command -v npx &>/dev/null; then
  echo "Skipping prettier: npx not found" >&2
  exit 0
fi

# ── Run prettier ──────────────────────────────────────────────────────────
echo "Running prettier on ${FILE_PATH}..." >&2

if npx prettier --write "$FILE_PATH" 2>&1 >&2; then
  echo "Formatted: ${FILE_PATH}" >&2
else
  echo "Prettier failed for ${FILE_PATH} (non-blocking)" >&2
fi

# Always exit 0 — formatting should not block the tool
exit 0
