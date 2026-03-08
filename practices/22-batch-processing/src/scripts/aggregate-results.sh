#!/usr/bin/env bash
#
# aggregate-results.sh — Combine JSON results from parallel Claude runs
#
# Usage:
#   bash aggregate-results.sh /tmp/review-*.json
#   bash aggregate-results.sh --format markdown /tmp/review-*.json
#   bash aggregate-results.sh --format json /tmp/review-*.json
#

set -euo pipefail

# Configuration
FORMAT="text"
OUTPUT_FILE=""

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)
      FORMAT="$2"
      shift 2
      ;;
    --output|-o)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    *)
      POSITIONAL_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#POSITIONAL_ARGS[@]} -eq 0 ]]; then
  echo "Usage: aggregate-results.sh [--format text|json|markdown] <result-files...>"
  exit 1
fi

# Collect all result files
RESULT_FILES=("${POSITIONAL_ARGS[@]}")
TOTAL_FILES=${#RESULT_FILES[@]}

echo "=== Aggregating Results ===" >&2
echo "Files: $TOTAL_FILES" >&2
echo "Format: $FORMAT" >&2
echo "" >&2

# Aggregate based on format
aggregate_text() {
  echo "═══════════════════════════════════════"
  echo "  Aggregated Review Report"
  echo "  $(date)"
  echo "  Files reviewed: $TOTAL_FILES"
  echo "═══════════════════════════════════════"
  echo ""

  local file_num=0
  local total_cost=0

  for result_file in "${RESULT_FILES[@]}"; do
    file_num=$((file_num + 1))
    local basename
    basename=$(basename "$result_file" .json)

    echo "──── [$file_num/$TOTAL_FILES] $basename ────"
    echo ""

    if [[ -f "$result_file" ]]; then
      # Extract result text
      local result
      result=$(jq -r '.result // "No result"' "$result_file" 2>/dev/null || echo "(failed to parse)")
      echo "$result"

      # Track cost if available
      local cost
      cost=$(jq -r '.cost_usd // 0' "$result_file" 2>/dev/null || echo "0")
      total_cost=$(echo "$total_cost + $cost" | bc 2>/dev/null || echo "$total_cost")
    else
      echo "(file not found)"
    fi

    echo ""
  done

  echo "═══════════════════════════════════════"
  echo "  Summary"
  echo "  Total files: $TOTAL_FILES"
  echo "  Total cost:  \$${total_cost}"
  echo "═══════════════════════════════════════"
}

aggregate_json() {
  # Combine all JSON results into a single array
  python3 -c "
import json, sys, os

results = []
total_cost = 0

for filepath in sys.argv[1:]:
    basename = os.path.basename(filepath).replace('.json', '')
    try:
        with open(filepath) as f:
            data = json.load(f)
        results.append({
            'file': basename,
            'result': data.get('result', ''),
            'cost_usd': data.get('cost_usd', 0),
            'model': data.get('model', 'unknown'),
            'status': 'success'
        })
        total_cost += data.get('cost_usd', 0)
    except Exception as e:
        results.append({
            'file': basename,
            'error': str(e),
            'status': 'error'
        })

output = {
    'summary': {
        'total_files': len(results),
        'successful': len([r for r in results if r['status'] == 'success']),
        'failed': len([r for r in results if r['status'] == 'error']),
        'total_cost_usd': round(total_cost, 4),
        'generated_at': '$(date -Iseconds)'
    },
    'results': results
}

print(json.dumps(output, indent=2))
" "${RESULT_FILES[@]}"
}

aggregate_markdown() {
  echo "# Code Review Report"
  echo ""
  echo "**Date**: $(date)"
  echo "**Files reviewed**: $TOTAL_FILES"
  echo ""
  echo "---"
  echo ""

  local file_num=0

  for result_file in "${RESULT_FILES[@]}"; do
    file_num=$((file_num + 1))
    local basename
    basename=$(basename "$result_file" .json)

    echo "## $file_num. $basename"
    echo ""

    if [[ -f "$result_file" ]]; then
      local result
      result=$(jq -r '.result // "No result"' "$result_file" 2>/dev/null || echo "(failed to parse)")
      echo "$result"
      echo ""

      local cost
      cost=$(jq -r '.cost_usd // "N/A"' "$result_file" 2>/dev/null || echo "N/A")
      echo "*Cost: \$$cost*"
    else
      echo "(result file not found)"
    fi

    echo ""
    echo "---"
    echo ""
  done

  echo "## Summary"
  echo ""
  echo "| Metric | Value |"
  echo "|--------|-------|"
  echo "| Files reviewed | $TOTAL_FILES |"
  echo "| Format | $FORMAT |"
  echo "| Generated | $(date) |"
}

# Execute aggregation
case "$FORMAT" in
  text)
    if [[ -n "$OUTPUT_FILE" ]]; then
      aggregate_text > "$OUTPUT_FILE"
      echo "Report saved to: $OUTPUT_FILE" >&2
    else
      aggregate_text
    fi
    ;;
  json)
    if [[ -n "$OUTPUT_FILE" ]]; then
      aggregate_json > "$OUTPUT_FILE"
      echo "Report saved to: $OUTPUT_FILE" >&2
    else
      aggregate_json
    fi
    ;;
  markdown)
    if [[ -n "$OUTPUT_FILE" ]]; then
      aggregate_markdown > "$OUTPUT_FILE"
      echo "Report saved to: $OUTPUT_FILE" >&2
    else
      aggregate_markdown
    fi
    ;;
  *)
    echo "Unknown format: $FORMAT"
    echo "Supported formats: text, json, markdown"
    exit 1
    ;;
esac
