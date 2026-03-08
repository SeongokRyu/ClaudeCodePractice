# Practice 16: Multi-Session Workflow

## Goal

Learn 8 multi-session patterns. Practice parallel work patterns such as Writer/Reviewer, Competing Prototypes, TDD Ping-Pong, and Specialist Team by utilizing two or more Claude sessions simultaneously.

## Prerequisites

- Practice 13 (Subagents) completed

## Time

45-60 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

- Writer/Reviewer pattern: Separating writing and reviewing
- Competing Prototypes pattern: Solving the same problem in different ways
- TDD Ping-Pong pattern: Separating test writing and implementation
- Specialist Team pattern: Running sessions by specialized domain

## Key Concepts

### Why Multi-Session Is Needed

Limitations of a single session:
- Context window exhaustion
- Getting stuck on a single perspective
- Quality degradation due to role mixing

Advantages of multi-session:
- Higher quality through role separation
- Verification from diverse perspectives
- Time savings through parallel work

### 4 Core Patterns

```
1. Writer/Reviewer     2. Competing Prototypes
   Session A: Write       Session A: Approach 1
   Session B: Review      Session B: Approach 2
                          → Compare and choose the best

3. TDD Ping-Pong       4. Specialist Team
   Session A: Tests        Session A: Frontend
   Session B: Implement    Session B: Backend
   → Repeat                Session C: Tests
                           → Parallel work
```

## Setup

```bash
uv sync
```

## Getting Started

1. Open `CHALLENGE.md` and follow the step-by-step exercises
2. Solve the problem defined in `src/problem.md` using multiple sessions
3. Implement the interface in `src/rate_limiter_interface.py`
