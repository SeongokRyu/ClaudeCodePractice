# Challenge: Context Management Hands-On

## Overview

`src/user_service.py` is a user CRUD service.
Practice context management techniques while exploring and modifying this code.

---

## Step 1: Observing Context Usage

Observe the context filling up as you ask Claude to perform several tasks.

### 1-1. Code Exploration

```
Read the entire code in src/user_service.py and explain the role of each method.
```

### 1-2. Type Analysis

```
Analyze the User dataclass in src/user_service.py and suggest additional fields that would be useful.
```

### 1-3. Test Analysis

```
Analyze the test coverage in src/test_user_service.py and
list the missing test cases.
```

### 1-4. Check Usage

```
/cost
```

Confirm that the context usage has increased.

---

## Step 2: Practicing /clear

### 2-1. Starting a New Unrelated Task

Use `/clear` before starting a new task unrelated to the previous one:

```
/clear
```

### 2-2. Perform the New Task

```
Add an email duplication check feature to src/user_service.py.
Modify the create_user method to raise an exception if a user with the same email already exists.
Add tests as well.
Verify with pytest.
```

**Observation point**: Notice that Claude can still read the files and work even after `/clear`.

---

## Step 3: Practicing /compact

### 3-1. Perform Several Tasks

Perform a few tasks in succession:

```
Add the following features to src/user_service.py:
1. find_by_email(email: str) method
2. Duplication check when email is changed in update_user
3. Tests for each feature
Verify with pytest.
```

### 3-2. Use /compact

Use the hint parameter to compress the context:

```
/compact Please summarize focusing on the user-service CRUD features and email validation logic
```

### 3-3. Continue Working After Compression

```
Add a list_users_paginated method with pagination to user_service.
It should accept offset and limit parameters and return a subset of the user list.
Add tests as well.
```

**Observation point**: Notice that the context from previous work is preserved even after `/compact`.

---

## Step 4: Writing HANDOFF.md

### 4-1. Document the Current State

Ask Claude to write a HANDOFF.md:

```
Based on the work performed on user-service so far, write a HANDOFF.md.
Include the current state, completed tasks, remaining tasks, and key decisions
so that another developer (or a new Claude session) can continue the work in the next session.
```

### 4-2. Continue in a New Session

Start a new Claude session and use the HANDOFF.md to continue the work:

```
Read HANDOFF.md and understand the current project state.
Pick one of the remaining tasks and implement it.
```

---

## Step 5: --resume and --continue Flags

### 5-1. Continue After Ending a Session

After exiting Claude in the terminal:

```bash
# Select from previous sessions and continue
claude --resume

# Or automatically continue from the last session
claude --continue
```

### 5-2. Verify Continuation

```
Summarize what was done in the previous session.
```

**Observation point**: Notice that the previous conversation content is preserved when using `--resume`/`--continue`.

---

## Completion Checklist

- [ ] Checked context usage with `/cost`
- [ ] Used `/clear` to reset context between unrelated tasks
- [ ] Used `/compact` with a hint to compress the context
- [ ] Wrote HANDOFF.md and used it in a new session
- [ ] Tried the `--resume` or `--continue` flags

## Tips

- Consider using `/compact` when the context exceeds 50%
- `/clear` is more appropriate when starting a completely different task
- HANDOFF.md is also useful for team collaboration (AI-to-AI handoff)
- `--resume` allows session selection, while `--continue` automatically continues from the last session
