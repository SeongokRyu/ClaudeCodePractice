#!/usr/bin/env bash
#
# auto-commit.sh — Generate commit messages using Claude headless mode
#
# Usage:
#   source auto-commit.sh   # Load the function
#   auto_commit              # Generate and commit with AI message
#   auto_commit --dry-run    # Preview the message without committing
#

set -euo pipefail

auto_commit() {
  local dry_run=false

  if [[ "${1:-}" == "--dry-run" ]]; then
    dry_run=true
  fi

  # Check for staged changes
  if ! git diff --cached --quiet 2>/dev/null; then
    echo "Generating commit message from staged changes..."
  else
    echo "Error: No staged changes found."
    echo "Stage your changes first: git add <files>"
    return 1
  fi

  # Get the staged diff
  local diff
  diff=$(git diff --cached --stat && echo "---" && git diff --cached)

  # Generate commit message using Claude headless mode
  local message
  message=$(echo "$diff" | claude -p "Based on this git diff, generate a concise commit message following the Conventional Commits format (e.g., feat:, fix:, refactor:, docs:, test:, chore:). Include a brief body if the change is non-trivial. Output ONLY the commit message, nothing else." --allowedTools "" --max-turns 1 2>/dev/null)

  if [[ -z "$message" ]]; then
    echo "Error: Failed to generate commit message."
    return 1
  fi

  echo ""
  echo "Generated commit message:"
  echo "─────────────────────────"
  echo "$message"
  echo "─────────────────────────"

  if [[ "$dry_run" == true ]]; then
    echo ""
    echo "(dry run — no commit created)"
    return 0
  fi

  # Confirm and commit
  echo ""
  read -p "Commit with this message? [Y/n/e(dit)] " -r response
  case "$response" in
    [nN])
      echo "Commit cancelled."
      return 0
      ;;
    [eE])
      # Open in editor for manual adjustment
      local tmpfile
      tmpfile=$(mktemp)
      echo "$message" > "$tmpfile"
      ${EDITOR:-vim} "$tmpfile"
      message=$(cat "$tmpfile")
      rm "$tmpfile"
      ;;
    *)
      # Accept as-is
      ;;
  esac

  git commit -m "$message"
  echo "Committed successfully."
}

# If script is run directly (not sourced), execute auto_commit
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  auto_commit "$@"
fi
