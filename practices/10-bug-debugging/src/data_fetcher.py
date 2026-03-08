import asyncio
import time
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class FetchResult:
    url: str
    data: str
    timestamp: float


async def simulate_fetch(url: str) -> str:
    """Simulated async data source."""
    await asyncio.sleep(0.01)
    return f"Data from {url}"


async def log_access(url: str) -> None:
    """Simulated async logging (e.g., writing to a log service)."""
    await asyncio.sleep(0.005)


class DataFetcher:
    def __init__(self) -> None:
        # BUG: shared mutable state — last_result is overwritten by concurrent calls
        self._last_result: Optional[FetchResult] = None
        self._cache: Dict[str, FetchResult] = {}

    # BUG: race condition — this method updates shared state without proper synchronization
    # When called concurrently, the last_result and cache may be inconsistent
    async def fetch_data(self, url: str) -> FetchResult:
        # Check cache first
        if url in self._cache:
            self._last_result = self._cache[url]
            return self._last_result

        # BUG: Between this point and setting last_result below,
        # another call can overwrite last_result
        data = await simulate_fetch(url)

        result = FetchResult(
            url=url,
            data=data,
            timestamp=time.time(),
        )

        # BUG: these two operations are not atomic
        # Another concurrent call may have already changed last_result
        self._last_result = result
        self._cache[url] = result

        return result

    # BUG: fetch_multiple uses shared mutable state (self._last_result)
    # and yields to the event loop between fetch_data and reading last_result
    async def fetch_multiple(self, urls: List[str]) -> List[FetchResult]:
        results: List[FetchResult] = []

        async def _fetch_one(url: str) -> None:
            # BUG: All fetches start concurrently
            await self.fetch_data(url)
            # BUG: This await yields control to the event loop, allowing other
            # concurrent fetch_data calls to overwrite self._last_result
            await log_access(url)
            # BUG: by now, self._last_result has likely been overwritten
            # by another concurrent fetch that completed while we were logging
            results.append(self._last_result)  # type: ignore

        # All fetches start concurrently
        await asyncio.gather(*[_fetch_one(url) for url in urls])
        return results

    def get_last_result(self) -> Optional[FetchResult]:
        return self._last_result

    def clear_cache(self) -> None:
        self._cache.clear()
        self._last_result = None
