/**
 * Practice 28: Research Worker Agent (TypeScript)
 *
 * A worker agent that researches a single subtopic within a codebase.
 * Workers operate independently and produce structured findings.
 */

import { Agent } from "@anthropic-ai/claude-agent-sdk";
import { WorkerFinding } from "./research-lead";

export class ResearchWorker {
  private workerId: number;
  private agent: Agent;

  constructor(workerId: number = 0) {
    this.workerId = workerId;
    this.agent = new Agent();
  }

  /**
   * Research a single subtopic within the codebase.
   */
  async research(
    subtopic: string,
    codebasePath: string
  ): Promise<WorkerFinding> {
    const result = await this.agent.query({
      prompt:
        `You are Research Worker #${this.workerId}.\n\n` +
        `## Your Research Task\n` +
        `Research this subtopic within the codebase at ${codebasePath}:\n\n` +
        `**Subtopic:** ${subtopic}\n\n` +
        `## Instructions\n` +
        `1. Search the codebase thoroughly for information related to this subtopic\n` +
        `2. Read relevant files to understand patterns and approaches\n` +
        `3. Note specific file paths and line numbers for key findings\n` +
        `4. Rate your confidence in your findings\n\n` +
        `## Output Format\n` +
        `Return your findings in this exact JSON format:\n` +
        `{\n` +
        `  "subtopic": "${subtopic}",\n` +
        `  "findings": "Detailed description of what you found",\n` +
        `  "key_files": ["file1.ts:10-20", "file2.py:30-40"],\n` +
        `  "confidence": "low|medium|high",\n` +
        `  "recommendations": ["recommendation 1", "recommendation 2"],\n` +
        `  "evidence_count": 0\n` +
        `}\n\n` +
        `Be thorough but focused. Only research this specific subtopic.`,
      allowedTools: ["Read", "Glob", "Grep"],
    });

    try {
      const jsonMatch = result.text.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        const parsed = JSON.parse(jsonMatch[0]);
        return {
          subtopic,
          findings: parsed.findings || result.text,
          keyFiles: parsed.key_files || [],
          confidence: parsed.confidence || "medium",
          recommendations: parsed.recommendations || [],
          evidenceCount: parsed.evidence_count || 0,
          rawText: result.text,
        };
      }
    } catch {
      // Fall through to default
    }

    return {
      subtopic,
      findings: result.text,
      keyFiles: [],
      confidence: "medium",
      recommendations: [],
      evidenceCount: 0,
      rawText: result.text,
    };
  }
}
