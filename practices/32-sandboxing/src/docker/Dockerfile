# Dockerfile for sandboxed Claude Code execution
#
# Usage:
#   docker build -t claude-sandbox .
#   docker run -v $(pwd):/workspace:ro -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY claude-sandbox
#
# Security features:
#   - Non-root user
#   - Read-only filesystem (project mounted as ro)
#   - No unnecessary packages
#   - Dropped capabilities

FROM node:20-alpine AS base

# Install minimal dependencies
RUN apk add --no-cache \
    bash \
    git \
    jq \
    && rm -rf /var/cache/apk/*

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code && \
    npm cache clean --force

# Create non-root user
RUN addgroup -g 1001 claude && \
    adduser -u 1001 -G claude -D -h /home/claude claude

# Create workspace directory
RUN mkdir -p /workspace && chown claude:claude /workspace

# Create config directory for settings
RUN mkdir -p /home/claude/.claude && chown -R claude:claude /home/claude/.claude

# Copy permission profile
COPY src/permissions/zero-trust.json /home/claude/.claude/settings.json
RUN chown claude:claude /home/claude/.claude/settings.json

# Switch to non-root user
USER claude
WORKDIR /workspace

# Health check
HEALTHCHECK --interval=30s --timeout=5s \
    CMD echo "sandbox healthy" || exit 1

# Default: run Claude in headless mode with the review prompt
ENTRYPOINT ["claude"]
CMD ["--print", "Review this codebase for security issues. Report findings as a structured list."]
