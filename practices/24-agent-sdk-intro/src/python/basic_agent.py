"""
Practice 24: Basic Agent — Minimal Python agent using Claude Agent SDK

This demonstrates the simplest possible agent: a single query() call
that sends a prompt and receives a response.
"""

import sys
from claude_agent_sdk import Agent


def main():
    """Create a minimal agent and send a single query."""

    # Create an agent instance
    # The SDK automatically picks up ANTHROPIC_API_KEY from the environment
    agent = Agent()

    try:
        # Send a simple query
        # The agent will use available tools (Read, Bash, etc.) to fulfill the request
        result = agent.query(
            prompt="List the files in the current directory and briefly describe what each one does.",
            system_prompt={"preset": "claude_code"},
        )

        # Print the agent's response
        print("Agent response:")
        print(result.text)

        # Print usage statistics
        print(f"\n--- Usage ---")
        print(f"Input tokens:  {result.usage.input_tokens}")
        print(f"Output tokens: {result.usage.output_tokens}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
