# AI Native Camp - Cohort 1

- **URL**: https://github.com/ai-native-camp/camp-1
- **Stars**: 196 | **Duration**: 2026-02-14 ~ 2026-02-21 (7 days)
- **Features**: Intensive Claude Code camp for non-developers. Curriculum structured as Skills (learn how to create Skills by using Skills)
- **Location**: Naver D2SF

---

## Curriculum

| Day | Skill | Topic |
|-----|-------|-------|
| 1 | day1-onboarding | Claude Code installation + 7 core features |
| 2 | day2-supplement-mcp | MCP deep dive |
| 2 | day2-create-context-sync-skill | Build your own Context Sync skill |
| 3 | coming soon | Requirements clarification |
| 4 | day4-wrap-and-analyze | session-wrap + history-insight + session-analyzer |
| 5 | day5-fetch-and-digest | fetch-tweet, fetch-youtube, content-digest |
| 6 | day6-prd-submit | PRD writing and GitHub PR submission |
| 7 | coming soon | Graduation |

---

## Day 1: Onboarding - 7 Core Features

### Block 0: Environment Setup
- Claude Code installation, Terminal/Git/GitHub basics

### Block 1: Hands-on Demo
- Experience Claude Code's capabilities firsthand

### Block 2: Why CLI?
- Reasons for choosing CLI over GUI

### Block 3: 7 Core Features
1. **CLAUDE.md**: The project's "constitution"
2. **Skill**: Reusable workflow definitions
3. **MCP**: Protocol for connecting external tools/services
4. **Subagent**: Delegation to sub-agents
5. **Agent Teams**: Multi-agent team collaboration
6. **Hook**: Deterministic automation
7. **Plugin**: Extension features

### Block 4: CLI/Git/GitHub Basics
- Basic commands, version control fundamentals

---

## Day 2: MCP + Context Sync Skill

### MCP Deep Dive
- Understanding the MCP concept
- Server installation methods
- Using the /mcp command
- Popular server introductions
- Plugin MCP

### Building a Context Sync Skill (Core Hands-on)
Step-by-step process:
1. **Tool Selection** (block0): Decide which MCP/API to use
2. **Project Exploration** (block1): Understand the existing codebase
3. **Tool Integration** (block2): Actual MCP/API integration
4. **Parallel Collection** (block3): Collect data from multiple sources simultaneously
5. **Output Formatting** (block4): Organize results in markdown
6. **Completion** (block5): Final skill verification and wrap-up

---

## Day 4: Wrap & Analyze

### Core Concepts
- Understanding multi-agent concepts
- Building skills to automatically organize session records

### Hands-on Content
1. **session-wrap skill**: Automatically summarize work when a session ends
2. **history-insight**: Extract insights from past session history
3. **session-analyzer**: Analyze session patterns (which tasks consume the most time)

---

## Day 5: Fetch & Digest

### Building a Content Pipeline
1. **fetch-tweet**: Fetch tweet content
2. **fetch-youtube**: Fetch YouTube content
3. **content-digest**: Content translation + Quiz-First learning
4. **Integration**: Connect the entire pipeline

---

## Key Insights

### "Skills as Curriculum" Approach
- Interactive learning where Claude teaches directly, rather than lecture slides
- Run `/day1-onboarding` and Claude guides you
- The act of building a Skill is itself the learning process

### Installation
```bash
npx skills add ai-native-camp/camp-1 --agent claude-code --yes
```

### Notes for Practice Design
- Difficulty designed to be accessible for non-developers
- "Learn by building" pattern is effective
- Progressive structure where each Day builds on the previous one
- Hands-on exercises that produce tangible outputs (skills)
