---
description: Pre-deployment checklist — verify everything before deploying
allowed-tools: Read, Bash, Grep, Glob
disable-model-invocation: true
argument-hint: "[staging|production]"
---

# Deploy Checklist

This is a non-interactive checklist. With `disable-model-invocation: true`, Claude will not make autonomous decisions — it will simply present the checklist results and let you decide.

## Pre-Deployment Checks

Run the following checks and report the results:

### 1. Tests
Run the test suite and report pass/fail:
```bash
npm test
```

### 2. Build
Verify the project builds without errors:
```bash
npm run build
```

### 3. Lint
Check for linting errors:
```bash
npm run lint
```

### 4. Type Check
Verify TypeScript types:
```bash
npx tsc --noEmit
```

### 5. Environment Variables
Check that all required environment variables are documented:
- Compare `.env.example` with the variables actually used in code
- Flag any variables used in code but missing from `.env.example`

### 6. Database Migrations
Check for pending migrations:
```bash
npx prisma migrate status
```

### 7. Dependencies
Check for security vulnerabilities:
```bash
npm audit
```

### 8. Git Status
Verify working directory is clean:
```bash
git status
git log --oneline -5
```

## Output Format

Present the results as a checklist:

```
## Deploy Readiness Report

- [x] Tests: All 42 tests passing
- [x] Build: Successful (no errors)
- [ ] Lint: 3 warnings found
- [x] Type Check: No type errors
- [x] Env Vars: All documented
- [x] Migrations: Up to date
- [ ] Dependencies: 1 moderate vulnerability
- [x] Git: Clean working directory

## Verdict
NOT READY — 2 issues need attention before deployment.
```

Do NOT fix any issues automatically. Only report them. The developer decides what to do.
