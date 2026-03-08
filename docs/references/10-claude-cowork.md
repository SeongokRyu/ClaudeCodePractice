# Claude Cowork

---

## One-Line Summary

**Cowork** is a **non-developer AI agent mode** within the Claude Desktop app.
If Claude Code is for developers, Cowork is for general knowledge workers.

---

## Core Concept

| Item | Details |
|------|---------|
| **Official Name** | Cowork (mode within Claude Desktop) |
| **Release Date** | 2026.01.12 (Research Preview) |
| **Target Users** | Non-developers -- marketers, planners, analysts, legal, HR, etc. |
| **Key Difference** | Claude Code = terminal-based, for developers / Cowork = GUI-based, for knowledge workers |
| **Common Foundation** | Claude Agent SDK (same architecture) |

---

## Claude Code vs Cowork

| Dimension | Claude Code | Cowork |
|-----------|-------------|--------|
| Interface | Terminal CLI | Claude Desktop GUI |
| Target | Developers | Knowledge workers |
| Work area | Codebase | Documents, spreadsheets, presentations |
| Execution environment | Local terminal | Isolated VM (sandbox) |
| Configuration files | CLAUDE.md, .claude/* | Global/folder-level instructions |
| Extensions | MCP, Skills, Agents, Hooks | Plugins, MCP connectors |
| Team collaboration | Agent Teams | (not yet supported) |

---

## How It Works

1. Claude Desktop app -> Switch to **Cowork tab**
2. Grant access permissions to specific local folders
3. Describe the desired task in natural language
4. Claude develops a plan -> decomposes into subtasks -> executes autonomously
5. Execution occurs inside an isolated VM (security)
6. Review completed results

---

## Key Features

- **Direct local file access**: Read/modify/create files without uploading/downloading
- **Subagent coordination**: Decompose complex tasks into parallel workstreams
- **Professional document generation**: Excel (with formulas), PowerPoint, formatted documents
- **Plugins**: Domain-specific extensions for HR, design, engineering, financial analysis, etc.
- **MCP Connectors**: Google Drive, Gmail, DocuSign, FactSet, etc.
- **Scheduled tasks**: On-demand or automated execution
- **Browser integration**: Web tasks with Claude in Chrome

---

## Release Timeline

| Date | Milestone |
|------|-----------|
| 2026.01.12 | Research Preview (Max, macOS) |
| 2026.01.16 | Expanded to Pro subscribers |
| 2026.01.23 | Expanded to Team/Enterprise |
| 2026.01.30 | Agentic Plugins launch |
| 2026.02.10 | Windows support |
| 2026.02.24 | Enterprise connector update |

---

## Limitations

- No memory between sessions
- Sessions cannot be shared
- Desktop only (no web/mobile support)
- Session ends when app is closed
- Higher token consumption than standard chat
- Compliance workloads not yet supported
- File deletion requires explicit permission

---

## Relevance to Practice

- Cowork is currently outside the scope of Practice (not developer-targeted)
- However, since it is **based on the same Agent SDK**, learning the Agent SDK also helps understand Cowork
- Useful as reference material when explaining Claude usage to non-developer colleagues
- If a "non-developer track" Practice is created in the future, it could be designed based on Cowork
