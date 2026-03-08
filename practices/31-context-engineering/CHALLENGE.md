# Challenge: Context Engineering

## Step 1: Audit Current Context Usage

Measure the tokens consumed in a typical Claude Code session.

Tasks:
1. Start a new Claude Code session for a simple task (e.g., "add a utility function")
2. Note the total tokens used (visible in the session summary)
3. Break down the sources:
   - System prompt (fixed cost)
   - CLAUDE.md content
   - File reads (how many files, how many tokens each)
   - Conversation history (user messages + assistant responses)
4. Identify the largest token consumers

Questions to answer:
- What percentage of tokens are "useful" vs "noise"?
- Which file reads were necessary vs speculative?
- Could any context have been deferred to later in the session?

## Step 2: Optimize CLAUDE.md

Compare the verbose CLAUDE.md (`src/context-audit/verbose-claude.md`, 150+ lines) with the optimized version (`src/context-audit/optimized-claude.md`, ~40 lines).

Both encode the same rules. The optimized version:
- Uses bullet points instead of paragraphs
- Removes obvious advice (things Claude already knows)
- Groups related rules together
- Uses terse, imperative language
- Omits justifications (the "why" behind each rule)

Test:
1. Use the verbose version as CLAUDE.md, do a task, note token usage and quality
2. Use the optimized version, do the same task, compare
3. Document: Did quality change? Did token usage change? By how much?

## Step 3: Path-Scoped Rules

Create rules that load only when Claude accesses specific file paths.

Setup:
1. Create `.claude/rules/` directory
2. Add `frontend.md` — rules for React/CSS files (only loads when working on `src/components/` or `*.tsx`)
3. Add `backend.md` — rules for API/database files (only loads when working on `src/api/` or `*.controller.ts`)
4. Add `testing.md` — rules for test files (only loads when working on `*.test.ts` or `*.spec.ts`)

Verify:
- Work on a frontend file: only frontend rules should load
- Work on a backend file: only backend rules should load
- Work on a test file: only testing rules should load
- Token savings should be measurable

## Step 4: Progressive Disclosure with @import

Use `@import` in CLAUDE.md to load detailed documentation only when needed.

Setup:
1. In CLAUDE.md, add import references:
   ```
   For API details, see @import docs/api-reference.md
   For architecture overview, see @import docs/architecture.md
   ```
2. These files are only loaded into context when Claude determines they are relevant

Test:
- Ask Claude to "fix the login endpoint" — should load api-reference.md
- Ask Claude to "add a CSS class" — should NOT load api-reference.md
- Compare token usage between tasks that need vs don't need the imported docs

## Step 5: Design a Context Budget

Create a context budget that allocates tokens across categories.

Template (fill in `src/context-budget.md`):

| Category | Token Budget | Priority | Notes |
|----------|-------------|----------|-------|
| System prompt | ~1,500 | Fixed | Cannot change |
| CLAUDE.md | 500-800 | High | Core rules only |
| Path-scoped rules | 200-400 each | Medium | Loaded conditionally |
| Imported docs | 1,000-2,000 each | Low | Only when needed |
| File reads | 2,000-5,000 | Variable | Read only what's needed |
| Conversation | Remaining | Variable | Grows with session |

Guidelines:
- Total context window: ~200k tokens
- Effective working memory: first ~40k tokens have the most impact
- Front-load the most important information
- Defer everything that can be deferred

## Step 6: Compare Results

Run the same task three times with different context configurations:

1. **Unoptimized**: verbose CLAUDE.md, no path-scoping, no imports
2. **Partially optimized**: concise CLAUDE.md, no path-scoping, no imports
3. **Fully optimized**: concise CLAUDE.md, path-scoped rules, progressive imports

For each run, measure:
- Total tokens consumed
- Time to completion
- Quality of output (does it follow all the rules?)
- Number of file reads

Document your findings in a comparison table.

## Success Criteria

- [ ] Token audit completed for a baseline session
- [ ] Verbose vs optimized CLAUDE.md compared with measurable results
- [ ] Path-scoped rules working (verified by checking which rules load)
- [ ] @import progressive disclosure tested
- [ ] Context budget template filled out with real numbers
- [ ] Three-way comparison completed with documented results
