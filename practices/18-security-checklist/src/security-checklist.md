# 8 Security Quality Gates

These are the 8 security quality gates that code must pass before being deployed to production.

## Gate 1: Secrets Management

- [ ] Are there no hardcoded secret keys, API keys, or passwords?
- [ ] Are secrets managed via environment variables or a secrets manager?
- [ ] Is the `.env` file included in `.gitignore`?
- [ ] Have secrets never been exposed in the commit history?

**Verification method**: `grep -r "password\|secret\|api_key\|token" --include="*.ts" src/`

## Gate 2: Input Validation

- [ ] Is all user input validated? (type, length, format)
- [ ] Are parameterized queries used for SQL/NoSQL queries?
- [ ] Is user data escaped in HTML output?
- [ ] Are file upload type and size validated?

**Verification method**: Review all `req.body`, `req.params`, `req.query` usage in request handlers

## Gate 3: Authentication & Authorization

- [ ] Is authentication applied to all protected endpoints?
- [ ] Is an expiration time set for authentication tokens?
- [ ] Is authorization checking properly performed? (RBAC/ABAC)
- [ ] Are passwords securely hashed? (bcrypt, argon2)

**Verification method**: Verify that authentication middleware is applied to each route

## Gate 4: Data Protection

- [ ] Is sensitive data excluded from API responses?
- [ ] Are passwords, tokens, etc. not logged?
- [ ] Is HTTPS enforced?
- [ ] Is sensitive data encrypted at rest?

**Verification method**: Review `password`, `token`, `secret` fields in API response schemas

## Gate 5: Error Handling

- [ ] Do error responses not expose internal information? (stack traces, DB queries)
- [ ] Is a consistent error format used?
- [ ] Are unexpected errors handled safely?
- [ ] Do error logs contain sufficient information? (excluding sensitive data)

**Verification method**: Check whether error handlers return `error.message`, `error.stack`

## Gate 6: CORS & Headers

- [ ] Does CORS allow only required domains? (no `*`)
- [ ] Are security headers configured?
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security`
  - `Content-Security-Policy`
- [ ] Is unnecessary server information not exposed? (remove `X-Powered-By`)

**Verification method**: Review response headers

## Gate 7: Dependencies

- [ ] Are there no packages with known vulnerabilities? (`npm audit`)
- [ ] Are there no suspicious package names? (slopsquatting/typosquatting)
- [ ] Are package versions pinned? (using lock files)
- [ ] Have unnecessary dependencies been removed?

**Verification method**: `npm audit`, check each package's npm page

## Gate 8: Access Control

- [ ] Are there no IDOR vulnerabilities? (ownership verification on direct object references)
- [ ] Is the principle of least privilege applied?
- [ ] Is additional security applied to admin functions?
- [ ] Is rate limiting applied?

**Verification method**: Review ownership/permission verification logic when accessing resources

---

## How to Use

### Request Gate Application from Claude

```
Please apply the 8 security gates from src/security-checklist.md to the current project.
Determine PASS or FAIL for each gate, and suggest remediation methods for items that FAIL.
```

### Result Format

| Gate | Item | Status | Notes |
|------|------|--------|-------|
| 1 | Secrets Management | FAIL | JWT_SECRET hardcoded |
| 2 | Input Validation | FAIL | SQL injection possible |
| ... | ... | ... | ... |

### Pass Criteria

- **Deployable**: All gates PASS
- **Conditional deployment**: Gates 1-4 PASS, some of Gates 5-8 FAIL (improvement plan required)
- **Not deployable**: Any of Gates 1-4 FAIL
