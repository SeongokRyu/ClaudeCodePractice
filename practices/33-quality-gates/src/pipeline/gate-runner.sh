#!/usr/bin/env bash
# gate-runner.sh — Runs all quality gates sequentially (fail-fast)
#
# Exit codes:
#   0 = all gates passed
#   1 = at least one gate failed
#
# Usage:
#   bash gate-runner.sh [--continue-on-failure]

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTINUE_ON_FAILURE=false

if [[ "${1:-}" == "--continue-on-failure" ]]; then
  CONTINUE_ON_FAILURE=true
fi

# ── Gate definitions ──────────────────────────────────────────────────────
# Format: "script|name"
GATES=(
  "${SCRIPT_DIR}/gate-test.sh|Tests"
  "${SCRIPT_DIR}/gate-lint.sh|Lint"
  "${SCRIPT_DIR}/gate-security.sh|Security"
  "${SCRIPT_DIR}/gate-review.sh|Review"
)

# ── State tracking ────────────────────────────────────────────────────────
TOTAL_GATES=${#GATES[@]}
PASSED=0
FAILED=0
SKIPPED=0
RESULTS=()
PIPELINE_START=$(date +%s)

# ── Header ────────────────────────────────────────────────────────────────
echo "===================================="
echo "Quality Gate Pipeline"
echo "===================================="
echo ""

# ── Run each gate ─────────────────────────────────────────────────────────
for i in "${!GATES[@]}"; do
  gate_entry="${GATES[$i]}"
  gate_script="${gate_entry%%|*}"
  gate_name="${gate_entry#*|}"
  gate_num=$((i + 1))

  # Skip if previous gate failed and not in continue mode
  if [[ $FAILED -gt 0 && "$CONTINUE_ON_FAILURE" != "true" ]]; then
    RESULTS+=("[${gate_num}/${TOTAL_GATES}] ${gate_name} ............ SKIPPED")
    SKIPPED=$((SKIPPED + 1))
    continue
  fi

  # Run the gate
  printf "[%d/%d] %s " "$gate_num" "$TOTAL_GATES" "$gate_name"

  GATE_START=$(date +%s)

  if [[ -f "$gate_script" ]]; then
    GATE_OUTPUT=$(bash "$gate_script" 2>&1) || GATE_EXIT=$?
    GATE_EXIT=${GATE_EXIT:-0}
  else
    GATE_OUTPUT="Gate script not found: ${gate_script}"
    GATE_EXIT=1
  fi

  GATE_END=$(date +%s)
  GATE_DURATION=$((GATE_END - GATE_START))

  # Pad dots for alignment
  DOTS=""
  NAME_LEN=${#gate_name}
  for ((d = NAME_LEN; d < 16; d++)); do
    DOTS="${DOTS}."
  done

  if [[ $GATE_EXIT -eq 0 ]]; then
    echo "${DOTS} PASSED (${GATE_DURATION}s)"
    RESULTS+=("[${gate_num}/${TOTAL_GATES}] ${gate_name} ${DOTS} PASSED (${GATE_DURATION}s)")
    PASSED=$((PASSED + 1))
  else
    echo "${DOTS} FAILED (${GATE_DURATION}s)"
    echo ""
    echo "  Failure details:"
    echo "$GATE_OUTPUT" | sed 's/^/    /'
    echo ""
    RESULTS+=("[${gate_num}/${TOTAL_GATES}] ${gate_name} ${DOTS} FAILED (${GATE_DURATION}s)")
    FAILED=$((FAILED + 1))
  fi
done

# ── Summary ───────────────────────────────────────────────────────────────
PIPELINE_END=$(date +%s)
PIPELINE_DURATION=$((PIPELINE_END - PIPELINE_START))

echo ""
echo "===================================="

if [[ $FAILED -eq 0 ]]; then
  echo "PIPELINE RESULT: ALL GATES PASSED"
else
  echo "PIPELINE RESULT: FAILED (${FAILED} gate(s) failed)"
fi

echo "  Passed:  ${PASSED}/${TOTAL_GATES}"
echo "  Failed:  ${FAILED}/${TOTAL_GATES}"
echo "  Skipped: ${SKIPPED}/${TOTAL_GATES}"
echo "  Total time: ${PIPELINE_DURATION}s"
echo "===================================="

# Exit with failure if any gate failed
if [[ $FAILED -gt 0 ]]; then
  exit 1
fi

exit 0
