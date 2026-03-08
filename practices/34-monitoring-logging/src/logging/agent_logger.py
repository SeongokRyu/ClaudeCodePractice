"""
agent_logger.py -- Structured logger for AI agent sessions

Captures tool calls, token usage, errors, and session metrics
in a structured JSON format for monitoring and analysis.
"""

import json
import os
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Any, Literal


# ── Types ────────────────────────────────────────────────────────────────

EventType = Literal[
    "session_start",
    "session_end",
    "tool_call_start",
    "tool_call_end",
    "tool_call_error",
    "cost_alert",
    "stuck_detected",
    "retry",
    "custom",
]

LogLevel = Literal["debug", "info", "warn", "error"]


@dataclass
class TokenCount:
    input: int = 0
    output: int = 0


@dataclass
class LogEntry:
    timestamp: str
    session_id: str
    event_type: EventType
    level: LogLevel
    tool_name: Optional[str] = None
    duration_ms: Optional[int] = None
    token_count: Optional[TokenCount] = None
    cumulative_tokens: Optional[TokenCount] = None
    status: Optional[Literal["success", "failure", "error"]] = None
    message: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class SessionStats:
    session_id: str
    start_time: str
    end_time: Optional[str]
    total_duration_ms: int
    total_tokens: TokenCount
    total_cost_usd: float
    tool_calls: int
    tool_errors: int
    tool_usage: dict[str, int]
    error_types: dict[str, int]


@dataclass
class LoggerConfig:
    session_id: Optional[str] = None
    output_file: Optional[str] = None
    console_output: bool = True
    log_level: LogLevel = "info"
    cost_per_input_token: Optional[float] = None
    cost_per_output_token: Optional[float] = None
    cost_budget_usd: Optional[float] = None


# ── Log level priority ───────────────────────────────────────────────────

LOG_LEVELS: dict[str, int] = {
    "debug": 0,
    "info": 1,
    "warn": 2,
    "error": 3,
}

# ── Default pricing (Claude Sonnet) ──────────────────────────────────────

DEFAULT_COST_PER_INPUT_TOKEN = 0.003 / 1000
DEFAULT_COST_PER_OUTPUT_TOKEN = 0.015 / 1000


# ── Helper to serialize dataclass ────────────────────────────────────────

def _token_count_to_dict(tc: Optional[TokenCount]) -> Optional[dict]:
    if tc is None:
        return None
    return {"input": tc.input, "output": tc.output}


def _entry_to_dict(entry: LogEntry) -> dict:
    d: dict[str, Any] = {
        "timestamp": entry.timestamp,
        "session_id": entry.session_id,
        "event_type": entry.event_type,
        "level": entry.level,
    }
    if entry.tool_name is not None:
        d["tool_name"] = entry.tool_name
    if entry.duration_ms is not None:
        d["duration_ms"] = entry.duration_ms
    if entry.token_count is not None:
        d["token_count"] = _token_count_to_dict(entry.token_count)
    if entry.cumulative_tokens is not None:
        d["cumulative_tokens"] = _token_count_to_dict(entry.cumulative_tokens)
    if entry.status is not None:
        d["status"] = entry.status
    if entry.message is not None:
        d["message"] = entry.message
    if entry.metadata is not None:
        d["metadata"] = entry.metadata
    return d


# ── AgentLogger class ────────────────────────────────────────────────────

class AgentLogger:
    def __init__(self, config: Optional[LoggerConfig] = None) -> None:
        if config is None:
            config = LoggerConfig()

        self._session_id: str = config.session_id or str(uuid.uuid4())
        self._output_file: Optional[str] = config.output_file
        self._console_output: bool = config.console_output
        self._log_level: LogLevel = config.log_level
        self._cost_per_input_token: float = (
            config.cost_per_input_token
            if config.cost_per_input_token is not None
            else DEFAULT_COST_PER_INPUT_TOKEN
        )
        self._cost_per_output_token: float = (
            config.cost_per_output_token
            if config.cost_per_output_token is not None
            else DEFAULT_COST_PER_OUTPUT_TOKEN
        )
        self._cost_budget_usd: Optional[float] = config.cost_budget_usd

        self._start_time: datetime = datetime.now(timezone.utc)
        self._cumulative_tokens: TokenCount = TokenCount(input=0, output=0)
        self._tool_calls: int = 0
        self._tool_errors: int = 0
        self._tool_usage: dict[str, int] = {}
        self._error_types: dict[str, int] = {}
        self._active_tool_calls: dict[str, dict] = {}  # call_id -> {tool, start}

        # Ensure output directory exists
        if self._output_file:
            directory = os.path.dirname(self._output_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

    # ── Core logging ─────────────────────────────────────────────────────

    def _log(self, entry: LogEntry) -> None:
        """Write a log entry to configured outputs."""
        if LOG_LEVELS.get(entry.level, 0) < LOG_LEVELS.get(self._log_level, 0):
            return

        line = json.dumps(_entry_to_dict(entry))

        # Console output
        if self._console_output:
            prefix = f"[{entry.level.upper()}]"
            tool_info = f" [{entry.tool_name}]" if entry.tool_name else ""
            print(
                f"{prefix}{tool_info} {entry.event_type}: {entry.message or ''}",
                file=sys.stderr,
            )

        # File output
        if self._output_file:
            with open(self._output_file, "a") as f:
                f.write(line + "\n")

    # ── Session lifecycle ────────────────────────────────────────────────

    def session_start(self, metadata: Optional[dict[str, Any]] = None) -> None:
        """Log session start."""
        self._start_time = datetime.now(timezone.utc)
        self._log(LogEntry(
            timestamp=self._start_time.isoformat(),
            session_id=self._session_id,
            event_type="session_start",
            level="info",
            message="Session started",
            metadata=metadata,
        ))

    def session_end(self) -> SessionStats:
        """Log session end and return stats."""
        end_time = datetime.now(timezone.utc)
        stats = self.get_stats(end_time)

        total_tokens = stats.total_tokens.input + stats.total_tokens.output
        self._log(LogEntry(
            timestamp=end_time.isoformat(),
            session_id=self._session_id,
            event_type="session_end",
            level="info",
            message=(
                f"Session ended. {stats.tool_calls} tool calls, "
                f"{total_tokens} tokens, ${stats.total_cost_usd:.4f}"
            ),
            cumulative_tokens=TokenCount(
                input=self._cumulative_tokens.input,
                output=self._cumulative_tokens.output,
            ),
            metadata={
                "total_cost_usd": stats.total_cost_usd,
                "tool_usage": stats.tool_usage,
            },
        ))

        return stats

    # ── Tool call tracking ───────────────────────────────────────────────

    def tool_call_start(
        self,
        tool_name: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> str:
        """Start tracking a tool call. Returns a unique call ID."""
        call_id = str(uuid.uuid4())
        self._active_tool_calls[call_id] = {
            "tool": tool_name,
            "start": _now_ms(),
        }

        meta = {"call_id": call_id}
        if metadata:
            meta.update(metadata)

        self._log(LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=self._session_id,
            event_type="tool_call_start",
            level="debug",
            tool_name=tool_name,
            message=f"Starting {tool_name}",
            metadata=meta,
        ))

        return call_id

    def tool_call_end(
        self,
        call_id: str,
        token_count: Optional[TokenCount] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """End tracking a tool call."""
        active = self._active_tool_calls.get(call_id)
        if active is None:
            self._log(LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                session_id=self._session_id,
                event_type="tool_call_error",
                level="warn",
                message=f"Unknown call ID: {call_id}",
            ))
            return

        duration = _now_ms() - active["start"]
        del self._active_tool_calls[call_id]

        # Update cumulative stats
        self._tool_calls += 1
        self._tool_usage[active["tool"]] = self._tool_usage.get(active["tool"], 0) + 1

        if token_count is not None:
            self._cumulative_tokens.input += token_count.input
            self._cumulative_tokens.output += token_count.output

        meta = {"call_id": call_id}
        if metadata:
            meta.update(metadata)

        self._log(LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=self._session_id,
            event_type="tool_call_end",
            level="info",
            tool_name=active["tool"],
            duration_ms=duration,
            token_count=token_count,
            cumulative_tokens=TokenCount(
                input=self._cumulative_tokens.input,
                output=self._cumulative_tokens.output,
            ),
            status="success",
            message=f"{active['tool']} completed in {duration}ms",
            metadata=meta,
        ))

        # Check cost budget
        self._check_cost_budget()

    def tool_call_error(
        self,
        call_id: str,
        error: Exception | str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Record a tool call error."""
        active = self._active_tool_calls.get(call_id)
        tool_name = active["tool"] if active else "unknown"
        duration = (_now_ms() - active["start"]) if active else 0

        if active:
            del self._active_tool_calls[call_id]

        self._tool_calls += 1
        self._tool_errors += 1
        self._tool_usage[tool_name] = self._tool_usage.get(tool_name, 0) + 1

        if isinstance(error, Exception):
            error_message = str(error)
            error_type = type(error).__name__
        else:
            error_message = error
            error_type = "Error"

        self._error_types[error_type] = self._error_types.get(error_type, 0) + 1

        meta = {
            "call_id": call_id,
            "error_type": error_type,
            "error_message": error_message,
        }
        if metadata:
            meta.update(metadata)

        self._log(LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=self._session_id,
            event_type="tool_call_error",
            level="error",
            tool_name=tool_name,
            duration_ms=duration,
            status="error",
            message=f"{tool_name} failed: {error_message}",
            metadata=meta,
        ))

    # ── Cost monitoring ──────────────────────────────────────────────────

    def _check_cost_budget(self) -> None:
        """Check if current cost is approaching the budget."""
        if self._cost_budget_usd is None:
            return

        current_cost = self.get_current_cost()
        percentage = (current_cost / self._cost_budget_usd) * 100

        if percentage >= 90:
            self._log(LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                session_id=self._session_id,
                event_type="cost_alert",
                level="error",
                message=(
                    f"Cost alert: ${current_cost:.4f} "
                    f"({percentage:.1f}% of ${self._cost_budget_usd} budget)"
                ),
                metadata={
                    "current_cost": current_cost,
                    "budget": self._cost_budget_usd,
                    "percentage": percentage,
                },
            ))
        elif percentage >= 75:
            self._log(LogEntry(
                timestamp=datetime.now(timezone.utc).isoformat(),
                session_id=self._session_id,
                event_type="cost_alert",
                level="warn",
                message=(
                    f"Cost warning: ${current_cost:.4f} "
                    f"({percentage:.1f}% of budget)"
                ),
                metadata={
                    "current_cost": current_cost,
                    "budget": self._cost_budget_usd,
                    "percentage": percentage,
                },
            ))

    def get_current_cost(self) -> float:
        """Calculate current session cost based on token usage."""
        return (
            self._cumulative_tokens.input * self._cost_per_input_token
            + self._cumulative_tokens.output * self._cost_per_output_token
        )

    # ── Custom events ────────────────────────────────────────────────────

    def log_custom(
        self,
        level: LogLevel,
        message: str,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """Log a custom event."""
        self._log(LogEntry(
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=self._session_id,
            event_type="custom",
            level=level,
            message=message,
            metadata=metadata,
        ))

    # ── Stats ────────────────────────────────────────────────────────────

    def get_stats(self, end_time: Optional[datetime] = None) -> SessionStats:
        """Get current session statistics."""
        end = end_time or datetime.now(timezone.utc)
        duration_ms = int((end - self._start_time).total_seconds() * 1000)

        return SessionStats(
            session_id=self._session_id,
            start_time=self._start_time.isoformat(),
            end_time=end.isoformat(),
            total_duration_ms=duration_ms,
            total_tokens=TokenCount(
                input=self._cumulative_tokens.input,
                output=self._cumulative_tokens.output,
            ),
            total_cost_usd=self.get_current_cost(),
            tool_calls=self._tool_calls,
            tool_errors=self._tool_errors,
            tool_usage=dict(self._tool_usage),
            error_types=dict(self._error_types),
        )

    def get_session_id(self) -> str:
        """Return the session ID."""
        return self._session_id

    def get_cumulative_tokens(self) -> TokenCount:
        """Return a copy of cumulative token counts."""
        return TokenCount(
            input=self._cumulative_tokens.input,
            output=self._cumulative_tokens.output,
        )


def _now_ms() -> int:
    """Return current time in milliseconds."""
    return int(datetime.now(timezone.utc).timestamp() * 1000)
