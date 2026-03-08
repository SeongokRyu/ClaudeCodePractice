#!/usr/bin/env bash
# gate-test.sh — Quality gate: automated tests
#
# Runs the project's test suite and checks for failures.
#
# Exit codes:
#   0 = all tests pass
#   1 = one or more tests failed or test runner error

set -uo pipefail

echo "[GATE: TESTS] Running test suite..."

# ── Check if test runner is available ─────────────────────────────────────
if [[ ! -f "package.json" ]]; then
  echo "[GATE: TESTS] No package.json found — skipping tests"
  echo "[GATE: TESTS] PASSED (no tests to run)"
  exit 0
fi

# Check if test script exists
HAS_TEST=$(node -e "const p=require('./package.json'); console.log(p.scripts && p.scripts.test ? 'yes' : 'no')" 2>/dev/null || echo "no")

if [[ "$HAS_TEST" != "yes" ]]; then
  echo "[GATE: TESTS] No test script in package.json — skipping"
  echo "[GATE: TESTS] PASSED (no tests configured)"
  exit 0
fi

# ── Run tests ─────────────────────────────────────────────────────────────
TEST_OUTPUT=$(npm test -- --ci --passWithNoTests 2>&1) || TEST_EXIT=$?
TEST_EXIT=${TEST_EXIT:-0}

# ── Parse results ─────────────────────────────────────────────────────────
TOTAL=$(echo "$TEST_OUTPUT" | grep -oP 'Tests:\s+.*' | tail -1 || echo "")
PASSED=$(echo "$TEST_OUTPUT" | grep -oP '\d+ passed' | grep -oP '\d+' || echo "0")
FAILED_COUNT=$(echo "$TEST_OUTPUT" | grep -oP '\d+ failed' | grep -oP '\d+' || echo "0")
SKIPPED=$(echo "$TEST_OUTPUT" | grep -oP '\d+ skipped' | grep -oP '\d+' || echo "0")

echo "[GATE: TESTS] Results: ${PASSED} passed, ${FAILED_COUNT} failed, ${SKIPPED} skipped"

# ── Evaluate ──────────────────────────────────────────────────────────────
if [[ $TEST_EXIT -ne 0 ]]; then
  echo "[GATE: TESTS] FAILED"
  echo ""
  # Show failure details
  echo "$TEST_OUTPUT" | grep -A 5 "FAIL\|Error\|✕\|✗" || true
  exit 1
fi

echo "[GATE: TESTS] PASSED"
exit 0
