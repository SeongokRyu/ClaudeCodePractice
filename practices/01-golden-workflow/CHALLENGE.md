# Challenge: Golden Workflow Hands-On

There is a simple todo management app in the `src/` directory.
You will experience the golden workflow by adding a "priority feature" to this code.

---

## Step 1: Explore — 5 min

**Goal**: Understand the existing code. Don't read it yourself — let Claude do it.

1. Start Claude Code in this practice directory:
   ```bash
   cd practices/01-golden-workflow
   claude
   ```

2. Switch to **Plan Mode**: Press `Shift+Tab` twice (Normal → Auto-accept → Plan)

3. Have Claude explore the code:
   ```
   Read the code in the src/ directory and explain its structure.
   What features does it have, and what does the data model look like?
   ```

4. Read Claude's response and understand the code structure.

> **Checkpoint**: Success if Claude explained the Todo dataclass, list of functions, and test structure.

---

## Step 2: Plan — 5 min

**Goal**: Create a change plan and verify the direction before implementing.

1. While still in **Plan Mode**, request the following:
   ```
   I want to add a priority feature to this Todo app.
   - Priority has 3 levels: high, medium, low
   - Default is medium
   - Filtering by priority
   - Sorting by priority

   Create a plan for which files need to be modified and in what order.
   ```

2. Review Claude's plan:
   - Is the list of files to modify reasonable?
   - Is the order logical? (Usually: data model → logic → tests)
   - Is anything missing?

3. (Optional) Press `Ctrl+G` to edit the plan in your editor.

> **Checkpoint**: Success if a plan with files to modify, changes, and order was produced.

---

## Step 3: Implement — 10 min

**Goal**: Exit Plan Mode and modify the actual code.

1. Switch to **Normal Mode**: `Shift+Tab` (Plan → Normal)

2. Instruct Claude to implement:
   ```
   Implement the priority feature according to the plan we just created.
   After implementation, run the tests to make sure they pass.
   ```

3. Watch Claude modify the files:
   - Observe which tools (Edit, Write, Bash) it uses
   - Check the test execution results

4. **If tests fail**:
   ```
   Fix the failing tests. Analyze the root cause and fix it.
   ```

> **Checkpoint**: Success if the code was modified and tests pass.
> (It's okay if they fail — the debugging process itself is a learning experience)

---

## Step 4: Commit — 5 min

**Goal**: Commit the changes cleanly.

1. Ask Claude to commit:
   ```
   Review the changes and commit them with an appropriate commit message.
   ```

2. Watch Claude review the changes with `git diff` and create the commit.

3. After committing, reset the conversation with `/clear`.

> **Checkpoint**: Success if a commit was created with a clean commit message.

---

## Self-Check

- [ ] Switched between Plan Mode and Normal Mode
- [ ] Created a plan before implementing
- [ ] Reviewed and evaluated Claude's plan
- [ ] Verified the implementation by running tests
- [ ] Used `Shift+Tab`, `Esc`, and `/clear`

## Bonus Challenge

Try the same process on your own project:
1. Start `claude` in your project directory
2. Explore the codebase in Plan Mode
3. Create a plan for a small feature addition
4. Switch to Normal Mode and implement
5. Commit

## Next Practice

[Practice 02: Prompting Techniques](../02-prompting-techniques/) — Learn verification criteria and interview techniques.
