import pytest
import asyncio
from data_fetcher import DataFetcher


class TestDataFetcherFetchData:
    def setup_method(self):
        self.fetcher = DataFetcher()

    @pytest.mark.asyncio
    async def test_should_fetch_data_from_a_url(self):
        result = await self.fetcher.fetch_data("https://api.example.com/data")
        assert result.url == "https://api.example.com/data"
        assert result.data == "Data from https://api.example.com/data"
        assert result.timestamp is not None

    @pytest.mark.asyncio
    async def test_should_cache_results(self):
        result1 = await self.fetcher.fetch_data("https://api.example.com/data")
        result2 = await self.fetcher.fetch_data("https://api.example.com/data")
        assert result1.timestamp == result2.timestamp

    @pytest.mark.asyncio
    async def test_should_update_last_result(self):
        await self.fetcher.fetch_data("https://api.example.com/data")
        last = self.fetcher.get_last_result()
        assert last is not None
        assert last.url == "https://api.example.com/data"


class TestDataFetcherFetchMultiple:
    def setup_method(self):
        self.fetcher = DataFetcher()

    # This test FAILS due to the race condition bug
    @pytest.mark.asyncio
    async def test_should_fetch_multiple_urls_and_return_all_results_correctly(self):
        urls = [
            "https://api.example.com/a",
            "https://api.example.com/b",
            "https://api.example.com/c",
        ]

        results = await self.fetcher.fetch_multiple(urls)

        assert len(results) == 3

        # BUG: Due to the race condition, results may all contain the same
        # last_result instead of different results for each URL
        result_urls = sorted(r.url for r in results)
        assert result_urls == [
            "https://api.example.com/a",
            "https://api.example.com/b",
            "https://api.example.com/c",
        ]

    @pytest.mark.asyncio
    async def test_should_have_unique_data_for_each_url(self):
        urls = [
            "https://api.example.com/x",
            "https://api.example.com/y",
        ]

        results = await self.fetcher.fetch_multiple(urls)

        # BUG: Due to race condition, both results might have the same data
        unique_data = set(r.data for r in results)
        assert len(unique_data) == 2


class TestDataFetcherClearCache:
    def setup_method(self):
        self.fetcher = DataFetcher()

    @pytest.mark.asyncio
    async def test_should_clear_cache_and_last_result(self):
        await self.fetcher.fetch_data("https://api.example.com/data")
        self.fetcher.clear_cache()
        assert self.fetcher.get_last_result() is None
