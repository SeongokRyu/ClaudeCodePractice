# Challenge: Multi-Session Workflow

## Step 1: Writer/Reviewer Pattern

One session writes the code, and another session reviews it.

### Preparation

Open 2 terminals.

### Terminal 1 — Writer Session

```bash
claude
```

Request to the Writer:

```
Implement a SlidingWindowRateLimiter class that implements the RateLimiter
interface from src/rate_limiter_interface.py.

Requirements:
- Use sliding window algorithm
- Implement in src/sliding_window_limiter.py
- All tests must pass
```

### Terminal 2 — Reviewer Session

After the Writer has written the code, request to the Reviewer:

```bash
claude
```

```
Please review src/sliding_window_limiter.py.

Evaluate from the following perspectives:
1. Correctness: Is the sliding window algorithm implemented correctly?
2. Edge cases: Concurrent requests, window boundaries, 0 limit, etc.
3. Performance: Memory leak potential, O(n) complexity check
4. Type safety: Are Python type hints appropriate?

Provide specific improvement suggestions with code.
```

### Checklist
- [ ] Does the Writer's code pass all tests?
- [ ] Did the Reviewer find issues the Writer missed?
- [ ] Was the code improved by incorporating the Reviewer's feedback?

---

## Step 2: Competing Prototypes Pattern

Solve the same problem in two different ways and compare.

### Problem Definition

Read `src/problem.md`. Implement the Rate Limiter in two ways:
- **Approach 1**: Sliding Window
- **Approach 2**: Token Bucket

### Terminal 1 — Sliding Window

```bash
claude
```

```
Read the requirements in src/problem.md and implement the
RateLimiter using the Sliding Window approach.

- File: src/sliding_window_limiter.py
- Implement the interface from src/rate_limiter_interface.py
- Must pass the tests in src/test_rate_limiter.py
- Explain the rationale for implementation choices in comments
```

### Terminal 2 — Token Bucket

```bash
claude
```

```
Read the requirements in src/problem.md and implement the
RateLimiter using the Token Bucket approach.

- File: src/token_bucket_limiter.py
- Implement the interface from src/rate_limiter_interface.py
- Must pass the tests in src/test_rate_limiter.py
- Explain the rationale for implementation choices in comments
```

### Comparative Analysis

Once both implementations are complete, compare them in a new session:

```
Compare and analyze src/sliding_window_limiter.py and src/token_bucket_limiter.py
based on the following criteria:

1. Correctness: Do both implementations pass the tests?
2. Memory efficiency: Which one uses less memory?
3. Time complexity: What is the Big-O of each operation?
4. Burst traffic: How does each respond to sudden large volumes of requests?
5. Suitable use cases: In what situations is each approach more appropriate?

Please organize as a table.
```

### Checklist
- [ ] Do both implementations pass the same tests?
- [ ] Are the pros and cons of each implementation clearly evident?
- [ ] Do you understand which implementation is more suitable in which situations?

---

## Step 3: TDD Ping-Pong Pattern

Session A writes failing tests, then Session B implements.

### Round 1

**Terminal 1 (Test Writer)**:

```
Write 3 failing tests for the RateLimiter interface
from src/rate_limiter_interface.py.

- File: src/test_tdd_limiter.py
- Basic functionality: isAllowed returns true within the limit
- Edge case: Always returns false when limit is 0
- Time elapsed: Allows again after windowMs has passed

Write tests only — do not implement.
```

**Terminal 2 (Implementer)**:

```
Implement TddRateLimiter to pass the 3 failing tests
in src/test_tdd_limiter.py.

- File: src/tdd_limiter.py
- Pass the tests with minimal code
- Verify with uv run pytest after implementation
```

### Round 2

**Terminal 1 (Test Writer)**:

```
Add 3 more tests to src/test_tdd_limiter.py.

- Concurrent requests: When 100 requests are sent simultaneously
- Multiple keys: Independent limiting for different keys
- Reset: Count resets after calling reset()
```

**Terminal 2 (Implementer)**:

```
Update src/tdd_limiter.py to pass the newly added tests
in src/test_tdd_limiter.py.
```

### Checklist
- [ ] In each round, do tests fail first and pass after implementation?
- [ ] Does the implementation contain only the minimal code needed for the tests?
- [ ] Does the implementation become more robust with each round?

---

## Step 4: Specialist Team Pattern

Split sessions by specialized domain for parallel work.

### Scenario

Complete a Rate Limiter service. 3 specialist sessions work in parallel.

### Terminal 1 — Backend Specialist

```
Implement the Rate Limiter backend.

1. src/rate_limiter_service.py — HTTP server
   - POST /check — { key, limit, windowMs } → { allowed, remaining, retryAfter }
   - GET /stats — overall statistics
   - DELETE /reset/:key — reset a specific key

2. Use sliding window algorithm
3. In-memory storage
```

### Terminal 2 — Frontend Specialist

```
Implement the Rate Limiter dashboard UI.

1. src/dashboard.html — single HTML file
   - Real-time rate limit status display
   - Send request button
   - Remaining requests count, reset time display
   - Simple chart (CSS bar graph)

2. Use Vanilla JS/HTML/CSS only (no frameworks)
3. Communicate with backend using fetch API
```

### Terminal 3 — Test Specialist

```
Write integration tests for the Rate Limiter service.

1. src/test_rate_limiter_service.py
   - Tests per API endpoint
   - Rate limit works correctly
   - Resets after window elapses
   - Concurrent request handling
   - Error handling (invalid input)

2. Each test must be independently runnable
```

### Integration

After all sessions' work is complete:

```
Verify the integration of results from the three specialist sessions:
1. Start the backend service
2. Run the integration tests
3. Confirm the dashboard communicates correctly with the backend
```

### Checklist
- [ ] Did each Specialist focus only on their own domain?
- [ ] Did they communicate through interfaces (API specs)?
- [ ] Were there no major issues when integrating?

---

## Success Criteria

- [ ] Improved code quality using the Writer/Reviewer pattern
- [ ] Selected the optimal implementation using Competing Prototypes
- [ ] Wrote robust code using TDD Ping-Pong
- [ ] Performed parallel development using the Specialist Team pattern

## Key Takeaways

1. **Role separation**: Separating writing and reviewing improves quality
2. **Diverse perspectives**: Solving the same problem in different ways helps find the best solution
3. **Incremental development**: TDD Ping-Pong ensures code that always works
4. **Specialization**: Efficiency increases when each session focuses on its specialized domain
5. **Interface-centric**: The key to multi-session is clear interfaces (contracts)
