# Skill: Coding Conventions

## Description
This skill defines the coding conventions for this project. Load this skill before implementing any new code.

## Naming Conventions
- **Variables & functions**: camelCase (`getUserById`, `isValid`)
- **Types & interfaces**: PascalCase (`UserProfile`, `AuthToken`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Files**: kebab-case for multi-word (`user-preferences.ts`)
- **Test files**: Same name + `.test.ts` suffix (`user-preferences.test.ts`)

## File Structure
```typescript
// 1. Imports (external first, then internal)
import { someLib } from "external-lib";
import { localUtil } from "./utils";

// 2. Types and interfaces
export interface MyType {
  field: string;
}

// 3. Constants
const MAX_ITEMS = 100;

// 4. Main exports (functions/classes)
export function myFunction(): void {
  // ...
}

// 5. Helper functions (not exported)
function helperFunction(): void {
  // ...
}
```

## Error Handling
- Always throw `Error` with descriptive messages
- Include the failing value in error messages: `throw new Error(\`User not found: \${id}\`)`
- Validate inputs at function boundaries
- Use early returns for guard clauses

## TypeScript Rules
- **No `any`** — use `unknown` if type is truly unknown
- **Prefer `interface` over `type`** for object shapes
- **Use `readonly`** for properties that shouldn't change
- **Prefer named exports** over default exports

## Comments
- JSDoc on all public (exported) functions
- Inline comments explain "why", not "what"
- No commented-out code

## Function Size
- Target: under 30 lines per function
- If a function is longer, extract helper functions
- Each function should do one thing well
