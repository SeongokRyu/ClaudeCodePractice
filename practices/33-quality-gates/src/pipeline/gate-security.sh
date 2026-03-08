#!/usr/bin/env bash
# gate-security.sh — Quality gate: security vulnerability pattern scan
#
# Scans source files for common security anti-patterns.
# This is a lightweight pattern-matching scanner, not a full SAST tool.
#
# Exit codes:
#   0 = no CRITICAL or HIGH findings
#   1 = CRITICAL or HIGH findings detected

set -uo pipefail

echo "[GATE: SECURITY] Scanning for security vulnerabilities..."

CRITICAL=0
HIGH=0
MEDIUM=0
LOW=0
FINDINGS=""

# ── Helper function ───────────────────────────────────────────────────────
report_finding() {
  local severity="$1"
  local description="$2"
  local file="$3"
  local line="${4:-}"

  local location="$file"
  if [[ -n "$line" ]]; then
    location="${file}:${line}"
  fi

  FINDINGS="${FINDINGS}\n  [${severity}] ${description} — ${location}"

  case "$severity" in
    CRITICAL) CRITICAL=$((CRITICAL + 1)) ;;
    HIGH) HIGH=$((HIGH + 1)) ;;
    MEDIUM) MEDIUM=$((MEDIUM + 1)) ;;
    LOW) LOW=$((LOW + 1)) ;;
  esac
}

# ── Find source files ─────────────────────────────────────────────────────
SOURCE_FILES=$(find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  2>/dev/null || true)

if [[ -z "$SOURCE_FILES" ]]; then
  echo "[GATE: SECURITY] No source files found to scan"
  echo "[GATE: SECURITY] PASSED"
  exit 0
fi

# ── Pattern checks ───────────────────────────────────────────────────────

# CRITICAL: Hardcoded secrets
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "CRITICAL" "Hardcoded secret detected" "$file" "$line_num"
  done < <(grep -nE "(password|api_key|secret|token|private_key)\s*[:=]\s*['\"][^'\"]+['\"]" "$file" 2>/dev/null \
    | grep -viE "(test|spec|mock|example|placeholder|TODO|FIXME|xxx)" || true)
done <<< "$SOURCE_FILES"

# HIGH: SQL injection (string concatenation in queries)
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "HIGH" "Potential SQL injection (string concatenation)" "$file" "$line_num"
  done < <(grep -nE "(query|execute|sql)\s*\(.*\+.*\$|`.*\$\{.*\}.*SELECT|`.*\$\{.*\}.*INSERT|`.*\$\{.*\}.*UPDATE|`.*\$\{.*\}.*DELETE" "$file" 2>/dev/null || true)
done <<< "$SOURCE_FILES"

# HIGH: eval() or Function() with dynamic input
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "HIGH" "Dynamic code execution (eval/Function)" "$file" "$line_num"
  done < <(grep -nE "\beval\s*\(|new\s+Function\s*\(" "$file" 2>/dev/null \
    | grep -v "// safe:" || true)
done <<< "$SOURCE_FILES"

# MEDIUM: XSS via innerHTML or dangerouslySetInnerHTML
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "MEDIUM" "Potential XSS (innerHTML/dangerouslySetInnerHTML)" "$file" "$line_num"
  done < <(grep -nE "\.innerHTML\s*=|dangerouslySetInnerHTML" "$file" 2>/dev/null || true)
done <<< "$SOURCE_FILES"

# MEDIUM: Insecure HTTP URLs
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "MEDIUM" "Insecure HTTP URL (should be HTTPS)" "$file" "$line_num"
  done < <(grep -nE "http://[^l][^o][^c][^a]" "$file" 2>/dev/null \
    | grep -v "localhost\|127\.0\.0\.1\|http://example" || true)
done <<< "$SOURCE_FILES"

# LOW: Weak crypto
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "LOW" "Weak cryptographic hash (use bcrypt/argon2 for passwords)" "$file" "$line_num"
  done < <(grep -nE "createHash\s*\(\s*['\"]md5['\"]|createHash\s*\(\s*['\"]sha1['\"]" "$file" 2>/dev/null || true)
done <<< "$SOURCE_FILES"

# LOW: console.log with sensitive-looking data
while IFS= read -r file; do
  while IFS=: read -r line_num line_content; do
    report_finding "LOW" "Logging potentially sensitive data" "$file" "$line_num"
  done < <(grep -nE "console\.(log|info|debug)\s*\(.*\b(password|token|secret|key|credential)" "$file" 2>/dev/null || true)
done <<< "$SOURCE_FILES"

# ── Results ───────────────────────────────────────────────────────────────
TOTAL=$((CRITICAL + HIGH + MEDIUM + LOW))

echo "[GATE: SECURITY] Scan complete: ${TOTAL} findings"
echo "[GATE: SECURITY]   CRITICAL: ${CRITICAL}"
echo "[GATE: SECURITY]   HIGH:     ${HIGH}"
echo "[GATE: SECURITY]   MEDIUM:   ${MEDIUM}"
echo "[GATE: SECURITY]   LOW:      ${LOW}"

if [[ $TOTAL -gt 0 ]]; then
  echo ""
  echo "[GATE: SECURITY] Findings:"
  echo -e "$FINDINGS"
  echo ""
fi

if [[ $((CRITICAL + HIGH)) -gt 0 ]]; then
  echo "[GATE: SECURITY] FAILED (${CRITICAL} critical, ${HIGH} high severity findings)"
  exit 1
fi

echo "[GATE: SECURITY] PASSED"
exit 0
