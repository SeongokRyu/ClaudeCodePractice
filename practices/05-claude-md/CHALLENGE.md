# Challenge: Writing CLAUDE.md

## Step 1: Run /init on an Empty Project

Create a temporary empty project and see what Claude generates.

```bash
mkdir /tmp/init-test && cd /tmp/init-test
git init
npm init -y
claude
```

Inside Claude, run:
```
/init
```

Examine what Claude generated:
- What sections did it create?
- How long is the file?
- What did it infer from your project structure?

**Takeaway:** `/init` gives you a starting point, but you should always edit it down.

---

## Step 2: Identify Problems in a Bad CLAUDE.md

Open `src/example-bad/CLAUDE.md` and review it critically.

Questions to answer:
1. Which lines state things that are already obvious? (e.g., "use descriptive variable names")
2. Which sections contain information Claude can read from config files?
3. Which parts are too verbose and could be shortened?
4. How many lines is it? Is it within the 200-line guideline?

Write down at least 5 specific lines you would remove and why.

---

## Step 3: Study a Good CLAUDE.md

Open `src/example-good/CLAUDE.md` and compare it to the bad example.

Notice:
- Every line is actionable or non-obvious
- Bash commands are provided, not descriptions
- Conventions are specific, not generic
- Gotchas mention real pitfalls

Questions to answer:
1. What makes this version more effective?
2. Could Claude follow these instructions without ambiguity?
3. Is there anything missing that should be added?

---

## Step 4: Write Your Own CLAUDE.md

Pick a real project you work on (or use a well-known open source project you contribute to).

Write a CLAUDE.md for it following these rules:
- Keep it under 50 lines (aim for 20-30)
- Every line must be either a command or a non-obvious convention
- Do not repeat what is in package.json, tsconfig.json, or similar config files
- Include at least one "gotcha" section

Test your CLAUDE.md against this checklist:
- [ ] Under 200 lines?
- [ ] No generic advice?
- [ ] Specific bash commands included?
- [ ] Non-obvious conventions documented?
- [ ] Gotchas mentioned?

---

## Step 5: Test Your CLAUDE.md

Start a Claude Code session in your project directory with your new CLAUDE.md.

```bash
cd your-project
claude
```

Try these tests:
1. Ask Claude to create a new file — does it follow your naming conventions?
2. Ask Claude to run tests — does it use the exact command from your CLAUDE.md?
3. Ask Claude about a gotcha you documented — does it know about it?

If Claude ignores a rule, your CLAUDE.md might be too long or the rule might be too vague. Revise and test again.

---

## Bonus: Monorepo Pattern

Examine the files in `src/example-monorepo/`:
- Root `CLAUDE.md` has project-wide rules
- `packages/frontend/CLAUDE.md` has React-specific rules
- `packages/backend/CLAUDE.md` has API-specific rules

Claude automatically reads the nearest CLAUDE.md when working in a subdirectory, plus all parent CLAUDE.md files. This means:
- Shared rules go in the root
- Package-specific rules go in package directories
- No duplication needed

---

## Success Criteria

You have completed this practice when:
- [x] You can explain what belongs and what does not belong in CLAUDE.md
- [x] You have written a CLAUDE.md under 50 lines for a real project
- [x] You have tested it and confirmed Claude follows the rules
- [x] You understand the monorepo CLAUDE.md hierarchy
