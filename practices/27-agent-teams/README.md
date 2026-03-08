# Practice 27: Agent Teams 실습

## Goal
Create and manage agent teams using Claude Code's experimental Agent Teams feature. Learn to spawn teammates, use shared task lists, and coordinate specialist teams for complex tasks.

## Prerequisites
- Practice 25 (커스텀 서브에이전트 설계)

## Time
90-120 minutes

## Difficulty
★★★

## Note
Agent Teams is an **experimental feature** and may change in future versions. Enable it with the environment variable `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

## What You'll Learn
- Enabling and configuring Agent Teams
- Spawning teammates with natural language prompts
- Using shared task lists for coordination
- Navigating between teammates
- Creating specialist teams (UX, Backend, Testing)
- The "competing hypotheses" pattern for debugging

## Project Structure
```
practices/27-agent-teams/
├── README.md
├── CHALLENGE.md
├── src/
│   ├── settings-example.json
│   ├── team-prompts/
│   │   ├── specialist-team.md
│   │   ├── competing-hypotheses.md
│   │   └── cross-layer-feature.md
│   └── project/
│       ├── frontend/
│       │   └── src/
│       │       └── App.tsx
│       ├── backend/
│       │   └── src/
│       │       └── server.ts
│       └── tests/
│           └── integration.test.ts
```

## Key Concepts

### Agent Teams Architecture
Agent Teams creates multiple Claude Code instances ("teammates") that:
- Share a **task list** visible to all teammates
- Work on different aspects of a problem **simultaneously**
- Can be navigated with keyboard shortcuts

### When to Use Agent Teams
- **Large features** spanning multiple layers (frontend + backend + tests)
- **Debugging** complex issues with multiple potential causes
- **Exploration** when you need to investigate several hypotheses
- **Parallel workstreams** where agents don't need to coordinate closely

### When NOT to Use Agent Teams
- Simple, single-file changes
- Tasks requiring sequential steps (use subagents instead)
- When you need tight coordination between agents (use writer/reviewer pattern)

### Keyboard Shortcuts
| Shortcut | Action |
|----------|--------|
| `Ctrl+T` | Toggle shared task list |
| `Tab` | Cycle between teammates |
| `Enter` | View selected teammate |
| Natural language | Spawn new teammate |
