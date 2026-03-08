# Competing Hypotheses Prompt

Debug the slow dashboard issue using three competing hypotheses.

## Problem Statement
The dashboard loads slowly (3-5 seconds) and sometimes shows stale data. Users report that refreshing the page sometimes fixes it, sometimes doesn't.

## Teammates — Each Investigates One Hypothesis

### Hypothesis A: Frontend Rendering Issue
**Investigator focus:** React component performance

Look for:
- Unnecessary re-renders (missing React.memo, useMemo, useCallback)
- useEffect with wrong dependency arrays causing infinite loops
- Large component trees rendering on every state change
- Missing keys in list rendering
- Large bundles or unoptimized imports

Evidence to gather:
- Component render counts
- Bundle size analysis
- useEffect dependency chains
- State update patterns

### Hypothesis B: Backend API Performance Issue
**Investigator focus:** Server-side performance

Look for:
- Slow database queries (N+1 problem, missing indexes)
- No pagination on large datasets
- Synchronous operations that should be async
- Missing caching headers
- Unoptimized data serialization

Evidence to gather:
- Query execution plans
- Response payload sizes
- Endpoint response times
- Database index usage

### Hypothesis C: Caching/State Management Issue
**Investigator focus:** Data freshness and consistency

Look for:
- Stale cache entries not being invalidated
- Race conditions between concurrent requests
- Optimistic updates that fail silently
- Browser cache vs. API cache conflicts
- WebSocket/polling timing issues

Evidence to gather:
- Cache invalidation logic
- Concurrent request handling
- State mutation patterns
- Cache-Control headers

## Reporting Format
Each teammate should report:
1. **Confidence:** low / medium / high that this hypothesis explains the issue
2. **Evidence found:** Specific findings with file:line references
3. **Evidence against:** Why this might NOT be the cause
4. **Suggested fix:** If confirmed, how to fix it
5. **Estimated impact:** How much improvement the fix would provide
