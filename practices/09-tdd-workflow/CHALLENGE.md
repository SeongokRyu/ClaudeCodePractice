# Challenge: TDD Workflow

## Step 1: Confirm Failing Tests (Red)

Tests for the shopping cart module have already been written in `src/test_shopping_cart.py`. First, confirm that the tests fail.

```bash
uv run pytest src/
```

All tests should fail. This is the Red phase of TDD.

### Prompts to Try with Claude

```
Look at the tests for the shopping cart module that has no implementation yet.
Read the tests and summarize what features are needed.
```

---

## Step 2: Make the Tests Pass (Green)

Ask Claude for the implementation. The key is to **write only the implementation without changing the tests**.

### Prompts to Try with Claude

```
Implement src/shopping_cart.py so that all tests in
src/test_shopping_cart.py pass.

Do not modify the tests. Only write the implementation.
```

After implementation, run the tests to confirm they all pass.

```bash
uv run pytest src/
```

---

## Step 3: Refactoring (Refactor)

Once all tests pass, improve the code quality. The tests serve as a safety net.

### Prompts to Try with Claude

```
Refactor the shopping_cart.py implementation.
- Improve code readability
- Remove duplication
- Strengthen type safety
- Improve error handling

All tests must continue to pass.
After refactoring, run uv run pytest src/ to verify.
```

---

## Step 4: Ralph Loop

The Ralph Loop is a pattern where you give Claude **success criteria** and let it iterate autonomously.

### Prompts to Try with Claude

```
Repeat the following process:
1. Run uv run pytest src/
2. If any tests fail, analyze the cause and fix it
3. Run uv run pytest src/ again
4. Repeat until all tests pass

Don't stop in the middle — let me know the results once all tests pass.
```

### Advanced: Adding New Features + Ralph Loop

```
Add the following features to the shopping cart:
- Apply coupon codes (SAVE10 = 10% discount, SAVE20 = 20% discount)
- Change item quantity in the cart
- Minimum order amount check (error if less than 10,000 won)

Write tests for each feature first,
then write the implementation to pass the tests.
Verify with uv run pytest src/, and if any fail, fix them and repeat until all tests pass.
```

---

## Completion Criteria

- [ ] Step 1: Confirmed that all tests fail
- [ ] Step 2: Implemented shopping_cart.py so all tests pass
- [ ] Step 3: All tests still pass after refactoring
- [ ] Step 4: Experienced Claude solving problems autonomously with the Ralph Loop

## Reflection Questions

1. In which phase of the TDD cycle did Claude help the most?
2. What was the difference between using the Ralph Loop versus giving instructions one at a time?
3. How much safer did refactoring feel when you had tests in place?
