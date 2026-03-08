# Testing Rules (Path-scoped)

Applies to: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`

## Structure
- Co-locate tests with source: `Component.test.tsx` next to `Component.tsx`
- Use `describe` blocks to group by function/component
- Use `it`/`test` with descriptive names: `should [behavior] when [condition]`

## Unit Tests
- Test one behavior per test case
- Use Arrange-Act-Assert pattern
- Mock external dependencies (API, DB, filesystem)
- Do NOT mock the module under test

## Component Tests (React Testing Library)
- Query by role, label, or text — not by test ID or class name
- Test user interactions, not implementation details
- Use `userEvent` over `fireEvent`
- Assert on visible output, not internal state

## Integration Tests
- Test real service-to-repository interactions
- Use test database with migrations applied
- Clean up data after each test (use transactions)
- Test error paths, not just happy paths

## Mocking
- Use `jest.mock()` at module level
- Use `jest.spyOn()` for partial mocking
- Always restore mocks: `jest.restoreAllMocks()` in `afterEach`
- Prefer dependency injection over module mocking when possible

## Coverage
- Target: 80% line coverage minimum
- Focus on branch coverage for critical logic
- 100% coverage on utility/helper functions
- Skip coverage for type-only files
