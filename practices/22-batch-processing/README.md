# Practice 22: Batch Processing and Fan-Out

## Goal

Learn to process multiple files or tasks in parallel using Claude Code's `/batch` command, `xargs -P` for fan-out parallelism, and result aggregation techniques.

## Prerequisites

- [Practice 19: Headless Mode](../19-headless-mode/) — `claude -p` fundamentals

## Time

60-90 minutes

## Difficulty

★★★ (Advanced)

## What You'll Learn

1. **`/batch` command** — Apply the same change across multiple files
2. **Fan-out with xargs** — Run multiple `claude -p` instances in parallel
3. **Result aggregation** — Combine outputs from parallel Claude runs
4. **Batch migration** — Migrate legacy code patterns at scale
5. **Performance comparison** — Serial vs parallel execution

## Key Concepts

### /batch Command

The `/batch` command tells Claude to apply a transformation across multiple matching files:
```
/batch "migrate all callback functions to async/await in src/legacy/"
```

### Fan-Out Pattern

Run multiple independent Claude tasks in parallel:
```bash
find src/ -name "*.ts" | xargs -P 4 -I {} claude -p "review {}" --output-format json
```

### Result Aggregation

Combine JSON outputs from parallel runs:
```bash
# Each run outputs a JSON file
# Aggregate them into a single report
jq -s '.' results/*.json > combined-report.json
```

## Directory Structure

```
22-batch-processing/
├── README.md
├── CHALLENGE.md
└── src/
    ├── scripts/
    │   ├── parallel-review.sh     # Parallel code review
    │   ├── batch-migrate.sh       # Batch file migration
    │   └── aggregate-results.sh   # Result aggregation
    └── legacy/
        ├── module-a.ts            # Legacy callback code
        ├── module-b.ts            # Legacy callback code
        └── module-c.ts            # Legacy callback code
```
