/**
 * log-analyzer.ts — Identify patterns and optimization opportunities in agent sessions
 *
 * Analyzes parsed session data to find:
 * - Repeated actions (potential optimization targets)
 * - Token spikes (where tokens were consumed most)
 * - Stuck patterns (edit-undo-edit cycles)
 * - Unused file reads (files read but not used for edits)
 */

import type { LogEntry, TokenCount } from "./agent-logger";
import type { ParsedSession } from "./log-parser";

// ── Types ────────────────────────────────────────────────────────────────

export interface Pattern {
  type: "repeated_action" | "token_spike" | "stuck_loop" | "unused_read" | "slow_operation";
  severity: "info" | "warning" | "critical";
  description: string;
  occurrences: number;
  details: string[];
}

export interface OptimizationSuggestion {
  area: string;
  current: string;
  suggested: string;
  estimated_savings: string;
}

export interface AnalysisReport {
  patterns: Pattern[];
  suggestions: OptimizationSuggestion[];
  health_score: number; // 0-100
}

// ── Analysis Functions ───────────────────────────────────────────────────

export function analyzeSession(
  entries: LogEntry[],
  session: ParsedSession
): AnalysisReport {
  const patterns: Pattern[] = [];

  patterns.push(...detectRepeatedActions(entries));
  patterns.push(...detectTokenSpikes(entries));
  patterns.push(...detectStuckLoops(entries));
  patterns.push(...detectUnusedReads(entries));
  patterns.push(...detectSlowOperations(entries));

  const suggestions = generateSuggestions(session, patterns);
  const healthScore = calculateHealthScore(session, patterns);

  return { patterns, suggestions, health_score: healthScore };
}

// ── Pattern Detection ────────────────────────────────────────────────────

function detectRepeatedActions(entries: LogEntry[]): Pattern[] {
  const patterns: Pattern[] = [];

  // Group consecutive tool calls by tool name and metadata
  const actionSignatures: Record<string, number> = {};

  for (const entry of entries) {
    if (entry.event_type !== "tool_call_end") continue;

    const filePath =
      (entry.metadata?.file_path as string) ??
      (entry.metadata?.path as string) ??
      "";
    const signature = `${entry.tool_name}:${filePath}`;
    actionSignatures[signature] = (actionSignatures[signature] ?? 0) + 1;
  }

  for (const [signature, count] of Object.entries(actionSignatures)) {
    if (count >= 3) {
      const [tool, file] = signature.split(":");
      patterns.push({
        type: "repeated_action",
        severity: count >= 5 ? "warning" : "info",
        description: `${tool} called ${count} times on ${file || "same target"}`,
        occurrences: count,
        details: [`Tool: ${tool}`, `Target: ${file || "various"}`, `Count: ${count}`],
      });
    }
  }

  return patterns;
}

function detectTokenSpikes(entries: LogEntry[]): Pattern[] {
  const patterns: Pattern[] = [];
  let prevTokens = 0;

  for (const entry of entries) {
    if (!entry.token_count) continue;

    const entryTokens = entry.token_count.input + entry.token_count.output;

    // Token spike: single call uses > 5000 tokens
    if (entryTokens > 5000) {
      patterns.push({
        type: "token_spike",
        severity: entryTokens > 10000 ? "warning" : "info",
        description: `High token usage: ${entryTokens} tokens in single ${entry.tool_name} call`,
        occurrences: 1,
        details: [
          `Tool: ${entry.tool_name}`,
          `Input tokens: ${entry.token_count.input}`,
          `Output tokens: ${entry.token_count.output}`,
          `Timestamp: ${entry.timestamp}`,
        ],
      });
    }

    prevTokens = entryTokens;
  }

  return patterns;
}

function detectStuckLoops(entries: LogEntry[]): Pattern[] {
  const patterns: Pattern[] = [];

  // Look for A-B-A-B patterns (e.g., edit-undo-edit-undo)
  const toolSequence = entries
    .filter((e) => e.event_type === "tool_call_end")
    .map((e) => e.tool_name ?? "");

  for (let i = 0; i < toolSequence.length - 3; i++) {
    if (
      toolSequence[i] === toolSequence[i + 2] &&
      toolSequence[i + 1] === toolSequence[i + 3] &&
      toolSequence[i] !== toolSequence[i + 1]
    ) {
      // Check if this pattern continues
      let repeatCount = 2;
      for (let j = i + 4; j < toolSequence.length - 1; j += 2) {
        if (
          toolSequence[j] === toolSequence[i] &&
          toolSequence[j + 1] === toolSequence[i + 1]
        ) {
          repeatCount++;
        } else {
          break;
        }
      }

      if (repeatCount >= 3) {
        patterns.push({
          type: "stuck_loop",
          severity: "critical",
          description: `Stuck loop detected: ${toolSequence[i]} <-> ${toolSequence[i + 1]} repeated ${repeatCount} times`,
          occurrences: repeatCount,
          details: [
            `Pattern: ${toolSequence[i]} -> ${toolSequence[i + 1]}`,
            `Repeats: ${repeatCount}`,
            `Starting at entry index: ${i}`,
          ],
        });
        break; // Report each unique loop once
      }
    }
  }

  return patterns;
}

function detectUnusedReads(entries: LogEntry[]): Pattern[] {
  const patterns: Pattern[] = [];

  // Track files that were read but never edited
  const readFiles = new Set<string>();
  const editedFiles = new Set<string>();

  for (const entry of entries) {
    if (entry.event_type !== "tool_call_end") continue;

    const filePath =
      (entry.metadata?.file_path as string) ??
      (entry.metadata?.path as string) ??
      "";

    if (!filePath) continue;

    if (entry.tool_name === "Read") {
      readFiles.add(filePath);
    } else if (entry.tool_name === "Edit" || entry.tool_name === "Write") {
      editedFiles.add(filePath);
    }
  }

  const unusedReads = [...readFiles].filter((f) => !editedFiles.has(f));

  if (unusedReads.length > 3) {
    patterns.push({
      type: "unused_read",
      severity: "info",
      description: `${unusedReads.length} files were read but never edited`,
      occurrences: unusedReads.length,
      details: unusedReads.slice(0, 10),
    });
  }

  return patterns;
}

function detectSlowOperations(entries: LogEntry[]): Pattern[] {
  const patterns: Pattern[] = [];

  for (const entry of entries) {
    if (
      entry.event_type !== "tool_call_end" ||
      !entry.duration_ms
    )
      continue;

    // Slow: > 30 seconds for a single tool call
    if (entry.duration_ms > 30000) {
      patterns.push({
        type: "slow_operation",
        severity: entry.duration_ms > 60000 ? "warning" : "info",
        description: `Slow operation: ${entry.tool_name} took ${(entry.duration_ms / 1000).toFixed(1)}s`,
        occurrences: 1,
        details: [
          `Tool: ${entry.tool_name}`,
          `Duration: ${(entry.duration_ms / 1000).toFixed(1)}s`,
          `Timestamp: ${entry.timestamp}`,
        ],
      });
    }
  }

  return patterns;
}

// ── Suggestions ──────────────────────────────────────────────────────────

function generateSuggestions(
  session: ParsedSession,
  patterns: Pattern[]
): OptimizationSuggestion[] {
  const suggestions: OptimizationSuggestion[] = [];

  // Check for high error rates
  for (const metric of Object.values(session.tool_metrics)) {
    if (metric.error_rate > 0.3 && metric.call_count >= 3) {
      suggestions.push({
        area: `${metric.tool_name} reliability`,
        current: `${(metric.error_rate * 100).toFixed(0)}% error rate (${metric.error_count}/${metric.call_count})`,
        suggested: "Investigate common error causes and add pre-validation",
        estimated_savings: `${metric.error_count} fewer failed calls`,
      });
    }
  }

  // Check for repeated actions
  const repeatedPatterns = patterns.filter((p) => p.type === "repeated_action");
  if (repeatedPatterns.length > 0) {
    suggestions.push({
      area: "Repeated operations",
      current: `${repeatedPatterns.length} repeated action patterns found`,
      suggested: "Cache results or batch operations to reduce redundant calls",
      estimated_savings: "20-40% fewer tool calls",
    });
  }

  // Check for stuck loops
  const stuckPatterns = patterns.filter((p) => p.type === "stuck_loop");
  if (stuckPatterns.length > 0) {
    suggestions.push({
      area: "Stuck loop prevention",
      current: `${stuckPatterns.length} stuck loop(s) detected`,
      suggested: "Add loop detection hooks and maximum iteration limits",
      estimated_savings: "Prevent wasted tokens and time",
    });
  }

  // Check for token spikes
  const spikePatterns = patterns.filter((p) => p.type === "token_spike");
  if (spikePatterns.length > 0) {
    suggestions.push({
      area: "Token usage optimization",
      current: `${spikePatterns.length} high-token operations`,
      suggested: "Reduce file read sizes, use targeted searches instead of full reads",
      estimated_savings: "10-30% token reduction",
    });
  }

  return suggestions;
}

// ── Health Score ──────────────────────────────────────────────────────────

function calculateHealthScore(
  session: ParsedSession,
  patterns: Pattern[]
): number {
  let score = 100;

  // Deduct for errors
  const totalCalls = Object.values(session.tool_metrics).reduce(
    (sum, m) => sum + m.call_count,
    0
  );
  const totalErrors = Object.values(session.tool_metrics).reduce(
    (sum, m) => sum + m.error_count,
    0
  );
  const errorRate = totalCalls > 0 ? totalErrors / totalCalls : 0;
  score -= errorRate * 30;

  // Deduct for patterns
  for (const pattern of patterns) {
    switch (pattern.severity) {
      case "critical":
        score -= 20;
        break;
      case "warning":
        score -= 10;
        break;
      case "info":
        score -= 2;
        break;
    }
  }

  return Math.max(0, Math.min(100, Math.round(score)));
}

// ── Report Formatting ────────────────────────────────────────────────────

export function formatAnalysisReport(report: AnalysisReport): string {
  const lines: string[] = [];

  lines.push("====================================");
  lines.push("Session Analysis");
  lines.push("====================================");
  lines.push("");
  lines.push(`Health Score: ${report.health_score}/100`);
  lines.push("");

  if (report.patterns.length > 0) {
    lines.push("Detected Patterns:");
    for (const pattern of report.patterns) {
      const icon =
        pattern.severity === "critical"
          ? "[CRITICAL]"
          : pattern.severity === "warning"
            ? "[WARNING]"
            : "[INFO]";
      lines.push(`  ${icon} ${pattern.description}`);
      for (const detail of pattern.details) {
        lines.push(`    - ${detail}`);
      }
    }
    lines.push("");
  }

  if (report.suggestions.length > 0) {
    lines.push("Optimization Suggestions:");
    for (const suggestion of report.suggestions) {
      lines.push(`  Area: ${suggestion.area}`);
      lines.push(`    Current: ${suggestion.current}`);
      lines.push(`    Suggested: ${suggestion.suggested}`);
      lines.push(`    Est. savings: ${suggestion.estimated_savings}`);
      lines.push("");
    }
  }

  lines.push("====================================");
  return lines.join("\n");
}
