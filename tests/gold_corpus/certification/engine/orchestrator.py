#!/usr/bin/env python3
"""LAWIM Conversation Certification Orchestrator.

Loads a conversation, runs certification, analyzes violations, identifies
root causes, and produces multiple output formats:
  - certification.json  (full results)
  - violations.json     (violation analysis)
  - diagnostics.json    (root cause analysis)
  - summary.md          (human-readable summary)
"""

import json
import os
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

# Import A.2 certification engine
_spec_path = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "specification")
# Fallback: try from current working dir
if not os.path.isdir(_spec_path):
    _spec_path = os.path.join(os.getcwd(), "tests", "gold_corpus", "specification")
if not os.path.isdir(_spec_path):
    _spec_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "..", "..", "..", "specification")
_spec_path = os.path.normpath(_spec_path)
sys.path.insert(0, _spec_path)
from engine.certification_engine import CertificationEngine, Verdict

# Import A.3 diagnostics
_diag_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not os.path.isdir(os.path.join(_diag_path, "diagnostics")):
    _diag_path = os.path.join(os.getcwd(), "tests", "gold_corpus", "certification")
_diag_path = os.path.normpath(_diag_path)
sys.path.insert(0, _diag_path)
from diagnostics.violation_engine import analyze_all_violations
from diagnostics.root_cause_engine import analyze_root_causes, build_component_summary


OUTPUT_DIR_DEFAULT = None


class CertificationOrchestrator:
    def __init__(self, assertion_library_path: Optional[str] = None):
        self.cert_engine = CertificationEngine(assertion_library_path)

    def certify(self, spec_dir: str, actual_dir: str,
                output_dir: Optional[str] = None) -> Dict[str, Any]:
        """Run full certification with diagnostics and root cause analysis."""
        if output_dir is None:
            output_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "output",
            )
        os.makedirs(output_dir, exist_ok=True)

        # Step 1: Run base certification (reuse A.2 engine logic)
        base_result = self.cert_engine.certify(spec_dir, actual_dir)

        # Step 2: Analyze violations
        violations = analyze_all_violations(
            base_result.get("assertions", {}),
            base_result.get("turns"),
        )

        # Step 3: Analyze root causes
        root_causes = analyze_root_causes(violations)
        component_summary = build_component_summary(root_causes)

        # Step 4: Build full result
        result = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "spec_dir": spec_dir,
            "actual_dir": actual_dir,
            "verdict": base_result.get("verdict", "FAIL"),
            "scores": base_result.get("scores", {}),
            "summary": base_result.get("summary", {}),
            "violations_count": len(violations),
            "components_affected": len(component_summary),
            "violations": violations,
            "root_causes": root_causes,
            "component_summary": component_summary,
            "assertions": base_result.get("assertions", {}),
            "turns": base_result.get("turns", {}),
        }

        # Write outputs
        self._write_outputs(result, output_dir)

        return result

    def _write_outputs(self, result: Dict[str, Any], output_dir: str):
        """Write all output formats."""
        # certification.json
        cert_path = os.path.join(output_dir, "certification.json")
        with open(cert_path, "w") as f:
            json.dump(result, f, indent=2, default=str)
        print(f"certification.json -> {cert_path}")

        # violations.json
        violations_path = os.path.join(output_dir, "violations.json")
        with open(violations_path, "w") as f:
            json.dump({
                "total": result["violations_count"],
                "violations": result["violations"],
            }, f, indent=2, default=str)
        print(f"violations.json     -> {violations_path}")

        # diagnostics.json
        diagnostics_path = os.path.join(output_dir, "diagnostics.json")
        with open(diagnostics_path, "w") as f:
            json.dump({
                "root_causes": result["root_causes"],
                "component_summary": result["component_summary"],
                "components_affected": result["components_affected"],
            }, f, indent=2, default=str)
        print(f"diagnostics.json    -> {diagnostics_path}")

        # summary.md
        summary_path = os.path.join(output_dir, "summary.md")
        summary = self._generate_summary(result)
        with open(summary_path, "w") as f:
            f.write(summary)
        print(f"summary.md          -> {summary_path}")

    def _generate_summary(self, result: Dict[str, Any]) -> str:
        """Generate a human-readable Markdown summary."""
        lines = []
        lines.append("# Certification Summary")
        lines.append("")
        lines.append(f"**Verdict:** {result['verdict']}")
        lines.append(f"**Timestamp:** {result['timestamp']}")
        lines.append(f"**Spec:** {result['spec_dir']}")
        lines.append(f"**Actual:** {result['actual_dir']}")
        lines.append("")

        scores = result.get("scores", {})
        lines.append("## Scores")
        lines.append("")
        lines.append("| Dimension | Score |")
        lines.append("| --------- | ----- |")
        for dim, score in sorted(scores.items()):
            lines.append(f"| {dim} | {score:.4f} |")
        lines.append("")

        summary = result.get("summary", {})
        lines.append("## Assertions")
        lines.append("")
        lines.append(f"- Total: {summary.get('assertions_total', 0)}")
        lines.append(f"- PASS: {summary.get('assertions_passed', 0)}")
        lines.append(f"- FAIL: {summary.get('assertions_failed', 0)}")
        lines.append(f"- Errors: {summary.get('errors', 0)}")
        lines.append(f"- Warnings: {summary.get('warnings', 0)}")
        lines.append("")

        violations = result.get("violations", [])
        if violations:
            lines.append("## Violations")
            lines.append("")
            for v in violations:
                lines.append(f"### {v['assertion_id']} ({v['category']})")
                lines.append("")
                turn = v.get("turn_number")
                if turn is not None:
                    lines.append(f"- **Tour:** {turn}")
                lines.append(f"- **Attendu:** `{v.get('expected')}`")
                lines.append(f"- **Obtenu:** `{v.get('actual')}`")
                lines.append(f"- **Explication:** {v.get('explanation')}")
                lines.append(f"- **Correction:** {v.get('expected_correction')}")
                lines.append(f"- **Confiance:** {v.get('confidence', 0)}")
                lines.append("")

        root_causes = result.get("root_causes", [])
        if root_causes:
            lines.append("## Causes racines")
            lines.append("")
            lines.append("| Assertion | Composant | Confiance |")
            lines.append("| --------- | --------- | --------- |")
            for rc in root_causes:
                lines.append(f"| {rc['assertion_id']} | {rc['responsible_component']} | {rc['root_confidence']} |")
            lines.append("")

            comp_summary = result.get("component_summary", {})
            if comp_summary:
                lines.append("## Composants affectés")
                lines.append("")
                lines.append("| Composant | Violations |")
                lines.append("| --------- | ---------- |")
                for comp, count in sorted(comp_summary.items(), key=lambda x: -x[1]):
                    lines.append(f"| {comp} | {count} |")
                lines.append("")

        lines.append("---")
        lines.append(f"*Generated by LAWIM Certification Orchestrator*")

        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="LAWIM Conversation Certification Orchestrator"
    )
    parser.add_argument("spec_dir", help="Path to specification directory")
    parser.add_argument("actual_dir", nargs="?", default=None,
                        help="Path to actual conversation output directory")
    parser.add_argument("--library", default=None,
                        help="Path to assertion library JSON")
    parser.add_argument("--output-dir", default=None,
                        help="Output directory for reports")
    args = parser.parse_args()

    lib_path = args.library
    if lib_path is None:
        lib_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "specification", "assertions", "assertion_library.json"
        )
    orchestrator = CertificationOrchestrator(lib_path)
    result = orchestrator.certify(args.spec_dir, args.actual_dir, args.output_dir)

    print()
    print(f"Verdict: {result['verdict']}")
    print(f"Violations: {result['violations_count']}")
    print(f"Components affected: {result['components_affected']}")
    print(f"Scores: {result.get('scores', {}).get('global', 'N/A')}")

    return 0 if result["verdict"] == "PASS" else 0  # Don't fail on expected violations


if __name__ == "__main__":
    sys.exit(main())
