#!/usr/bin/env bash
# gate-review.sh — Quality gate: LLM-as-judge code review
#
# Uses claude -p to review staged changes and produce a quality score.
# Gate passes if score >= 3/5.
#
# Exit codes:
#   0 = quality score >= 3
#   1 = quality score < 3 or review failed

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JUDGE_PROMPT="${SCRIPT_DIR}/../agents/quality-judge.md"
MIN_SCORE=3

echo "[GATE: REVIEW] Starting LLM-as-judge review..."

# ── Get the diff to review ────────────────────────────────────────────────
DIFF=$(git diff --cached 2>/dev/null || git diff HEAD~1 2>/dev/null || echo "")

if [[ -z "$DIFF" ]]; then
  echo "[GATE: REVIEW] No changes to review"
  echo "[GATE: REVIEW] PASSED (nothing to review)"
  exit 0
fi

# Limit diff size to avoid excessive token usage
DIFF_LINES=$(echo "$DIFF" | wc -l)
if [[ $DIFF_LINES -gt 500 ]]; then
  echo "[GATE: REVIEW] Warning: diff is ${DIFF_LINES} lines, truncating to 500"
  DIFF=$(echo "$DIFF" | head -500)
  DIFF="${DIFF}\n\n... (truncated, ${DIFF_LINES} total lines)"
fi

# ── Check if claude CLI is available ──────────────────────────────────────
if ! command -v claude &>/dev/null; then
  echo "[GATE: REVIEW] claude CLI not found — skipping review"
  echo "[GATE: REVIEW] PASSED (review skipped)"
  exit 0
fi

# ── Load the judge prompt ─────────────────────────────────────────────────
if [[ -f "$JUDGE_PROMPT" ]]; then
  SYSTEM_PROMPT=$(cat "$JUDGE_PROMPT")
else
  SYSTEM_PROMPT="You are a code quality reviewer. Score the code 1-5 and explain your reasoning. Output your score as: SCORE: N/5"
fi

# ── Run the review ────────────────────────────────────────────────────────
REVIEW_INPUT="Review the following code changes:\n\n\`\`\`diff\n${DIFF}\n\`\`\`\n\nProvide your quality score and detailed feedback."

REVIEW_OUTPUT=$(echo -e "$REVIEW_INPUT" | claude -p "$SYSTEM_PROMPT" 2>/dev/null) || {
  echo "[GATE: REVIEW] Review failed (claude CLI error)"
  echo "[GATE: REVIEW] FAILED"
  exit 1
}

# ── Parse the score ───────────────────────────────────────────────────────
# Look for patterns like "SCORE: 4/5" or "Score: 4" or "4/5"
SCORE=$(echo "$REVIEW_OUTPUT" | grep -oiE "score:?\s*(\d)" | grep -oE "[0-9]" | head -1 || echo "")

if [[ -z "$SCORE" ]]; then
  # Try alternate pattern: N/5
  SCORE=$(echo "$REVIEW_OUTPUT" | grep -oE "[1-5]/5" | head -1 | cut -d'/' -f1 || echo "")
fi

if [[ -z "$SCORE" ]]; then
  echo "[GATE: REVIEW] Could not parse quality score from review"
  echo "[GATE: REVIEW] Review output:"
  echo "$REVIEW_OUTPUT" | head -20
  echo "[GATE: REVIEW] FAILED (unparseable score)"
  exit 1
fi

# ── Display review ────────────────────────────────────────────────────────
echo "[GATE: REVIEW] Quality Score: ${SCORE}/5"
echo ""
echo "  Review Summary:"
echo "$REVIEW_OUTPUT" | sed 's/^/    /'
echo ""

# ── Evaluate ──────────────────────────────────────────────────────────────
if [[ $SCORE -ge $MIN_SCORE ]]; then
  echo "[GATE: REVIEW] PASSED (score ${SCORE}/5 >= ${MIN_SCORE}/5)"
  exit 0
else
  echo "[GATE: REVIEW] FAILED (score ${SCORE}/5 < ${MIN_SCORE}/5)"
  exit 1
fi
