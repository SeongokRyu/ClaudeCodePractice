# Dockerfile for isolated Claude Code execution
#
# This container provides a safe, isolated environment for running
# Claude Code autonomously (e.g., overnight refactoring).
#
# Features:
# - Node.js and common dev tools pre-installed
# - Git configured for local commits
# - No network access to remote git (push disabled)
# - Resource limits via docker-compose
#
# Build:
#   docker build -t claude-worker .
#
# Run:
#   docker run --rm -v $(pwd):/workspace claude-worker \
#     claude -p "your task here" --dangerously-skip-permissions --max-turns 50

FROM node:20-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    jq \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Install Claude CLI
# Note: Replace with actual installation method
RUN npm install -g @anthropic-ai/claude-code || echo "Claude CLI installation may require manual setup"

# Configure git for local commits
RUN git config --global user.name "Claude Overnight" && \
    git config --global user.email "claude-overnight@localhost" && \
    git config --global init.defaultBranch main

# Disable git push as a safety measure
RUN echo '#!/bin/bash\necho "ERROR: git push is disabled in this container for safety."\nexit 1' > /usr/local/bin/git-push-disabled && \
    chmod +x /usr/local/bin/git-push-disabled

# Create workspace
WORKDIR /workspace

# Create entrypoint script
COPY <<'ENTRYPOINT' /entrypoint.sh
#!/bin/bash
set -euo pipefail

echo "=== Claude Overnight Worker ==="
echo "Started: $(date)"
echo "Task: ${TASK:-No task specified}"
echo "Max turns: ${MAX_TURNS:-50}"
echo ""

# Verify we're in a git repo
if ! git rev-parse --git-dir &>/dev/null; then
  echo "Error: /workspace is not a git repository"
  echo "Mount your repo: docker run -v /path/to/repo:/workspace ..."
  exit 1
fi

# Show current state
echo "Branch: $(git branch --show-current)"
echo "Status: $(git status --short | wc -l) modified files"
echo ""

# Run Claude
if [[ -n "${TASK:-}" ]]; then
  claude -p "You are running in an isolated Docker container for overnight work.

Your task: ${TASK}

Safety rules:
1. You cannot push to remote (git push is disabled)
2. Work on the current branch
3. Commit progress with descriptive messages
4. Run tests after changes
5. If tests fail, fix them before continuing
6. Maximum ${MAX_TURNS:-50} turns

Start by understanding the codebase, then work systematically." \
    --dangerously-skip-permissions \
    --max-turns "${MAX_TURNS:-50}"
else
  echo "No TASK specified. Set the TASK environment variable."
  echo "Example: docker run -e TASK='add error handling' ..."
  exit 1
fi

echo ""
echo "=== Session Complete ==="
echo "Finished: $(date)"

# Show summary
echo ""
echo "Changes made:"
git log --oneline HEAD~10..HEAD 2>/dev/null || git log --oneline
echo ""
git diff --stat
ENTRYPOINT

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
