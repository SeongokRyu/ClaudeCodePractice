"""
Quality Gate Pipeline — Python Agent SDK Implementation

Implements the full quality gate pipeline using the Anthropic Agent SDK:
  Gate 1: Automated tests (npm test)
  Gate 2: Lint + type check (eslint + tsc)
  Gate 3: Security scan (pattern matching)
  Gate 4: LLM-as-judge review (claude as reviewer)

Usage:
    python quality_pipeline.py [--continue-on-failure] [--skip-review]
"""

import asyncio
import subprocess
import sys
import time
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional

import anthropic


# ── Data Models ───────────────────────────────────────────────────────────


class GateStatus(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"


@dataclass
class GateResult:
    """Result of a single quality gate."""

    name: str
    status: GateStatus
    duration_seconds: float
    message: str = ""
    details: list[str] = field(default_factory=list)
    score: Optional[int] = None  # For review gate


@dataclass
class PipelineResult:
    """Result of the full pipeline run."""

    gates: list[GateResult]
    total_duration_seconds: float

    @property
    def passed(self) -> bool:
        return all(g.status in (GateStatus.PASSED, GateStatus.SKIPPED) for g in self.gates)

    @property
    def summary(self) -> str:
        lines = [
            "====================================",
            "Quality Gate Pipeline Results",
            "====================================",
            "",
        ]
        for i, gate in enumerate(self.gates, 1):
            total = len(self.gates)
            dots = "." * max(1, 16 - len(gate.name))
            score_info = f" [Score: {gate.score}/5]" if gate.score else ""
            lines.append(
                f"[{i}/{total}] {gate.name} {dots} {gate.status.value} "
                f"({gate.duration_seconds:.1f}s){score_info}"
            )

        lines.append("")
        lines.append("====================================")
        if self.passed:
            lines.append("PIPELINE RESULT: ALL GATES PASSED")
        else:
            failed_count = sum(1 for g in self.gates if g.status == GateStatus.FAILED)
            lines.append(f"PIPELINE RESULT: FAILED ({failed_count} gate(s) failed)")
        lines.append(f"Total time: {self.total_duration_seconds:.1f}s")
        lines.append("====================================")
        return "\n".join(lines)


# ── Gate Implementations ──────────────────────────────────────────────────


def run_command(cmd: str, timeout: int = 120) -> tuple[int, str]:
    """Run a shell command and return (exit_code, output)."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout + result.stderr
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 1, f"Command timed out after {timeout}s"
    except Exception as e:
        return 1, f"Command error: {e}"


def gate_test() -> GateResult:
    """Gate 1: Run automated tests."""
    start = time.time()

    if not Path("package.json").exists():
        return GateResult(
            name="Tests",
            status=GateStatus.PASSED,
            duration_seconds=time.time() - start,
            message="No package.json found, skipping tests",
        )

    exit_code, output = run_command("npm test -- --ci --passWithNoTests")
    duration = time.time() - start

    # Parse results
    passed = len(re.findall(r"(\d+) passed", output))
    failed = len(re.findall(r"(\d+) failed", output))

    if exit_code == 0:
        return GateResult(
            name="Tests",
            status=GateStatus.PASSED,
            duration_seconds=duration,
            message=f"{passed} passed, {failed} failed",
        )
    else:
        # Extract failure details
        details = [line for line in output.split("\n") if "FAIL" in line or "Error" in line]
        return GateResult(
            name="Tests",
            status=GateStatus.FAILED,
            duration_seconds=duration,
            message=f"Tests failed: {failed} failures",
            details=details[:10],
        )


def gate_lint() -> GateResult:
    """Gate 2: Run ESLint and TypeScript type check."""
    start = time.time()
    errors = 0
    details = []

    # ESLint
    eslint_exit, eslint_output = run_command("npx eslint . --ext .ts,.tsx,.js,.jsx --format compact")
    eslint_errors = len(re.findall(r"Error -", eslint_output))
    eslint_warnings = len(re.findall(r"Warning -", eslint_output))
    details.append(f"ESLint: {eslint_errors} errors, {eslint_warnings} warnings")
    errors += eslint_errors

    # TypeScript
    if Path("tsconfig.json").exists():
        tsc_exit, tsc_output = run_command("npx tsc --noEmit")
        tsc_errors = len(re.findall(r"error TS", tsc_output))
        details.append(f"TypeScript: {tsc_errors} errors")
        errors += tsc_errors
    else:
        details.append("TypeScript: skipped (no tsconfig.json)")

    duration = time.time() - start

    return GateResult(
        name="Lint",
        status=GateStatus.PASSED if errors == 0 else GateStatus.FAILED,
        duration_seconds=duration,
        message=f"{errors} total errors",
        details=details,
    )


def gate_security() -> GateResult:
    """Gate 3: Security vulnerability scan."""
    start = time.time()
    findings: dict[str, list[str]] = {"CRITICAL": [], "HIGH": [], "MEDIUM": [], "LOW": []}

    # Define patterns: (severity, pattern_regex, description)
    patterns = [
        ("CRITICAL", r'(password|api_key|secret|token)\s*[:=]\s*["\'][^"\']+["\']', "Hardcoded secret"),
        ("HIGH", r'\beval\s*\(', "Dynamic code execution (eval)"),
        ("HIGH", r'query\s*\(.*\+.*\$', "Potential SQL injection"),
        ("MEDIUM", r'\.innerHTML\s*=|dangerouslySetInnerHTML', "Potential XSS"),
        ("MEDIUM", r'http://(?!localhost|127\.0\.0\.1)', "Insecure HTTP URL"),
        ("LOW", r'createHash\s*\(\s*["\'](?:md5|sha1)["\']', "Weak cryptographic hash"),
        ("LOW", r'console\.(log|info|debug)\s*\(.*\b(password|token|secret)', "Logging sensitive data"),
    ]

    # Find source files
    source_extensions = {".ts", ".tsx", ".js", ".jsx"}
    skip_dirs = {"node_modules", ".git", "dist", "build"}

    for path in Path(".").rglob("*"):
        if path.suffix not in source_extensions:
            continue
        if any(skip in path.parts for skip in skip_dirs):
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue

        for severity, pattern, description in patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count("\n") + 1
                findings[severity].append(f"{description} — {path}:{line_num}")

    duration = time.time() - start

    total = sum(len(v) for v in findings.values())
    critical_high = len(findings["CRITICAL"]) + len(findings["HIGH"])

    details = []
    for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = len(findings[severity])
        details.append(f"{severity}: {count}")
        for finding in findings[severity][:5]:
            details.append(f"  {finding}")

    return GateResult(
        name="Security",
        status=GateStatus.PASSED if critical_high == 0 else GateStatus.FAILED,
        duration_seconds=duration,
        message=f"{total} findings ({critical_high} critical/high)",
        details=details,
    )


async def gate_review() -> GateResult:
    """Gate 4: LLM-as-judge review using Claude API."""
    start = time.time()

    # Get diff
    exit_code, diff = run_command("git diff --cached")
    if not diff.strip():
        exit_code, diff = run_command("git diff HEAD~1")

    if not diff.strip():
        return GateResult(
            name="Review",
            status=GateStatus.PASSED,
            duration_seconds=time.time() - start,
            message="No changes to review",
        )

    # Truncate large diffs
    diff_lines = diff.split("\n")
    if len(diff_lines) > 500:
        diff = "\n".join(diff_lines[:500]) + f"\n\n... (truncated, {len(diff_lines)} total lines)"

    # Load judge prompt
    judge_prompt_path = Path(__file__).parent.parent / "agents" / "quality-judge.md"
    if judge_prompt_path.exists():
        system_prompt = judge_prompt_path.read_text()
    else:
        system_prompt = (
            "You are a code quality reviewer. Score the code 1-5 and explain your reasoning. "
            "Output your score as: SCORE: N/5"
        )

    # Call Claude API
    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Review the following code changes:\n\n```diff\n{diff}\n```\n\nProvide your quality score and detailed feedback.",
                }
            ],
        )

        review_text = message.content[0].text

        # Parse score
        score_match = re.search(r"SCORE:\s*(\d)/5", review_text, re.IGNORECASE)
        if not score_match:
            score_match = re.search(r"(\d)/5", review_text)

        if score_match:
            score = int(score_match.group(1))
        else:
            return GateResult(
                name="Review",
                status=GateStatus.ERROR,
                duration_seconds=time.time() - start,
                message="Could not parse score from review",
                details=[review_text[:500]],
            )

        passed = score >= 3
        return GateResult(
            name="Review",
            status=GateStatus.PASSED if passed else GateStatus.FAILED,
            duration_seconds=time.time() - start,
            message=f"Score: {score}/5",
            score=score,
            details=review_text.split("\n")[:20],
        )

    except Exception as e:
        return GateResult(
            name="Review",
            status=GateStatus.ERROR,
            duration_seconds=time.time() - start,
            message=f"Review failed: {e}",
        )


# ── Pipeline Runner ───────────────────────────────────────────────────────


async def run_pipeline(
    continue_on_failure: bool = False,
    skip_review: bool = False,
) -> PipelineResult:
    """Run the full quality gate pipeline."""
    pipeline_start = time.time()
    results: list[GateResult] = []
    has_failure = False

    # Define gates
    sync_gates = [
        ("Tests", gate_test),
        ("Lint", gate_lint),
        ("Security", gate_security),
    ]

    # Run synchronous gates
    for name, gate_fn in sync_gates:
        if has_failure and not continue_on_failure:
            results.append(
                GateResult(
                    name=name,
                    status=GateStatus.SKIPPED,
                    duration_seconds=0,
                    message="Skipped due to previous failure",
                )
            )
            continue

        print(f"Running gate: {name}...")
        result = gate_fn()
        results.append(result)
        print(f"  {result.status.value}: {result.message}")

        if result.status == GateStatus.FAILED:
            has_failure = True

    # Run async review gate
    if skip_review:
        results.append(
            GateResult(
                name="Review",
                status=GateStatus.SKIPPED,
                duration_seconds=0,
                message="Skipped by flag",
            )
        )
    elif has_failure and not continue_on_failure:
        results.append(
            GateResult(
                name="Review",
                status=GateStatus.SKIPPED,
                duration_seconds=0,
                message="Skipped due to previous failure",
            )
        )
    else:
        print("Running gate: Review...")
        result = await gate_review()
        results.append(result)
        print(f"  {result.status.value}: {result.message}")

    pipeline_duration = time.time() - pipeline_start
    return PipelineResult(gates=results, total_duration_seconds=pipeline_duration)


# ── Main ──────────────────────────────────────────────────────────────────


async def main() -> None:
    continue_on_failure = "--continue-on-failure" in sys.argv
    skip_review = "--skip-review" in sys.argv

    result = await run_pipeline(
        continue_on_failure=continue_on_failure,
        skip_review=skip_review,
    )

    print()
    print(result.summary)

    # Print details for failed gates
    for gate in result.gates:
        if gate.status == GateStatus.FAILED and gate.details:
            print(f"\n--- {gate.name} Details ---")
            for detail in gate.details:
                print(f"  {detail}")

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    asyncio.run(main())
