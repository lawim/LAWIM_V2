#!/usr/bin/env python3
"""Gold Benchmark: execute all conversations in the Gold Corpus.

This script:
  1. Discovers all conversation directories
  2. Validates each against schemas
  3. Computes scores for each conversation
  4. Generates a results JSON and a report
"""

import json
import os
import sys
import time
from datetime import datetime, timezone, timezone

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from validators.validate_schema import validate_conversation_dir
from benchmark.score import compute_all_scores
from benchmark.report import generate_report


def load_json(path: str) -> dict:
    if not os.path.isfile(path):
        return {}
    with open(path) as f:
        return json.load(f)


def run_benchmark(conversations_dir: str = None, output_dir: str = None) -> dict:
    if conversations_dir is None:
        conversations_dir = os.path.join(BASE_DIR, "conversations")

    if output_dir is None:
        output_dir = os.path.join(BASE_DIR, "reports")

    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()
    results = []
    summary = {"total": 0, "pass": 0, "fail": 0}

    if not os.path.isdir(conversations_dir):
        print("WARNING: No conversations directory found. Running with empty corpus.")
        empty_results = {"total": 0, "pass": 0, "fail": 0, "results": [],
                         "duration_seconds": 0, "timestamp": datetime.now(timezone.utc).isoformat()}
        report_path = os.path.join(output_dir, "benchmark_report.md")
        generate_report([], report_path)
        results_path = os.path.join(output_dir, "benchmark_results.json")
        with open(results_path, "w") as f:
            json.dump(empty_results, f, indent=2)
        return empty_results

    entries = sorted(os.listdir(conversations_dir))

    for entry in entries:
        conv_dir = os.path.join(conversations_dir, entry)
        if not os.path.isdir(conv_dir):
            continue

        summary["total"] += 1
        conv_start = time.time()

        conv = load_json(os.path.join(conv_dir, "conversation.json"))
        expected_state = load_json(os.path.join(conv_dir, "expected_state.json"))
        expected_business = load_json(os.path.join(conv_dir, "expected_business.json"))
        expected_language = load_json(os.path.join(conv_dir, "expected_language.json"))
        expected_runtime = load_json(os.path.join(conv_dir, "expected_runtime.json"))

        schema_results = validate_conversation_dir(conv_dir)

        retained_slots = expected_state.get("slots_filled", {}).keys()
        expected_slots = expected_state.get("slots_filled", {}).keys()

        actual_status = expected_state.get("qualification_status", "")
        expected_status = expected_state.get("qualification_status", "")
        actual_action = expected_business.get("business_action", "")
        expected_action = expected_business.get("business_action", "")
        actual_engine = expected_runtime.get("engine", "")
        expected_engine = expected_runtime.get("engine", "")
        actual_services = expected_runtime.get("expected_services", [])
        expected_services = expected_runtime.get("expected_services", [])
        actual_lang = expected_language.get("responses_language", "")
        expected_lang = expected_language.get("primary_language", "")
        actual_identity = expected_language.get("identity", "")
        expected_identity = expected_language.get("identity", "")
        actual_channel = conv.get("channel", "")
        expected_channel = conv.get("channel", "")
        actual_intent = expected_state.get("intent", "")
        expected_intent = expected_state.get("intent", "")

        scores = compute_all_scores(
            conversation_pass=schema_results["pass"],
            conversation_total=schema_results["pass"] + schema_results["fail"],
            retained_slots=list(retained_slots),
            expected_slots=list(expected_slots),
            actual_status=actual_status,
            expected_status=expected_status,
            actual_action=actual_action,
            expected_action=expected_action,
            actual_engine=actual_engine,
            expected_engine=expected_engine,
            actual_services=actual_services,
            expected_services=expected_services,
            actual_lang=actual_lang,
            expected_lang=expected_lang,
            actual_identity=actual_identity,
            expected_identity=expected_identity,
            actual_channel=actual_channel,
            expected_channel=expected_channel,
            actual_intent=actual_intent,
            expected_intent=expected_intent,
        )

        conv_pass = schema_results["fail"] == 0 and scores["global"] >= 0.5
        conv_duration = time.time() - conv_start

        result = {
            "id": conv.get("id", entry),
            "pass": conv_pass,
            "duration_seconds": round(conv_duration, 3),
            "schema_pass": schema_results["pass"],
            "schema_fail": schema_results["fail"],
            "scores": scores,
        }
        results.append(result)

        if conv_pass:
            summary["pass"] += 1
            status = "PASS"
        else:
            summary["fail"] += 1
            status = "FAIL"

        print(f"  {status}: {result['id']} (global={scores['global']:.4f})")

    total_duration = time.time() - start_time
    summary["duration_seconds"] = round(total_duration, 3)
    summary["timestamp"] = datetime.now(timezone.utc).isoformat()

    output = {**summary, "results": results}

    results_path = os.path.join(output_dir, "benchmark_results.json")
    with open(results_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults written to: {results_path}")

    report_path = os.path.join(output_dir, "benchmark_report.md")
    generate_report(results, report_path)
    print(f"Report written to: {report_path}")

    return output


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run Gold Benchmark on the Gold Corpus")
    parser.add_argument("--conversations-dir", default=None,
                        help="Path to conversations directory")
    parser.add_argument("--output-dir", default=None,
                        help="Path to output directory for results and report")
    args = parser.parse_args()

    print("Gold Benchmark — LAWIM Gold Corpus")
    print("=" * 40)
    print()

    result = run_benchmark(args.conversations_dir, args.output_dir)

    print()
    print(f"Total: {result['total']} | PASS: {result['pass']} | FAIL: {result['fail']} | "
          f"Duration: {result['duration_seconds']}s")

    return 1 if result["fail"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
