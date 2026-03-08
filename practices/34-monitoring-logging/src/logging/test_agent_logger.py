"""Tests for the AgentLogger."""

import json
import os
import pytest
from pathlib import Path

from agent_logger import AgentLogger, LoggerConfig, TokenCount


class TestConstructor:
    def test_default_config(self) -> None:
        logger = AgentLogger()
        assert logger.get_session_id() is not None
        assert len(logger.get_session_id()) > 0

    def test_custom_session_id(self) -> None:
        config = LoggerConfig(session_id="test-123")
        logger = AgentLogger(config)
        assert logger.get_session_id() == "test-123"

    def test_initial_zero_tokens(self) -> None:
        logger = AgentLogger()
        tokens = logger.get_cumulative_tokens()
        assert tokens.input == 0
        assert tokens.output == 0


class TestToolCallTracking:
    def test_track_successful_call(self) -> None:
        config = LoggerConfig(session_id="test-track", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call_id = logger.tool_call_start("Edit", {"file_path": "test.py"})
        assert call_id is not None

        logger.tool_call_end(call_id, TokenCount(input=100, output=50))

        stats = logger.get_stats()
        assert stats.tool_calls == 1
        assert stats.tool_errors == 0
        assert stats.tool_usage["Edit"] == 1

    def test_track_multiple_calls(self) -> None:
        config = LoggerConfig(session_id="test-multi", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call1 = logger.tool_call_start("Read")
        logger.tool_call_end(call1, TokenCount(input=200, output=100))

        call2 = logger.tool_call_start("Edit")
        logger.tool_call_end(call2, TokenCount(input=150, output=80))

        call3 = logger.tool_call_start("Read")
        logger.tool_call_end(call3, TokenCount(input=100, output=50))

        stats = logger.get_stats()
        assert stats.tool_calls == 3
        assert stats.tool_usage["Read"] == 2
        assert stats.tool_usage["Edit"] == 1

    def test_track_tool_call_errors(self) -> None:
        config = LoggerConfig(session_id="test-error", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call_id = logger.tool_call_start("Bash")
        logger.tool_call_error(call_id, Exception("Command failed"))

        stats = logger.get_stats()
        assert stats.tool_calls == 1
        assert stats.tool_errors == 1
        assert stats.error_types["Exception"] == 1

    def test_handle_string_errors(self) -> None:
        config = LoggerConfig(session_id="test-string-error", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call_id = logger.tool_call_start("Bash")
        logger.tool_call_error(call_id, "something went wrong")

        stats = logger.get_stats()
        assert stats.tool_errors == 1

    def test_handle_unknown_call_ids(self) -> None:
        config = LoggerConfig(session_id="test-unknown", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        # Should not raise
        logger.tool_call_end("nonexistent-id", TokenCount(input=100, output=50))


class TestTokenTracking:
    def test_accumulate_tokens(self) -> None:
        config = LoggerConfig(session_id="test-tokens", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call1 = logger.tool_call_start("Read")
        logger.tool_call_end(call1, TokenCount(input=100, output=50))

        call2 = logger.tool_call_start("Edit")
        logger.tool_call_end(call2, TokenCount(input=200, output=100))

        tokens = logger.get_cumulative_tokens()
        assert tokens.input == 300
        assert tokens.output == 150

    def test_calls_without_token_counts(self) -> None:
        config = LoggerConfig(session_id="test-no-tokens", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call_id = logger.tool_call_start("Glob")
        logger.tool_call_end(call_id)

        tokens = logger.get_cumulative_tokens()
        assert tokens.input == 0
        assert tokens.output == 0


class TestCostCalculation:
    def test_calculate_cost(self) -> None:
        config = LoggerConfig(
            session_id="test-cost",
            console_output=False,
            cost_per_input_token=0.001,
            cost_per_output_token=0.002,
        )
        logger = AgentLogger(config)
        logger.session_start()

        call_id = logger.tool_call_start("Read")
        logger.tool_call_end(call_id, TokenCount(input=1000, output=500))

        cost = logger.get_current_cost()
        assert cost == pytest.approx(1000 * 0.001 + 500 * 0.002)

    def test_zero_cost_with_no_usage(self) -> None:
        config = LoggerConfig(session_id="test-zero-cost", console_output=False)
        logger = AgentLogger(config)
        assert logger.get_current_cost() == 0


class TestSessionLifecycle:
    def test_complete_session_stats(self) -> None:
        config = LoggerConfig(session_id="test-lifecycle", console_output=False)
        logger = AgentLogger(config)
        logger.session_start()

        call1 = logger.tool_call_start("Read")
        logger.tool_call_end(call1, TokenCount(input=100, output=50))

        call2 = logger.tool_call_start("Edit")
        logger.tool_call_end(call2, TokenCount(input=200, output=100))

        call3 = logger.tool_call_start("Bash")
        logger.tool_call_error(call3, Exception("fail"))

        stats = logger.session_end()

        assert stats.session_id == "test-lifecycle"
        assert stats.start_time is not None
        assert stats.end_time is not None
        assert stats.tool_calls == 3
        assert stats.tool_errors == 1
        assert stats.total_tokens.input == 300
        assert stats.total_tokens.output == 150
        assert stats.total_cost_usd > 0
        assert stats.tool_usage == {"Read": 1, "Edit": 1, "Bash": 1}


class TestFileOutput:
    def test_write_log_entries_to_file(self, tmp_path: Path) -> None:
        test_log_file = str(tmp_path / "test-output.log")

        config = LoggerConfig(
            session_id="test-file",
            output_file=test_log_file,
            console_output=False,
        )
        logger = AgentLogger(config)
        logger.session_start()

        call_id = logger.tool_call_start("Read")
        logger.tool_call_end(call_id, TokenCount(input=100, output=50))
        logger.session_end()

        assert os.path.exists(test_log_file)

        with open(test_log_file, "r") as f:
            content = f.read()

        lines = content.strip().split("\n")
        assert len(lines) >= 3  # start, call_end, end (call_start is debug, filtered)

        # Each line should be valid JSON
        for line in lines:
            entry = json.loads(line)
            assert entry["session_id"] == "test-file"
            assert "timestamp" in entry
            assert "event_type" in entry


class TestCustomEvents:
    def test_log_custom_events(self) -> None:
        config = LoggerConfig(session_id="test-custom", console_output=False)
        logger = AgentLogger(config)

        # Should not raise
        logger.log_custom("info", "Custom event", {"key": "value"})
        logger.log_custom("warn", "Warning event")
        logger.log_custom("error", "Error event")


class TestLogLevelFiltering:
    def test_filter_debug_when_level_is_info(self, tmp_path: Path) -> None:
        log_file = str(tmp_path / "test-level.log")

        config = LoggerConfig(
            session_id="test-level",
            output_file=log_file,
            console_output=False,
            log_level="info",
        )
        logger = AgentLogger(config)

        logger.session_start()  # info -- should be logged
        call_id = logger.tool_call_start("Read")  # debug -- should be filtered
        logger.tool_call_end(call_id)  # info -- should be logged
        logger.session_end()  # info -- should be logged

        with open(log_file, "r") as f:
            content = f.read()

        lines = content.strip().split("\n")

        # Debug entries should be filtered out
        debug_entries = [
            json.loads(line)
            for line in lines
            if json.loads(line).get("level") == "debug"
        ]
        assert len(debug_entries) == 0
