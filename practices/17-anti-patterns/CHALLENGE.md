# Challenge: Experiencing the 7 Common Mistakes

## Step 1: Blind Trust — Uncritical Acceptance

### The Wrong Way

Ask Claude the following:

```
Check the deepMerge function in src/anti_pattern_1_blind_trust.py.
Does it work well?
```

Claude will probably say "it works fine" or only mention minor improvements.

### Discovering Hidden Problems

Now ask the following:

```
Intensively analyze whether there are security vulnerabilities
in the deepMerge function in src/anti_pattern_1_blind_trust.py.
Specifically check if Prototype Pollution attacks are possible.
```

### Verify Yourself

Run the "Blind Trust" tests in `src/test_anti_patterns.py`:

```bash
uv run pytest src/test_anti_patterns.py -k "BlindTrust"
```

### Lesson

- Even if Claude says "no problem," separate verification from a security perspective is essential
- **Providing specific perspectives** improves Claude's analysis quality
- "Check it" vs "Check if Prototype Pollution is possible" yields different results

---

## Step 2: Kitchen Sink Session

### The Wrong Way

Request the following 5 things consecutively in a single Claude session:

```
1. "Design a data model for a simple TODO app"
2. "Explain the differences in state management between React and Vue"
3. "Write a Docker compose file"
4. "Add user authentication to the TODO app created earlier"
5. "Create a web scraper in Python"
```

### Observation

Check whether Claude accurately remembers the details of the TODO app from request #1 when processing request #4. The context will likely be blurred.

### The Correct Way

```bash
# Use independent sessions for each task
claude  # Session 1: TODO app only
claude  # Session 2: Docker setup only

# Or when switching tasks in the same session
> /clear
> Starting a new task now. Please write a Docker compose file.
```

### Lesson

- One session = one related task
- Use `/clear` to reset context when switching tasks
- 5 unrelated tasks → 5 sessions

---

## Step 3: Over-specified CLAUDE.md

### The Wrong Way — 200-line CLAUDE.md

Try using a long CLAUDE.md like this:

```markdown
# Rules (Don't actually create this file — just think about it)

1. Always use camelCase
2. Always add JSDoc to every function
3. Never use var
4. Always use const over let
5. Maximum line length is 80 characters
6. Use 2 spaces for indentation
7. Always use semicolons
8. No trailing commas
9. Use single quotes
10. Always use strict equality
... (190 more lines)
```

When you have Claude write code, many rules will be ignored.
Putting 200 rules in the context scatters Claude's attention.

### The Correct Way — 30-line CLAUDE.md

```markdown
# Project Rules

## Code Style
- Python type hints throughout
- Prefer dataclasses, avoid Any
- Functions under 20 lines

## Testing
- pytest for testing
- Test file: test_*.py

## Git
- Conventional commits
- PR required for main
```

### Experiment

Request the same task with both CLAUDE.md versions and compare rule compliance rates.

### Lesson

- CLAUDE.md is optimal at 30 lines or fewer
- Include only essential rules (delegate the rest to ruff/mypy)
- "More rules ≠ better code"

---

## Step 4: No Verification — Development Without Testing

### The Wrong Way

```
Create a function that formats currency amounts.
- 1234567.89 → "$1,234,567.89"
- Display up to 2 decimal places
- Display negatives in parentheses: -1234 → "($1,234.00)"
```

Use Claude's generated code as-is.

### Hidden Problem

Check `src/anti_pattern_2_no_verification.py`.
This code compiles and works correctly in most cases, but...

```bash
uv run pytest src/test_anti_patterns.py -k "NoVerification"
```

There's a floating-point problem hidden inside!

### The Correct Way

```
Create a function that formats currency amounts.
Write the tests first, then implement.

Edge cases:
- 0.1 + 0.2 = 0.3 displays correctly
- Very large numbers (Number.MAX_SAFE_INTEGER)
- Very small numbers (0.001)
- NaN, Infinity
```

### Lesson

- Code that "seems to work" without tests is dangerous
- When edge cases are specified, Claude writes more robust code
- TDD workflow prevents this problem proactively

---

## Step 5: Scope Creep — Uncontrolled Expansion

### The Wrong Way

Incrementally add features in a single session:

```
1. "Create a simple TODO app" (good start)
2. "Add user authentication too" (still okay)
3. "Add real-time sync too" (getting complex)
4. "Add team features too" (structure breaks down)
5. "Add a notification system too" (spaghetti code)
6. "Add a calendar view too" (chaos)
```

### Observation

Check the state of the code after the 6th request:
- Is the file structure organized?
- Are concerns separated?
- Are there tests?
- Is the structure easy to add new features to?

### The Correct Way

```
I'm going to build a TODO app that needs these features:
1. Basic CRUD
2. User authentication
3. Real-time sync
4. Team features

First, please design the overall architecture.
Define responsibilities and interfaces for each module,
and suggest an implementation order.
```

Then implement each module in separate sessions.

### Lesson

- Designing the overall structure upfront makes feature additions clean
- "Add one at a time" is worse than "plan everything → implement in stages"
- Implement each feature in an independent session

---

## Step 6: Summarizing the Correct Approaches

Summarize what you learned about each anti-pattern.

Ask Claude the following:

```
Summarize the 5 anti-patterns experienced today.

For each pattern:
1. Symptoms of the wrong approach
2. Why it's a problem
3. The correct approach
4. A one-line summary to remember

Organize as a markdown table.
```

### Final Checklist

- [ ] Blind Trust: Always review Claude's code from a security perspective
- [ ] Kitchen Sink: Perform only one task per session
- [ ] Over-specified: Keep CLAUDE.md under 30 lines
- [ ] No Verification: Always write tests first
- [ ] Scope Creep: Design the overall structure first

---

## Success Criteria

- [ ] Experienced the problems of each anti-pattern firsthand
- [ ] Discovered the hidden security vulnerability (Prototype Pollution)
- [ ] Discovered the floating-point bug
- [ ] Felt the difference between the wrong way and the correct way
- [ ] Summarized the 5 lessons

## Key Takeaways

1. **Trust but verify**: Claude is a tool, not an oracle
2. **Stay focused**: One session, one task
3. **Keep it concise**: Fewer rules are better followed
4. **Test it**: Don't trust code that "seems to work"
5. **Plan it**: Don't pile features without structure
