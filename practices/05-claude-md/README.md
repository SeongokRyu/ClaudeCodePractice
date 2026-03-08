# Practice 05: Writing CLAUDE.md

## Goal

Learn to write effective CLAUDE.md files. Understand what to include and exclude, the 200-line guideline, /init usage, and monorepo patterns.

## Prerequisites

- [Practice 01: Golden Workflow](../01-golden-workflow/)

## Time

30-45 minutes

## Why This Matters

> "An over-specified CLAUDE.md is too long — Claude ignores half."
> — Anthropic

CLAUDE.md is Claude Code's memory file. It is read at the start of every session and shapes how Claude behaves in your project. But more is not better. A bloated CLAUDE.md full of obvious advice ("write clean code", "use descriptive variable names") wastes context and dilutes the rules that actually matter.

An effective CLAUDE.md is:
- **Concise** — under 200 lines, ideally much shorter
- **Actionable** — specific commands, not vague principles
- **Non-obvious** — things Claude cannot infer from code alone
- **Hierarchical** — in monorepos, each package gets its own CLAUDE.md

## What You Will Learn

1. How `/init` generates a starting CLAUDE.md
2. What to include: bash commands, conventions, gotchas, test commands
3. What to exclude: obvious advice, verbose API docs, things readable from code
4. Monorepo pattern: root CLAUDE.md + package-level CLAUDE.md files

## Directory Structure

```
src/
├── example-bad/
│   └── CLAUDE.md          # Deliberately bad — too long, too obvious
├── example-good/
│   └── CLAUDE.md          # Good — concise, actionable, non-obvious
└── example-monorepo/
    ├── CLAUDE.md           # Root-level monorepo CLAUDE.md
    └── packages/
        ├── frontend/
        │   └── CLAUDE.md   # Frontend-specific rules
        └── backend/
            └── CLAUDE.md   # Backend-specific rules
```

## Key Concepts

### Include in CLAUDE.md
- Build/test/lint commands (`npm test`, `cargo build --release`)
- Non-obvious project conventions (naming, file structure)
- Git workflow rules (branch naming, commit message format)
- Known gotchas and workarounds
- Preferred libraries or patterns

### Exclude from CLAUDE.md
- Generic advice ("write clean code", "handle errors")
- Things Claude can read from package.json, tsconfig.json, etc.
- Full API documentation (link instead)
- Language tutorials
- Anything already enforced by linters or CI
