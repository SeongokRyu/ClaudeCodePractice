import { DataFetcher } from './data-fetcher';

describe('DataFetcher', () => {
  let fetcher: DataFetcher;

  beforeEach(() => {
    fetcher = new DataFetcher();
  });

  describe('fetchData', () => {
    it('should fetch data from a URL', async () => {
      const result = await fetcher.fetchData('https://api.example.com/data');
      expect(result.url).toBe('https://api.example.com/data');
      expect(result.data).toBe('Data from https://api.example.com/data');
      expect(result.timestamp).toBeDefined();
    });

    it('should cache results', async () => {
      const result1 = await fetcher.fetchData('https://api.example.com/data');
      const result2 = await fetcher.fetchData('https://api.example.com/data');
      expect(result1.timestamp).toBe(result2.timestamp);
    });

    it('should update lastResult', async () => {
      await fetcher.fetchData('https://api.example.com/data');
      const last = fetcher.getLastResult();
      expect(last).not.toBeNull();
      expect(last!.url).toBe('https://api.example.com/data');
    });
  });

  describe('fetchMultiple', () => {
    // This test FAILS due to the race condition bug
    it('should fetch multiple URLs and return all results correctly', async () => {
      const urls = [
        'https://api.example.com/a',
        'https://api.example.com/b',
        'https://api.example.com/c',
      ];

      const results = await fetcher.fetchMultiple(urls);

      expect(results).toHaveLength(3);

      // BUG: Due to the race condition, results may all contain the same
      // lastResult instead of different results for each URL
      const resultUrls = results.map((r) => r.url).sort();
      expect(resultUrls).toEqual([
        'https://api.example.com/a',
        'https://api.example.com/b',
        'https://api.example.com/c',
      ]);
    });

    it('should have unique data for each URL', async () => {
      const urls = [
        'https://api.example.com/x',
        'https://api.example.com/y',
      ];

      const results = await fetcher.fetchMultiple(urls);

      // BUG: Due to race condition, both results might have the same data
      const uniqueData = new Set(results.map((r) => r.data));
      expect(uniqueData.size).toBe(2);
    });
  });

  describe('clearCache', () => {
    it('should clear cache and lastResult', async () => {
      await fetcher.fetchData('https://api.example.com/data');
      fetcher.clearCache();
      expect(fetcher.getLastResult()).toBeNull();
    });
  });
});
