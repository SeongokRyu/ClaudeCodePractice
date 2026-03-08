#!/usr/bin/env bash
# auto-lint.sh — PostToolUse hook that runs eslint after TypeScript file edits
#
# This hook always exits 0 — linting is advisory, not blocking.
# Lint results are logged to stderr for visibility.
#
# Input: JSON on stdin with tool_name and tool_input fields
# Example: {"tool_name":"Edit","tool_input":{"file_path":"src/app.ts",...}}

set -uo pipefail

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

# ── Check if it's a TypeScript file ───────────────────────────────────────
EXTENSION="${FILE_PATH##*.}"

if [[ "$EXTENSION" != "ts" && "$EXTENSION" != "tsx" ]]; then
  exit 0
fi

# ── Check if file exists ─────────────────────────────────────────────────
if [[ ! -f "$FILE_PATH" ]]; then
  echo "Skipping eslint: file not found '${FILE_PATH}'" >&2
  exit 0
fi

# ── Check if eslint is available ──────────────────────────────────────────
if ! command -v npx &>/dev/null; then
  echo "Skipping eslint: npx not found" >&2
  exit 0
fi

# ── Run eslint with auto-fix ──────────────────────────────────────────────
echo "Running eslint on ${FILE_PATH}..." >&2

LINT_OUTPUT=$(npx eslint --fix "$FILE_PATH" 2>&1) || true

if [[ -n "$LINT_OUTPUT" ]]; then
  echo "ESLint results for ${FILE_PATH}:" >&2
  echo "$LINT_OUTPUT" >&2
else
  echo "ESLint: no issues in ${FILE_PATH}" >&2
fi

# Always exit 0 — linting is advisory
exit 0
