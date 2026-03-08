# Practice 07: MCP 서버 연동

## Goal

Learn to set up and use MCP (Model Context Protocol) servers with Claude Code. Configure Context7 for live documentation, Playwright for browser automation, and GitHub MCP for repository management.

## Prerequisites

- [Practice 05: CLAUDE.md 작성법](../05-claude-md/)

## Time

30-45 minutes

## Why This Matters

MCP extends Claude's capabilities far beyond code editing. With MCP servers, Claude can:

- **Context7**: Look up real-time documentation for any npm package, framework, or library — no more outdated training data
- **Playwright**: Automate browsers, take screenshots, run E2E tests interactively
- **GitHub**: Create issues, review PRs, manage releases — all from the Claude session

MCP turns Claude from a code editor into a full development environment.

## What You Will Learn

1. What MCP is and how it works
2. Adding MCP servers with `claude mcp add`
3. Configuring MCP in `.mcp.json` for team sharing
4. Using Context7 for live documentation lookup
5. Using Playwright for browser automation
6. Combining multiple MCP servers in a single project

## Directory Structure

```
src/
└── mcp-configs/
    ├── context7.json      # .mcp.json with Context7 only
    ├── playwright.json    # .mcp.json with Playwright only
    ├── full-stack.json    # .mcp.json with multiple servers
    └── README.md          # Detailed server explanations
```

## Key Concepts

### What is MCP?

MCP (Model Context Protocol) is a standard for connecting AI models to external tools and data sources. An MCP server exposes "tools" that Claude can call, just like the built-in Edit, Write, and Bash tools.

### Adding MCP Servers

Two ways to add MCP servers:

**1. CLI command (user-level)**
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

**2. Project `.mcp.json` (team-level, committed to repo)**
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

### When to Use Which Server

| Server | Use When |
|--------|---------|
| Context7 | You need current docs for a library (not what Claude was trained on) |
| Playwright | You need to interact with a browser (E2E testing, screenshots) |
| GitHub | You want to manage issues/PRs/releases from Claude |
