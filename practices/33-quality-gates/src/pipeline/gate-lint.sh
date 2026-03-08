#!/usr/bin/env bash
# gate-lint.sh — Quality gate: ESLint + TypeScript type checking
#
# Runs both ESLint and the TypeScript compiler in noEmit mode.
# Gate passes only if both have zero errors (warnings are acceptable).
#
# Exit codes:
#   0 = zero errors from both tools
#   1 = one or more errors found

set -uo pipefail

ERRORS=0

echo "[GATE: LINT] Starting lint and type check..."

# ── ESLint ────────────────────────────────────────────────────────────────
echo "[GATE: LINT] Running ESLint..."

if command -v npx &>/dev/null && [[ -f "package.json" ]]; then
  ESLINT_OUTPUT=$(npx eslint . --ext .ts,.tsx,.js,.jsx --format compact 2>&1) || ESLINT_EXIT=$?
  ESLINT_EXIT=${ESLINT_EXIT:-0}

  # Count errors and warnings
  ESLINT_ERRORS=$(echo "$ESLINT_OUTPUT" | grep -c "Error -" 2>/dev/null || echo "0")
  ESLINT_WARNINGS=$(echo "$ESLINT_OUTPUT" | grep -c "Warning -" 2>/dev/null || echo "0")

  echo "[GATE: LINT] ESLint: ${ESLINT_ERRORS} errors, ${ESLINT_WARNINGS} warnings"

  if [[ $ESLINT_EXIT -ne 0 && $ESLINT_ERRORS -gt 0 ]]; then
    echo "[GATE: LINT] ESLint errors found:"
    echo "$ESLINT_OUTPUT" | grep "Error -" | head -20
    ERRORS=$((ERRORS + ESLINT_ERRORS))
  fi
else
  echo "[GATE: LINT] ESLint: skipped (not available)"
fi

# ── TypeScript ────────────────────────────────────────────────────────────
echo "[GATE: LINT] Running TypeScript compiler..."

if command -v npx &>/dev/null && [[ -f "tsconfig.json" ]]; then
  TSC_OUTPUT=$(npx tsc --noEmit 2>&1) || TSC_EXIT=$?
  TSC_EXIT=${TSC_EXIT:-0}

  # Count TypeScript errors
  TSC_ERRORS=$(echo "$TSC_OUTPUT" | grep -c "error TS" 2>/dev/null || echo "0")

  echo "[GATE: LINT] TypeScript: ${TSC_ERRORS} errors"

  if [[ $TSC_EXIT -ne 0 && $TSC_ERRORS -gt 0 ]]; then
    echo "[GATE: LINT] TypeScript errors found:"
    echo "$TSC_OUTPUT" | grep "error TS" | head -20
    ERRORS=$((ERRORS + TSC_ERRORS))
  fi
else
  echo "[GATE: LINT] TypeScript: skipped (no tsconfig.json)"
fi

# ── Result ────────────────────────────────────────────────────────────────
if [[ $ERRORS -gt 0 ]]; then
  echo "[GATE: LINT] FAILED (${ERRORS} total errors)"
  exit 1
fi

echo "[GATE: LINT] PASSED"
exit 0
