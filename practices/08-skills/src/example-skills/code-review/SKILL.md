---
description: Review code changes for bugs, style issues, and improvements
allowed-tools: Read, Bash, Grep, Glob
argument-hint: "[--strict] [--focus=security|performance|style]"
---

# Code Review

Review the staged changes (or working directory changes if nothing is staged) and provide a structured code review.

## Context

Current staged changes:
!`git diff --staged`

If no staged changes, review working directory changes:
!`git diff`

## Review Checklist

For each changed file, check the following:

### Correctness
- Are there any logic errors or off-by-one bugs?
- Are edge cases handled (null, undefined, empty arrays, etc.)?
- Are error cases handled properly (try/catch, error returns)?

### Type Safety (TypeScript)
- Are types properly defined (no `any` types)?
- Are function parameters and return types annotated?
- Are null/undefined checks present where needed?

### Naming and Clarity
- Are variable and function names descriptive and consistent?
- Is the code self-documenting or does it need comments?

### Performance
- Are there unnecessary loops or repeated computations?
- Are database queries efficient (N+1 problem)?
- Are large objects being cloned unnecessarily?

### Security
- Is user input validated and sanitized?
- Are there hardcoded secrets or credentials?
- Is sensitive data properly handled?

## Output Format

Provide the review in this format:

```
## Review Summary
- Files reviewed: N
- Issues found: N (X critical, Y warnings, Z suggestions)

## Issues

### [CRITICAL] filename.ts:L42
Description of the critical issue.
**Suggestion:** How to fix it.

### [WARNING] filename.ts:L15
Description of the warning.
**Suggestion:** How to improve it.

### [SUGGESTION] filename.ts:L88
Description of the suggestion.
**Suggestion:** How to improve it.

## Overall Assessment
Brief summary of code quality and readiness for merge.
```
