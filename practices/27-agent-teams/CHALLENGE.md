# Challenge: Agent Teams 실습

## Step 1: Enable Agent Teams

Enable the experimental Agent Teams feature.

### Setup
```bash
# Option 1: Environment variable
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1

# Option 2: settings.json (see src/settings-example.json)
# Add to ~/.claude/settings.json or project .claude/settings.json
```

### Verification
1. Start Claude Code: `claude`
2. You should see a team panel or indicator in the UI
3. Try `Ctrl+T` to toggle the shared task list

---

## Step 2: Create a Team

Use natural language to spawn teammates.

### Basic Team Creation
In the Claude Code prompt, type:
```
Create a team with two teammates:
1. A frontend developer working on the Streamlit app in src/project/frontend/
2. A backend developer working on the Flask API in src/project/backend/
```

### What Should Happen
- Two additional Claude Code instances spawn
- Each has its own context and working area
- A shared task list appears

### Verification
- [ ] Multiple teammates are visible
- [ ] Each teammate has a separate conversation
- [ ] Shared task list is accessible with `Ctrl+T`

---

## Step 3: Use the Shared Task List

Learn to coordinate work through the shared task list.

### Creating Tasks
Ask the lead agent to create tasks:
```
Add these tasks to the shared list:
- [ ] Frontend: Create UserProfile page in Streamlit
- [ ] Frontend: Add authentication form
- [ ] Backend: Create /api/users endpoint in Flask
- [ ] Backend: Add JWT middleware
- [ ] Testing: Write integration tests for auth flow (pytest)
```

### Task Coordination
- Tasks are visible to all teammates
- Teammates can claim and complete tasks
- Use `Ctrl+T` to toggle the task list view

### Verification
- [ ] Tasks appear in the shared list
- [ ] Teammates can see the same tasks
- [ ] Task status updates are visible to all

---

## Step 4: Navigate Between Teammates

Learn to switch between and monitor teammates.

### Navigation
| Action | Shortcut |
|--------|----------|
| Toggle task list | `Ctrl+T` |
| Cycle teammates | `Tab` |
| View teammate | `Enter` |

### Monitoring
1. Use `Tab` to cycle through teammates
2. Check what each teammate is working on
3. Verify they are making progress on their assigned tasks
4. Look for any conflicts (both editing the same file)

### Verification
- [ ] Can cycle between all teammates
- [ ] Can view each teammate's conversation
- [ ] Can see what each teammate is working on

---

## Step 5: Specialist Team

Create a team of specialists for a complex feature.

### Prompt
Use the prompt from `src/team-prompts/specialist-team.md`:
```
Create a specialist team to implement a user dashboard feature:

1. UX Specialist — Focus on Streamlit layout, styling, and user experience.
   Work in src/project/frontend/src/. Create the dashboard pages.

2. Backend Specialist — Focus on Flask API design, data models, and business logic.
   Work in src/project/backend/src/. Create the dashboard API endpoints.

3. Testing Specialist — Focus on test coverage, edge cases, and integration.
   Work in src/project/tests/. Write comprehensive pytest tests.

Shared task list:
- [ ] Design dashboard data model
- [ ] Create GET /api/dashboard endpoint
- [ ] Create DashboardView component
- [ ] Create DashboardWidget component
- [ ] Write unit tests for dashboard API (pytest)
- [ ] Write tests for Streamlit dashboard page
- [ ] Write integration test for full dashboard flow (pytest)
```

### Verification
- [ ] Three specialists are spawned
- [ ] Each works in their designated area
- [ ] Task list shows progress
- [ ] No file conflicts between specialists

---

## Step 6: Competing Hypotheses

Use the "competing hypotheses" pattern for debugging.

### Scenario
Imagine a bug: "The dashboard loads slowly and sometimes shows stale data."

### Prompt
Use the prompt from `src/team-prompts/competing-hypotheses.md`:
```
Debug the slow dashboard issue. Spawn 3 teammates, each investigating a different hypothesis:

1. Hypothesis A — "It's a frontend rendering issue"
   Investigate: Streamlit re-renders, caching with st.cache_data, session state

2. Hypothesis B — "It's a backend API performance issue"
   Investigate: Database queries, N+1 problems, missing indexes, caching

3. Hypothesis C — "It's a caching/state management issue"
   Investigate: Stale cache, race conditions, optimistic updates gone wrong

Each teammate should:
- Investigate their hypothesis thoroughly
- Find evidence for or against
- Report confidence level (low/medium/high)
- Suggest specific fixes if the hypothesis is confirmed
```

### Evaluation
After all teammates report:
1. Compare confidence levels
2. Look for overlapping findings
3. Identify the most likely root cause
4. Plan the fix based on the winning hypothesis

### Verification
- [ ] Three teammates investigate simultaneously
- [ ] Each produces a focused investigation report
- [ ] Evidence is specific (file:line references)
- [ ] At least one hypothesis is confirmed or ruled out

---

## Success Criteria

- [ ] Agent Teams feature is enabled and working
- [ ] Can create teams with natural language prompts
- [ ] Shared task list is functional
- [ ] Can navigate between teammates
- [ ] Specialist team completes a feature across layers
- [ ] Competing hypotheses pattern produces useful debugging insights

## Bonus Challenges

1. **4+ team members**: Create a larger team for a complex feature
2. **Team communication**: Have teammates share findings via the task list
3. **Team retrospective**: After completion, review what each teammate did
4. **Cross-layer feature**: Use `src/team-prompts/cross-layer-feature.md` for a feature spanning frontend, backend, and database
