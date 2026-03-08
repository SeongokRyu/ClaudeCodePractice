# CLAUDE.md — Frontend Package

## Commands
- Dev: `pnpm dev` (port 3000, proxies API to localhost:3001)
- Build: `pnpm build`
- Test: `pnpm test`
- Test watch: `pnpm test:watch`
- Storybook: `pnpm storybook`

## Conventions
- Components in `src/components/` — one component per directory with index.ts barrel
- Pages in `src/pages/` — file-based routing (Next.js convention)
- Hooks in `src/hooks/` — prefix with `use` (e.g., `useAuth.ts`)
- API calls only through `src/api/` client — never use fetch directly
- Styling: Tailwind CSS only, no CSS modules or styled-components
- State: Zustand for global state, React Query for server state

## Gotchas
- Images must go in `public/images/`, not `src/assets/`
- Environment variables must be prefixed with `NEXT_PUBLIC_` to be available in browser
- The `src/api/client.ts` automatically handles token refresh — do not add auth headers manually
