# Challenge: 품질 게이트 파이프라인

## Step 1: Design the Pipeline

Plan a quality gate pipeline with this flow:

```
Code Change
    |
    v
[Gate 1: Tests]     -- npm test must pass
    |
    v
[Gate 2: Lint]      -- eslint + tsc must have zero errors
    |
    v
[Gate 3: Security]  -- no known vulnerability patterns
    |
    v
[Gate 4: Review]    -- LLM-as-judge scores >= 3/5
    |
    v
APPROVED
```

Rules:
- Each gate is a shell script that exits 0 (pass) or non-zero (fail)
- The pipeline stops at the first failure (fail-fast)
- Each gate logs its results to stdout
- The gate runner collects all results and produces a summary

## Step 2: Gate 1 — Automated Tests

Create `gate-test.sh` that runs the project's test suite.

Requirements:
- Run `npm test` (or `npx jest`)
- Capture the exit code
- Parse test results: total, passed, failed, skipped
- Exit 0 if all tests pass, exit 1 if any fail
- Output a structured summary

Example output:
```
[GATE: TESTS] Running test suite...
[GATE: TESTS] Results: 42 passed, 0 failed, 2 skipped
[GATE: TESTS] PASSED
```

## Step 3: Gate 2 — Lint and Type Check

Create `gate-lint.sh` that runs eslint and TypeScript compiler.

Requirements:
- Run `npx eslint . --ext .ts,.tsx` and capture errors
- Run `npx tsc --noEmit` and capture type errors
- Exit 0 only if BOTH have zero errors
- Warnings are acceptable (don't fail on warnings)
- Output error counts for each tool

Example output:
```
[GATE: LINT] Running ESLint...
[GATE: LINT] ESLint: 0 errors, 3 warnings
[GATE: LINT] Running TypeScript compiler...
[GATE: LINT] TypeScript: 0 errors
[GATE: LINT] PASSED
```

## Step 4: Gate 3 — Security Scan

Create `gate-security.sh` that checks for common security vulnerabilities.

Patterns to detect:
- Hardcoded secrets: `password = "..."`, `api_key = "..."`, `secret = "..."`
- SQL injection: string concatenation in SQL queries
- XSS vulnerabilities: `innerHTML`, `dangerouslySetInnerHTML` without sanitization
- Insecure dependencies: `eval()`, `exec()` with user input
- Exposed debug info: `console.log` with sensitive data patterns
- Insecure HTTP: `http://` URLs (should be `https://`)
- Weak crypto: `md5`, `sha1` for password hashing

Requirements:
- Scan all `.ts`, `.tsx`, `.js`, `.jsx` files in the project
- Report each finding with file path and line number
- Classify findings: CRITICAL, HIGH, MEDIUM, LOW
- Exit 1 if any CRITICAL or HIGH findings
- Exit 0 if only MEDIUM/LOW findings (with warnings)

## Step 5: Gate 4 — LLM-as-Judge Review

Create `gate-review.sh` that uses Claude as a quality reviewer.

Requirements:
1. Collect the git diff of staged changes
2. Send the diff to `claude -p` with the quality judge prompt
3. Parse the response for a quality score (1-5)
4. Exit 0 if score >= 3, exit 1 if score < 3
5. Include the full review in the output

The quality judge prompt (`agents/quality-judge.md`) should evaluate:
- Code correctness
- Naming and readability
- Error handling
- Test coverage of the change
- Adherence to project conventions

Score rubric:
- 5: Excellent — production-ready, no issues
- 4: Good — minor improvements possible, approve
- 3: Acceptable — some issues, but approve with notes
- 2: Needs work — significant issues, do not approve
- 1: Reject — fundamental problems, rewrite needed

## Step 6: Wire All Gates Together

Create `gate-runner.sh` that executes all gates sequentially.

Requirements:
- Run each gate in order
- Stop at the first failure
- Track timing for each gate
- Produce a final summary report

Example output:
```
====================================
Quality Gate Pipeline
====================================

[1/4] Tests ............ PASSED (12s)
[2/4] Lint ............. PASSED (8s)
[3/4] Security ......... PASSED (3s)
[4/4] Review ........... PASSED (25s) [Score: 4/5]

====================================
PIPELINE RESULT: ALL GATES PASSED
Total time: 48s
====================================
```

Wire the pipeline into hooks (`settings/quality-gates.json`) so it runs automatically before every commit.

## Bonus: Python Agent SDK Implementation

Implement the full pipeline in Python using the Agent SDK (`python/quality_pipeline.py`).

Benefits of the Python version:
- Structured error handling with try/except
- Async gate execution where possible
- Rich logging with the logging module
- Type-safe gate results with dataclasses
- Easier to extend with new gates

## Success Criteria

- [ ] All four gates are independently executable and testable
- [ ] Gate runner executes all gates in sequence with fail-fast
- [ ] LLM-as-judge produces structured quality scores
- [ ] Security scan detects common vulnerability patterns
- [ ] Pipeline summary report is clear and informative
- [ ] Hooks configuration runs the pipeline on commit
