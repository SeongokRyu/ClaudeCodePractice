# Example Agent Definitions

This directory contains example subagent definitions.

## File List

| File | Role | Model | Purpose |
|------|------|-------|---------|
| `researcher.md` | Code exploration/analysis | haiku | Large codebase exploration, pattern analysis |
| `code-reviewer.md` | Code review | sonnet | Security/performance/maintainability review |
| `test-writer.md` | Test writing | sonnet | Test code generation and verification |

## Subagent vs. Direct Execution

### When to Use Subagents

- **Large-scale exploration**: Analysis tasks that require reading many files (context protection)
- **Specialized roles**: Focused analysis from a specific perspective (security, performance, etc.)
- **Writer/Reviewer separation**: When you want to separate the writer and reviewer perspectives
- **Repetitive tasks**: When applying the same pattern across multiple locations

### When Direct Execution is Better

- **Simple tasks**: Tasks that modify only 1-2 files
- **Interactive tasks**: Tasks that require back-and-forth feedback
- **Context-dependent**: Tasks that need previous conversation context
- **Quick fixes**: Simple bug fixes or minor changes

## Agent Definition Format

```markdown
---
tools:
  - Tool1
  - Tool2
model: haiku | sonnet | opus
permissionMode: plan    # optional
memory: project         # optional
---

# Agent Title

Write the role description and instructions in Markdown.
```

### Key Settings

- **tools**: List of tools the agent can use
- **model**: Model to use (haiku: fast and cheap, sonnet: balanced, opus: highest quality)
- **permissionMode**: If `plan`, shows the plan before execution
- **memory**: If `project`, uses project-level memory

## Usage Tips

1. **Model selection**: haiku for exploration/analysis, sonnet for code generation/review, opus for complex design
2. **Minimize tools**: Limit the agent's scope by granting only necessary tools
3. **Clear instructions**: Defining the output format specifically yields consistent results
4. **Team sharing**: Managing the `.claude/agents/` directory with git enables team sharing
