# Practice 03: Context Management

## Goal

Learn how to effectively manage Claude Code's context window -- master `/clear`, `/compact`, session management, and writing `HANDOFF.md`.

## Why This Matters

> "Context window is the most important resource to manage when working with AI coding assistants."
> -- Anthropic

When the context window fills up, Claude's performance degrades. Efficient context management is key to productivity.

## Prerequisites

- Practice 01 (Golden Workflow) completed

## Time

20-30 minutes

## What You'll Learn

1. **Observing context usage** -- Checking usage with the `/cost` command
2. **Using `/clear`** -- Resetting context between unrelated tasks
3. **Using `/compact`** -- Context compression using hint parameters
4. **Writing HANDOFF.md** -- Creating handoff documents between sessions
5. **`--resume` and `--continue` flags** -- Continuing from a previous session

## Getting Started

```bash
cd practices/03-context-management
uv sync
uv run pytest
```

Confirm that tests pass, then follow the step-by-step instructions in `CHALLENGE.md`.

## Key Concepts

### /clear

Reset the context when starting a new, unrelated task:

```
/clear
```

### /compact

Summarize the current conversation to compress the context. Providing a hint preserves important information:

```
/compact Please summarize focusing on the user-service CRUD implementation
```

### HANDOFF.md

A document for handing off work between sessions:

```markdown
# Handoff

## Current State
- How far the work has progressed

## What's Done
- List of completed tasks

## What's Left
- List of remaining tasks

## Key Decisions
- Important decisions made

## How to Verify
- How to verify the current state
```

### --resume & --continue

```bash
# Select and continue from a previous session
claude --resume

# Automatically continue from the last session
claude --continue
```
