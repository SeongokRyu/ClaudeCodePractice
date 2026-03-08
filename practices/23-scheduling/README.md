# Practice 23: Scheduling and Cron

## Goal

Learn to schedule and automate recurring Claude Code tasks: using `/loop` for polling, GitHub Actions cron schedules for nightly jobs, overnight autonomous refactoring with `--dangerously-skip-permissions`, and tmux-based autonomous sessions.

## Prerequisites

- [Practice 19: Headless Mode](../19-headless-mode/) — `claude -p` fundamentals

## Time

60-90 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

1. **`/loop` command** — Set up recurring checks within a Claude session
2. **GitHub Actions cron** — Nightly dependency checks and weekly reports
3. **Overnight refactoring** — Autonomous Claude running in isolated containers
4. **tmux sessions** — Long-running autonomous Claude tasks
5. **Safety patterns** — Guardrails for unattended Claude execution

## Key Concepts

### /loop Command

The `/loop` command tells Claude to repeat a task at regular intervals:
```
/loop every 5 minutes: check if the build is passing
```

### GitHub Actions Schedule

Use cron syntax for scheduled workflows:
```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Every day at 2 AM UTC
```

### Overnight Autonomous Work

For long-running refactoring tasks:
```bash
claude -p "refactor all error handling to use Result type" \
  --dangerously-skip-permissions \
  --max-turns 100
```

**Safety Requirements**:
- Run in an isolated container (Docker)
- Work on a separate branch
- Set `--max-turns` limit
- Review results before merging

### tmux Sessions

Run Claude in a detached terminal:
```bash
tmux new-session -d -s claude-work 'claude -p "..." --dangerously-skip-permissions'
```

## Directory Structure

```
23-scheduling/
├── README.md
├── CHALLENGE.md
└── src/
    ├── workflows/
    │   ├── nightly-deps.yml      # Nightly dependency check
    │   └── weekly-report.yml     # Weekly code quality report
    ├── scripts/
    │   ├── overnight-refactor.sh # Overnight autonomous refactoring
    │   └── tmux-autonomous.sh    # tmux session management
    └── docker/
        ├── Dockerfile            # Isolated Claude execution
        └── docker-compose.yml    # Container orchestration
```
