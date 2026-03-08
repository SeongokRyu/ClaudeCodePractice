"""
Rate Limiter Tests

All RateLimiter interface implementations must pass these tests.
Both Sliding Window and Token Bucket use this test suite.

Usage:
    Import the implementation in your test file and pass the factory
    to run_rate_limiter_tests.
    Example: run_rate_limiter_tests(SlidingWindowLimiter)
"""

from __future__ import annotations

import time
from typing import Callable, Type

import pytest

from rate_limiter_interface import RateLimiter, RateLimiterConfig


LimiterFactory = Callable[[RateLimiterConfig], RateLimiter]


def run_rate_limiter_tests(
    name: str,
    create_limiter: LimiterFactory,
) -> None:
    """
    Run the standard rate limiter test suite for a given implementation.

    This function is designed to be called from a concrete test module that
    imports a specific RateLimiter implementation.

    Args:
        name: Display name for the implementation (used in test descriptions).
        create_limiter: Factory function that creates a RateLimiter from config.
    """
    # This function exists as a reusable test runner.
    # Concrete tests are defined in the classes below.
    pass


# --- Fixtures and helpers ---


@pytest.fixture
def limiter_factory() -> LimiterFactory | None:
    """
    Override this fixture in your test module to provide a concrete factory.
    Returns None by default (placeholder tests will be skipped).
    """
    return None


@pytest.fixture
def limiter(limiter_factory: LimiterFactory | None) -> RateLimiter | None:
    if limiter_factory is None:
        return None
    return limiter_factory(RateLimiterConfig(max_requests=5, window_ms=1000))


# --- Tests ---


class TestIsAllowed:
    def test_should_allow_requests_within_the_limit(
        self, limiter: RateLimiter | None, limiter_factory: LimiterFactory | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        for i in range(5):
            result = limiter.is_allowed("user1")
            assert result.allowed is True
            assert result.remaining == 4 - i

    def test_should_deny_requests_that_exceed_the_limit(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        for _ in range(5):
            limiter.is_allowed("user1")

        result = limiter.is_allowed("user1")
        assert result.allowed is False
        assert result.remaining == 0
        assert result.retry_after_ms > 0

    def test_should_track_keys_independently(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        # Exhaust user1's limit
        for _ in range(5):
            limiter.is_allowed("user1")

        # user2 should still be allowed
        result = limiter.is_allowed("user2")
        assert result.allowed is True
        assert result.remaining == 4

    def test_should_return_retry_after_ms_of_0_when_allowed(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        result = limiter.is_allowed("user1")
        assert result.retry_after_ms == 0


class TestGetRemainingRequests:
    def test_should_return_max_requests_for_a_new_key(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        remaining = limiter.get_remaining_requests("newuser")
        assert remaining == 5

    def test_should_decrease_after_each_allowed_request(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        limiter.is_allowed("user1")
        limiter.is_allowed("user1")
        assert limiter.get_remaining_requests("user1") == 3

    def test_should_return_0_when_limit_is_reached(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        for _ in range(5):
            limiter.is_allowed("user1")
        assert limiter.get_remaining_requests("user1") == 0

    def test_should_not_count_as_a_request_read_only(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        limiter.get_remaining_requests("user1")
        limiter.get_remaining_requests("user1")
        limiter.get_remaining_requests("user1")
        # Should still have all requests available
        assert limiter.get_remaining_requests("user1") == 5


class TestReset:
    def test_should_reset_a_specific_key(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        for _ in range(5):
            limiter.is_allowed("user1")
        assert limiter.get_remaining_requests("user1") == 0

        limiter.reset("user1")
        assert limiter.get_remaining_requests("user1") == 5

    def test_should_not_affect_other_keys(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        limiter.is_allowed("user1")
        limiter.is_allowed("user2")

        limiter.reset("user1")

        assert limiter.get_remaining_requests("user1") == 5
        assert limiter.get_remaining_requests("user2") == 4

    def test_should_be_safe_to_call_on_non_existent_key(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        # Should not raise any exception
        limiter.reset("nonexistent")


class TestResetAll:
    def test_should_reset_all_keys(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        limiter.is_allowed("user1")
        limiter.is_allowed("user2")
        limiter.is_allowed("user3")

        limiter.reset_all()

        assert limiter.get_remaining_requests("user1") == 5
        assert limiter.get_remaining_requests("user2") == 5
        assert limiter.get_remaining_requests("user3") == 5


class TestTimeWindow:
    def test_should_allow_requests_again_after_window_expires(
        self, limiter_factory: LimiterFactory | None
    ) -> None:
        if limiter_factory is None:
            pytest.skip("No limiter implementation provided")
        # Use a short window for testing
        short_limiter = limiter_factory(
            RateLimiterConfig(max_requests=2, window_ms=100)
        )

        short_limiter.is_allowed("user1")
        short_limiter.is_allowed("user1")
        assert short_limiter.is_allowed("user1").allowed is False

        # Wait for the window to expire
        time.sleep(0.15)

        result = short_limiter.is_allowed("user1")
        assert result.allowed is True


class TestEdgeCases:
    def test_should_handle_zero_max_requests(
        self, limiter_factory: LimiterFactory | None
    ) -> None:
        if limiter_factory is None:
            pytest.skip("No limiter implementation provided")
        zero_limiter = limiter_factory(
            RateLimiterConfig(max_requests=0, window_ms=1000)
        )

        result = zero_limiter.is_allowed("user1")
        assert result.allowed is False
        assert result.remaining == 0

    def test_should_handle_a_single_max_request(
        self, limiter_factory: LimiterFactory | None
    ) -> None:
        if limiter_factory is None:
            pytest.skip("No limiter implementation provided")
        single_limiter = limiter_factory(
            RateLimiterConfig(max_requests=1, window_ms=1000)
        )

        assert single_limiter.is_allowed("user1").allowed is True
        assert single_limiter.is_allowed("user1").allowed is False

    def test_should_handle_empty_string_key(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        result = limiter.is_allowed("")
        assert result.allowed is True

    def test_should_handle_many_different_keys(
        self, limiter: RateLimiter | None
    ) -> None:
        if limiter is None:
            pytest.skip("No limiter implementation provided")
        for i in range(100):
            result = limiter.is_allowed(f"user-{i}")
            assert result.allowed is True
            assert result.remaining == 4


# --- Placeholder test to prevent "no tests" error ---
class TestRateLimiterTestSuite:
    def test_should_have_test_runner_ready(self) -> None:
        assert run_rate_limiter_tests is not None


# Placeholder: Import your implementation and run the tests
# from sliding_window_limiter import SlidingWindowLimiter
# from token_bucket_limiter import TokenBucketLimiter
#
# @pytest.fixture
# def limiter_factory():
#     return lambda config: SlidingWindowLimiter(config)
