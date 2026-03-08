# Skill: Testing Patterns

## Description
This skill defines how to write tests in this project. Load this skill before writing any test code.

## Framework
- **Jest** with **ts-jest** for TypeScript support
- Test files live next to source files: `module.ts` → `module.test.ts`

## Test Structure

```typescript
import { functionUnderTest } from "./module";

describe("ModuleName", () => {
  // Group by function or behavior
  describe("functionName", () => {
    // Happy path tests first
    it("should do X when given valid input", () => {
      const result = functionUnderTest("valid");
      expect(result).toBe(expected);
    });

    // Error cases
    it("should throw when given empty string", () => {
      expect(() => functionUnderTest("")).toThrow("descriptive message");
    });

    // Edge cases
    it("should handle edge case: very long input", () => {
      const longInput = "a".repeat(10000);
      const result = functionUnderTest(longInput);
      expect(result).toBeDefined();
    });
  });
});
```

## What to Test

### Always Test
1. **Happy path**: Normal, expected usage
2. **Error cases**: Invalid input, missing data, network failures
3. **Edge cases**: Empty strings, zero, null/undefined, very large inputs
4. **Boundary conditions**: Off-by-one, max values, min values

### Test Categories per Function
- At least 1 happy path test
- At least 1 error/throw test
- At least 1 edge case test
- Total: minimum 3 tests per public function

## Assertions
```typescript
// Equality
expect(value).toBe(expected);           // strict equality
expect(value).toEqual(expected);        // deep equality

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeDefined();
expect(value).toBeUndefined();

// Numbers
expect(value).toBeGreaterThan(3);
expect(value).toBeLessThanOrEqual(10);

// Strings
expect(value).toMatch(/regex/);
expect(value).toContain("substring");

// Arrays
expect(array).toHaveLength(3);
expect(array).toContain(item);

// Errors
expect(() => fn()).toThrow();
expect(() => fn()).toThrow("message");
expect(() => fn()).toThrow(ErrorType);
```

## Setup and Teardown
```typescript
describe("ModuleName", () => {
  let instance: MyClass;

  beforeEach(() => {
    instance = new MyClass();
  });

  afterEach(() => {
    instance.cleanup();
  });
});
```

## Avoid
- Tests that depend on execution order
- Tests that depend on external state (network, filesystem)
- Tests that only check `toBeDefined()` (test actual behavior)
- Flaky tests with timeouts or race conditions
- Testing implementation details (private methods)
