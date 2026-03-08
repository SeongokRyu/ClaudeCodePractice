#!/usr/bin/env bash
#
# batch-migrate.sh — Batch file migration using parallel Claude instances
#
# Usage:
#   bash batch-migrate.sh --pattern "src/legacy/*.ts" --transform "convert callbacks to async/await"
#   bash batch-migrate.sh --pattern "src/**/*.js" --transform "convert to TypeScript" --parallel 4
#   bash batch-migrate.sh --pattern "src/legacy/*.ts" --transform "add error handling" --dry-run
#

set -euo pipefail

# Configuration
FILE_PATTERN=""
TRANSFORM=""
PARALLEL=3
DRY_RUN=false
BACKUP_BRANCH=""
OUTPUT_DIR="/tmp/claude-migration-$$"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --pattern)
      FILE_PATTERN="$2"
      shift 2
      ;;
    --transform)
      TRANSFORM="$2"
      shift 2
      ;;
    --parallel|-P)
      PARALLEL="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --help)
      echo "Usage: batch-migrate.sh --pattern <glob> --transform <description> [--parallel N] [--dry-run]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

if [[ -z "$FILE_PATTERN" || -z "$TRANSFORM" ]]; then
  echo "Error: --pattern and --transform are required."
  echo "Usage: batch-migrate.sh --pattern <glob> --transform <description>"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "=== Batch Migration ==="
echo "Pattern:     $FILE_PATTERN"
echo "Transform:   $TRANSFORM"
echo "Parallelism: $PARALLEL"
echo "Dry run:     $DRY_RUN"
echo ""

# ─── Step 1: Discover files ───
echo "Step 1: Discovering files..."
FILES=$(eval ls -1 $FILE_PATTERN 2>/dev/null || true)

if [[ -z "$FILES" ]]; then
  echo "No files matched pattern: $FILE_PATTERN"
  exit 0
fi

FILE_COUNT=$(echo "$FILES" | wc -l)
echo "Found $FILE_COUNT file(s) to migrate."
echo ""

# ─── Step 2: Create backup branch ───
if [[ "$DRY_RUN" == false ]]; then
  echo "Step 2: Creating backup branch..."
  BACKUP_BRANCH="backup/pre-migration-$(date +%Y%m%d-%H%M%S)"
  if git rev-parse --git-dir > /dev/null 2>&1; then
    git checkout -b "$BACKUP_BRANCH" 2>/dev/null || true
    git checkout - 2>/dev/null || true
    echo "Backup branch: $BACKUP_BRANCH"
  else
    echo "Not in a git repo, skipping backup."
  fi
  echo ""
fi

# ─── Step 3: Analyze (dry run) or migrate files ───
migrate_file() {
  local file="$1"
  local transform="$2"
  local output_dir="$3"
  local dry_run="$4"
  local basename
  basename=$(basename "$file")
  local result_file="${output_dir}/${basename}.result.json"

  echo "[START] $file"

  if [[ "$dry_run" == true ]]; then
    # Dry run: analyze only, don't edit
    claude -p "Analyze this file and describe what changes would be needed to: ${transform}

File: $file

List the specific changes that would be made, without making them. Output as structured analysis." \
      --allowedTools Read,Grep \
      --max-turns 5 \
      --output-format json \
      > "$result_file" 2>/dev/null
  else
    # Real migration: read and edit the file
    claude -p "Migrate this file: ${transform}

File: $file

Rules:
1. Preserve the existing behavior exactly
2. Maintain all comments and documentation
3. Keep the same exports and public API
4. Add appropriate error handling if missing" \
      --allowedTools Read,Edit,Grep \
      --max-turns 10 \
      --output-format json \
      > "$result_file" 2>/dev/null
  fi

  local status=$?
  if [[ $status -eq 0 ]]; then
    echo "[DONE]  $file"
  else
    echo "[ERROR] $file (exit code: $status)"
  fi
}

export -f migrate_file

echo "Step 3: ${DRY_RUN:+Analyzing}${DRY_RUN:+Migrating} files ($PARALLEL workers)..."
echo ""

echo "$FILES" | xargs -P "$PARALLEL" -I {} bash -c \
  'migrate_file "$@"' _ {} "$TRANSFORM" "$OUTPUT_DIR" "$DRY_RUN"

echo ""

# ─── Step 4: Generate report ───
echo "Step 4: Generating report..."

REPORT_FILE="${OUTPUT_DIR}/migration-report.md"
{
  echo "# Migration Report"
  echo ""
  echo "**Date**: $(date)"
  echo "**Transform**: $TRANSFORM"
  echo "**Files processed**: $FILE_COUNT"
  echo "**Mode**: $(if [[ "$DRY_RUN" == true ]]; then echo "Dry Run"; else echo "Applied"; fi)"
  echo ""

  if [[ "$BACKUP_BRANCH" ]]; then
    echo "**Backup branch**: \`$BACKUP_BRANCH\`"
    echo ""
  fi

  echo "## Results"
  echo ""

  for result_file in "$OUTPUT_DIR"/*.result.json; do
    if [[ -f "$result_file" ]]; then
      local_basename=$(basename "$result_file" .result.json)
      echo "### $local_basename"
      echo ""
      jq -r '.result // .error // "No output"' "$result_file" 2>/dev/null || echo "(parse error)"
      echo ""
    fi
  done
} > "$REPORT_FILE"

echo "Report saved to: $REPORT_FILE"
echo ""

# ─── Summary ───
echo "=== Migration Complete ==="
echo ""
echo "Results: $OUTPUT_DIR/"
echo "Report:  $REPORT_FILE"

if [[ "$DRY_RUN" == true ]]; then
  echo ""
  echo "This was a dry run. To apply changes:"
  echo "  bash $0 --pattern \"$FILE_PATTERN\" --transform \"$TRANSFORM\" --parallel $PARALLEL"
else
  echo ""
  echo "To revert all changes:"
  if [[ "$BACKUP_BRANCH" ]]; then
    echo "  git checkout $BACKUP_BRANCH -- ."
  else
    echo "  git checkout -- ."
  fi
fi
