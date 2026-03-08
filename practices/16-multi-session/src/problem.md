# Problem: Rate Limiter Implementation

## Requirements

Implement a Rate Limiter that restricts API request rates.

### Functional Requirements

1. **Determine whether a request is allowed** (`isAllowed`)
   - Determine whether a request is allowed for a given key (e.g., IP address, API key)
   - Deny if the maximum number of requests is exceeded within the specified time window

2. **Query remaining requests** (`getRemainingRequests`)
   - Return the number of remaining allowed requests in the current time window

3. **Reset count** (`reset`)
   - Reset the request count for a specific key

### Non-Functional Requirements

- Must be memory efficient
- O(1) or O(log n) time complexity
- Thread-safe (safe for concurrent access)
- Old data must be automatically cleaned up over time

## Comparison of Two Approaches

### Approach 1: Sliding Window

```
Time ────────────────────────────────►
     [──── Window ────]
         ↑ Count requests within the current window
              [──── Window ────]
                   ↑ Window slides
```

**Pros**: Precise limiting, uniform traffic distribution
**Cons**: Must store timestamps for each request (high memory usage)

### Approach 2: Token Bucket

```
Bucket: [●●●●●] (max 5 tokens)
Request → consume token: [●●●●○]
Request → consume token: [●●●○○]
Time passes → refill token: [●●●●○]
```

**Pros**: Memory efficient (only 2 numbers per key), allows bursts
**Cons**: Bursts can occur at window boundaries

## Interface

Implement the `RateLimiter` interface defined in `src/rate-limiter-interface.ts`.

## Tests

Must pass the tests defined in `src/rate-limiter.test.ts`.
Both implementations must pass the same test suite.

## Evaluation Criteria

| Criterion | Score |
|-----------|-------|
| All tests pass | 40 points |
| Edge case handling | 20 points |
| Memory efficiency | 15 points |
| Time complexity | 15 points |
| Code readability | 10 points |
