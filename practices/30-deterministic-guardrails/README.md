# Practice 30: 결정론적 가드레일

## Goal

Build deterministic guardrails with Hooks -- file protection, dangerous command blocking, and auto-formatting enforcement. Hooks provide a reliable, code-based safety layer that runs before or after every tool call, ensuring that Claude operates within defined boundaries regardless of how it interprets a prompt.

## Prerequisites

- **Practice 06**: Hooks (basic hook concepts and configuration)
- **Practice 24**: Agent SDK Intro (understanding tool calls and agent flow)

## Time

90-120 minutes

## Difficulty

★★★

## What You Will Learn

1. How to write PreToolUse hooks that block dangerous operations
2. How to write PostToolUse hooks that enforce code quality automatically
3. How to combine multiple hooks into a production-ready configuration
4. The exit code protocol: exit 0 (allow), exit 2 (block), other (error)
5. How to design layered guardrails for different environments

## Key Concepts

- **Deterministic guardrails** are rules enforced by code, not by prompting. They cannot be bypassed by creative prompt engineering.
- **PreToolUse hooks** run before a tool executes. They can inspect the tool name and input, then block (exit 2) or allow (exit 0).
- **PostToolUse hooks** run after a tool executes. They can inspect the output and trigger follow-up actions like formatting or linting.
- **Exit code protocol**: `exit 0` = allow, `exit 2` = block with message, any other = hook error.

## Structure

```
src/
  hooks/
    protect-files.sh       # Blocks edits to protected files
    block-dangerous.sh     # Blocks dangerous bash commands
    auto-format.sh         # Runs prettier after file edits
    auto-lint.sh           # Runs eslint after .ts file edits
    notify-completion.sh   # Desktop notification on completion
  settings/
    development.json       # Dev environment hooks config
    production.json        # Production environment hooks config
    README.md              # Hook guide with exit code explanations
```

## Tips

- Start with a single hook and test it thoroughly before combining
- Use `jq` to parse the JSON input that hooks receive on stdin
- Always test both the "allow" and "block" paths
- Log hook actions for debugging (stderr goes to Claude's log)
