# Practice 26: Writer/Reviewer Pattern

## Goal
Build a writer+reviewer collaboration pipeline where one agent implements features and another reviews them, iterating until the code meets quality standards.

## Prerequisites
- Practice 25 (Custom Subagent Design)

## Time
90-120 minutes

## Difficulty
★★★

## What You'll Learn
- The Writer/Reviewer pattern for iterative code quality
- Setting up complementary agent roles (creator vs. critic)
- Building feedback loops between agents
- Adding a verification agent as a final quality gate
- Implementing the full pipeline with Agent SDK (Python)

## Project Structure
```
practices/26-writer-reviewer/
├── README.md
├── CHALLENGE.md
├── src/
│   ├── agents/
│   │   ├── writer.md
│   │   ├── reviewer.md
│   │   └── verifier.md
│   ├── python/
│   │   └── writer_reviewer_pipeline.py
│   └── project/
│       └── src/
│           ├── auth.py
│           ├── test_auth.py
│           └── auth_types.py
```

## Key Concepts

### The Writer/Reviewer Pattern
This pattern mimics human code review workflows:

```
Writer implements → Reviewer reviews → Writer fixes → Reviewer re-reviews → ...
```

The loop continues until the reviewer approves or a maximum iteration count is reached.

### Why This Works
- **Writer** focuses on implementation without self-doubt
- **Reviewer** focuses on quality without implementation pressure
- **Separation of concerns** prevents bias
- **Iteration** drives incremental improvement

### Agent Roles
| Agent | Role | Tools | Model |
|-------|------|-------|-------|
| Writer | Implement features, fix issues | All tools | sonnet |
| Reviewer | Review code, find issues | Read-only | opus |
| Verifier | Run tests, check coverage | Bash (tests only) | haiku |

### Pipeline Flow
```
1. Writer: Implement the feature
2. Reviewer: Review the implementation → APPROVED or CHANGES_REQUESTED
3. If CHANGES_REQUESTED:
   a. Writer: Fix the issues from review feedback
   b. Reviewer: Re-review
   c. Repeat (max 3 iterations)
4. Verifier: Run tests as final gate
5. Done: Feature complete
```
