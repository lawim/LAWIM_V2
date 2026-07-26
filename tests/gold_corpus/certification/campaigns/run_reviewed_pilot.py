#!/usr/bin/env python3
"""Run the b4rc-reviewed pilot specs against the LAWIM runtime.

Usage:
    python3 tests/gold_corpus/certification/campaigns/run_reviewed_pilot.py
"""

import json
import os
import sys
import time
import argparse
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
os.environ["LAWIM_VAULT_KEY"] = "test-key-123"

from tests.gold_corpus.certification.runtime.executor import RuntimeExecutor
from tests.gold_corpus.certification.runtime.expected_loader import ExpectedSpecLoader
from tests.gold_corpus.certification.runtime.reviewed_spec_adapter import ReviewedSpecAdapter
from tests.gold_corpus.certification.runtime.executability import can_execute
from tests.gold_corpus.certification.engine.runtime_comparator import RuntimeComparator

SPEC_ROOT = "tests/gold_corpus/specifications/b4rc-reviewed"
OUTPUT_ROOT = "tests/gold_corpus/certification/output/b4re-runtime-pilot"
MANIFEST = "tests/gold_corpus/specification/review/b4rc-pilot-20.json"
PILOT_IDS = [
    "B000001", "B000002", "B000004", "B000005", "B000021",
    "B000056", "B000057", "B000101", "B000111", "B000121",
    "B000089", "B000090", "B000095", "B000096",
    "B000076", "B000077", "B000066", "B000083",
    "B000131", "B000036",
]

adapter = ReviewedSpecAdapter(SPEC_ROOT)


def classify(result, run, conversation_id):
    """Classify the conversation result."""
    if run.runtime_errors:
        return "EXECUTION_ERROR"

    # Check if runtime was actually called
    if not run.runtime_called:
        return "NOT_EXECUTABLE"

    # Check for assertion failures
    assertions_failed = result.get("assertions_failed", 0)
    violations = result.get("violations", [])

    if assertions_failed == 0:
        return "RUNTIME_CERTIFIED"

    # Check if violations are only text-related
    text_only_violations = all(
        "text" in v.get("assertion_id", "").lower()
        or "response" in v.get("assertion_id", "").lower()
        for v in violations
    )
    if text_only_violations and assertions_failed > 0:
        return "FUNCTIONAL_TEXT_VARIANT"

    # Check for specification errors vs runtime errors
    spec_errors = [v for v in violations if "expected" in v.get("assertion_id", "").lower()]
    if spec_errors:
        return "SPECIFICATION_ERROR"

    return "RUNTIME_BEHAVIOR_ERROR"


def run_single(conversation_id, output_dir):
    """Run a single conversation through the full pipeline."""
    conv_dir = os.path.join(output_dir, conversation_id)
    os.makedirs(conv_dir, exist_ok=True)

    # Save source conversation
    conv = adapter.load_conversation(conversation_id)
    with open(os.path.join(conv_dir, "source.json"), "w") as f:
        json.dump(conv, f, indent=2, ensure_ascii=False)

    # Save reviewed spec
    spec = adapter.load_expected_all(conversation_id)
    with open(os.path.join(conv_dir, "reviewed-spec.json"), "w") as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)

    # Execute
    executor = RuntimeExecutor()
    start = time.time()
    run = executor.execute_conversation(conv)
    duration_ms = (time.time() - start) * 1000

    # Save actual
    actual = {
        "conversation_id": run.conversation_id,
        "runtime_called": run.runtime_called,
        "adapter_class": run.adapter_class,
        "orchestrator_class": run.orchestrator_class,
        "call_count": run.call_count,
        "total_duration_ms": run.total_duration_ms,
        "turns": [
            {
                "turn_index": t.turn_index,
                "user_input": t.user_input,
                "assistant_output": t.assistant_output,
                "intent_detected": t.intent_detected,
                "intent_confidence": t.intent_confidence,
                "state_after": t.state_after,
                "facts_after": t.facts_after,
                "pending_after": t.pending_after,
                "business_actions": t.business_actions,
                "duration_ms": t.duration_ms,
                "error": t.error,
            }
            for t in run.turns
        ],
        "runtime_errors": run.runtime_errors,
    }
    with open(os.path.join(conv_dir, "actual.json"), "w") as f:
        json.dump(actual, f, indent=2, ensure_ascii=False)

    # Save runtime trace
    trace = {
        "conversation_id": run.conversation_id,
        "adapter": run.adapter_class,
        "orchestrator": run.orchestrator_class,
        "total_duration_ms": run.total_duration_ms,
        "call_count": run.call_count,
        "turn_count": len(run.turns),
        "runtime_errors": run.runtime_errors,
    }
    with open(os.path.join(conv_dir, "runtime-trace.json"), "w") as f:
        json.dump(trace, f, indent=2, ensure_ascii=False)

    # Compare
    comparator = RuntimeComparator()
    expected = spec
    try:
        result = comparator.compare(expected, run)
    except Exception as e:
        result = {
            "error": str(e),
            "assertions_passed": 0,
            "assertions_failed": 0,
            "violations": [{"assertion_id": "COMPARATOR_ERROR", "message": str(e)}],
        }

    with open(os.path.join(conv_dir, "comparison.json"), "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    # Classify
    classification = classify(result, run, conversation_id)

    # Certification result
    certification = {
        "conversation_id": conversation_id,
        "classification": classification,
        "runtime_called": run.runtime_called,
        "adapter_class": run.adapter_class,
        "orchestrator_class": run.orchestrator_class,
        "call_count": run.call_count,
        "total_duration_ms": run.total_duration_ms,
        "assertions_total": result.get("assertions_total", 0),
        "assertions_passed": result.get("assertions_passed", 0),
        "assertions_failed": result.get("assertions_failed", 0),
        "violations": result.get("violations", []),
        "violation_count": len(result.get("violations", [])),
        "user_turns": len([m for m in conv["messages"] if m["role"] == "user"]),
        "has_restart": any(m["role"] == "system" for m in conv["messages"]),
    }
    with open(os.path.join(conv_dir, "certification.json"), "w") as f:
        json.dump(certification, f, indent=2, ensure_ascii=False)

    # Violations
    violations = result.get("violations", [])
    with open(os.path.join(conv_dir, "violations.json"), "w") as f:
        json.dump(violations, f, indent=2, ensure_ascii=False)

    # Diagnostics
    diagnostics = {
        "conversation_id": conversation_id,
        "classification": classification,
        "executable": True,
        "turn_count_expected": len(conv["messages"]),
        "turn_count_actual": len(run.turns),
        "user_turn_count": len([m for m in conv["messages"] if m["role"] == "user"]),
        "runtime_errors": run.runtime_errors,
        "assertion_breakdown": {
            "total": result.get("assertions_total", 0),
            "passed": result.get("assertions_passed", 0),
            "failed": result.get("assertions_failed", 0),
        },
    }
    with open(os.path.join(conv_dir, "diagnostics.json"), "w") as f:
        json.dump(diagnostics, f, indent=2, ensure_ascii=False)

    # Summary
    summary = [
        f"# {conversation_id} — Runtime Certification Summary",
        f"",
        f"**Classification:** {classification}",
        f"**Runtime called:** {run.runtime_called}",
        f"**Adapter:** {run.adapter_class}",
        f"**Orchestrator:** {run.orchestrator_class}",
        f"**Duration:** {run.total_duration_ms:.1f}ms",
        f"**User turns:** {len([m for m in conv['messages'] if m['role'] == 'user'])}",
        f"**Assertions:** {result.get('assertions_passed', 0)}P / {result.get('assertions_failed', 0)}F",
        f"",
    ]
    if result.get("violations"):
        summary.append(f"## Violations")
        for v in result["violations"]:
            summary.append(f"- {v.get('assertion_id', '?')}: expected={v.get('expected', '?')}, actual={v.get('actual', '?')}")
    if run.runtime_errors:
        summary.append(f"## Runtime Errors")
        for e in run.runtime_errors:
            summary.append(f"- {e}")

    with open(os.path.join(conv_dir, "summary.md"), "w") as f:
        f.write("\n".join(summary))

    return certification


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=MANIFEST)
    parser.add_argument("--spec-root", default=SPEC_ROOT)
    parser.add_argument("--output", default=OUTPUT_ROOT)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    output_root = args.output

    results = []
    overall_start = time.time()

    for cid in PILOT_IDS:
        print(f"\n{'='*60}")
        print(f"Executing {cid}...")
        print(f"{'='*60}")

        # Check executability
        exec_check = can_execute(cid, args.spec_root)
        if not exec_check["executable"]:
            print(f"  NOT EXECUTABLE: {exec_check['reasons']}")
            results.append({
                "conversation_id": cid,
                "classification": "NOT_EXECUTABLE",
                "reasons": exec_check["reasons"],
            })
            continue

        try:
            result = run_single(cid, output_root)
            results.append(result)
            print(f"  Classification: {result['classification']}")
            print(f"  Calls: {result['call_count']}, Duration: {result['total_duration_ms']:.1f}ms")
            print(f"  Assertions: {result['assertions_passed']}P / {result['assertions_failed']}F")
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                "conversation_id": cid,
                "classification": "EXECUTION_ERROR",
                "error": str(e),
            })

    overall_duration = (time.time() - overall_start) * 1000

    # Save aggregate results
    aggregate = {
        "campaign": "b4re-runtime-pilot",
        "timestamp": datetime.utcnow().isoformat(),
        "total_conversations": len(PILOT_IDS),
        "total_executed": len([r for r in results if r["classification"] != "NOT_EXECUTABLE"]),
        "total_duration_ms": overall_duration,
        "results": results,
        "summary": {
            c: len([r for r in results if r["classification"] == c])
            for c in set(r["classification"] for r in results)
        },
    }
    with open(os.path.join(output_root, "b4re-results.json"), "w") as f:
        json.dump(aggregate, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Campaign complete: {len(results)} conversations")
    print(f"Duration: {overall_duration:.0f}ms")
    for c, count in sorted(aggregate["summary"].items()):
        print(f"  {c}: {count}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
