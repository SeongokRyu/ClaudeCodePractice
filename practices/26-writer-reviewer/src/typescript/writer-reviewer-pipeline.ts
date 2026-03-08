/**
 * Practice 26: Writer/Reviewer Pipeline — TypeScript Agent SDK Implementation
 *
 * A complete writer/reviewer collaboration pipeline:
 * 1. Writer implements a feature
 * 2. Reviewer reviews the implementation
 * 3. Writer fixes issues (loop until APPROVED or max iterations)
 * 4. Verifier runs tests as final gate
 */

import { Agent } from "@anthropic-ai/claude-agent-sdk";

// ── Types ────────────────────────────────────────────────────────

enum Verdict {
  APPROVED = "APPROVED",
  CHANGES_REQUESTED = "CHANGES_REQUESTED",
  UNKNOWN = "UNKNOWN",
}

interface ReviewResult {
  verdict: Verdict;
  qualityScore: number;
  feedback: string;
  rawText: string;
}

interface VerificationResult {
  passed: boolean;
  totalTests: number;
  passedTests: number;
  failedTests: number;
  rawText: string;
}

// ── Parsers ──────────────────────────────────────────────────────

function parseReview(reviewText: string): ReviewResult {
  let verdict = Verdict.UNKNOWN;
  if (
    reviewText.includes("APPROVED") &&
    !reviewText.includes("CHANGES_REQUESTED")
  ) {
    verdict = Verdict.APPROVED;
  } else if (reviewText.includes("CHANGES_REQUESTED")) {
    verdict = Verdict.CHANGES_REQUESTED;
  }

  const scoreMatch = reviewText.match(/Quality Score:\s*(\d+)\/10/);
  const qualityScore = scoreMatch ? parseInt(scoreMatch[1], 10) : 0;

  return {
    verdict,
    qualityScore,
    feedback: reviewText,
    rawText: reviewText,
  };
}

function parseVerification(verificationText: string): VerificationResult {
  const passed =
    verificationText.includes("PASS") &&
    !verificationText.replace("Failed: 0", "").includes("FAIL");

  const totalMatch = verificationText.match(/Total:\s*(\d+)/);
  const passedMatch = verificationText.match(/Passed:\s*(\d+)/);
  const failedMatch = verificationText.match(/Failed:\s*(\d+)/);

  return {
    passed,
    totalTests: totalMatch ? parseInt(totalMatch[1], 10) : 0,
    passedTests: passedMatch ? parseInt(passedMatch[1], 10) : 0,
    failedTests: failedMatch ? parseInt(failedMatch[1], 10) : 0,
    rawText: verificationText,
  };
}

// ── Agent Factories ──────────────────────────────────────────────

function createWriterAgent(): Agent {
  return new Agent();
}

function createReviewerAgent(): Agent {
  return new Agent();
}

function createVerifierAgent(): Agent {
  return new Agent();
}

// ── Pipeline ─────────────────────────────────────────────────────

async function runPipeline(
  featureRequest: string,
  projectPath: string = "src/project",
  maxIterations: number = 3
): Promise<boolean> {
  const writer = createWriterAgent();
  const reviewer = createReviewerAgent();
  const verifier = createVerifierAgent();

  // ── Phase 1: Writer implements the feature ───────────────────
  console.log("=".repeat(60));
  console.log("PHASE 1: Writer — Implementing feature");
  console.log("=".repeat(60));

  const writerResult = await writer.query({
    prompt:
      `Implement the following feature in ${projectPath}:\n\n` +
      `${featureRequest}\n\n` +
      `Follow existing code patterns. Write tests. Run tests to verify.`,
    systemPrompt: { preset: "claude_code" },
  });
  console.log(writerResult.text.substring(0, 500));

  // ── Phase 2: Review/Fix Loop ─────────────────────────────────
  let approved = false;

  for (let iteration = 1; iteration <= maxIterations; iteration++) {
    console.log(`\n${"=".repeat(60)}`);
    console.log(
      `PHASE 2: Reviewer — Review iteration ${iteration}/${maxIterations}`
    );
    console.log("=".repeat(60));

    const reviewResult = await reviewer.query({
      prompt:
        `Review the code in ${projectPath}. ` +
        `Focus on the recently implemented feature. ` +
        `Use the exact output format: Verdict: APPROVED or CHANGES_REQUESTED`,
      allowedTools: ["Read", "Glob", "Grep"],
    });

    const review = parseReview(reviewResult.text);
    console.log(`\nVerdict: ${review.verdict}`);
    console.log(`Quality Score: ${review.qualityScore}/10`);

    if (review.verdict === Verdict.APPROVED) {
      console.log(`\nApproved after ${iteration} review iteration(s)!`);
      approved = true;
      break;
    }

    if (iteration === maxIterations) {
      console.log(
        `\nMax iterations (${maxIterations}) reached without approval.`
      );
      return false;
    }

    // Writer fixes issues
    console.log(`\n${"=".repeat(60)}`);
    console.log(`PHASE 2b: Writer — Fixing issues (iteration ${iteration})`);
    console.log("=".repeat(60));

    await writer.query({
      prompt:
        `The reviewer found issues. Fix them:\n\n` +
        `${review.feedback}\n\n` +
        `Address each issue and re-run tests.`,
      systemPrompt: { preset: "claude_code" },
    });
  }

  // ── Phase 3: Verifier runs tests ─────────────────────────────
  console.log(`\n${"=".repeat(60)}`);
  console.log("PHASE 3: Verifier — Running tests");
  console.log("=".repeat(60));

  const verifyResult = await verifier.query({
    prompt:
      `Run the test suite in ${projectPath}. ` +
      `Report test results and coverage. ` +
      `Give a final PASS or FAIL verdict.`,
    allowedTools: ["Bash", "Read", "Glob"],
  });

  const verification = parseVerification(verifyResult.text);
  console.log(`\nVerification: ${verification.passed ? "PASS" : "FAIL"}`);
  console.log(
    `Tests: ${verification.passedTests}/${verification.totalTests} passed`
  );

  if (!verification.passed) {
    console.log("\nVerification FAILED — tests did not pass.");
    return false;
  }

  console.log(
    "\nPipeline complete — Feature implemented, reviewed, and verified!"
  );
  return true;
}

// ── Main ─────────────────────────────────────────────────────────

async function main(): Promise<void> {
  const featureRequest = `Add a user authentication module with:
- login(email, password) function that returns a JWT token
- logout(token) function that invalidates the token
- validateToken(token) function that checks if a token is valid
- Password comparison (simulated, no actual bcrypt needed)
- Token expiration handling
- Comprehensive tests for all functions`;

  const projectPath = process.argv[2] || "src/project";

  const success = await runPipeline(featureRequest, projectPath);
  process.exit(success ? 0 : 1);
}

main().catch((err) => {
  console.error("Pipeline error:", err);
  process.exit(1);
});
