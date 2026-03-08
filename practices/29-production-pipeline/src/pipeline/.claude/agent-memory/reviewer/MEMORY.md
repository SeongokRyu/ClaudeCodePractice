# Reviewer Memory

This file accumulates patterns learned across review sessions. The reviewer agent loads this before each review and updates it after.

## Patterns Learned

### Code Quality Patterns
- Functions should be < 30 lines
- All public APIs need JSDoc comments
- Error messages should be descriptive and include the failing value
- Prefer early returns for guard clauses

### Common Issues
- Missing input validation on user-facing functions
- Inconsistent error handling (some functions throw, others return null)
- Tests that only check happy path (missing error and edge case tests)
- Using `any` type instead of proper TypeScript types

### Project-Specific Conventions
- Use named exports (not default exports)
- Test files live next to source files (e.g., `app.ts` / `app.test.ts`)
- Use `interface` for object shapes, `type` for unions and intersections
- Constants are UPPER_SNAKE_CASE
- Error messages follow pattern: `${entity} not found: ${id}`

### Testing Patterns
- Minimum 3 tests per public function (happy, error, edge)
- Use `describe` blocks grouped by function name
- `beforeEach` for fresh state in each test
- Assert specific error messages, not just that errors are thrown

---

## Review History

_New entries will be appended below by the reviewer agent after each session._
