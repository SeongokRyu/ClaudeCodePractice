/**
 * Practice 24: Tool-Restricted Agent (TypeScript)
 *
 * Demonstrates limiting agent capabilities using allowedTools
 * and disallowedTools for safety and role separation.
 */

import { Agent } from "@anthropic-ai/claude-agent-sdk";

/**
 * Read-only agent: can only use Read, Glob, Grep.
 * Cannot modify files or run shell commands.
 */
async function readOnlyAgent(targetPath: string): Promise<string> {
  const agent = new Agent();

  const result = await agent.query({
    prompt: `Analyze the code in ${targetPath}. Report on structure, patterns, and potential issues.`,
    allowedTools: ["Read", "Glob", "Grep"],
    systemPrompt: {
      content:
        "You are a code analyst. You can only read and search files. " +
        "Provide detailed analysis without making any changes.",
    },
  });

  return result.text;
}

/**
 * Safe agent: can do most things except run shell or write files.
 * Uses disallowedTools to blacklist dangerous operations.
 */
async function safeAgent(targetPath: string): Promise<string> {
  const agent = new Agent();

  const result = await agent.query({
    prompt: `Review the code in ${targetPath} and suggest improvements.`,
    disallowedTools: ["Bash", "Write", "Edit"],
    systemPrompt: {
      content:
        "You are a code reviewer. You cannot modify files or run commands. " +
        "Provide your review as structured feedback.",
    },
  });

  return result.text;
}

/**
 * Security auditor: combined allowed + disallowed restrictions.
 */
async function securityAuditor(targetPath: string): Promise<string> {
  const agent = new Agent();

  const result = await agent.query({
    prompt: `Search for security issues in ${targetPath}.`,
    allowedTools: ["Read", "Glob", "Grep", "Bash"],
    disallowedTools: ["Bash"], // Further restrict from allowed set
    systemPrompt: {
      content:
        "You are a security auditor. Search for common vulnerabilities: " +
        "SQL injection, XSS, hardcoded secrets, insecure dependencies.",
    },
  });

  return result.text;
}

async function main(): Promise<void> {
  const target = process.argv[2] || ".";

  console.log("=".repeat(60));
  console.log("1. Read-Only Agent (allowedTools: Read, Glob, Grep)");
  console.log("=".repeat(60));
  const readOnlyResult = await readOnlyAgent(target);
  console.log(readOnlyResult);

  console.log("\n" + "=".repeat(60));
  console.log("2. Safe Agent (disallowedTools: Bash, Write, Edit)");
  console.log("=".repeat(60));
  const safeResult = await safeAgent(target);
  console.log(safeResult);

  console.log("\n" + "=".repeat(60));
  console.log("3. Security Auditor (combined restrictions)");
  console.log("=".repeat(60));
  const securityResult = await securityAuditor(target);
  console.log(securityResult);
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
