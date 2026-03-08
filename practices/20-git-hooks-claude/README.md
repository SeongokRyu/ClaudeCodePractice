# Practice 20: Git Hooks + Claude

## Goal

Learn to integrate Claude Code with Git hooks for automated security checks, commit message validation, and pre-push testing. Also explore Claude Code's own hook system for intercepting tool usage.

## Prerequisites

- [Practice 06: Hooks](../06-hooks/) — Claude Code hooks basics
- [Practice 19: Headless Mode](../19-headless-mode/) — `claude -p` fundamentals

## Time

60-90 minutes

## Difficulty

★★☆ (Intermediate)

## What You'll Learn

1. **Pre-commit hooks** — Automated secret scanning before every commit
2. **Commit-msg hooks** — Validating commit messages follow conventions
3. **Pre-push hooks** — Running tests before pushing
4. **Claude Code hooks** — Intercepting Claude's own git operations via PreToolUse/PostToolUse
5. **Integration patterns** — Combining Git hooks with Claude headless mode

## Key Concepts

### Git Hooks

Git hooks are scripts that run at specific points in the Git workflow:
- `pre-commit` — Before a commit is created (can reject the commit)
- `commit-msg` — After message is written (can modify or reject it)
- `pre-push` — Before pushing to remote (can reject the push)

### Claude Code Hooks

Claude Code has its own hook system that intercepts tool usage:
- `PreToolUse` — Runs before Claude uses a tool (can block the tool call)
- `PostToolUse` — Runs after a tool completes (can modify results)
- Configured in `.claude/settings.json`

### Secret Detection Patterns

Common patterns to catch:
- API keys (`[A-Za-z0-9]{32,}`)
- AWS keys (`AKIA[0-9A-Z]{16}`)
- Private keys (`-----BEGIN.*PRIVATE KEY-----`)
- Passwords in code (`password\s*=\s*['"][^'"]+['"]`)

## Directory Structure

```
20-git-hooks-claude/
├── README.md
├── CHALLENGE.md
└── src/
    ├── hooks/
    │   ├── pre-commit          # Secret scanning hook
    │   ├── commit-msg          # Commit message validation
    │   └── pre-push            # Pre-push test runner
    ├── claude-hooks/
    │   └── settings-example.json   # Claude Code hooks config
    ├── example-code/
    │   ├── app.ts              # Code WITH embedded secrets (for testing)
    │   └── safe-app.ts         # Same code using env variables
    └── README.md               # Installation guide
```
