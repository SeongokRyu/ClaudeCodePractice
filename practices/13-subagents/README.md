# Practice 13: Using Subagents

## Objective

Learn how to use subagents to perform context protection, Writer/Reviewer patterns, and parallel tasks.

## Difficulty

:star::star::star:

## Prerequisites

- Practice 05 (CLAUDE.md) completed
- Practice 08 (Skills) completed
- Basic understanding of the subagent concept

## Estimated Time

45-60 minutes

## Key Concepts

### What is a Subagent?

A subagent is a separate agent spawned from the main Claude session. It has its own independent context window, performs a specific task, and returns only the results.

### When to Use Subagents

1. **Context Protection**: Prevent the main context from filling up with large exploration tasks
2. **Specialization**: Agents focused on specific roles (reviewer, test writer, etc.)
3. **Writer/Reviewer Pattern**: One agent writes, another agent reviews
4. **Parallel Tasks**: Perform independent tasks simultaneously

### Agent Definition Files

Define agents as Markdown files in the `.claude/agents/` directory:

```markdown
---
tools:
  - Read
  - Grep
  - Glob
model: haiku
---

# Agent Name

Write the agent's role and instructions here.
```

## Getting Started

```bash
cd practices/13-subagents
uv sync
```

There are example agent definitions in the `src/example-agents/` directory. Follow `CHALLENGE.md` to create and use subagents.

## Learning Points

- Subagents are the most effective way to protect the context window
- The Writer/Reviewer pattern significantly improves code quality
- Not every task needs a subagent — proper judgment is important
- Agent definition files are reusable assets that can be shared with your team
