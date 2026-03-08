"""
Practice 26: Writer/Reviewer Pipeline — Python Agent SDK Implementation

A complete writer/reviewer collaboration pipeline that:
1. Writer implements a feature
2. Reviewer reviews the implementation
3. Writer fixes issues (loop until APPROVED or max iterations)
4. Verifier runs tests as final gate
"""

import sys
import re
from dataclasses import dataclass
from enum import Enum
from claude_agent_sdk import Agent


class Verdict(Enum):
    APPROVED = "APPROVED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    UNKNOWN = "UNKNOWN"


@dataclass
class ReviewResult:
    verdict: Verdict
    quality_score: int
    feedback: str
    raw_text: str


@dataclass
class VerificationResult:
    passed: bool
    total_tests: int
    passed_tests: int
    failed_tests: int
    raw_text: str


def parse_review(review_text: str) -> ReviewResult:
    """Parse the reviewer's output to extract verdict and score."""

    # Extract verdict
    verdict = Verdict.UNKNOWN
    if "APPROVED" in review_text and "CHANGES_REQUESTED" not in review_text:
        verdict = Verdict.APPROVED
    elif "CHANGES_REQUESTED" in review_text:
        verdict = Verdict.CHANGES_REQUESTED

    # Extract quality score
    score_match = re.search(r"Quality Score:\s*(\d+)/10", review_text)
    quality_score = int(score_match.group(1)) if score_match else 0

    return ReviewResult(
        verdict=verdict,
        quality_score=quality_score,
        feedback=review_text,
        raw_text=review_text,
    )


def parse_verification(verification_text: str) -> VerificationResult:
    """Parse the verifier's output to extract test results."""

    passed = "PASS" in verification_text and "FAIL" not in verification_text.replace(
        "Failed: 0", ""
    )

    total_match = re.search(r"Total:\s*(\d+)", verification_text)
    passed_match = re.search(r"Passed:\s*(\d+)", verification_text)
    failed_match = re.search(r"Failed:\s*(\d+)", verification_text)

    return VerificationResult(
        passed=passed,
        total_tests=int(total_match.group(1)) if total_match else 0,
        passed_tests=int(passed_match.group(1)) if passed_match else 0,
        failed_tests=int(failed_match.group(1)) if failed_match else 0,
        raw_text=verification_text,
    )


def create_writer_agent() -> Agent:
    """Create a writer agent with full tool access."""
    return Agent()


def create_reviewer_agent() -> Agent:
    """Create a reviewer agent with read-only tools."""
    return Agent()


def create_verifier_agent() -> Agent:
    """Create a verifier agent for running tests."""
    return Agent()


def run_pipeline(
    feature_request: str,
    project_path: str = "src/project",
    max_iterations: int = 3,
) -> bool:
    """
    Run the full writer/reviewer pipeline.

    Args:
        feature_request: Description of the feature to implement
        project_path: Path to the project directory
        max_iterations: Maximum review/fix cycles

    Returns:
        True if the feature was approved and verified, False otherwise
    """

    writer = create_writer_agent()
    reviewer = create_reviewer_agent()
    verifier = create_verifier_agent()

    # ── Phase 1: Writer implements the feature ──────────────────────
    print("=" * 60)
    print("PHASE 1: Writer — Implementing feature")
    print("=" * 60)

    writer_result = writer.query(
        prompt=(
            f"Implement the following feature in {project_path}:\n\n"
            f"{feature_request}\n\n"
            f"Follow existing code patterns. Write tests. Run tests to verify."
        ),
        system_prompt={"preset": "claude_code"},
    )
    print(writer_result.text[:500] + "..." if len(writer_result.text) > 500 else writer_result.text)

    # ── Phase 2: Review/Fix Loop ────────────────────────────────────
    for iteration in range(1, max_iterations + 1):
        print(f"\n{'=' * 60}")
        print(f"PHASE 2: Reviewer — Review iteration {iteration}/{max_iterations}")
        print("=" * 60)

        # Reviewer reviews the implementation
        review_result = reviewer.query(
            prompt=(
                f"Review the code in {project_path}. "
                f"Focus on the recently implemented feature. "
                f"Use the exact output format: Verdict: APPROVED or CHANGES_REQUESTED"
            ),
            allowed_tools=["Read", "Glob", "Grep"],
        )

        review = parse_review(review_result.text)
        print(f"\nVerdict: {review.verdict.value}")
        print(f"Quality Score: {review.quality_score}/10")

        if review.verdict == Verdict.APPROVED:
            print(f"\nApproved after {iteration} review iteration(s)!")
            break

        if iteration == max_iterations:
            print(f"\nMax iterations ({max_iterations}) reached without approval.")
            return False

        # Writer fixes issues
        print(f"\n{'=' * 60}")
        print(f"PHASE 2b: Writer — Fixing issues (iteration {iteration})")
        print("=" * 60)

        writer_result = writer.query(
            prompt=(
                f"The reviewer found issues. Fix them:\n\n"
                f"{review.feedback}\n\n"
                f"Address each issue and re-run tests."
            ),
            system_prompt={"preset": "claude_code"},
        )
        print(writer_result.text[:500] + "..." if len(writer_result.text) > 500 else writer_result.text)

    # ── Phase 3: Verifier runs tests ────────────────────────────────
    print(f"\n{'=' * 60}")
    print("PHASE 3: Verifier — Running tests")
    print("=" * 60)

    verify_result = verifier.query(
        prompt=(
            f"Run the test suite in {project_path}. "
            f"Report test results and coverage. "
            f"Give a final PASS or FAIL verdict."
        ),
        allowed_tools=["Bash", "Read", "Glob"],
    )

    verification = parse_verification(verify_result.text)
    print(f"\nVerification: {'PASS' if verification.passed else 'FAIL'}")
    print(f"Tests: {verification.passed_tests}/{verification.total_tests} passed")

    if not verification.passed:
        print("\nVerification FAILED — tests did not pass.")
        return False

    print("\nPipeline complete — Feature implemented, reviewed, and verified!")
    return True


def main():
    """Run the pipeline with a sample feature request."""
    feature_request = (
        "Add a user authentication module with:\n"
        "- login(email, password) function that returns a JWT token\n"
        "- logout(token) function that invalidates the token\n"
        "- validateToken(token) function that checks if a token is valid\n"
        "- Password comparison (simulated, no actual bcrypt needed)\n"
        "- Token expiration handling\n"
        "- Comprehensive tests for all functions"
    )

    project_path = sys.argv[1] if len(sys.argv) > 1 else "src/project"

    success = run_pipeline(feature_request, project_path)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
