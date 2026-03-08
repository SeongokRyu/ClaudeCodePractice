# Context Budget Template

## Overview

A context budget plans how tokens are allocated across different sources in a Claude Code session.
Effective budgeting ensures the most important information is always present while deferring details until needed.

## Budget Allocation

| Category | Token Budget | Priority | Load Strategy | Notes |
|----------|-------------|----------|---------------|-------|
| System prompt | ~1,500 | Fixed | Always loaded | Cannot change, built into Claude Code |
| CLAUDE.md | 500-800 | High | Always loaded | Core project rules, keep concise |
| Path-scoped rules | 200-400 each | Medium | Conditional | Loaded when matching files are accessed |
| @import docs | 1,000-2,000 each | Low | On demand | Only loaded when Claude determines relevance |
| File reads | 2,000-5,000 | Variable | On demand | Read only what's needed for the task |
| Conversation history | Remaining | Variable | Automatic | Grows with session length |

## Token Estimates by Content Type

| Content | Approx Tokens | Example |
|---------|--------------|---------|
| 1 line of code | 10-15 tokens | `const x = await fetch(url);` |
| 1 paragraph of text | 50-80 tokens | A 3-sentence explanation |
| Small file (~50 lines) | 500-800 tokens | A utility module |
| Medium file (~200 lines) | 2,000-3,000 tokens | A React component |
| Large file (~500 lines) | 5,000-8,000 tokens | A service class |
| CLAUDE.md (verbose) | 2,000-3,000 tokens | The verbose-claude.md example |
| CLAUDE.md (optimized) | 400-600 tokens | The optimized-claude.md example |

## Budget Planning Process

### 1. Identify fixed costs
- System prompt: ~1,500 tokens (always present)
- CLAUDE.md: measure your current version

### 2. Identify conditional costs
- How many path-scoped rules do you have?
- How many @import documents exist?
- What's the average size of files Claude reads?

### 3. Calculate remaining budget
```
Effective budget = 40,000 tokens (practical attention window)
Fixed costs = system prompt + CLAUDE.md
Conditional = sum of rules and imports that might load
Remaining = Effective budget - Fixed - Conditional
```

### 4. Optimize if over budget
- Can CLAUDE.md be more concise?
- Can any rule be split into path-scoped rules?
- Can any large document be split for partial loading?
- Are there files being read that don't need to be?

## My Project Budget

Fill in your actual numbers:

| Category | Actual Tokens | % of Budget | Optimized? |
|----------|--------------|-------------|------------|
| System prompt | _____ | ___% | N/A |
| CLAUDE.md | _____ | ___% | [ ] |
| Rules (frontend) | _____ | ___% | [ ] |
| Rules (backend) | _____ | ___% | [ ] |
| Rules (testing) | _____ | ___% | [ ] |
| API reference | _____ | ___% | [ ] |
| Architecture doc | _____ | ___% | [ ] |
| Avg file read | _____ | ___% | [ ] |
| **Total (typical session)** | **_____** | **___%** | |

## Optimization Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| CLAUDE.md tokens | _____ | _____ | ___% |
| Avg session tokens | _____ | _____ | ___% |
| Task completion quality | ___/5 | ___/5 | |
| Unnecessary file reads | _____ | _____ | ___% |
