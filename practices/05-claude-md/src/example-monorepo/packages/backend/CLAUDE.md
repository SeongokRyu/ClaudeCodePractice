# CLAUDE.md — Backend Package

## Commands
- Dev: `pnpm dev` (port 3001)
- Build: `pnpm build`
- Test: `pnpm test`
- Test single: `pnpm test -- --grep "test name"`
- DB migrate: `pnpm prisma:migrate`
- DB seed: `pnpm prisma:seed`

## Conventions
- Route files in `src/routes/` — each file exports a Fastify plugin
- Services in `src/services/` — business logic, throw `AppError` on failure
- Repositories in `src/repositories/` — data access layer, no business logic
- Middleware in `src/middleware/` — auth, validation, error handling
- Use Zod schemas for request validation (in `src/schemas/`)

## Gotchas
- This uses Fastify, not Express — do not use Express middleware patterns
- Prisma Client is a singleton in `src/lib/prisma.ts` — always import from there
- Test database is separate: `DATABASE_URL_TEST` in `.env.test`
- After changing Prisma schema, run `pnpm prisma:generate` before `pnpm prisma:migrate`
- Logger is `request.log` inside route handlers, `fastify.log` elsewhere
