# Challenge: Creating Skills

## Step 1: Read the Example Skills

Review all files in `src/example-skills/`:

1. `code-review/SKILL.md` — A basic skill with frontmatter and step-by-step instructions
2. `pr-summary/SKILL.md` — Uses dynamic context (`!` backtick) to inject git data
3. `security-scan/SKILL.md` — Uses fork context (`@`) for background analysis
4. `deploy-checklist/SKILL.md` — Uses `disable-model-invocation: true`

Read `src/example-skills/README.md` for a detailed explanation of each part.

Questions to answer:
- What is the purpose of the `description` frontmatter field?
- What does `allowed-tools` restrict?
- When would you use `disable-model-invocation: true`?
- What is the difference between `!` backtick and `@` context?

---

## Step 2: Create a Code Review Skill

Create your own code review skill:

1. Create the directory: `mkdir -p .claude/skills`
2. Create `.claude/skills/code-review/SKILL.md`
3. Add frontmatter with description and allowed-tools
4. Write step-by-step instructions for reviewing code

Your skill should:
- Look at the staged git diff
- Check for common issues (error handling, type safety, naming)
- Provide a structured review with severity levels
- Suggest specific improvements

Test it:
```bash
claude
> /code-review
```

---

## Step 3: Add Frontmatter

Enhance your skill with frontmatter:

```yaml
---
description: Review staged changes for bugs, style issues, and improvements
allowed-tools: Read, Bash, Grep, Glob
argument-hint: "[--strict] [--focus=security|performance|style]"
---
```

Key frontmatter fields:
- **description**: Shown when listing skills (helps you find the right one)
- **allowed-tools**: Restricts which tools the skill can use (security measure)
- **argument-hint**: Shows usage hint when the skill is invoked

Test with arguments:
```bash
> /code-review --strict --focus=security
```

---

## Step 4: Create a Skill with Dynamic Context

Create a PR summary skill that uses `!` backtick syntax:

1. Create `.claude/skills/pr-summary/SKILL.md`
2. Use `!` backtick to inject live data:

```markdown
!`git log --oneline main..HEAD`
!`git diff --stat main..HEAD`
```

When the skill is invoked, these commands run and their output is injected into the prompt. This means the skill always has fresh data.

Test it:
```bash
# Make sure you have commits on a feature branch
> /pr-summary
```

The skill should generate a PR summary based on the actual current diff.

---

## Step 5: Create a Skill with Fork Context

Create a security scan skill that uses fork context:

1. Create `.claude/skills/security-scan/SKILL.md`
2. Use `@` to launch background subagents:

```markdown
@Check package.json for known vulnerable dependency versions
@Scan source files for hardcoded secrets or API keys
@Review authentication and authorization patterns
```

Each `@` line spawns a subagent that works independently, then feeds results back.

Test it:
```bash
> /security-scan
```

---

## Step 6: Test Your Skills

Verify all skills work correctly:

```bash
claude

# List available skills
> What skills are available?

# Run each skill
> /code-review
> /pr-summary
> /security-scan
```

Check that:
- Skills appear in the skill list with their descriptions
- Dynamic context injects fresh data
- Fork context gathers information in the background
- Allowed-tools restrictions are enforced

---

## Bonus: Skill Organization

Organize skills for a team:
- Project-specific skills in `.claude/skills/` (committed to repo)
- Personal workflow skills in `~/.claude/skills/` (not committed)
- Shared team skills distributed as a git repo

---

## Success Criteria

You have completed this practice when:
- [x] You can explain the SKILL.md file structure
- [x] You have created a skill with frontmatter
- [x] You have created a skill with dynamic context (`!` backtick)
- [x] You understand fork context (`@`) and when to use it
- [x] You can invoke skills with `/skill-name`
- [x] You understand `disable-model-invocation` and `allowed-tools`
