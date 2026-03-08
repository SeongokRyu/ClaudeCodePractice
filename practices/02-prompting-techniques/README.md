# Practice 02: Prompting Techniques

## Goal

Learn effective prompting techniques -- master verification criteria, the interview technique, and structured prompt writing.

## Why This Matters

> "Providing verification means is the single highest-leverage action you can take to improve Claude's output quality."
> -- Anthropic Official Documentation

There is a significant difference in output quality between simply telling Claude "fix this" and providing clear criteria and verification methods.

## Prerequisites

- Practice 01 (Golden Workflow) completed

## Time

20-30 minutes

## What You'll Learn

1. **Bad prompts vs good prompts** -- The difference between vague and specific requests
2. **Providing verification criteria** -- How to ask Claude for test verification alongside feature implementation
3. **Interview technique** -- How to get Claude to ask questions first
4. **Structured prompts** -- Role + Context + Constraints + Expected output + Verification

## Getting Started

```bash
cd practices/02-prompting-techniques
uv sync
uv run pytest
```

Confirm that tests pass, then follow the step-by-step instructions in `CHALLENGE.md`.

## Key Concepts

### Verification Criteria

When requesting work from Claude, also tell it "how to verify":

```
After implementation, run pytest to confirm all tests pass.
```

### Interview Technique

Ask Claude to ask questions first:

```
Before implementing this feature, please ask any questions you have about the requirements first.
```

### Structured Prompt

```
Role: Senior Python developer
Context: Improving error handling in the calculator module
Constraints: Do not break existing tests
Expected output: Modified code + new tests
Verification: All tests pass with pytest
```
