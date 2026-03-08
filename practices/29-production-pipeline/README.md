# Practice 29: Production Multi-Agent Pipeline

## Goal
Build a production-ready Command -> Agent -> Skill pipeline with agent memory. This practice combines everything from Phase 5 into a complete, reusable multi-agent system.

## Prerequisites
- Practice 25 (Custom Subagent Design)
- Practice 26 (Writer/Reviewer Pattern)
- Practice 28 (Scatter-Gather Research System)

## Time
90-120 minutes

## Difficulty
★★★

## What You'll Learn
- The 3-layer architecture: Commands -> Agents -> Skills
- Creating reusable Skills (coding conventions, testing patterns, security review)
- Creating specialized Agents with memory
- Creating Commands that orchestrate the full pipeline
- Agent memory for cross-session learning
- End-to-end production pipeline execution

## Project Structure
```
practices/29-production-pipeline/
├── README.md
├── CHALLENGE.md
├── src/
│   ├── pipeline/
│   │   ├── CLAUDE.md
│   │   ├── .claude/
│   │   │   ├── skills/
│   │   │   │   ├── coding-conventions/SKILL.md
│   │   │   │   ├── testing-patterns/SKILL.md
│   │   │   │   └── security-review/SKILL.md
│   │   │   ├── agents/
│   │   │   │   ├── researcher.md
│   │   │   │   ├── implementer.md
│   │   │   │   ├── reviewer.md (with memory)
│   │   │   │   └── tester.md
│   │   │   ├── commands/
│   │   │   │   └── build-feature.md
│   │   │   └── agent-memory/
│   │   │       └── reviewer/
│   │   │           └── MEMORY.md
│   │   └── src/
│   │       ├── app.py
│   │       └── test_app.py
│   └── python/
│       └── production_pipeline.py
```

## Key Concepts

### The 3-Layer Architecture
```
┌─────────────────────────────────────────┐
│  Layer 1: Commands                       │
│  /build-feature — Orchestrates the       │
│  entire pipeline                         │
├─────────────────────────────────────────┤
│  Layer 2: Agents                         │
│  researcher → implementer → reviewer     │
│  → tester                               │
│  Each has: role, tools, model, memory   │
├─────────────────────────────────────────┤
│  Layer 3: Skills                         │
│  coding-conventions, testing-patterns,   │
│  security-review                        │
│  Reusable knowledge bases               │
└─────────────────────────────────────────┘
```

### Agent Memory
- Reviewer agent uses `memory: project` to accumulate patterns
- Memory persists across sessions in `.claude/agent-memory/reviewer/MEMORY.md`
- Each review adds new patterns to the memory file
- Over time, the reviewer becomes more effective

## Setup

```bash
pip install pytest pytest-cov
cd src/pipeline && pytest src/
```

### Command Orchestration
The `/build-feature` command ties everything together:
1. Spawns researcher agent to analyze the codebase
2. Spawns implementer agent to write code (with skills preloaded)
3. Spawns reviewer agent to review (with memory)
4. Spawns tester agent to verify
5. Loops if reviewer requests changes
