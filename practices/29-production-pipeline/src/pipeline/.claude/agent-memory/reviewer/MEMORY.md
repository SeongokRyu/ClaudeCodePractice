# Reviewer Memory

This file accumulates patterns learned across review sessions. The reviewer agent loads this before each review and updates it after.

## Patterns Learned

### Code Quality Patterns
- Functions should be < 30 lines
- All public APIs need docstrings
- Error messages should be descriptive and include the failing value
- Prefer early returns for guard clauses

### Common Issues
- Missing input validation on user-facing functions
- Inconsistent error handling (some functions raise, others return None)
- Tests that only check happy path (missing error and edge case tests)
- Missing type hints on function parameters and return types

### Project-Specific Conventions
- Use explicit imports (not wildcard imports)
- Test files live next to source files (e.g., `app.py` / `test_app.py`)
- Use `dataclasses` for structured data
- Constants are UPPER_SNAKE_CASE
- Error messages follow pattern: `{entity} not found: {id}`

### Testing Patterns
- Minimum 3 tests per public function (happy, error, edge)
- Use pytest classes grouped by function name
- Use `@pytest.fixture` for fresh state in each test
- Assert specific error messages with `pytest.raises(match=...)`

---

## Review History

_New entries will be appended below by the reviewer agent after each session._
