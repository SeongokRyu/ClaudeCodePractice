/**
 * Practice 28: Research Lead Agent (TypeScript)
 *
 * The lead agent decomposes research questions into subtopics
 * and synthesizes worker findings into comprehensive reports.
 */

import { Agent } from "@anthropic-ai/claude-agent-sdk";

export interface WorkerFinding {
  subtopic: string;
  findings: string;
  keyFiles: string[];
  confidence: "low" | "medium" | "high" | "none";
  recommendations: string[];
  evidenceCount: number;
  rawText?: string;
}

export class ResearchLead {
  private agent: Agent;

  constructor() {
    this.agent = new Agent();
  }

  /**
   * Decompose a research question into independent subtopics.
   */
  async decompose(
    question: string,
    numSubtopics: number = 3
  ): Promise<string[]> {
    const result = await this.agent.query({
      prompt:
        `Decompose this research question into exactly ${numSubtopics} ` +
        `independent, focused subtopics for parallel research.\n\n` +
        `Question: ${question}\n\n` +
        `Return ONLY a JSON array of strings, each being a focused ` +
        `research subtopic. Example:\n` +
        `["subtopic 1", "subtopic 2", "subtopic 3"]\n\n` +
        `Rules:\n` +
        `- Each subtopic should be independently researchable\n` +
        `- Together they should cover the full question\n` +
        `- They should not overlap significantly\n` +
        `- Each should be specific enough for a single worker`,
      disallowedTools: ["Bash", "Write", "Edit"],
    });

    try {
      const jsonMatch = result.text.match(/\[.*\]/s);
      if (jsonMatch) {
        const subtopics = JSON.parse(jsonMatch[0]) as string[];
        return subtopics.slice(0, numSubtopics);
      }
    } catch {
      // Fall through to line-based parsing
    }

    // Fallback: parse lines
    return result.text
      .split("\n")
      .map((line) => line.trim().replace(/^[\d.\-)\s]+/, ""))
      .filter((line) => line.length > 0 && !line.startsWith("#"))
      .slice(0, numSubtopics);
  }

  /**
   * Synthesize worker findings into a comprehensive report.
   */
  async synthesize(
    question: string,
    findings: WorkerFinding[],
    subtopics: string[]
  ): Promise<string> {
    let formattedFindings = "";
    findings.forEach((finding, i) => {
      formattedFindings += `\n### Worker ${i + 1}: ${subtopics[i] || finding.subtopic}\n`;
      formattedFindings += `**Confidence:** ${finding.confidence}\n`;
      formattedFindings += `**Findings:**\n${finding.findings}\n`;
      formattedFindings += `**Key files:**\n${finding.keyFiles.join(", ") || "None listed"}\n`;
      formattedFindings += `---\n`;
    });

    const result = await this.agent.query({
      prompt:
        `You are a research lead synthesizing findings from ` +
        `${findings.length} research workers.\n\n` +
        `## Original Question\n${question}\n\n` +
        `## Worker Findings\n${formattedFindings}\n\n` +
        `## Your Task\n` +
        `Produce a comprehensive research report with:\n\n` +
        `### 1. Executive Summary\n` +
        `2-3 sentences answering the original question.\n\n` +
        `### 2. Key Findings\n` +
        `Bullet points of the most important discoveries.\n\n` +
        `### 3. Detailed Analysis\n` +
        `Organized by subtopic, with cross-references.\n\n` +
        `### 4. Patterns Identified\n` +
        `Common themes across subtopics.\n\n` +
        `### 5. Contradictions\n` +
        `Where findings disagree.\n\n` +
        `### 6. Recommendations\n` +
        `Actionable next steps.\n\n` +
        `### 7. Confidence Assessment\n` +
        `Overall and per-subtopic confidence.`,
      disallowedTools: ["Bash", "Write", "Edit"],
    });

    return result.text;
  }
}
