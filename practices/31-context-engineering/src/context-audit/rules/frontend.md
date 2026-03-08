# Frontend Rules (Path-scoped)

Applies to: `src/components/**`, `*.tsx`, `*.css`

## Component Structure
- One component per file, filename = component name
- Props interface above component: `interface ComponentNameProps {}`
- Export as named export, not default
- Order: imports > types > component > styles

## Hooks
- Custom hooks in `src/hooks/`, prefixed with `use`
- Keep hooks focused: one concern per hook
- Always include cleanup in useEffect

## Styling
- CSS Modules: `import styles from './Component.module.css'`
- No inline styles except dynamic values
- Use design tokens from `src/styles/tokens.css`
- Mobile-first responsive design

## State Management
- Local state: useState/useReducer
- Server state: React Query (TanStack Query)
- Global state: Context API (no Redux unless justified)

## Accessibility
- All interactive elements must be keyboard-accessible
- Use semantic HTML elements
- Include aria-labels for icon-only buttons
- Test with screen reader
