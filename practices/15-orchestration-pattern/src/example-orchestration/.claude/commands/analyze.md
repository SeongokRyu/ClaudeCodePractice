# /analyze Command

Analyze code quality for the specified path using the Code Analyzer pipeline.

## Usage

```
/analyze <target-path>
```

## Arguments

- `$ARGUMENTS`: Directory or file path to analyze
  - Default: `src/`
  - Examples: `/analyze src/utils/`, `/analyze lib/`

## Execution Flow

```
/analyze src/
    ↓
[1] Argument parsing: target = $ARGUMENTS (default: src/)
    ↓
[2] Call analyzer-agent
    → Agent loads code-analyzer Skill
    → Discovers target files
    → Performs per-file analysis
    ↓
[3] Format and output results
    → Per-file score table
    → Overall project summary
    → Improvement suggestions
```

## Agent Delegation

This Command delegates the analysis work to **analyzer-agent**.

- Agent location: `.claude/agents/analyzer-agent.md`
- Skill used by the Agent: `.claude/skills/code-analyzer/SKILL.md`

Passes the target path to the Agent and displays the Agent's analysis results in a user-friendly format.

## Expected Output

1. **Per-file quality score table** — Complexity, maintainability, and best practices scores for each file
2. **Overall project average score** — Code quality grade for the entire project
3. **Top 3 improvement priorities** — Files most in need of improvement
4. **Specific improvement suggestions** — Actionable suggestions for each file

## Example Output

```
## Code Quality Analysis Report

### Summary
- Analysis target: src/
- Files analyzed: 5
- Project average: 78/100 (C)

### File Details
| File | Complexity | Maintainability | Best Practices | Total | Grade |
|------|--------|-----------|---------|------|------|
| app.ts | 25/30 | 20/30 | 30/40 | 75/100 | C |
| utils.ts | 30/30 | 28/30 | 35/40 | 93/100 | A |
| ...  | ...    | ...       | ...     | ...  | ... |

### Top 3 Improvement Targets
1. router.ts (62/100) — Function length exceeded, nesting depth 5 levels
2. db.ts (68/100) — `any` type used 4 times, insufficient error handling
3. app.ts (75/100) — No tests, missing JSDoc

### Recommendations
- router.ts: Split handleRequest function into 3 smaller functions
- db.ts: Replace `any` types with specific interfaces
- app.ts: Add unit tests, write JSDoc for key functions
```
