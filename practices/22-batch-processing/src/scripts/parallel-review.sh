#!/usr/bin/env bash
#
# parallel-review.sh — Review multiple files in parallel using Claude
#
# Usage:
#   bash parallel-review.sh src/              # Review all .ts files in src/
#   bash parallel-review.sh src/ --parallel 4  # Use 4 parallel workers
#   bash parallel-review.sh src/ --json        # Output JSON results
#

set -euo pipefail

# Configuration
TARGET_DIR="${1:-.}"
PARALLEL=3
OUTPUT_DIR="/tmp/claude-reviews-$$"
OUTPUT_FORMAT="text"

# Parse arguments
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --parallel|-P)
      PARALLEL="$2"
      shift 2
      ;;
    --json)
      OUTPUT_FORMAT="json"
      shift
      ;;
    --output-dir)
      OUTPUT_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

mkdir -p "$OUTPUT_DIR"

echo "=== Parallel Code Review ==="
echo "Target: $TARGET_DIR"
echo "Parallelism: $PARALLEL"
echo "Output: $OUTPUT_DIR"
echo ""

# Find all TypeScript files
FILES=$(find "$TARGET_DIR" -name "*.ts" -not -name "*.test.ts" -not -name "*.d.ts" -not -path "*/node_modules/*" -type f)

if [[ -z "$FILES" ]]; then
  echo "No .ts files found in $TARGET_DIR"
  exit 0
fi

FILE_COUNT=$(echo "$FILES" | wc -l)
echo "Found $FILE_COUNT file(s) to review."
echo "Starting parallel review with $PARALLEL workers..."
echo ""

# Review function for each file
review_file() {
  local file="$1"
  local output_dir="$2"
  local basename
  basename=$(basename "$file" .ts)
  local output_file="${output_dir}/${basename}.json"

  echo "[START] $file"

  claude -p "Review this TypeScript file for:
1. Potential bugs or logic errors
2. Security concerns
3. Performance issues
4. Code quality improvements

File: $file

Output your review as a structured analysis with severity levels (CRITICAL, WARNING, INFO) for each finding." \
    --allowedTools Read,Grep \
    --max-turns 5 \
    --output-format json \
    > "$output_file" 2>/dev/null

  local status=$?

  if [[ $status -eq 0 ]]; then
    echo "[DONE]  $file -> $output_file"
  else
    echo "[ERROR] $file (exit code: $status)"
    echo "{\"error\": \"Review failed with exit code $status\", \"file\": \"$file\"}" > "$output_file"
  fi
}

export -f review_file

# Fan out reviews in parallel
echo "$FILES" | xargs -P "$PARALLEL" -I {} bash -c 'review_file "$@"' _ {} "$OUTPUT_DIR"

echo ""
echo "=== Review Complete ==="
echo "Results saved to: $OUTPUT_DIR/"
echo ""

# Quick summary
RESULT_COUNT=$(ls -1 "$OUTPUT_DIR"/*.json 2>/dev/null | wc -l)
echo "Generated $RESULT_COUNT review file(s)."
echo ""
echo "To aggregate results:"
echo "  bash src/scripts/aggregate-results.sh $OUTPUT_DIR/*.json"
