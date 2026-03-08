/**
 * agent-logger.ts — Structured logger for AI agent sessions
 *
 * Captures tool calls, token usage, errors, and session metrics
 * in a structured JSON format for monitoring and analysis.
 */

import { randomUUID } from "crypto";
import { appendFileSync, mkdirSync, existsSync } from "fs";
import { join, dirname } from "path";

// ── Types ────────────────────────────────────────────────────────────────

export type EventType =
  | "session_start"
  | "session_end"
  | "tool_call_start"
  | "tool_call_end"
  | "tool_call_error"
  | "cost_alert"
  | "stuck_detected"
  | "retry"
  | "custom";

export type LogLevel = "debug" | "info" | "warn" | "error";

export interface TokenCount {
  input: number;
  output: number;
}

export interface LogEntry {
  timestamp: string;
  session_id: string;
  event_type: EventType;
  level: LogLevel;
  tool_name?: string;
  duration_ms?: number;
  token_count?: TokenCount;
  cumulative_tokens?: TokenCount;
  status?: "success" | "failure" | "error";
  message?: string;
  metadata?: Record<string, unknown>;
}

export interface SessionStats {
  session_id: string;
  start_time: string;
  end_time?: string;
  total_duration_ms: number;
  total_tokens: TokenCount;
  total_cost_usd: number;
  tool_calls: number;
  tool_errors: number;
  tool_usage: Record<string, number>;
  error_types: Record<string, number>;
}

export interface LoggerConfig {
  session_id?: string;
  output_file?: string;
  console_output?: boolean;
  log_level?: LogLevel;
  cost_per_input_token?: number;
  cost_per_output_token?: number;
  cost_budget_usd?: number;
}

// ── Log level priority ───────────────────────────────────────────────────

const LOG_LEVELS: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

// ── Default pricing (Claude Sonnet) ──────────────────────────────────────

const DEFAULT_COST_PER_INPUT_TOKEN = 0.003 / 1000;
const DEFAULT_COST_PER_OUTPUT_TOKEN = 0.015 / 1000;

// ── AgentLogger class ────────────────────────────────────────────────────

export class AgentLogger {
  private sessionId: string;
  private outputFile: string | null;
  private consoleOutput: boolean;
  private logLevel: LogLevel;
  private costPerInputToken: number;
  private costPerOutputToken: number;
  private costBudgetUsd: number | null;

  private startTime: Date;
  private cumulativeTokens: TokenCount = { input: 0, output: 0 };
  private toolCalls = 0;
  private toolErrors = 0;
  private toolUsage: Record<string, number> = {};
  private errorTypes: Record<string, number> = {};
  private activeToolCalls: Map<string, { tool: string; start: number }> =
    new Map();

  constructor(config: LoggerConfig = {}) {
    this.sessionId = config.session_id ?? randomUUID();
    this.outputFile = config.output_file ?? null;
    this.consoleOutput = config.console_output ?? true;
    this.logLevel = config.log_level ?? "info";
    this.costPerInputToken =
      config.cost_per_input_token ?? DEFAULT_COST_PER_INPUT_TOKEN;
    this.costPerOutputToken =
      config.cost_per_output_token ?? DEFAULT_COST_PER_OUTPUT_TOKEN;
    this.costBudgetUsd = config.cost_budget_usd ?? null;
    this.startTime = new Date();

    // Ensure output directory exists
    if (this.outputFile) {
      const dir = dirname(this.outputFile);
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }
    }
  }

  // ── Core logging ─────────────────────────────────────────────────────

  private log(entry: LogEntry): void {
    // Check log level
    if (LOG_LEVELS[entry.level] < LOG_LEVELS[this.logLevel]) {
      return;
    }

    const line = JSON.stringify(entry);

    // Console output
    if (this.consoleOutput) {
      const prefix = `[${entry.level.toUpperCase()}]`;
      const toolInfo = entry.tool_name ? ` [${entry.tool_name}]` : "";
      console.error(
        `${prefix}${toolInfo} ${entry.event_type}: ${entry.message ?? ""}`
      );
    }

    // File output
    if (this.outputFile) {
      appendFileSync(this.outputFile, line + "\n");
    }
  }

  // ── Session lifecycle ────────────────────────────────────────────────

  sessionStart(metadata?: Record<string, unknown>): void {
    this.startTime = new Date();
    this.log({
      timestamp: this.startTime.toISOString(),
      session_id: this.sessionId,
      event_type: "session_start",
      level: "info",
      message: "Session started",
      metadata,
    });
  }

  sessionEnd(): SessionStats {
    const endTime = new Date();
    const stats = this.getStats(endTime);

    this.log({
      timestamp: endTime.toISOString(),
      session_id: this.sessionId,
      event_type: "session_end",
      level: "info",
      message: `Session ended. ${stats.tool_calls} tool calls, ${stats.total_tokens.input + stats.total_tokens.output} tokens, $${stats.total_cost_usd.toFixed(4)}`,
      cumulative_tokens: this.cumulativeTokens,
      metadata: {
        total_cost_usd: stats.total_cost_usd,
        tool_usage: stats.tool_usage,
      },
    });

    return stats;
  }

  // ── Tool call tracking ───────────────────────────────────────────────

  toolCallStart(
    toolName: string,
    metadata?: Record<string, unknown>
  ): string {
    const callId = randomUUID();
    this.activeToolCalls.set(callId, {
      tool: toolName,
      start: Date.now(),
    });

    this.log({
      timestamp: new Date().toISOString(),
      session_id: this.sessionId,
      event_type: "tool_call_start",
      level: "debug",
      tool_name: toolName,
      message: `Starting ${toolName}`,
      metadata: { call_id: callId, ...metadata },
    });

    return callId;
  }

  toolCallEnd(
    callId: string,
    tokenCount?: TokenCount,
    metadata?: Record<string, unknown>
  ): void {
    const active = this.activeToolCalls.get(callId);
    if (!active) {
      this.log({
        timestamp: new Date().toISOString(),
        session_id: this.sessionId,
        event_type: "tool_call_error",
        level: "warn",
        message: `Unknown call ID: ${callId}`,
      });
      return;
    }

    const duration = Date.now() - active.start;
    this.activeToolCalls.delete(callId);

    // Update cumulative stats
    this.toolCalls++;
    this.toolUsage[active.tool] = (this.toolUsage[active.tool] ?? 0) + 1;

    if (tokenCount) {
      this.cumulativeTokens.input += tokenCount.input;
      this.cumulativeTokens.output += tokenCount.output;
    }

    this.log({
      timestamp: new Date().toISOString(),
      session_id: this.sessionId,
      event_type: "tool_call_end",
      level: "info",
      tool_name: active.tool,
      duration_ms: duration,
      token_count: tokenCount,
      cumulative_tokens: { ...this.cumulativeTokens },
      status: "success",
      message: `${active.tool} completed in ${duration}ms`,
      metadata: { call_id: callId, ...metadata },
    });

    // Check cost budget
    this.checkCostBudget();
  }

  toolCallError(
    callId: string,
    error: Error | string,
    metadata?: Record<string, unknown>
  ): void {
    const active = this.activeToolCalls.get(callId);
    const toolName = active?.tool ?? "unknown";
    const duration = active ? Date.now() - active.start : 0;

    if (active) {
      this.activeToolCalls.delete(callId);
    }

    this.toolCalls++;
    this.toolErrors++;
    this.toolUsage[toolName] = (this.toolUsage[toolName] ?? 0) + 1;

    const errorMessage = error instanceof Error ? error.message : error;
    const errorType = error instanceof Error ? error.constructor.name : "Error";
    this.errorTypes[errorType] = (this.errorTypes[errorType] ?? 0) + 1;

    this.log({
      timestamp: new Date().toISOString(),
      session_id: this.sessionId,
      event_type: "tool_call_error",
      level: "error",
      tool_name: toolName,
      duration_ms: duration,
      status: "error",
      message: `${toolName} failed: ${errorMessage}`,
      metadata: {
        call_id: callId,
        error_type: errorType,
        error_message: errorMessage,
        ...metadata,
      },
    });
  }

  // ── Cost monitoring ──────────────────────────────────────────────────

  private checkCostBudget(): void {
    if (!this.costBudgetUsd) return;

    const currentCost = this.getCurrentCost();
    const percentage = (currentCost / this.costBudgetUsd) * 100;

    if (percentage >= 90) {
      this.log({
        timestamp: new Date().toISOString(),
        session_id: this.sessionId,
        event_type: "cost_alert",
        level: "error",
        message: `Cost alert: $${currentCost.toFixed(4)} (${percentage.toFixed(1)}% of $${this.costBudgetUsd} budget)`,
        metadata: {
          current_cost: currentCost,
          budget: this.costBudgetUsd,
          percentage,
        },
      });
    } else if (percentage >= 75) {
      this.log({
        timestamp: new Date().toISOString(),
        session_id: this.sessionId,
        event_type: "cost_alert",
        level: "warn",
        message: `Cost warning: $${currentCost.toFixed(4)} (${percentage.toFixed(1)}% of budget)`,
        metadata: {
          current_cost: currentCost,
          budget: this.costBudgetUsd,
          percentage,
        },
      });
    }
  }

  getCurrentCost(): number {
    return (
      this.cumulativeTokens.input * this.costPerInputToken +
      this.cumulativeTokens.output * this.costPerOutputToken
    );
  }

  // ── Custom events ────────────────────────────────────────────────────

  logCustom(
    level: LogLevel,
    message: string,
    metadata?: Record<string, unknown>
  ): void {
    this.log({
      timestamp: new Date().toISOString(),
      session_id: this.sessionId,
      event_type: "custom",
      level,
      message,
      metadata,
    });
  }

  // ── Stats ────────────────────────────────────────────────────────────

  getStats(endTime?: Date): SessionStats {
    const end = endTime ?? new Date();
    return {
      session_id: this.sessionId,
      start_time: this.startTime.toISOString(),
      end_time: end.toISOString(),
      total_duration_ms: end.getTime() - this.startTime.getTime(),
      total_tokens: { ...this.cumulativeTokens },
      total_cost_usd: this.getCurrentCost(),
      tool_calls: this.toolCalls,
      tool_errors: this.toolErrors,
      tool_usage: { ...this.toolUsage },
      error_types: { ...this.errorTypes },
    };
  }

  getSessionId(): string {
    return this.sessionId;
  }

  getCumulativeTokens(): TokenCount {
    return { ...this.cumulativeTokens };
  }
}
