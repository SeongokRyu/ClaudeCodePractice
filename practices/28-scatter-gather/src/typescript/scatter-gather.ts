/**
 * Practice 28: Scatter-Gather Research System — TypeScript Implementation
 *
 * Main orchestrator that:
 * 1. Lead agent decomposes a research question
 * 2. Worker agents research subtopics in parallel
 * 3. Lead agent synthesizes findings into a report
 */

import { ResearchLead, WorkerFinding } from "./research-lead";
import { ResearchWorker } from "./research-worker";

interface ScatterGatherOptions {
  numWorkers?: number;
  verbose?: boolean;
}

async function scatterGather(
  question: string,
  codebasePath: string,
  options: ScatterGatherOptions = {}
): Promise<string> {
  const { numWorkers = 3, verbose = false } = options;

  const lead = new ResearchLead();
  const startTime = Date.now();

  // ── Phase 1: Decompose ──────────────────────────────────────
  console.log("=".repeat(60));
  console.log("PHASE 1: Lead Agent — Decomposing question");
  console.log("=".repeat(60));
  console.log(`Question: ${question}\n`);

  const subtopics = await lead.decompose(question, numWorkers);

  console.log(`Decomposed into ${subtopics.length} subtopics:`);
  subtopics.forEach((st, i) => console.log(`  ${i + 1}. ${st}`));

  const decomposeTime = Date.now() - startTime;

  // ── Phase 2: Scatter (parallel research) ────────────────────
  console.log(`\n${"=".repeat(60)}`);
  console.log(
    `PHASE 2: Workers — Researching ${subtopics.length} subtopics in parallel`
  );
  console.log("=".repeat(60));

  const scatterStart = Date.now();

  // Run all workers in parallel using Promise.all
  const findingsPromises = subtopics.map(async (subtopic, i) => {
    const worker = new ResearchWorker(i + 1);
    try {
      const finding = await worker.research(subtopic, codebasePath);
      if (verbose) {
        console.log(`\n  Worker ${i + 1} completed:`);
        console.log(`    Subtopic: ${subtopic}`);
        console.log(`    Confidence: ${finding.confidence}`);
        console.log(`    Evidence count: ${finding.evidenceCount}`);
        console.log(`    Key files: ${finding.keyFiles.length}`);
      } else {
        console.log(
          `  Worker ${i + 1} completed: ${subtopic.substring(0, 50)}...`
        );
      }
      return finding;
    } catch (error) {
      console.log(`  Worker ${i + 1} FAILED: ${error}`);
      return {
        subtopic,
        findings: `Research failed: ${error}`,
        keyFiles: [],
        confidence: "none" as const,
        recommendations: [],
        evidenceCount: 0,
      };
    }
  });

  const findings: WorkerFinding[] = await Promise.all(findingsPromises);
  const scatterTime = Date.now() - scatterStart;

  // ── Phase 3: Gather & Synthesize ────────────────────────────
  console.log(`\n${"=".repeat(60)}`);
  console.log("PHASE 3: Lead Agent — Synthesizing findings");
  console.log("=".repeat(60));

  const synthesizeStart = Date.now();
  const report = await lead.synthesize(question, findings, subtopics);
  const synthesizeTime = Date.now() - synthesizeStart;

  const totalTime = Date.now() - startTime;

  // ── Report ──────────────────────────────────────────────────
  console.log(`\n${"=".repeat(60)}`);
  console.log("RESEARCH REPORT");
  console.log("=".repeat(60));
  console.log(report);

  // ── Statistics ──────────────────────────────────────────────
  console.log(`\n${"=".repeat(60)}`);
  console.log("STATISTICS");
  console.log("=".repeat(60));
  console.log(`Decomposition time: ${(decomposeTime / 1000).toFixed(1)}s`);
  console.log(
    `Research time:      ${(scatterTime / 1000).toFixed(1)}s (parallel)`
  );
  console.log(`Synthesis time:     ${(synthesizeTime / 1000).toFixed(1)}s`);
  console.log(`Total time:         ${(totalTime / 1000).toFixed(1)}s`);
  console.log(`Workers used:       ${subtopics.length}`);
  console.log(
    `Total findings:     ${findings.reduce((sum, f) => sum + f.evidenceCount, 0)}`
  );

  return report;
}

// ── Main ─────────────────────────────────────────────────────────

async function main(): Promise<void> {
  const question =
    "How is error handling implemented across this codebase? " +
    "What patterns are used, what are the gaps, and what improvements " +
    "could be made?";

  const codebasePath = process.argv[2] || ".";
  const verbose = process.argv.includes("--verbose");

  await scatterGather(question, codebasePath, { verbose });
}

main().catch((err) => {
  console.error("Error:", err);
  process.exit(1);
});
