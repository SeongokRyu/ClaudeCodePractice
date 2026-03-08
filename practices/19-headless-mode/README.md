# Practice 19: Headless Mode 기초

## Goal

Learn how to use Claude Code in headless mode (`claude -p`) for non-interactive automation. Master piping input, controlling output format, restricting available tools, and building shell scripts that leverage Claude programmatically.

## Prerequisites

- [Practice 01: Golden Workflow](../01-golden-workflow/) — Basic Claude Code usage
- [Practice 05: CLAUDE.md](../05-claude-md/) — Project configuration

## Time

60-90 minutes

## Difficulty

★★☆ (Intermediate)

## What You'll Learn

1. **`claude -p` basics** — Running Claude non-interactively with a prompt
2. **Pipe input** — Feeding file contents and command output to Claude via stdin
3. **JSON output** — Getting structured responses with `--output-format json`
4. **Tool restrictions** — Limiting which tools Claude can use with `--allowedTools`
5. **Shell integration** — Building practical shell scripts powered by Claude

## Key Concepts

### Headless Mode

Headless mode runs Claude without the interactive REPL. You pass a prompt with `-p` and Claude responds to stdout, then exits. This is the foundation for all task automation.

### Output Formats

- **Text (default)** — Human-readable output
- **JSON** — Structured output with `result`, `cost`, and metadata fields
- **Stream JSON** — Real-time streaming of events

### Tool Restrictions

Use `--allowedTools` to limit what Claude can do in headless mode. This is critical for safety when running automated scripts:
- `Read,Grep` — Read-only analysis
- `Read,Grep,Edit` — Analysis with editing capability
- `Read,Grep,Bash` — Full automation (use with caution)

## Quick Reference

```bash
# Basic headless prompt
claude -p "explain what this project does"

# Pipe file content
cat src/app.py | claude -p "review this code"

# JSON output
claude -p "list TODO comments" --output-format json

# Restrict tools and limit turns
claude -p "review src/" --allowedTools Read,Grep --max-turns 5
```

## Directory Structure

```
19-headless-mode/
├── README.md
├── CHALLENGE.md
├── pyproject.toml
└── src/
    ├── app.py              # Sample app for scripts to analyze
    ├── test_app.py         # Tests for the sample app (pytest)
    └── scripts/
        ├── auto-commit.sh      # Automatic commit message generation
        ├── review-changes.sh   # Review changed files via git diff
        └── todo-scanner.sh     # Scan for TODO/FIXME comments
```

## Setup

```bash
uv sync
uv run pytest
```
