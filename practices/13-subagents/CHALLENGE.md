# Challenge: Using Subagents

## Step 1: Observe Context Filling

First, perform a large-scale exploration task without a subagent and observe how the context fills up.

### Prompts to Try with Claude

```
Explore the entire project (all files under the practices/ directory),
and summarize the purpose, file structure, and patterns used in each practice.
Check the contents of all .py files.
```

After this task, confirm that the context has been significantly consumed. You can check token usage with the `/cost` command.

---

## Step 2: Use the Built-in Explore Agent

Delegate the same task to a subagent and compare the difference.

### Prompts to Try with Claude

```
Use a subagent to analyze the structure of the practices/ directory.
Delegate the task of summarizing the purpose and file structure of each practice to a subagent.
```

### Comparison Points

- Difference in main context usage between Step 1 and Step 2
- Difference in result quality
- Difference in response time

---

## Step 3: Create Custom Subagents

Create custom agents in the `.claude/agents/` directory.

### 3-1: Researcher Agent

Create `.claude/agents/researcher.md` using `src/example-agents/researcher.md` as a reference.

### Prompts to Try with Claude

```
Using src/example-agents/researcher.md as a reference,
create a .claude/agents/researcher.md agent.

This agent should:
- Explore and analyze the codebase
- Use only Read, Grep, and Glob tools
- Use the haiku model (fast and inexpensive)
- Return results in a structured format
```

After creating it, try using it:

```
Use the @researcher agent to find all classes used in this project.
```

---

## Step 4: Writer/Reviewer Pattern

Practice the pattern where one agent writes code and another agent reviews it.

### Prompts to Try with Claude

First, write the code:
```
Add new endpoints to src/app.py:
- GET /users/:id/stats — Returns user request statistics
- POST /users/:id/preferences — Saves user preferences
- DELETE /users/:id/cache — Deletes user cache

Write tests for each endpoint as well.
```

Then delegate the review:
```
Have a subagent perform a code review of the code you just wrote.
Using the definition in src/example-agents/code-reviewer.md as a reference,
ask it to review from security, performance, and error handling perspectives.
```

---

## Step 5: Code Review Agent with Memory

Create an agent that utilizes project memory.

### Prompts to Try with Claude

```
Using src/example-agents/code-reviewer.md as a reference,
create .claude/agents/code-reviewer.md.

This agent should:
- Specialize in code review
- Remember the project's coding conventions (memory: project)
- Accumulate patterns discovered in previous reviews
- Always apply the security checklist

After creating it, use this agent to review src/app.py.
```

---

## Completion Criteria

- [ ] Step 1: Checked context usage after exploring without a subagent
- [ ] Step 2: Understood the difference when using a subagent for the same task
- [ ] Step 3: Created and used a custom researcher agent
- [ ] Step 4: Separated code writing and review with the Writer/Reviewer pattern
- [ ] Step 5: Created a code review agent with memory

## Reflection Questions

1. Did you feel the context protection benefit when using subagents?
2. What was the difference between having a separate agent review vs. reviewing in the same context in the Writer/Reviewer pattern?
3. Which tasks should be delegated to subagents, and which should be performed directly?
4. Think of at least 3 useful agent definitions that could be shared with your team.
