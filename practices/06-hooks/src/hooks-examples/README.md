# Hooks Examples

## Overview

Claude Code Hooks are shell scripts that run at specific points during Claude's workflow. Unlike CLAUDE.md rules (which are probabilistic — Claude usually follows them but might not), Hooks are **deterministic** — they always execute and can enforce rules with code.

## Hook Types

### PreToolUse

Runs **before** a tool is executed. Can **block** the action.

- **Exit 0**: Allow the tool call to proceed
- **Exit 2**: Block the tool call; stderr message is shown to Claude
- **Use cases**: File protection, command blocklist, input validation

### PostToolUse

Runs **after** a tool is executed. Cannot block (the action already happened).

- **Exit code**: Ignored (cannot block after the fact)
- **Use cases**: Auto-formatting, logging, metrics

### Notification

Runs when Claude produces a notification (e.g., when waiting for user input).

- **Exit code**: Ignored
- **Use cases**: Desktop alerts, Slack messages, sound effects

## Hook Input

All hooks receive a JSON object on stdin:

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

PostToolUse hooks also receive `tool_output` with the result.

## Configuration

Hooks are configured in `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hook": ".claude/hooks/protect-files.sh",
        "description": "Block edits to .env files"
      }
    ]
  }
}
```

### Fields

- **matcher**: Regex pattern for tool names to match. Empty string matches all tools.
  - `"Edit"` — matches only Edit tool
  - `"Edit|Write"` — matches Edit or Write
  - `"Bash"` — matches Bash tool
  - `""` — matches all tools (useful for Notification hooks)
- **hook**: Path to the shell script (relative to project root)
- **description**: Human-readable description (shown in Claude's UI)

## Files in This Directory

### protect-files.sh
PreToolUse hook that blocks edits to:
- `.env` files (any variant: `.env`, `.env.local`, `.env.production`)
- Files in `generated/` directories

Uses `jq` to parse the JSON input and extract the file path.

### auto-format.sh
PostToolUse hook that auto-formats files after Edit/Write:
- TypeScript/JavaScript: Prettier
- Python: Black or autopep8
- Go: gofmt
- Rust: rustfmt

Only runs if the formatter is installed.

### notify.sh
Notification hook that sends desktop alerts:
- macOS: `osascript` (native notification)
- Linux: `notify-send` (requires libnotify) or `zenity`
- Windows (Git Bash): PowerShell toast notification

### settings-example.json
Complete `.claude/settings.json` with all three hooks configured. Copy this to your project's `.claude/settings.json` to use.

## Tips

1. **Always use `jq`** to parse JSON input — do not try to parse JSON with sed/grep
2. **Make hooks fast** — they run on every tool call; slow hooks degrade the experience
3. **Use stderr for messages** — in PreToolUse hooks, stderr output is shown to Claude as the reason for blocking
4. **Test hooks manually** — pipe test JSON to your script: `echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | bash protect-files.sh`
5. **Hooks are per-project** — they live in `.claude/settings.json` in your project root
