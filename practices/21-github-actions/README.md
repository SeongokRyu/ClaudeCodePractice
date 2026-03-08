# Practice 21: GitHub Actions Automation

## Goal

Learn to use `claude-code-action` for automating GitHub workflows: PR auto-review triggered by @claude mentions, automatic issue triage, scheduled code health checks, and release notes generation.

## Prerequisites

- [Practice 19: Headless Mode](../19-headless-mode/) — `claude -p` fundamentals

## Time

60-90 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

1. **claude-code-action** — The official GitHub Action for Claude Code
2. **PR auto-review** — Trigger Claude reviews with @claude mention in PR comments
3. **Issue triage** — Automatically label and respond to new issues
4. **Scheduled checks** — Nightly code health and dependency audits
5. **Release notes** — Auto-generate release notes on tag push

## Key Concepts

### claude-code-action

The `anthropics/claude-code-action@beta` GitHub Action runs Claude Code in your CI/CD pipeline. It can:
- Read and analyze your codebase
- Comment on PRs and issues
- Create commits and push changes
- Use all Claude Code tools (Read, Edit, Bash, etc.)

### Trigger Patterns

| Trigger | Event | Use Case |
|---------|-------|----------|
| `@claude` mention | `issue_comment` | On-demand PR review |
| New issue | `issues.opened` | Auto-triage |
| Schedule | `schedule` (cron) | Nightly checks |
| Tag push | `push` (tags) | Release notes |

### Required Secrets

- `ANTHROPIC_API_KEY` — Your Anthropic API key (set in repo Settings > Secrets)

### Required GitHub App

Run `/install-github-app` in Claude Code to install the required GitHub App for your repository.

## Directory Structure

```
21-github-actions/
├── README.md
├── CHALLENGE.md
└── src/
    └── workflows/
        ├── pr-review.yml       # PR review on @claude mention
        ├── issue-triage.yml    # Auto-triage new issues
        ├── nightly-health.yml  # Scheduled code health check
        ├── release-notes.yml   # Release notes on tag push
        └── README.md           # Workflow documentation
```
