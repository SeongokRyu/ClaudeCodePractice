# Practice 33: 품질 게이트 파이프라인

## Goal

Build a verification pipeline with quality gates -- automated tests, lint/type checks, LLM-as-judge review, and security scanning. Each gate must pass before the pipeline proceeds, ensuring every change meets quality standards.

## Prerequisites

- **Practice 30**: Deterministic Guardrails (hooks configuration)
- **Practice 25**: Custom Subagents (agent orchestration)

## Time

90-120 minutes

## Difficulty

★★★

## What You Will Learn

1. How to design a multi-gate quality pipeline
2. How to use shell scripts as individual quality gates
3. How to use `claude -p` as an LLM-as-judge for quality scoring
4. How to scan for common security vulnerabilities with pattern matching
5. How to wire gates together so any failure blocks the pipeline
6. How to implement the same pipeline in Python with the Agent SDK

## Key Concepts

- **Quality gate**: a checkpoint that must pass before work proceeds. Like a toll booth -- no passage without approval.
- **Pipeline**: a sequence of gates where each depends on the previous passing.
- **LLM-as-judge**: using an AI model to evaluate the quality of another AI's output.
- **Fail-fast**: stop the pipeline at the first failure to save time and resources.
- **Exit codes**: each gate script exits 0 (pass) or non-zero (fail), making them composable.

## Structure

```
src/
  pipeline/
    gate-runner.sh       # Runs all gates sequentially
    gate-test.sh         # Gate 1: automated tests
    gate-lint.sh         # Gate 2: lint + type check
    gate-security.sh     # Gate 3: security scan
    gate-review.sh       # Gate 4: LLM-as-judge review
  agents/
    quality-judge.md     # Agent definition for quality scoring
  settings/
    quality-gates.json   # Hooks config enforcing gates on commit
  python/
    quality_pipeline.py  # Agent SDK implementation
```

## Tips

- Start with the simplest gate (tests) and add complexity gradually
- Each gate should be independently testable
- The LLM-as-judge gate is the most flexible but also the slowest -- put it last
- Security scanning with patterns catches common issues but is not a replacement for proper security tools
