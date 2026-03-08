export interface FetchResult {
  url: string;
  data: string;
  timestamp: number;
}

// Simulated async data source
async function simulateFetch(url: string): Promise<string> {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(`Data from ${url}`);
    }, 10);
  });
}

// Simulated async logging (e.g., writing to a log service)
async function logAccess(url: string): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(() => resolve(), 5);
  });
}

export class DataFetcher {
  // BUG: shared mutable state — lastResult is overwritten by concurrent calls
  private lastResult: FetchResult | null = null;
  private cache: Map<string, FetchResult> = new Map();

  // BUG: race condition — this method updates shared state without proper synchronization
  // When called concurrently, the lastResult and cache may be inconsistent
  async fetchData(url: string): Promise<FetchResult> {
    // Check cache first
    if (this.cache.has(url)) {
      this.lastResult = this.cache.get(url)!;
      return this.lastResult;
    }

    // BUG: Between this point and setting lastResult below,
    // another call can overwrite lastResult
    const data = await simulateFetch(url);

    const result: FetchResult = {
      url,
      data,
      timestamp: Date.now(),
    };

    // BUG: these two operations are not atomic
    // Another concurrent call may have already changed lastResult
    this.lastResult = result;
    this.cache.set(url, result);

    return result;
  }

  // BUG: fetchMultiple uses shared mutable state (this.lastResult)
  // and yields to the event loop between fetchData and reading lastResult
  async fetchMultiple(urls: string[]): Promise<FetchResult[]> {
    const results: FetchResult[] = [];

    // BUG: All fetches start concurrently
    const promises = urls.map(async (url) => {
      await this.fetchData(url);
      // BUG: This await yields control to the event loop, allowing other
      // concurrent fetchData calls to overwrite this.lastResult
      await logAccess(url);
      // BUG: by now, this.lastResult has likely been overwritten
      // by another concurrent fetch that completed while we were logging
      results.push(this.lastResult!);
    });

    await Promise.all(promises);
    return results;
  }

  getLastResult(): FetchResult | null {
    return this.lastResult;
  }

  clearCache(): void {
    this.cache.clear();
    this.lastResult = null;
  }
}
