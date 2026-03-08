# Challenge: Scatter-Gather Research System

## Step 1: Design the Scatter-Gather Architecture

Design the architecture for a research system with a lead agent and multiple research workers.

### Architecture Components

**Lead Agent:**
- Receives a research question
- Decomposes it into 3-5 independent subtopics
- Dispatches subtopics to worker agents
- Gathers results from all workers
- Synthesizes findings into a comprehensive report

**Worker Agents:**
- Receive a single, focused research subtopic
- Research the subtopic thoroughly within the codebase
- Produce structured findings
- Operate independently (no inter-worker communication)

### Data Flow
```
Input: "How is error handling done across the codebase?"
  ↓
Lead decomposes:
  1. "Error handling patterns in API layer"
  2. "Error handling in data access layer"
  3. "Client-side error handling"
  ↓
Workers research (parallel):
  Worker 1 → API error patterns report
  Worker 2 → Data layer error patterns report
  Worker 3 → Client error patterns report
  ↓
Lead synthesizes:
  → Comprehensive error handling report
```

---

## Step 2: Implement in Python

Build the scatter-gather system in Python using the Agent SDK.

### Files
- `src/python/research_lead.py` — Lead agent logic
- `src/python/research_worker.py` — Worker agent logic
- `src/python/scatter_gather.py` — Main orchestration

### Lead Agent (`research_lead.py`)

```python
# The lead agent should:
# 1. Accept a research question
# 2. Decompose it into subtopics (using Claude to generate the decomposition)
# 3. Return a list of focused research tasks

class ResearchLead:
    def decompose(self, question: str) -> list[str]:
        """Break a research question into subtopics."""
        ...

    def synthesize(self, question: str, findings: list[dict]) -> str:
        """Combine worker findings into a comprehensive report."""
        ...
```

### Worker Agent (`research_worker.py`)

```python
# The worker agent should:
# 1. Accept a single research subtopic
# 2. Research it within the codebase (read-only)
# 3. Return structured findings

class ResearchWorker:
    def research(self, subtopic: str, codebase_path: str) -> dict:
        """Research a single subtopic and return findings."""
        ...
```

### Orchestrator (`scatter_gather.py`)

```python
# The orchestrator should:
# 1. Create the lead and workers
# 2. Lead decomposes the question
# 3. Workers research in parallel (using threads or asyncio)
# 4. Lead synthesizes the results

def scatter_gather(question: str, codebase_path: str) -> str:
    lead = ResearchLead()
    subtopics = lead.decompose(question)

    # Scatter: run workers in parallel
    with ThreadPoolExecutor(max_workers=len(subtopics)) as executor:
        futures = [
            executor.submit(ResearchWorker().research, subtopic, codebase_path)
            for subtopic in subtopics
        ]
        findings = [f.result() for f in futures]

    # Gather: synthesize results
    report = lead.synthesize(question, findings)
    return report
```

---

## Step 3: Implement in TypeScript

Build the same scatter-gather system in TypeScript.

### Files
- `src/typescript/research-lead.ts` — Lead agent logic
- `src/typescript/research-worker.ts` — Worker agent logic
- `src/typescript/scatter-gather.ts` — Main orchestration

### Key Difference: Parallel Execution
```typescript
// TypeScript uses Promise.all for parallel execution
const findings = await Promise.all(
  subtopics.map((subtopic) =>
    new ResearchWorker().research(subtopic, codebasePath)
  )
);
```

---

## Step 4: Add Result Synthesis

Enhance the lead agent's synthesis capabilities.

### Synthesis Requirements
The lead agent should produce a report with:

1. **Executive Summary** — 2-3 sentence overview
2. **Key Findings** — Bullet points of the most important discoveries
3. **Detailed Analysis** — Organized by subtopic, with cross-references
4. **Patterns Identified** — Common themes across subtopics
5. **Contradictions** — Where worker findings disagree
6. **Recommendations** — Actionable next steps
7. **Confidence Assessment** — How confident is each finding

### Synthesis Prompt Template
```
You are a research lead synthesizing findings from {n} research workers.

Original question: {question}

Worker findings:
{formatted_findings}

Produce a comprehensive report that:
1. Identifies the most important findings
2. Notes patterns across the subtopics
3. Highlights any contradictions between workers
4. Provides actionable recommendations
5. Rates confidence for each finding (low/medium/high)
```

---

## Step 5: Compare with Single-Agent Research

Run the same research question with a single agent and compare quality.

### Single Agent Approach
```python
def single_agent_research(question: str, codebase_path: str) -> str:
    agent = Agent()
    result = agent.query(
        prompt=f"Research: {question}\nCodebase: {codebase_path}",
        allowed_tools=["Read", "Glob", "Grep"],
    )
    return result.text
```

### Comparison Criteria
| Criterion | Single Agent | Scatter-Gather |
|-----------|-------------|----------------|
| Breadth of coverage | ? | ? |
| Depth per topic | ? | ? |
| Total time | ? | ? |
| Total tokens used | ? | ? |
| Actionability of findings | ? | ? |
| Missed areas | ? | ? |

### Evaluation Questions
1. Did scatter-gather find things the single agent missed?
2. Did the single agent find things scatter-gather missed?
3. Which approach was faster?
4. Which approach used fewer tokens?
5. Which report was more actionable?

---

## Success Criteria

- [ ] Lead agent correctly decomposes research questions into subtopics
- [ ] Worker agents produce focused, structured findings
- [ ] Workers execute in parallel (not sequentially)
- [ ] Lead agent synthesizes findings into a coherent report
- [ ] Report includes cross-references between subtopics
- [ ] Both Python and TypeScript implementations work
- [ ] Comparison with single-agent shows clear trade-offs

## Bonus Challenges

1. **Adaptive decomposition**: Lead adjusts subtopic count based on question complexity
2. **Worker specialization**: Different workers use different search strategies
3. **Iterative deepening**: If initial findings are shallow, send workers back for more
4. **Confidence scoring**: Workers rate their own confidence, lead weighs accordingly
5. **Caching**: Cache worker results for repeated research on same codebase
