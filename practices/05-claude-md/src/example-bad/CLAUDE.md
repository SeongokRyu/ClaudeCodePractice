# Project Guidelines

## General Coding Standards

- Write clean, readable code
- Use descriptive variable names that clearly indicate purpose
- Keep functions small and focused on a single responsibility
- Follow the DRY principle (Don't Repeat Yourself)
- Write meaningful comments that explain "why", not "what"
- Handle errors gracefully and provide useful error messages
- Use consistent indentation (2 spaces for JavaScript/TypeScript)
- Always use semicolons at the end of statements
- Prefer const over let, never use var
- Use async/await instead of callbacks or raw promises

## TypeScript Guidelines

- Always define types for function parameters and return values
- Use interfaces for object shapes
- Prefer type unions over enums when possible
- Use generics when a function works with multiple types
- Enable strict mode in tsconfig.json
- Never use `any` type — use `unknown` if the type is truly unknown

## Project Structure

This is a Node.js project using TypeScript with Express for the API server.
We use PostgreSQL for the database with Prisma as the ORM.
The frontend is built with React and uses Tailwind CSS for styling.

### Directory Layout
- src/ — Source code
- src/routes/ — Express route handlers
- src/models/ — Prisma model definitions
- src/services/ — Business logic layer
- src/utils/ — Utility functions
- src/middleware/ — Express middleware
- tests/ — Test files
- config/ — Configuration files

## API Documentation

### Authentication Endpoints

POST /api/auth/login
- Body: { email: string, password: string }
- Response: { token: string, user: User }
- Error codes: 401 (invalid credentials), 422 (validation error)

POST /api/auth/register
- Body: { email: string, password: string, name: string }
- Response: { token: string, user: User }
- Error codes: 409 (email exists), 422 (validation error)

POST /api/auth/refresh
- Headers: Authorization: Bearer <refresh_token>
- Response: { token: string }

### User Endpoints

GET /api/users/:id
- Headers: Authorization: Bearer <token>
- Response: { user: User }

PUT /api/users/:id
- Headers: Authorization: Bearer <token>
- Body: { name?: string, email?: string }
- Response: { user: User }

## Database Schema

The User table has the following columns:
- id: UUID (primary key)
- email: string (unique)
- password: string (hashed with bcrypt)
- name: string
- createdAt: DateTime
- updatedAt: DateTime

## Testing

- Write tests for all new features
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies
- Aim for high code coverage

## Git Practices

- Write clear commit messages
- Keep commits small and focused
- Use feature branches
- Review code before merging

## Security

- Never store passwords in plain text
- Validate all user input
- Use parameterized queries to prevent SQL injection
- Set appropriate CORS headers
- Use HTTPS in production
