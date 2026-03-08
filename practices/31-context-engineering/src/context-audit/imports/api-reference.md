# API Reference

This document is loaded via @import when Claude works on API-related tasks.

## Endpoints

### Authentication

#### POST /api/auth/login
Request: `{ email: string, password: string }`
Response: `{ success: true, data: { token: string, refreshToken: string, user: User } }`
Errors: 401 (invalid credentials), 422 (validation error)

#### POST /api/auth/register
Request: `{ email: string, password: string, name: string }`
Response: `{ success: true, data: { user: User } }`
Errors: 409 (email exists), 422 (validation error)

#### POST /api/auth/refresh
Request: `{ refreshToken: string }`
Response: `{ success: true, data: { token: string } }`
Errors: 401 (invalid/expired refresh token)

### Users

#### GET /api/users
Query: `?page=1&limit=20&search=query`
Response: `{ success: true, data: { users: User[], total: number, page: number } }`
Auth: Required (admin only)

#### GET /api/users/:id
Response: `{ success: true, data: { user: User } }`
Auth: Required (self or admin)

#### PATCH /api/users/:id
Request: `{ name?: string, email?: string }`
Response: `{ success: true, data: { user: User } }`
Auth: Required (self or admin)

### Posts

#### GET /api/posts
Query: `?page=1&limit=20&authorId=uuid&status=published`
Response: `{ success: true, data: { posts: Post[], total: number, page: number } }`
Auth: Optional (unpublished posts require auth)

#### POST /api/posts
Request: `{ title: string, content: string, status: 'draft' | 'published' }`
Response: `{ success: true, data: { post: Post } }`
Auth: Required

#### PATCH /api/posts/:id
Request: `{ title?: string, content?: string, status?: 'draft' | 'published' }`
Response: `{ success: true, data: { post: Post } }`
Auth: Required (author or admin)

#### DELETE /api/posts/:id
Response: `{ success: true, data: null }`
Auth: Required (author or admin)

## Data Models

### User
```typescript
interface User {
  id: string;          // UUID
  email: string;
  name: string;
  role: 'user' | 'admin';
  createdAt: string;   // ISO 8601
  updatedAt: string;   // ISO 8601
}
```

### Post
```typescript
interface Post {
  id: string;          // UUID
  title: string;
  content: string;
  status: 'draft' | 'published';
  authorId: string;    // UUID, references User
  createdAt: string;   // ISO 8601
  updatedAt: string;   // ISO 8601
}
```

## Validation Schemas (Zod)

```typescript
const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  status: z.enum(['draft', 'published']).default('draft'),
});
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTH_REQUIRED | 401 | Missing or invalid token |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 422 | Request body validation failed |
| CONFLICT | 409 | Resource already exists |
| INTERNAL_ERROR | 500 | Unexpected server error |
