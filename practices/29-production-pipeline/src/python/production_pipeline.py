"""
Practice 29: Production Multi-Agent Pipeline — Python Agent SDK Implementation

A production-ready Command → Agent → Skill pipeline with agent memory.

Pipeline stages:
1. Researcher: Analyze codebase and create implementation plan
2. Implementer: Write code + tests (with skills loaded)
3. Reviewer: Review implementation (with memory)
4. Tester: Run tests and verify
5. Memory Update: Record new patterns learned
"""

import sys
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from claude_agent_sdk import Agent


# ── Types ────────────────────────────────────────────────────────

class Verdict(Enum):
    APPROVED = "APPROVED"
    CHANGES_REQUESTED = "CHANGES_REQUESTED"
    UNKNOWN = "UNKNOWN"


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass
class PipelineConfig:
    """Configuration for the production pipeline."""
    project_path: str = "src/pipeline"
    max_review_iterations: int = 3
    max_test_fix_attempts: int = 2
    skills_path: str = ".claude/skills"
    agents_path: str = ".claude/agents"
    memory_path: str = ".claude/agent-memory/reviewer/MEMORY.md"


@dataclass
class PipelineResult:
    """Result of the full pipeline execution."""
    feature: str
    status: str  # SUCCESS, PARTIAL, FAILED
    research_time: float = 0
    implement_time: float = 0
    review_iterations: int = 0
    review_verdict: str = ""
    test_result: str = ""
    files_changed: list[str] = field(default_factory=list)
    memory_updated: bool = False
    total_time: float = 0


# ── Agent Factories ──────────────────────────────────────────────

def create_researcher(config: PipelineConfig) -> Agent:
    """Create a researcher agent (read-only, haiku)."""
    return Agent()


def create_implementer(config: PipelineConfig) -> Agent:
    """Create an implementer agent (full access, sonnet, skills loaded)."""
    return Agent()


def create_reviewer(config: PipelineConfig) -> Agent:
    """Create a reviewer agent (read-only, with memory)."""
    return Agent()


def create_tester(config: PipelineConfig) -> Agent:
    """Create a tester agent (bash for tests, haiku)."""
    return Agent()


# ── Pipeline Stages ──────────────────────────────────────────────

def research_phase(feature: str, config: PipelineConfig) -> str:
    """
    Phase 1: Research the codebase and create an implementation plan.

    Returns the implementation plan as a string.
    """
    print_phase("RESEARCH", "Analyzing codebase and creating plan")

    researcher = create_researcher(config)
    result = researcher.query(
        prompt=(
            f"Analyze the codebase at {config.project_path} and create an "
            f"implementation plan for this feature:\n\n{feature}\n\n"
            f"Read CLAUDE.md for project conventions. "
            f"Produce a detailed implementation plan with files to create/modify, "
            f"step-by-step approach, and patterns to follow."
        ),
        allowed_tools=["Read", "Glob", "Grep"],
    )

    print(f"  Plan created ({len(result.text)} chars)")
    return result.text


def implement_phase(plan: str, config: PipelineConfig, feedback: str = "") -> str:
    """
    Phase 2: Implement the feature based on the plan.

    Args:
        plan: Implementation plan from the researcher
        feedback: Optional feedback from reviewer to address

    Returns the implementation report.
    """
    phase_name = "IMPLEMENT" if not feedback else "IMPLEMENT (fixing review feedback)"
    print_phase(phase_name, "Writing code and tests")

    implementer = create_implementer(config)

    prompt = (
        f"Implement the following plan in {config.project_path}:\n\n"
        f"{plan}\n\n"
        f"Before implementing:\n"
        f"1. Read the coding-conventions skill at {config.skills_path}/coding-conventions/SKILL.md\n"
        f"2. Read the testing-patterns skill at {config.skills_path}/testing-patterns/SKILL.md\n"
        f"3. Follow all conventions strictly\n\n"
        f"After implementing, run `pytest` to verify."
    )

    if feedback:
        prompt += f"\n\nAlso fix these issues from the reviewer:\n{feedback}"

    result = implementer.query(
        prompt=prompt,
        system_prompt={"preset": "claude_code"},
    )

    print(f"  Implementation complete ({len(result.text)} chars)")
    return result.text


def review_phase(config: PipelineConfig) -> tuple[Verdict, str, str]:
    """
    Phase 3: Review the implementation.

    Returns (verdict, feedback, new_patterns).
    """
    print_phase("REVIEW", "Reviewing implementation")

    reviewer = create_reviewer(config)

    memory_file = Path(config.project_path) / config.memory_path
    memory_prompt = ""
    if memory_file.exists():
        memory_prompt = (
            f"\nBefore reviewing, load your memory from {memory_file} "
            f"and apply learned patterns."
        )

    result = reviewer.query(
        prompt=(
            f"Review the recent code changes in {config.project_path}/src/.\n"
            f"Also load the security-review skill at "
            f"{config.skills_path}/security-review/SKILL.md.\n"
            f"{memory_prompt}\n\n"
            f"Produce a review with:\n"
            f"- Verdict: APPROVED or CHANGES_REQUESTED\n"
            f"- Quality Score: X/10\n"
            f"- Issues (Critical/Warning/Info)\n"
            f"- New patterns learned for your memory"
        ),
        allowed_tools=["Read", "Glob", "Grep"],
    )

    # Parse verdict
    verdict = Verdict.UNKNOWN
    if "APPROVED" in result.text and "CHANGES_REQUESTED" not in result.text:
        verdict = Verdict.APPROVED
    elif "CHANGES_REQUESTED" in result.text:
        verdict = Verdict.CHANGES_REQUESTED

    # Extract new patterns (rough extraction)
    patterns = ""
    pattern_match = re.search(
        r"(New Patterns|Patterns Learned|Memory Update).*?(?=###|$)",
        result.text,
        re.DOTALL | re.IGNORECASE,
    )
    if pattern_match:
        patterns = pattern_match.group()

    print(f"  Verdict: {verdict.value}")
    return verdict, result.text, patterns


def test_phase(config: PipelineConfig) -> tuple[TestResult, str]:
    """
    Phase 4: Run tests.

    Returns (result, details).
    """
    print_phase("TEST", "Running test suite")

    tester = create_tester(config)
    result = tester.query(
        prompt=(
            f"Run the test suite in {config.project_path}.\n"
            f"Run: cd {config.project_path} && pytest src/\n"
            f"Report: PASS or FAIL with details."
        ),
        allowed_tools=["Bash", "Read", "Glob"],
    )

    test_result = TestResult.UNKNOWN
    if "PASS" in result.text and "FAIL" not in result.text.replace("Failed: 0", ""):
        test_result = TestResult.PASS
    elif "FAIL" in result.text:
        test_result = TestResult.FAIL

    print(f"  Result: {test_result.value}")
    return test_result, result.text


def update_memory(config: PipelineConfig, new_patterns: str) -> bool:
    """
    Phase 5: Update reviewer memory with new patterns.
    """
    if not new_patterns.strip():
        return False

    memory_file = Path(config.project_path) / config.memory_path
    try:
        date_str = time.strftime("%Y-%m-%d")
        entry = f"\n\n## Session: {date_str}\n{new_patterns}\n"

        with open(memory_file, "a") as f:
            f.write(entry)

        print(f"  Memory updated: {memory_file}")
        return True
    except Exception as e:
        print(f"  Memory update failed: {e}")
        return False


# ── Main Pipeline ────────────────────────────────────────────────

def run_pipeline(
    feature: str,
    config: PipelineConfig | None = None,
) -> PipelineResult:
    """
    Run the full production pipeline.

    Args:
        feature: Description of the feature to build
        config: Pipeline configuration (uses defaults if not provided)

    Returns:
        PipelineResult with details of the pipeline execution
    """
    if config is None:
        config = PipelineConfig()

    result = PipelineResult(feature=feature)
    start_time = time.time()
    accumulated_patterns = ""

    try:
        # Phase 1: Research
        t = time.time()
        plan = research_phase(feature, config)
        result.research_time = time.time() - t

        # Phase 2: Implement
        t = time.time()
        implement_phase(plan, config)
        result.implement_time = time.time() - t

        # Phase 3: Review loop
        for iteration in range(1, config.max_review_iterations + 1):
            result.review_iterations = iteration
            verdict, feedback, patterns = review_phase(config)
            accumulated_patterns += patterns

            if verdict == Verdict.APPROVED:
                result.review_verdict = "APPROVED"
                break

            if iteration == config.max_review_iterations:
                result.review_verdict = "NOT_APPROVED"
                result.status = "PARTIAL"
                break

            # Fix issues
            implement_phase(plan, config, feedback=feedback)

        # Phase 4: Test
        test_result, test_details = test_phase(config)
        result.test_result = test_result.value

        if test_result == TestResult.FAIL:
            # One retry
            implement_phase(plan, config, feedback=f"Tests failed:\n{test_details}")
            test_result, _ = test_phase(config)
            result.test_result = test_result.value

        # Phase 5: Update memory
        result.memory_updated = update_memory(config, accumulated_patterns)

        # Final status
        if result.review_verdict == "APPROVED" and result.test_result == "PASS":
            result.status = "SUCCESS"
        elif result.review_verdict == "APPROVED" or result.test_result == "PASS":
            result.status = "PARTIAL"
        else:
            result.status = "FAILED"

    except Exception as e:
        print(f"\nPipeline error: {e}")
        result.status = "FAILED"

    result.total_time = time.time() - start_time

    # Print summary
    print_summary(result)
    return result


# ── Utilities ────────────────────────────────────────────────────

def print_phase(name: str, description: str) -> None:
    """Print a phase header."""
    print(f"\n{'=' * 60}")
    print(f"PHASE: {name}")
    print(f"  {description}")
    print("=" * 60)


def print_summary(result: PipelineResult) -> None:
    """Print the final pipeline summary."""
    print(f"\n{'=' * 60}")
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print(f"Feature: {result.feature[:80]}")
    print(f"Status:  {result.status}")
    print(f"Research time:     {result.research_time:.1f}s")
    print(f"Implementation time: {result.implement_time:.1f}s")
    print(f"Review iterations: {result.review_iterations}")
    print(f"Review verdict:    {result.review_verdict}")
    print(f"Test result:       {result.test_result}")
    print(f"Memory updated:    {result.memory_updated}")
    print(f"Total time:        {result.total_time:.1f}s")


# ── Entry Point ──────────────────────────────────────────────────

def main():
    """Run the pipeline with a sample feature request."""
    feature = (
        "Add a user preferences module with:\n"
        "- getUserPreferences(userId) — returns all preferences for a user\n"
        "- updatePreference(userId, key, value) — sets a single preference\n"
        "- resetPreferences(userId) — resets to defaults\n"
        "- Default preferences: { theme: 'light', language: 'en', notifications: true }\n"
        "- Comprehensive tests following project testing patterns"
    )

    config = PipelineConfig(
        project_path=sys.argv[1] if len(sys.argv) > 1 else "src/pipeline",
    )

    result = run_pipeline(feature, config)
    sys.exit(0 if result.status == "SUCCESS" else 1)


if __name__ == "__main__":
    main()
