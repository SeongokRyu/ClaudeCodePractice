"""
Practice 28: Research Worker Agent

A worker agent that researches a single subtopic within a codebase.
Workers operate independently and produce structured findings.
"""

import json
import re
from claude_agent_sdk import Agent


class ResearchWorker:
    """Worker agent that researches a single subtopic."""

    def __init__(self, worker_id: int = 0):
        self.worker_id = worker_id
        self.agent = Agent()

    def research(self, subtopic: str, codebase_path: str) -> dict:
        """
        Research a single subtopic within the codebase.

        Args:
            subtopic: The focused research subtopic
            codebase_path: Path to the codebase to research

        Returns:
            Dict with: subtopic, findings, key_files, confidence, recommendations
        """
        result = self.agent.query(
            prompt=(
                f"You are Research Worker #{self.worker_id}.\n\n"
                f"## Your Research Task\n"
                f"Research this subtopic within the codebase at {codebase_path}:\n\n"
                f"**Subtopic:** {subtopic}\n\n"
                f"## Instructions\n"
                f"1. Search the codebase thoroughly for information related to this subtopic\n"
                f"2. Read relevant files to understand patterns and approaches\n"
                f"3. Note specific file paths and line numbers for key findings\n"
                f"4. Rate your confidence in your findings\n\n"
                f"## Output Format\n"
                f"Return your findings in this exact JSON format:\n"
                f'{{\n'
                f'  "subtopic": "{subtopic}",\n'
                f'  "findings": "Detailed description of what you found",\n'
                f'  "key_files": ["file1.ts:10-20", "file2.py:30-40"],\n'
                f'  "confidence": "low|medium|high",\n'
                f'  "recommendations": ["recommendation 1", "recommendation 2"],\n'
                f'  "evidence_count": 0\n'
                f'}}\n\n'
                f"Be thorough but focused. Only research this specific subtopic."
            ),
            allowed_tools=["Read", "Glob", "Grep"],
        )

        # Try to parse JSON from the response
        try:
            json_match = re.search(r"\{.*\}", result.text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return {
                    "subtopic": subtopic,
                    "findings": parsed.get("findings", result.text),
                    "key_files": parsed.get("key_files", []),
                    "confidence": parsed.get("confidence", "medium"),
                    "recommendations": parsed.get("recommendations", []),
                    "evidence_count": parsed.get("evidence_count", 0),
                    "raw_text": result.text,
                    "tokens_used": getattr(result, "usage", None),
                }
        except (json.JSONDecodeError, AttributeError):
            pass

        # Fallback: return the raw text as findings
        return {
            "subtopic": subtopic,
            "findings": result.text,
            "key_files": [],
            "confidence": "medium",
            "recommendations": [],
            "evidence_count": 0,
            "raw_text": result.text,
            "tokens_used": getattr(result, "usage", None),
        }
