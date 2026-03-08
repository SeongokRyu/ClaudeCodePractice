# Challenge: Git Workflow Hands-On

## Overview

Practice Git workflows while modifying the string utility functions in `src/string_utils.py`.
Ask Claude to perform the Git operations at each step.

**Prerequisite**: The current directory must be inside a Git repository before starting this exercise.

---

## Step 1: Creating a Backup Branch

Before starting changes, ask Claude to create a backup branch:

```
Before starting changes, please create a backup branch for safety.
Name the branch backup/before-string-utils-refactor.
```

**Observation point**: Observe the process of Claude checking the current branch and creating the backup branch.

---

## Step 2: Descriptive Commit After Changes

### 2-1. Request Changes

```
Improve the capitalize function in src/string_utils.py.
Currently it only capitalizes the first letter, but also add a
capitalize_words function that capitalizes the first letter of each word.
Add tests as well.
Verify with pytest.
```

### 2-2. Request a Commit

```
Commit the changes so far with a descriptive commit message.
The commit message can be written in English.
```

**Observation point**: Check the structure of the commit message Claude writes (title + body).

---

## Step 3: Implement a New Feature on a Feature Branch

### 3-1. Create a Feature Branch

```
Create a new feature branch named feature/add-pad-functions and
add the following functions to src/string_utils.py:
- pad_start(s, length, char): Pads the beginning of a string with a specific character to reach the desired length
- pad_end(s, length, char): Pads the end of a string with a specific character to reach the desired length
Add tests and verify with pytest.
```

### 3-2. Commit

```
Commit the changes.
```

**Observation point**: Observe the process of Claude creating and switching to the branch.

---

## Step 4: Write a PR Description

Ask Claude to summarize the changes on the current branch as a PR description:

```
Compare the changes on the current branch with the main branch (or previous branch)
and summarize them in PR description format.

Write it in the following format:
## Summary
## Changes
## Test Plan
```

**Observation point**: Notice how Claude uses git diff and git log to analyze the changes.

---

## Step 5: Practicing /rewind

### 5-1. Make an Intentional Change

```
Completely rewrite the slugify function in src/string_utils.py.
Improve it to support Unicode characters.
```

### 5-2. Revert the Changes

Assume you don't like the changes and use `/rewind`:

```
/rewind
```

Select the checkpoint before the slugify modification from the list.

### 5-3. Verify After Reverting

```
Verify that the slugify function in src/string_utils.py has been restored to its original state.
Run pytest to confirm tests pass.
```

**Observation point**: Notice that `/rewind` reverts both file changes and Git state.

---

## Completion Checklist

- [ ] Created a backup branch as a safety net
- [ ] Asked Claude to commit with a descriptive commit message
- [ ] Created a feature branch and implemented a new feature
- [ ] Summarized changes in PR description format
- [ ] Used `/rewind` to revert changes

## Tips

- Build the habit of always creating a backup branch before making changes
- When you ask Claude to "write a commit message," it analyzes the changes and writes an appropriate message
- `/rewind` can revert all of Claude's changes (file modifications, Git operations)
- Claude will warn you about dangerous Git operations (force push, reset --hard, etc.)
