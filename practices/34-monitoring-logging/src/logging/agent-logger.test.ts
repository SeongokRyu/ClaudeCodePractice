/**
 * agent-logger.test.ts — Tests for the AgentLogger
 */

import { AgentLogger } from "./agent-logger";
import type { LoggerConfig, SessionStats, TokenCount } from "./agent-logger";
import { existsSync, readFileSync, unlinkSync, mkdirSync } from "fs";
import { join } from "path";

// Suppress console.error during tests
const originalConsoleError = console.error;
beforeAll(() => {
  console.error = jest.fn();
});
afterAll(() => {
  console.error = originalConsoleError;
});

describe("AgentLogger", () => {
  describe("constructor", () => {
    it("should create a logger with default config", () => {
      const logger = new AgentLogger();
      expect(logger.getSessionId()).toBeDefined();
      expect(logger.getSessionId().length).toBeGreaterThan(0);
    });

    it("should accept a custom session ID", () => {
      const logger = new AgentLogger({ session_id: "test-123" });
      expect(logger.getSessionId()).toBe("test-123");
    });

    it("should initialize with zero tokens", () => {
      const logger = new AgentLogger();
      const tokens = logger.getCumulativeTokens();
      expect(tokens.input).toBe(0);
      expect(tokens.output).toBe(0);
    });
  });

  describe("tool call tracking", () => {
    it("should track a successful tool call", () => {
      const logger = new AgentLogger({ session_id: "test-track" });
      logger.sessionStart();

      const callId = logger.toolCallStart("Edit", { file_path: "test.ts" });
      expect(callId).toBeDefined();

      logger.toolCallEnd(callId, { input: 100, output: 50 });

      const stats = logger.getStats();
      expect(stats.tool_calls).toBe(1);
      expect(stats.tool_errors).toBe(0);
      expect(stats.tool_usage["Edit"]).toBe(1);
    });

    it("should track multiple tool calls", () => {
      const logger = new AgentLogger({ session_id: "test-multi" });
      logger.sessionStart();

      const call1 = logger.toolCallStart("Read");
      logger.toolCallEnd(call1, { input: 200, output: 100 });

      const call2 = logger.toolCallStart("Edit");
      logger.toolCallEnd(call2, { input: 150, output: 80 });

      const call3 = logger.toolCallStart("Read");
      logger.toolCallEnd(call3, { input: 100, output: 50 });

      const stats = logger.getStats();
      expect(stats.tool_calls).toBe(3);
      expect(stats.tool_usage["Read"]).toBe(2);
      expect(stats.tool_usage["Edit"]).toBe(1);
    });

    it("should track tool call errors", () => {
      const logger = new AgentLogger({ session_id: "test-error" });
      logger.sessionStart();

      const callId = logger.toolCallStart("Bash");
      logger.toolCallError(callId, new Error("Command failed"));

      const stats = logger.getStats();
      expect(stats.tool_calls).toBe(1);
      expect(stats.tool_errors).toBe(1);
      expect(stats.error_types["Error"]).toBe(1);
    });

    it("should handle string errors", () => {
      const logger = new AgentLogger({ session_id: "test-string-error" });
      logger.sessionStart();

      const callId = logger.toolCallStart("Bash");
      logger.toolCallError(callId, "something went wrong");

      const stats = logger.getStats();
      expect(stats.tool_errors).toBe(1);
    });

    it("should handle unknown call IDs gracefully", () => {
      const logger = new AgentLogger({ session_id: "test-unknown" });
      logger.sessionStart();

      // Should not throw
      logger.toolCallEnd("nonexistent-id", { input: 100, output: 50 });
    });
  });

  describe("token tracking", () => {
    it("should accumulate tokens across calls", () => {
      const logger = new AgentLogger({ session_id: "test-tokens" });
      logger.sessionStart();

      const call1 = logger.toolCallStart("Read");
      logger.toolCallEnd(call1, { input: 100, output: 50 });

      const call2 = logger.toolCallStart("Edit");
      logger.toolCallEnd(call2, { input: 200, output: 100 });

      const tokens = logger.getCumulativeTokens();
      expect(tokens.input).toBe(300);
      expect(tokens.output).toBe(150);
    });

    it("should handle calls without token counts", () => {
      const logger = new AgentLogger({ session_id: "test-no-tokens" });
      logger.sessionStart();

      const callId = logger.toolCallStart("Glob");
      logger.toolCallEnd(callId);

      const tokens = logger.getCumulativeTokens();
      expect(tokens.input).toBe(0);
      expect(tokens.output).toBe(0);
    });
  });

  describe("cost calculation", () => {
    it("should calculate cost based on token usage", () => {
      const logger = new AgentLogger({
        session_id: "test-cost",
        cost_per_input_token: 0.001,
        cost_per_output_token: 0.002,
      });
      logger.sessionStart();

      const callId = logger.toolCallStart("Read");
      logger.toolCallEnd(callId, { input: 1000, output: 500 });

      const cost = logger.getCurrentCost();
      expect(cost).toBeCloseTo(1000 * 0.001 + 500 * 0.002);
    });

    it("should return zero cost with no token usage", () => {
      const logger = new AgentLogger({ session_id: "test-zero-cost" });
      expect(logger.getCurrentCost()).toBe(0);
    });
  });

  describe("session lifecycle", () => {
    it("should produce complete session stats", () => {
      const logger = new AgentLogger({ session_id: "test-lifecycle" });
      logger.sessionStart();

      const call1 = logger.toolCallStart("Read");
      logger.toolCallEnd(call1, { input: 100, output: 50 });

      const call2 = logger.toolCallStart("Edit");
      logger.toolCallEnd(call2, { input: 200, output: 100 });

      const call3 = logger.toolCallStart("Bash");
      logger.toolCallError(call3, new Error("fail"));

      const stats = logger.sessionEnd();

      expect(stats.session_id).toBe("test-lifecycle");
      expect(stats.start_time).toBeDefined();
      expect(stats.end_time).toBeDefined();
      expect(stats.tool_calls).toBe(3);
      expect(stats.tool_errors).toBe(1);
      expect(stats.total_tokens.input).toBe(300);
      expect(stats.total_tokens.output).toBe(150);
      expect(stats.total_cost_usd).toBeGreaterThan(0);
      expect(stats.tool_usage).toEqual({
        Read: 1,
        Edit: 1,
        Bash: 1,
      });
    });
  });

  describe("file output", () => {
    const testLogFile = join(__dirname, "test-output.log");

    afterEach(() => {
      if (existsSync(testLogFile)) {
        unlinkSync(testLogFile);
      }
    });

    it("should write log entries to file", () => {
      const logger = new AgentLogger({
        session_id: "test-file",
        output_file: testLogFile,
        console_output: false,
      });
      logger.sessionStart();

      const callId = logger.toolCallStart("Read");
      logger.toolCallEnd(callId, { input: 100, output: 50 });
      logger.sessionEnd();

      expect(existsSync(testLogFile)).toBe(true);

      const content = readFileSync(testLogFile, "utf-8");
      const lines = content.trim().split("\n");
      expect(lines.length).toBeGreaterThanOrEqual(3); // start, call_start, call_end, end

      // Each line should be valid JSON
      for (const line of lines) {
        const entry = JSON.parse(line);
        expect(entry.session_id).toBe("test-file");
        expect(entry.timestamp).toBeDefined();
        expect(entry.event_type).toBeDefined();
      }
    });
  });

  describe("custom events", () => {
    it("should log custom events", () => {
      const logger = new AgentLogger({
        session_id: "test-custom",
        console_output: false,
      });

      // Should not throw
      logger.logCustom("info", "Custom event", { key: "value" });
      logger.logCustom("warn", "Warning event");
      logger.logCustom("error", "Error event");
    });
  });

  describe("log level filtering", () => {
    it("should filter debug messages when level is info", () => {
      const logFile = join(__dirname, "test-level.log");

      const logger = new AgentLogger({
        session_id: "test-level",
        output_file: logFile,
        console_output: false,
        log_level: "info",
      });

      logger.sessionStart(); // info — should be logged
      const callId = logger.toolCallStart("Read"); // debug — should be filtered
      logger.toolCallEnd(callId); // info — should be logged
      logger.sessionEnd(); // info — should be logged

      const content = readFileSync(logFile, "utf-8");
      const lines = content.trim().split("\n");

      // Debug entries should be filtered out
      const debugEntries = lines
        .map((l) => JSON.parse(l))
        .filter((e: { level: string }) => e.level === "debug");
      expect(debugEntries.length).toBe(0);

      // Cleanup
      unlinkSync(logFile);
    });
  });
});
