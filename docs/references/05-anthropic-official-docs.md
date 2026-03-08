# Anthropic Official Documentation and Resources

---

## 1. Official Documentation (code.claude.com/docs)

### Best Practices - Key Summary

**Core Constraint**: Performance degrades when the context window fills up. This is the foundation of all Best Practices.

**7 Core Principles**

1. **Provide verification means** (Single highest-leverage action)
   - Never request implementation without tests, screenshots, or expected output
   - Without verification, produces plausible but broken code

2. **Explore → Plan → Code**
   - Separate exploration and execution with Plan Mode (Shift+Tab)
   - Edit plans in the editor with Ctrl+G
   - Unnecessary for trivial tasks

3. **Provide specific context**
   - Specify scope, indicate sources, reference existing patterns, describe symptoms
   - Use @ references, image pasting, URLs, pipe input

4. **Configure the environment**
   - CLAUDE.md: Create with `/init`, keep under 200 lines
   - Permissions: `/permissions` or `/sandbox`
   - CLI tools: Install gh, aws, gcloud, etc.
   - MCP: `claude mcp add`
   - Hooks: Deterministic scripts
   - Skills: `.claude/skills/` SKILL.md
   - Subagents: `.claude/agents/`
   - Plugins: `/plugin`

5. **Communicate effectively**
   - Ask Claude the questions you'd ask a senior engineer
   - For large features, let Claude interview you
   - Start with minimal prompts → let Claude dig into the hard parts

6. **Session management**
   - Esc to interrupt, Esc+Esc or /rewind to restore checkpoint
   - /clear to reset between unrelated tasks
   - /compact for controlled compression
   - Delegate investigation tasks to subagents

7. **Automation and scaling**
   - `claude -p "prompt"` for CI/pre-commit integration
   - Parallel sessions (desktop app, web, Agent Teams)
   - Writer/Reviewer pattern

### Common Failure Patterns
- Kitchen sink session: Mixing unrelated tasks → /clear
- Repeated fixes: Failed approach contamination → /clear and restart
- Excessive CLAUDE.md: Too long gets ignored → prune ruthlessly
- Trust without verification: Deploying broken code → always provide tests
- Endless exploration: Investigation without scope → narrow scope, use subagents

---

## 2. CLAUDE.md and Memory System

### CLAUDE.md Loading Locations (in priority order)
| Location | Scope | Shared |
|----------|-------|--------|
| /Library/.../ClaudeCode/CLAUDE.md (macOS) | Admin policy | Organization |
| /etc/claude-code/CLAUDE.md (Linux) | Admin policy | Organization |
| ./CLAUDE.md or ./.claude/CLAUDE.md | Project | Git |
| ~/.claude/CLAUDE.md | User-wide | No |
| ./CLAUDE.local.md | Project personal | No |

### Other
- `@path/to/file` import syntax
- `.claude/rules/` directory for organizing rules
- `paths:` YAML frontmatter for path-specific rules
- Auto Memory: `~/.claude/projects/<project>/memory/`

---

## 3. Common Workflows

- Codebase exploration, bug fixing, refactoring
- Subagents, Plan Mode, testing
- PR creation/review, documentation
- Image analysis (drag/drop, paste)
- Extended Thinking (`ultrathink` keyword)
- Session management (/rename, /resume, --continue, --from-pr)
- Git Worktree parallel sessions
- Unix pipes: `cat file | claude -p "prompt" > output.txt`

---

## 4. Official GitHub Repositories

| Repository | Stars | Description |
|------------|-------|-------------|
| anthropics/claude-code | 75.1k | Claude Code main repository |
| anthropics/claude-code-action | 6.1k | GitHub Actions PR/issue automation |
| anthropics/claude-plugins-official | - | Official plugin directory |
| anthropics/skills | - | Public Agent Skills |

### claude-code-action Key Features
- Auto-respond to PRs/issues via @claude mention
- Code review, implementation, Q&A
- 9 solution patterns (auto PR review, security review, issue triage, etc.)
- Installation: `/install-github-app`

---

## 5. Sandboxing and Security

- **Sandboxed Bash**: Linux bubblewrap, macOS seatbelt
- Filesystem isolation + network isolation
- 84% reduction in permission prompts
- Activate with `/sandbox` command
- Web version runs in an isolated cloud sandbox

---

## 6. How the Anthropic Team Uses It

- Infrastructure team: Accelerating onboarding (reading codebases, explaining dependencies)
- Product engineering: The "first gateway" for file exploration
- Security engineering: Switching to TDD, 3x faster control flow tracing
- Product design: Figma → code autonomous loop
- Reasoning team: Converting test logic between languages (e.g., Rust)
- Data infrastructure: Diagnosing K8s issues within 20 minutes
- Key takeaway: **Use it as a thinking partner, not a code generator**

---

## 7. Agent SDK

- Framework for building autonomous agents
- Core idea: "Give agents a computer and let them work like humans"
- Feedback loop: Collect context → Act → Verify → Repeat
- Use `systemPrompt: { preset: "claude_code" }`
- CLAUDE.md loading: Must specify `settingSources: ['project']`
