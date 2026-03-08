"""
log_parser.py -- Parse agent transcripts and extract structured metrics

Reads log files produced by AgentLogger and extracts:
- Tool call frequency
- Error rates per tool
- Token usage over time
- Session duration breakdown
"""

import json
from dataclasses import dataclass, field
from typing import Any, Optional

from agent_logger import LogEntry, TokenCount, EventType


# ── Types ────────────────────────────────────────────────────────────────


@dataclass
class ToolCallMetric:
    tool_name: str
    call_count: int = 0
    error_count: int = 0
    error_rate: float = 0.0
    avg_duration_ms: float = 0.0
    total_duration_ms: float = 0.0
    total_tokens: TokenCount = field(default_factory=TokenCount)


@dataclass
class TimeSeriesPoint:
    timestamp: str
    cumulative_input_tokens: int
    cumulative_output_tokens: int
    cumulative_cost_usd: float


@dataclass
class ParsedSession:
    session_id: str
    start_time: Optional[str]
    end_time: Optional[str]
    total_entries: int
    tool_metrics: dict[str, ToolCallMetric]
    token_timeline: list[TimeSeriesPoint]
    errors: list[dict[str, Any]]
    event_counts: dict[str, int]


# ── Parser ───────────────────────────────────────────────────────────────


def parse_log_file(file_path: str) -> list[dict[str, Any]]:
    """Parse a log file into a list of entry dicts."""
    with open(file_path, "r") as f:
        content = f.read()

    lines = [line.strip() for line in content.split("\n") if line.strip()]

    entries: list[dict[str, Any]] = []
    for line in lines:
        try:
            entry = json.loads(line)
            entries.append(entry)
        except json.JSONDecodeError:
            # Skip malformed lines
            continue

    return entries


def parse_log_entries(entries: list[dict[str, Any]]) -> ParsedSession:
    """Parse a list of log entry dicts into a structured session summary."""
    tool_metrics: dict[str, ToolCallMetric] = {}
    token_timeline: list[TimeSeriesPoint] = []
    errors: list[dict[str, Any]] = []
    event_counts: dict[str, int] = {}

    session_id = ""
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    # Cost per token (Sonnet pricing)
    cost_per_input = 0.003 / 1000
    cost_per_output = 0.015 / 1000

    for entry in entries:
        # Track session info
        if entry.get("session_id"):
            session_id = entry["session_id"]

        # Count events
        event_type = entry.get("event_type", "unknown")
        event_counts[event_type] = event_counts.get(event_type, 0) + 1

        # Track session boundaries
        if event_type == "session_start":
            start_time = entry.get("timestamp")
        if event_type == "session_end":
            end_time = entry.get("timestamp")

        # Track tool calls
        if event_type in ("tool_call_end", "tool_call_error"):
            tool_name = entry.get("tool_name", "unknown")

            if tool_name not in tool_metrics:
                tool_metrics[tool_name] = ToolCallMetric(tool_name=tool_name)

            metric = tool_metrics[tool_name]
            metric.call_count += 1

            if event_type == "tool_call_error":
                metric.error_count += 1

            duration = entry.get("duration_ms")
            if duration is not None:
                metric.total_duration_ms += duration

            token_count = entry.get("token_count")
            if token_count is not None:
                metric.total_tokens.input += token_count.get("input", 0)
                metric.total_tokens.output += token_count.get("output", 0)

            # Update averages
            metric.avg_duration_ms = metric.total_duration_ms / metric.call_count
            metric.error_rate = metric.error_count / metric.call_count

        # Track errors
        if entry.get("level") == "error":
            errors.append(entry)

        # Track token timeline
        cumulative = entry.get("cumulative_tokens")
        if cumulative is not None:
            input_tokens = cumulative.get("input", 0)
            output_tokens = cumulative.get("output", 0)
            token_timeline.append(TimeSeriesPoint(
                timestamp=entry.get("timestamp", ""),
                cumulative_input_tokens=input_tokens,
                cumulative_output_tokens=output_tokens,
                cumulative_cost_usd=(
                    input_tokens * cost_per_input + output_tokens * cost_per_output
                ),
            ))

    return ParsedSession(
        session_id=session_id,
        start_time=start_time,
        end_time=end_time,
        total_entries=len(entries),
        tool_metrics=tool_metrics,
        token_timeline=token_timeline,
        errors=errors,
        event_counts=event_counts,
    )


# ── Formatting ───────────────────────────────────────────────────────────


def format_session_report(session: ParsedSession) -> str:
    """Format a parsed session into a human-readable report."""
    lines: list[str] = []

    lines.append("====================================")
    lines.append("Session Analysis Report")
    lines.append("====================================")
    lines.append("")
    lines.append(f"Session ID: {session.session_id}")
    lines.append(f"Start: {session.start_time or 'unknown'}")
    lines.append(f"End: {session.end_time or 'unknown'}")
    lines.append(f"Total log entries: {session.total_entries}")
    lines.append("")

    # Tool usage table
    lines.append("Tool Usage:")
    lines.append(
        "  Tool              Calls  Errors  Error%  Avg(ms)  Tokens(in)  Tokens(out)"
    )
    lines.append(
        "  ----              -----  ------  ------  -------  ----------  ----------"
    )

    sorted_tools = sorted(
        session.tool_metrics.values(),
        key=lambda m: m.call_count,
        reverse=True,
    )

    for metric in sorted_tools:
        name = metric.tool_name.ljust(18)
        calls = str(metric.call_count).rjust(5)
        errs = str(metric.error_count).rjust(6)
        err_rate = f"{metric.error_rate * 100:.0f}%".rjust(6)
        avg_ms = str(round(metric.avg_duration_ms)).rjust(7)
        tok_in = str(metric.total_tokens.input).rjust(10)
        tok_out = str(metric.total_tokens.output).rjust(10)
        lines.append(f"  {name}{calls}{errs}{err_rate}{avg_ms}{tok_in}{tok_out}")

    lines.append("")

    # Token summary
    if session.token_timeline:
        last_point = session.token_timeline[-1]
        lines.append("Token Summary:")
        lines.append(f"  Input tokens:  {last_point.cumulative_input_tokens:,}")
        lines.append(f"  Output tokens: {last_point.cumulative_output_tokens:,}")
        lines.append(f"  Estimated cost: ${last_point.cumulative_cost_usd:.4f}")
        lines.append("")

    # Errors
    if session.errors:
        lines.append(f"Errors ({len(session.errors)}):")
        for error in session.errors[:10]:
            tool = error.get("tool_name", "")
            msg = error.get("message", "unknown error")
            ts = error.get("timestamp", "")
            lines.append(f"  [{ts}] {tool}: {msg}")
        if len(session.errors) > 10:
            lines.append(f"  ... and {len(session.errors) - 10} more")

    lines.append("")
    lines.append("====================================")

    return "\n".join(lines)
