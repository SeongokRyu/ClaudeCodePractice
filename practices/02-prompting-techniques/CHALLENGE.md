# Challenge: Prompting Techniques Hands-On

## Overview

`src/calculator.py` has intentionally hidden bugs and edge cases.
Use various prompting techniques to improve the code together with Claude.

---

## Step 1: Bad Prompts vs Good Prompts

### 1-1. Try a Bad Prompt

Ask Claude the following:

```
Take a look at this code. Something seems off, fix it.
```

Observe Claude's response. What did it do? Are the changes accurate?

### 1-2. Try a Good Prompt

This time, make a specific request:

```
Please review the divide function in src/calculator.py.
- Check whether the error handling for division by zero is correct
- If there is a problem, fix it to raise an exception
- After fixing, run pytest to confirm existing tests still pass
```

**Observation point**: Compare the difference in results between the two prompts.

---

## Step 2: Providing Verification Criteria

Ask Claude for verification alongside the feature implementation:

```
Regarding the format_number function in src/calculator.py:
1. Analyze what edge cases are currently not handled
2. Modify the code to handle the missing edge cases
3. Add tests for the new edge cases to src/test_calculator.py
4. Run pytest to confirm all tests pass

Verification criteria:
- Negative numbers should be formatted correctly
- Numbers with decimal points should be handled correctly
- Very large and very small numbers should be handled
```

**Observation point**: Notice how Claude works more systematically when verification criteria are provided.

---

## Step 3: Interview Technique

Ask Claude to ask questions first instead of implementing directly:

```
I want to add a power (exponentiation) function to calculator.py.
Before implementing, please ask any questions you have about the requirements first.
```

Example questions Claude might ask:
- Should negative exponents be supported?
- Should decimal exponents be supported?
- How should results that are too large be handled?
- How should 0 to the power of 0 be handled?

After answering the questions, notice how Claude provides a more accurate implementation.

---

## Step 4: Structured Prompt

Write a structured prompt that combines all techniques:

```
Role: Please conduct a code review as a senior Python developer.

Context: src/calculator.py is a basic calculator module.
It currently has add, subtract, multiply, divide, and format_number functions implemented.

Tasks:
1. Review the entire code and list improvements
2. Fix any missing error handling
3. Add docstrings to each function
4. Add missing test cases

Constraints:
- Do not break existing tests
- Do not change function signatures
- Use Python 3.10+ syntax

Expected output:
- Modified src/calculator.py
- Updated src/test_calculator.py
- Summary of changes

Verification:
- Run pytest to confirm all tests pass
- Confirm that newly added tests actually verify edge cases
```

**Observation point**: Notice how structured prompts affect Claude's work quality.

---

## Completion Checklist

- [ ] Experienced the difference in results between bad and good prompts
- [ ] Wrote a prompt with verification criteria and confirmed Claude's systematic work
- [ ] Used the interview technique to get Claude to ask questions first
- [ ] Wrote a structured prompt and obtained high-quality results

## Tips

- Including "why" in your prompt helps Claude make better judgments
- The more specific the verification criteria, the better (e.g., "tests pass" > "works well")
- The interview technique is especially effective for complex feature implementations
- Structured prompts may feel cumbersome at first, but they reduce rework
