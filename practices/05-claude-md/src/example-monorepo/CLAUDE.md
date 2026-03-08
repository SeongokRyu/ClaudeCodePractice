# CLAUDE.md — Monorepo Root

## Monorepo Structure
This is a pnpm workspace monorepo. All packages are in `packages/`.

## Commands (root level)
- Install all: `pnpm install`
- Build all: `pnpm -r build`
- Test all: `pnpm -r test`
- Lint all: `pnpm -r lint`
- Run specific package: `pnpm --filter @app/frontend dev`

## Conventions
- Shared types in `packages/shared-types/` — import as `@app/shared-types`
- Each package has its own CLAUDE.md with package-specific rules
- Inter-package imports use workspace protocol: `"@app/shared-types": "workspace:*"`
- All packages use the same TypeScript version (pinned in root package.json)

## Git
- Branch: `feat/JIRA-123-short-description`
- Commit: `feat(package-name): message` — scope must be the package name
- PR must pass `pnpm -r test` before merge

## Do Not
- Do not install dependencies in the root — install in the specific package
- Do not import between packages without going through the package's public API (index.ts)
