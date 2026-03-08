/**
 * Rate Limiter Tests
 *
 * 이 테스트는 RateLimiter 인터페이스의 모든 구현이 통과해야 합니다.
 * Sliding Window와 Token Bucket 모두 이 테스트를 사용합니다.
 *
 * 사용법:
 *   테스트 파일에서 구현체를 import하고 createLimiter에 팩토리를 전달합니다.
 *   예: runRateLimiterTests("SlidingWindow", (config) => new SlidingWindowLimiter(config));
 */

import { RateLimiter, RateLimiterConfig } from "./rate-limiter-interface";

type LimiterFactory = (config: RateLimiterConfig) => RateLimiter;

export function runRateLimiterTests(
  name: string,
  createLimiter: LimiterFactory
): void {
  describe(`${name} RateLimiter`, () => {
    let limiter: RateLimiter;

    beforeEach(() => {
      limiter = createLimiter({ maxRequests: 5, windowMs: 1000 });
    });

    describe("isAllowed", () => {
      it("should allow requests within the limit", () => {
        for (let i = 0; i < 5; i++) {
          const result = limiter.isAllowed("user1");
          expect(result.allowed).toBe(true);
          expect(result.remaining).toBe(4 - i);
        }
      });

      it("should deny requests that exceed the limit", () => {
        for (let i = 0; i < 5; i++) {
          limiter.isAllowed("user1");
        }

        const result = limiter.isAllowed("user1");
        expect(result.allowed).toBe(false);
        expect(result.remaining).toBe(0);
        expect(result.retryAfterMs).toBeGreaterThan(0);
      });

      it("should track keys independently", () => {
        // Exhaust user1's limit
        for (let i = 0; i < 5; i++) {
          limiter.isAllowed("user1");
        }

        // user2 should still be allowed
        const result = limiter.isAllowed("user2");
        expect(result.allowed).toBe(true);
        expect(result.remaining).toBe(4);
      });

      it("should return retryAfterMs of 0 when allowed", () => {
        const result = limiter.isAllowed("user1");
        expect(result.retryAfterMs).toBe(0);
      });
    });

    describe("getRemainingRequests", () => {
      it("should return max requests for a new key", () => {
        const remaining = limiter.getRemainingRequests("newuser");
        expect(remaining).toBe(5);
      });

      it("should decrease after each allowed request", () => {
        limiter.isAllowed("user1");
        limiter.isAllowed("user1");
        expect(limiter.getRemainingRequests("user1")).toBe(3);
      });

      it("should return 0 when limit is reached", () => {
        for (let i = 0; i < 5; i++) {
          limiter.isAllowed("user1");
        }
        expect(limiter.getRemainingRequests("user1")).toBe(0);
      });

      it("should not count as a request (read-only)", () => {
        limiter.getRemainingRequests("user1");
        limiter.getRemainingRequests("user1");
        limiter.getRemainingRequests("user1");

        // Should still have all requests available
        expect(limiter.getRemainingRequests("user1")).toBe(5);
      });
    });

    describe("reset", () => {
      it("should reset a specific key", () => {
        for (let i = 0; i < 5; i++) {
          limiter.isAllowed("user1");
        }
        expect(limiter.getRemainingRequests("user1")).toBe(0);

        limiter.reset("user1");
        expect(limiter.getRemainingRequests("user1")).toBe(5);
      });

      it("should not affect other keys", () => {
        limiter.isAllowed("user1");
        limiter.isAllowed("user2");

        limiter.reset("user1");

        expect(limiter.getRemainingRequests("user1")).toBe(5);
        expect(limiter.getRemainingRequests("user2")).toBe(4);
      });

      it("should be safe to call on non-existent key", () => {
        expect(() => limiter.reset("nonexistent")).not.toThrow();
      });
    });

    describe("resetAll", () => {
      it("should reset all keys", () => {
        limiter.isAllowed("user1");
        limiter.isAllowed("user2");
        limiter.isAllowed("user3");

        limiter.resetAll();

        expect(limiter.getRemainingRequests("user1")).toBe(5);
        expect(limiter.getRemainingRequests("user2")).toBe(5);
        expect(limiter.getRemainingRequests("user3")).toBe(5);
      });
    });

    describe("time window", () => {
      it("should allow requests again after window expires", (done) => {
        // Use a short window for testing
        const shortLimiter = createLimiter({
          maxRequests: 2,
          windowMs: 100,
        });

        shortLimiter.isAllowed("user1");
        shortLimiter.isAllowed("user1");
        expect(shortLimiter.isAllowed("user1").allowed).toBe(false);

        // Wait for the window to expire
        setTimeout(() => {
          const result = shortLimiter.isAllowed("user1");
          expect(result.allowed).toBe(true);
          done();
        }, 150);
      });
    });

    describe("edge cases", () => {
      it("should handle zero maxRequests", () => {
        const zeroLimiter = createLimiter({
          maxRequests: 0,
          windowMs: 1000,
        });

        const result = zeroLimiter.isAllowed("user1");
        expect(result.allowed).toBe(false);
        expect(result.remaining).toBe(0);
      });

      it("should handle a single maxRequest", () => {
        const singleLimiter = createLimiter({
          maxRequests: 1,
          windowMs: 1000,
        });

        expect(singleLimiter.isAllowed("user1").allowed).toBe(true);
        expect(singleLimiter.isAllowed("user1").allowed).toBe(false);
      });

      it("should handle empty string key", () => {
        const result = limiter.isAllowed("");
        expect(result.allowed).toBe(true);
      });

      it("should handle many different keys", () => {
        for (let i = 0; i < 100; i++) {
          const result = limiter.isAllowed(`user-${i}`);
          expect(result.allowed).toBe(true);
          expect(result.remaining).toBe(4);
        }
      });
    });
  });
}

// Placeholder: Import your implementation and run the tests
// import { SlidingWindowLimiter } from "./sliding-window-limiter";
// runRateLimiterTests("SlidingWindow", (config) => new SlidingWindowLimiter(config));

// import { TokenBucketLimiter } from "./token-bucket-limiter";
// runRateLimiterTests("TokenBucket", (config) => new TokenBucketLimiter(config));

// Dummy test to prevent "no tests" error
describe("Rate Limiter Test Suite", () => {
  it("should have test runner ready", () => {
    expect(runRateLimiterTests).toBeDefined();
  });
});
