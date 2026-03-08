# Challenge: Production Multi-Agent Pipeline

## Step 1: Design the 3-Layer Architecture

Design a production-ready pipeline for a "build feature" workflow.

### Architecture Overview
```
User: /build-feature "Add user preferences module"
  ↓
Command Layer: /build-feature
  Orchestrates the full pipeline
  ↓
Agent Layer:
  1. Researcher → analyzes codebase, creates plan
  2. Implementer → writes code + tests (loads Skills)
  3. Reviewer → reviews implementation (uses Memory)
  4. Tester → runs tests, verifies quality
  ↓
Skill Layer:
  - coding-conventions → code style rules
  - testing-patterns → how to write tests
  - security-review → security checklist
```

### Design Questions to Answer
1. What data flows between layers?
2. How does the command know when to loop vs. finish?
3. How does the implementer load skills?
4. How does the reviewer use memory?
5. What happens when tests fail?

---

## Step 2: Create Skills

Create three reusable Skills that agents can load.

### Coding Conventions Skill
**File:** `src/pipeline/.claude/skills/coding-conventions/SKILL.md`

Content should cover:
- Naming conventions (snake_case for variables/functions, PascalCase for classes)
- File structure patterns
- Error handling approach
- Import ordering
- Docstring style

### Testing Patterns Skill
**File:** `src/pipeline/.claude/skills/testing-patterns/SKILL.md`

Content should cover:
- Test file naming (`test_*.py`)
- Test structure (pytest classes and functions)
- What to test (happy path, errors, edge cases)
- Assertion patterns
- Mock/fixture conventions

### Security Review Skill
**File:** `src/pipeline/.claude/skills/security-review/SKILL.md`

Content should cover:
- Input validation checklist
- Common vulnerability patterns
- Secret handling rules
- Authentication/authorization checks
- Dependency audit process

---

## Step 3: Create Agents

Create four specialized agents with appropriate configurations.

### Researcher Agent
**File:** `src/pipeline/.claude/agents/researcher.md`
- Tools: Read, Glob, Grep (read-only)
- Model: haiku
- Output: Implementation plan

### Implementer Agent
**File:** `src/pipeline/.claude/agents/implementer.md`
- Tools: All
- Model: sonnet
- Skills: coding-conventions, testing-patterns
- Output: Working code + tests

### Reviewer Agent (with memory)
**File:** `src/pipeline/.claude/agents/reviewer.md`
- Tools: Read, Glob, Grep (read-only)
- Model: inherit
- Memory: project (accumulates patterns)
- Output: APPROVED or CHANGES_REQUESTED

### Tester Agent
**File:** `src/pipeline/.claude/agents/tester.md`
- Tools: Bash (tests only), Read, Glob
- Model: haiku
- Output: PASS or FAIL with test results

---

## Step 4: Create the Build-Feature Command

Create the orchestration command that runs the full pipeline.

**File:** `src/pipeline/.claude/commands/build-feature.md`

### Command Behavior
When the user runs `/build-feature "description"`:

1. **Research Phase**
   - Spawn researcher agent
   - Input: feature description + codebase path
   - Output: implementation plan

2. **Implementation Phase**
   - Spawn implementer agent with skills loaded
   - Input: implementation plan
   - Output: code changes + tests

3. **Review Phase** (loop)
   - Spawn reviewer agent with memory
   - Input: code changes
   - Output: APPROVED or CHANGES_REQUESTED
   - If CHANGES_REQUESTED:
     - Re-spawn implementer with feedback
     - Re-review (max 3 iterations)

4. **Testing Phase**
   - Spawn tester agent
   - Input: project path
   - Output: PASS or FAIL
   - If FAIL: back to implementer with test failures

5. **Completion**
   - Update reviewer memory with new patterns learned
   - Report summary to user

---

## Step 5: Add Agent Memory

Set up the reviewer agent's memory system.

### Memory File
**File:** `src/pipeline/.claude/agent-memory/reviewer/MEMORY.md`

Start with seed patterns:
```markdown
# Reviewer Memory

## Patterns Learned

### Code Quality Patterns
- Functions should be < 30 lines
- All public APIs need JSDoc comments
- Error messages should be descriptive

### Common Issues
- Missing input validation on user-facing functions
- Inconsistent error handling (throw vs. return)
- Tests that only check happy path

### Project-Specific Conventions
- Use `Result<T, E>` pattern for operations that can fail
- Prefer named exports over default exports
- Test files live next to source files
```

### How Memory Works
1. Before review: Reviewer loads memory from MEMORY.md
2. During review: Reviewer applies known patterns
3. After review: New patterns are appended to MEMORY.md
4. Over time: Reviewer becomes more effective for this project

### Memory Update Format
After each review, append to MEMORY.md:
```markdown
## Session: [date]
### New Patterns Discovered
- [pattern description]

### Issues Found
- [recurring issue type]
```

---

## Step 6: End-to-End Test

Run the full pipeline on a real feature.

### Test Feature
"Add a user preferences module with:
- getUserPreferences(userId) function
- updatePreference(userId, key, value) function
- resetPreferences(userId) function
- Default preferences support
- Comprehensive tests"

### Expected Pipeline Flow
```
1. /build-feature "Add user preferences module"

2. Researcher analyzes → Plan:
   - Create src/preferences.py
   - Create src/test_preferences.py
   - Follow existing patterns from src/app.py

3. Implementer builds → Code:
   - src/preferences.py (3 functions + types)
   - src/test_preferences.py (10+ test cases)
   - Uses coding-conventions skill

4. Reviewer reviews → CHANGES_REQUESTED:
   - Missing edge case for invalid userId
   - No JSDoc on resetPreferences
   → Reviewer memory updated

5. Implementer fixes → Updated code

6. Reviewer re-reviews → APPROVED

7. Tester verifies → PASS (all tests green)

8. Done!
```

### Verification Checklist
- [ ] Research phase produces useful plan
- [ ] Implementation follows coding conventions skill
- [ ] Reviewer applies patterns from memory
- [ ] Review loop iterates correctly
- [ ] Tester catches real test failures
- [ ] Memory file is updated after review
- [ ] Full pipeline completes successfully

---

## Success Criteria

- [ ] All 3 skills are complete and informative
- [ ] All 4 agents have clear role definitions
- [ ] The /build-feature command orchestrates correctly
- [ ] Reviewer memory persists and accumulates patterns
- [ ] End-to-end pipeline works on a real feature
- [ ] Pipeline handles failures gracefully (test failures, review loops)
- [ ] Python SDK implementation works as an alternative

## Bonus Challenges

1. **Parallel review**: Add security-review agent running in parallel with code review
2. **Cost tracking**: Track and report total token usage across all agents
3. **Pipeline visualization**: Log a visual timeline of the pipeline execution
4. **Feature complexity detection**: Lead agent adjusts pipeline based on feature complexity
5. **Regression testing**: After feature is built, run full project test suite
