"""
Practice 24: Tool-Restricted Agent

Demonstrates how to limit agent capabilities using allowedTools
and disallowedTools for safety and role separation.
"""

import sys
from claude_agent_sdk import Agent


def read_only_agent(target_path: str):
    """
    Create an agent that can only read files — no writes, no shell access.

    Uses allowedTools to whitelist only safe, read-only tools.
    """
    agent = Agent()

    result = agent.query(
        prompt=f"Analyze the code in {target_path}. Report on structure, patterns, and potential issues.",
        allowed_tools=["Read", "Glob", "Grep"],
        system_prompt={
            "content": (
                "You are a code analyst. You can only read and search files. "
                "Provide detailed analysis without making any changes."
            )
        },
    )

    return result


def safe_agent(target_path: str):
    """
    Create an agent that can do most things except run shell commands or write files.

    Uses disallowedTools to blacklist dangerous tools while allowing everything else.
    """
    agent = Agent()

    result = agent.query(
        prompt=f"Review the code in {target_path} and suggest improvements.",
        disallowed_tools=["Bash", "Write", "Edit"],
        system_prompt={
            "content": (
                "You are a code reviewer. You cannot modify files or run commands. "
                "Provide your review as structured feedback."
            )
        },
    )

    return result


def combined_restrictions_agent(target_path: str):
    """
    Create an agent with both allowed and disallowed tools.

    allowedTools takes precedence — only whitelisted tools are available,
    and disallowedTools further restricts from that set.
    """
    agent = Agent()

    result = agent.query(
        prompt=f"Search for security issues in {target_path}.",
        allowed_tools=["Read", "Glob", "Grep", "Bash"],
        disallowed_tools=["Bash"],  # Further restrict: remove Bash from allowed set
        system_prompt={
            "content": (
                "You are a security auditor. Search for common vulnerabilities: "
                "SQL injection, XSS, hardcoded secrets, insecure dependencies."
            )
        },
    )

    return result


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."

    print("=" * 60)
    print("1. Read-Only Agent (allowedTools: Read, Glob, Grep)")
    print("=" * 60)
    result = read_only_agent(target)
    print(result.text)

    print("\n" + "=" * 60)
    print("2. Safe Agent (disallowedTools: Bash, Write, Edit)")
    print("=" * 60)
    result = safe_agent(target)
    print(result.text)

    print("\n" + "=" * 60)
    print("3. Combined Restrictions Agent")
    print("=" * 60)
    result = combined_restrictions_agent(target)
    print(result.text)


if __name__ == "__main__":
    main()
