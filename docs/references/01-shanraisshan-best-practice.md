# shanraisshan/claude-code-best-practice

- **URL**: https://github.com/shanraisshan/claude-code-best-practice
- **Stars**: 12.4k | **License**: MIT
- **Features**: A collection of best practices centered on real-world examples. Demonstrates the Command/Agent/Skill pattern using a weather system.

---

## Core Content Structure

### Best Practice Documents
| File | Content |
|------|---------|
| claude-commands.md | Command frontmatter, string substitution, invocation methods, all built-in slash commands |
| claude-subagents.md | Subagent frontmatter, 6 built-in agent types |
| claude-skills.md | Skill frontmatter, 2 patterns (skill vs agent skill), invocation/scope |
| claude-memory.md | CLAUDE.md loading mechanism (upward/downward/lazy), monorepo scenarios |
| claude-settings.md | 55+ settings, 140+ environment variables |
| claude-mcp.md | Recommended MCP servers (Context7, Playwright, Chrome, DeepWiki, Excalidraw) |
| claude-cli-startup-flags.md | Complete CLI startup flag reference |

### Orchestration Workflow
**Command -> Agent -> Skill Pattern**
- Command: User entry point (slash commands)
- Agent: Task coordinator (model/tool selection)
- Skill: Execution unit (concrete task execution)

### Development Workflows
- **Cross-Model Workflow**: Claude Code + Codex (Plan → QA Review → Implement → Verify)
- **RPI Workflow**: Research → Plan → Implement (with verification gates)

### Reports (In-Depth Analysis)
- Agent SDK vs CLI system prompt comparison
- Browser automation MCP comparison (Chrome DevTools vs Playwright)
- Skills discovery mechanism in monorepos
- Agent Memory internals
- Programmatic Tool Calling (PTC), Dynamic Filtering
- Usage/Rate Limits guide
- LLM daily performance variation analysis

### Tips
- Boris Cherny's 12 customization tips (2026.02)

---

## Key Excerpts

### Orchestration Pattern (Most Important)
```
User → /command execution
  → Agent invocation (model/tool decision)
    → Skill execution (concrete task)
      → Result returned
```

### CLAUDE.md Loading Order (Monorepo)
1. **Upward loading**: Auto-loads all CLAUDE.md files from current directory up to root
2. **Downward loading**: Subdirectories are lazy-loaded (only when needed)

### Recommended MCP Server Combination
- **Context7**: Real-time official docs lookup (prevents hallucination)
- **Playwright**: Browser automation, E2E testing
- **Chrome DevTools**: Real-time browser debugging
- **DeepWiki**: GitHub repo analysis
- **Excalidraw**: Diagram generation
