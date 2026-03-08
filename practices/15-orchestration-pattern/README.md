# Practice 15: Command→Agent→Skill Pattern

## Goal

Design and implement the 3-layer orchestration pattern for Claude Code. Learn the structure where Commands provide entry points, Agents handle execution, and Skills provide domain knowledge.

## Prerequisites

- Practice 08 (Skills) completed
- Practice 13 (Subagents) completed

## Time

45-60 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

- Roles and responsibilities of Commands, Agents, and Skills
- Design principles of the 3-layer orchestration pattern
- How to connect Skills to Agents and invoke Agents from Commands
- Building reusable automation pipelines

## Key Concepts

### 3-Layer Architecture

```
┌─────────────────────────────────────────────┐
│  Layer 1: Commands (Entry Point)             │
│  .claude/commands/analyze.md                 │
│  → User runs with /analyze src/              │
│  → Calls Agent and organizes results         │
├─────────────────────────────────────────────┤
│  Layer 2: Agents (Executor)                  │
│  .claude/agents/analyzer-agent.md            │
│  → Performs the actual analysis work         │
│  → Loads analysis criteria from Skill        │
│  → Reads files, analyzes, generates report   │
├─────────────────────────────────────────────┤
│  Layer 3: Skills (Knowledge Provider)        │
│  .claude/skills/code-analyzer/SKILL.md       │
│  → Defines code quality analysis criteria    │
│  → Guides which patterns to look for         │
│  → Provides scoring standards               │
└─────────────────────────────────────────────┘
```

### Responsibilities of Each Layer

| Layer | Role | Analogy |
|------|------|------|
| Command | Entry point, argument parsing, result formatting | Receptionist |
| Agent | Task execution, logic processing, tool usage | Engineer |
| Skill | Domain knowledge, rules, criteria | Manual/Textbook |

## Getting Started

1. Open `CHALLENGE.md` and follow the step-by-step exercises
2. A completed example is available in `src/example-orchestration/`
3. Refer to the example to create your own orchestration pipeline
