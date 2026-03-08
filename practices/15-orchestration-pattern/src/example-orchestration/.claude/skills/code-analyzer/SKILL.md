# Code Analyzer Skill

## Purpose

Analyzes TypeScript/JavaScript code quality and assigns scores.
This Skill defines the analysis criteria and scoring rules.

## Analysis Criteria

### 1. Complexity — 30 points

| Item | Criteria | Score |
|------|------|------|
| Function length | 20 lines or fewer | 10 pts |
| | 21-50 lines | 5 pts |
| | Over 50 lines | 0 pts |
| Nesting depth | 3 levels or fewer | 10 pts |
| | 4-5 levels | 5 pts |
| | 6 levels or more | 0 pts |
| Number of parameters | 3 or fewer | 10 pts |
| | 4-5 | 5 pts |
| | 6 or more | 0 pts |

### 2. Maintainability — 30 points

| Item | Criteria | Score |
|------|------|------|
| Type safety | No `any` usage | 10 pts |
| | `any` used 1-2 times | 5 pts |
| | `any` used 3+ times | 0 pts |
| Error handling | Appropriate try-catch | 10 pts |
| | Partially missing | 5 pts |
| | No error handling | 0 pts |
| Naming | Meaningful names | 10 pts |
| | Some unclear names | 5 pts |
| | Many single-character variables | 0 pts |

### 3. Best Practices — 40 points

| Item | Criteria | Score |
|------|------|------|
| Single Responsibility Principle | Compliant | 10 pts |
| | Some violations | 5 pts |
| | Many violations | 0 pts |
| DRY Principle | No duplication | 10 pts |
| | Minor duplication | 5 pts |
| | Significant duplication | 0 pts |
| Test existence | Test file exists | 10 pts |
| | Only partial coverage | 5 pts |
| | No tests | 0 pts |
| Documentation | JSDoc present | 10 pts |
| | Only partial coverage | 5 pts |
| | No documentation | 0 pts |

## Patterns to Detect

### Red Flags (Penalty factors)
- Leftover `console.log` debugging code
- 3 or more `// TODO` comments
- Hard-coded magic numbers
- Unused imports
- `@ts-ignore` usage

### Green Flags (Bonus factors)
- Consistent coding style
- Meaningful commit messages
- Separated interfaces/types
- Appropriate abstraction levels

## Output Format

### Per-file Report

```
| File | Complexity | Maintainability | Best Practices | Total | Grade |
|------|--------|-----------|---------|------|------|
| file.ts | X/30 | X/30 | X/40 | X/100 | A~F |
```

### Grade Criteria

- **A** (90-100): Excellent — Exemplary code
- **B** (80-89): Good — Minor room for improvement
- **C** (70-79): Average — Improvement needed
- **D** (60-69): Below average — Significant improvement needed
- **F** (0-59): Poor — Immediate refactoring required

### Overall Summary

```
Project average: X/100 (Grade)
Files analyzed: N
Files needing improvement: N
```
