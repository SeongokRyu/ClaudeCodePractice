# Challenge: GitHub Actions Automation

## Overview

Set up GitHub Actions workflows that use `claude-code-action` to automate PR reviews, issue triage, code health checks, and release notes generation.

---

## Step 1: Understand claude-code-action

Read and understand the workflow files before deploying them.

### Tasks

1. Read `src/workflows/pr-review.yml`
2. Understand the key components:
   - **Trigger**: `issue_comment` event with `@claude` in the body
   - **Action**: `anthropics/claude-code-action@beta`
   - **Inputs**: `prompt`, `allowed_tools`, `max_turns`
   - **Authentication**: `ANTHROPIC_API_KEY` secret
3. Read the other workflow files to understand their patterns
4. Note how each workflow restricts Claude's capabilities with `allowed_tools`

### Key Configuration

```yaml
- uses: anthropics/claude-code-action@beta
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Review this PR for bugs and security issues"
    allowed_tools: "Read,Grep,Glob"
    max_turns: 10
```

### Verification

- Understand the trigger, permissions, and tool restrictions for each workflow
- Identify which workflows can modify code and which are read-only

---

## Step 2: PR Auto-Review

Set up the PR review workflow triggered by @claude mentions.

### Tasks

1. Copy `src/workflows/pr-review.yml` to your repository:
   ```bash
   mkdir -p .github/workflows
   cp src/workflows/pr-review.yml .github/workflows/claude-pr-review.yml
   ```
2. Set up the required secret:
   - Go to your repo Settings > Secrets and variables > Actions
   - Add `ANTHROPIC_API_KEY` with your Anthropic API key
3. Create a test PR and comment `@claude review this PR`
4. Observe Claude's review response

### How It Works

1. Someone comments `@claude` on a PR
2. The workflow triggers and checks out the PR branch
3. Claude analyzes the PR diff and codebase
4. Claude posts a review comment with findings

### Verification

- The workflow should trigger on `@claude` comments
- Claude should provide a meaningful code review
- The review should focus on the actual changes in the PR

---

## Step 3: Issue Auto-Triage

Set up automatic issue triage when new issues are created.

### Tasks

1. Copy `src/workflows/issue-triage.yml` to `.github/workflows/`
2. The workflow triggers on `issues.opened`
3. Claude will:
   - Read the issue title and body
   - Analyze the codebase for related files
   - Add appropriate labels (bug, feature, question, etc.)
   - Post a helpful initial response
4. Create a test issue and verify the triage

### Verification

- New issues should be automatically labeled
- Claude should identify related files and areas of the codebase
- The response should be helpful and not robotic

---

## Step 4: Nightly Code Health Check

Set up a scheduled workflow for code health monitoring.

### Tasks

1. Copy `src/workflows/nightly-health.yml` to `.github/workflows/`
2. The workflow runs on a cron schedule (default: 2 AM UTC)
3. Claude will:
   - Scan for TODO/FIXME comments
   - Check for outdated dependencies
   - Look for potential security issues
   - Generate a health report as a GitHub issue
4. Wait for the scheduled run or trigger manually

### Manual Trigger

```bash
# Trigger the workflow manually
gh workflow run nightly-health.yml
```

### Verification

- The workflow should create a new issue with the health report
- Reports should be actionable with specific file references
- The workflow should run on schedule and on manual trigger

---

## Step 5: Install the GitHub App

Set up the required GitHub App for full functionality.

### Tasks

1. In Claude Code interactive mode, run:
   ```
   /install-github-app
   ```
2. Follow the installation prompts
3. Grant the app access to your repository
4. Verify the app is installed:
   ```bash
   gh api repos/{owner}/{repo}/installation --jq '.id'
   ```

### Why the GitHub App

The GitHub App provides:
- Higher API rate limits
- Better authentication for posting comments
- Access to PR review APIs
- Webhook integration

### Verification

- The GitHub App should be installed on your repository
- Workflows should be able to post comments and create issues
- Authentication should work without personal access tokens

---

## Bonus Challenges

1. **Custom review focus**: Modify the PR review to focus on specific areas (security, performance, accessibility)
2. **Multi-repo**: Set up the same workflows across multiple repositories
3. **Review gate**: Make the PR review a required check before merging
4. **Cost tracking**: Add cost tracking to monitor API usage per workflow
5. **Conditional review**: Only trigger review for PRs that touch specific directories

---

## Key Takeaways

- `claude-code-action` brings Claude Code into your GitHub CI/CD pipeline
- Different trigger patterns serve different automation needs
- Tool restrictions are critical for safety in CI environments
- Scheduled workflows enable proactive code maintenance
- The GitHub App provides better integration than API keys alone
