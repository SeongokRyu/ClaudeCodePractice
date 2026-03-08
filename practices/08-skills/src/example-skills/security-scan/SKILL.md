---
description: Scan the project for security vulnerabilities and bad practices
allowed-tools: Read, Bash, Grep, Glob
argument-hint: "[--deep] [--focus=deps|secrets|auth]"
---

# Security Scan

Perform a security audit of the current project.

## Background Analysis

@Check package.json and any lock files for dependencies with known vulnerabilities. Look for outdated packages that have had security patches released.

@Scan all source files for hardcoded secrets, API keys, passwords, tokens, or credentials. Check for patterns like `password = "..."`, `apiKey: "..."`, `SECRET_KEY`, Bearer tokens, and AWS access keys.

@Review authentication and authorization code for common vulnerabilities: missing auth checks on routes, insecure token storage, weak password requirements, missing CSRF protection, and improper session handling.

## Additional Checks

After the background analysis completes, also check for:

### Input Validation
- Search for unvalidated user input (query params, body, headers)
- Check for SQL injection risks (string concatenation in queries)
- Check for XSS risks (unescaped HTML rendering)
- Check for path traversal risks (user input in file paths)

### Configuration
- Check if debug mode is disabled in production configs
- Check if CORS is properly configured (not `*` in production)
- Check if HTTPS is enforced
- Check if security headers are set (CSP, HSTS, X-Frame-Options)

### Data Handling
- Check if sensitive data is logged (passwords, tokens, PII)
- Check if errors expose internal details to users
- Check if file uploads are validated (type, size, content)

## Output Format

```
## Security Scan Results

### Critical
- [CRITICAL] Description and file location
  **Risk:** What could go wrong
  **Fix:** How to fix it

### High
- [HIGH] Description and file location
  **Risk:** What could go wrong
  **Fix:** How to fix it

### Medium
- [MEDIUM] Description and file location

### Low
- [LOW] Description and file location

### Summary
- Critical: N
- High: N
- Medium: N
- Low: N
- Overall risk level: HIGH/MEDIUM/LOW
```
