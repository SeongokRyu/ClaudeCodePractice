# Challenge: Deterministic Guardrails

## Step 1: File Protection Hook (PreToolUse)

Create a PreToolUse hook that blocks edits to protected files.

Protected paths:
- `.env` and `.env.*` files
- `migrations/` directory
- `package-lock.json`
- Any file matching a configurable protected paths list

The hook should:
- Read the tool input from stdin (JSON with tool_name and tool_input)
- Check if the target file matches any protected path pattern
- Exit 2 with a descriptive message if blocked
- Exit 0 if the file is allowed

Test cases:
- Try editing `.env` -- should be blocked
- Try editing `migrations/001_create_users.sql` -- should be blocked
- Try editing `src/index.ts` -- should be allowed

## Step 2: Dangerous Command Blocker (PreToolUse)

Create a PreToolUse hook that blocks dangerous bash commands.

Blocked patterns:
- `rm -rf /` or `rm -rf ~` (destructive deletion)
- `git push --force` or `git push -f` (force push)
- `DROP TABLE`, `DROP DATABASE` (SQL destruction)
- `chmod 777` (insecure permissions)
- `curl | sh` or `wget | bash` (pipe to shell)

The hook should:
- Only activate for the Bash tool
- Parse the command from the tool input
- Check against all dangerous patterns
- Provide a clear explanation of why the command was blocked

Test cases:
- `rm -rf /tmp/test` -- should be blocked
- `git push --force origin main` -- should be blocked
- `DROP TABLE users;` -- should be blocked
- `git push origin main` -- should be allowed
- `rm file.txt` -- should be allowed

## Step 3: Auto-Format Hook (PostToolUse)

Create a PostToolUse hook that automatically runs prettier after every file edit.

The hook should:
- Only activate after the Edit or Write tools
- Extract the file path from the tool input
- Only run prettier on supported file types (.ts, .js, .tsx, .jsx, .json, .css, .md)
- Run `npx prettier --write` on the file
- Log the formatting result to stderr

## Step 4: Auto-Lint Hook (PostToolUse)

Create a PostToolUse hook that automatically runs eslint after edits to TypeScript files.

The hook should:
- Only activate after the Edit or Write tools
- Check if the edited file ends in `.ts` or `.tsx`
- Run `npx eslint --fix` on the file
- Report any remaining errors via stderr
- Do NOT block the tool (always exit 0) -- linting is advisory

## Step 5: Test Each Hook

For each hook, verify:
1. **Block path**: Trigger the block condition and confirm exit code 2
2. **Allow path**: Trigger the allow condition and confirm exit code 0
3. **Edge cases**: Empty input, missing fields, unusual file paths
4. **Error handling**: What happens when jq is not installed? When prettier is not found?

Testing approach:
```bash
# Test protect-files hook
echo '{"tool_name":"Edit","tool_input":{"file_path":".env"}}' | bash src/hooks/protect-files.sh
echo $?  # Should be 2

echo '{"tool_name":"Edit","tool_input":{"file_path":"src/app.ts"}}' | bash src/hooks/protect-files.sh
echo $?  # Should be 0
```

## Step 6: Production Configuration

Combine all hooks into a production `settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Edit|Write", "hook": "bash src/hooks/protect-files.sh" },
      { "matcher": "Bash", "hook": "bash src/hooks/block-dangerous.sh" }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write", "hook": "bash src/hooks/auto-format.sh" },
      { "matcher": "Edit|Write", "hook": "bash src/hooks/auto-lint.sh" }
    ]
  }
}
```

Compare the development vs production configurations:
- Development: warnings only, fewer blocked patterns
- Production: strict blocking, all guardrails active

## Success Criteria

- [ ] Protected file edits are blocked with clear messages
- [ ] Dangerous commands are caught and blocked
- [ ] Files are auto-formatted after every edit
- [ ] TypeScript files are auto-linted after edits
- [ ] All hooks handle edge cases gracefully
- [ ] Development and production configs are properly differentiated
