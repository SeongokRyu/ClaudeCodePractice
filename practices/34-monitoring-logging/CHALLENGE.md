# Challenge: 에이전트 모니터링과 로깅

## Step 1: Structured Logging

Create a TypeScript logger (`src/logging/agent-logger.ts`) that captures every tool call with structured data.

Log entry format:
```json
{
  "timestamp": "2025-01-15T10:30:00.000Z",
  "session_id": "abc-123",
  "event_type": "tool_call",
  "tool_name": "Edit",
  "duration_ms": 150,
  "token_count": {
    "input": 1200,
    "output": 450
  },
  "status": "success",
  "metadata": {
    "file_path": "src/app.ts",
    "action": "edit"
  }
}
```

Requirements:
- Generate unique session IDs
- Track cumulative token usage
- Record tool call durations
- Support multiple output targets (file, console, both)
- Include session-level aggregations (total tokens, total time, tool usage counts)

## Step 2: Error Handling Hooks

Create hooks (`src/hooks/logging-hooks.json`) that catch and log failures.

Hook behaviors:
- **PreToolUse**: log every tool call attempt
- **PostToolUse**: log tool results and detect errors
- **On error**: log the error with full context (what was attempted, what failed, input data)

Error categories to track:
- Tool execution failures (non-zero exit codes)
- File not found errors
- Permission denied errors
- Timeout errors
- API errors (rate limits, token limits)

## Step 3: Monitoring Dashboard

Build log analysis tools:

### log-parser.ts
Parse raw agent transcripts and extract:
- Tool call frequency (which tools are used most)
- Error rates (failures per tool type)
- Token usage over time
- Session duration breakdown

### log-analyzer.ts
Identify patterns:
- Most commonly used tools
- Most common errors
- Token usage trends
- Files accessed most frequently
- Repeated actions (potential optimization targets)

### cost-monitor.sh
Monitor session cost in real-time:
- Parse token usage from logs
- Calculate cost based on model pricing
- Alert if cost exceeds threshold
- Support configurable thresholds per session

## Step 4: Failure Recovery

Implement recovery strategies:

### Retry Logic
- Exponential backoff for transient failures
- Maximum retry count (configurable)
- Different strategies per error type:
  - File not found: no retry (deterministic failure)
  - API rate limit: retry with backoff
  - Timeout: retry with increased timeout

### Fallback Strategies
- If a tool fails, try an alternative approach
- If the primary model fails, fall back to a simpler model
- If an edit fails, read the file first and try again

### Graceful Degradation
- If non-critical tools fail, continue with reduced functionality
- Log degraded operations for later review

## Step 5: Alerting System

Build alerting scripts:

### cost-monitor.sh
- Track cumulative session cost
- Alert at 50%, 75%, 90% of budget
- Hard stop at 100% of budget
- Send notification (desktop, log, or both)

### stuck-detector.sh
Detect stuck-in-loop agents:
- Monitor for repeated identical tool calls
- Detect "edit-undo-edit" cycles
- Check for progress indicators (new files created, tests passing)
- Alert if no progress after N iterations

## Step 6: Session Analysis

Build a session analysis workflow:

1. Parse a complete session log
2. Generate a summary report:
   - Total duration, total tokens, total cost
   - Tool usage breakdown (pie chart data)
   - Error timeline
   - Token usage over time
   - Files touched and frequency
3. Identify optimization opportunities:
   - Unnecessary file reads (file read but not used)
   - Repeated tool calls (same operation multiple times)
   - Large token spikes (where did tokens go?)
   - Slow operations (bottleneck identification)

## Success Criteria

- [ ] Structured logger captures all tool calls with timestamps and token counts
- [ ] Error handling hooks catch and categorize failures
- [ ] Log parser extracts meaningful metrics from transcripts
- [ ] Cost monitor tracks spending and alerts at thresholds
- [ ] Stuck detector identifies loop behavior
- [ ] Session summary report provides actionable insights
- [ ] All logger tests pass
