# Practice 28: Scatter-Gather Research System

## Goal
Build a research system using the scatter-gather pattern: a lead agent decomposes a research question, multiple worker agents research in parallel, and the lead agent synthesizes the findings into a comprehensive report.

## Prerequisites
- Practice 24 (Agent SDK Introduction)

## Time
90-120 minutes

## Difficulty
★★★

## What You'll Learn
- The scatter-gather architectural pattern
- Lead agent design (decompose, delegate, synthesize)
- Worker agent design (focused, independent research)
- Parallel agent execution
- Result synthesis and quality assessment
- Comparing multi-agent vs. single-agent research quality

## Project Structure
```
practices/28-scatter-gather/
├── README.md
├── CHALLENGE.md
├── src/
│   ├── python/
│   │   ├── scatter_gather.py
│   │   ├── research_lead.py
│   │   └── research_worker.py
│   └── typescript/
│       ├── scatter-gather.ts
│       ├── research-lead.ts
│       └── research-worker.ts
```

## Key Concepts

### Scatter-Gather Pattern
```
                    ┌──────────┐
                    │   Lead   │
                    │  Agent   │
                    └────┬─────┘
                         │ decompose
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         ┌─────────┐ ┌─────────┐ ┌─────────┐
         │ Worker  │ │ Worker  │ │ Worker  │
         │   #1    │ │   #2    │ │   #3    │
         └────┬────┘ └────┬────┘ └────┬────┘
              │          │          │
              └──────────┼──────────┘
                         │ gather
                    ┌────▼─────┐
                    │   Lead   │
                    │  Agent   │
                    │(synthesize)│
                    └──────────┘
```

### Why Scatter-Gather Works for Research
- **Depth**: Each worker dives deep into one subtopic
- **Breadth**: Multiple workers cover more ground
- **Independence**: Workers don't influence each other's findings
- **Synthesis**: Lead agent combines diverse perspectives
- **Parallelism**: Workers run simultaneously for faster results

### Agent Roles
| Agent | Responsibility | Tools | Model |
|-------|---------------|-------|-------|
| Lead | Decompose question, synthesize results | All | sonnet |
| Worker | Research one subtopic deeply | Read-only | haiku |
