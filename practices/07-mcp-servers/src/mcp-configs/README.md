# MCP Server Configurations

## What is MCP?

MCP (Model Context Protocol) is a standard protocol for connecting AI models to external tools and data sources. Each MCP server is a separate process that exposes tools Claude can call.

## Configuration Methods

### 1. CLI (User-Level)

```bash
claude mcp add <server-name> -- <command> <args...>
```

This adds the server to your personal `~/.claude/settings.json`. Only you have access.

### 2. Project `.mcp.json` (Team-Level)

Create a `.mcp.json` file in your project root and commit it to the repository. When teammates run `claude` in the project, they will be prompted to approve the MCP servers.

## Available Servers

### Context7 (`context7.json`)

**What it does:** Provides real-time, up-to-date documentation for npm packages, frameworks, and libraries. Instead of relying on Claude's training data (which may be outdated), Context7 fetches the latest docs.

**When to use:**
- You are using a library that has changed significantly since Claude's training cutoff
- You need the exact current API signature for a function
- You want to verify that Claude's suggestion matches the latest version

**Example prompts:**
```
Using context7, show me the latest API for React Server Components
Using context7, what changed in Prisma 6.x client API?
```

**Config:** See `context7.json`

### Playwright (`playwright.json`)

**What it does:** Gives Claude the ability to control a browser — navigate to URLs, click elements, fill forms, take screenshots, and read page content.

**When to use:**
- Debugging a frontend issue by visually inspecting the page
- Running E2E test scenarios interactively
- Scraping structured data from a website
- Verifying that a UI change looks correct

**Example prompts:**
```
Navigate to localhost:3000 and take a screenshot
Fill in the login form and submit it
Check if the homepage has any console errors
```

**Config:** See `playwright.json`

### GitHub (`full-stack.json`)

**What it does:** Integrates with GitHub's API to manage repositories, issues, pull requests, and releases directly from the Claude session.

**When to use:**
- Creating or updating GitHub issues from code analysis
- Reviewing PR diffs and leaving comments
- Creating releases with changelogs
- Managing project boards

**Setup:** Requires a `GITHUB_TOKEN` environment variable with appropriate permissions.

**Config:** See `full-stack.json` (part of the multi-server configuration)

## Combining Multiple Servers

You can configure multiple MCP servers in a single `.mcp.json`. See `full-stack.json` for an example with all three servers.

Each server runs as an independent process. They do not interfere with each other, and Claude can use tools from any of them in the same session.

## Tips

1. **Start with Context7** — it is the most universally useful server
2. **Use `.mcp.json` for team projects** — so everyone gets the same tools
3. **Use CLI for personal servers** — tools you use across all projects
4. **Check `claude mcp list`** to see all configured servers
5. **MCP servers start on demand** — they do not run until Claude needs them
