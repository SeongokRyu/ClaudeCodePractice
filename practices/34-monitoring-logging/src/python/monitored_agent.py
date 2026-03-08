"""
monitored_agent.py — Python Agent SDK agent with full monitoring, error handling, and retry logic

Demonstrates:
- Structured logging for every tool call
- Cost tracking and budget enforcement
- Stuck loop detection
- Retry logic with exponential backoff
- Failure recovery and graceful degradation
- Session summary generation

Usage:
    python monitored_agent.py "Your task description here" [--budget 1.00] [--max-retries 3]
"""

import asyncio
import json
import logging
import sys
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

import anthropic

# ── Structured Logger ─────────────────────────────────────────────────────


class StructuredLogger:
    """JSON-formatted logger for agent sessions."""

    def __init__(
        self,
        session_id: str,
        log_file: Optional[str] = None,
        console: bool = True,
    ):
        self.session_id = session_id
        self.log_file = Path(log_file) if log_file else None
        self.console = console

        if self.log_file:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def _write(self, entry: dict[str, Any]) -> None:
        entry["session_id"] = self.session_id
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        line = json.dumps(entry, default=str)

        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(line + "\n")

        if self.console:
            level = entry.get("level", "info")
            tool = entry.get("tool_name", "")
            msg = entry.get("message", "")
            prefix = f"[{level.upper()}]"
            tool_info = f" [{tool}]" if tool else ""
            print(f"{prefix}{tool_info} {msg}", file=sys.stderr)

    def session_start(self, metadata: Optional[dict] = None) -> None:
        self._write({"event": "session_start", "level": "info", "message": "Session started", "metadata": metadata or {}})

    def session_end(self, stats: dict) -> None:
        self._write({"event": "session_end", "level": "info", "message": "Session ended", "metadata": stats})

    def tool_start(self, tool_name: str, metadata: Optional[dict] = None) -> None:
        self._write({"event": "tool_call_start", "level": "debug", "tool_name": tool_name, "message": f"Starting {tool_name}", "metadata": metadata or {}})

    def tool_end(self, tool_name: str, duration_ms: float, tokens: Optional[dict] = None, metadata: Optional[dict] = None) -> None:
        self._write({
            "event": "tool_call_end",
            "level": "info",
            "tool_name": tool_name,
            "duration_ms": round(duration_ms),
            "token_count": tokens,
            "message": f"{tool_name} completed in {duration_ms:.0f}ms",
            "metadata": metadata or {},
        })

    def tool_error(self, tool_name: str, error: str, metadata: Optional[dict] = None) -> None:
        self._write({"event": "tool_call_error", "level": "error", "tool_name": tool_name, "message": f"{tool_name} failed: {error}", "metadata": metadata or {}})

    def alert(self, alert_type: str, message: str, metadata: Optional[dict] = None) -> None:
        self._write({"event": alert_type, "level": "warn", "message": message, "metadata": metadata or {}})

    def info(self, message: str, metadata: Optional[dict] = None) -> None:
        self._write({"event": "custom", "level": "info", "message": message, "metadata": metadata or {}})


# ── Cost Tracker ──────────────────────────────────────────────────────────


@dataclass
class CostTracker:
    """Tracks token usage and cost, alerts at thresholds."""

    budget_usd: float = 1.00
    cost_per_input_token: float = 0.003 / 1000   # Sonnet pricing
    cost_per_output_token: float = 0.015 / 1000
    input_tokens: int = 0
    output_tokens: int = 0
    _alerted_thresholds: set = field(default_factory=set)

    @property
    def current_cost(self) -> float:
        return (
            self.input_tokens * self.cost_per_input_token
            + self.output_tokens * self.cost_per_output_token
        )

    @property
    def budget_percentage(self) -> float:
        if self.budget_usd <= 0:
            return 0
        return (self.current_cost / self.budget_usd) * 100

    def add_tokens(self, input_tokens: int, output_tokens: int) -> None:
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens

    def check_budget(self, logger: StructuredLogger) -> bool:
        """Check budget and alert. Returns False if budget exceeded."""
        pct = self.budget_percentage
        thresholds = [(50, "INFO"), (75, "WARNING"), (90, "CRITICAL"), (100, "EXCEEDED")]

        for threshold, level in thresholds:
            if pct >= threshold and threshold not in self._alerted_thresholds:
                self._alerted_thresholds.add(threshold)
                logger.alert(
                    "cost_alert",
                    f"Cost {level}: ${self.current_cost:.4f} ({pct:.1f}% of ${self.budget_usd} budget)",
                    {"current_cost": self.current_cost, "budget": self.budget_usd, "percentage": pct},
                )

        return pct < 100


# ── Stuck Detector ────────────────────────────────────────────────────────


@dataclass
class StuckDetector:
    """Detects when an agent is stuck in a loop."""

    repeat_threshold: int = 5
    cycle_threshold: int = 3
    recent_tools: list[str] = field(default_factory=list)
    max_history: int = 20

    def record_tool_call(self, tool_name: str) -> None:
        self.recent_tools.append(tool_name)
        if len(self.recent_tools) > self.max_history:
            self.recent_tools = self.recent_tools[-self.max_history:]

    def is_stuck(self) -> Optional[str]:
        """Returns a reason string if stuck, None otherwise."""
        if len(self.recent_tools) < self.repeat_threshold:
            return None

        # Check for repeated identical calls
        recent = self.recent_tools[-self.repeat_threshold:]
        if len(set(recent)) == 1:
            return f"Repeated: {recent[0]} called {self.repeat_threshold} times consecutively"

        # Check for A-B-A-B cycles
        if len(self.recent_tools) >= self.cycle_threshold * 2:
            recent_pairs = self.recent_tools[-(self.cycle_threshold * 2):]
            is_cycle = True
            a, b = recent_pairs[-2], recent_pairs[-1]
            if a == b:
                is_cycle = False
            else:
                for i in range(0, len(recent_pairs) - 1, 2):
                    if recent_pairs[i] != a or recent_pairs[i + 1] != b:
                        is_cycle = False
                        break
            if is_cycle:
                return f"Cycle: {a} <-> {b} repeated {self.cycle_threshold} times"

        return None


# ── Retry Logic ───────────────────────────────────────────────────────────


class RetryStrategy(Enum):
    NO_RETRY = "no_retry"
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"


def get_retry_strategy(error: str) -> tuple[RetryStrategy, int]:
    """Determine retry strategy based on error type. Returns (strategy, max_retries)."""
    error_lower = error.lower()

    # No retry for deterministic failures
    if any(term in error_lower for term in ["not found", "permission denied", "invalid", "syntax error"]):
        return RetryStrategy.NO_RETRY, 0

    # Retry with backoff for transient failures
    if any(term in error_lower for term in ["rate limit", "429", "timeout", "connection"]):
        return RetryStrategy.EXPONENTIAL_BACKOFF, 3

    # Default: limited retry
    return RetryStrategy.LINEAR_BACKOFF, 2


async def retry_with_backoff(
    func,
    strategy: RetryStrategy,
    max_retries: int,
    logger: StructuredLogger,
) -> Any:
    """Execute a function with retry logic."""
    if strategy == RetryStrategy.NO_RETRY:
        return await func()

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_error = e
            if attempt == max_retries:
                break

            if strategy == RetryStrategy.EXPONENTIAL_BACKOFF:
                delay = 2**attempt
            else:
                delay = attempt + 1

            logger.info(
                f"Retry {attempt + 1}/{max_retries} after {delay}s",
                {"error": str(e), "delay": delay},
            )
            await asyncio.sleep(delay)

    raise last_error  # type: ignore[misc]


# ── Monitored Agent ──────────────────────────────────────────────────────


class MonitoredAgent:
    """An agent with comprehensive monitoring, error handling, and retry logic."""

    def __init__(
        self,
        budget_usd: float = 1.00,
        max_retries: int = 3,
        log_file: Optional[str] = None,
    ):
        self.session_id = str(uuid.uuid4())[:8]
        self.logger = StructuredLogger(
            session_id=self.session_id,
            log_file=log_file or f"/tmp/agent-session-{self.session_id}.log",
            console=True,
        )
        self.cost_tracker = CostTracker(budget_usd=budget_usd)
        self.stuck_detector = StuckDetector()
        self.max_retries = max_retries
        self.client = anthropic.Anthropic()
        self.start_time = time.time()
        self.tool_calls = 0
        self.tool_errors = 0

    async def run(self, task: str) -> str:
        """Run a task with full monitoring."""
        self.logger.session_start({"task": task, "budget": self.cost_tracker.budget_usd})
        self.start_time = time.time()

        try:
            result = await self._execute_task(task)
            return result
        except Exception as e:
            self.logger.tool_error("agent", f"Task failed: {e}")
            return f"Task failed: {e}"
        finally:
            duration = time.time() - self.start_time
            stats = {
                "duration_seconds": round(duration, 1),
                "tool_calls": self.tool_calls,
                "tool_errors": self.tool_errors,
                "total_tokens": self.cost_tracker.input_tokens + self.cost_tracker.output_tokens,
                "total_cost_usd": round(self.cost_tracker.current_cost, 4),
            }
            self.logger.session_end(stats)
            self._print_summary(stats)

    async def _execute_task(self, task: str) -> str:
        """Execute the task using Claude API with monitoring."""
        messages = [{"role": "user", "content": task}]

        # Single-turn for simplicity (extend for multi-turn)
        tool_start = time.time()
        self.logger.tool_start("claude_api", {"model": "claude-sonnet-4-20250514"})

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                messages=messages,
            )

            duration_ms = (time.time() - tool_start) * 1000
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens

            self.cost_tracker.add_tokens(input_tokens, output_tokens)
            self.tool_calls += 1

            self.logger.tool_end(
                "claude_api",
                duration_ms,
                {"input": input_tokens, "output": output_tokens},
            )

            # Check budget
            if not self.cost_tracker.check_budget(self.logger):
                self.logger.alert("cost_alert", "Budget exceeded, stopping")
                return "Task stopped: budget exceeded"

            # Check for stuck
            self.stuck_detector.record_tool_call("claude_api")
            stuck_reason = self.stuck_detector.is_stuck()
            if stuck_reason:
                self.logger.alert("stuck_detected", stuck_reason)

            return response.content[0].text

        except anthropic.RateLimitError as e:
            self.tool_errors += 1
            self.logger.tool_error("claude_api", f"Rate limited: {e}")

            strategy, retries = get_retry_strategy("rate limit")

            async def retry_fn():
                return self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=4096,
                    messages=messages,
                )

            response = await retry_with_backoff(retry_fn, strategy, retries, self.logger)
            return response.content[0].text

        except Exception as e:
            self.tool_errors += 1
            self.logger.tool_error("claude_api", str(e))
            raise

    def _print_summary(self, stats: dict) -> None:
        """Print a human-readable session summary."""
        print("\n" + "=" * 40, file=sys.stderr)
        print("  Session Summary", file=sys.stderr)
        print("=" * 40, file=sys.stderr)
        print(f"  Session ID:  {self.session_id}", file=sys.stderr)
        print(f"  Duration:    {stats['duration_seconds']}s", file=sys.stderr)
        print(f"  Tool calls:  {stats['tool_calls']}", file=sys.stderr)
        print(f"  Errors:      {stats['tool_errors']}", file=sys.stderr)
        print(f"  Tokens:      {stats['total_tokens']}", file=sys.stderr)
        print(f"  Cost:        ${stats['total_cost_usd']}", file=sys.stderr)
        print(f"  Log file:    {self.logger.log_file}", file=sys.stderr)
        print("=" * 40 + "\n", file=sys.stderr)


# ── Main ──────────────────────────────────────────────────────────────────


async def main() -> None:
    args = sys.argv[1:]

    if not args or args[0].startswith("--"):
        print("Usage: python monitored_agent.py 'task description' [--budget 1.00] [--max-retries 3]")
        sys.exit(1)

    task = args[0]
    budget = 1.00
    max_retries = 3

    i = 1
    while i < len(args):
        if args[i] == "--budget" and i + 1 < len(args):
            budget = float(args[i + 1])
            i += 2
        elif args[i] == "--max-retries" and i + 1 < len(args):
            max_retries = int(args[i + 1])
            i += 2
        else:
            i += 1

    agent = MonitoredAgent(budget_usd=budget, max_retries=max_retries)
    result = await agent.run(task)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
