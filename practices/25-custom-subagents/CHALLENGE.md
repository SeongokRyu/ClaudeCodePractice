# Challenge: Custom Subagent Design

## Step 1: Design a 3-Agent System

Design a system with three specialized agents: researcher, implementer, and reviewer.

### Requirements
1. Define clear boundaries for each agent's responsibilities
2. Map out the workflow: researcher -> implementer -> reviewer
3. Document what each agent can and cannot do
4. Decide on model selection for each role

### Design Document
Create a brief design showing:
- Agent roles and responsibilities
- Tool permissions per agent
- Model assignments
- Data flow between agents
- Expected output format from each agent

---

## Step 2: Create Researcher Agent

**File:** `src/agents/researcher.md`

### Requirements
1. Read-only tools: `Read`, `Glob`, `Grep` only
2. Model: `haiku` (fast, cheap — good for exploration)
3. Mode: Plan mode — analyze, don't implement
4. Output: Structured analysis with:
   - File inventory
   - Architecture overview
   - Key patterns identified
   - Recommended approach for changes

### Testing
```bash
# The researcher should analyze src/project/ and produce a plan
# It should NOT be able to modify any files
claude --agent src/agents/researcher.md "Analyze the Python project in src/project/ and create an implementation plan for adding a user authentication module"
```

---

## Step 3: Create Implementer Agent

**File:** `src/agents/implementer.md`

### Requirements
1. Full tool access: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`
2. Model: `sonnet` (balanced quality and speed)
3. Skills preloaded: coding conventions, testing patterns
4. Output: Working code with tests
5. Constraints:
   - Must follow existing code patterns
   - Must write tests for new code
   - Must not modify unrelated files

### Testing
```bash
# Give it the researcher's plan and let it implement
claude --agent src/agents/implementer.md "Implement the authentication module based on this plan: [paste researcher output]"
```

---

## Step 4: Create Reviewer Agent

**File:** `src/agents/reviewer.md`

### Requirements
1. Read-only tools: `Read`, `Glob`, `Grep` only
2. Model: `inherit` (use whatever the parent uses)
3. Memory: enabled — accumulates patterns across reviews
4. Output: Structured review with:
   - Issues found (severity: critical/warning/info)
   - Code quality score (1-10)
   - Specific suggestions with file:line references
   - Approval status: APPROVED / CHANGES_REQUESTED

### Testing
```bash
# Review the implementer's changes
claude --agent src/agents/reviewer.md "Review the recent changes to src/project/ for code quality, security, and test coverage"
```

---

## Step 5: Test Each Agent Independently

Run each agent on the sample project in `src/project/` and verify:

### Researcher
- [ ] Only reads files (no modifications)
- [ ] Produces structured analysis
- [ ] Identifies existing patterns correctly
- [ ] Creates actionable implementation plan

### Implementer
- [ ] Writes working code
- [ ] Creates corresponding tests
- [ ] Follows existing code patterns
- [ ] Does not modify unrelated files

### Reviewer
- [ ] Only reads files (no modifications)
- [ ] Identifies real issues
- [ ] Provides specific file:line references
- [ ] Gives clear approval/rejection

### Additional Agents
Also test the tester and security-auditor agents:
- **Tester**: Runs tests, reports coverage, suggests missing test cases
- **Security Auditor**: Scans for vulnerabilities, checks dependencies

---

## Step 6: Wire Them Together in a Workflow

Create a workflow that chains all three agents:

### Workflow
```
1. Researcher analyzes the codebase → produces plan
2. Implementer takes the plan → writes code + tests
3. Reviewer reviews the changes → approves or requests changes
4. If CHANGES_REQUESTED: loop back to Implementer with feedback
5. If APPROVED: done
```

### Implementation Options

**Option A: Shell script orchestration**
```bash
#!/bin/bash
# 1. Research phase
PLAN=$(claude --agent src/agents/researcher.md --print "Analyze src/project/")

# 2. Implementation phase
claude --agent src/agents/implementer.md "Implement based on: $PLAN"

# 3. Review phase
REVIEW=$(claude --agent src/agents/reviewer.md --print "Review changes in src/project/")

# 4. Check approval
if echo "$REVIEW" | grep -q "CHANGES_REQUESTED"; then
  claude --agent src/agents/implementer.md "Fix issues: $REVIEW"
fi
```

**Option B: Agent SDK orchestration (Python)**
Use the Agent SDK to programmatically manage the workflow with proper error handling and retry logic.

---

## Success Criteria

- [ ] All 5 agent definitions are complete and well-documented
- [ ] Tool restrictions are correctly enforced per agent
- [ ] Model selection is appropriate for each role
- [ ] Each agent produces structured, useful output
- [ ] The 3-agent workflow completes successfully
- [ ] Reviewer correctly identifies issues in implementer's code

## Bonus Challenges

1. **Add a Tester agent**: Runs tests and reports coverage
2. **Add a Security Auditor agent**: Scans for vulnerabilities
3. **Agent memory**: Make the reviewer remember patterns across sessions
4. **Dynamic model selection**: Use haiku for simple tasks, sonnet for complex ones
