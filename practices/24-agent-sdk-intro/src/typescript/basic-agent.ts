/**
 * Practice 24: Basic Agent — Minimal TypeScript agent using Claude Agent SDK
 *
 * This demonstrates the simplest possible agent: a single query() call
 * that sends a prompt and receives a response.
 */

import { Agent } from "@anthropic-ai/claude-agent-sdk";

async function main(): Promise<void> {
  // Create an agent instance
  // The SDK automatically picks up ANTHROPIC_API_KEY from the environment
  const agent = new Agent();

  try {
    // Send a simple query
    const result = await agent.query({
      prompt:
        "List the files in the current directory and briefly describe what each one does.",
      systemPrompt: { preset: "claude_code" },
    });

    // Print the agent's response
    console.log("Agent response:");
    console.log(result.text);

    // Print usage statistics
    console.log("\n--- Usage ---");
    console.log(`Input tokens:  ${result.usage.inputTokens}`);
    console.log(`Output tokens: ${result.usage.outputTokens}`);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

main();
