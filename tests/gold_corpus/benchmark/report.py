#!/usr/bin/env python3
"""Generate Gold Benchmark report."""

import json
import os
import sys
from datetime import datetime, timezone


def generate_report(results: list, output_path: str = None) -> str:
    lines = []
    lines.append("# Gold Benchmark Report")
    lines.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")

    total = len(results)
    passed = sum(1 for r in results if r.get("pass", False))
    failed = total - passed

    global_scores = [r.get("scores", {}).get("global", 0) for r in results]
    avg_global = sum(global_scores) / len(global_scores) if global_scores else 0.0

    lines.append(f"| Metric | Value |")
    lines.append(f"| ------ | ----- |")
    lines.append(f"| Total Conversations | {total} |")
    lines.append(f"| PASS | {passed} |")
    lines.append(f"| FAIL | {failed} |")
    lines.append(f"| Average Global Score | {avg_global:.4f} |")
    lines.append("")

    if results:
        lines.append("## Per-Conversation Results")
        lines.append("")
        lines.append("| ID | Status | Global Score | Conversation | Memory | Qualification | Business | Runtime | Language | Channel | Intent |")
        lines.append("| -- | ------ | ------------ | ------------ | ------ | ------------- | -------- | ------- | -------- | ------- | ------ |")
        for r in results:
            s = r.get("scores", {})
            conv_id = r.get("id", "?")
            status = "PASS" if r.get("pass") else "FAIL"
            lines.append(
                f"| {conv_id} | {status} | "
                f"{s.get('global', 0):.4f} | "
                f"{s.get('conversation', 0):.4f} | "
                f"{s.get('memory', 0):.4f} | "
                f"{s.get('qualification', 0):.4f} | "
                f"{s.get('business', 0):.4f} | "
                f"{s.get('runtime', 0):.4f} | "
                f"{s.get('language', 0):.4f} | "
                f"{s.get('channel', 0):.4f} | "
                f"{s.get('intent', 0):.4f} |"
            )

    lines.append("")
    lines.append("## Scoring Weights")
    lines.append("")
    lines.append("| Category | Weight |")
    lines.append("| -------- | ------ |")
    from score import WEIGHTS
    for cat, w in sorted(WEIGHTS.items()):
        lines.append(f"| {cat} | {w} |")

    report = "\n".join(lines)

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(report)
        print(f"Report written to: {output_path}")

    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate Gold Benchmark report from results JSON")
    parser.add_argument("results_file", help="Path to benchmark results JSON file")
    parser.add_argument("-o", "--output", default=None, help="Output report path")
    args = parser.parse_args()

    with open(args.results_file) as f:
        results = json.load(f)

    report = generate_report(results, args.output)
    print(report)


if __name__ == "__main__":
    sys.exit(main())
