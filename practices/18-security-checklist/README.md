# Practice 18: Security Checklist

## Goal

Learn the security review workflow. Analyze vulnerable code based on the OWASP Top 10, fix vulnerabilities, and learn how to detect slopsquatting (fake package attacks).

## Prerequisites

- Practice 01 (Golden Workflow) completed

## Time

45-60 minutes

## Difficulty

★★☆ (Intermediate)

## What You'll Learn

- How to identify OWASP Top 10 vulnerabilities
- Security code review using Claude
- Vulnerability severity assessment (Critical/High/Medium/Low)
- Vulnerability remediation and verification
- Slopsquatting detection (fake/similar package name attacks)

## Key Concepts

### OWASP Top 10 (2021)

| # | Vulnerability | Example in This Practice |
|---|--------------|--------------------------|
| A01 | Broken Access Control | Admin endpoint without authentication |
| A02 | Cryptographic Failures | Hardcoded secret keys |
| A03 | Injection | SQL injection (string templates) |
| A04 | Insecure Design | IDOR (Insecure Direct Object Reference) |
| A05 | Security Misconfiguration | CORS allow all |
| A06 | Vulnerable Components | Fake packages (slopsquatting) |
| A07 | Auth Failures | Plaintext password storage |
| A08 | Data Integrity Failures | No input validation |
| A09 | Logging Failures | Logging sensitive information |
| A10 | SSRF | URL requests without validation |

### What Is Slopsquatting?

Slopsquatting is an attack that exploits AI hallucinating non-existent package names by registering malicious packages under those names.

```
Claude: "Install flask-rate-limiter-v2"  ← Non-existent package!
Attacker: Registers malicious package on PyPI as flask-rate-limiter-v2
Developer: pip install flask-rate-limiter-v2  ← Malicious code executed!
```

## Setup

```bash
uv sync
```

## Getting Started

1. Open `CHALLENGE.md` and follow the step-by-step exercises
2. `src/vulnerable_app.py` contains intentionally vulnerable code
3. Find vulnerabilities, fix them, and verify with tests
