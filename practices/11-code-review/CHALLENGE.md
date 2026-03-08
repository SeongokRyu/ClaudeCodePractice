# Challenge: Code Review

## Step 1: Basic Review

Ask Claude for the simplest form of review on `src/api_handler.py`.

### Prompts to Try with Claude

```
Review src/api_handler.py.
```

Observe the level of feedback Claude provides. This is your baseline.

---

## Step 2: Role-Based Review

Ask for a review of the same code from the perspective of a specific role.

### Prompts to Try with Claude

```
You are a senior security engineer with 10 years of experience.
Review src/api_handler.py from a security perspective based on OWASP Top 10.
Assign a severity level (Critical/High/Medium/Low) to each vulnerability.
```

Compare with the results from Step 1. What difference does assigning a role make?

---

## Step 3: Quantitative Assessment

Ask Claude to score the code.

### Prompts to Try with Claude

```
Rate src/api_handler.py on a 1-5 scale for the following criteria:

1. Security: SQL injection, XSS, authentication/authorization, etc.
2. Performance: Efficiency, caching, optimization
3. Maintainability: Readability, modularity, documentation
4. Error Handling: Exception handling, input validation
5. Testability: Dependency injection, mockability

Explain each score in 1-2 lines, and provide a total score with improvement priorities.
```

---

## Step 4: Self-Review

Have Claude write code, then review it from a different perspective.

### Prompts to Try with Claude

First, have it write the code:
```
Write an improved version that fixes the issues in src/api_handler.py.
```

Then request a self-review:
```
Review the improved version you just wrote from the perspective of a tough code reviewer.
In particular:
- Are there any missed edge cases?
- Are there areas that could be further improved?
- Are there any new problems that this code could introduce?
```

---

## Step 5: Checklist Review

Perform a systematic review based on a security checklist.

### Prompts to Try with Claude

```
Review src/api_handler.py using the following security checklist.
Mark each item as PASS, FAIL, or N/A.

Security Checklist:
- [ ] Is all user input validated/sanitized?
- [ ] Is SQL/NoSQL injection prevention in place?
- [ ] Are API keys or secrets not hardcoded?
- [ ] Is proper error handling in place? (No internal information exposed in error messages?)
- [ ] Are authentication/authorization checks in place?
- [ ] Is rate limiting implemented?
- [ ] Is CORS configuration appropriate?
- [ ] Is logging appropriate? (No sensitive information being logged?)
- [ ] Are timeouts configured?
- [ ] Are there no known vulnerabilities in dependencies?
```

---

## Completion Criteria

- [ ] Step 1: Performed a basic review and established baseline feedback
- [ ] Step 2: Obtained deeper security analysis with role-based review
- [ ] Step 3: Performed systematic evaluation using quantitative scores
- [ ] Step 4: Experienced AI critically analyzing its own code through self-review
- [ ] Step 5: Performed systematic review using a checklist-based approach

## Reflection Questions

1. Which of the 5 review patterns did you find most useful?
2. How did the depth of the review change when you assigned a role?
3. In the self-review pattern, how well did Claude critique its own code?
4. How would you integrate these patterns into your actual code review workflow?
