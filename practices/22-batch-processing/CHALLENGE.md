# Challenge: Batch Processing and Fan-Out

## Overview

Process multiple files and tasks in parallel using Claude Code. Learn to fan out work across parallel Claude instances and aggregate the results.

---

## Step 1: Try /batch

Use the `/batch` command to apply a transformation across multiple files.

### Tasks

1. Open Claude Code in interactive mode in this practice directory
2. Run the batch command:
   ```
   /batch "migrate all callback functions to async/await" in src/legacy/
   ```
3. Observe how Claude:
   - Identifies all files matching the pattern
   - Plans the transformation
   - Applies changes to each file
   - Reports results
4. Review the changes with `git diff`

### What /batch Does

1. Scans the target directory for matching files
2. Analyzes each file for the specified pattern
3. Applies the transformation to each file
4. Reports which files were changed and how

### Verification

- All three legacy modules should be updated
- Callback patterns should be converted to async/await
- The transformed code should be functionally equivalent
- No files outside the target directory should be modified

---

## Step 2: Manual Fan-Out

Review multiple directories in parallel using `xargs -P`.

### Tasks

1. Read `src/scripts/parallel-review.sh` to understand the approach
2. Run it:
   ```bash
   bash src/scripts/parallel-review.sh src/legacy/
   ```
3. Understand the fan-out pattern:
   ```bash
   # Find all .ts files and review them in parallel (4 at a time)
   find src/ -name "*.ts" -type f | \
     xargs -P 4 -I {} bash -c '
       claude -p "review this file for code quality" \
         --allowedTools Read --max-turns 3 \
         --output-format json < {} > "/tmp/review-$(basename {}).json"
     '
   ```
4. Try adjusting the parallelism level (`-P` flag)

### Key Considerations

- **Parallelism level**: Start with `-P 4`, adjust based on API rate limits
- **Rate limiting**: Too many parallel requests may hit API limits
- **Isolation**: Each Claude instance is independent (no shared context)
- **Output management**: Write results to separate files, aggregate later

### Verification

- Multiple reviews should run simultaneously
- Each review should complete independently
- Results should be written to separate output files

---

## Step 3: Aggregate Results

Combine JSON outputs from parallel reviews into a single report.

### Tasks

1. Read `src/scripts/aggregate-results.sh`
2. Run it after the parallel review:
   ```bash
   bash src/scripts/aggregate-results.sh /tmp/review-*.json
   ```
3. The script should:
   - Parse each JSON result file
   - Combine findings into a single report
   - Sort by severity
   - Output a summary with statistics
4. Try different output formats:
   ```bash
   bash src/scripts/aggregate-results.sh --format markdown /tmp/review-*.json
   bash src/scripts/aggregate-results.sh --format json /tmp/review-*.json
   ```

### Verification

- All individual results should be included in the aggregate
- The summary should show total findings by severity
- The report should be easy to read and actionable

---

## Step 4: Build a Batch Migration Script

Create a comprehensive migration script that transforms legacy code.

### Tasks

1. Read `src/scripts/batch-migrate.sh`
2. Understand the migration workflow:
   - Discover files matching a pattern
   - Create a backup branch
   - Fan out Claude calls for migration
   - Validate each migration (run tests)
   - Aggregate results
3. Run it on the legacy modules:
   ```bash
   bash src/scripts/batch-migrate.sh \
     --pattern "src/legacy/*.ts" \
     --transform "convert callbacks to async/await" \
     --parallel 3
   ```
4. Verify the migrations:
   ```bash
   # Check the diff
   git diff

   # Run tests if available
   npm test
   ```

### Verification

- All matching files should be transformed
- A backup branch should exist with the original code
- Each file's transformation should be validated
- A summary report should be generated

---

## Step 5: Compare Serial vs Parallel

Measure the performance difference between serial and parallel execution.

### Tasks

1. Time serial execution:
   ```bash
   time for file in src/legacy/*.ts; do
     claude -p "review $file" --allowedTools Read --max-turns 3 --output-format json > /dev/null
   done
   ```
2. Time parallel execution:
   ```bash
   time find src/legacy/ -name "*.ts" | \
     xargs -P 3 -I {} bash -c \
       'claude -p "review {}" --allowedTools Read --max-turns 3 --output-format json > /dev/null'
   ```
3. Calculate the speedup:
   ```
   Speedup = Serial Time / Parallel Time
   ```
4. Try different parallelism levels and observe diminishing returns

### Expected Results

- With 3 files and `-P 3`: ~3x speedup
- With more files: speedup approaches the parallelism level
- Diminishing returns beyond API rate limits

### Verification

- Parallel execution should be significantly faster
- Results should be identical between serial and parallel
- Rate limit errors should be handled gracefully

---

## Bonus Challenges

1. **Smart batching**: Group files by type and apply different transforms per group
2. **Progress bar**: Add a progress indicator for long-running batch operations
3. **Retry logic**: Automatically retry failed Claude calls with exponential backoff
4. **Cost tracking**: Track and report total API cost across all parallel calls
5. **Dependency-aware batching**: Order file processing based on import dependencies

---

## Key Takeaways

- `/batch` provides a high-level way to apply transformations across files
- `xargs -P` enables manual fan-out for custom parallel workflows
- Result aggregation is essential for making sense of parallel outputs
- Parallelism level should balance speed with API rate limits
- Always validate transformations (tests, type checking) after batch operations
