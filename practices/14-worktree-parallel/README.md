# Practice 14: Worktree Parallel Development

## Goal

Learn the parallel development workflow using Git worktrees. Learn how to develop multiple features simultaneously on independent branches using the `claude --worktree` option.

## Prerequisites

- Practice 13 (Subagents) completed

## Time

45-60 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

- The concept and mechanics of Git worktrees
- Working on independent branches in parallel with the `claude --worktree` option
- Developing different features simultaneously in multiple terminals
- The workflow for merging worktree-based branches via PRs

## Key Concepts

### What is a Git Worktree?

A feature that allows you to check out multiple working directories (working trees) simultaneously from a single Git repository.

```
my-project/              (main branch)
├── .git/
├── src/
└── ...

my-project-feature-auth/  (feature-auth branch - worktree)
├── src/
└── ...

my-project-feature-log/   (feature-logging branch - worktree)
├── src/
└── ...
```

### claude --worktree Workflow

```
Terminal 1: claude --worktree feature-auth
  → Automatically creates new worktree + new branch
  → Focus on developing authentication features

Terminal 2: claude --worktree feature-logging
  → Creates another worktree + branch
  → Focus on developing logging features

Result: Both features developed independently at the same time
```

## Setup

```bash
uv sync
```

## Getting Started

1. Open `CHALLENGE.md` to follow the step-by-step exercises
2. Add two features in parallel based on `src/app.py`
3. Merge the work from each worktree via PRs
