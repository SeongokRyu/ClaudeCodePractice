# Multi-Agent Systems

---

## Core Concept

Claude Code provides a 3-tier multi-agent mechanism:

```
Complexity (high)
  |  Agent Teams    (independent sessions, direct communication, shared task list)
  |  Subagents      (child agents, return only results to parent)
  |  Skills/Commands (reusable prompts, inline execution)
Complexity (low)                                          Token cost ->
```

---

## 1. Claude Agent SDK

Open-source Python/TypeScript framework. Provides the same infrastructure as Claude Code as a programmable library.

### Basic Usage

**Python:**
```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="Find and fix bugs in auth.py",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

**TypeScript:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Find and fix bugs in auth.py",
  options: { allowedTools: ["Read", "Edit", "Bash"] }
})) {
  console.log(message);
}
```

### Agent Loop
`Context gathering -> Action -> Verification -> Repeat`

---

## 2. Subagents vs Agent Teams

| Dimension | Subagents | Agent Teams |
|-----------|-----------|-------------|
| Context | Own window, returns only results to parent | Own window, fully independent |
| Communication | Reports only to parent | Direct messaging between teammates |
| Coordination | Main agent manages | Autonomous coordination via shared task list |
| Best for | Focused tasks where only results are needed | Complex tasks requiring discussion/debate |
| Token cost | Low (result summary) | High (each teammate = separate instance) |

---

## 3. Subagent Definition

### File-based (`.claude/agents/`)
```markdown
---
name: code-reviewer
description: Quality/security review after code changes
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: plan
---
As a senior code reviewer, review the changes for:
1. Security vulnerabilities
2. Performance issues
3. Maintainability
```

### Key Configuration Fields
| Field | Description |
|-------|-------------|
| `model` | sonnet, opus, haiku, inherit |
| `tools` | Allowed tools list |
| `isolation` | `worktree` for Git worktree isolation |
| `permissionMode` | default, acceptEdits, plan, etc. |
| `maxTurns` | Maximum number of turns |
| `skills` | Skills to preload |
| `memory` | Persistent memory (user/project/local) |
| `background` | Whether to run in background |

### Built-in Subagents
- **Explore**: Haiku model, read-only, optimized for codebase search
- **Plan**: Inherited model, read-only, context gathering for planning
- **General-purpose**: Inherited model, full tools, complex multi-step tasks

---

## 4. Agent Teams (Experimental Feature)

Activation: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

```
+-------------------------------------+
|          TEAM LEAD                   |
|   (main session, task distribution   |
|    and coordination)                 |
+------+----+----+----+---------------+
       |    |    |    |
       v    v    v    v
     Mem1 Mem2 Mem3 Mem4
       |    |    |    |
       +----+----+----+
            |         |
     Shared task list  Mailbox
     (dependency       (direct
      tracking)        messaging)
```

### How to Start
```text
Create an agent team:
- Member 1: Analyze from a UX perspective
- Member 2: Analyze technical architecture
- Member 3: Play devil's advocate
```

### Team-specific Hooks
- `TeammateIdle`: When a teammate becomes idle (exit 2 to keep them working)
- `TaskCompleted`: When a task is completed (exit 2 to reject completion)

---

## 5. 6 Core Multi-Agent Patterns

### Pattern 1: Writer/Reviewer
```
Writer -> Write code -> Reviewer -> Review/feedback -> Writer -> Revise -> ...
```
Implementation agent + read-only review agent. Eliminates human review wait time.

### Pattern 2: Specialist Team
```
Team Lead -> Security reviewer + Performance reviewer + Test coverage reviewer (parallel)
```
Each reviewer examines from a different perspective simultaneously. Lead synthesizes results.

### Pattern 3: Competing Hypotheses
```
Team Lead -> Hypothesis1 + Hypothesis2 + Hypothesis3 + Hypothesis4 + Hypothesis5 (parallel)
           -> Debate and refute each other -> Reach consensus
```
Overcomes anchoring bias. Adversarial discussion converges quickly on root causes.

### Pattern 4: Cross-Layer
```
Frontend agent | Backend agent | Test agent
Each owns their file domain, communicates via API contracts
```

### Pattern 5: Verification Subagent
```
Main agent -> Output -> Verification agent -> pass/fail + feedback -> Main
```
The most universally useful pattern. Avoids the "telephone game" problem.

### Pattern 6: Scatter-Gather
```
Lead -> Researchers 1-5 (parallel WebSearch) -> Collect results -> Comprehensive report
```
Opus Lead + Sonnet subagent combination improves 90.2% over single Opus.

---

## 6. Command -> Agent -> Skill Pattern

3-tier separation of concerns:

```
Layer 1: Commands (.claude/commands/)
  User entry point, parameter collection, delegate to agents, ZERO business logic

Layer 2: Agents (.claude/agents/)
  Autonomous execution context, data processing, skill preloading, state maintenance

Layer 3: Skills (.claude/skills/)
  Reusable units of knowledge, domain expertise, progressive disclosure
```

**Design Principles**:
- Commands only orchestrate, no data processing
- Agents do not spawn other Agents (only Commands orchestrate)
- Skills are atomic -- they do one thing well

---

## 7. Worktree Parallel Execution

```
main repo (branch: main)
  +-- worktree-1/ (branch: agent-1-auth)     <- Agent 1
  +-- worktree-2/ (branch: agent-2-api)      <- Agent 2
  +-- worktree-3/ (branch: agent-3-frontend)  <- Agent 3
```

Even the same file can be edited simultaneously with different approaches. No conflicts.

```markdown
---
name: refactor-agent
isolation: worktree
tools: Read, Write, Edit, Bash, Glob, Grep
---
```

---

## 8. Building Production Multi-Agent Systems

### Project Structure
```
.claude/
  agents/
    researcher.md     # Exploration/investigation
    implementer.md    # Implementation
    reviewer.md       # Review
    tester.md         # Testing
  skills/
    coding-conventions/SKILL.md
    error-handling/SKILL.md
  commands/
    build-feature.md  # Orchestration entry point
  agent-memory/
    reviewer/MEMORY.md  # Pattern accumulation
CLAUDE.md
```

### Building CI/CD Pipeline with SDK
```python
async def build_feature(description: str):
    async for msg in query(
        prompt=f"Build feature: {description}",
        options=ClaudeAgentOptions(
            setting_sources=["project"],  # Load .claude/ settings
            agents={
                "researcher": AgentDefinition(
                    tools=["Read", "Glob", "Grep"],
                    model="haiku",
                ),
                "implementer": AgentDefinition(
                    tools=["Read", "Write", "Edit", "Bash"],
                    model="sonnet",
                ),
                "reviewer": AgentDefinition(
                    tools=["Read", "Glob", "Grep"],
                    model="inherit",
                ),
            },
        ),
    ):
        if hasattr(msg, "result"):
            print(msg.result)
```

---

## 9. Decision Framework

```
Simple/single-domain task? -> Single agent
  | NO
Need communication between agents? -> NO -> Subagents
  | YES
Need discussion/debate? -> NO -> Subagents (sequential chaining)
  | YES
Agent Teams (shared tasks, mailbox)
```

### Core Principles
1. **Start with a single agent**, add complexity only when needed
2. **Verification subagent** is the most universally useful
3. **File ownership** prevents conflicts (or use worktree isolation)
4. **Decompose by context boundaries**, not problem types -- use independent information paths
5. **80% planning, 20% execution** -- good specs produce good agent output
