# Command: /build-feature

Build a feature using the full multi-agent pipeline.

## Usage
```
/build-feature "Description of the feature to build"
```

## Pipeline

### Phase 1: Research
Spawn the **researcher** agent to analyze the codebase and create an implementation plan.

```
Agent: .claude/agents/researcher.md
Input: Feature description + codebase context
Output: Implementation plan
```

### Phase 2: Implement
Spawn the **implementer** agent with skills preloaded.

```
Agent: .claude/agents/implementer.md
Skills: coding-conventions, testing-patterns
Input: Implementation plan from Phase 1
Output: Code + tests
```

### Phase 3: Review (loop, max 3 iterations)
Spawn the **reviewer** agent with memory.

```
Agent: .claude/agents/reviewer.md
Memory: .claude/agent-memory/reviewer/MEMORY.md
Skill: security-review
Input: Code changes from Phase 2
Output: APPROVED or CHANGES_REQUESTED
```

If CHANGES_REQUESTED:
- Feed reviewer feedback back to implementer
- Re-run review
- Max 3 iterations

### Phase 4: Test
Spawn the **tester** agent.

```
Agent: .claude/agents/tester.md
Input: Project path
Output: PASS or FAIL
```

If FAIL:
- Feed test failures back to implementer
- Re-run tests after fixes

### Phase 5: Finalize
- Update reviewer memory with new patterns
- Report final summary to user

## Error Handling
- If any agent fails to spawn: report error, stop pipeline
- If max review iterations reached without approval: report and stop
- If tests fail after 2 fix attempts: report and stop

## Output
```
## Build Feature: Complete

### Feature: [description]
### Status: SUCCESS | PARTIAL | FAILED

### Pipeline Summary
1. Research: [time] — Plan created
2. Implementation: [time] — X files created, Y files modified
3. Review: [iterations] iterations — [verdict]
4. Testing: [result] — X/Y tests passing

### Files Changed
- [list of files]

### Reviewer Memory Updated
- [new patterns added]
```
