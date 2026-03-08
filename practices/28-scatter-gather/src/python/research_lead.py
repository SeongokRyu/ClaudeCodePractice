"""
Practice 28: Research Lead Agent

The lead agent decomposes research questions into subtopics
and synthesizes worker findings into comprehensive reports.
"""

import json
import re
from claude_agent_sdk import Agent


class ResearchLead:
    """Lead agent that decomposes questions and synthesizes findings."""

    def __init__(self):
        self.agent = Agent()

    def decompose(self, question: str, num_subtopics: int = 3) -> list[str]:
        """
        Break a research question into independent subtopics.

        Args:
            question: The research question to decompose
            num_subtopics: Target number of subtopics (default 3)

        Returns:
            List of focused research subtopics
        """
        result = self.agent.query(
            prompt=(
                f"Decompose this research question into exactly {num_subtopics} "
                f"independent, focused subtopics for parallel research.\n\n"
                f"Question: {question}\n\n"
                f"Return ONLY a JSON array of strings, each being a focused "
                f"research subtopic. Example:\n"
                f'["subtopic 1", "subtopic 2", "subtopic 3"]\n\n'
                f"Rules:\n"
                f"- Each subtopic should be independently researchable\n"
                f"- Together they should cover the full question\n"
                f"- They should not overlap significantly\n"
                f"- Each should be specific enough for a single worker"
            ),
            disallowed_tools=["Bash", "Write", "Edit"],
        )

        # Parse the JSON array from the response
        try:
            # Try to extract JSON array from the response
            json_match = re.search(r"\[.*\]", result.text, re.DOTALL)
            if json_match:
                subtopics = json.loads(json_match.group())
                return subtopics[:num_subtopics]
        except json.JSONDecodeError:
            pass

        # Fallback: split by newlines and clean up
        lines = [
            line.strip().lstrip("0123456789.-) ")
            for line in result.text.strip().split("\n")
            if line.strip() and not line.strip().startswith("#")
        ]
        return lines[:num_subtopics]

    def synthesize(
        self, question: str, findings: list[dict], subtopics: list[str]
    ) -> str:
        """
        Synthesize worker findings into a comprehensive report.

        Args:
            question: The original research question
            findings: List of worker findings (dicts with subtopic, findings, confidence)
            subtopics: The original subtopics assigned to workers

        Returns:
            Comprehensive research report as a string
        """
        # Format findings for the synthesis prompt
        formatted_findings = ""
        for i, (subtopic, finding) in enumerate(zip(subtopics, findings), 1):
            formatted_findings += f"\n### Worker {i}: {subtopic}\n"
            formatted_findings += f"**Confidence:** {finding.get('confidence', 'unknown')}\n"
            formatted_findings += f"**Findings:**\n{finding.get('findings', 'No findings')}\n"
            formatted_findings += f"**Key files:**\n{finding.get('key_files', 'None listed')}\n"
            formatted_findings += "---\n"

        result = self.agent.query(
            prompt=(
                f"You are a research lead synthesizing findings from "
                f"{len(findings)} research workers.\n\n"
                f"## Original Question\n{question}\n\n"
                f"## Worker Findings\n{formatted_findings}\n\n"
                f"## Your Task\n"
                f"Produce a comprehensive research report with:\n\n"
                f"### 1. Executive Summary\n"
                f"2-3 sentences answering the original question.\n\n"
                f"### 2. Key Findings\n"
                f"Bullet points of the most important discoveries.\n\n"
                f"### 3. Detailed Analysis\n"
                f"Organized by subtopic, with cross-references between them.\n\n"
                f"### 4. Patterns Identified\n"
                f"Common themes that appear across multiple subtopics.\n\n"
                f"### 5. Contradictions\n"
                f"Where worker findings disagree or conflict.\n\n"
                f"### 6. Recommendations\n"
                f"Actionable next steps based on the findings.\n\n"
                f"### 7. Confidence Assessment\n"
                f"Rate overall confidence and per-subtopic confidence."
            ),
            disallowed_tools=["Bash", "Write", "Edit"],
        )

        return result.text
