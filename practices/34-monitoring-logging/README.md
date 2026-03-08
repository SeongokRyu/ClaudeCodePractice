# Practice 34: 에이전트 모니터링과 로깅

## Goal

Build structured logging, error handling, real-time monitoring, and failure recovery systems for AI agents. Learn to observe what agents are doing, detect when they are stuck, control costs, and recover from failures.

## Prerequisites

- **Practice 30**: Deterministic Guardrails (hooks and settings)
- **Practice 33**: Quality Gates (pipeline concepts)

## Time

90-120 minutes

## Difficulty

★★★

## What You Will Learn

1. How to implement structured logging for agent sessions
2. How to create error handling hooks that catch and log failures
3. How to build monitoring tools that parse agent logs
4. How to detect stuck agents and implement recovery strategies
5. How to monitor and alert on session costs
6. How to analyze session logs for optimization opportunities

## Key Concepts

- **Structured logging**: JSON-formatted logs with timestamps, event types, token counts, and tool names.
- **Observability**: the ability to understand what an agent is doing from its external outputs (logs, metrics).
- **Stuck detection**: identifying when an agent is repeating the same actions without progress.
- **Cost monitoring**: tracking token usage in real-time to prevent budget overruns.
- **Failure recovery**: retry logic, fallback strategies, and graceful degradation.

## Structure

```
src/
  logging/
    agent-logger.ts       # Structured logger for agent sessions
    log-parser.ts         # Extracts metrics from agent transcripts
    log-analyzer.ts       # Identifies patterns in session data
    agent-logger.test.ts  # Tests for the logger
  monitoring/
    cost-monitor.sh       # Session cost monitoring and alerting
    stuck-detector.sh     # Detects stuck-in-loop agents
    session-summary.sh    # Generates session summary reports
  hooks/
    logging-hooks.json    # Hooks for comprehensive logging
  python/
    monitored_agent.py    # Agent SDK agent with full monitoring

package.json              # Node.js dependencies
tsconfig.json             # TypeScript configuration
jest.config.js            # Jest test configuration
```

## Tips

- Start with logging -- you cannot monitor what you cannot observe
- Keep log entries small but complete (structured JSON is ideal)
- The stuck detector is critical for headless/CI operation
- Cost monitoring prevents surprise bills on long-running tasks
