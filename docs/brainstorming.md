# Claude Code Practice - Brainstorming

## Goal

Create a collection of hands-on practice exercises for effectively utilizing Claude Code.
Rather than a simple usage guide, the focus is on Practice-centered content that can be learned through direct experience.

---

## Reference Material Analysis (docs/references/)

| # | Material | Characteristics | Points to Leverage for Practice |
|---|----------|----------------|---------------------------------|
| 01 | [shanraisshan/claude-code-best-practice](references/01-shanraisshan-best-practice.md) | Command→Agent→Skill pattern, weather system example | Orchestration pattern, configuration reference |
| 02 | [Claude Code Master Guide 2026](references/02-claude-master-guide-2026.md) | 28 sections, 120+ tips, Korean | 10 golden rules, 7 major mistakes, 20 prompt templates |
| 03 | [AI Native Camp](references/03-ai-native-camp.md) | Non-developer 7-day camp, Skill-based curriculum | "Learn through Skills" approach, incremental structure |
| 04 | [WikiDocs Claude Code Guide](references/04-wikidocs-claude-code-guide.md) | 25-chapter comprehensive reference | Systematic feature-by-feature guide, troubleshooting |
| 05 | [Anthropic Official Documentation](references/05-anthropic-official-docs.md) | Official Best Practices, Agent SDK | 7 core principles, failure patterns |
| 06 | [Task Automation](references/06-task-automation.md) | headless mode, CI/CD, Hooks, batch processing | Automation patterns, scripting, scheduling |
| 07 | [Multi-Agent Systems](references/07-multi-agent-systems.md) | Agent SDK, Subagents, Agent Teams, 6 patterns | Production multi-agent construction |
| 08 | [Harness Engineering](references/08-harness-engineering.md) | Deterministic control, governance, context engineering | Production-grade agent control system |
| 09 | [Markdown Configuration File Guide](references/09-markdown-config-files.md) | Complete .claude/ structure, all .md config files | Project configuration reference |
| 10 | [Claude Cowork](references/10-claude-cowork.md) | Desktop GUI agent, for non-developers | Non-developer track, shared Agent SDK foundation |

### Core Principles Commonly Emphasized Across Materials
1. **Explore → Plan → Implement → Commit** (repeated across all materials)
2. **Provide verification means** = single highest-leverage action (Anthropic official)
3. **Context window management** = key to performance (/clear, /compact)
4. **Keep CLAUDE.md short, essentials only** (under 200 lines)
5. **Hooks = deterministic** vs CLAUDE.md = probabilistic
6. **Protect context with subagents**
7. **Trust but Verify**

---

## Basic Concepts / Terminology (For Beginners)

> Essential terms to know before starting the Practices. Explanations for those starting from "What is this?"

### What is Claude Code?

**Claude Code** is a **terminal (CLI) based AI coding agent** created by Anthropic.
When you give instructions in natural language as if chatting, Claude reads code, modifies it, and executes commands.
It can be used within IDEs like VS Code or JetBrains, or run directly from the terminal.

### Basic Terminology

| Term | Description |
|------|-------------|
| **CLI** | Command Line Interface. A way to operate the computer using text commands rather than a mouse. Also called a terminal or console. |
| **Prompt** | The instruction/question text sent to Claude. Something like "Find the bug in this file." |
| **Token** | The smallest unit for AI text processing. One Korean character ≈ 2-3 tokens, one English word ≈ 1 token. Directly affects cost and performance. |
| **Context Window** | The total amount of conversation Claude can remember at once (in tokens). Performance degrades when the window fills up. A key constraint in Claude Code usage. |
| **Session** | A single conversation unit with Claude Code. Start with the `claude` command, reset with `/clear`, resume a previous session with `--resume`. |
| **Compaction** | Automatically summarizing previous content to free up context when the conversation gets long. Can be manually triggered with `/compact`. Auto-triggers at ~80% capacity. |

### Claude Code Tools

Claude Code internally invokes **tools** to carry out user instructions.

| Tool | What It Does | Analogy |
|------|-------------|---------|
| **Read** | Reads file contents | Opening a file to view |
| **Edit** | Modifies specific parts of a file | Find and replace |
| **Write** | Creates a new file or overwrites entirely | Save as new file |
| **Glob** | Searches by file name patterns (`*.ts`, `src/**/*.py`) | Searching in file explorer |
| **Grep** | Searches for text within file contents | Ctrl+Shift+F (global search) |
| **Bash** | Executes terminal commands (`uv sync`, `git status`, etc.) | Typing directly in terminal |
| **Agent** | Spawns a separate subagent to perform independent tasks | Delegating work to a colleague |

### Configuration and Customization

| Term | Description |
|------|-------------|
| **CLAUDE.md** | A configuration file placed at the project root. The "project constitution" that Claude automatically reads at the start of every session. Contains coding rules, build commands, notes, etc. |
| **CLAUDE.local.md** | A personal version of CLAUDE.md. Your own settings that are not committed to Git. |
| **Hooks** | Scripts that automatically run before/after specific Claude actions (file modification, command execution, etc.). Rules in CLAUDE.md can be ignored, but Hooks are **100% enforced**. |
| **Skills** | Reusable workflows defined in `.claude/skills/SKILL.md`. Manuals that teach Claude specific task patterns. |
| **Commands** | Slash commands defined in `.claude/commands/`. Invoked with `/my-command`. |
| **MCP** | Model Context Protocol. A standard specification for Claude to communicate with external tools/services (DB, Slack, Figma, etc.). Extends functionality like plugins. |
| **.claudeignore** | A list of files/folders for Claude to ignore. Same syntax as `.gitignore`. Saves tokens by excluding unnecessary files like `node_modules/`, `dist/`, etc. |

### Workflow Related

| Term | Description |
|------|-------------|
| **Plan Mode** | Enter with Shift+Tab. A read-only mode that only creates plans without modifying code. Plan first → Implement after approval. |
| **Subagent** | A child agent spawned internally by Claude. Performs complex investigation tasks in a separate context to protect the main conversation's context. |
| **Agent Teams** | A feature where multiple Claude instances collaborate as a team (experimental). Team members communicate directly and work independently. |
| **Worktree** | Using Git worktree to perform multiple tasks simultaneously in isolated branches. `claude --worktree feature-auth` |
| **Checkpoint** | Save points automatically created by Claude during work. Can revert to a previous state with Esc+Esc or `/rewind`. |
| **HANDOFF.md** | A handover document written when passing a session. Records what was attempted, successes/failures, and remaining tasks so the next session can pick up immediately. |

### Key Slash Commands

| Command | What It Does |
|---------|-------------|
| `/init` | Auto-generate CLAUDE.md (based on project analysis) |
| `/clear` | Reset current conversation (start new session) |
| `/compact` | Compress conversation content (free up context) |
| `/rewind` | Revert to previous checkpoint |
| `/model` | Change model in use (opus/sonnet/haiku) |
| `/permissions` | Configure permissions (allowed tools/domains) |
| `/sandbox` | Enable OS-level isolation |
| `/cost` | Check current session cost |

### Key Shortcuts

| Shortcut | Action |
|----------|--------|
| Shift+Tab | Cycle modes (Normal → Auto-accept → Plan) |
| Esc | Stop current task |
| Esc+Esc | Checkpoint list / revert |
| Ctrl+G | Edit plan in editor |

### Project Configuration File System (.claude/ Directory)

To customize Claude Code for your project, you use various types of markdown/json configuration files.
A well-organized `.claude/` directory significantly improves Claude's performance and consistency.

**Step-by-step Setup (Starting from Scratch)**

```
Level 1 — Minimal (All projects)
  CLAUDE.md                      ← Auto-generated with /init. Project rules.

Level 2 — Standard (Team projects)
  CLAUDE.md
  CLAUDE.local.md                ← Personal settings (gitignore)
  .claude/settings.json          ← Permissions, hook settings
  .claude/rules/*.md             ← Path-specific rules (frontend/backend, etc.)
  .mcp.json                      ← External tool connections

Level 3 — Advanced (Automated projects)
  + .claude/agents/*.md          ← Custom subagents (reviewer, tester, etc.)
  + .claude/skills/*/SKILL.md    ← Reusable workflows (deploy, review, etc.)

Level 4 — Production (Enterprise)
  + Managed policy CLAUDE.md     ← Organization-wide rules (cannot be overridden)
  + Plugin directory              ← Team-specific extension packages
  + agent-memory/                 ← Agent learns across sessions
```

> For detailed fields and examples, see [Markdown Configuration File Guide](references/09-markdown-config-files.md).

### Claude Cowork — AI Agent for Non-Developers

| | Claude Code | Cowork |
|---|-------------|--------|
| Interface | Terminal CLI | Claude Desktop GUI |
| Target Audience | Developers | Knowledge workers (marketers, planners, analysts, etc.) |
| Work Area | Codebase | Documents, spreadsheets, presentations |
| Shared Foundation | Claude Agent SDK | Claude Agent SDK |

**Cowork** is the agent mode of the Claude Desktop app released in January 2026.
It is built on the **same Agent SDK** as Claude Code, but specializes in document/file tasks rather than code.
You grant access to a local folder, give instructions in natural language, and it autonomously executes in an isolated VM.

> This Practice focuses on Claude Code for developers, but understanding the Agent SDK naturally leads to understanding Cowork as well.
> For details, see [Claude Cowork](references/10-claude-cowork.md).

---

## Practice Categories (Redesigned Based on Materials)

### 1. Foundation - Mastering Core Workflows

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 01 | Golden Workflow | Explore→Plan→Implement→Commit cycle | Official, Master Guide | ★☆☆ |
| 02 | Prompting Techniques | Providing verification means, interview techniques, structured prompts | Official, Master Guide | ★☆☆ |
| 03 | Context Management | /clear, /compact, HANDOFF.md, session management | Official, Master Guide | ★☆☆ |
| 04 | Git Workflow | Commits, branches, PR creation, safe Git habits | Master Guide | ★☆☆ |

### 2. Configuration - Mastering Environment Setup

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 05 | Writing CLAUDE.md | /init, include/exclude criteria, under 200 lines, monorepo | Official, shanraisshan | ★★☆ |
| 06 | Hooks Setup | Protected file blocking, auto-formatting, notifications, exit code | Master Guide | ★★☆ |
| 07 | MCP Server Integration | Context7, Playwright, Chrome DevTools setup | shanraisshan, Master Guide | ★★☆ |
| 08 | Creating Skills | Writing SKILL.md, defining reusable workflows | AI Native Camp, shanraisshan | ★★☆ |

### 3. Workflow Patterns - Acquiring Practical Patterns

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 09 | TDD Workflow | Test → Implement → Refactor, Ralph Loop | Master Guide | ★★☆ |
| 10 | Bug Debugging | 15 debugging strategies, root cause analysis | Master Guide | ★★☆ |
| 11 | Code Review | 8 AI code review patterns, expanding trust levels | Master Guide | ★★☆ |
| 12 | Multi-File Refactoring | Large-scale changes, dependency tracking, safe refactoring | Official | ★★★ |

### 4. Advanced - Advanced Usage

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 13 | Using Subagents | Context protection, Writer/Reviewer, parallel tasks | Official, Master Guide | ★★★ |
| 14 | Worktree Parallel Development | claude --worktree, simultaneous development on independent branches | Master Guide | ★★★ |
| 15 | Command→Agent→Skill | Designing and implementing orchestration patterns | shanraisshan | ★★★ |
| 16 | Multi-Session Workflow | 8 patterns (competing prototypes, TDD Ping-Pong, etc.) | Master Guide | ★★★ |

### 5. Anti-patterns & Troubleshooting

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 17 | Experiencing the 7 Major Mistakes | Intentionally experiencing anti-patterns then learning the correct approach | Master Guide | ★★☆ |
| 18 | Security Checklist | Slopsquatting, OWASP Top 10, security quality gates | Master Guide, Official | ★★☆ |

### 6. Task Automation

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 19 | Headless Mode Basics | `claude -p`, pipe input, JSON output, tool restrictions | Official, Automation | ★★☆ |
| 20 | Git Hooks + Claude | pre-commit security checks, auto commit messages, post-commit automation | Automation | ★★☆ |
| 21 | GitHub Actions Automation | Auto PR review with claude-code-action, issue triage | Automation | ★★★ |
| 22 | Batch Processing and Fan-Out | Parallel processing with `/batch`, `xargs -P`, result aggregation | Automation | ★★★ |
| 23 | Scheduling and Cron | `/loop`, Desktop scheduling, GitHub Actions schedule, overnight autonomous tasks | Automation | ★★★ |

### 7. Multi-Agent Systems - Building Multi-Agent Systems

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 24 | Agent SDK Introduction | Building your first agent with Python/TS, query() calls, tool configuration | Multi-Agent | ★★★ |
| 25 | Custom Subagent Design | `.claude/agents/` definition, role-specific tool/model separation | Multi-Agent | ★★★ |
| 26 | Writer/Reviewer Pattern | Building a collaboration pipeline with implementation agent + review agent | Multi-Agent | ★★★ |
| 27 | Agent Teams Practice | Team creation, shared task list, direct communication between team members | Multi-Agent | ★★★ |
| 28 | Scatter-Gather Research System | Lead + multiple research subagents → comprehensive report | Multi-Agent | ★★★ |
| 29 | Production Multi-Agent Pipeline | Command→Agent→Skill 3-tier, role-specific agents, Agent Memory | Multi-Agent, shanraisshan | ★★★ |

### 8. Harness Engineering - Agent Control System

| # | Practice | Key Learning Points | Source | Difficulty |
|---|----------|---------------------|--------|------------|
| 30 | Deterministic Guardrails | File protection with Hooks, blocking dangerous commands, enforcing auto-formatting | Harness | ★★★ |
| 31 | Context Engineering | Designing information environments rather than prompts, selecting minimal high-signal tokens | Harness | ★★★ |
| 32 | Sandboxing and Permission Control | `/sandbox`, filesystem/network isolation, tool whitelisting | Harness, Official | ★★★ |
| 33 | Quality Gate Pipeline | Verification gates, automated testing, LLM-as-judge, output validation | Harness | ★★★ |
| 34 | Agent Monitoring and Logging | Structured logging, error handling, real-time monitoring, failure recovery | Harness | ★★★ |

---

## Practice Session Construction Guide

### Overall Roadmap (5 Phases)

```
Phase 1: Foundation (Practice 01-04)          <- 1-2 days
  "What is Claude Code and how to interact with it"
  Purely conversational. Possible without code.

Phase 2: Configuration (Practice 05-08)       <- 2-3 days
  "Building your own Claude Code environment"
  Hands-on setup of CLAUDE.md, Hooks, MCP, Skills.

Phase 3: Workflow Patterns (Practice 09-18)   <- 3-5 days
  "Patterns used daily in practice"
  TDD, debugging, code review, refactoring + anti-patterns.

Phase 4: Automation (Practice 19-23)          <- 2-3 days
  "Delegating repetitive tasks to Claude"
  headless mode, CI/CD, batch processing, scheduling.

Phase 5: Multi-Agent & Harness (Practice 24-34) <- 5-7 days
  "Production-grade AI agent systems"
  Agent SDK, multi-agent, governance, monitoring.
```

### Practice Session Structure for Each Phase

#### Phase 1-3: Interactive Hands-on (30 min - 1 hour)

```
1. Concept Introduction (5 min)
   - Explain in one paragraph why this is important
   - 3 things you will learn in this Practice

2. Hands-on in a Prepared Environment (15-30 min)
   - Pre-prepared code exists in src/
   - Follow the step-by-step tasks in CHALLENGE.md
   - Example: "Ask Claude to find the bug in this code"

3. Free Practice (10-15 min)
   - Apply learned patterns to your own project
   - Try variations of the tasks

4. Self-Assessment Checklist (5 min)
   - [ ] Have you tried the key commands/patterns?
   - [ ] Have you verified the results?
   - [ ] Can you recognize anti-patterns?
```

#### Phase 4: Automation Hands-on (1-2 hours)

```
1. Scenario Description (10 min)
   - Present a real work scenario
   - Example: "Spending 2 hours daily reviewing PRs"

2. Manual → Automation Conversion (30-45 min)
   - First do it manually
   - Automate the same task with claude -p
   - Package as scripts/Actions

3. Integration Testing (15-30 min)
   - Verify automation works on actual PRs/commits
   - Handle edge cases

4. Production Checklist (10 min)
   - [ ] Is there error handling?
   - [ ] Is cost controlled? (--max-turns)
   - [ ] Are secrets managed securely?
```

#### Phase 5: Multi-Agent & Harness Hands-on (2-4 hours)

```
1. Architecture Design (30 min)
   - Diagram which agents are needed
   - Decide communication methods between agents
   - Allocate tools/permissions/models

2. Agent Definition & Implementation (1-2 hours)
   - Write .claude/agents/, skills/, commands/
   - Or program with Agent SDK
   - Start with a single agent -> gradually expand

3. Harness Construction (30-60 min)
   - Set up guardrails with Hooks
   - Add quality gates
   - Configure logging/monitoring

4. Integration Execution & Verification (30 min)
   - Run the entire pipeline end-to-end
   - Simulate failure scenarios
   - Evaluate output quality

5. Retrospective (15 min)
   - Improvements compared to a single agent
   - Token cost analysis
   - Areas for improvement
```

### Practice Session Design Principles

1. **Always start with "why"**: Start with "why is this needed" rather than how to use the tool
2. **Prepared environment**: Practice code ready in `src/` so no time is wasted on setup
3. **Experience failure first**: Try anti-patterns first, understand why they fail, then learn the correct approach
4. **Incremental complexity**: Easy to hard ordering within each Phase as well
5. **Real deliverables**: After practice, something immediately usable in your own project should remain
6. **Self-verification**: Check your own learning progress with checklists

---

## Design Decisions (Plan)

### Q1. What is the appropriate time for each Practice?

**Decision: Differentiated time per Phase**

| Phase | Time per Practice | Rationale |
|-------|-------------------|-----------|
| Phase 1: Foundation | **20-30 min** | Focused on concept acquisition. Possible conversationally without code. Short repetitions are effective. |
| Phase 2: Configuration | **30-45 min** | Writing configuration files hands-on. Time for trial and error needed. |
| Phase 3: Workflow | **45-60 min** | Hands-on with actual code. TDD/debugging needs time for iteration loops. |
| Phase 4: Automation | **60-90 min** | Includes manual-to-automation conversion process. CI/CD needs setup + verification time. |
| Phase 5: Multi-Agent & Harness | **90-120 min** | Architecture design + implementation + verification. Most complex. Split into sub-tasks. |

**Principle**: Place **interruptible checkpoints** within tasks, without the pressure of "must finish in one sitting."
Each Practice's CHALLENGE.md will have a "minimum goal achieved if you get this far" marker.

---

### Q2. Should we unify on one programming language or use multiple?

**Decision: TypeScript as default + Python as supplement (Phase 5)**

| Phase | Language | Reason |
|-------|----------|--------|
| Phase 1-4 | **TypeScript** | Claude Code itself is TS-based. Rich web ecosystem examples. Natural to use tool chains like `uv run`, `pytest`, `ruff`. |
| Phase 5 | **TypeScript + Python** | Agent SDK supports both. Python has high real-world usage. Experiencing both is valuable. |

**Reasons**:
- Claude Code's tools (Bash, Read, Edit, etc.) are language-agnostic, but having practice code is more effective
- Unifying on one language minimizes environment setup burden (just need `uv` to start, dependency management with `pyproject.toml`)
- Agent SDK in Phase 5 has richer Python examples, and Python is natural for data/ML engineers

**Prerequisites**: uv, Python 3.10+, Git.

---

### Q3. Is a preparation guide needed so beginners can start right away?

**Decision: YES -- Create a separate `docs/getting-started.md`**

Content to include:
```
1. Environment Check (3 min)
   - Verify uv installation: uv --version
   - Verify Python 3.10+ installation: python --version
   - Verify Git installation: git --version
   - Editor: VS Code recommended (Claude Code extension support)

2. Claude Code Installation (5 min)
   - curl -fsSL https://claude.ai/install.sh | bash  (macOS/Linux)
   - irm https://claude.ai/install.ps1 | iex           (Windows)
   - Verify with claude --version

3. Authentication Setup (3 min)
   - Run claude -> follow the login instructions
   - API key or Claude subscription required

4. First Conversation (5 min)
   - mkdir practice-test && cd practice-test
   - claude
   - "Hello, create a hello.ts file in this directory"
   - Verify it works then /clear

5. Clone This Practice Repo (2 min)
   - git clone <repo-url>
   - cd ClaudeCodePractice
```

**Principle**: From installation to first conversation should be completable **within 15 minutes**.

---

### Q4. Should there be dependencies between Practices, or should they be independent?

**Decision: Sequential between Phases, independent within Phases (Hybrid)**

```
Phase 1 --> Phase 2 --> Phase 3 --> Phase 4 --> Phase 5
(sequential) (sequential) (sequential) (sequential) (sequential)

Within a Phase:
+- Practice 01 (required prerequisite)
+- Practice 02 (independent)
+- Practice 03 (independent)
+- Practice 04 (independent)
```

**Specific dependencies**:

| Practice | Required Prerequisites | Reason |
|----------|----------------------|--------|
| 01 (Golden Workflow) | None | Foundation of everything |
| 05 (CLAUDE.md) | 01 completed | Must know the workflow to write rules |
| 09-18 (Workflow) | 05 completed | Meaningful only when practicing in a project with CLAUDE.md |
| 19-23 (Automation) | 01, 05 completed | Headless mode assumes basic understanding |
| 24-29 (Multi-Agent) | 05, 08, 13 completed | Requires foundational understanding of Skills and Subagents |
| 30-34 (Harness) | 06, 24 completed | Requires Hooks basics + Agent SDK understanding |

**Stated in each Practice README.md**:
```markdown
## Prerequisites
- [x] Practice 01 (Golden Workflow) completed
- [x] Practice 05 (CLAUDE.md) completed
```

---

### Q5. Should we create a Skill-based curriculum like AI Native Camp?

**Decision: Document-based main + Skill as supplement (Hybrid)**

**Reasons for choosing document-based as the main approach**:
- Skill-based requires Claude Code to be installed just to view the curriculum itself
- Low accessibility since README cannot be read directly on GitHub
- Markdown is easier to review when contributors send PRs

**How to use Skills as a supplement**:
```
practice-01-golden-workflow/
├── README.md           # Main curriculum (readable directly on GitHub)
├── CHALLENGE.md        # Practice tasks
├── src/                # Practice code
└── .claude/
    └── skills/
        └── practice-01/
            └── SKILL.md  # "Work through this Practice with Claude"
```

**SKILL.md role**: Running `/practice-01` switches Claude into tutor mode for step-by-step guidance.
AI Native Camp's "learn how to create Skills through a Skill" approach is utilized in Phase 2 Practice 08.

---

### Q6. Should there be a separate track for non-developers?

**Decision: NO -- This repo is for developers only. Non-developers are directed to Cowork.**

**Reasons**:
- Claude Cowork has already been released as a dedicated agent for non-developers (January 2026)
- Teaching terminal-based Claude Code to non-developers is inefficient
- Managing two tracks in one repo only increases complexity

**Instead**:
- Write a single page in `docs/for-non-developers.md` with Cowork guidance + recommended resource links
- Add one line in Practice 01 README.md: "If you're a non-developer -> Cowork is recommended"

**Target user clarification**:
> This Practice is a collection of hands-on exercises for **developers with programming experience**
> to effectively use Claude Code in real work. If you have no coding experience, we recommend [Claude Cowork](https://claude.com/product/cowork).

---

## Each Practice Folder Structure (Draft)

```
practice-XX-name/
├── README.md        # Goals, background, learning points
├── CHALLENGE.md     # Practice tasks (step-by-step)
├── src/             # Source code for practice
├── tests/           # Test code (when needed)
└── solution/        # Reference solution (optional)
```

---

## Additional Content Ideas (Discovered from Materials)

- **Cheat sheet**: Summary of Claude Code key commands/shortcuts/patterns
- **Anti-pattern collection**: 7 major mistakes + 5 failure patterns in detail
- **20 prompt templates**: Excerpted from the Master Guide (copy and use immediately)
- **12 project recipes**: Real-world project guides for SaaS, CLI, Chrome extensions, etc.
- **Cost optimization guide**: 10 strategies
- **Comparison experiments**: Comparing results by varying only the prompt for the same task
- **10 golden rules poster**: At-a-glance principles summary
