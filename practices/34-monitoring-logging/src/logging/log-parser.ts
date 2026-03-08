/**
 * log-parser.ts — Parse agent transcripts and extract structured metrics
 *
 * Reads log files produced by AgentLogger and extracts:
 * - Tool call frequency
 * - Error rates per tool
 * - Token usage over time
 * - Session duration breakdown
 */

import { readFileSync } from "fs";
import type { LogEntry, TokenCount, EventType } from "./agent-logger";

// ── Types ────────────────────────────────────────────────────────────────

export interface ToolCallMetric {
  tool_name: string;
  call_count: number;
  error_count: number;
  error_rate: number;
  avg_duration_ms: number;
  total_duration_ms: number;
  total_tokens: TokenCount;
}

export interface TimeSeriesPoint {
  timestamp: string;
  cumulative_input_tokens: number;
  cumulative_output_tokens: number;
  cumulative_cost_usd: number;
}

export interface ParsedSession {
  session_id: string;
  start_time: string | null;
  end_time: string | null;
  total_entries: number;
  tool_metrics: Record<string, ToolCallMetric>;
  token_timeline: TimeSeriesPoint[];
  errors: LogEntry[];
  event_counts: Record<EventType, number>;
}

// ── Parser ───────────────────────────────────────────────────────────────

export function parseLogFile(filePath: string): LogEntry[] {
  const content = readFileSync(filePath, "utf-8");
  const lines = content.split("\n").filter((line) => line.trim().length > 0);

  const entries: LogEntry[] = [];
  for (const line of lines) {
    try {
      const entry = JSON.parse(line) as LogEntry;
      entries.push(entry);
    } catch {
      // Skip malformed lines
      continue;
    }
  }

  return entries;
}

export function parseLogEntries(entries: LogEntry[]): ParsedSession {
  const toolMetrics: Record<string, ToolCallMetric> = {};
  const tokenTimeline: TimeSeriesPoint[] = [];
  const errors: LogEntry[] = [];
  const eventCounts: Record<string, number> = {};

  let sessionId = "";
  let startTime: string | null = null;
  let endTime: string | null = null;

  // Cost per token (Sonnet pricing)
  const costPerInput = 0.003 / 1000;
  const costPerOutput = 0.015 / 1000;

  for (const entry of entries) {
    // Track session info
    if (entry.session_id) {
      sessionId = entry.session_id;
    }

    // Count events
    eventCounts[entry.event_type] =
      (eventCounts[entry.event_type] ?? 0) + 1;

    // Track session boundaries
    if (entry.event_type === "session_start") {
      startTime = entry.timestamp;
    }
    if (entry.event_type === "session_end") {
      endTime = entry.timestamp;
    }

    // Track tool calls
    if (
      entry.event_type === "tool_call_end" ||
      entry.event_type === "tool_call_error"
    ) {
      const toolName = entry.tool_name ?? "unknown";

      if (!toolMetrics[toolName]) {
        toolMetrics[toolName] = {
          tool_name: toolName,
          call_count: 0,
          error_count: 0,
          error_rate: 0,
          avg_duration_ms: 0,
          total_duration_ms: 0,
          total_tokens: { input: 0, output: 0 },
        };
      }

      const metric = toolMetrics[toolName];
      metric.call_count++;

      if (entry.event_type === "tool_call_error") {
        metric.error_count++;
      }

      if (entry.duration_ms) {
        metric.total_duration_ms += entry.duration_ms;
      }

      if (entry.token_count) {
        metric.total_tokens.input += entry.token_count.input;
        metric.total_tokens.output += entry.token_count.output;
      }

      // Update averages
      metric.avg_duration_ms = metric.total_duration_ms / metric.call_count;
      metric.error_rate = metric.error_count / metric.call_count;
    }

    // Track errors
    if (entry.level === "error") {
      errors.push(entry);
    }

    // Track token timeline
    if (entry.cumulative_tokens) {
      const inputTokens = entry.cumulative_tokens.input;
      const outputTokens = entry.cumulative_tokens.output;
      tokenTimeline.push({
        timestamp: entry.timestamp,
        cumulative_input_tokens: inputTokens,
        cumulative_output_tokens: outputTokens,
        cumulative_cost_usd:
          inputTokens * costPerInput + outputTokens * costPerOutput,
      });
    }
  }

  return {
    session_id: sessionId,
    start_time: startTime,
    end_time: endTime,
    total_entries: entries.length,
    tool_metrics: toolMetrics,
    token_timeline: tokenTimeline,
    errors,
    event_counts: eventCounts as Record<EventType, number>,
  };
}

// ── Formatting ───────────────────────────────────────────────────────────

export function formatSessionReport(session: ParsedSession): string {
  const lines: string[] = [];

  lines.push("====================================");
  lines.push("Session Analysis Report");
  lines.push("====================================");
  lines.push("");
  lines.push(`Session ID: ${session.session_id}`);
  lines.push(`Start: ${session.start_time ?? "unknown"}`);
  lines.push(`End: ${session.end_time ?? "unknown"}`);
  lines.push(`Total log entries: ${session.total_entries}`);
  lines.push("");

  // Tool usage table
  lines.push("Tool Usage:");
  lines.push(
    "  Tool              Calls  Errors  Error%  Avg(ms)  Tokens(in)  Tokens(out)"
  );
  lines.push(
    "  ────              ─────  ──────  ──────  ───────  ──────────  ──────────"
  );

  const sortedTools = Object.values(session.tool_metrics).sort(
    (a, b) => b.call_count - a.call_count
  );

  for (const metric of sortedTools) {
    const name = metric.tool_name.padEnd(18);
    const calls = String(metric.call_count).padStart(5);
    const errs = String(metric.error_count).padStart(6);
    const errRate = `${(metric.error_rate * 100).toFixed(0)}%`.padStart(6);
    const avgMs = String(Math.round(metric.avg_duration_ms)).padStart(7);
    const tokIn = String(metric.total_tokens.input).padStart(10);
    const tokOut = String(metric.total_tokens.output).padStart(10);
    lines.push(`  ${name}${calls}${errs}${errRate}${avgMs}${tokIn}${tokOut}`);
  }

  lines.push("");

  // Token summary
  const lastPoint =
    session.token_timeline[session.token_timeline.length - 1];
  if (lastPoint) {
    lines.push("Token Summary:");
    lines.push(
      `  Input tokens:  ${lastPoint.cumulative_input_tokens.toLocaleString()}`
    );
    lines.push(
      `  Output tokens: ${lastPoint.cumulative_output_tokens.toLocaleString()}`
    );
    lines.push(
      `  Estimated cost: $${lastPoint.cumulative_cost_usd.toFixed(4)}`
    );
    lines.push("");
  }

  // Errors
  if (session.errors.length > 0) {
    lines.push(`Errors (${session.errors.length}):`);
    for (const error of session.errors.slice(0, 10)) {
      lines.push(
        `  [${error.timestamp}] ${error.tool_name ?? ""}: ${error.message ?? "unknown error"}`
      );
    }
    if (session.errors.length > 10) {
      lines.push(`  ... and ${session.errors.length - 10} more`);
    }
  }

  lines.push("");
  lines.push("====================================");

  return lines.join("\n");
}
