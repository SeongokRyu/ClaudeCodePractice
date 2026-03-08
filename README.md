# Claude Code Practice

A collection of hands-on exercises for using Claude Code effectively.

This is not a simple how-to guide, but rather a Practice-oriented collection designed so you can **learn by doing**.

> These Practices are intended for **developers with programming experience**.
> If you have no coding experience, we recommend [Claude Cowork](https://claude.com/product/cowork).

## Getting Started

Follow the [Getting Started](docs/getting-started.md) guide to set up your environment in 15 minutes.

## Roadmap

34 Practices organized in 5 phases.

| Phase | Topic | Practice | Time Required |
|-------|-------|----------|---------------|
| **1. Foundation** | Master core workflows | 01-04 | 20-30 min each |
| **2. Configuration** | Master environment setup | 05-08 | 30-45 min each |
| **3. Workflow Patterns** | Learn practical patterns | 09-18 | 45-60 min each |
| **4. Automation** | Automate tasks | 19-23 | 60-90 min each |
| **5. Multi-Agent & Harness** | Production-grade agent systems | 24-34 | 90-120 min each |

## Phase 1: Foundation

| # | Practice | Key Learning Points | Difficulty |
|---|----------|---------------------|------------|
| 01 | [Golden Workflow](practices/01-golden-workflow/) | Explore→Plan→Implement→Commit cycle | ★☆☆ |
| 02 | [Prompting Techniques](practices/02-prompting-techniques/) | Providing verification means, interview technique, structured prompts | ★☆☆ |
| 03 | [Context Management](practices/03-context-management/) | /clear, /compact, HANDOFF.md, session management | ★☆☆ |
| 04 | [Git Workflow](practices/04-git-workflow/) | Commits, branches, PR creation, safe Git habits | ★☆☆ |

## Phase 2: Configuration

| # | Practice | Key Learning Points | Difficulty |
|---|----------|---------------------|------------|
| 05 | [Writing CLAUDE.md](practices/05-claude-md/) | /init, include/exclude criteria, under 200 lines | ★★☆ |
| 06 | [Hooks Setup](practices/06-hooks/) | Protected file blocking, auto-formatting, notifications | ★★☆ |
| 07 | [MCP Server Integration](practices/07-mcp-servers/) | Context7, Playwright, Chrome DevTools | ★★☆ |
| 08 | [Creating Skills](practices/08-skills/) | Writing SKILL.md, defining reusable workflows | ★★☆ |

## Phase 3: Workflow Patterns

| # | Practice | Key Learning Points | Difficulty |
|---|----------|---------------------|------------|
| 09 | [TDD Workflow](practices/09-tdd-workflow/) | Test→Implement→Refactor, Ralph Loop | ★★☆ |
| 10 | [Bug Debugging](practices/10-bug-debugging/) | 15 debugging strategies, root cause analysis | ★★☆ |
| 11 | [Code Review](practices/11-code-review/) | 8 AI code review patterns, expanding trust levels | ★★☆ |
| 12 | [Multi-File Refactoring](practices/12-multi-file-refactoring/) | Large-scale changes, dependency tracking | ★★★ |
| 13 | [Using Subagents](practices/13-subagents/) | Context protection, Writer/Reviewer, parallel tasks | ★★★ |
| 14 | [Worktree Parallel Development](practices/14-worktree-parallel/) | claude --worktree, simultaneous independent branch development | ★★★ |
| 15 | [Command→Agent→Skill](practices/15-orchestration-pattern/) | Designing and implementing orchestration patterns | ★★★ |
| 16 | [Multi-Session Workflows](practices/16-multi-session/) | Competing prototypes, TDD Ping-Pong, etc. | ★★★ |
| 17 | [Experiencing the 7 Common Mistakes](practices/17-anti-patterns/) | Learning correct methods after experiencing anti-patterns | ★★☆ |
| 18 | [Security Checklist](practices/18-security-checklist/) | Slopsquatting, OWASP Top 10 | ★★☆ |

## Phase 4: Automation

| # | Practice | Key Learning Points | Difficulty |
|---|----------|---------------------|------------|
| 19 | [Headless Mode Basics](practices/19-headless-mode/) | claude -p, pipe input, JSON output | ★★☆ |
| 20 | [Git Hooks + Claude](practices/20-git-hooks-claude/) | Pre-commit security checks, auto commit messages | ★★☆ |
| 21 | [GitHub Actions Automation](practices/21-github-actions/) | Automated PR review, issue triage | ★★★ |
| 22 | [Batch Processing and Fan-Out](practices/22-batch-processing/) | /batch, xargs -P parallel processing | ★★★ |
| 23 | [Scheduling and Cron](practices/23-scheduling/) | /loop, overnight autonomous tasks | ★★★ |

## Phase 5: Multi-Agent & Harness

| # | Practice | Key Learning Points | Difficulty |
|---|----------|---------------------|------------|
| 24 | [Agent SDK Introduction](practices/24-agent-sdk-intro/) | Building your first agent with Python/TS | ★★★ |
| 25 | [Custom Subagent Design](practices/25-custom-subagents/) | .claude/agents/ definitions, role-based separation | ★★★ |
| 26 | [Writer/Reviewer Pattern](practices/26-writer-reviewer/) | Implementation + review agent collaboration pipeline | ★★★ |
| 27 | [Agent Teams Practice](practices/27-agent-teams/) | Team creation, shared task lists | ★★★ |
| 28 | [Scatter-Gather Research System](practices/28-scatter-gather/) | Lead + research subagents → report | ★★★ |
| 29 | [Production Multi-Agent Pipeline](practices/29-production-pipeline/) | Command→Agent→Skill 3-tier | ★★★ |
| 30 | [Deterministic Guardrails](practices/30-deterministic-guardrails/) | File protection with Hooks, blocking dangerous commands | ★★★ |
| 31 | [Context Engineering](practices/31-context-engineering/) | Information environment design, high-signal token selection | ★★★ |
| 32 | [Sandboxing and Permission Control](practices/32-sandboxing/) | /sandbox, filesystem/network isolation | ★★★ |
| 33 | [Quality Gate Pipeline](practices/33-quality-gates/) | Validation gates, LLM-as-judge | ★★★ |
| 34 | [Agent Monitoring and Logging](practices/34-monitoring-logging/) | Structured logging, failure recovery | ★★★ |

## Core Principles

1. **Explore → Plan → Implement → Commit**
2. **Providing verification means** = single highest-leverage action
3. **Context window management** = key to performance
4. **Keep CLAUDE.md short, essential only** (under 200 lines)
5. **Hooks = deterministic** vs CLAUDE.md = probabilistic
6. **Protect context with subagents**
7. **Trust but Verify**

## References

| Resource | Description |
|----------|-------------|
| [Anthropic Official Best Practices](https://code.claude.com/docs/en/best-practices) | Official guide |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | Orchestration patterns |
| [Claude Code Master Guide 2026](https://claudeguide-dv5ktqnq.manus.space/) | 28 sections, 120+ tips |
| [AI Native Camp](https://github.com/ai-native-camp/camp-1) | Skill-based curriculum |
| [WikiDocs Claude Code Guide](https://wikidocs.net/book/19104) | Comprehensive Korean reference |
