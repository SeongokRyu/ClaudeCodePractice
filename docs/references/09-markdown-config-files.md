# Claude Code Markdown Configuration Files Complete Guide

---

## Full .claude/ Directory Structure

```
project-root/
+-- CLAUDE.md                        # Team project rules (shared via git)
+-- CLAUDE.local.md                  # Personal project settings (gitignore)
+-- .mcp.json                        # MCP server configuration
+-- .claude/
|   +-- CLAUDE.md                    # Alternate team rules location
|   +-- settings.json                # Team shared settings
|   +-- settings.local.json          # Personal settings (gitignore)
|   +-- agents/                      # Subagent definitions
|   |   +-- *.md
|   +-- skills/                      # Skill definitions
|   |   +-- <skill-name>/
|   |       +-- SKILL.md
|   +-- commands/                    # Slash commands (legacy, merged into skills)
|   |   +-- *.md
|   +-- rules/                       # Path-specific rule files
|   |   +-- *.md
|   +-- agent-memory/                # Subagent project memory
|   |   +-- <agent-name>/MEMORY.md
|   +-- agent-memory-local/          # Subagent local memory (gitignore)

~/.claude/
+-- CLAUDE.md                        # User global rules
+-- settings.json                    # User global settings
+-- agents/*.md                      # User subagents
+-- skills/<name>/SKILL.md           # User skills
+-- commands/*.md                    # User commands
+-- rules/*.md                       # User rules
+-- agent-memory/<agent>/MEMORY.md   # User agent memory
+-- projects/<project>/memory/       # Per-project Auto Memory
    +-- MEMORY.md
    +-- <topic>.md
```

---

## 1. CLAUDE.md -- Project Constitution

### All Variants and Locations (by priority)

| Priority | Location | Shared | Purpose |
|----------|----------|--------|---------|
| 1 (highest) | Managed policy: `/etc/claude-code/CLAUDE.md` (Linux) | Organization | Organization-wide rules (cannot be overridden) |
| 2 | CLI arguments | Session | Per-session overrides |
| 3 | `./CLAUDE.local.md` | No | Personal project settings |
| 4 | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Git | Team project rules |
| 5 (lowest) | `~/.claude/CLAUDE.md` | No | User global rules |

### Key Behaviors
- CLAUDE.md from parent directories are all loaded at startup (upward loading)
- CLAUDE.md from child directories are loaded when those files are accessed (downward/lazy)
- `@path/to/import` syntax for including external files (max 5 levels)
- **Recommended to keep under 200 lines**
- `claudeMdExcludes` to skip unnecessary CLAUDE.md files in monorepos

---

## 2. .claude/agents/*.md -- Subagent Definitions

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase+hyphens) |
| `description` | Yes | When to use this agent |
| `tools` | No | Allowed tools list (inherits all if omitted) |
| `disallowedTools` | No | Tools to deny |
| `model` | No | sonnet, opus, haiku, inherit |
| `permissionMode` | No | default, acceptEdits, plan, etc. |
| `maxTurns` | No | Maximum number of turns |
| `skills` | No | Skills to preload |
| `memory` | No | Persistent memory: user, project, local |
| `background` | No | Whether to run in background |
| `isolation` | No | worktree isolation |
| `hooks` | No | Hooks specific to this agent |
| `mcpServers` | No | Available MCP servers |

### Example
```markdown
---
name: code-reviewer
description: Quality/security review after code changes. Runs automatically on changes.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: user
---
As a senior code reviewer, review the changes.
```

---

## 3. .claude/skills/*/SKILL.md -- Skill Definitions

### Directory Structure
```
my-skill/
+-- SKILL.md           # Main instructions (required)
+-- template.md        # Template for Claude to fill
+-- reference.md       # Detailed reference documentation
+-- examples/          # Examples
+-- scripts/           # Scripts
```

### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `name` | Display name (max 64 characters) |
| `description` | Used for automatic invocation judgment |
| `argument-hint` | Autocomplete hint (`[issue-number]`) |
| `disable-model-invocation` | true = only user can invoke |
| `user-invocable` | false = hidden from `/` menu |
| `allowed-tools` | Tools allowed when skill is active |
| `model` | Model to use when skill is active |
| `context` | `fork` = run in subagent context |
| `agent` | Agent type to use with `context: fork` |

### Dynamic Context (Shell Command Execution)
```markdown
---
name: pr-summary
context: fork
agent: Explore
---
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

### String Substitution
- `$ARGUMENTS` -- full arguments
- `$ARGUMENTS[N]` or `$N` -- Nth argument
- `${CLAUDE_SKILL_DIR}` -- SKILL.md directory path

---

## 4. .claude/commands/*.md -- Slash Commands (Legacy)

Merged into Skills. Existing files continue to work, but Skills are recommended for new ones.
If a Skill and Command share the same name, the Skill takes priority.

---

## 5. .claude/rules/*.md -- Path-Specific Rules

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/**/*.test.ts"
---
# API Development Rules
- Input validation required for all endpoints
- Use standard error response format
```

- Without `paths`, always loaded
- With `paths`, loaded only when working with matching files
- Symlinks can share rules across multiple projects

---

## 6. MEMORY.md -- Auto Memory

```
~/.claude/projects/<project>/memory/
+-- MEMORY.md          # Only first 200 lines loaded at startup
+-- debugging.md       # Topic-specific files (loaded on demand)
+-- api-conventions.md
```

- Git worktrees share the same directory
- `autoMemoryEnabled` setting or `/memory` toggle

---

## 7. .mcp.json -- MCP Server Configuration

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "remote-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "headers": { "Authorization": "Bearer ${API_KEY}" }
    }
  }
}
```

Environment variable expansion supported: `${VAR}`, `${VAR:-default}`

---

## 8. settings.json -- Project Settings

```json
{
  "permissions": {
    "allow": ["Bash(npm run lint)"],
    "deny": ["Read(./.env)"]
  },
  "env": { "ENABLE_TOOL_SEARCH": "true" },
  "hooks": { ... },
  "autoMemoryEnabled": true,
  "claudeMdExcludes": ["**/irrelevant/CLAUDE.md"]
}
```

---

## 9. Community Convention Files (Unofficial)

| File | Purpose |
|------|---------|
| HANDOFF.md | Session handoff (what was tried, successes/failures, remaining work) |
| SPEC.md | Feature spec (written using interview technique) |
| MIGRATION.md | Migration progress tracking |

---

## Recommended Configurations

### Minimal Configuration (All Projects)
```
CLAUDE.md                    # Project rules
.claude/settings.json        # Permission/hook settings
```

### Standard Configuration (Team Projects)
```
CLAUDE.md
CLAUDE.local.md
.claude/settings.json
.claude/rules/               # Path-specific rules
.mcp.json                    # MCP servers
```

### Advanced Configuration (Production-Grade)
```
CLAUDE.md
CLAUDE.local.md
.claude/settings.json
.claude/settings.local.json
.claude/rules/               # Path-specific rules
.claude/agents/              # Custom agents
.claude/skills/              # Reusable workflows
.mcp.json                    # MCP servers
```

### Enterprise Configuration (Full Set)
```
All of the above +
Managed policy CLAUDE.md           # Organization-wide rule enforcement
Managed policy managed-settings.json  # Organization settings enforcement
Managed policy managed-mcp.json    # Organization MCP enforcement
Plugin directory                   # Per-team extensions
```
