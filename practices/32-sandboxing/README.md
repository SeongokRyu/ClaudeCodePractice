# Practice 32: 샌드박싱과 권한 제어

## Goal

Implement OS-level isolation with sandbox mode, filesystem and network restrictions, and tool whitelisting. Learn to create permission profiles for different use cases -- from trusted development to zero-trust code review.

## Prerequisites

- **Practice 30**: Deterministic Guardrails (hooks and settings.json)

## Time

90-120 minutes

## Difficulty

★★★

## What You Will Learn

1. How to enable and configure Claude Code's sandbox mode
2. How to create permission profiles (allow/deny lists)
3. How to design profiles for different trust levels
4. How to use Docker for additional isolation in CI/CD
5. How to build a zero-trust configuration for reviewing untrusted code

## Key Concepts

- **Sandboxing** restricts what an agent can access at the OS level -- filesystem, network, and system calls.
- **Permission profiles** define which tools and commands are allowed/denied in `settings.json`.
- **Principle of least privilege**: grant only the minimum permissions needed for the task.
- **Trust levels**: different tasks require different permission levels (development vs code review vs CI/CD).
- **Defense in depth**: combine sandbox mode + permission profiles + hooks for layered security.

## Structure

```
src/
  permissions/
    readonly-review.json   # Read-only review permission profile
    trusted-dev.json       # Trusted developer profile
    ci-cd.json             # CI/CD profile (minimal tools)
    zero-trust.json        # Zero trust for untrusted code
    README.md              # Permission profile guide
  docker/
    Dockerfile             # Dockerfile for sandboxed execution
    docker-compose.yml     # Docker compose for isolated environment
```

## Tips

- Start with the most restrictive profile and add permissions as needed
- Test each profile by trying operations that should be blocked
- Docker adds an extra layer of isolation beyond Claude's built-in sandbox
- Always review what tools a profile allows before using it for sensitive work
