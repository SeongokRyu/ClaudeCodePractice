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
```typescript
// BAD: SQL injection
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// GOOD: Parameterized query
const query = `SELECT * FROM users WHERE id = $1`;
db.query(query, [userId]);

// BAD: Command injection
exec(`ls ${userInput}`);

// GOOD: Use safe APIs
const files = fs.readdirSync(sanitizedPath);
```

### Cross-Site Scripting (XSS)
```typescript
// BAD: Direct HTML insertion
element.innerHTML = userInput;

// GOOD: Text content or sanitized HTML
element.textContent = userInput;
```

### Hardcoded Secrets
```typescript
// BAD
const API_KEY = "sk-1234567890";
const DB_PASSWORD = "admin123";

// GOOD
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;
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
- [ ] No known vulnerabilities in dependencies (`npm audit`)
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
