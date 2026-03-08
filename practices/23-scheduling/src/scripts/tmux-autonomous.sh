#!/usr/bin/env bash
#
# tmux-autonomous.sh — Manage tmux-based autonomous Claude sessions
#
# Usage:
#   bash tmux-autonomous.sh start  --name "my-task" --task "add error handling" --max-turns 50
#   bash tmux-autonomous.sh status --name "my-task"
#   bash tmux-autonomous.sh attach --name "my-task"
#   bash tmux-autonomous.sh logs   --name "my-task"
#   bash tmux-autonomous.sh stop   --name "my-task"
#   bash tmux-autonomous.sh list
#

set -euo pipefail

# Configuration
SESSION_PREFIX="claude-auto"
LOG_DIR="/tmp/claude-autonomous"
ACTION="${1:-help}"

# Parse common arguments
shift || true
SESSION_NAME=""
TASK=""
MAX_TURNS=50
BRANCH=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      SESSION_NAME="$2"
      shift 2
      ;;
    --task)
      TASK="$2"
      shift 2
      ;;
    --max-turns)
      MAX_TURNS="$2"
      shift 2
      ;;
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

FULL_SESSION_NAME="${SESSION_PREFIX}-${SESSION_NAME}"
SESSION_LOG="${LOG_DIR}/${SESSION_NAME}.log"

mkdir -p "$LOG_DIR"

# ─── Actions ───

action_start() {
  if [[ -z "$SESSION_NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi

  if [[ -z "$TASK" ]]; then
    echo "Error: --task is required"
    exit 1
  fi

  # Check if session already exists
  if tmux has-session -t "$FULL_SESSION_NAME" 2>/dev/null; then
    echo "Error: Session '$SESSION_NAME' already exists."
    echo "Use 'stop' to end it first, or 'attach' to view it."
    exit 1
  fi

  # Check prerequisites
  if ! command -v claude &>/dev/null; then
    echo "Error: claude CLI not found"
    exit 1
  fi

  if ! command -v tmux &>/dev/null; then
    echo "Error: tmux not found. Install it: sudo apt install tmux"
    exit 1
  fi

  # Create branch if specified
  if [[ -n "$BRANCH" ]]; then
    echo "Creating branch: $BRANCH"
    git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
  fi

  # Build the Claude command
  local claude_cmd="claude -p \"You are running in an autonomous session. Your task:

${TASK}

Rules:
1. Work systematically through the codebase
2. Make small, focused changes
3. Run tests after significant changes
4. Commit progress with descriptive messages
5. Do NOT push to remote
6. Add TODO comments for anything you're unsure about
7. Stop if you encounter merge conflicts\" \
    --dangerously-skip-permissions \
    --max-turns ${MAX_TURNS} \
    2>&1 | tee -a ${SESSION_LOG}"

  # Start tmux session
  echo "Starting autonomous session: $SESSION_NAME"
  echo "Task: $TASK"
  echo "Max turns: $MAX_TURNS"
  echo "Log file: $SESSION_LOG"
  echo ""

  # Record session metadata
  {
    echo "=== Session Started ==="
    echo "Name:      $SESSION_NAME"
    echo "Task:      $TASK"
    echo "Max turns: $MAX_TURNS"
    echo "Branch:    ${BRANCH:-$(git branch --show-current 2>/dev/null || echo 'N/A')}"
    echo "Started:   $(date)"
    echo "PWD:       $(pwd)"
    echo "========================"
    echo ""
  } > "$SESSION_LOG"

  tmux new-session -d -s "$FULL_SESSION_NAME" "bash -c '${claude_cmd}; echo \"\"; echo \"=== Session Complete ===\"; echo \"Finished: \$(date)\"; echo \"Press Enter to close.\"; read'"

  echo "Session started in background."
  echo ""
  echo "Commands:"
  echo "  bash $0 status --name $SESSION_NAME   # Check if running"
  echo "  bash $0 attach --name $SESSION_NAME   # View live output (Ctrl+B, D to detach)"
  echo "  bash $0 logs   --name $SESSION_NAME   # View log file"
  echo "  bash $0 stop   --name $SESSION_NAME   # Stop the session"
}

action_status() {
  if [[ -z "$SESSION_NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi

  if tmux has-session -t "$FULL_SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' is RUNNING"
    echo ""

    # Show session info
    tmux list-sessions -F '#{session_name}: #{session_created_string} (#{session_windows} windows)' \
      | grep "$FULL_SESSION_NAME" || true

    # Show last few lines of log
    if [[ -f "$SESSION_LOG" ]]; then
      echo ""
      echo "Last 5 lines of output:"
      tail -5 "$SESSION_LOG"
    fi
  else
    echo "Session '$SESSION_NAME' is NOT RUNNING"

    if [[ -f "$SESSION_LOG" ]]; then
      echo ""
      echo "Last log entry:"
      tail -3 "$SESSION_LOG"
    fi
  fi
}

action_attach() {
  if [[ -z "$SESSION_NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi

  if ! tmux has-session -t "$FULL_SESSION_NAME" 2>/dev/null; then
    echo "Error: Session '$SESSION_NAME' is not running"
    exit 1
  fi

  echo "Attaching to session '$SESSION_NAME'..."
  echo "(Press Ctrl+B, then D to detach without stopping)"
  echo ""

  tmux attach-session -t "$FULL_SESSION_NAME"
}

action_logs() {
  if [[ -z "$SESSION_NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi

  if [[ ! -f "$SESSION_LOG" ]]; then
    echo "No log file found for session '$SESSION_NAME'"
    exit 1
  fi

  echo "=== Log: $SESSION_NAME ==="
  echo "File: $SESSION_LOG"
  echo "Size: $(du -h "$SESSION_LOG" | cut -f1)"
  echo ""

  # Show with less for large files, cat for small ones
  local line_count
  line_count=$(wc -l < "$SESSION_LOG")

  if [[ $line_count -gt 100 ]]; then
    echo "(Showing last 50 lines. Full log: $SESSION_LOG)"
    echo ""
    tail -50 "$SESSION_LOG"
  else
    cat "$SESSION_LOG"
  fi
}

action_stop() {
  if [[ -z "$SESSION_NAME" ]]; then
    echo "Error: --name is required"
    exit 1
  fi

  if tmux has-session -t "$FULL_SESSION_NAME" 2>/dev/null; then
    echo "Stopping session '$SESSION_NAME'..."
    tmux kill-session -t "$FULL_SESSION_NAME"
    echo "Session stopped."

    # Append to log
    {
      echo ""
      echo "=== Session Stopped (manual) ==="
      echo "Stopped: $(date)"
    } >> "$SESSION_LOG" 2>/dev/null || true
  else
    echo "Session '$SESSION_NAME' is not running."
  fi

  # Show summary if log exists
  if [[ -f "$SESSION_LOG" ]]; then
    echo ""
    echo "Log file: $SESSION_LOG"
  fi
}

action_list() {
  echo "=== Active Claude Autonomous Sessions ==="
  echo ""

  local sessions
  sessions=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep "^${SESSION_PREFIX}" || true)

  if [[ -z "$sessions" ]]; then
    echo "No active sessions."
  else
    while IFS= read -r session; do
      local name="${session#${SESSION_PREFIX}-}"
      local created
      created=$(tmux list-sessions -F '#{session_name}: #{session_created_string}' | grep "^${session}:" | cut -d: -f2-)
      echo "  - $name (started:$created)"
    done <<< "$sessions"
  fi

  echo ""
  echo "=== Log Files ==="
  if ls "$LOG_DIR"/*.log &>/dev/null; then
    for log in "$LOG_DIR"/*.log; do
      local name
      name=$(basename "$log" .log)
      local size
      size=$(du -h "$log" | cut -f1)
      echo "  - $name ($size)"
    done
  else
    echo "  (none)"
  fi
}

action_help() {
  echo "tmux-autonomous.sh — Manage autonomous Claude sessions"
  echo ""
  echo "Commands:"
  echo "  start   --name <name> --task <task> [--max-turns N] [--branch <branch>]"
  echo "  status  --name <name>"
  echo "  attach  --name <name>"
  echo "  logs    --name <name>"
  echo "  stop    --name <name>"
  echo "  list"
  echo ""
  echo "Examples:"
  echo "  bash tmux-autonomous.sh start --name refactor --task 'add error handling' --max-turns 50"
  echo "  bash tmux-autonomous.sh status --name refactor"
  echo "  bash tmux-autonomous.sh attach --name refactor"
  echo "  bash tmux-autonomous.sh stop --name refactor"
}

# ─── Route to action ───
case "$ACTION" in
  start)  action_start ;;
  status) action_status ;;
  attach) action_attach ;;
  logs)   action_logs ;;
  stop)   action_stop ;;
  list)   action_list ;;
  help|--help|-h)  action_help ;;
  *)
    echo "Unknown action: $ACTION"
    action_help
    exit 1
    ;;
esac
