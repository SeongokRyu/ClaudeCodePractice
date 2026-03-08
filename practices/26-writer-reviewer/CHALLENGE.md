# Challenge: Writer/Reviewer Pattern

## Step 1: Set Up Writer Agent

Create a Writer agent that implements features with full tool access.

**File:** `src/agents/writer.md`

### Requirements
1. Full tool access: Read, Write, Edit, Bash, Glob, Grep
2. Model: sonnet (balanced implementation quality)
3. Responsibilities:
   - Implement requested features
   - Write tests for new code
   - Follow existing code patterns
   - Fix issues identified by the reviewer
4. Output: Modified/created files + summary of changes

### Writer Behavior
- On first call: implement the full feature
- On subsequent calls: fix issues from reviewer feedback
- Always run tests after making changes
- Report what was changed and why

---

## Step 2: Set Up Reviewer Agent

Create a Reviewer agent that reviews implementations with read-only access.

**File:** `src/agents/reviewer.md`

### Requirements
1. Read-only tools: Read, Glob, Grep only
2. Model: opus (highest quality review)
3. Responsibilities:
   - Review code for correctness, security, and style
   - Identify bugs and edge cases
   - Check test coverage and quality
   - Provide specific, actionable feedback
4. Output: Structured review with APPROVED or CHANGES_REQUESTED verdict

### Review Output Format
```
## Review

### Verdict: APPROVED | CHANGES_REQUESTED

### Issues
1. [CRITICAL] file:line — Description
2. [WARNING] file:line — Description
3. [INFO] file:line — Description

### Feedback for Writer
Specific instructions on what to fix.
```

---

## Step 3: Run the Pipeline Manually

Execute the writer/reviewer pipeline manually using Claude CLI.

### Workflow
```bash
# 1. Writer implements the feature
claude --agent src/agents/writer.md \
  "Implement a user authentication module in src/project/src/auth.py with:
   - login(email, password) function
   - logout(token) function
   - validate_token(token) function
   - Password hashing (simulated)
   - JWT-like token generation
   Include tests in src/project/src/test_auth.py"

# 2. Reviewer reviews the implementation
REVIEW=$(claude --agent src/agents/reviewer.md --print \
  "Review the authentication module in src/project/src/auth.py and its tests")

# 3. If changes requested, writer fixes
echo "$REVIEW" | grep -q "CHANGES_REQUESTED" && \
  claude --agent src/agents/writer.md \
    "Fix the following issues from the reviewer: $REVIEW"

# 4. Re-review
claude --agent src/agents/reviewer.md --print \
  "Re-review the authentication module after fixes"
```

---

## Step 4: Implement with Agent SDK

Build the full pipeline programmatically using the Agent SDK.

**File:** `src/python/writer_reviewer_pipeline.py`

### Requirements
1. Implement the writer/reviewer loop with max iterations
2. Parse the reviewer's verdict (APPROVED vs. CHANGES_REQUESTED)
3. Pass reviewer feedback to the writer for fixes
4. Track iteration count and stop after max attempts
5. Handle errors gracefully
6. Log each step for observability

### Pipeline Logic (Pseudocode)
```python
def run_pipeline(feature_request: str, max_iterations: int = 3):
    # Step 1: Writer implements
    writer_result = writer_agent.query(f"Implement: {feature_request}")

    for i in range(max_iterations):
        # Step 2: Reviewer reviews
        review = reviewer_agent.query("Review the recent changes")

        if "APPROVED" in review.text:
            print(f"Approved after {i + 1} iteration(s)")
            return True

        # Step 3: Writer fixes based on review
        writer_result = writer_agent.query(
            f"Fix these issues from the reviewer:\n{review.text}"
        )

    print(f"Not approved after {max_iterations} iterations")
    return False
```

---

## Step 5: Add Verification Agent

Add a final verification agent that runs tests as a quality gate.

**File:** `src/agents/verifier.md`

### Requirements
1. Tools: Bash (test commands only), Read, Glob
2. Model: haiku (fast, just runs tests)
3. Responsibilities:
   - Run the full test suite
   - Check test pass/fail status
   - Report coverage metrics
   - Give final PASS/FAIL verdict
4. Only runs after reviewer approves

### Updated Pipeline
```
Writer implements
  → Reviewer reviews (loop until APPROVED)
    → Verifier runs tests (final gate)
      → PASS: Feature complete
      → FAIL: Back to Writer with test failures
```

---

## Success Criteria

- [ ] Writer agent correctly implements features with tests
- [ ] Reviewer agent finds real issues and gives structured feedback
- [ ] Writer agent correctly fixes issues based on reviewer feedback
- [ ] Pipeline loops until approval or max iterations
- [ ] Verifier agent runs tests and gives final verdict
- [ ] Full pipeline works end-to-end (implement → review → fix → verify)
- [ ] Python SDK implementation works

## Bonus Challenges

1. **Parallel reviews**: Run multiple reviewers (security, performance, style) in parallel
2. **Quality metrics**: Track quality score over iterations
3. **Smart stopping**: Stop early if reviewer finds no critical issues
4. **Review memory**: Reviewer remembers patterns from past reviews
