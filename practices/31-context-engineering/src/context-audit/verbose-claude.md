# Project Guidelines

## About This Project

This is a web application built with React on the frontend and Node.js/Express on the backend. We use TypeScript throughout the entire codebase for type safety. The project was started in 2024 and has been growing steadily.

## Code Style and Formatting

We follow a strict code style to keep the codebase consistent and readable for all team members. Here are our guidelines:

### TypeScript

When writing TypeScript code, please make sure to always use explicit return types on all functions. This is important because it helps with documentation and catches errors early. For example, instead of writing `function add(a: number, b: number)`, you should write `function add(a: number, b: number): number`.

We prefer using `interface` over `type` for object shapes because interfaces are more extensible and can be merged. However, for union types or more complex type operations, `type` is acceptable.

Please avoid using the `any` type whenever possible. If you absolutely must use it, add a comment explaining why. The `unknown` type is almost always a better choice than `any` because it forces you to narrow the type before using it.

We use `const` for all variable declarations by default, and only use `let` when you know the variable will be reassigned. Never use `var`.

### React

For React components, we always use functional components with hooks. Class components should not be used in new code.

Component files should be named with PascalCase (e.g., `UserProfile.tsx`). Each component should be in its own file, and the file name should match the component name.

We use CSS Modules for styling. Each component should have a corresponding `.module.css` file. Avoid inline styles except for truly dynamic values.

Props should always be defined with a TypeScript interface. The interface should be named `ComponentNameProps` (e.g., `UserProfileProps`).

### Naming Conventions

Variables and functions should use camelCase. Types and interfaces should use PascalCase. Constants that represent truly fixed values should use UPPER_SNAKE_CASE.

File names for React components use PascalCase. All other files use kebab-case.

## Testing

We use Jest as our testing framework along with React Testing Library for component tests.

Every new feature should have corresponding tests. We aim for at least 80% code coverage, but coverage alone is not the goal — meaningful tests are more important than high coverage numbers.

Test files should be co-located with the files they test, using the `.test.ts` or `.test.tsx` suffix.

When writing tests, please use descriptive test names that explain what behavior is being tested. For example, instead of `test('works')`, write `test('should return the sum of two positive numbers')`.

We prefer `describe` blocks to group related tests, and `it` or `test` for individual test cases.

Mock external dependencies (API calls, database connections) but try to avoid mocking internal modules. Integration tests should test the real implementation whenever possible.

## API Development

Our API follows RESTful conventions. Endpoints should use plural nouns (e.g., `/api/users`, not `/api/user`).

All API responses should follow a consistent format:
```json
{
  "success": true,
  "data": {},
  "error": null
}
```

Error responses should include an appropriate HTTP status code and a human-readable message.

We use Zod for request validation. Every endpoint should validate its input before processing.

## Database

We use PostgreSQL as our primary database. All database access goes through Prisma ORM.

Never write raw SQL unless there is a compelling performance reason, and always document why raw SQL was used.

Database migrations should be created using Prisma's migration system. Never modify a migration file after it has been applied.

## Git Workflow

We use conventional commits. Every commit message should start with a type prefix:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `refactor:` for code refactoring
- `test:` for test additions or changes
- `chore:` for maintenance tasks

Always create a feature branch from `main`. Branch names should follow the pattern `type/description` (e.g., `feat/user-authentication`).

## Error Handling

Always use try-catch blocks for async operations. Never let errors silently fail.

Use custom error classes for domain-specific errors. Each error should have a clear error code and message.

Log errors with sufficient context (what was being attempted, what input was provided, etc.) but never log sensitive information like passwords or tokens.

## Security

Never commit secrets or credentials to the repository. Use environment variables for all sensitive configuration.

All user input should be validated and sanitized before processing. This includes query parameters, request bodies, and URL parameters.

We use bcrypt for password hashing and JWT for authentication tokens.

## Performance

Keep components small and focused. If a component is doing too many things, break it down into smaller components.

Use React.memo for components that render frequently with the same props. Use useMemo and useCallback appropriately, but don't over-optimize — premature optimization is the root of all evil.

For API endpoints, always consider pagination for list endpoints that could return many results.
