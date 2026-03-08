# Challenge: Hooks 설정

## Step 1: Read the Example Hooks

Review all files in `src/hooks-examples/`:

1. `protect-files.sh` — How does it decide which files to block?
2. `auto-format.sh` — When does it run and on which tools?
3. `notify.sh` — How does it detect the operating system?
4. `settings-example.json` — How are hooks registered?

Read `src/hooks-examples/README.md` for detailed explanations.

Questions to answer:
- What exit code blocks a tool call?
- What data does a hook receive on stdin?
- Can a PostToolUse hook block an action?

---

## Step 2: Set Up File Protection Hook

Navigate to the practice project:
```bash
cd practices/06-hooks/src/practice-project
```

Set up a PreToolUse hook that prevents Claude from editing `.env` files:

1. Create `.claude/settings.json` in the practice project (use `settings-example.json` as reference)
2. Copy `protect-files.sh` to the practice project's `.claude/hooks/` directory
3. Make it executable: `chmod +x .claude/hooks/protect-files.sh`
4. Configure the hook in settings.json to run on `Edit` and `Write` tools

Test it:
```
# Start Claude in the practice project
claude

# Ask Claude to create a .env file
> Create a .env file with DATABASE_URL=postgres://localhost/mydb

# The hook should block this with an error message
```

---

## Step 3: Set Up Auto-Format Hook

Add a PostToolUse hook that runs Prettier after every Edit or Write operation:

1. Copy `auto-format.sh` to `.claude/hooks/`
2. Add the PostToolUse hook to your settings.json
3. Make sure it only triggers on `Edit` and `Write` tools

Test it:
```
# Ask Claude to write some messy TypeScript
> Write a function in src/utils.ts with inconsistent formatting

# After Claude writes the file, the hook should auto-format it
# Check the file — it should be properly formatted
```

---

## Step 4: Set Up Notification Hook

Add a Notification hook for desktop alerts:

1. Copy `notify.sh` to `.claude/hooks/`
2. Add the Notification hook to your settings.json
3. The script auto-detects macOS (osascript) vs Linux (notify-send)

Test it:
```
# Ask Claude to do a long task
> Read all files in this project and summarize the architecture

# You should receive a desktop notification when Claude has something to tell you
```

---

## Step 5: Test the Full Setup

With all three hooks configured, test the complete setup:

1. Start Claude in the practice project
2. Try to edit `.env.example` — should be blocked
3. Ask Claude to write a new TypeScript file — should be auto-formatted
4. Ask Claude a question — should trigger a notification

Verify your settings.json has all three hooks properly configured.

---

## Bonus: Custom File Protection

Modify `protect-files.sh` to also protect:
- `*.lock` files (package-lock.json, yarn.lock, pnpm-lock.yaml)
- Any file in a `generated/` directory
- `tsconfig.json` (to prevent Claude from modifying compiler settings)

---

## Success Criteria

You have completed this practice when:
- [x] You can explain the difference between PreToolUse and PostToolUse hooks
- [x] You have a working file protection hook that blocks .env edits
- [x] You have a working auto-format hook
- [x] You understand exit code 0 (allow) vs exit code 2 (block)
- [x] Your settings.json correctly configures all three hook types
