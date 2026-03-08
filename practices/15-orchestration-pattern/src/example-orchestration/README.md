# Example Orchestration: Code Analyzer

This directory is a completed example of the Command→Agent→Skill 3-layer orchestration pattern.

## Architecture

```
User Input
    │
    ▼
┌──────────────────────────────────────────────┐
│  /analyze src/                                │
│  .claude/commands/analyze.md                  │
│                                               │
│  Role:                                        │
│  - Receives target path via $ARGUMENTS        │
│  - Delegates work to analyzer-agent           │
│  - Formats results and outputs to user        │
└──────────────┬───────────────────────────────┘
               │ Delegation
               ▼
┌──────────────────────────────────────────────┐
│  analyzer-agent                               │
│  .claude/agents/analyzer-agent.md             │
│                                               │
│  Role:                                        │
│  - Loads code-analyzer Skill                  │
│  - Discovers and collects target files        │
│  - Analyzes each file based on Skill criteria │
│  - Generates analysis report                  │
└──────────────┬───────────────────────────────┘
               │ Reference
               ▼
┌──────────────────────────────────────────────┐
│  code-analyzer Skill                          │
│  .claude/skills/code-analyzer/SKILL.md        │
│                                               │
│  Role:                                        │
│  - Complexity analysis criteria (30 pts)      │
│  - Maintainability analysis criteria (30 pts) │
│  - Best practices analysis criteria (40 pts)  │
│  - Grade assignment criteria (A~F)            │
│  - Output format template                     │
└──────────────────────────────────────────────┘
```

## File Structure

```
.claude/
├── commands/
│   └── analyze.md          ← Layer 1: User entry point
├── agents/
│   └── analyzer-agent.md   ← Layer 2: Execution logic
└── skills/
    └── code-analyzer/
        └── SKILL.md        ← Layer 3: Domain knowledge
```

## How It Works

### 1. Command Layer (Entry Point)

`analyze.md` is executed when the user enters `/analyze src/`.
- Receives the target path through `$ARGUMENTS`
- Delegates the actual analysis work to the Agent
- Displays the Agent's results in a user-friendly format

### 2. Agent Layer (Executor)

`analyzer-agent.md` performs the actual analysis work.
- Preloads the Skill to reference analysis criteria
- Proceeds in 3 steps: file discovery → individual analysis → report generation
- Generates a structured report

### 3. Skill Layer (Knowledge Provider)

`SKILL.md` defines the domain knowledge needed for code quality analysis.
- 3 categories: complexity, maintainability, and best practices
- Specific scoring criteria for each category
- Grade standards and output format template

## Extending This Pattern

You can use this pattern to create new pipelines:

| Command | Agent | Skill | Purpose |
|---------|-------|-------|------|
| /analyze | analyzer-agent | code-analyzer | Code quality analysis |
| /review | review-agent | code-reviewer | Code review |
| /docs | docs-agent | docs-generator | Automated documentation generation |
| /security | security-agent | security-checker | Security audit |

Key point: Skills can be shared by multiple Agents, and Agents can be reused across multiple Commands.
