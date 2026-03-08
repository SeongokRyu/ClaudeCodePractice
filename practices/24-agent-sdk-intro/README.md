# Practice 24: Agent SDK 입문

## Goal
Build your first agent with the Claude Agent SDK in both Python and TypeScript. Learn the fundamentals of programmatic agent creation, tool restrictions, system prompts, and streaming responses.

## Prerequisites
- Practice 05 (CLAUDE.md)
- Practice 08 (Skills)
- Practice 13 (Subagents)

## Time
90-120 minutes

## Difficulty
★★★

## What You'll Learn
- Installing and configuring the Claude Agent SDK (Python & TypeScript)
- Creating minimal agents with `query()` calls
- Restricting tools with `allowedTools` and `disallowedTools`
- Using system prompt presets like `claude_code`
- Handling streaming responses for real-time output

## Project Structure
```
practices/24-agent-sdk-intro/
├── README.md
├── CHALLENGE.md
├── pyproject.toml
├── src/
│   ├── python/
│   │   ├── basic_agent.py
│   │   ├── tool_restricted_agent.py
│   │   └── streaming_agent.py
│   └── typescript/
│       ├── package.json
│       ├── basic-agent.ts
│       └── tool-restricted-agent.ts
```

## Key Concepts

### Agent SDK vs Direct API
The Agent SDK wraps the Anthropic API with agent-specific capabilities:
- **Tool integration**: Agents can use tools (file I/O, shell, search) automatically
- **Session management**: Conversations persist across multiple turns
- **Streaming**: Real-time output as the agent works
- **Presets**: Pre-configured system prompts optimized for different tasks

### Tool Restrictions
Control what your agent can do:
- `allowedTools`: Whitelist specific tools only
- `disallowedTools`: Blacklist dangerous tools
- Combine both for fine-grained control

### System Prompt Presets
Pre-built configurations for common use cases:
- `claude_code`: Full coding assistant capabilities
- Custom prompts: Define your own agent persona and rules
