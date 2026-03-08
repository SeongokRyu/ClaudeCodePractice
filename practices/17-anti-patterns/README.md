# Practice 17: Experiencing the 7 Common Mistakes

## Goal

Intentionally experience common anti-patterns when using Claude Code, and learn the correct usage. By experiencing mistakes firsthand, you'll understand "why it doesn't work."

## Prerequisites

- Practice 01 (Golden Workflow) completed

## Time

45-60 minutes

## Difficulty

★★☆ (Intermediate)

## What You'll Learn

- Blind Trust: The danger of uncritically accepting Claude's code
- Kitchen Sink Session: The problem of doing too many tasks in one session
- Over-specified CLAUDE.md: The problem of overly long configuration files
- No Verification: The danger of developing without tests
- Scope Creep: The problem of adding features without structure

## Key Concepts

### The 7 Common Mistakes

| # | Anti-Pattern | Symptom | Solution |
|---|-------------|---------|----------|
| 1 | Blind Trust | Overlooking security vulnerabilities | Always review code |
| 2 | Kitchen Sink | Session quality degradation | 1 session per task |
| 3 | Over-specified | Rules get ignored | Keep CLAUDE.md under 30 lines |
| 4 | No Verification | Hidden bugs | TDD workflow |
| 5 | Scope Creep | Spaghetti code | Design structure upfront |
| 6 | Copy-Paste Prompt | Context loss | Conversational iteration |
| 7 | Ignoring Warnings | Technical debt | Resolve warnings immediately |

### Philosophy of This Practice

> "Don't fear mistakes — experience them directly in a safe environment"

Intentionally execute each anti-pattern, observe the results, then compare with the correct approach.

## Setup

```bash
uv sync
```

## Getting Started

1. Open `CHALLENGE.md` and follow the step-by-step exercises
2. Intentionally problematic code is prepared in the `src/` directory
3. In each step, first experience the "wrong way," then apply the "correct way"
