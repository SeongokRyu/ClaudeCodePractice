# Practice 31: 컨텍스트 엔지니어링

## Goal

Design information environments, not just prompts. Learn to provide the minimum number of high-signal tokens, use progressive disclosure to load context only when needed, and measure the impact of context optimization on agent performance.

## Prerequisites

- **Practice 05**: CLAUDE.md (understanding project-level context files)

## Time

90-120 minutes

## Difficulty

★★★

## What You Will Learn

1. How to audit and measure context usage (tokens per session)
2. How to optimize CLAUDE.md for signal-to-noise ratio
3. How to use path-scoped rules to load context conditionally
4. How to use `@import` for progressive disclosure of detailed documentation
5. How to design a context budget across system prompt, CLAUDE.md, file reads, and conversation
6. How to compare performance between optimized and unoptimized contexts

## Key Concepts

- **Context engineering** is about designing the information environment an agent operates in, not just the prompt you give it.
- **Token budget**: Every token in context costs money, adds latency, and competes for attention. Less is more.
- **Signal-to-noise ratio**: High-signal context (precise rules, examples) outperforms verbose explanations.
- **Progressive disclosure**: Start with essentials, load details only when the agent works on relevant files.
- **Path-scoped rules**: Rules in `.claude/rules/` can be loaded only when specific file paths are accessed.

## Structure

```
src/
  context-audit/
    verbose-claude.md      # Verbose CLAUDE.md (150+ lines)
    optimized-claude.md    # Optimized version (40 lines, same rules)
    rules/
      frontend.md          # Path-scoped rule for frontend files
      backend.md           # Path-scoped rule for backend files
      testing.md           # Path-scoped rule for test files
    imports/
      api-reference.md     # Importable API reference doc
      architecture.md      # Importable architecture doc
  context-budget.md        # Template for planning context budget
```

## Tips

- Measure first: know your current token usage before optimizing
- The goal is not fewer words, but higher information density
- Path-scoped rules are one of the most powerful context optimization tools
- Test the same task with both verbose and optimized context to see real differences
