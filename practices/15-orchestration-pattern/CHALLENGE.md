# Challenge: Command→Agent→Skill Orchestration

## Step 1: Understanding the 3-Layer Pattern

### Why 3 Layers?

Handling complex tasks with a single prompt leads to the following problems:
- The prompt becomes too long and Claude ignores parts of it
- Not reusable (must explain from scratch every time)
- Difficult to test and debug

By separating into 3 layers:
- **Skill**: Reusable knowledge module (shared by multiple Agents)
- **Agent**: Reusable execution module (shared by multiple Commands)
- **Command**: User-friendly entry point

### Data Flow

```
User → /analyze src/
         ↓
  Command (analyze.md)
    - Argument parsing: target = "src/"
    - Call Agent
         ↓
  Agent (analyzer-agent.md)
    - Load Skill: code-analyzer
    - File discovery: src/**/*.ts
    - Analyze each file
    - Generate report
         ↓
  Skill (SKILL.md)
    - Provide analysis criteria
    - Scoring rules
    - Pattern matching rules
         ↓
  Result → Output report to user
```

### Exercise

Examine the example in the `src/example-orchestration/` directory:

```bash
ls -la src/example-orchestration/.claude/
```

Identify each file's role and trace how data flows through the pipeline.

---

## Step 2: Create a Skill — Code Analysis Knowledge

A Skill is a knowledge base that Claude references when performing a specific task.

### Create a Skill in the Project Root

```bash
mkdir -p .claude/skills/code-analyzer
```

Create the `.claude/skills/code-analyzer/SKILL.md` file:

```markdown
# Code Analyzer Skill

## Purpose
Analyzes TypeScript/JavaScript code quality and assigns scores.

## Analysis Criteria

### 1. Complexity — 30 points
- Lines per function: 20 or fewer = 10 pts, 50 or fewer = 5 pts, over 50 = 0 pts
- Nesting depth: 3 levels or fewer = 10 pts, 5 levels or fewer = 5 pts
- Number of parameters: 3 or fewer = 10 pts, 5 or fewer = 5 pts

### 2. Maintainability — 30 points
- Type safety: no use of `any` = 10 pts
- Error handling: appropriate use of try-catch = 10 pts
- Naming: meaningful variable/function names = 10 pts

### 3. Best Practices — 40 points
- Single Responsibility Principle compliance = 10 pts
- DRY principle (no duplicate code) = 10 pts
- Tests exist = 10 pts
- Documentation (JSDoc, etc.) = 10 pts

## Output Format

Report for each file in the following format:

| File | Complexity | Maintainability | Best Practices | Total | Grade |
|------|--------|-----------|---------|------|------|
| file.ts | X/30 | X/30 | X/40 | X/100 | A~F |

Grade criteria: A(90+), B(80+), C(70+), D(60+), F(below 60)
```

### Checklist
- [ ] Does SKILL.md define specific analysis criteria
- [ ] Are scoring rules clear
- [ ] Is the output format defined

---

## Step 3: Create an Agent — Analysis Executor

An Agent uses the Skill's knowledge to perform the actual work.

### Create the Agent File

```bash
mkdir -p .claude/agents
```

Create the `.claude/agents/analyzer-agent.md` file:

```markdown
# Code Analyzer Agent

## Role
An agent that performs code quality analysis.

## Preloaded Skills
- code-analyzer: .claude/skills/code-analyzer/SKILL.md

## Instructions

1. Find all .ts, .tsx, .js, .jsx files in the target directory
2. Analyze each file according to the code-analyzer Skill criteria
3. Calculate scores for each file
4. Generate an overall summary report

## Execution Steps

### Step 1: File Discovery
Collect the list of files to analyze from the target path.
Exclude test files (*.test.ts, *.spec.ts) from the analysis.

### Step 2: Individual Analysis
Read each file and assign scores based on the Skill criteria.

### Step 3: Report Generation
- Detailed score table per file
- Overall average score
- Top 3 files most in need of improvement
- Specific improvement suggestions

## Output
Output the analysis results in markdown table format.
```

### Checklist
- [ ] Does the Agent reference the Skill
- [ ] Are execution steps clearly defined
- [ ] Are input (target path) and output (report) formats defined

---

## Step 4: Create a Command — User Entry Point

A Command is the entry point that users execute with the `/analyze` slash command.

### Create the Command File

```bash
mkdir -p .claude/commands
```

Create the `.claude/commands/analyze.md` file:

```markdown
# /analyze Command

Analyze code quality for the specified path.

## Usage
/analyze <target-path>

## Arguments
- $ARGUMENTS: Directory or file path to analyze (default: src/)

## Execution

1. Verify the target path: $ARGUMENTS (defaults to src/ if not specified)
2. Call analyzer-agent to perform the code analysis
3. Format and display the analysis results

## Agent Delegation
This analysis task is delegated to analyzer-agent.
analyzer-agent analyzes code according to the code-analyzer Skill criteria.

## Expected Output
- Quality score table per file
- Overall project average score
- Top 3 improvement priorities
- Specific improvement suggestions
```

### Checklist
- [ ] Does it accept arguments using $ARGUMENTS
- [ ] Does it delegate the task to an Agent
- [ ] Is the output format for the user defined

---

## Step 5: Full Pipeline Test

### 5-1. Run the Command

```bash
claude
> /analyze src/
```

### 5-2. Verify the Results

Confirm that Claude goes through the following process:

1. Command receives `src/` via `$ARGUMENTS`
2. Agent discovers files in the `src/` directory
3. Each file is analyzed according to the Skill criteria
4. Scores and report are output to the user

### 5-3. Test with Different Paths

```bash
> /analyze lib/
> /analyze src/utils/
```

### 5-4. Create Your Own Pipeline

Using the patterns you learned, create a new orchestration:

**Example ideas:**
- `/review` — Automated code review (review-skill + review-agent + review command)
- `/docs` — Automated documentation generation (docs-skill + docs-agent + docs command)
- `/refactor` — Refactoring suggestions (refactor-skill + refactor-agent + refactor command)

---

## Success Criteria

- [ ] Skill defines specific analysis criteria
- [ ] Agent performs work by referencing the Skill
- [ ] Command accepts user input and delegates to the Agent
- [ ] Running `/analyze src/` outputs an analysis report
- [ ] Each of the 3 layers is independently reusable

## Key Takeaways

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Reusability**: Skills can be shared by multiple Agents; Agents can be shared by multiple Commands
3. **Testability**: Each layer can be tested independently
4. **Extensibility**: When adding a new Command, existing Agents and Skills can be reused
5. **Maintainability**: When analysis criteria change, only the Skill needs to be modified
