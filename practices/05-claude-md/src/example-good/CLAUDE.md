# CLAUDE.md

## Commands
- Build: `npm run build`
- Test all: `npm test`
- Test single: `npm test -- --grep "test name"`
- Lint: `npm run lint -- --fix`
- Dev server: `npm run dev` (port 3001, not 3000)
- DB migrate: `npx prisma migrate dev`

## Conventions
- File naming: kebab-case for files, PascalCase for React components
- Route handlers return `ApiResponse<T>` wrapper, never raw objects
- Services throw `AppError(code, message)`, middleware catches them
- All dates stored as UTC, converted to user timezone in frontend only
- Feature flags in `src/config/features.ts`, never hardcoded booleans

## Git
- Branch: `feat/JIRA-123-short-description`
- Commit: `feat(scope): message` (conventional commits)
- Always run `npm test` before committing

## Gotchas
- Prisma Client must be regenerated after schema changes: `npx prisma generate`
- The `user.email` field has a unique constraint — tests need unique emails (use `faker.internet.email()`)
- Port 3000 is used by the frontend dev server, backend uses 3001
- `npm test` runs in-band by default (no --parallel) due to shared test DB
- Never import from `@prisma/client` directly — use `src/lib/prisma.ts` singleton

## Do Not
- Do not create migration files manually — use `npx prisma migrate dev`
- Do not add `console.log` — use the `logger` from `src/lib/logger.ts`
- Do not modify `src/generated/` — these files are auto-generated
