# Practice 11: Code Review

## Objective

Learn AI-powered code review patterns. Practice 8 master patterns and learn Trust Level Expansion strategies.

## Prerequisites

- Practice 05 (CLAUDE.md) completed
- Basic understanding of security concepts (optional)

## Estimated Time

45-60 minutes

## Key Concepts

### 8 Code Review Master Patterns

1. **Basic Review**: "Review this code"
2. **Role-Based Review**: "Review as a senior security engineer"
3. **Quantitative Assessment**: Security/Performance/Maintainability scores (1-5)
4. **Self-Review**: Review from a different perspective after writing code
5. **Checklist Review**: Systematic review based on a security checklist
6. **Comparative Review**: Compare two implementations and analyze pros/cons
7. **Incremental Review**: Review each commit of a PR in order
8. **Educational Review**: Review as if explaining to a junior developer

### Trust Level Expansion

Start with small-scope reviews, verify Claude's review quality, and then gradually expand the scope.

## Getting Started

```bash
cd practices/11-code-review
uv sync
```

`src/api_handler.py` contains API handler code with **intentionally embedded issues**. Use various review patterns with Claude to find the problems.

Now follow the steps in `CHALLENGE.md` to practice.

## Learning Points

- Different review perspectives reveal different issues in the same code
- Assigning a role makes Claude analyze more deeply from that expert's perspective
- Quantitative scores are useful for establishing code quality standards within a team
- Self-review is a surprisingly powerful pattern
