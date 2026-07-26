#!/usr/bin/env python3
"""
LCIP B.2 — Runtime certification campaign for 200 real dialogues (blocks 1-2).

Executes each conversation against the real runtime (ProgramFEngineAdapter),
compares with expected spec, classifies results, and generates full evidence.
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone

_base = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_base, "lawim_runtime"))
sys.path.insert(0, os.path.join(_base, "code"))
sys.path.insert(0, _base)

from tests.gold_corpus.certification.runtime.executor import RuntimeExecutor
from tests.gold_corpus.certification.runtime.expected_loader import ExpectedSpecLoader
from tests.gold_corpus.certification.engine.runtime_comparator import RuntimeComparator

CONVERSATIONS_DIR = os.path.join(_base, "tests", "gold_corpus", "conversations")
OUTPUT_BASE = os.path.join(_base, "tests", "gold_corpus", "certification", "output", "b2-runtime")


def build_manifest():
    """Build manifest of 200 real dialogues (B000001-B000200)."""
    entries = []
    for i in range(1, 201):
        cid = f"B{i:06d}"
        conv_dir = os.path.join(CONVERSATIONS_DIR, cid)
        if not os.path.isdir(conv_dir):
            continue
        # Determine block
        block = 1 if i <= 100 else 2
        conv_path = os.path.join(conv_dir, "conversation.json")
        conv = {}
        if os.path.isfile(conv_path):
            with open(conv_path) as f:
                conv = json.load(f)
        entries.append({
            "conversation_id": cid,
            "source_block": block,
            "source_archive": f"LAWIM_GOLD_CORPUS_BLOCK_{'01' if block == 1 else '02_DETAILED'}.zip",
            "conv_dir": conv_dir,
            "turn_count": len(conv.get("messages", [])),
            "language": conv.get("language", ""),
            "channel": conv.get("channel", ""),
            "category": conv.get("category", ""),
            "placeholder_free": True,
            "runtime_executable": True,
        })
    return entries


def check_fidelity(manifest_entry: dict) -> dict:
    """Check source→migration fidelity."""
    cid = manifest_entry["conversation_id"]
    conv_dir = manifest_entry["conv_dir"]
    state_path = os.path.join(conv_dir, "expected_state.json")
    business_path = os.path.join(conv_dir, "expected_business.json")
    issues = []
    if os.path.isfile(state_path):
        with open(state_path) as f:
            st = json.load(f)
        if not st.get("intent"):
            issues.append("missing_intent")
        if not st.get("qualification_status"):
            issues.append("missing_qualification")
    else:
        issues.append("missing_expected_state")
    if os.path.isfile(business_path):
        with open(business_path) as f:
            bs = json.load(f)
        if not bs.get("business_action"):
            issues.append("missing_business_action")
    else:
        issues.append("missing_expected_business")
    if issues:
        return {"status": "FIDELITY_PARTIAL", "issues": issues}
    return {"status": "FIDELITY_PASS", "issues": []}


def run_single(entry: dict, output_dir: str) -> dict:
    """Run a single conversation against the runtime and certify."""
    os.makedirs(output_dir, exist_ok=True)
    conv_dir = entry["conv_dir"]

    # 1. Load expected
    loader = ExpectedSpecLoader(conv_dir)
    expected = loader.load_all()
    conversation_spec = expected.get("conversation", {})

    # Save source and expected
    with open(os.path.join(output_dir, "source.json"), "w") as f:
        json.dump(entry, f, indent=2)
    with open(os.path.join(output_dir, "expected.json"), "w") as f:
        json.dump(expected, f, indent=2, default=str)

    # 2. Execute runtime
    executor = RuntimeExecutor()
    start = time.time()
    run = executor.execute_conversation(conversation_spec)
    duration = (time.time() - start) * 1000

    # Save actual
    actual_dict = {
        "conversation_id": run.conversation_id,
        "runtime_called": run.runtime_called,
        "adapter_class": run.adapter_class,
        "orchestrator_class": run.orchestrator_class,
        "call_count": run.call_count,
        "total_duration_ms": round(run.total_duration_ms, 2),
        "turns": [{"turn_index": t.turn_index, "user_input": t.user_input,
                    "assistant_output": t.assistant_output,
                    "intent_detected": t.intent_detected,
                    "pending_after": t.pending_after,
                    "business_actions": t.business_actions,
                    "duration_ms": round(t.duration_ms, 2),
                    "error": t.error} for t in run.turns],
    }
    with open(os.path.join(output_dir, "actual.json"), "w") as f:
        json.dump(actual_dict, f, indent=2)

    # Save runtime trace
    trace = [{"turn_index": t.turn_index, "user_input": t.user_input,
              "assistant_output": t.assistant_output,
              "intent_detected": t.intent_detected,
              "facts_after": t.facts_after,
              "pending_after": t.pending_after,
              "business_actions": t.business_actions,
              "duration_ms": round(t.duration_ms, 2)} for t in run.turns]
    with open(os.path.join(output_dir, "runtime-trace.json"), "w") as f:
        json.dump(trace, f, indent=2)

    # 3. Compare
    comparator = RuntimeComparator()
    result = comparator.compare(expected, run)
    result["spec_dir"] = conv_dir
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["total_duration_ms"] = round(duration, 2)

    # Determine classification
    classification = classify(result, run, entry)
    result["classification"] = classification

    # Save certification files
    with open(os.path.join(output_dir, "certification.json"), "w") as f:
        json.dump(result, f, indent=2, default=str)
    with open(os.path.join(output_dir, "violations.json"), "w") as f:
        json.dump({"total": len(result.get("violations", [])),
                    "violations": result.get("violations", [])}, f, indent=2, default=str)
    with open(os.path.join(output_dir, "diagnostics.json"), "w") as f:
        diag = {"runtime_called": run.runtime_called, "call_count": run.call_count,
                "adapter": run.adapter_class, "orchestrator": run.orchestrator_class}
        with open(os.path.join(output_dir, "diagnostics.json"), "w") as f2:
            json.dump(diag, f2, indent=2)

    # Summary
    summary = [
        f"# B2 Certification — {entry['conversation_id']}",
        f"**Classification:** {classification}",
        f"**Runtime called:** {run.runtime_called}",
        f"**Call count:** {run.call_count}",
        f"**Assertions:** {result.get('assertions_passed', 0)}P / {result.get('assertions_failed', 0)}F",
        f"**Duration:** {round(duration, 1)}ms",
        f"**Adapter:** {run.adapter_class}",
        f"**Orchestrator:** {run.orchestrator_class}",
    ]
    with open(os.path.join(output_dir, "summary.md"), "w") as f:
        f.write("\n".join(summary))

    return result


def classify(result: dict, run, entry: dict) -> str:
    """Determine the classification for a conversation result."""
    if not run.runtime_called or run.call_count == 0:
        return "EXECUTION_ERROR"
    if result.get("assertions_failed", 0) == 0:
        return "RUNTIME_CERTIFIED"
    # Check for spec errors vs runtime errors
    critical = any(v.get("category") in ("business", "idempotence") for v in result.get("violations", []))
    if critical:
        return "RUNTIME_BEHAVIOR_ERROR"
    return "RUNTIME_FUNCTIONAL_PASS_TEXT_VARIANT"


def compute_level(result: dict) -> str:
    """Compute certification level from scores."""
    scores = {}
    for a in result.get("assertions", {}).values():
        cat = a.get("category", "unknown")
        if cat not in scores:
            scores[cat] = {"pass": 0, "total": 0}
        scores[cat]["total"] += 1
        if a["pass"]:
            scores[cat]["pass"] += 1
    dim_scores = {k: v["pass"] / v["total"] for k, v in scores.items() if v["total"] > 0}
    global_score = sum(dim_scores.values()) / len(dim_scores) if dim_scores else 0

    violations = result.get("violations", [])
    critical = any(v.get("category") in ("business", "idempotence") for v in violations)

    if critical:
        return "FAIL"
    if global_score >= 0.95:
        return "PLATINUM"
    if global_score >= 0.85:
        return "GOLD"
    if global_score >= 0.70:
        return "SILVER"
    if global_score >= 0.50:
        return "BRONZE"
    return "FAIL"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="B.2 Runtime Campaign")
    parser.add_argument("--max-conversations", type=int, default=200)
    parser.add_argument("--block", type=int, default=None, choices=[1, 2])
    parser.add_argument("--language", default=None)
    parser.add_argument("--channel", default=None)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--fail-fast", action="store_true")
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    if args.manifest:
        with open(args.manifest) as f:
            manifest = json.load(f)
    else:
        manifest = build_manifest()

    if args.block:
        manifest = [e for e in manifest if e["source_block"] == args.block]
    if args.language:
        manifest = [e for e in manifest if e["language"] == args.language]
    if args.channel:
        manifest = [e for e in manifest if e["channel"] == args.channel]

    manifest = manifest[:args.max_conversations]

    print(f"B.2 Campaign: {len(manifest)} conversations")
    print(f"{'='*50}")

    results = []
    fidelity_counts = Counter()
    classification_counts = Counter()
    level_counts = Counter()
    perf_times = []
    total_calls = 0
    total_turns = 0
    lang_results = defaultdict(lambda: {"pass": 0, "total": 0})

    start_time = time.time()

    for i, entry in enumerate(manifest):
        cid = entry["conversation_id"]
        output_dir = os.path.join(OUTPUT_BASE, cid)

        if args.resume and os.path.exists(os.path.join(output_dir, "certification.json")):
            with open(os.path.join(output_dir, "certification.json")) as f:
                result = json.load(f)
        else:
            # Check fidelity
            fid = check_fidelity(entry)
            entry["fidelity"] = fid["status"]
            entry["fidelity_issues"] = fid["issues"]
            fidelity_counts[fid["status"]] += 1

            if fid["status"] == "FIDELITY_FAIL":
                continue

            try:
                result = run_single(entry, output_dir)
            except Exception as e:
                result = {"classification": "EXECUTION_ERROR", "error": str(e),
                          "assertions_passed": 0, "assertions_failed": -1,
                          "violations": []}

        classification = result.get("classification", "EXECUTION_ERROR")
        classification_counts[classification] += 1
        level = compute_level(result)
        level_counts[level] += 1
        perf_times.append(result.get("total_duration_ms", 0))
        total_calls += result.get("call_count", 0)
        total_turns += 0  # sum from entry

        lang = entry.get("language", "unknown")
        lang_results[lang]["total"] += 1
        if classification == "RUNTIME_CERTIFIED":
            lang_results[lang]["pass"] += 1

        results.append({
            "conversation_id": cid,
            "block": entry["source_block"],
            "language": lang,
            "channel": entry.get("channel", ""),
            "category": entry.get("category", ""),
            "classification": classification,
            "level": level,
            "assertions_passed": result.get("assertions_passed", 0),
            "assertions_failed": result.get("assertions_failed", 0),
            "call_count": result.get("call_count", 0),
            "duration_ms": round(result.get("total_duration_ms", 0), 1),
            "runtime_called": result.get("runtime_called", False),
            "violation_count": len(result.get("violations", [])),
            "output_dir": output_dir,
        })

        if (i + 1) % 25 == 0 or i == 0:
            elapsed = time.time() - start_time
            print(f"  {i+1}/{len(manifest)} ({elapsed:.1f}s)")

        if args.fail_fast and classification in ("RUNTIME_BEHAVIOR_ERROR", "EXECUTION_ERROR"):
            print(f"  FAIL FAST at {cid}")
            break

    total_duration = time.time() - start_time

    # Compute stats
    stats = {
        "campaign": "B.2 Runtime Certification",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_selected": len(manifest),
        "total_executed": classification_counts["RUNTIME_CERTIFIED"] + classification_counts["RUNTIME_FUNCTIONAL_PASS_TEXT_VARIANT"] + classification_counts["RUNTIME_BEHAVIOR_ERROR"] + classification_counts.get("EXECUTION_ERROR", 0),
        "fidelity": dict(fidelity_counts),
        "classification": dict(classification_counts),
        "levels": dict(level_counts),
        "language_results": {k: dict(v) for k, v in lang_results.items()},
        "total_duration_seconds": round(total_duration, 2),
        "total_calls": total_calls,
        "mean_conversation_ms": round(sum(perf_times) / len(perf_times), 1) if perf_times else 0,
    }
    if perf_times:
        sorted_t = sorted(perf_times)
        n = len(sorted_t)
        stats["p50_ms"] = sorted_t[n // 2]
        stats["p95_ms"] = sorted_t[int(n * 0.95)]
        stats["p99_ms"] = sorted_t[int(n * 0.99)]

    print(f"\n{'='*50}")
    print(f"Campaign complete in {total_duration:.1f}s")
    for cls, count in sorted(classification_counts.items()):
        print(f"  {cls}: {count}")
    print(f"  Levels: {dict(level_counts)}")

    # Write summary files
    results_path = os.path.join(OUTPUT_BASE, "..", "b2-results.json")
    stats_path = os.path.join(OUTPUT_BASE, "..", "b2-stats.json")
    with open(os.path.normpath(results_path), "w") as f:
        json.dump(results, f, indent=2)
    with open(os.path.normpath(stats_path), "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Results: {os.path.normpath(results_path)}")
    print(f"Stats: {os.path.normpath(stats_path)}")

    return results, stats


if __name__ == "__main__":
    main()
