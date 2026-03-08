# Practice 10: Bug Debugging

## Objective

Learn how to debug bugs together with Claude. Practice root cause analysis rather than just fixing symptoms, and learn 15 systematic debugging strategies for various types of bugs.

## Prerequisites

- Practice 05 (CLAUDE.md) completed
- Basic understanding of Python and pytest

## Estimated Time

45-60 minutes

## Key Concepts

### 3 Types of Bugs

1. **Logic Bug** - Code runs but produces incorrect results (off-by-one, etc.)
2. **Async Bug** - Asynchronous execution order issues, race conditions
3. **Type Bug** - Incorrect type conversions or wrong type assumptions

### Claude Debugging Strategies

- **Execution Trace**: "Trace through this code line by line"
- **Root Cause Analysis**: "Find the root cause, not just the symptom"
- **Hypothesis Testing**: "Suggest 3 possible causes for this bug and verify each one"
- **Minimal Reproduction**: "Write the smallest possible test that reproduces this bug"

## Getting Started

```bash
cd practices/10-bug-debugging
uv sync
uv run pytest src/
```

Running the tests will show some test failures. Each file contains intentionally planted bugs.

Now follow the steps in `CHALLENGE.md` to practice debugging with Claude.

## Learning Points

- Asking Claude "trace the execution flow" yields better results than "why does it fail"
- You learn to distinguish between root causes and symptoms
- Async bugs are especially easier to understand when you visualize the execution order
- Type coercion bugs are the hardest to find
