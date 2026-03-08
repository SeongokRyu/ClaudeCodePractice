# Backend Rules (Path-scoped)

Applies to: `src/api/**`, `*.controller.ts`, `*.service.ts`, `*.repository.ts`

## Architecture
- Controllers: handle HTTP (parse request, call service, send response)
- Services: business logic (no HTTP concepts)
- Repositories: data access (Prisma calls)
- Never skip layers (controller must not call repository directly)

## API Endpoints
- RESTful conventions, plural nouns
- Consistent response: `{ success: boolean, data: T | null, error: string | null }`
- Always return appropriate HTTP status codes
- Use Zod schemas for request validation

## Error Handling
- Throw domain-specific errors from services
- Controllers catch and map to HTTP responses
- Global error handler as Express middleware
- Log with correlation ID for tracing

## Database
- All queries through Prisma
- Use transactions for multi-step operations
- Always handle connection errors gracefully
- Index frequently queried fields

## Authentication
- JWT tokens in Authorization header
- Middleware: `authenticateToken` before protected routes
- Role-based access: `requireRole('admin')`
- Refresh tokens stored in httpOnly cookies

## Performance
- Paginate all list endpoints (default limit: 20, max: 100)
- Use `select` in Prisma to fetch only needed fields
- Cache frequently accessed, rarely changed data
- Use connection pooling
