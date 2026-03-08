# Challenge: Scheduling and Cron

## Overview

Set up scheduled and autonomous Claude Code tasks for overnight refactoring, nightly dependency checks, and recurring code quality monitoring.

---

## Step 1: Use /loop

Set up a recurring check within a Claude Code session.

### Tasks

1. Open Claude Code in interactive mode
2. Set up a loop to monitor build status:
   ```
   /loop every 5 minutes: run npm test and report if any tests are failing
   ```
3. Set up a loop to watch for TODO growth:
   ```
   /loop every 10 minutes: count TODO comments in src/ and alert if the count increased since last check
   ```
4. Observe how Claude:
   - Remembers the previous state
   - Only reports changes
   - Continues running until stopped

### Use Cases for /loop

- **Build monitoring**: Watch for test failures during a long refactor
- **Deployment monitoring**: Check health endpoint after deploying
- **File watching**: Monitor for changes in specific files
- **Progress tracking**: Report on the status of a long-running task

### Verification

- The loop should execute at the specified interval
- Claude should maintain state between iterations
- Use Ctrl+C to stop the loop gracefully

---

## Step 2: GitHub Actions Schedule

Set up nightly and weekly scheduled workflows.

### Tasks

1. Read `src/workflows/nightly-deps.yml`
2. Understand the cron schedule:
   ```yaml
   on:
     schedule:
       - cron: '0 3 * * 1-5'  # 3 AM UTC, weekdays
   ```
3. Copy to your repository:
   ```bash
   cp src/workflows/nightly-deps.yml .github/workflows/
   cp src/workflows/weekly-report.yml .github/workflows/
   ```
4. The nightly workflow:
   - Runs `npm audit` to find vulnerabilities
   - Uses Claude to analyze and prioritize findings
   - Creates an issue if critical vulnerabilities found
5. The weekly workflow:
   - Generates a comprehensive code quality report
   - Tracks metrics over time
   - Posts to a designated issue or Slack

### Manual Testing

```bash
# Trigger workflows manually
gh workflow run nightly-deps.yml
gh workflow run weekly-report.yml
```

### Verification

- Workflows should run on schedule
- Reports should be actionable and not noisy
- Critical findings should create issues automatically

---

## Step 3: Overnight Refactoring

Set up Claude for long-running autonomous refactoring in an isolated container.

### Tasks

1. Read `src/scripts/overnight-refactor.sh`
2. Read `src/docker/Dockerfile` and `src/docker/docker-compose.yml`
3. Understand the safety pattern:
   ```
   ┌─────────────────────────────────┐
   │  Docker Container (isolated)    │
   │  ┌───────────────────────────┐  │
   │  │  Git worktree (separate)  │  │
   │  │  ┌─────────────────────┐  │  │
   │  │  │  Claude session      │  │  │
   │  │  │  --max-turns 100     │  │  │
   │  │  │  --dangerously-skip  │  │  │
   │  │  └─────────────────────┘  │  │
   │  └───────────────────────────┘  │
   └─────────────────────────────────┘
   ```
4. Set up and run:
   ```bash
   # Build the container
   docker compose -f src/docker/docker-compose.yml build

   # Run overnight refactoring
   bash src/scripts/overnight-refactor.sh \
     --task "migrate all error handling to use custom Result<T, E> type" \
     --branch "refactor/result-type" \
     --max-turns 100
   ```
5. Review results in the morning (Step 5)

### Safety Checklist

- [ ] Running in a Docker container (not on host)
- [ ] Using a separate git branch
- [ ] `--max-turns` is set to prevent runaway
- [ ] Network access is restricted (no pushing)
- [ ] Results will be reviewed before merging

### Verification

- The container should start and Claude should begin working
- Work should be on a separate branch
- The script should log progress to a file
- `--max-turns` should prevent infinite loops

---

## Step 4: tmux Autonomous Session

Set up a tmux-based autonomous Claude session.

### Tasks

1. Read `src/scripts/tmux-autonomous.sh`
2. Start an autonomous session:
   ```bash
   bash src/scripts/tmux-autonomous.sh start \
     --name "overnight-refactor" \
     --task "add comprehensive error handling to all API endpoints" \
     --max-turns 50
   ```
3. Monitor the session:
   ```bash
   # Check if still running
   bash src/scripts/tmux-autonomous.sh status --name "overnight-refactor"

   # View live output
   bash src/scripts/tmux-autonomous.sh attach --name "overnight-refactor"
   # (Ctrl+B, D to detach without stopping)

   # View log file
   bash src/scripts/tmux-autonomous.sh logs --name "overnight-refactor"
   ```
4. Stop the session:
   ```bash
   bash src/scripts/tmux-autonomous.sh stop --name "overnight-refactor"
   ```

### tmux vs Docker

| Feature | tmux | Docker |
|---------|------|--------|
| Isolation | Process-level | Container-level |
| Setup | Simple | Requires Docker |
| Safety | Lower | Higher |
| Resource control | Limited | Full |
| Best for | Short tasks | Overnight work |

### Verification

- The tmux session should start in the background
- You should be able to attach and detach without interrupting
- Logs should capture all Claude output
- The stop command should clean up properly

---

## Step 5: Review Results

Check what the overnight session accomplished.

### Tasks

1. Review the git log on the refactoring branch:
   ```bash
   git log --oneline refactor/result-type
   ```
2. Review the diff:
   ```bash
   git diff main...refactor/result-type --stat
   git diff main...refactor/result-type
   ```
3. Use Claude to review the overnight work:
   ```bash
   git diff main...refactor/result-type | claude -p "Review this refactoring work done by an overnight Claude session. Check for:
   1. Consistency of changes across files
   2. Any incomplete or broken transformations
   3. Test coverage for new patterns
   4. Anything that looks incorrect or unsafe"
   ```
4. Run tests:
   ```bash
   git checkout refactor/result-type
   npm test
   ```
5. Decide: merge, continue refactoring, or discard

### Verification

- Changes should be consistent and complete
- Tests should pass (or test updates should be included)
- No security regressions should be introduced
- The refactoring should be reviewable and understandable

---

## Bonus Challenges

1. **Notification**: Send a Slack/email notification when overnight work completes
2. **Checkpoint commits**: Have Claude commit progress every N turns
3. **Cost budgeting**: Set a maximum dollar cost for overnight sessions
4. **Multi-repo overnight**: Run overnight sessions across multiple repositories
5. **Rollback automation**: Automatically rollback if tests fail after refactoring

---

## Key Takeaways

- `/loop` is ideal for short-term monitoring within an interactive session
- GitHub Actions cron handles recurring scheduled tasks reliably
- Overnight autonomous work requires strong isolation (Docker containers)
- `--dangerously-skip-permissions` should only be used in isolated environments
- Always review autonomous work before merging — trust but verify
- tmux provides a lightweight alternative for shorter autonomous tasks
- Set `--max-turns` to prevent runaway sessions and control costs
