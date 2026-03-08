# Task Automation with Claude Code

---

## Core Concept

Claude Code automation is based on **`claude -p` (headless mode)**.
All automation patterns (CI/CD, scripts, cron, git hooks) are built on top of this mode.

---

## 1. Headless Mode (`claude -p`)

Non-interactive mode. Receives a prompt, executes it, and outputs results to stdout.

```bash
# Basic usage
claude -p "Explain the architecture of this project"

# Pipe input (PR diff review)
gh pr diff 42 | claude -p "Review for security vulnerabilities"

# JSON output (programmatic parsing)
claude -p "List of TODO comments" --output-format json | jq '.result'

# Tool restrictions (CI safety)
claude -p "Review src/" --allowedTools Read,Grep --max-turns 5

# Add system prompt
git diff --cached | claude -p "Write a commit message" \
  --append-system-prompt "Be concise like a senior engineer"
```

**Output formats**: `text` (default), `json` (structured), `stream-json` (streaming)

**CI safety rules**: Exclude Bash with `--allowedTools`, store API keys in a secret manager, prevent infinite loops with `--max-turns`

---

## 2. GitHub Actions (`claude-code-action`)

Official GitHub Action. Core of PR/issue automation.

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
  issues:
    types: [opened, assigned, labeled]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_args: "--max-turns 10"
```

| Trigger | Use Case |
|---------|----------|
| `@claude` mention | Interactive code review, Q&A |
| `issues: [opened]` | Automatic issue triage |
| `pull_request_review` | Automatic review per PR |
| `push: tags` | Automatic release note generation |
| `schedule: cron` | Regular maintenance (dependency checks, etc.) |

**Installation**: Run `/install-github-app` in the Claude Code terminal

---

## 3. Hooks - Deterministic Workflow Control

Unlike Skills, Hooks **always execute** and cannot be skipped by the LLM.

### Lifecycle Events

| Event | Timing | Use Case |
|-------|--------|----------|
| PreToolUse | Before tool execution | Block risky operations, modify inputs |
| PostToolUse | After tool execution | Code formatting, logging |
| SessionStart | Session start | Load environment, reminders |
| SessionEnd | Session end | Cleanup, generate summaries |
| Notification | Notification fired | Custom notification routing |

### Exit Code
- `0` = Allow (continue)
- `2` = Block (stop tool execution, stderr message sent to Claude)
- Other = Non-blocking error (show warning and continue)

### Practical Examples

**Auto-format after edit (PostToolUse):**
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit|Write",
      "type": "command",
      "command": "prettier --write \"$CLAUDE_FILE_PATH\" 2>/dev/null || true"
    }]
  }
}
```

**Block sensitive file edits (PreToolUse):**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "type": "command",
      "command": "python3 -c \"import json,sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); sys.exit(2) if any(s in path for s in ['.env','package-lock.json']) else sys.exit(0)\""
    }]
  }
}
```

**v2.0.10+**: PreToolUse hooks can modify tool inputs before execution (no need to block + retry)

---

## 4. Batch Processing and Fan-Out Pattern

### `/batch` Command (Built-in)
Safe parallel execution with Git Worktree isolation. Creates a PR for each upon completion.
```
/batch "Migrate all React class components to functional components"
```

### Manual Fan-Out (bash scripting)
```bash
#!/bin/bash
# Parallel review of multiple directories
for dir in src/auth src/api src/frontend; do
  claude -p "Review security issues in $dir. Output as JSON." \
    --output-format json > "review_${dir//\//_}.json" &
done
wait
jq -s '.' review_*.json > full_review.json
```

### Auto Commit Message Generation
```bash
ai_commit() {
  msg=$(git diff --cached | claude -p \
    "Write a one-line commit message for this diff. Output only the message.")
  git commit -m "$msg"
}
```

---

## 5. Scheduling / Cron Automation

| Method | Description |
|--------|-------------|
| `/loop` | Repeated execution within a session (`/loop 5m /check-status`) |
| Desktop scheduled tasks | Persists across restarts, GUI configuration |
| GitHub Actions `schedule` | Infrastructure-level automation |
| cron + `claude -p` | Headless invocation from system cron |

```yaml
# Daily code health check at 2 AM
on:
  schedule:
    - cron: '0 2 * * *'
```

---

## 6. Git Hooks and Claude Code Integration

### Security Check with Claude in pre-commit
```bash
#!/bin/bash
# .git/hooks/pre-commit
DIFF=$(git diff --cached)
RESULT=$(echo "$DIFF" | claude -p \
  "Output BLOCK if there are secrets or security issues, otherwise output PASS" \
  --max-turns 1)
if echo "$RESULT" | grep -q "^BLOCK"; then
  echo "Pre-commit failed: $RESULT"
  exit 1
fi
```

---

## 7. Real-World Examples

| Organization | Use Case | Result |
|-------------|----------|--------|
| Anthropic Marketing | CSV ad data analysis, variant generation | Hours to minutes, 0.5 sec per batch |
| Anthropic Security | Stack trace analysis, control flow tracing | 3x faster incident resolution |
| Anthropic Legal | Built a "phone tree" system | Prototype without developers |
| General Pilot | Automated code review | 30% faster PR processing, 72% test coverage |
