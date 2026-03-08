# Challenge: Git Hooks + Claude

## Overview

Set up Git hooks that use Claude for intelligent security scanning, commit message validation, and quality checks. Also configure Claude Code's own hook system to control how Claude interacts with git.

---

## Step 1: Pre-Commit Secret Scanner

Set up a pre-commit hook that uses Claude to detect secrets in staged files.

### Tasks

1. Read `src/hooks/pre-commit` to understand the hook script
2. Install it in a test repository:
   ```bash
   cp src/hooks/pre-commit .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```
3. Test with the unsafe example code:
   ```bash
   cp src/example-code/app.ts /tmp/test-repo/app.ts
   cd /tmp/test-repo
   git add app.ts
   git commit -m "test"
   # Should be BLOCKED by the pre-commit hook
   ```
4. Test with the safe example code:
   ```bash
   cp src/example-code/safe-app.ts /tmp/test-repo/app.ts
   git add app.ts
   git commit -m "test"
   # Should PASS the pre-commit hook
   ```

### How It Works

The pre-commit hook:
1. Gets the list of staged files
2. For each file, pipes the content to `claude -p`
3. Claude analyzes for hardcoded secrets, API keys, passwords
4. If secrets are found, the commit is blocked

### Verification

- Committing code with hardcoded secrets should be blocked
- Committing code using environment variables should pass
- The hook should give clear feedback about what was found

---

## Step 2: Commit Message Validation

Set up a commit-msg hook that validates the format of commit messages.

### Tasks

1. Read `src/hooks/commit-msg` to understand the validation logic
2. Install it:
   ```bash
   cp src/hooks/commit-msg .git/hooks/commit-msg
   chmod +x .git/hooks/commit-msg
   ```
3. Test with a bad commit message:
   ```bash
   git commit -m "fixed stuff"
   # Should be REJECTED — not following conventional commits
   ```
4. Test with a good commit message:
   ```bash
   git commit -m "fix: resolve null pointer in user authentication"
   # Should PASS
   ```

### How It Works

The commit-msg hook:
1. Reads the commit message from the file passed as argument
2. Validates it against Conventional Commits format
3. Optionally uses Claude to check if the message accurately describes the diff

### Verification

- Non-conventional commit messages should be rejected
- Properly formatted messages should pass
- Claude-enhanced mode should check message accuracy

---

## Step 3: Claude Code PreToolUse Hook

Create a Claude Code hook that intercepts git commit operations.

### Tasks

1. Read `src/claude-hooks/settings-example.json`
2. Understand the hook configuration:
   ```json
   {
     "hooks": {
       "PreToolUse": [
         {
           "matcher": "Bash",
           "hook": "/path/to/hook-script.sh"
         }
       ]
     }
   }
   ```
3. The hook script receives the tool input as JSON on stdin
4. It can:
   - Return `{"decision": "allow"}` to permit the tool call
   - Return `{"decision": "block", "reason": "..."}` to block it
5. Create a hook that blocks `git push --force` commands

### Verification

- Claude should be unable to force-push when the hook is active
- Regular git operations should work normally
- The hook should provide a clear reason when blocking

---

## Step 4: Test the Hooks

Test the complete hook pipeline with realistic scenarios.

### Tasks

1. Create a test repository:
   ```bash
   mkdir /tmp/hooks-test && cd /tmp/hooks-test
   git init
   ```
2. Install all hooks from `src/hooks/`
3. Test scenario: Commit with a secret
   ```bash
   echo 'const API_KEY = "sk-1234567890abcdef";' > config.ts
   git add config.ts
   git commit -m "add config"
   # pre-commit should BLOCK this
   ```
4. Test scenario: Bad commit message
   ```bash
   echo 'const x = 1;' > safe.ts
   git add safe.ts
   git commit -m "stuff"
   # commit-msg should REJECT this
   ```
5. Test scenario: Clean commit
   ```bash
   echo 'const x = process.env.API_KEY;' > safe.ts
   git add safe.ts
   git commit -m "feat: add API key from environment"
   # Should PASS all hooks
   ```

### Verification

- All three scenarios should behave as expected
- Hook messages should be clear and actionable
- Hooks should run fast enough for a good developer experience

---

## Step 5: Auto-Commit Shell Function

Create the auto-commit shell function for daily use.

### Tasks

1. Combine the knowledge from Steps 1-4
2. Create a shell function that:
   - Runs security scan on staged changes
   - Generates a commit message with Claude
   - Validates the message format
   - Creates the commit
3. Add it to your shell profile:
   ```bash
   # In ~/.bashrc or ~/.zshrc
   source /path/to/auto-commit.sh
   ```
4. Test in your daily workflow

### Verification

- The function should handle edge cases (no changes, merge commits, etc.)
- It should be fast enough for regular use (< 10 seconds)
- It should provide an option to edit the generated message

---

## Bonus Challenges

1. **Severity levels**: Make the pre-commit hook configurable with severity thresholds
2. **Team config**: Create a shared hook configuration that the whole team can use
3. **Metrics**: Track how many commits are blocked and why
4. **IDE integration**: Make the hooks work with VS Code's Git integration

---

## Key Takeaways

- Git hooks + Claude = intelligent code gatekeeping
- Pre-commit hooks can catch security issues before they enter version control
- Claude Code hooks provide a second layer of control over Claude's own actions
- Shell functions make AI-powered workflows feel native
- Balance thoroughness with speed — hooks should not slow down development
