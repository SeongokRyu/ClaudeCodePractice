# Harness Engineering Reference

---

## 1. Definition of Harness Engineering

### Core Concept

Harness Engineering is the discipline of designing the infrastructure, constraints, and feedback mechanisms surrounding AI agents. Rather than writing code directly, it is about creating the environment in which AI systems operate within defined guardrails.

**Analogy**: The AI model is the "horse" (powerful but unpredictable), the harness is the "infrastructure" (constraints and feedback loops), and the engineer is the "jockey" (providing direction).

> "2025 was the year of agents. 2026 is the year of agent harnesses. The agent isn't the hard part -- the harness is the hard part."
> -- Aakash Gupta, Medium

### Martin Fowler / Birgitta Boeckeler's Definition

Harness Engineering is the **tools and practices for constraining and maintaining reliability** when AI agents generate code at scale. The term originated from OpenAI's experiment in building codebases of over 1 million lines using only agents.

Core philosophy: **Treat agent failures as signals** -- when an agent struggles, identify the missing elements (tools, guardrails, documentation) and reflect improvements in the codebase.

### Computer Architecture Analogy (Philipp Schmid)

| Concept | Analogy |
|---------|---------|
| Model | CPU -- raw computational power |
| Context Window | RAM -- limited and volatile working memory |
| Agent Harness | Operating System -- context curation, boot sequence, tool handling |
| Agent | Application -- user-specific logic running on top of the OS |

### 4 Core Functions of an Agent Harness

1. **Constrain** what AI agents can do
2. **Inform** agents about what they should do
3. **Verify** that agents did it correctly
4. **Correct** when they did it wrong

---

## 2. 3 Core Components of a Harness

### 2.1 Context Engineering

Ensures that agents access the right information at the right time.

**Static elements:**
- Repository documentation
- `AGENTS.md` / `CLAUDE.md` files
- Verified design specs

**Dynamic elements:**
- Real-time logs, metrics, traces
- Directory structure mapping
- CI/CD status

**Core principle**: Everything the agent needs should be accessible from the repository. Knowledge that exists only in Slack or Google Docs is invisible to the system.

### 2.2 Architectural Constraints

Enforce structural standards **mechanically**, not as suggestions.

- Dependency layering rules
- Custom linters for violation detection
- LLM-based code auditors
- Structural test frameworks
- Pre-commit automation

> **Paradox**: Constraining the solution space makes agents more productive -- by eliminating dead-end exploration.

### 2.3 Entropy Management

Periodic cleanup agents maintain codebase health:

- Documentation consistency verification
- Constraint violation scanning
- Pattern application
- Dependency auditing

---

## 3. Deterministic vs Probabilistic Control

### Fundamental Difference

| Category | Probabilistic Control | Deterministic Control |
|----------|----------------------|----------------------|
| Mechanism | CLAUDE.md, prompts, natural language instructions | Hooks, linters, tests, sandboxes |
| Enforcement | Advisory | Enforced Gates |
| Reliability | Model can ignore it | Physically impossible to bypass |
| Timing | During model reasoning | Before/after model execution |

### Praetorian's "Thin Agent / Fat Platform" Pattern

> "The current 'agentic' approach fails at scale because it relies on probabilistic guidance (prompts) for deterministic engineering tasks."

**Solution -- Invert the traditional architecture:**

- **Agent**: Stateless temporary workers (< 150 lines)
- **Skills**: Domain knowledge, JIT loaded
- **Hooks**: Enforce constraints outside LLM context
- **Orchestration**: Manage specialized role lifecycles

### Constraint-Based Determinism Through Tool Restrictions

Instead of relying on prompt suggestions, **enforce behavior through tool restrictions**:

- **Orchestrator**: Receives only `Task` tool (no Edit) -> physically cannot write code, must delegate
- **Executor**: Receives only `Edit`/`Write` tools (no Task) -> physically cannot delegate, must work
- **Cannot spawn subagents**: Prevents infinite recursion

### Relationship Between CLAUDE.md and Hooks

- CLAUDE.md rules are merely **advisory** without Hooks
- With Hooks, they become **enforced gates**
- `PreToolUse` Hooks: Block actions that require review
- `PostToolUse` Hooks: Run quality checks
- `Stop` Hooks: Verify final output

---

## 4. Claude Code Hooks System -- Harness Mechanism

### 4.1 Full Hook Event Lifecycle

| Event | Trigger Timing |
|-------|---------------|
| `SessionStart` | Session start or resume |
| `UserPromptSubmit` | Prompt submitted, before Claude processing |
| `PreToolUse` | Before tool call execution -- **can block** |
| `PermissionRequest` | When permission dialog is displayed |
| `PostToolUse` | After successful tool call |
| `PostToolUseFailure` | After failed tool call |
| `Notification` | When Claude Code sends a notification |
| `SubagentStart` | When a subagent is spawned |
| `SubagentStop` | When a subagent completes |
| `Stop` | When Claude response is complete |
| `TeammateIdle` | When a teammate agent transitions to idle |
| `TaskCompleted` | When a task is marked complete |
| `InstructionsLoaded` | When CLAUDE.md is loaded |
| `ConfigChange` | When a settings file changes |
| `WorktreeCreate` | When a worktree is created |
| `WorktreeRemove` | When a worktree is removed |
| `PreCompact` | Before context compaction |
| `SessionEnd` | Session end |

### 4.2 Hook Types (4 types)

| Type | Description |
|------|-------------|
| `command` | Execute a shell command |
| `http` | POST to an HTTP endpoint |
| `prompt` | Single-turn LLM evaluation (for decisions requiring judgment) |
| `agent` | Multi-turn verification (with tool access) |

### 4.3 PreToolUse -- The Most Important Harness Mechanism

**Only PreToolUse can block actions.** PostToolUse cannot undo already-executed actions.

**Decision options:**
- `"allow"`: Proceed without permission prompt
- `"deny"`: Cancel tool call, feed reason back to Claude
- `"ask"`: Show permission prompt to user

**Input modification available from v2.0.10:**
- Instead of blocking, intercept and modify tool inputs before execution
- Enables transparent sandboxing, automatic security enforcement, team convention compliance

### 4.4 Core Practical Patterns

#### Protected File Blocking

```bash
#!/bin/bash
# protect-files.sh
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

for pattern in "${PROTECTED_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]]; then
    echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
    exit 2
  fi
done
exit 0
```

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
          }
        ]
      }
    ]
  }
}
```

#### Dangerous Bash Command Blocking

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2
  exit 2
fi
exit 0
```

#### Automatic Code Formatting (PostToolUse)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

#### Context Re-injection After Compaction

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

#### Agent-Based Stop Hook (Test Pass Verification)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

#### Prompt-Based Stop Hook (Task Completion Verification)

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

### 4.5 Hook Storage Locations and Scope

| Location | Scope | Shareable |
|----------|-------|-----------|
| `~/.claude/settings.json` | All projects | No (local) |
| `.claude/settings.json` | Single project | Yes (committable) |
| `.claude/settings.local.json` | Single project | No (gitignored) |
| Managed policy settings | Entire organization | Yes (admin-controlled) |

---

## 5. Sandboxing and Security Boundaries

### 5.1 Claude Code Native Sandboxing

Claude Code provides filesystem and network isolation using OS-level primitives.

**Filesystem isolation:**
- Default: Read/write only to the current working directory
- Read access to the entire computer (except specific denied directories)
- Allow additional paths with `sandbox.filesystem.allowWrite`
- macOS: Seatbelt, Linux: bubblewrap

**Network isolation:**
- Only approved domains are accessible
- Permission prompt for new domain requests
- Applies to all scripts/programs/subprocesses

**Sandbox modes:**
- **Auto-allow mode**: Automatically approves Bash commands within the sandbox
- **Regular permissions mode**: All Bash commands go through the standard permission flow

### 5.2 Production AI Agent Sandboxing Principles

**Zero-Trust Principle**: Treat all AI-generated code as potentially malicious

**Defense-in-Depth:**
1. Isolation Boundaries
2. Resource Limits
3. Network Controls
4. Permission Scoping
5. Monitoring

**Pre-production deployment checklist:**
- Drop `CAP_SYS_ADMIN`
- Zero default network access, implement egress deny lists
- Route necessary traffic through logging proxies
- Assign unique time-limited service accounts to all agent sessions

### 5.3 Isolation Technology Tiers

| Technology | Isolation Strength | Use Case |
|------------|-------------------|----------|
| Firecracker microVMs | Strongest | Production untrusted code |
| Kata Containers | Strong | Hardware-enforced boundaries |
| gVisor | Medium | Kernel call interception |
| Standard containers | Insufficient | Not enough for untrusted code |

---

## 6. "Stop Prompting, Start Governing" Paradigm

### Paradigm Shift

2026 marks the transition from AI agent experimentation to enterprise governance and operational control.

**Key changes:**
- From "encouraging adoption" to "enforcing governance"
- Shifting focus from build time to runtime
- Managing agents is more complex than creating them

> "The goal is not to prevent AI agent usage, but to ensure they operate within a defined 'Trust Sandbox'."

### Enterprise Governance Framework

**Regulatory context (2026):**
- ISO 42001 compliance as baseline
- NIST AI Risk Management Framework
- EU AI Act and DORA in full effect
- Technical debt from AI models treated with same severity as financial errors

**Core governance patterns:**
- Separate systems that build agents from systems that govern them
- Runtime control plane: prompt firewalls, agent Zero Trust, behavioral monitoring
- Fine-grained role-based access, data governance policies, sensitive operation approval workflows

### Failure of Probabilistic Guardrails

> "Current soft guardrails are failing critically. These controls are often probabilistic, pattern-based, or rely on LLM self-evaluation, and are easily bypassed by the core capabilities of agents -- autonomy and composability."

---

## 7. Context Engineering vs Prompt Engineering

### Key Difference

| Category | Prompt Engineering | Context Engineering |
|----------|-------------------|---------------------|
| Focus | What you ask | What the model already knows when it is asked |
| Scope | One-time text instructions | Entire information environment architecture |
| Target | Single LLM call | Multi-step agent interactions |
| Management | Writing instructions | Memory, documentation, tool definitions, conversation history |

### Anthropic Official Guide Core Principles

**Attention Budget Problem:**
- LLMs experience "context rot": information recall accuracy degrades as token volume increases
- Tension between context size and attention due to the transformer's n-squared relationship
- **Treat context as a precious and finite resource**

**System Prompt Structuring:**
- Find the "right altitude" -- specific enough but avoid rigid hardcoding
- Sections delineated by XML tags or Markdown headers:
  - `<background_information>`
  - `<instructions>`
  - `## Tool guidance`
  - `## Output description`

**Tool Design Principles:**
- Must be self-contained and unambiguous
- No functional overlap
- If a human engineer can't confidently say which tool to use, the AI agent can't either

**Runtime Context Retrieval -- Hybrid Approach:**
- Instead of preloading all data, maintain lightweight identifiers (file paths, links)
- Dynamically load information through tools
- Claude Code example: CLAUDE.md is preloaded, grep/glob for runtime exploration

**Long-Running Task Techniques:**
1. **Compaction**: Summarize conversation history, preserve architectural decisions/unresolved bugs/implementation details
2. **Agentic Memory**: Track progress in external files/DBs
3. **Subagent Architecture**: Specialized agents perform focused tasks, return compressed summaries

**Core rule**: Find the smallest high-signal token set that maximizes desired outcomes.

---

## 8. Agent Orchestration Patterns

### 9 Production-Ready Patterns

#### 1. Deterministic State Machine Orchestration
Replace free-form agent decision-making with explicit workflow states. The orchestrator manages valid states; agents make limited choices within those constraints.

#### 2. Supervisor + Specialists Architecture
Instead of one agent handling everything, route to domain-specific specialist agents. Each specialist has reduced tool access, clear policies, and independent ownership.

#### 3. Strict Tool Contracts
Require for all tools:
- Typed input/output schemas
- Idempotency controls
- Permission enforcement
- Rate limits and timeouts

#### 4. Two-Phase Actions (Plan -> Validate -> Execute)
Separate proposal from execution. Agent generates plan -> deterministic policy check -> only approved plans execute.

#### 5. Event-Driven Queue-Backed Workflows
Use asynchronous task queues for long-running tasks. Persistently save workflow state.

#### 6. Model Routing + Fallback
Route requests by task complexity and risk level. Implement fallback chains. Per-request budget control (tokens, tool calls, wall-clock time).

#### 7. Hierarchical Context Management
Separate session context (conversation window) / task state (persistent checkpoints) / system state (policies). Most "memory" failures are actually data governance failures.

#### 8. Structured Escalation Surfaces
Design HITL (Human-in-the-loop) as a product feature, not a safety valve. Show reviewers evidence, proposed plans, and policy checks.

#### 9. Continuous Evaluation + Replay
Golden datasets, regression tests, shadow mode, canary releases. Version control everything (prompts, tools, policies, models).

### Praetorian 16-Step Orchestration State Machine

A strict state machine that all complex workflows follow:

| Phase | Purpose |
|-------|---------|
| 1-4 | Setup, triage, discovery, skill mapping |
| 5-7 | Complexity analysis, design refinement, architecture planning |
| 8-11 | Implementation, verification, compliance, code quality |
| 12-16 | Test planning, testing, coverage verification, completion |

**Intelligent step skipping**: Bug fixes run ~5 steps; new subsystems use all 16 steps.

### 5-Role Development Pattern (Praetorian)

| Role | Responsibility | Output |
|------|---------------|--------|
| Lead | Architecture & strategic decomposition | Architecture Plan |
| Developer | Subtask implementation | Source Code |
| Reviewer | Compliance verification | Review Report |
| Test Lead | Test strategy analysis | Test Plan |
| Tester | Test writing & execution | Test Cases |

---

## 9. Quality Gates and Validation Gates

### Quality Gate Implementation Patterns

**Routing gates vs Git hooks:**
- Git hooks can be skipped by users
- Routing gates are embedded in agent instructions and enforced through transcript evidence

**CI/CD pipeline quality gates:**
- Enforce coding, security, and architecture policies before human review
- Resolve review bottlenecks and standardize feedback

**Task decomposition and verification:**
- Checkpointing, fine-grained verification, parallel execution enabled
- Durable execution handles infrastructure failures
- Validation gates catch AI hallucinations

### Compaction Gates (Praetorian)

Hard blocks that programmatically enforce token hygiene:

| Context Usage | Action |
|--------------|--------|
| < 75% | Proceed |
| 75-85% | Warning |
| > 85% | **Hard block** -- until context compaction runs |

### 3-Level Loop System

**Level 1 (Intra-Task)**: Single agent prevents infinite repetition for shell commands (max 10 iterations)

**Level 2 (Inter-Phase)**: Multi-domain feedback loops enforce implementation -> review -> test cycles

```yaml
modified_domains: ["backend", "frontend"]
domain_phases:
  backend: {review: PASS, testing: PASS}
  frontend: {review: PASS, testing: FAIL}
# Block exit until all domains pass all phases
```

**Level 3 (Orchestrator)**: Re-invoke entire phases when macro goals are unmet

---

## 10. Production Readiness: Reliability, Error Handling, Monitoring

### Four Pillars

#### 1. Structured Logging
- Log every decision point with Correlation IDs
- Tool calls, model decisions, execution results, all errors

#### 2. Multi-Layer Error Handling

| Layer | Error Type | Action |
|-------|-----------|--------|
| 1 | Transient (timeouts, rate limits) | Automatic retry with exponential backoff |
| 2 | LLM-recoverable (wrong parameters) | Return error context to model |
| 3 | User-correctable (authentication, permissions) | Request human intervention |
| 4 | Unexpected | Alert and escalate |

#### 3. Output Validation
Never trust model output:
- Schema validation (Pydantic)
- Semantic checks (confidence thresholds, reasoning quality)
- Tool-specific format validators

#### 4. Real-Time Monitoring
Execution event streaming and tracing:
- Success/error rates by task type
- Latency by phase
- Token usage and cost
- Recovery rates

### Measurable Improvements (Empirical Data)

| Metric | Before | After |
|--------|--------|-------|
| Failure rate | 22% | 2.1% |
| Mean diagnosis time | 3+ days | < 30 min |
| Auto-recovery rate | 0% | 87% |

### Production Readiness Checklist

Required before deployment:
- [ ] Explicit orchestrator states with defined transitions
- [ ] All tool schemas validated and allowlisted
- [ ] Idempotency for operations with side effects
- [ ] End-to-end traces with correlation IDs
- [ ] Golden test sets including adversarial inputs
- [ ] Per-request token/time budget enforcement
- [ ] Shadow/canary release strategy with rollback capability

### Anti-Patterns to Avoid

- Unlimited tool access
- Workflow state that exists only in conversation
- Mega-prompts handling all concerns
- Permissions enforced through prompt language
- No observability layer
- Quality evaluated only by demos
- Dozens of tool integrations without contracts
- Uncontrolled token spending

---

## 11. CNCF's 4 Platform Control Principles (Applied to Agents)

### 1. Golden Paths
Pre-approved configurations and standardized harness setups. Teams inherit rather than independently create.

### 2. Guardrails
"Non-overridable hard policy enforcement. Cost caps, time limits, blocked output patterns, tool allowlists."

### 3. Safety Nets
Auto-recovery mechanisms: retry logic, fallback responses, circuit breakers.

### 4. Manual Review
Human intervention gates for low-confidence or sensitive system-related situations.

**Synergy**: Golden Paths reduce Guardrail surface area, Safety Nets catch what Guardrails miss, Manual Review handles automation edge cases.

---

## 12. Practical Strategy and Implementation Levels

### Implementation Level Roadmap

| Level | Target | Content | Time Required |
|-------|--------|---------|---------------|
| Level 1 | Individual | `.cursorrules`, pre-commit hooks, test suites | 1-2 hours |
| Level 2 | Small team | `CLAUDE.md`, CI-enforced constraints, shared templates | 1-2 days |
| Level 3 | Organization | Custom middleware, observability integration, performance dashboards | 1-2 weeks |

### Key Insights

**LangChain case study**: Modified only the harness while keeping the model identical -> performance improved from 52.8% to 66.5% on Terminal Bench 2.0 -> jumped from Top 30 to Top 5.

**OpenAI results**: Built a 1M+ line production application in roughly 1/10 of normal development time. Zero manually written code. 3 engineers merged ~1,500 PRs (3.5 PRs per engineer per day).

### "Build to Delete" Principle

> "Every new model release brings a different optimal way to structure agents."

Design modular architectures so that when models evolve, yesterday's logic can be quickly removed.

**Competitive advantage**: Companies investing in harness engineering now are building lasting advantages.

---

## 13. Secret Management and Security Patterns

### JIT (Just-In-Time) Injection Pattern (Praetorian)

```
Agent request: run_with_secrets("aws s3 ls")
-> Wrapper spawns child process
-> 1Password injects as ENV variables
-> Command runs in isolated enclave
-> Secrets are neither logged nor contextualized
```

Ensures secrets never enter the LLM context.

### Prompt Injection Defense (Claude Code)

Sandboxing successfully defends against prompt injection attacks:
- **Filesystem**: Cannot modify core files like `~/.bashrc`, `/bin/`, etc.
- **Network**: Cannot exfiltrate data to attacker servers, cannot download scripts from unapproved domains
- **Monitoring**: All boundary testing attempts are blocked at the OS level and immediately alerted

---

## 14. Agent Observability

### Core Metrics

- **Latency**: Measured per task and per individual step
- **Error rate**: Success/failure rates by task type
- **Token usage**: Cost tracking
- **Reasoning quality**: Factual accuracy, decision-making patterns
- **Recovery rate**: Auto-recovery success rate

### Distributed Tracing

Trace agent execution paths from initial prompt through tool calls to final output. Enables precise diagnosis of bottlenecks.

### Tool Ecosystem

- **Langfuse**: Detailed trace collection
- **Arize**: Real-time metric monitoring dashboards
- **LangGraph**: Graph-based approach with fallback paths on failure

---

## 15. Core Summary: The Essence of Harness Engineering

### "The Harness Determines the Product"

> "Two systems using the same model show completely different performance depending on harness quality."

### 5 Key Strategic Lessons

1. **Systems over models**: The base model is becoming less important; the system surrounding it matters more
2. **Constraints enable autonomy**: Giving up flexibility and adopting standardized patterns increases agent autonomy
3. **Deterministic wrapping**: Treat the LLM as a non-deterministic kernel process and wrap it with a deterministic runtime
4. **Feedback loops**: Continuously improve the harness by learning from agent failures
5. **Source of competitive advantage**: True competitive advantage lies not in prompts but in trajectory data captured during execution

---

## Sources

- [Harness Engineering -- Martin Fowler](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html)
- [Harness Engineering: Complete Guide 2026 -- NxCode](https://www.nxcode.io/resources/news/harness-engineering-complete-guide-ai-agent-codex-2026)
- [2025 Was Agents. 2026 Is Agent Harnesses -- Aakash Gupta](https://aakashgupta.medium.com/2025-was-agents-2026-is-agent-harnesses-heres-why-that-changes-everything-073e9877655e)
- [The Importance of Agent Harness in 2026 -- Philipp Schmid](https://www.philschmid.de/agent-harness-2026)
- [What is an Agent Harness -- Parallel AI](https://parallel.ai/articles/what-is-an-agent-harness)
- [Agent Harnesses: Why 2026 Isn't About More Agents -- DEV Community](https://dev.to/htekdev/agent-harnesses-why-2026-isnt-about-more-agents-its-about-controlling-them-1f24)
- [Deterministic AI Orchestration -- Praetorian](https://www.praetorian.com/blog/deterministic-ai-orchestration-a-platform-architecture-for-autonomous-development/)
- [Effective Context Engineering for AI Agents -- Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Claude Code Hooks Guide -- Anthropic](https://code.claude.com/docs/en/hooks-guide)
- [Claude Code Sandboxing -- Anthropic](https://code.claude.com/docs/en/sandboxing)
- [Context Engineering: Why It's Replacing Prompt Engineering -- DEV Community](https://dev.to/serenitiesai/context-engineering-why-its-replacing-prompt-engineering-in-2026-1b4g)
- [Context Engineering vs Prompt Engineering -- Firecrawl](https://www.firecrawl.dev/blog/context-engineering)
- [AI Agent Orchestration Patterns -- Microsoft Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Orchestrating AI Agents in Production -- Hatchworks](https://hatchworks.com/blog/ai-agents/orchestrating-ai-agents/)
- [From Guardrails to Governance -- MIT Technology Review](https://www.technologyreview.com/2026/02/04/1131014/from-guardrails-to-governance-a-ceos-guide-for-securing-agentic-systems)
- [AI Agent Reliability Guide -- BSWEN](https://docs.bswen.com/blog/2026-03-06-agent-reliability/)
- [Top Runtime AI Governance Platforms 2026 -- AccuKnox](https://accuknox.com/blog/runtime-ai-governance-security-platforms-llm-systems-2026)
- [How to Sandbox AI Agents 2026 -- Northflank](https://northflank.com/blog/how-to-sandbox-ai-agents)
- [AI Agent Sandboxing & Progressive Enforcement -- ARMO](https://www.armosec.io/blog/ai-agent-sandboxing-progressive-enforcement-guide/)
- [Agentic AI Governance Frameworks 2026 -- CertMage](https://certmage.com/agentic-ai-governance-frameworks/)
- [Quality Gates -- DeepWiki](https://deepwiki.com/rjmurillo/ai-agents/7.1-skill-architecture-and-frontmatter)
- [AI Code Guardrails -- CodeScene](https://codescene.com/use-cases/ai-code-quality)
- [Taming AI Agents 2026 -- CIO](https://www.cio.com/article/4064998/taming-ai-agents-the-autonomous-workforce-of-2026.html)
