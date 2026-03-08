#!/usr/bin/env bash
#
# overnight-refactor.sh — Run Claude autonomously for overnight refactoring
#
# This script sets up a safe environment for long-running Claude sessions:
# 1. Creates a separate git branch
# 2. Optionally runs inside a Docker container
# 3. Limits the number of turns
# 4. Logs all output
# 5. Commits progress periodically
#
# Usage:
#   bash overnight-refactor.sh \
#     --task "migrate all error handling to use Result type" \
#     --branch "refactor/result-type" \
#     --max-turns 100
#
#   bash overnight-refactor.sh \
#     --task "add input validation to all API endpoints" \
#     --branch "feat/input-validation" \
#     --max-turns 50 \
#     --docker
#

set -euo pipefail

# Configuration
TASK=""
BRANCH=""
MAX_TURNS=100
USE_DOCKER=false
LOG_DIR="/tmp/claude-overnight"
COMMIT_INTERVAL=10  # Commit every N turns (approximate)
REPO_DIR=$(pwd)

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --task)
      TASK="$2"
      shift 2
      ;;
    --branch)
      BRANCH="$2"
      shift 2
      ;;
    --max-turns)
      MAX_TURNS="$2"
      shift 2
      ;;
    --docker)
      USE_DOCKER=true
      shift
      ;;
    --log-dir)
      LOG_DIR="$2"
      shift 2
      ;;
    --repo)
      REPO_DIR="$2"
      shift 2
      ;;
    --help)
      echo "Usage: overnight-refactor.sh --task <description> --branch <name> [--max-turns N] [--docker]"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$TASK" ]]; then
  echo "Error: --task is required"
  exit 1
fi

if [[ -z "$BRANCH" ]]; then
  BRANCH="refactor/overnight-$(date +%Y%m%d-%H%M%S)"
  echo "No branch specified, using: $BRANCH"
fi

# Setup
mkdir -p "$LOG_DIR"
LOG_FILE="${LOG_DIR}/overnight-$(date +%Y%m%d-%H%M%S).log"
START_TIME=$(date +%s)

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# ─── Pre-flight checks ───
log "=== Overnight Refactoring Session ==="
log "Task:       $TASK"
log "Branch:     $BRANCH"
log "Max turns:  $MAX_TURNS"
log "Docker:     $USE_DOCKER"
log "Log file:   $LOG_FILE"
log "Repository: $REPO_DIR"
log ""

# Check prerequisites
if ! command -v claude &>/dev/null; then
  log "Error: claude CLI not found in PATH"
  exit 1
fi

if ! git rev-parse --git-dir &>/dev/null; then
  log "Error: Not in a git repository"
  exit 1
fi

# Check for uncommitted changes
if ! git diff --quiet || ! git diff --cached --quiet; then
  log "Error: Uncommitted changes detected. Commit or stash them first."
  exit 1
fi

# ─── Create branch ───
log "Creating branch: $BRANCH"
CURRENT_BRANCH=$(git branch --show-current)
git checkout -b "$BRANCH" 2>/dev/null || git checkout "$BRANCH"
log "On branch: $(git branch --show-current)"

# ─── Run Claude ───
if [[ "$USE_DOCKER" == true ]]; then
  log "Starting Docker container..."

  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
  DOCKER_COMPOSE="${SCRIPT_DIR}/../docker/docker-compose.yml"

  if [[ -f "$DOCKER_COMPOSE" ]]; then
    TASK="$TASK" MAX_TURNS="$MAX_TURNS" \
      docker compose -f "$DOCKER_COMPOSE" run --rm claude-worker 2>&1 | tee -a "$LOG_FILE"
  else
    log "Error: docker-compose.yml not found at $DOCKER_COMPOSE"
    log "Falling back to direct execution..."
    USE_DOCKER=false
  fi
fi

if [[ "$USE_DOCKER" == false ]]; then
  log "Starting Claude session (direct mode)..."
  log ""

  # Build the prompt with safety instructions
  PROMPT="You are running in an autonomous overnight session. Your task:

${TASK}

IMPORTANT RULES:
1. Work methodically through the codebase, file by file
2. Make small, focused changes — one concern per edit
3. Run tests after each significant change (npm test or equivalent)
4. If tests fail, fix them before moving on
5. Commit your progress every few changes with descriptive messages
6. If you encounter something you're unsure about, add a TODO comment and move on
7. Do NOT push to remote — only local commits
8. Do NOT modify configuration files (.env, CI configs) unless directly related to the task
9. Do NOT delete files unless the task explicitly requires it
10. Stop if you encounter merge conflicts

After completing each file, commit with a message like:
refactor(<scope>): <what you changed>

Start by analyzing the codebase to understand the scope of work, then proceed systematically."

  # Run Claude with --dangerously-skip-permissions for unattended execution
  claude -p "$PROMPT" \
    --dangerously-skip-permissions \
    --max-turns "$MAX_TURNS" \
    2>&1 | tee -a "$LOG_FILE"
fi

# ─── Post-session ───
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
DURATION_MIN=$((DURATION / 60))

log ""
log "=== Session Complete ==="
log "Duration: ${DURATION_MIN} minutes"
log "Branch:   $BRANCH"
log ""

# Show summary of changes
COMMIT_COUNT=$(git log "$CURRENT_BRANCH..$BRANCH" --oneline 2>/dev/null | wc -l || echo "0")
FILES_CHANGED=$(git diff "$CURRENT_BRANCH..$BRANCH" --stat 2>/dev/null | tail -1 || echo "no changes")

log "Commits:  $COMMIT_COUNT"
log "Changes:  $FILES_CHANGED"
log ""
log "To review the changes:"
log "  git log --oneline $CURRENT_BRANCH..$BRANCH"
log "  git diff $CURRENT_BRANCH..$BRANCH"
log ""
log "To merge:"
log "  git checkout $CURRENT_BRANCH"
log "  git merge $BRANCH"
log ""
log "To discard:"
log "  git checkout $CURRENT_BRANCH"
log "  git branch -D $BRANCH"
log ""
log "Full log: $LOG_FILE"
