"""
log_analyzer.py -- Identify patterns and optimization opportunities in agent sessions

Analyzes parsed session data to find:
- Repeated actions (potential optimization targets)
- Token spikes (where tokens were consumed most)
- Stuck patterns (edit-undo-edit cycles)
- Unused file reads (files read but not used for edits)
"""

from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from log_parser import ParsedSession


# ── Types ────────────────────────────────────────────────────────────────

PatternType = Literal[
    "repeated_action", "token_spike", "stuck_loop", "unused_read", "slow_operation"
]
Severity = Literal["info", "warning", "critical"]


@dataclass
class Pattern:
    type: PatternType
    severity: Severity
    description: str
    occurrences: int
    details: list[str]


@dataclass
class OptimizationSuggestion:
    area: str
    current: str
    suggested: str
    estimated_savings: str


@dataclass
class AnalysisReport:
    patterns: list[Pattern]
    suggestions: list[OptimizationSuggestion]
    health_score: int  # 0-100


# ── Analysis Functions ───────────────────────────────────────────────────


def analyze_session(
    entries: list[dict[str, Any]],
    session: ParsedSession,
) -> AnalysisReport:
    """Analyze a session and produce a report with patterns and suggestions."""
    patterns: list[Pattern] = []

    patterns.extend(_detect_repeated_actions(entries))
    patterns.extend(_detect_token_spikes(entries))
    patterns.extend(_detect_stuck_loops(entries))
    patterns.extend(_detect_unused_reads(entries))
    patterns.extend(_detect_slow_operations(entries))

    suggestions = _generate_suggestions(session, patterns)
    health_score = _calculate_health_score(session, patterns)

    return AnalysisReport(
        patterns=patterns,
        suggestions=suggestions,
        health_score=health_score,
    )


# ── Pattern Detection ────────────────────────────────────────────────────


def _detect_repeated_actions(entries: list[dict[str, Any]]) -> list[Pattern]:
    """Detect repeated tool calls on the same target."""
    patterns: list[Pattern] = []

    action_signatures: dict[str, int] = {}

    for entry in entries:
        if entry.get("event_type") != "tool_call_end":
            continue

        metadata = entry.get("metadata", {})
        file_path = metadata.get("file_path", metadata.get("path", ""))
        signature = f"{entry.get('tool_name', '')}:{file_path}"
        action_signatures[signature] = action_signatures.get(signature, 0) + 1

    for signature, count in action_signatures.items():
        if count >= 3:
            tool, file_path = signature.split(":", 1)
            patterns.append(Pattern(
                type="repeated_action",
                severity="warning" if count >= 5 else "info",
                description=f"{tool} called {count} times on {file_path or 'same target'}",
                occurrences=count,
                details=[
                    f"Tool: {tool}",
                    f"Target: {file_path or 'various'}",
                    f"Count: {count}",
                ],
            ))

    return patterns


def _detect_token_spikes(entries: list[dict[str, Any]]) -> list[Pattern]:
    """Detect individual tool calls with high token usage."""
    patterns: list[Pattern] = []

    for entry in entries:
        token_count = entry.get("token_count")
        if token_count is None:
            continue

        entry_tokens = token_count.get("input", 0) + token_count.get("output", 0)

        if entry_tokens > 5000:
            patterns.append(Pattern(
                type="token_spike",
                severity="warning" if entry_tokens > 10000 else "info",
                description=(
                    f"High token usage: {entry_tokens} tokens "
                    f"in single {entry.get('tool_name', 'unknown')} call"
                ),
                occurrences=1,
                details=[
                    f"Tool: {entry.get('tool_name', 'unknown')}",
                    f"Input tokens: {token_count.get('input', 0)}",
                    f"Output tokens: {token_count.get('output', 0)}",
                    f"Timestamp: {entry.get('timestamp', '')}",
                ],
            ))

    return patterns


def _detect_stuck_loops(entries: list[dict[str, Any]]) -> list[Pattern]:
    """Detect A-B-A-B patterns (e.g., edit-undo-edit-undo)."""
    patterns: list[Pattern] = []

    tool_sequence = [
        entry.get("tool_name", "")
        for entry in entries
        if entry.get("event_type") == "tool_call_end"
    ]

    for i in range(len(tool_sequence) - 3):
        if (
            tool_sequence[i] == tool_sequence[i + 2]
            and tool_sequence[i + 1] == tool_sequence[i + 3]
            and tool_sequence[i] != tool_sequence[i + 1]
        ):
            # Check if this pattern continues
            repeat_count = 2
            j = i + 4
            while j < len(tool_sequence) - 1:
                if (
                    tool_sequence[j] == tool_sequence[i]
                    and tool_sequence[j + 1] == tool_sequence[i + 1]
                ):
                    repeat_count += 1
                    j += 2
                else:
                    break

            if repeat_count >= 3:
                patterns.append(Pattern(
                    type="stuck_loop",
                    severity="critical",
                    description=(
                        f"Stuck loop detected: {tool_sequence[i]} <-> "
                        f"{tool_sequence[i + 1]} repeated {repeat_count} times"
                    ),
                    occurrences=repeat_count,
                    details=[
                        f"Pattern: {tool_sequence[i]} -> {tool_sequence[i + 1]}",
                        f"Repeats: {repeat_count}",
                        f"Starting at entry index: {i}",
                    ],
                ))
                break  # Report each unique loop once

    return patterns


def _detect_unused_reads(entries: list[dict[str, Any]]) -> list[Pattern]:
    """Detect files that were read but never edited."""
    patterns: list[Pattern] = []

    read_files: set[str] = set()
    edited_files: set[str] = set()

    for entry in entries:
        if entry.get("event_type") != "tool_call_end":
            continue

        metadata = entry.get("metadata", {})
        file_path = metadata.get("file_path", metadata.get("path", ""))

        if not file_path:
            continue

        tool_name = entry.get("tool_name", "")
        if tool_name == "Read":
            read_files.add(file_path)
        elif tool_name in ("Edit", "Write"):
            edited_files.add(file_path)

    unused_reads = [f for f in read_files if f not in edited_files]

    if len(unused_reads) > 3:
        patterns.append(Pattern(
            type="unused_read",
            severity="info",
            description=f"{len(unused_reads)} files were read but never edited",
            occurrences=len(unused_reads),
            details=unused_reads[:10],
        ))

    return patterns


def _detect_slow_operations(entries: list[dict[str, Any]]) -> list[Pattern]:
    """Detect tool calls that took longer than 30 seconds."""
    patterns: list[Pattern] = []

    for entry in entries:
        if entry.get("event_type") != "tool_call_end":
            continue

        duration_ms = entry.get("duration_ms")
        if duration_ms is None:
            continue

        if duration_ms > 30000:
            patterns.append(Pattern(
                type="slow_operation",
                severity="warning" if duration_ms > 60000 else "info",
                description=(
                    f"Slow operation: {entry.get('tool_name', 'unknown')} "
                    f"took {duration_ms / 1000:.1f}s"
                ),
                occurrences=1,
                details=[
                    f"Tool: {entry.get('tool_name', 'unknown')}",
                    f"Duration: {duration_ms / 1000:.1f}s",
                    f"Timestamp: {entry.get('timestamp', '')}",
                ],
            ))

    return patterns


# ── Suggestions ──────────────────────────────────────────────────────────


def _generate_suggestions(
    session: ParsedSession,
    patterns: list[Pattern],
) -> list[OptimizationSuggestion]:
    """Generate optimization suggestions based on session metrics and patterns."""
    suggestions: list[OptimizationSuggestion] = []

    # Check for high error rates
    for metric in session.tool_metrics.values():
        if metric.error_rate > 0.3 and metric.call_count >= 3:
            suggestions.append(OptimizationSuggestion(
                area=f"{metric.tool_name} reliability",
                current=(
                    f"{metric.error_rate * 100:.0f}% error rate "
                    f"({metric.error_count}/{metric.call_count})"
                ),
                suggested="Investigate common error causes and add pre-validation",
                estimated_savings=f"{metric.error_count} fewer failed calls",
            ))

    # Check for repeated actions
    repeated_patterns = [p for p in patterns if p.type == "repeated_action"]
    if repeated_patterns:
        suggestions.append(OptimizationSuggestion(
            area="Repeated operations",
            current=f"{len(repeated_patterns)} repeated action patterns found",
            suggested="Cache results or batch operations to reduce redundant calls",
            estimated_savings="20-40% fewer tool calls",
        ))

    # Check for stuck loops
    stuck_patterns = [p for p in patterns if p.type == "stuck_loop"]
    if stuck_patterns:
        suggestions.append(OptimizationSuggestion(
            area="Stuck loop prevention",
            current=f"{len(stuck_patterns)} stuck loop(s) detected",
            suggested="Add loop detection hooks and maximum iteration limits",
            estimated_savings="Prevent wasted tokens and time",
        ))

    # Check for token spikes
    spike_patterns = [p for p in patterns if p.type == "token_spike"]
    if spike_patterns:
        suggestions.append(OptimizationSuggestion(
            area="Token usage optimization",
            current=f"{len(spike_patterns)} high-token operations",
            suggested="Reduce file read sizes, use targeted searches instead of full reads",
            estimated_savings="10-30% token reduction",
        ))

    return suggestions


# ── Health Score ──────────────────────────────────────────────────────────


def _calculate_health_score(
    session: ParsedSession,
    patterns: list[Pattern],
) -> int:
    """Calculate a health score (0-100) for the session."""
    score = 100.0

    # Deduct for errors
    total_calls = sum(m.call_count for m in session.tool_metrics.values())
    total_errors = sum(m.error_count for m in session.tool_metrics.values())
    error_rate = total_errors / total_calls if total_calls > 0 else 0
    score -= error_rate * 30

    # Deduct for patterns
    for pattern in patterns:
        if pattern.severity == "critical":
            score -= 20
        elif pattern.severity == "warning":
            score -= 10
        elif pattern.severity == "info":
            score -= 2

    return max(0, min(100, round(score)))


# ── Report Formatting ────────────────────────────────────────────────────


def format_analysis_report(report: AnalysisReport) -> str:
    """Format an analysis report as a human-readable string."""
    lines: list[str] = []

    lines.append("====================================")
    lines.append("Session Analysis")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Health Score: {report.health_score}/100")
    lines.append("")

    if report.patterns:
        lines.append("Detected Patterns:")
        for pattern in report.patterns:
            if pattern.severity == "critical":
                icon = "[CRITICAL]"
            elif pattern.severity == "warning":
                icon = "[WARNING]"
            else:
                icon = "[INFO]"
            lines.append(f"  {icon} {pattern.description}")
            for detail in pattern.details:
                lines.append(f"    - {detail}")
        lines.append("")

    if report.suggestions:
        lines.append("Optimization Suggestions:")
        for suggestion in report.suggestions:
            lines.append(f"  Area: {suggestion.area}")
            lines.append(f"    Current: {suggestion.current}")
            lines.append(f"    Suggested: {suggestion.suggested}")
            lines.append(f"    Est. savings: {suggestion.estimated_savings}")
            lines.append("")

    lines.append("====================================")
    return "\n".join(lines)
