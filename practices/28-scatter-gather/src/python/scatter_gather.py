"""
Practice 28: Scatter-Gather Research System — Python Implementation

Main orchestrator that:
1. Lead agent decomposes a research question
2. Worker agents research subtopics in parallel
3. Lead agent synthesizes findings into a report
"""

import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from research_lead import ResearchLead
from research_worker import ResearchWorker


def scatter_gather(
    question: str,
    codebase_path: str,
    num_workers: int = 3,
    verbose: bool = False,
) -> str:
    """
    Run the scatter-gather research pipeline.

    Args:
        question: The research question to investigate
        codebase_path: Path to the codebase to research
        num_workers: Number of parallel research workers
        verbose: Print progress details

    Returns:
        Comprehensive research report
    """
    lead = ResearchLead()
    start_time = time.time()

    # ── Phase 1: Decompose ──────────────────────────────────────
    print("=" * 60)
    print("PHASE 1: Lead Agent — Decomposing question")
    print("=" * 60)
    print(f"Question: {question}\n")

    subtopics = lead.decompose(question, num_subtopics=num_workers)

    print(f"Decomposed into {len(subtopics)} subtopics:")
    for i, subtopic in enumerate(subtopics, 1):
        print(f"  {i}. {subtopic}")

    decompose_time = time.time() - start_time

    # ── Phase 2: Scatter (parallel research) ────────────────────
    print(f"\n{'=' * 60}")
    print(f"PHASE 2: Workers — Researching {len(subtopics)} subtopics in parallel")
    print("=" * 60)

    scatter_start = time.time()
    findings = []

    with ThreadPoolExecutor(max_workers=len(subtopics)) as executor:
        # Submit all research tasks
        future_to_subtopic = {
            executor.submit(
                ResearchWorker(worker_id=i).research, subtopic, codebase_path
            ): (i, subtopic)
            for i, subtopic in enumerate(subtopics, 1)
        }

        # Gather results as they complete
        for future in as_completed(future_to_subtopic):
            worker_id, subtopic = future_to_subtopic[future]
            try:
                result = future.result()
                findings.append(result)
                if verbose:
                    print(f"\n  Worker {worker_id} completed:")
                    print(f"    Subtopic: {subtopic}")
                    print(f"    Confidence: {result['confidence']}")
                    print(f"    Evidence count: {result['evidence_count']}")
                    print(f"    Key files: {len(result['key_files'])}")
                else:
                    print(f"  Worker {worker_id} completed: {subtopic[:50]}...")
            except Exception as e:
                print(f"  Worker {worker_id} FAILED: {e}")
                findings.append({
                    "subtopic": subtopic,
                    "findings": f"Research failed: {e}",
                    "key_files": [],
                    "confidence": "none",
                    "recommendations": [],
                    "evidence_count": 0,
                })

    scatter_time = time.time() - scatter_start

    # ── Phase 3: Gather & Synthesize ────────────────────────────
    print(f"\n{'=' * 60}")
    print("PHASE 3: Lead Agent — Synthesizing findings")
    print("=" * 60)

    synthesize_start = time.time()
    report = lead.synthesize(question, findings, subtopics)
    synthesize_time = time.time() - synthesize_start

    total_time = time.time() - start_time

    # ── Report ──────────────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print("RESEARCH REPORT")
    print("=" * 60)
    print(report)

    # ── Statistics ──────────────────────────────────────────────
    print(f"\n{'=' * 60}")
    print("STATISTICS")
    print("=" * 60)
    print(f"Decomposition time: {decompose_time:.1f}s")
    print(f"Research time:      {scatter_time:.1f}s (parallel)")
    print(f"Synthesis time:     {synthesize_time:.1f}s")
    print(f"Total time:         {total_time:.1f}s")
    print(f"Workers used:       {len(subtopics)}")
    print(f"Total findings:     {sum(f.get('evidence_count', 0) for f in findings)}")

    return report


def single_agent_research(question: str, codebase_path: str) -> str:
    """
    Run the same research with a single agent for comparison.

    Args:
        question: The research question
        codebase_path: Path to the codebase

    Returns:
        Research report from a single agent
    """
    from claude_agent_sdk import Agent

    agent = Agent()
    start_time = time.time()

    result = agent.query(
        prompt=(
            f"Research this question thoroughly within the codebase at {codebase_path}:\n\n"
            f"{question}\n\n"
            f"Produce a comprehensive report with:\n"
            f"1. Executive Summary\n"
            f"2. Key Findings (with file:line references)\n"
            f"3. Patterns Identified\n"
            f"4. Recommendations\n"
            f"5. Confidence Assessment"
        ),
        allowed_tools=["Read", "Glob", "Grep"],
    )

    elapsed = time.time() - start_time
    print(f"\nSingle agent research completed in {elapsed:.1f}s")

    return result.text


def main():
    """Run scatter-gather research with a sample question."""
    question = (
        "How is error handling implemented across this codebase? "
        "What patterns are used, what are the gaps, and what improvements "
        "could be made?"
    )

    codebase_path = sys.argv[1] if len(sys.argv) > 1 else "."
    verbose = "--verbose" in sys.argv
    compare = "--compare" in sys.argv

    # Run scatter-gather
    sg_report = scatter_gather(question, codebase_path, verbose=verbose)

    # Optionally compare with single-agent
    if compare:
        print(f"\n{'=' * 60}")
        print("COMPARISON: Single Agent Research")
        print("=" * 60)
        sa_report = single_agent_research(question, codebase_path)
        print(sa_report)

        print(f"\n{'=' * 60}")
        print("COMPARISON SUMMARY")
        print("=" * 60)
        print(f"Scatter-Gather report length: {len(sg_report)} chars")
        print(f"Single-Agent report length:   {len(sa_report)} chars")


if __name__ == "__main__":
    main()
