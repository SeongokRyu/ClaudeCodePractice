# Git Hooks Installation Guide

## Quick Setup

### Option 1: Manual Installation

Copy the hooks to your repository's `.git/hooks/` directory:

```bash
# Navigate to your repository
cd /path/to/your/repo

# Copy hooks
cp /path/to/this/practice/src/hooks/pre-commit .git/hooks/pre-commit
cp /path/to/this/practice/src/hooks/commit-msg .git/hooks/commit-msg
cp /path/to/this/practice/src/hooks/pre-push .git/hooks/pre-push

# Make them executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/pre-push
```

### Option 2: Symlink (for development)

```bash
# Symlink so changes to the practice files are reflected immediately
ln -sf /path/to/this/practice/src/hooks/pre-commit .git/hooks/pre-commit
ln -sf /path/to/this/practice/src/hooks/commit-msg .git/hooks/commit-msg
ln -sf /path/to/this/practice/src/hooks/pre-push .git/hooks/pre-push
```

### Option 3: Git core.hooksPath

```bash
# Point Git to a shared hooks directory
git config core.hooksPath /path/to/this/practice/src/hooks
```

## Claude Code Hooks Setup

Claude Code hooks are configured in `.claude/settings.json`, not in `.git/hooks/`.

```bash
# Copy the example config
mkdir -p .claude
cp src/claude-hooks/settings-example.json .claude/settings.json
```

Then edit `.claude/settings.json` to keep only the hooks you want.

## Hook Descriptions

### pre-commit

**Purpose**: Scans staged files for hardcoded secrets before committing.

**How it works**:
1. Quick regex scan for common secret patterns
2. If a pattern matches, uses Claude for intelligent analysis
3. Blocks the commit if real secrets are found

**Requirements**: `claude` CLI must be in PATH.

**Skip**: `git commit --no-verify` (not recommended)

### commit-msg

**Purpose**: Validates commit messages follow Conventional Commits format.

**Format**: `type(scope): description`

**Valid types**: feat, fix, docs, style, refactor, test, chore, perf, ci, build

**Requirements**: None (Claude is optional for suggestions).

### pre-push

**Purpose**: Runs tests and security scan before pushing.

**Checks**:
1. Runs test suite (npm test or pytest)
2. TypeScript type checking (if applicable)
3. Claude security scan on new commits

**Requirements**: Test runner, optionally `claude` CLI.

## Troubleshooting

### Hook not running
- Check permissions: `ls -la .git/hooks/`
- Ensure the hook is executable: `chmod +x .git/hooks/<hook-name>`
- Check the shebang line: must be `#!/usr/bin/env bash`

### Hook too slow
- The pre-commit hook only scans files that match secret patterns
- Reduce the number of files scanned by adjusting patterns
- Set a timeout: add `timeout 30` before the `claude` command

### Claude not found
- Ensure Claude CLI is installed: `which claude`
- The hooks gracefully degrade when Claude is not available
- Regex-based checks still work without Claude

### Bypassing hooks (emergency only)
```bash
git commit --no-verify  # Skip pre-commit and commit-msg
git push --no-verify    # Skip pre-push
```
