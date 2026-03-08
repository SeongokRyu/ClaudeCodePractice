# Getting Started

Complete everything from installing Claude Code to your first conversation in 15 minutes.

---

## 1. Check Your Environment (3 min)

```bash
uv --version      # Verify uv is installed
python --version   # Python 3.10 or higher recommended
git --version      # Any version is OK
```

If uv is not installed:
- macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- Or Homebrew: `brew install uv`

Editor: **VS Code** recommended (supports Claude Code extension)

---

## 2. Install Claude Code (5 min)

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows (PowerShell)
irm https://claude.ai/install.ps1 | iex

# Verify installation
claude --version
```

---

## 3. Authentication (3 min)

```bash
claude
```

When you run it for the first time, a login prompt will appear. You need one of the following:
- **Claude Pro/Max subscription** (easiest)
- **Anthropic API key** (pay-as-you-go)

---

## 4. First Conversation (5 min)

```bash
mkdir practice-test && cd practice-test
claude
```

Once Claude Code starts, try typing the following:

```
Create a hello.ts file in this directory.
Make it a simple program that prints "Hello from Claude Code!"
```

After Claude creates the file, try this:

```
Run the file you just created
```

After confirming it works, type `/clear` to reset the conversation.

---

## 5. Start This Practice Repo (2 min)

```bash
cd ..
git clone <repo-url> ClaudeCodePractice
cd ClaudeCodePractice
```

Now start with [Practice 01: Golden Workflow](../practices/01-golden-workflow/).

---

## Good to Know

| Shortcut | Action |
|----------|--------|
| Shift+Tab | Cycle modes (Normal → Auto-accept → Plan) |
| Esc | Stop current task |
| Esc+Esc | Revert to previous state |

| Command | Action |
|---------|--------|
| `/clear` | Reset conversation |
| `/compact` | Compress conversation (free up context) |
| `/cost` | Check current session cost |
| `/help` | Help |
