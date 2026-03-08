# Challenge: Multi-File Refactoring

## Pre-check

First, confirm that all tests pass:

```bash
uv run pytest src/
```

All tests should pass. This is the safety net for your refactoring.

---

## Step 1: Exploration — Identify the Dependency Graph

Ask Claude to analyze the codebase structure and dependencies.

### Prompts to Try with Claude

```
Read all the files in the src/ directory and draw a dependency graph.
Analyze which file imports which, and how the callback pattern is being used.
```

### Expected Result

```
types.py               ← No dependencies (lowest level)
database.py            ← No dependencies
user_repository.py     ← database.py
order_repository.py    ← database.py
notification_service.py ← No dependencies
app.py                 ← All modules (highest level)
```

---

## Step 2: Planning — Determine the Refactoring Order

Have Claude create a plan for the callback to async/await refactoring.

### Prompts to Try with Claude

```
I want to refactor this codebase from the callback pattern to async/await.
Based on the dependency graph, plan a safe refactoring order.

Conditions:
- Change only one file at a time
- Tests must pass after each change
- Do not change types.py
```

---

## Step 3: Step-by-Step Implementation

Refactor one file at a time according to the plan. **Run tests after every file change**.

### Prompts to Try with Claude

```
Execute step 1 of the refactoring plan.
Convert database.py from the callback pattern to async/await.

After conversion:
1. Run uv run pytest src/ and check the results
2. If any tests fail, update those tests to async/await as well
3. Repeat until all tests pass
```

Then refactor the remaining files in the same order:

```
Refactor the next file (user_repository.py) to async/await.
Use the new interface from database.py that was changed in the previous step.
After the change, run uv run pytest src/ to verify.
```

---

## Step 4: Verification

Perform final verification after all refactoring is complete.

### Prompts to Try with Claude

```
All refactoring is complete. Please verify the following:

1. Run uv run pytest src/ to confirm all tests pass
2. Search for any remaining callback patterns (the word "callback" should not appear)
3. Summarize the code comparison before and after refactoring

In particular, verify:
- Do all async functions use async/await?
- Has error handling been converted to try/except?
- Are types correctly preserved?
```

---

## Completion Criteria

- [ ] Step 1: Understood the dependency graph
- [ ] Step 2: Established a refactoring plan
- [ ] Step 3: Refactored one file at a time, passing tests each time
- [ ] Step 4: All tests pass and callback patterns have been removed

## Reflection Questions

1. How did identifying the dependency graph first help with refactoring?
2. What is the difference between changing one file at a time versus changing all files at once?
3. How much riskier would this refactoring have been without tests?
4. What was the benefit of asking Claude to "make a plan" versus directly saying "refactor it"?
