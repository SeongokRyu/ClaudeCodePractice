# Claude Code Master Guide 2026

- **URL**: https://claudeguide-dv5ktqnq.manus.space/
- **Features**: 28 sections, 120+ practical tips, Korean, single-page app
- **Sources**: Anthropic Docs, paddo.dev, Andrej Karpathy, Simon Willison, Reddit, and 20+ other sources
- **Last Updated**: 2026.02.25

---

## Summary of 28 Sections

### Beginner Sections

**Core Philosophy**
- Intent over Implementation: Define "what/why" and AI handles "how"
- Conductor, not Coder: Act as a conductor
- Trust but Verify: Trust but always verify
- Context Engineering: Structure the environment so the correct answer becomes self-evident

**Golden Workflow**: Explore → Plan → Implement → Commit

**How to Write CLAUDE.md**
- Include: bash commands, style rules, testing methods, branch conventions, architecture decisions, environment variables
- Exclude: Things readable from code, standard language rules, detailed API docs
- Pro Tip: "If I remove this line, will Claude make mistakes?" → If NO, delete it

**7 Major Mistakes**
1. Blind trust (accepting without review)
2. Lack of architecture (spaghetti code)
3. Latent bugs (missing edge cases)
4. Technical debt acceleration (exceeding maintenance capacity)
5. Learning debt (using without understanding)
6. Scope creep (scope bloat)
7. Over-trusting autonomous loops (automating areas requiring judgment)

**10 Golden Principles**
1. Code is worthless. The spec is what matters
2. Plan Before Execute
3. Compact Often (/clear)
4. Keep CLAUDE.md short
5. Delegate to Subagents
6. Parallelize with Git Worktree
7. CLI > MCP (context efficiency)
8. Enforce with Hooks (deterministic)
9. Rewind Freely
10. If you reviewed/tested/understood, it's safe

### Intermediate Sections

**Context Management**
- LLM performance = context window management
- Auto compaction: triggers at ~80%
- HANDOFF.md for cross-session handoffs

**Prompting Techniques**
- Providing verification means is the single highest-leverage action
- Interview technique: Have Claude ask counter-questions to complete the spec
- Structured prompting: Role + Context + Constraints + Expected output + Verification criteria
- Use @ references to explicitly reference only needed files
- Pipe input: `cat error.log | claude`

**Subagents**
- Multitask while protecting the main context
- Match haiku/sonnet/opus to task complexity
- Worktree parallel development
- Writer/Reviewer pattern

**Security Checklist**
- Watch for slopsquatting: AI recommending non-existent packages
- 8 essential security quality gates

**12 Project Recipes**
- SaaS, Chrome extension, REST API, CLI, React Native, landing page, dashboard, AI chatbot, VS Code extension, automation script, Canvas game, ETL pipeline

**20 Prompt Templates** (copy and use directly)

**15 Debugging Master Strategies**
- Key points: Reset contaminated context with /clear, approve designs with Plan Mode, make minimal unit changes

### Advanced Sections

**Agent Teams** (Research Preview)
- Multi-agent team collaboration, Lead agent coordination
- Unlike subagents, team members communicate directly with each other

**Hooks System**
- CLAUDE.md = probabilistic / Hooks = deterministic
- Block protected file edits, auto-format, notifications
- Exit code: 0=continue, 2=block

**8 Multi-Session Workflow Patterns**
1. Writer/Reviewer
2. Specialist team (parallel)
3. Competing prototypes
4. Phased migration
5. TDD Ping-Pong
6. Overnight autonomous work
7. Review pipeline
8. Microservices development

**10 Cost Optimization Tips**
- Best cost optimization: CLAUDE.md + clear prompts + /compact

**MCP Practical Usage**
- Major servers: Context7, Playwright, GitHub, Supabase, PostgreSQL, Notion, Slack, Figma, Exa

**8 AI Code Review Master Patterns**
- Gradual trust level escalation (Level 1~4)
- "AI writes → Human verifies → Tests prove" 3-stage pipeline
