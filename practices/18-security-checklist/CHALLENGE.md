# Challenge: Security Checklist

## Step 1: Reviewing Vulnerable Code

Open `src/vulnerable_app.py` and read the code yourself.

### Find Issues Yourself First

Read the code and look for security problems. Take notes on what you find:

```
My findings:
1. _______________
2. _______________
3. _______________
...
```

### Hints

Review the code from the following perspectives:
- Where is user input used directly in queries?
- Where are hardcoded secrets?
- What admin functions are accessible without authentication?
- Where is data in HTML output not escaped?
- Where can a user access another user's data?

---

## Step 2: Request Security Review from Claude

Request a security review from Claude based on the OWASP Top 10.

```
Please perform a security review of src/vulnerable_app.py based on the OWASP Top 10.

For each vulnerability:
1. OWASP category (A01~A10)
2. Location of vulnerable code (line number)
3. Attack scenario (how it can be exploited)
4. Remediation method

Find all vulnerabilities without exception.
```

### Checklist
- [ ] Did Claude find more vulnerabilities than you found yourself?
- [ ] Are there vulnerabilities you found that Claude missed?

---

## Step 3: Vulnerability Severity Assessment

Have Claude assess the severity of each vulnerability.

```
Please assess the severity of all discovered vulnerabilities.

Severity criteria:
- Critical: Immediately exploitable, system-wide impact
- High: Exploitable, data breach or privilege escalation
- Medium: Conditionally exploitable, limited impact
- Low: Difficult to exploit, minimal impact

Please organize in table format:
| # | Vulnerability | OWASP | Severity | Impact Scope |
```

### Determine Priorities

```
Please determine the remediation priority.
Sort by Critical → High → Medium → Low,
and include the estimated remediation time for each.
```

---

## Step 4: Fixing Vulnerabilities

Fix the vulnerabilities together with Claude.

### 4-1. Fix Critical/High Vulnerabilities

```
Please fix the Critical and High severity vulnerabilities in src/vulnerable_app.py.

Remediation principles:
1. SQL injection → Use parameterized queries
2. XSS → Escape output
3. Hardcoded secrets → Use environment variables
4. Missing authentication → Add middleware
5. IDOR → Add authorization checks
6. Input validation → Add schema validation

Write the fixed code in src/secure_app.py.
```

### 4-2. Fix Medium/Low Vulnerabilities

```
Please fix the remaining Medium and Low severity vulnerabilities as well.
Update src/secure_app.py.
```

---

## Step 5: Verify with Security Tests

Verify the fixed code is secure with tests.

### Run Tests

```bash
uv run pytest
```

Security tests are prepared in `src/test_vulnerable_app.py`.
These tests verify that the vulnerabilities have been fixed.

### Request Additional Tests from Claude

```
Please write additional security tests for src/secure_app.py.

Test scenarios:
1. SQL injection attempts are handled safely
2. XSS payloads are escaped
3. Unauthenticated admin API calls return 403
4. Accessing another user's data returns 403
5. Invalid input returns 400
```

---

## Step 6: Slopsquatting Detection

### Check for Fake Packages

Check `requirements-check.txt`. This file contains suspicious package names.

```
Please check the dependencies in requirements-check.txt.

For each package:
1. Is it a package that actually exists on PyPI?
2. Is the name similar to a well-known package? (typosquatting)
3. Is it a non-existent package that Claude might have recommended? (slopsquatting)
4. Is it a suspicious package with extremely low weekly downloads?

Organize suspicious packages in a table.
```

### Slopsquatting Prevention Checklist

```
Please create a checklist to verify before installing packages recommended by AI.

Items to include:
- Verify package existence on the official PyPI page
- Check weekly download count (minimum threshold)
- Package maintenance status (last update date)
- Verify GitHub repository
- Name similarity check (flask-limiter vs flask-limmiter)
```

---

## Security Checklist Summary

Check `src/security-checklist.md`. 8 security quality gates are defined.

Have Claude apply this checklist to the project:

```
Please apply the 8 security gates from src/security-checklist.md to the current project.
Determine PASS or FAIL for each gate.
```

---

## Success Criteria

- [ ] Identified at least 6 security vulnerabilities in the code
- [ ] Assessed the OWASP category and severity for each vulnerability
- [ ] Fixed all Critical/High vulnerabilities
- [ ] Security tests pass
- [ ] Understood the slopsquatting risk and created a prevention checklist

## Key Takeaways

1. **Security is a property, not a feature**: Security should be considered from the start, not added later
2. **OWASP Top 10 is the minimum**: Checking just 10 items prevents most vulnerabilities
3. **Use Claude as a security reviewer**: Effective when specific criteria are provided
4. **Verify with tests**: Always confirm with security tests after remediation
5. **Verify packages**: Always manually verify AI-recommended packages
