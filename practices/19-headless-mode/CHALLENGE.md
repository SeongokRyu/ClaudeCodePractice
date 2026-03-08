# Challenge: Headless Mode 기초

## Overview

Build a set of shell scripts that use `claude -p` (headless mode) to automate common development tasks: code review, commit message generation, and TODO scanning.

---

## Step 1: Basic Headless Mode

Run Claude non-interactively with a simple prompt.

### Tasks

1. Navigate to this practice directory
2. Run your first headless command:
   ```bash
   claude -p "explain what this project does"
   ```
3. Try with a more specific prompt:
   ```bash
   claude -p "list all Python files in src/ and describe their purpose"
   ```
4. Observe that Claude uses tools (Read, Glob, etc.) automatically

### Verification

- Claude should output a text response to stdout and exit
- The response should accurately describe the project structure

---

## Step 2: Pipe Input

Feed file contents to Claude via stdin.

### Tasks

1. Pipe a single file:
   ```bash
   cat src/app.py | claude -p "review this code for potential issues"
   ```
2. Pipe multiple files:
   ```bash
   cat src/app.py src/test_app.py | claude -p "review this code and its tests"
   ```
3. Pipe command output:
   ```bash
   git log --oneline -10 | claude -p "summarize recent changes"
   ```
4. Pipe with context:
   ```bash
   git diff HEAD~1 | claude -p "review this diff and suggest improvements"
   ```

### Verification

- Claude should analyze the piped content without needing to read files itself
- Responses should be specific to the piped content

---

## Step 3: JSON Output

Get structured responses for programmatic consumption.

### Tasks

1. Get JSON output:
   ```bash
   claude -p "list all TODO comments in src/" --output-format json
   ```
2. Parse the result field with jq:
   ```bash
   claude -p "list TODO comments as a JSON array" --output-format json | jq '.result'
   ```
3. Extract specific fields:
   ```bash
   claude -p "count lines of code in src/" --output-format json | jq '{result: .result, cost: .cost_usd}'
   ```
4. Use in a script:
   ```bash
   RESULT=$(claude -p "is there a security issue in src/app.py? answer yes or no" --output-format json | jq -r '.result')
   echo "Security check: $RESULT"
   ```

### Verification

- JSON output should be valid and parseable with jq
- The `result` field should contain Claude's response text
- Cost information should be available in the output

---

## Step 4: Tool Restrictions

Limit what Claude can do for safety and focus.

### Tasks

1. Read-only review (no editing):
   ```bash
   claude -p "review src/app.py for bugs" --allowedTools Read,Grep --max-turns 5
   ```
2. Analysis only (no file system access):
   ```bash
   cat src/app.py | claude -p "review this code" --allowedTools "" --max-turns 3
   ```
3. Limited editing:
   ```bash
   claude -p "fix typos in src/app.py" --allowedTools Read,Edit --max-turns 5
   ```
4. Verify restrictions work:
   ```bash
   # This should fail to create files since Write is not allowed
   claude -p "create a new file called test.txt" --allowedTools Read,Grep --max-turns 3
   ```

### Verification

- Claude should respect tool restrictions
- With `--max-turns`, Claude should stop after the specified number of tool calls
- Without necessary tools, Claude should explain what it cannot do

---

## Step 5: Auto Commit Message

Create a shell function that generates commit messages using Claude.

### Tasks

1. Read `src/scripts/auto-commit.sh`
2. Understand how it:
   - Captures `git diff --staged`
   - Pipes the diff to `claude -p`
   - Uses the generated message for `git commit`
3. Test the function:
   ```bash
   # Make a change to src/app.py
   git add src/app.py
   source src/scripts/auto-commit.sh
   auto_commit
   ```
4. Improve the prompt to match your team's commit message conventions

### Verification

- The generated commit message should follow conventional commit format
- The message should accurately describe the staged changes
- The function should handle the case where there are no staged changes

---

## Step 6: Review Script

Build a simple review script that reviews changed files.

### Tasks

1. Read `src/scripts/review-changes.sh`
2. Understand how it:
   - Gets the list of changed files from `git diff`
   - Reviews each file using `claude -p`
   - Aggregates results into a report
3. Run the script:
   ```bash
   bash src/scripts/review-changes.sh
   ```
4. Extend it to:
   - Output results as JSON
   - Filter by file type
   - Set severity levels for findings

### Verification

- The script should review all changed files
- Output should be clear and actionable
- The script should handle no changes gracefully

---

## Bonus Challenges

1. **Pipeline script**: Chain multiple `claude -p` calls where the output of one feeds into the next
2. **Parallel review**: Use `xargs -P` to review multiple files in parallel (preview of Practice 22)
3. **Custom formatter**: Build a script that reformats Claude's JSON output into a markdown report
4. **Git alias**: Create a git alias that uses Claude for interactive rebase message editing

---

## Key Takeaways

- `claude -p` is the foundation for all Claude Code automation
- Pipe input avoids the need for file system access in many cases
- JSON output enables programmatic consumption of results
- Tool restrictions are essential for safe automation
- Shell scripts can orchestrate multiple Claude calls for complex workflows
