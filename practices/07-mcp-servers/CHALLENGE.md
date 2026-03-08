# Challenge: MCP Server Integration

## Step 1: Understand MCP

Before adding servers, understand the concept:

**MCP (Model Context Protocol)** is a way to give Claude access to external tools. Think of it as plugins for Claude Code.

- Each MCP server runs as a separate process
- It exposes "tools" that Claude can call
- Tools appear alongside built-in tools (Edit, Write, Bash)
- Configuration lives in `.mcp.json` (project) or `~/.claude/settings.json` (global)

Read the examples in `src/mcp-configs/` to see how different servers are configured.

Questions to answer:
- What is the difference between adding MCP via CLI vs `.mcp.json`?
- When would you use a project-level `.mcp.json` vs user-level config?

---

## Step 2: Add Context7 MCP Server

Context7 provides real-time documentation for npm packages and frameworks.

Add it using the CLI:
```bash
claude mcp add context7 -- npx -y @upstash/context7-mcp@latest
```

Verify it was added:
```bash
claude mcp list
```

You should see `context7` in the list of configured servers.

---

## Step 3: Test Context7

Start a Claude session and test the Context7 integration:

```bash
claude
```

Try these prompts:
```
> Using context7, look up the latest API for zod's z.object() method

> Using context7, what is the current API for Next.js App Router's generateMetadata?

> Using context7, show me the latest Prisma Client query syntax for findMany with relations
```

Compare the answers to what Claude would say without Context7 — the docs should be up-to-date, not from training data.

---

## Step 4: Add Playwright MCP

Playwright MCP lets Claude automate browsers.

Add it:
```bash
claude mcp add playwright -- npx -y @anthropic-ai/mcp-playwright@latest
```

Test it by asking Claude to:
```
> Navigate to https://example.com and take a screenshot

> Open https://jsonplaceholder.typicode.com/posts/1 and read the JSON response
```

Playwright is especially useful for:
- Debugging frontend issues by seeing what the page looks like
- Running E2E test scenarios interactively
- Scraping data from web pages

---

## Step 5: Create a Project .mcp.json

For team sharing, create a `.mcp.json` file in your project root.

1. Review `src/mcp-configs/full-stack.json` for a complete example
2. Create `.mcp.json` in a project of your choice
3. Add the MCP servers your team needs

Example workflow:
```bash
# Copy the full-stack example as a starting point
cp src/mcp-configs/full-stack.json /path/to/your-project/.mcp.json

# Edit it to match your needs
# Commit it to your repo so the whole team benefits
```

When a teammate clones the repo and runs `claude`, the MCP servers will be automatically available (after they approve them).

---

## Bonus: Custom MCP Server

If you are adventurous, explore building a custom MCP server:
- Use the `@modelcontextprotocol/sdk` npm package
- Create a server that exposes your internal API as tools
- Add it to your `.mcp.json`

---

## Success Criteria

You have completed this practice when:
- [x] You can explain what MCP is and why it is useful
- [x] You have added Context7 and verified it returns live docs
- [x] You have added Playwright and taken a screenshot
- [x] You have created a `.mcp.json` for a project
- [x] You understand the difference between CLI-added and project-level MCP servers
