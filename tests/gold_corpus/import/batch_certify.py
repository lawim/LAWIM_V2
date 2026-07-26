#!/usr/bin/env python3
"""
Batch certification for all migrated Gold Corpus conversations.
Uses LCIP A.3 Certification Orchestrator on each conversation.
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
GOLD_CORPUS_DIR = os.path.join(REPO_ROOT, "tests", "gold_corpus")
CONVERSATIONS_DIR = os.path.join(GOLD_CORPUS_DIR, "conversations")
IMPORT_DIR = os.path.join(GOLD_CORPUS_DIR, "import")
SCHEMA_DIR = os.path.join(GOLD_CORPUS_DIR, "schema")

sys.path.insert(0, os.path.join(GOLD_CORPUS_DIR, "certification", "engine"))
sys.path.insert(0, os.path.join(GOLD_CORPUS_DIR, "certification"))
from orchestrator import CertificationOrchestrator


def certify_all(output_dir: str = None) -> dict:
    if output_dir is None:
        output_dir = os.path.join(IMPORT_DIR, "certification_output")
    os.makedirs(output_dir, exist_ok=True)

    orchestrator = CertificationOrchestrator(
        os.path.join(GOLD_CORPUS_DIR, "specification", "assertions", "assertion_library.json")
    )

    conv_ids = sorted([
        d for d in os.listdir(CONVERSATIONS_DIR)
        if os.path.isdir(os.path.join(CONVERSATIONS_DIR, d))
    ])

    print(f"Batch certifying {len(conv_ids)} conversations...\n")

    all_results = []
    scores_summary = defaultdict(list)
    violations_counter = Counter()
    components_counter = Counter()
    certified = []
    repairable = []
    rejected = []

    start_time = time.time()

    for i, cid in enumerate(conv_ids):
        conv_dir = os.path.join(CONVERSATIONS_DIR, cid)
        # Use the conversation directory as both spec and actual
        result = orchestrator.certify(conv_dir, conv_dir, output_dir=os.path.join(output_dir, cid))
        all_results.append(result)

        global_score = result.get("scores", {}).get("global", 0)
        scores_summary["global"].append(global_score)

        for dim, score in result.get("scores", {}).items():
            if dim != "global":
                scores_summary[dim].append(score)

        violations = result.get("violations", [])
        for v in violations:
            violations_counter[v["assertion_id"]] += 1

        for rc in result.get("root_causes", []):
            components_counter[rc["responsible_component"]] += 1

        # Classify
        if global_score >= 0.85:
            certified.append(cid)
        elif global_score >= 0.5:
            repairable.append(cid)
        else:
            rejected.append(cid)

        if (i + 1) % 100 == 0:
            print(f"  Progress: {i+1}/{len(conv_ids)} ({time.time()-start_time:.1f}s)")

    duration = time.time() - start_time

    # Aggregate scores
    def avg(vals):
        return round(sum(vals) / len(vals), 4) if vals else 0.0

    def median(vals):
        sv = sorted(vals)
        n = len(sv)
        if n == 0:
            return 0.0
        if n % 2 == 0:
            return round((sv[n // 2 - 1] + sv[n // 2]) / 2, 4)
        return round(sv[n // 2], 4)

    statistics = {
        "total_conversations": len(conv_ids),
        "duration_seconds": round(duration, 2),
        "certified": len(certified),
        "repairable": len(repairable),
        "rejected": len(rejected),
        "scores": {
            "mean": {dim: avg(vals) for dim, vals in scores_summary.items()},
            "median": {dim: median(vals) for dim, vals in scores_summary.items()},
            "min": {dim: round(min(vals), 4) for dim, vals in scores_summary.items()},
            "max": {dim: round(max(vals), 4) for dim, vals in scores_summary.items()},
        },
        "most_violated_assertions": violations_counter.most_common(20),
        "most_responsible_components": components_counter.most_common(20),
    }

    classification = {
        "Gold Certified": certified,
        "Gold Repairable": repairable,
        "Gold Rejected": rejected,
    }

    # Write outputs
    stats_path = os.path.join(output_dir, "certification_statistics.json")
    with open(stats_path, "w") as f:
        json.dump(statistics, f, indent=2)

    class_path = os.path.join(output_dir, "certification_classification.json")
    with open(class_path, "w") as f:
        json.dump(classification, f, indent=2)

    results_path = os.path.join(output_dir, "all_results.json")
    with open(results_path, "w") as f:
        json.dump(all_results, f, indent=2, default=str)

    print(f"\nBatch certification complete in {duration:.1f}s")
    print(f"  Total: {len(conv_ids)}")
    print(f"  Certified: {len(certified)}")
    print(f"  Repairable: {len(repairable)}")
    print(f"  Rejected: {len(rejected)}")
    print(f"  Mean global score: {avg(scores_summary['global']):.4f}")
    print(f"  Median global score: {median(scores_summary['global']):.4f}")
    print(f"\nOutput: {output_dir}/")

    return statistics


if __name__ == "__main__":
    certify_all()
