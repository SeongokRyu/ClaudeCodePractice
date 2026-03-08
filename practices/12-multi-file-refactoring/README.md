# Practice 12: Multi-File Refactoring

## Objective

Perform large-scale refactoring across multiple files together with Claude. Learn dependency tracking, safe refactoring strategies, and the "one at a time" approach.

## Difficulty

:star::star::star:

## Prerequisites

- Practice 05 (CLAUDE.md) completed
- Basic understanding of callback patterns and async/await

## Estimated Time

45-60 minutes

## Key Concepts

### Risks of Multi-File Refactoring

- Changes in one file can cascade to other files
- Without understanding the dependency graph, things break in unexpected places
- Refactoring without tests means missing regressions

### Safe Refactoring Strategy

1. **Identify Dependencies**: First, determine which files depend on which
2. **Make a Plan**: Decide the refactoring order (starting from the lowest dependencies)
3. **One File at a Time**: Change only one file at a time
4. **Test Every Time**: Run tests after each change
5. **Prepare for Rollback**: Be ready to revert immediately if issues arise

### Goal of This Exercise

Refactor a codebase written with the callback pattern into an **async/await** pattern. All tests must pass both before and after refactoring.

## Getting Started

```bash
cd practices/12-multi-file-refactoring
uv sync
uv run pytest src/  # Confirm all tests pass
```

Codebase structure:
```
src/
  types.py               # Shared type definitions
  database.py            # Database module (callback pattern)
  user_repository.py     # User repository (callback pattern)
  order_repository.py    # Order repository (callback pattern)
  notification_service.py  # Notification service (callback pattern)
  app.py                 # Main app (callback chain)
```

All modules use the callback pattern, and the goal is to convert them to async/await.

Now follow the steps in `CHALLENGE.md` to practice.

## Learning Points

- Asking Claude to draw a dependency graph helps identify the refactoring order
- The "one file at a time, run tests" pattern is the key to safe refactoring
- Claude can modify multiple files at once, but doing it step by step is safer
- Callback to async/await conversion is a pattern you frequently encounter in practice
