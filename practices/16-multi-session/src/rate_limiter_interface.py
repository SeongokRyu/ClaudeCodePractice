"""
Rate Limiter Interface

Common interface for Rate Limiters that throttle API request rates.
Both Sliding Window and Token Bucket implementations follow this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RateLimiterConfig:
    """Rate limiter configuration."""

    # Maximum number of allowed requests within the time window
    max_requests: int

    # Time window size (in milliseconds)
    window_ms: int


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""

    # Whether the request was allowed
    allowed: bool

    # Number of remaining allowed requests in the current window
    remaining: int

    # Time until the next request is allowed (in milliseconds). 0 if allowed
    retry_after_ms: int


class RateLimiter(ABC):
    """
    Rate limiter abstract base class.

    All rate limiter implementations must implement this interface.
    """

    @abstractmethod
    def is_allowed(self, key: str) -> RateLimitResult:
        """
        Check whether a request for the given key is allowed,
        and record the request if allowed.

        Args:
            key: The key to apply rate limiting to (e.g., IP address, API key)

        Returns:
            Result containing whether the request is allowed and related info
        """
        ...

    @abstractmethod
    def get_remaining_requests(self, key: str) -> int:
        """
        Return the number of remaining allowed requests for the given key
        in the current window. Unlike is_allowed, this does not record
        the request (read-only).

        Args:
            key: The key to query

        Returns:
            Number of remaining requests
        """
        ...

    @abstractmethod
    def reset(self, key: str) -> None:
        """
        Reset the request history for the given key.

        Args:
            key: The key to reset
        """
        ...

    @abstractmethod
    def reset_all(self) -> None:
        """
        Reset the request history for all keys.
        """
        ...
