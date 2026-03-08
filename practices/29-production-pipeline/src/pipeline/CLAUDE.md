# Project: Production Multi-Agent Pipeline

This project demonstrates a production-ready multi-agent pipeline using Claude Code's Command → Agent → Skill architecture.

## Architecture
- **Commands**: `/build-feature` orchestrates the full pipeline
- **Agents**: researcher, implementer, reviewer (with memory), tester
- **Skills**: coding-conventions, testing-patterns, security-review

## Code Conventions
- TypeScript with strict mode
- No `any` types
- JSDoc comments on all public APIs
- Error handling with descriptive messages
- Functions under 30 lines

## Testing
- Test files: `*.test.ts` next to source files
- Framework: Jest with ts-jest
- Pattern: describe/it blocks
- Coverage target: 80%+

## File Structure
```
src/
├── app.ts          — Main application module
├── app.test.ts     — Tests for app module
└── [new-module].ts — New modules added by the pipeline
```
