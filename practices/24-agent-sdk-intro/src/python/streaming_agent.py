"""
Practice 24: Streaming Agent

Demonstrates streaming responses from the Agent SDK for real-time output.
Handles different event types: text, tool_use, tool_result, done.
"""

import sys
import time
from claude_agent_sdk import Agent


def streaming_query(prompt: str, verbose: bool = False):
    """
    Send a query and stream the response in real-time.

    Args:
        prompt: The prompt to send to the agent
        verbose: If True, show tool usage details
    """
    agent = Agent()

    tool_count = 0
    text_chunks = 0
    start_time = time.time()

    print(f"Prompt: {prompt}")
    print("-" * 60)

    for event in agent.query_stream(
        prompt=prompt,
        system_prompt={"preset": "claude_code"},
    ):
        if event.type == "text":
            # Print text tokens as they arrive for a real-time effect
            print(event.text, end="", flush=True)
            text_chunks += 1

        elif event.type == "tool_use":
            tool_count += 1
            if verbose:
                print(f"\n  [Tool: {event.tool}({event.input})]", flush=True)
            else:
                print(f"\n  [Using: {event.tool}]", flush=True)

        elif event.type == "tool_result":
            if verbose:
                # Truncate long tool results
                result_preview = str(event.result)[:200]
                print(f"  [Result: {result_preview}...]", flush=True)
            else:
                print(f"  [Done]", flush=True)

        elif event.type == "done":
            elapsed = time.time() - start_time
            print(f"\n\n--- Statistics ---")
            print(f"Time:          {elapsed:.1f}s")
            print(f"Text chunks:   {text_chunks}")
            print(f"Tools used:    {tool_count}")
            if hasattr(event, "usage") and event.usage:
                print(f"Input tokens:  {event.usage.input_tokens}")
                print(f"Output tokens: {event.usage.output_tokens}")
                print(f"Total tokens:  {event.usage.total_tokens}")

        elif event.type == "error":
            print(f"\n[ERROR: {event.error}]", file=sys.stderr)


def main():
    """Run streaming agent with a sample prompt."""
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "Explain the file structure of this project and what each file does."

    try:
        streaming_query(prompt, verbose="--verbose" in sys.argv)
    except KeyboardInterrupt:
        print("\n\nStreaming interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
