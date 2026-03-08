# Practice 09: TDD Workflow

## Objective

Practice Test-Driven Development (TDD) together with Claude. Learn the Red-Green-Refactor cycle and the Ralph Loop pattern, and internalize a TDD workflow in collaboration with AI.

## Prerequisites

- Practice 05 (CLAUDE.md) completed
- Basic understanding of Python and pytest

## Estimated Time

45-60 minutes

## Key Concepts

### TDD Cycle: Red → Green → Refactor

1. **Red**: Write a failing test first
2. **Green**: Write the minimum code to pass the test
3. **Refactor**: Improve code quality while keeping tests passing

### Ralph Loop

A pattern where you give Claude success criteria and let it iterate:

```
"Run the tests, fix any failures, and run them again. Repeat until all tests pass."
```

This pattern lets Claude drive its own feedback loop to solve the problem.

## Getting Started

```bash
cd practices/09-tdd-workflow
uv sync
```

There are pre-written tests in `src/test_shopping_cart.py`. The implementation file (`src/shopping_cart.py`) only defines the interface, so all tests will **fail**.

```bash
uv run pytest src/  # Confirm that all tests fail
```

Now follow the steps in `CHALLENGE.md` to practice TDD with Claude.

## Learning Points

- Writing tests first makes the requirements clear
- Telling Claude "make the tests pass" performs the Green phase of TDD
- In the Refactor phase, Claude can refactor freely thanks to the safety net of tests
- The Ralph Loop is a powerful pattern that lets Claude solve problems autonomously
