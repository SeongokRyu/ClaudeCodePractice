# Challenge: Worktree Parallel Development

## Step 1: Understanding Git Worktree Concepts

Git worktree allows you to maintain multiple working directories simultaneously from a single repository.

### Regular Branch Switching vs Worktree

```
Regular branch switching:
  git checkout feature-auth   → work → git stash
  git checkout feature-log    → work → git stash
  git checkout feature-auth   → git stash pop → continue working
  ❌ High context switching cost

Worktree:
  Terminal 1: ~/project/           (main)
  Terminal 2: ~/project-auth/      (feature-auth)
  Terminal 3: ~/project-log/       (feature-logging)
  ✅ Work independently in each terminal
```

### Basic Commands

```bash
# Create worktree
git worktree add ../my-project-feature-auth -b feature-auth

# List worktrees
git worktree list

# Remove worktree
git worktree remove ../my-project-feature-auth
```

### Exercise

Run the following command to verify worktree behavior:

```bash
git worktree list
```

---

## Step 2: Starting a Worktree Session — Authentication Feature

Start a worktree-based Claude session in the first terminal.

```bash
claude --worktree feature-auth
```

This command automatically performs the following:
1. Creates the `feature-auth` branch
2. Creates a new worktree directory
3. Starts a Claude session in that directory

### Request Authentication Feature Implementation

Ask Claude the following:

```
Add authentication features to src/app.py:
1. POST /auth/login endpoint — accepts username, password and returns JWT token
2. POST /auth/register endpoint — register new user
3. auth_middleware — token verification middleware
4. Apply authentication middleware to existing GET /users endpoint
5. Please add tests as well
```

### Checklist
- [ ] Confirm you are working on the feature-auth branch
- [ ] Confirm authentication-related code has been added
- [ ] Confirm tests pass

---

## Step 3: Second Worktree Session — Logging Feature

Open **another terminal** and start a second worktree session.

```bash
claude --worktree feature-logging
```

### Request Logging Feature Implementation

Ask Claude the following:

```
Add request logging features to src/app.py:
1. requestLogger middleware — logs method, path, response time for all requests
2. GET /logs endpoint — view recent logs
3. Log level support (info, warn, error)
4. Automatically record error logs when errors occur
5. Please add tests as well
```

### Checklist
- [ ] Confirm you are working on the feature-logging branch (independent from feature-auth!)
- [ ] Confirm logging-related code has been added
- [ ] Confirm tests pass
- [ ] Confirm changes from feature-auth are not in this branch

---

## Step 4: Performing Parallel Work

Experience simultaneous work in progress across both terminals.

### In Terminal 1 (feature-auth)

```
Add password hashing to the authentication feature.
Use bcrypt to securely store passwords.
```

### In Terminal 2 (feature-logging)

```
Add structured JSON format to logging.
Make each log entry include timestamp, level, message, and metadata.
```

### Verify Benefits of Parallel Work

```bash
# In Terminal 1
git log --oneline feature-auth

# In Terminal 2
git log --oneline feature-logging

# The commit histories of both branches are completely independent!
```

---

## Step 5: Merging via PR

Merge the work from each worktree via pull requests.

### 5-1. Create PR from Each Branch

```bash
# Terminal 1 (feature-auth)
git push -u origin feature-auth
gh pr create --title "feat: Add authentication system" --body "Add JWT-based authentication system"

# Terminal 2 (feature-logging)
git push -u origin feature-logging
gh pr create --title "feat: Add request logging" --body "Add structured request logging system"
```

### 5-2. PR Review and Merge

```bash
# Review and merge each PR
gh pr merge --squash
```

### 5-3. Clean Up Worktrees

```bash
# Remove worktrees after work is complete
git worktree list
git worktree remove ../project-feature-auth
git worktree remove ../project-feature-logging
git worktree prune
```

---

## Success Criteria

- [ ] Developed features independently in two worktrees
- [ ] Changes in each worktree were isolated from each other
- [ ] Tests passed for both features
- [ ] Was able to merge to the main branch via PRs
- [ ] Cleaned up worktrees after completion

## Key Takeaways

1. **worktree = physical isolation**: Each feature is developed in a completely independent directory
2. **Zero context switching**: Just switch terminals without stash/checkout
3. **Claude session isolation**: Claude in each worktree focuses only on that feature
4. **PR-based integration**: Each feature can be reviewed and merged independently
