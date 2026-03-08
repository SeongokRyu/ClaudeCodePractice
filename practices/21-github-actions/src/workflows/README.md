# GitHub Actions Workflows

## Overview

These workflows use `anthropics/claude-code-action@beta` to automate development tasks with Claude Code in GitHub Actions.

## Workflows

### 1. PR Review (`pr-review.yml`)

**Trigger**: Comment containing `@claude` on a Pull Request

**What it does**:
- Checks out the PR branch
- Claude reviews the diff for bugs, security issues, and style problems
- Posts findings as a PR comment

**Tools allowed**: Read, Grep, Glob (read-only)

**Example trigger**:
```
@claude review this PR, focusing on security
@claude are there any performance concerns here?
```

---

### 2. Issue Triage (`issue-triage.yml`)

**Trigger**: New issue opened

**What it does**:
- Reads the issue title and body
- Searches codebase for related files
- Adds appropriate labels (bug, feature, question, etc.)
- Posts an initial helpful response

**Tools allowed**: Read, Grep, Glob, Bash (gh issue commands only)

**Labels to create** (if not existing):
- `bug` — Bug reports
- `feature` — Feature requests
- `question` — Questions about usage
- `documentation` — Documentation improvements
- `good-first-issue` — Suitable for newcomers

---

### 3. Nightly Health Check (`nightly-health.yml`)

**Trigger**: Cron schedule (2 AM UTC, Mon-Fri) or manual dispatch

**What it does**:
- TODO/FIXME audit with staleness detection
- Dependency health check
- Code quality analysis (long functions, duplication)
- Security scan for hardcoded secrets
- Creates a GitHub issue with findings

**Tools allowed**: Read, Grep, Glob, Bash (full access)

**Manual trigger**:
```bash
gh workflow run claude-nightly-health.yml
```

---

### 4. Release Notes (`release-notes.yml`)

**Trigger**: Tag push matching `v*.*.*`

**What it does**:
- Analyzes commits between previous tag and new tag
- Groups changes by category (features, fixes, etc.)
- Creates a GitHub release with formatted notes

**Tools allowed**: Read, Grep, Glob, Bash (full access)

**Trigger**:
```bash
git tag v1.2.0
git push origin v1.2.0
```

---

## Setup Instructions

### 1. Add the API Key Secret

```bash
# Using GitHub CLI
gh secret set ANTHROPIC_API_KEY --body "sk-ant-your-key-here"

# Or: Settings > Secrets and variables > Actions > New repository secret
```

### 2. Install the GitHub App

In Claude Code interactive mode:
```
/install-github-app
```

### 3. Copy Workflows

```bash
# Copy all workflows at once
mkdir -p .github/workflows
cp src/workflows/pr-review.yml .github/workflows/claude-pr-review.yml
cp src/workflows/issue-triage.yml .github/workflows/claude-issue-triage.yml
cp src/workflows/nightly-health.yml .github/workflows/claude-nightly-health.yml
cp src/workflows/release-notes.yml .github/workflows/claude-release-notes.yml
```

### 4. Create Required Labels

```bash
gh label create "bug" --color "d73a4a" --description "Bug report" 2>/dev/null || true
gh label create "feature" --color "0075ca" --description "Feature request" 2>/dev/null || true
gh label create "question" --color "d876e3" --description "Question" 2>/dev/null || true
gh label create "documentation" --color "0075ca" --description "Documentation" 2>/dev/null || true
gh label create "maintenance" --color "ededed" --description "Maintenance" 2>/dev/null || true
gh label create "good-first-issue" --color "7057ff" --description "Good for newcomers" 2>/dev/null || true
```

## Cost Considerations

| Workflow | Frequency | Est. Cost/Run | Monthly Est. |
|----------|-----------|---------------|--------------|
| PR Review | On demand | $0.05-0.20 | Varies |
| Issue Triage | Per issue | $0.02-0.05 | Varies |
| Nightly Health | 5x/week | $0.10-0.30 | $2-6 |
| Release Notes | Per release | $0.05-0.15 | < $1 |

Costs depend on codebase size and the number of turns Claude needs.

## Troubleshooting

### Workflow not triggering
- Check that the workflow file is in `.github/workflows/`
- Verify the trigger event matches (e.g., `issue_comment` for PR reviews)
- Check Actions tab for workflow run logs

### Authentication errors
- Verify `ANTHROPIC_API_KEY` is set in repo secrets
- Ensure the GitHub App is installed
- Check permissions in the workflow YAML

### Claude timeout
- Increase `max_turns` if Claude needs more steps
- Reduce the scope of the prompt
- Split large tasks into smaller workflows
