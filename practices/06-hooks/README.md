# Practice 06: Hooks 설정

## Goal

Learn to configure Claude Code Hooks — file protection, auto-formatting, notifications. Understand exit codes, hook types, and the difference between deterministic enforcement (Hooks) and probabilistic guidance (CLAUDE.md).

## Prerequisites

- [Practice 05: CLAUDE.md 작성법](../05-claude-md/)

## Time

30-45 minutes

## Why This Matters

> "CLAUDE.md rules are probabilistic, Hooks are deterministic."

When you write "Do not edit .env files" in CLAUDE.md, Claude will usually follow it — but not always. It is a suggestion, not a guarantee. Hooks solve this by intercepting tool calls and enforcing rules with code.

Hooks run at specific points in Claude's workflow:
- **PreToolUse** — runs before a tool is executed (can block it)
- **PostToolUse** — runs after a tool is executed (can modify results)
- **Notification** — runs when Claude produces a notification

## What You Will Learn

1. How to configure hooks in `.claude/settings.json`
2. PreToolUse hooks for file protection (exit code 2 = block)
3. PostToolUse hooks for auto-formatting after edits
4. Notification hooks for desktop alerts
5. The exit code convention: 0 = allow, 2 = block

## Directory Structure

```
src/
├── hooks-examples/
│   ├── protect-files.sh       # Block edits to protected files
│   ├── auto-format.sh         # Auto-format after Edit/Write
│   ├── notify.sh              # Desktop notifications
│   ├── settings-example.json  # Example .claude/settings.json
│   └── README.md              # Detailed hook explanations
└── practice-project/
    ├── package.json
    ├── tsconfig.json
    └── src/
        ├── app.ts             # Basic Express-like server
        └── .env.example       # Example env file to protect
```

## Key Concepts

### Hook Types

| Type | When It Runs | Can Block? | Use Case |
|------|-------------|-----------|----------|
| PreToolUse | Before tool execution | Yes (exit 2) | File protection, input validation |
| PostToolUse | After tool execution | No | Auto-format, logging |
| Notification | On notification | No | Desktop alerts, Slack messages |

### Exit Codes

- **Exit 0** — Allow the action to proceed
- **Exit 2** — Block the action (PreToolUse only); message on stderr shown to Claude

### Hook Input

Hooks receive a JSON object on stdin with:
- `tool_name` — the tool being used (e.g., "Edit", "Write", "Bash")
- `tool_input` — the parameters passed to the tool
- `tool_output` — the result (PostToolUse only)
