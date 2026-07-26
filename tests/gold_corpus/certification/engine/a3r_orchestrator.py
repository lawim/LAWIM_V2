#!/usr/bin/env python3
"""A.3R Orchestrator — Certification avec exécution runtime réelle.

Pipeline :
  1. ExpectedSpecLoader → expected (depuis fichiers corpus)
  2. RuntimeExecutor → actual (exécution runtime réelle)
  3. RuntimeComparator → différences, violations, score
  4. Output writer → certification.json, violations.json, runtime-trace.json, summary.md
"""

import json
import os
import sys
import time
from datetime import datetime, timezone

_base = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(_base, "lawim_runtime"))
sys.path.insert(0, os.path.join(_base, "code"))
sys.path.insert(0, _base)

from tests.gold_corpus.certification.runtime.expected_loader import ExpectedSpecLoader
from tests.gold_corpus.certification.runtime.executor import RuntimeExecutor
from tests.gold_corpus.certification.engine.runtime_comparator import RuntimeComparator, check_tautology


class A3ROrchestrator:
    def __init__(self):
        self.executor = RuntimeExecutor()
        self.comparator = RuntimeComparator()

    def certify(self, spec_dir: str, output_dir: str = None) -> dict:
        if output_dir is None:
            output_dir = os.path.join(
                os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..")),
                "output", "runtime-a3r",
                os.path.basename(spec_dir),
            )
        os.makedirs(output_dir, exist_ok=True)

        # 1. Load expected
        loader = ExpectedSpecLoader(spec_dir)
        expected = loader.load_all()
        conversation_spec = expected.get("conversation", {})
        if not conversation_spec:
            return {"verdict": "SPEC_INVALID", "error": "No conversation.json found"}

        # 2. Execute runtime
        run = self.executor.execute_conversation(conversation_spec)

        # 3. Compare
        result = self.comparator.compare(expected, run)

        # 4. Add metadata
        result["spec_dir"] = spec_dir
        result["timestamp"] = datetime.now(timezone.utc).isoformat()
        result["expected_loader"] = "ExpectedSpecLoader"
        result["actual_executor"] = "RuntimeExecutor"
        result["expected_type"] = "CORPUS_FILE"
        result["actual_type"] = "RUNTIME_EXECUTION"

        # 5. Determine verdict
        if not result["runtime_called"] or result["call_count"] == 0:
            result["verdict"] = "NOT_EXECUTED"
        elif not result["tautology_check"]:
            result["verdict"] = "TAUTOLOGY_DETECTED"
        elif result["assertions_failed"] > 0:
            result["verdict"] = "RUNTIME_FAIL"
        else:
            result["verdict"] = "RUNTIME_PASS"

        # 6. Write outputs
        self._write_outputs(result, output_dir, run)
        self._write_trace(run, output_dir)

        return result

    def _write_outputs(self, result: dict, output_dir: str, run=None):
        cert_path = os.path.join(output_dir, "certification.json")
        with open(cert_path, "w") as f:
            json.dump(result, f, indent=2, default=str)

        violations = result.get("violations", [])
        vio_path = os.path.join(output_dir, "violations.json")
        with open(vio_path, "w") as f:
            json.dump({"total": len(violations), "violations": violations}, f, indent=2)

        diag_path = os.path.join(output_dir, "diagnostics.json")
        with open(diag_path, "w") as f:
            json.dump({
                "tautology": result["tautology_check"],
                "runtime_called": result["runtime_called"],
                "call_count": result["call_count"],
                "adapter": result.get("adapter_class", ""),
                "orchestrator": result.get("orchestrator_class", ""),
                "violations": [
                    {"id": v["assertion_id"], "category": v["category"],
                     "detail": v["detail"]}
                    for v in violations
                ],
            }, f, indent=2)

        summary = self._generate_summary(result)
        with open(os.path.join(output_dir, "summary.md"), "w") as f:
            f.write(summary)

    def _write_trace(self, run, output_dir: str):
        trace = []
        for t in run.turns:
            trace.append({
                "turn_index": t.turn_index,
                "user_input": t.user_input,
                "assistant_output": t.assistant_output,
                "intent_detected": t.intent_detected,
                "facts_after": t.facts_after,
                "pending_after": t.pending_after,
                "business_actions": t.business_actions,
                "duration_ms": round(t.duration_ms, 2),
                "error": t.error,
            })
        trace_path = os.path.join(output_dir, "runtime-trace.json")
        with open(trace_path, "w") as f:
            json.dump({
                "conversation_id": run.conversation_id,
                "runtime_called": run.runtime_called,
                "adapter_class": run.adapter_class,
                "orchestrator_class": run.orchestrator_class,
                "total_duration_ms": round(run.total_duration_ms, 2),
                "call_count": run.call_count,
                "turns": trace,
            }, f, indent=2)

    def _generate_summary(self, result: dict) -> str:
        lines = []
        lines.append("# A.3R Runtime Certification Summary\n")
        lines.append(f"**Verdict:** {result.get('verdict', 'UNKNOWN')}")
        lines.append(f"**Runtime called:** {result.get('runtime_called', False)}")
        lines.append(f"**Adapter:** {result.get('adapter_class', 'N/A')}")
        lines.append(f"**Orchestrator:** {result.get('orchestrator_class', 'N/A')}")
        lines.append(f"**Call count:** {result.get('call_count', 0)}")
        lines.append(f"**Tautology check:** {result.get('tautology_check', False)}")
        lines.append(f"**Expected type:** {result.get('expected_type', '?')}")
        lines.append(f"**Actual type:** {result.get('actual_type', '?')}")
        lines.append("")
        lines.append("## Assertions")
        lines.append(f"- Total: {result.get('assertions_total', 0)}")
        lines.append(f"- PASS: {result.get('assertions_passed', 0)}")
        lines.append(f"- FAIL: {result.get('assertions_failed', 0)}")
        lines.append("")
        if result.get("violations"):
            lines.append("## Violations")
            for v in result["violations"]:
                lines.append(f"- {v['assertion_id']}: {v['detail']}")
        return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="A.3R Runtime Certification")
    parser.add_argument("spec_dir", help="Path to conversation directory")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    args = parser.parse_args()

    orch = A3ROrchestrator()
    result = orch.certify(args.spec_dir, args.output_dir)

    if not args.quiet:
        print(f"A.3R Certification: {result.get('verdict', 'ERROR')}")
        print(f"  Runtime called: {result.get('runtime_called', False)}")
        print(f"  Call count: {result.get('call_count', 0)}")
        print(f"  Tautology check: {result.get('tautology_check', False)}")
        print(f"  Assertions: {result.get('assertions_passed', 0)}P / {result.get('assertions_failed', 0)}F")
        print(f"  Adapter: {result.get('adapter_class', 'N/A')}")
        print(f"  Orchestrator: {result.get('orchestrator_class', 'N/A')}")

    return 0 if result.get("verdict") == "RUNTIME_PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
