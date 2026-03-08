# Permission Profile Guide

## Overview

Permission profiles control which tools and commands Claude Code can use. They are defined in `settings.json` and can be loaded per-project or per-session.

## Trust Levels

| Profile | Trust Level | Can Read | Can Write | Can Execute | Can Network |
|---------|------------|----------|-----------|-------------|-------------|
| `zero-trust.json` | None | Project files only | No | No | No |
| `readonly-review.json` | Minimal | All project files | No | git read commands | No |
| `ci-cd.json` | Low | All project files | No | test/build/lint | No |
| `trusted-dev.json` | High | All files | Yes | Most commands | Localhost |

## Profile Details

### zero-trust.json

**Use case:** Reviewing untrusted or potentially malicious code.

**Allowed:**
- Read files in mounted directory
- Search with Grep/Glob
- Basic file inspection (ls, wc, file, head, tail)

**Blocked:** Everything else. No git, no npm, no node, no network, no writes.

**Recommended setup:** Use inside Docker container with read-only mount and no network.

### readonly-review.json

**Use case:** Code review, codebase Q&A, audit.

**Allowed:**
- All read operations
- Git read commands (log, diff, show, blame, status, branch)
- Basic file inspection commands

**Blocked:** All write operations, all execution, all network.

**When to use:** When you want Claude to analyze code without any risk of modification.

### ci-cd.json

**Use case:** Automated pipelines -- running tests, checking builds, reporting results.

**Allowed:**
- Read operations
- npm test, npm run build, npm run lint
- TypeScript type checking
- Jest test running
- Git read commands

**Blocked:** Writes, installs, publishes, network tools, arbitrary code execution.

**When to use:** In GitHub Actions or other CI systems where Claude should only verify, not modify.

### trusted-dev.json

**Use case:** Daily development by trusted team members.

**Allowed:**
- All standard development tools (read, write, edit)
- Git operations (commit, push -- but not force push)
- npm commands (install, run, test)
- Node.js execution
- File management (cp, mv, mkdir)

**Blocked:** Destructive operations (rm -rf /, force push, chmod 777), system commands (sudo, shutdown), unsafe network patterns (curl|sh).

**When to use:** Regular development work in trusted repositories.

## How to Use

### Per-project configuration

Place the profile as `.claude/settings.json` in your project root:
```bash
cp permissions/trusted-dev.json /path/to/project/.claude/settings.json
```

### Switching profiles

To switch profiles for a session:
```bash
cp permissions/readonly-review.json .claude/settings.json
```

### Combining with hooks

Profiles work alongside hooks. You can have both permission deny lists (hard blocks) and hooks (programmatic checks):

```json
{
  "permissions": {
    "deny": ["Bash(rm -rf *)"]
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hook": "bash hooks/block-dangerous.sh" }
    ]
  }
}
```

The deny list provides a fast, hard block. The hook provides more nuanced checks with custom logic.

## Designing Custom Profiles

1. **Start with zero-trust** — deny everything
2. **Add only what's needed** — for the specific task
3. **Test the boundaries** — try operations that should be blocked
4. **Document the use case** — so others know when to use the profile
5. **Review periodically** — remove permissions that are no longer needed
