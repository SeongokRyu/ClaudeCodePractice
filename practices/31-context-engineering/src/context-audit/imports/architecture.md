# Architecture Overview

This document is loaded via @import when Claude works on architectural tasks.

## System Architecture

```
Client (React SPA)
    |
    v
API Gateway (Express)
    |
    +-- Auth Middleware (JWT validation)
    |
    +-- Controllers (HTTP layer)
    |       |
    |       v
    +-- Services (Business logic)
    |       |
    |       v
    +-- Repositories (Data access)
            |
            v
      PostgreSQL (via Prisma ORM)
```

## Directory Structure

```
src/
  api/
    controllers/        # Express route handlers
    services/           # Business logic
    repositories/       # Prisma data access
    middleware/          # Auth, validation, error handling
    routes/             # Route definitions
    validators/         # Zod schemas
  components/           # React components
    common/             # Shared components (Button, Input, Modal)
    features/           # Feature-specific components
    layouts/            # Layout components (Header, Sidebar, Footer)
  hooks/                # Custom React hooks
  lib/                  # Shared utilities
    prisma.ts           # Prisma client singleton
    logger.ts           # Structured logger
    errors.ts           # Custom error classes
  styles/               # Global styles and tokens
  types/                # Shared TypeScript types
```

## Data Flow

1. **Request arrives** at Express router
2. **Middleware** validates auth token, parses body
3. **Controller** extracts params, calls service
4. **Service** applies business rules, calls repository
5. **Repository** executes Prisma query
6. **Response** flows back through controller with consistent format

## Key Design Decisions

### Why layered architecture?
- Separation of concerns makes testing easier
- Services can be reused across controllers
- Database layer can be swapped without touching business logic

### Why Prisma?
- Type-safe database access
- Auto-generated migrations
- Great developer experience with autocomplete

### Why Zod over class-validator?
- Works with plain objects (no class instantiation)
- Composable schemas
- TypeScript type inference from schemas

### Why CSS Modules over styled-components?
- Zero runtime cost
- Standard CSS syntax (no learning curve)
- Easy to migrate to/from plain CSS

## Deployment

```
GitHub Push
    |
    v
GitHub Actions CI
    |
    +-- Lint + Type Check
    +-- Run Tests
    +-- Build Docker Image
    |
    v
Docker Registry
    |
    v
Kubernetes (Production)
    +-- API Pod (3 replicas)
    +-- Worker Pod (2 replicas)
    +-- PostgreSQL (managed)
    +-- Redis (managed, for caching)
```

## Environment Configuration

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| JWT_SECRET | Secret for signing JWTs | Yes |
| JWT_EXPIRY | Token expiry (default: 15m) | No |
| REDIS_URL | Redis connection string | No |
| PORT | API server port (default: 3000) | No |
| NODE_ENV | Environment (development/production) | Yes |
