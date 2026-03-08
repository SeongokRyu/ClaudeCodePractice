# Practice 08: Skills 만들기

## Goal

Learn to create SKILL.md files — reusable workflows with frontmatter, dynamic context, fork context, and auto-invocation. Build skills that encode your team's expertise into shareable, consistent workflows.

## Prerequisites

- [Practice 05: CLAUDE.md 작성법](../05-claude-md/)

## Time

30-45 minutes

## Why This Matters

Skills encode your team's expertise into reusable, shareable workflows that Claude follows consistently. Instead of typing the same complex instructions every time, you write a SKILL.md once and invoke it with `/skill-name`.

Think of Skills as:
- **Runbooks** that Claude executes
- **Recipes** for common workflows
- **Team knowledge** captured as instructions

## What You Will Learn

1. SKILL.md file structure and frontmatter
2. Creating basic skills with step-by-step instructions
3. Dynamic context with `!` backtick syntax (runs commands, injects output)
4. Fork context (runs as subagent in background)
5. Frontmatter fields: description, allowed-tools, argument-hint, disable-model-invocation
6. Invoking skills with `/skill-name`

## Directory Structure

```
src/
└── example-skills/
    ├── code-review/
    │   └── SKILL.md          # Code review skill with frontmatter
    ├── pr-summary/
    │   └── SKILL.md          # PR summary using dynamic context
    ├── security-scan/
    │   └── SKILL.md          # Security scan with fork context
    ├── deploy-checklist/
    │   └── SKILL.md          # Deploy checklist (no model invocation)
    └── README.md             # Skill structure explained
```

## Key Concepts

### Skill File Location

Skills are SKILL.md files placed in:
- `.claude/skills/` — project-level skills
- `~/.claude/skills/` — global skills (available in all projects)

### Frontmatter

```yaml
---
description: Short description shown in skill list
allowed-tools: Edit, Write, Bash, Read
argument-hint: "<file-path> [--strict]"
disable-model-invocation: false
---
```

### Dynamic Context

Use `!` followed by a backtick command to inject live data:

```markdown
Current git diff:
!`git diff --staged`
```

The command runs when the skill is invoked, and the output replaces the line.

### Fork Context

Use `@` to run a subagent that gathers context in the background:

```markdown
@Check for security vulnerabilities in package.json dependencies
```

The subagent runs independently and feeds results back into the skill.
