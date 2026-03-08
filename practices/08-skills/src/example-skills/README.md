# Example Skills

## What Are Skills?

Skills are reusable workflows defined in SKILL.md files. They encode repeatable processes — like code reviews, security scans, or deploy checklists — into instructions that Claude follows consistently every time.

Think of them as **runbooks for Claude**.

## Skill File Structure

A SKILL.md file has two parts:

### 1. Frontmatter (YAML, between `---` markers)

```yaml
---
description: Short description shown in skill list
allowed-tools: Read, Bash, Grep, Glob
argument-hint: "<file-path> [--strict]"
disable-model-invocation: false
---
```

### 2. Body (Markdown instructions)

The rest of the file is instructions Claude follows when the skill is invoked.

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `description` | Recommended | Short description shown when listing skills. Helps you find the right skill. |
| `allowed-tools` | Optional | Comma-separated list of tools the skill can use. Restricts Claude for safety. If omitted, all tools are available. |
| `argument-hint` | Optional | Usage hint shown when the skill is invoked. Helps users know what arguments to pass. |
| `disable-model-invocation` | Optional | When `true`, Claude will not make autonomous decisions. It reports results but does not take action. Useful for checklists and audits. |

## Dynamic Context (`!` Backtick)

Lines starting with `!` followed by a backtick command inject live data:

```markdown
Current branch:
!`git branch --show-current`

Recent commits:
!`git log --oneline -10`
```

When the skill is invoked:
1. The command runs in the project directory
2. The output replaces the `!` backtick line
3. Claude sees the fresh data as part of its instructions

**Use cases:**
- Injecting current git state (diff, log, branch)
- Reading current config files
- Getting system information

**Example:** See `pr-summary/SKILL.md`

## Fork Context (`@`)

Lines starting with `@` spawn subagents that work in the background:

```markdown
@Check all source files for TODO comments and report them
@Analyze test coverage and identify untested functions
```

When the skill is invoked:
1. Each `@` line spawns an independent subagent
2. Subagents work in parallel, gathering information
3. Results are fed back into the main skill context

**Use cases:**
- Parallel analysis tasks
- Background research
- Gathering data from multiple sources simultaneously

**Example:** See `security-scan/SKILL.md`

## Skill Location

### Project-Level (shared with team)
```
your-project/
└── .claude/
    └── skills/
        └── code-review/
            └── SKILL.md
```

### User-Level (personal)
```
~/.claude/
└── skills/
    └── my-workflow/
        └── SKILL.md
```

## Invoking Skills

```bash
# In a Claude session
> /code-review
> /pr-summary
> /security-scan --deep
> /deploy-checklist production
```

Skills are discovered by their directory name under `.claude/skills/`.

## Example Skills in This Directory

### code-review
A comprehensive code review skill that:
- Reads staged or working directory changes
- Checks for correctness, type safety, naming, performance, security
- Outputs a structured review with severity levels
- Uses dynamic context to inject the current git diff

### pr-summary
A PR summary generator that:
- Injects branch info, commits, and diff using dynamic context
- Generates a structured PR description
- Groups changes by category (Added, Changed, Fixed)
- Includes testing instructions

### security-scan
A security audit skill that:
- Uses fork context to run parallel checks (dependencies, secrets, auth)
- Scans for input validation, configuration, and data handling issues
- Outputs a categorized vulnerability report with severity levels

### deploy-checklist
A pre-deployment checklist that:
- Uses `disable-model-invocation: true` for reporting only (no autonomous fixes)
- Runs tests, build, lint, type check
- Checks environment variables, migrations, dependencies
- Reports a pass/fail verdict without taking action

## Tips

1. **Keep skills focused** — one skill, one workflow. Do not combine unrelated tasks.
2. **Use dynamic context for freshness** — `!` backtick ensures skills always work with current data.
3. **Use fork context for parallel work** — `@` lines run simultaneously, saving time.
4. **Restrict tools for safety** — `allowed-tools` prevents skills from doing things they should not.
5. **Use `disable-model-invocation`** for audit/reporting skills that should not modify anything.
6. **Name directories clearly** — the directory name becomes the `/command` name.
