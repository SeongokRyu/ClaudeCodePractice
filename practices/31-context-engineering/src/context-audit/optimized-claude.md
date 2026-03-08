# Project Rules

## Stack
React + Node.js/Express, TypeScript throughout, PostgreSQL + Prisma, Jest + RTL.

## TypeScript
- Explicit return types on all functions
- `interface` for object shapes, `type` for unions
- No `any` — use `unknown` and narrow
- `const` by default, `let` only when reassigned

## React
- Functional components only, no class components
- PascalCase filenames matching component names
- CSS Modules for styling (no inline styles)
- Props interface: `ComponentNameProps`

## Naming
- camelCase: variables/functions
- PascalCase: types/interfaces/components
- UPPER_SNAKE_CASE: constants
- kebab-case: non-component files

## Testing
- Co-located test files: `*.test.ts(x)`
- Descriptive names: `should [behavior] when [condition]`
- Mock external deps only, not internal modules
- Aim for 80% coverage with meaningful tests

## API
- RESTful, plural nouns: `/api/users`
- Response format: `{ success, data, error }`
- Zod validation on all inputs
- Paginate list endpoints

## Database
- Prisma ORM only, no raw SQL without documented reason
- Never modify applied migrations

## Git
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Branch: `type/description` from `main`

## Security
- No secrets in repo — use env vars
- Validate/sanitize all user input
- bcrypt for passwords, JWT for auth

## Error Handling
- try-catch all async operations
- Custom error classes with codes
- Log context, never log secrets
