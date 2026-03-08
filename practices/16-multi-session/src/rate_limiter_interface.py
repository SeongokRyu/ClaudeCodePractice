"""
Rate Limiter Interface

API 요청 속도를 제한하는 Rate Limiter의 공통 인터페이스.
Sliding Window와 Token Bucket 두 가지 구현 모두 이 인터페이스를 따릅니다.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class RateLimiterConfig:
    """Rate limiter configuration."""

    # 시간 윈도우 내 최대 허용 요청 수
    max_requests: int

    # 시간 윈도우 크기 (밀리초)
    window_ms: int


@dataclass
class RateLimitResult:
    """Result of a rate limit check."""

    # 요청이 허용되었는지 여부
    allowed: bool

    # 현재 윈도우에서 남은 허용 요청 수
    remaining: int

    # 다음 요청이 허용될 때까지의 시간 (밀리초). 허용된 경우 0
    retry_after_ms: int


class RateLimiter(ABC):
    """
    Rate limiter abstract base class.

    All rate limiter implementations must implement this interface.
    """

    @abstractmethod
    def is_allowed(self, key: str) -> RateLimitResult:
        """
        주어진 키에 대한 요청이 허용되는지 확인하고,
        허용되면 요청을 기록합니다.

        Args:
            key: 제한을 적용할 키 (예: IP 주소, API 키)

        Returns:
            요청 허용 여부와 관련 정보
        """
        ...

    @abstractmethod
    def get_remaining_requests(self, key: str) -> int:
        """
        주어진 키의 현재 윈도우에서 남은 허용 요청 수를 반환합니다.
        is_allowed와 달리 요청을 기록하지 않습니다 (조회만).

        Args:
            key: 조회할 키

        Returns:
            남은 요청 수
        """
        ...

    @abstractmethod
    def reset(self, key: str) -> None:
        """
        주어진 키의 요청 기록을 초기화합니다.

        Args:
            key: 초기화할 키
        """
        ...

    @abstractmethod
    def reset_all(self) -> None:
        """
        모든 키의 요청 기록을 초기화합니다.
        """
        ...
