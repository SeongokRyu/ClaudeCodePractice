# Skill: Security Review

## Description
This skill provides a security review checklist for code review. Load this skill when reviewing code for security issues.

## Input Validation Checklist
- [ ] All user inputs are validated before use
- [ ] String inputs have length limits
- [ ] Numeric inputs have range checks
- [ ] Email/URL inputs are validated with proper patterns
- [ ] File paths are sanitized (no path traversal: `../`)
- [ ] Array inputs have size limits

## Common Vulnerability Patterns

### Injection Attacks
```python
# BAD: SQL injection
query = f"SELECT * FROM users WHERE id = '{user_id}'"

# GOOD: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

# BAD: Command injection
os.system(f"ls {user_input}")

# GOOD: Use safe APIs
files = os.listdir(sanitized_path)
# or use subprocess with list args
subprocess.run(["ls", sanitized_path], check=True)
```

### Hardcoded Secrets
```python
# BAD
API_KEY = "sk-1234567890"
DB_PASSWORD = "admin123"

# GOOD
API_KEY = os.environ.get("API_KEY")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```

## Authentication & Authorization
- [ ] Passwords are hashed (bcrypt/argon2), never stored in plaintext
- [ ] Tokens have expiration times
- [ ] Token validation checks expiration
- [ ] Sensitive operations require re-authentication
- [ ] Role-based access control is enforced

## Data Protection
- [ ] Sensitive data is not logged
- [ ] Error messages don't leak internal details
- [ ] PII is handled according to privacy requirements
- [ ] Data is encrypted at rest and in transit

## Dependencies
- [ ] No known vulnerabilities in dependencies (`pip-audit` / `safety check`)
- [ ] Dependencies are from trusted sources
- [ ] Dependency versions are pinned
- [ ] No unnecessary dependencies

## Security Review Output Format
```
### Security Assessment: LOW | MEDIUM | HIGH | CRITICAL

### Findings
1. [SEVERITY] Description — File:line — Remediation
2. [SEVERITY] Description — File:line — Remediation

### Positive Practices
- What's already done well

### Recommendations
1. Priority fix: ...
2. Short-term: ...
```
