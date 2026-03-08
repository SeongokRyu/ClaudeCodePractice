# Challenge: Bug Debugging

## Step 1: Bug 1 — Logic Bug

The event scheduler in `src/event_scheduler.py` has an **off-by-one error** in the date range check.

```bash
uv run pytest src/test_event_scheduler.py
```

Running the tests will show most passing, but one boundary test fails.

### Prompts to Try with Claude

```
When I run src/test_event_scheduler.py, some tests fail.
Check the failing tests and trace the execution flow line by line
to find the root cause.
```

---

## Step 2: Bug 2 — Async Bug

The data fetcher in `src/data_fetcher.py` has a **race condition**. It fails to properly manage shared mutable state, causing issues with concurrent calls.

```bash
uv run pytest src/test_data_fetcher.py
```

### Prompts to Try with Claude

```
There's a race condition bug in src/data_fetcher.py.
Draw a timeline showing the execution order when
multiple requests come in simultaneously.
```

---

## Step 3: Bug 3 — Type Bug

The config parser in `src/config_parser.py` **incorrectly converts the string "false" to True**. This is a subtle bug caused by Python's truthy/falsy evaluation.

```bash
uv run pytest src/test_config_parser.py
```

### Prompts to Try with Claude

```
Boolean value parsing is broken in src/config_parser.py.
This is related to Python's type coercion.
Trace step by step how the "false" string is being processed.
```

---

## Step 4: Execution Trace Request

For each bug, ask Claude for an execution trace.

### Prompts to Try with Claude

```
Trace the execution flow step by step for the following function call:

scheduler.get_events_in_range(datetime(2024, 3, 1), datetime(2024, 3, 31))

Show how the variable values change at each step.
```

---

## Step 5: Root Cause Analysis

Ask Claude for a **root cause fix, not just a symptom fix**.

### Prompts to Try with Claude

```
For each of these 3 bugs:
1. What is the symptom?
2. What is the root cause?
3. What is the difference between fixing the symptom vs. fixing the root cause?

Explain each one, apply the root cause fix,
and verify that all tests pass.
```

---

## Completion Criteria

- [ ] Bug 1 (off-by-one): Understood and fixed the root cause
- [ ] Bug 2 (race condition): Understood the race condition timeline
- [ ] Bug 3 (type coercion): Understood the type coercion issue
- [ ] All tests pass (`uv run pytest src/`)
- [ ] Can explain the difference between "symptom" and "root cause" for each bug

## Reflection Questions

1. How did the quality of answers differ between asking Claude "why does it fail?" vs. "trace the execution flow"?
2. Which of the three bug types was the hardest to find?
3. How would you use Claude when you encounter similar bugs in real projects?
