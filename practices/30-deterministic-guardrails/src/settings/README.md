# Hook Configuration Guide

## Exit Code Protocol

Every hook script must exit with one of these codes:

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| `0` | Allow | Tool call proceeds normally |
| `2` | Block | Tool call is blocked; stdout is shown as the reason |
| Other | Error | Hook error; behavior depends on configuration |

## Hook Types

### PreToolUse

Runs **before** a tool executes. Receives the tool name and input on stdin as JSON.

Use cases:
- Block dangerous operations (file protection, command blocking)
- Validate inputs before execution
- Log intended actions

### PostToolUse

Runs **after** a tool executes. Receives the tool name, input, and output on stdin as JSON.

Use cases:
- Auto-format code after edits
- Run linting after edits
- Send notifications on completion
- Log results

## Hook Input Format

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "src/app.ts",
    "old_string": "...",
    "new_string": "..."
  }
}
```

For PostToolUse hooks, an additional `tool_output` field is included.

## Hooks in This Collection

### protect-files.sh (PreToolUse)

Blocks edits to sensitive files.

**Protected by default:**
- `.env`, `.env.*` — environment variables with secrets
- `migrations/` — database migration files (should be immutable)
- `package-lock.json` — auto-generated, should not be manually edited
- `*.pem`, `*.key` — cryptographic keys
- `secrets/` — secrets directory

**Customization:** Edit the `PROTECTED_PATTERNS` array in the script.

### block-dangerous.sh (PreToolUse)

Blocks dangerous bash commands.

**Blocked patterns:**
- `rm -rf /` — destructive deletion from root
- `git push --force` — force push destroys remote history
- `DROP TABLE` / `DROP DATABASE` — destructive SQL
- `chmod 777` — insecure permissions
- `curl | sh` — piping untrusted code to shell

**Customization:** Edit the `DANGEROUS_PATTERNS` array in the script.

### auto-format.sh (PostToolUse)

Runs prettier on edited files. Supports: .ts, .js, .tsx, .jsx, .json, .css, .md, .yaml, .html.

Always exits 0 (non-blocking).

### auto-lint.sh (PostToolUse)

Runs eslint with auto-fix on edited TypeScript files (.ts, .tsx only).

Always exits 0 (advisory only).

### notify-completion.sh (PostToolUse)

Sends a desktop notification when it detects task completion patterns in tool output. Supports macOS (osascript) and Linux (notify-send).

## Environment Configurations

### development.json

- File protection: active
- Dangerous command blocking: **disabled** (more freedom for local dev)
- Auto-format: active
- Auto-lint: **disabled** (to reduce noise)
- Notifications: **disabled**

### production.json

- File protection: active
- Dangerous command blocking: active
- Auto-format: active
- Auto-lint: active
- Notifications: active
- Additional permission deny list
