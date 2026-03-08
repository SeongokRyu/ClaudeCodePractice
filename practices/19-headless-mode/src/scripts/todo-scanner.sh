#!/usr/bin/env bash
#
# todo-scanner.sh — Scan for TODO/FIXME comments and analyze them with Claude
#
# Usage:
#   bash todo-scanner.sh                    # Scan current directory
#   bash todo-scanner.sh src/               # Scan specific directory
#   bash todo-scanner.sh --prioritize       # Scan and prioritize TODOs
#   bash todo-scanner.sh --json             # Output as JSON
#

set -euo pipefail

# Configuration
SCAN_DIR="${1:-.}"
PRIORITIZE=false
OUTPUT_FORMAT="text"

# Parse arguments
POSITIONAL_ARGS=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --prioritize)
      PRIORITIZE=true
      shift
      ;;
    --json)
      OUTPUT_FORMAT="json"
      shift
      ;;
    --help)
      echo "Usage: todo-scanner.sh [directory] [--prioritize] [--json]"
      exit 0
      ;;
    *)
      POSITIONAL_ARGS+=("$1")
      shift
      ;;
  esac
done

if [[ ${#POSITIONAL_ARGS[@]} -gt 0 ]]; then
  SCAN_DIR="${POSITIONAL_ARGS[0]}"
fi

# Find TODO/FIXME comments
scan_todos() {
  local dir="$1"

  # Search for TODO, FIXME, HACK, XXX, WARN comments
  # Exclude node_modules, dist, .git, and binary files
  grep -rn \
    --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" \
    --include="*.py" --include="*.go" --include="*.rs" --include="*.java" \
    --include="*.sh" --include="*.yml" --include="*.yaml" \
    -E "(TODO|FIXME|HACK|XXX|WARN):" \
    "$dir" 2>/dev/null || true
}

# Main logic
main() {
  echo "=== TODO/FIXME Scanner ==="
  echo "Scanning: $SCAN_DIR"
  echo ""

  local todos
  todos=$(scan_todos "$SCAN_DIR")

  if [[ -z "$todos" ]]; then
    echo "No TODO/FIXME comments found."
    exit 0
  fi

  local count
  count=$(echo "$todos" | wc -l)
  echo "Found ${count} TODO/FIXME comment(s)."
  echo ""

  if [[ "$PRIORITIZE" == true ]]; then
    echo "Analyzing and prioritizing with Claude..."
    echo ""

    local analysis
    analysis=$(echo "$todos" | claude -p "Analyze these TODO/FIXME comments from a codebase. For each one:
1. Categorize it (feature, bug, tech-debt, security, performance)
2. Assign priority (P0-critical, P1-high, P2-medium, P3-low)
3. Estimate effort (small/medium/large)
4. Suggest an approach if applicable

Group them by priority. Output in a clean, readable format." \
      --allowedTools "" --max-turns 1 2>/dev/null || echo "Error: Failed to analyze TODOs.")

    echo "$analysis"
  elif [[ "$OUTPUT_FORMAT" == "json" ]]; then
    # Parse into JSON format
    echo "$todos" | python3 -c '
import sys, json, re

todos = []
for line in sys.stdin:
    line = line.strip()
    match = re.match(r"^(.+?):(\d+):(.+)$", line)
    if match:
        file_path, line_num, content = match.groups()
        # Detect type
        todo_type = "TODO"
        for t in ["FIXME", "HACK", "XXX", "WARN"]:
            if t in content:
                todo_type = t
                break
        todos.append({
            "file": file_path,
            "line": int(line_num),
            "type": todo_type,
            "content": content.strip()
        })

print(json.dumps(todos, indent=2))
'
  else
    # Simple text output grouped by file
    local current_file=""
    while IFS= read -r line; do
      local file
      file=$(echo "$line" | cut -d: -f1)
      if [[ "$file" != "$current_file" ]]; then
        echo ""
        echo "── $file ──"
        current_file="$file"
      fi
      local line_num
      line_num=$(echo "$line" | cut -d: -f2)
      local content
      content=$(echo "$line" | cut -d: -f3-)
      echo "  L${line_num}: ${content}"
    done <<< "$todos"
  fi

  echo ""
  echo "=== Scan Complete ==="
}

main
