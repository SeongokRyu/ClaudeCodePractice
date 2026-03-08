# Challenge: Agent SDK 입문

## Step 1: Install Agent SDK

Install the Claude Agent SDK in both Python and TypeScript environments.

**Python:**
```bash
uv sync
```

**TypeScript:**
```bash
npm install @anthropic-ai/claude-agent-sdk
```

### Verification
- `python -c "import claude_agent_sdk; print('OK')"` should succeed
- `npx ts-node -e "import '@anthropic-ai/claude-agent-sdk'"` should succeed

---

## Step 2: Build Minimal Agent (Python)

Create a minimal Python agent that makes a `query()` call with a prompt.

**File:** `src/python/basic_agent.py`

### Requirements
1. Import the Agent SDK
2. Create an agent session
3. Send a simple prompt: "List the files in the current directory"
4. Print the agent's response
5. Handle errors gracefully

### Expected Behavior
```
$ python src/python/basic_agent.py
Agent response:
Here are the files in the current directory:
- basic_agent.py
- tool_restricted_agent.py
- streaming_agent.py
```

---

## Step 3: Build Minimal Agent (TypeScript)

Create the same minimal agent in TypeScript.

**File:** `src/typescript/basic-agent.ts`

### Requirements
1. Import the Agent SDK
2. Create an agent session
3. Send a prompt: "List the files in the current directory"
4. Print the response
5. Use async/await properly

---

## Step 4: Add Tool Restrictions

Create agents with explicit tool restrictions.

**Files:**
- `src/python/tool_restricted_agent.py`
- `src/typescript/tool-restricted-agent.ts`

### Requirements
1. Create a **read-only agent** using `allowedTools`:
   - Only allow: `Read`, `Glob`, `Grep`
   - Disallow all write operations
2. Create a **safe agent** using `disallowedTools`:
   - Disallow: `Bash`, `Write`
   - Allow everything else
3. Test that restricted tools are actually blocked

### Key Concepts
```python
# Python - allowedTools
result = agent.query(
    prompt="Analyze the codebase",
    allowed_tools=["Read", "Glob", "Grep"]
)

# Python - disallowedTools
result = agent.query(
    prompt="Review this code",
    disallowed_tools=["Bash", "Write"]
)
```

```typescript
// TypeScript - allowedTools
const result = await agent.query({
  prompt: "Analyze the codebase",
  allowedTools: ["Read", "Glob", "Grep"],
});

// TypeScript - disallowedTools
const result = await agent.query({
  prompt: "Review this code",
  disallowedTools: ["Bash", "Write"],
});
```

---

## Step 5: Add System Prompt Preset

Configure agents with system prompt presets.

### Requirements
1. Use the `claude_code` preset for full coding capabilities
2. Create a custom system prompt for a specialized agent
3. Compare behavior with and without presets

### Key Concepts
```python
# Using preset
result = agent.query(
    prompt="Fix the bug in app.py",
    system_prompt={"preset": "claude_code"}
)

# Using custom system prompt
result = agent.query(
    prompt="Review this PR",
    system_prompt={"content": "You are a senior code reviewer. Focus on security, performance, and maintainability."}
)
```

```typescript
// Using preset
const result = await agent.query({
  prompt: "Fix the bug in app.ts",
  systemPrompt: { preset: "claude_code" },
});

// Using custom system prompt
const result = await agent.query({
  prompt: "Review this PR",
  systemPrompt: {
    content:
      "You are a senior code reviewer. Focus on security, performance, and maintainability.",
  },
});
```

---

## Step 6: Handle Streaming Responses

Implement streaming to get real-time output from the agent.

**File:** `src/python/streaming_agent.py`

### Requirements
1. Use the streaming API to get incremental responses
2. Print tokens as they arrive (real-time effect)
3. Handle different event types (text, tool_use, tool_result)
4. Track total token usage

### Key Concepts
```python
# Streaming in Python
for event in agent.query_stream(
    prompt="Explain the architecture of this project",
    system_prompt={"preset": "claude_code"}
):
    if event.type == "text":
        print(event.text, end="", flush=True)
    elif event.type == "tool_use":
        print(f"\n[Using tool: {event.tool}]")
    elif event.type == "tool_result":
        print(f"[Tool result received]")
    elif event.type == "done":
        print(f"\n\nTotal tokens: {event.usage.total_tokens}")
```

---

## Success Criteria

- [ ] Agent SDK installed in both Python and TypeScript
- [ ] Basic agents work and produce meaningful output
- [ ] Tool restrictions correctly limit agent capabilities
- [ ] System prompt presets change agent behavior
- [ ] Streaming responses display in real-time
- [ ] Error handling is robust (API key missing, network errors, etc.)

## Bonus Challenges

1. **Multi-turn conversation**: Maintain context across multiple `query()` calls
2. **Custom tool**: Register a custom tool the agent can use
3. **Token budget**: Set a max token limit and handle the budget exceeded case
