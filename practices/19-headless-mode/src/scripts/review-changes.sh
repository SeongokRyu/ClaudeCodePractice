#!/usr/bin/env bash
#
# review-changes.sh — Review changed files using Claude headless mode
#
# Usage:
#   bash review-changes.sh              # Review unstaged changes
#   bash review-changes.sh --staged     # Review staged changes
#   bash review-changes.sh --branch     # Review all changes on current branch vs main
#   bash review-changes.sh --json       # Output results as JSON
#

set -euo pipefail

# Configuration
MAX_FILES=20
OUTPUT_FORMAT="text"
DIFF_MODE="unstaged"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --staged)
      DIFF_MODE="staged"
      shift
      ;;
    --branch)
      DIFF_MODE="branch"
      shift
      ;;
    --json)
      OUTPUT_FORMAT="json"
      shift
      ;;
    --max-files)
      MAX_FILES="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: review-changes.sh [--staged|--branch] [--json] [--max-files N]"
      exit 1
      ;;
  esac
done

# Get changed files based on mode
get_changed_files() {
  case "$DIFF_MODE" in
    staged)
      git diff --cached --name-only
      ;;
    branch)
      local base_branch
      base_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
      git diff --name-only "${base_branch}...HEAD"
      ;;
    unstaged)
      git diff --name-only
      ;;
  esac
}

# Get diff for a specific file
get_file_diff() {
  local file="$1"
  case "$DIFF_MODE" in
    staged)
      git diff --cached -- "$file"
      ;;
    branch)
      local base_branch
      base_branch=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
      git diff "${base_branch}...HEAD" -- "$file"
      ;;
    unstaged)
      git diff -- "$file"
      ;;
  esac
}

# Main review logic
main() {
  echo "=== Code Review (${DIFF_MODE} changes) ==="
  echo ""

  local files
  files=$(get_changed_files)

  if [[ -z "$files" ]]; then
    echo "No changes found."
    exit 0
  fi

  local file_count
  file_count=$(echo "$files" | wc -l)
  echo "Found ${file_count} changed file(s)."

  if [[ $file_count -gt $MAX_FILES ]]; then
    echo "Warning: More than ${MAX_FILES} files changed. Reviewing first ${MAX_FILES} only."
    files=$(echo "$files" | head -n "$MAX_FILES")
  fi

  echo ""

  local review_results=""
  local file_num=0

  while IFS= read -r file; do
    file_num=$((file_num + 1))
    echo "[$file_num] Reviewing: $file"

    local diff
    diff=$(get_file_diff "$file")

    if [[ -z "$diff" ]]; then
      echo "  (no diff available, skipping)"
      continue
    fi

    local review
    review=$(echo "$diff" | claude -p "Review this git diff for the file '${file}'. Focus on:
1. Potential bugs or logic errors
2. Security concerns
3. Performance issues
4. Code style improvements

Be concise. If no issues found, say 'No issues found.'
Format each finding as: [SEVERITY] Description
Where SEVERITY is one of: CRITICAL, WARNING, INFO" \
      --allowedTools "" --max-turns 1 2>/dev/null || echo "Error: Failed to review this file.")

    if [[ "$OUTPUT_FORMAT" == "json" ]]; then
      # Escape for JSON
      local escaped_review
      escaped_review=$(echo "$review" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))')
      review_results="${review_results}{\"file\":\"${file}\",\"review\":${escaped_review}},"
    else
      echo "  $review"
      echo ""
    fi
  done <<< "$files"

  # Output summary
  if [[ "$OUTPUT_FORMAT" == "json" ]]; then
    # Remove trailing comma and wrap in array
    review_results="${review_results%,}"
    echo "[${review_results}]"
  else
    echo "=== Review Complete ==="
    echo "Reviewed ${file_num} file(s)."
  fi
}

main
