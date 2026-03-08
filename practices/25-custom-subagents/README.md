# Practice 25: 커스텀 서브에이전트 설계

## Goal
Design role-based subagents with proper tool, model, and permission separation. Learn to create a multi-agent system where each agent has a clearly defined role, restricted capabilities, and appropriate model selection.

## Prerequisites
- Practice 24 (Agent SDK 입문)

## Time
90-120 minutes

## Difficulty
★★★

## What You'll Learn
- Designing agent roles with clear responsibility boundaries
- Tool restrictions per agent role (read-only vs. full access)
- Model selection per agent (haiku for speed, sonnet for balance, opus for quality)
- Agent modes (plan mode, implement mode)
- Wiring multiple agents into a coordinated workflow

## Project Structure
```
practices/25-custom-subagents/
├── README.md
├── CHALLENGE.md
├── src/
│   ├── agents/
│   │   ├── researcher.md
│   │   ├── implementer.md
│   │   ├── reviewer.md
│   │   ├── tester.md
│   │   └── security-auditor.md
│   └── project/
│       ├── app.py
│       ├── utils.py
│       └── test_app.py
```

## Setup

```bash
uv sync
uv run pytest
```

## Key Concepts

### Role-Based Agent Design
Each agent should have:
1. **Clear responsibility**: What is this agent's job?
2. **Tool restrictions**: What tools can it use?
3. **Model selection**: Which model fits its task?
4. **Output format**: What should it produce?

### The 3-Agent System
| Agent | Tools | Model | Mode | Purpose |
|-------|-------|-------|------|---------|
| Researcher | Read, Glob, Grep | haiku | Plan | Understand codebase |
| Implementer | All tools | sonnet | Implement | Write code |
| Reviewer | Read, Glob, Grep | inherit | Review | Check quality |

### Agent Definition Files
Agent `.md` files define the agent's persona, capabilities, and constraints. They serve as the "job description" for each subagent.
