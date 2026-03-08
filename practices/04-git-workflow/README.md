# Practice 04: Git Workflow

## Goal

Learn safe Git workflows with Claude Code -- master commits, branches, PRs, and safe practices.

## Why This Matters

Safe Git habits prevent data loss when working with AI agents. Claude can automate Git operations, but you need to understand proper workflows.

## Prerequisites

- Practice 01 (Golden Workflow) completed

## Time

20-30 minutes

## What You'll Learn

1. **Creating backup branches** -- Building a safety net before making changes
2. **Descriptive commit messages** -- How to ask Claude to commit
3. **Feature branches** -- Creating branches and implementing new features
4. **Writing PR descriptions** -- How to summarize changes
5. **Using /rewind** -- Reverting changes

## Getting Started

```bash
cd practices/04-git-workflow
uv sync
uv run pytest
```

**Important**: A Git repository must be initialized for this exercise.
If it is not yet a Git repository:

```bash
cd /path/to/ClaudeCodePractice
git init
git add .
git commit -m "Initial commit"
```

Confirm that tests pass, then follow the step-by-step instructions in `CHALLENGE.md`.

## Key Concepts

### Backup Branches

Always create a backup branch before making changes:

```
Before making changes, please create a backup branch named backup/before-refactor.
```

### Descriptive Commits

When asking Claude to commit:

```
Commit the changes so far with a descriptive commit message.
```

### /rewind

When you want to revert Claude's changes:

```
/rewind
```

A list of previous checkpoints will be displayed, and you can revert to the desired point.
