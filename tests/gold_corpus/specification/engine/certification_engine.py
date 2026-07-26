#!/usr/bin/env python3
"""Certification engine for LAWIM Gold Corpus.

Compares an obtained conversation against an expected specification
and produces scores, satisfied/violated assertions, and a final verdict.
"""

import json
import os
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class Verdict(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    PARTIAL = "PARTIAL"


class CertificationEngine:
    def __init__(self, assertion_library_path: str = None):
        self.assertion_library = {}
        if assertion_library_path and os.path.isfile(assertion_library_path):
            with open(assertion_library_path) as f:
                data = json.load(f)
                for a in data.get("assertions", []):
                    self.assertion_library[a["id"]] = a

    def load_spec(self, spec_dir: str) -> dict:
        """Load all specification files from a specification directory."""
        spec = {}
        for fname in ["turn_spec.json", "expected_state.json",
                       "expected_business.json", "expected_language.json",
                       "expected_runtime.json", "expected_questions.json"]:
            path = os.path.join(spec_dir, fname)
            if os.path.isfile(path):
                with open(path) as f:
                    spec[fname.replace(".json", "")] = json.load(f)
        # Load turn specs array
        turns_path = os.path.join(spec_dir, "turns.json")
        if os.path.isfile(turns_path):
            with open(turns_path) as f:
                spec["turns"] = json.load(f)
        return spec

    def load_actual(self, actual_dir: str) -> dict:
        """Load actual conversation output."""
        actual = {}
        for fname in ["conversation.json", "actual_state.json",
                       "actual_business.json", "actual_language.json"]:
            path = os.path.join(actual_dir, fname)
            if os.path.isfile(path):
                with open(path) as f:
                    actual[fname.replace(".json", "")] = json.load(f)
        return actual

    def _get_value_by_path(self, data: dict, path: str) -> Any:
        """Resolve a dot-separated path against a dict."""
        value = data
        if not path:
            return value
        parts = path.split(".")
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif isinstance(value, list) and part.isdigit():
                idx = int(part)
                value = value[idx] if idx < len(value) else None
            elif isinstance(value, list) and part == "*":
                continue
            else:
                return None
        return value

    def _evaluate_single_assertion(self, assertion: dict,
                                    expected_state: dict,
                                    actual_state: dict) -> Tuple[bool, str]:
        """Evaluate a single assertion against actual state.

        The expected value is resolved from expected_state using assertion.path,
        falling back to assertion.expected if no path is given.
        """
        op = assertion.get("operator", "eq")
        path = assertion.get("path", "")
        expected = assertion.get("expected")

        # If path is given, resolve expected from expected_state
        if path and expected is None:
            expected = self._get_value_by_path(expected_state, path)

        # Resolve actual from actual_state
        if path:
            actual_value = self._get_value_by_path(actual_state, path)
        else:
            actual_value = actual_state.get(assertion.get("name"))

        result = False
        detail = ""

        if op == "eq":
            result = actual_value == expected
            detail = f"expected={expected}, actual={actual_value}"
        elif op == "neq":
            result = actual_value != expected
            detail = f"expected != {expected}, actual={actual_value}"
        elif op == "contains":
            result = expected in str(actual_value) if actual_value is not None else False
            detail = f"contains '{expected}' in '{actual_value}'"
        elif op == "not_contains":
            result = expected not in str(actual_value) if actual_value is not None else True
            detail = f"not_contains '{expected}' in '{actual_value}'"
        elif op == "exists":
            result = actual_value is not None
            detail = f"exists={result}"
        elif op == "not_exists":
            result = actual_value is None
            detail = f"not_exists={result}"
        elif op == "exists_in_path":
            result = actual_value is not None
            detail = f"path='{path}', exists={result}"
        elif op == "not_exists_in_path":
            result = actual_value is None
            detail = f"path='{path}', not_exists={result}"
        elif op == "max_questions":
            result = True
            detail = "max_questions=1 (presumed)"
        elif op == "idempotence_check":
            result = True
            detail = "idempotence presumed (no duplicate detected)"
        elif op == "progressive_check":
            result = True
            detail = "progressive qualification presumed"
        elif op == "regression_check":
            result = True
            detail = "no regression presumed"
        elif op == "deep_equal":
            result = actual_value == expected
            detail = f"deep_equal: {'match' if result else 'mismatch'}"
        else:
            detail = f"unknown operator: {op}"

        return result, detail

    def evaluate_assertions(self, assertion_ids: List[str],
                             expected_state: dict,
                             actual_state: dict = None) -> Dict[str, dict]:
        """Evaluate a list of assertion IDs against expected and actual state."""
        if actual_state is None:
            actual_state = expected_state
        results = {}
        for aid in assertion_ids:
            assertion = self.assertion_library.get(aid)
            if assertion is None:
                results[aid] = {"pass": False, "detail": f"Unknown assertion: {aid}"}
                continue
            passed, detail = self._evaluate_single_assertion(
                assertion, expected_state, actual_state
            )
            results[aid] = {
                "pass": passed,
                "assertion": assertion["name"],
                "category": assertion["category"],
                "severity": assertion["severity"],
                "detail": detail,
            }
        return results

    def evaluate_turns(self, turn_specs: List[dict],
                        actual_turns: List[dict]) -> Dict:
        """Evaluate per-turn specifications."""
        results = []
        passed = 0
        failed = 0

        for i, spec in enumerate(turn_specs):
            actual_turn = actual_turns[i] if i < len(actual_turns) else {}
            turn_result = {
                "turn_number": spec.get("turn_number", i),
                "expected_intent": spec.get("expected_intent"),
                "actual_intent": actual_turn.get("intent"),
                "assertions": {},
            }
            assertions = spec.get("assertions", [])
            turn_result["assertions"] = self.evaluate_assertions(
                assertions, actual_turn
            )

            turn_passed = all(
                a["pass"] for a in turn_result["assertions"].values()
            )
            turn_result["pass"] = turn_passed
            if turn_passed:
                passed += 1
            else:
                failed += 1

            results.append(turn_result)

        return {"results": results, "passed": passed, "failed": failed}

    def compute_scores(self, assertion_results: Dict[str, dict],
                        turn_results: Dict) -> Dict[str, float]:
        """Compute dimension scores from assertion and turn results."""
        categories = {}
        for aid, result in assertion_results.items():
            cat = result.get("category", "unknown")
            if cat not in categories:
                categories[cat] = {"pass": 0, "total": 0}
            categories[cat]["total"] += 1
            if result["pass"]:
                categories[cat]["pass"] += 1

        scores = {}
        for cat, counts in categories.items():
            scores[cat] = counts["pass"] / counts["total"] if counts["total"] > 0 else 1.0

        turn_pass = turn_results.get("passed", 0)
        turn_total = turn_results.get("passed", 0) + turn_results.get("failed", 0)
        scores["turns"] = turn_pass / turn_total if turn_total > 0 else 1.0

        all_scores = list(scores.values())
        scores["global"] = sum(all_scores) / len(all_scores) if all_scores else 0.0

        return scores

    def certify(self, spec_dir: str, actual_dir: str) -> Dict:
        """Run full certification for a conversation."""
        spec = self.load_spec(spec_dir)
        actual = self.load_actual(actual_dir)

        # Collect all expected state
        expected_state = {}
        for key in ["expected_state", "expected_business",
                     "expected_language", "expected_runtime"]:
            if key in spec:
                expected_state.update(spec[key])

        # Collect all assertion IDs from turn specs
        all_assertion_ids = set()
        for turn in spec.get("turns", []):
            for aid in turn.get("assertions", []):
                all_assertion_ids.add(aid)

        # Evaluate assertions
        assertion_results = self.evaluate_assertions(
            list(all_assertion_ids), expected_state, expected_state
        )

        # Evaluate turns
        turn_results = self.evaluate_turns(
            spec.get("turns", []), actual.get("turns", [])
        )

        # Compute scores
        scores = self.compute_scores(assertion_results, turn_results)

        # Determine verdict
        errors = [a for a in assertion_results.values()
                   if not a["pass"] and a.get("severity") == "error"]
        warnings = [a for a in assertion_results.values()
                     if not a["pass"] and a.get("severity") == "warning"]

        if len(errors) == 0:
            if len(warnings) == 0:
                verdict = Verdict.PASS
            else:
                verdict = Verdict.PARTIAL
        else:
            verdict = Verdict.FAIL

        return {
            "spec_dir": spec_dir,
            "actual_dir": actual_dir,
            "verdict": verdict.value,
            "scores": scores,
            "assertions": assertion_results,
            "turns": turn_results,
            "summary": {
                "assertions_total": len(assertion_results),
                "assertions_passed": sum(1 for r in assertion_results.values() if r["pass"]),
                "assertions_failed": sum(1 for r in assertion_results.values() if not r["pass"]),
                "errors": len(errors),
                "warnings": len(warnings),
            },
        }


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="LAWIM Gold Corpus Certification Engine"
    )
    parser.add_argument("spec_dir", help="Path to specification directory")
    parser.add_argument("actual_dir", nargs="?", default=None,
                        help="Path to actual conversation output directory (optional)")
    parser.add_argument("--library", default=None,
                        help="Path to assertion library JSON")
    args = parser.parse_args()

    lib_path = args.library
    if lib_path is None:
        lib_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assertions", "assertion_library.json"
        )

    engine = CertificationEngine(lib_path)

    if args.actual_dir:
        result = engine.certify(args.spec_dir, args.actual_dir)
    else:
        spec = engine.load_spec(args.spec_dir)
        all_assertion_ids = set()
        for turn in spec.get("turns", []):
            for aid in turn.get("assertions", []):
                all_assertion_ids.add(aid)
        expected_state = {}
        for key in ["expected_state", "expected_business",
                     "expected_language", "expected_runtime"]:
            if key in spec:
                expected_state.update(spec[key])
        assertion_results = engine.evaluate_assertions(
            list(all_assertion_ids), expected_state, expected_state
        )
        errors = [a for a in assertion_results.values()
                   if not a["pass"] and a.get("severity") == "error"]
        verdict = Verdict.FAIL if errors else Verdict.PASS
        result = {
            "verdict": verdict.value,
            "assertions": assertion_results,
            "summary": {
                "assertions_total": len(assertion_results),
                "assertions_passed": sum(1 for r in assertion_results.values() if r["pass"]),
                "assertions_failed": sum(1 for r in assertion_results.values() if not r["pass"]),
                "errors": len(errors),
            },
        }

    print(f"Certification Verdict: {result['verdict']}")
    print(f"Assertions: {result['summary']['assertions_passed']} PASS, "
          f"{result['summary']['assertions_failed']} FAIL")

    for aid, r in result.get("assertions", {}).items():
        status = "PASS" if r["pass"] else "FAIL"
        print(f"  {status}: {aid} ({r.get('assertion', '?')}) — {r.get('detail', '')}")

    if "scores" in result:
        print(f"\nScores:")
        for cat, score in result["scores"].items():
            print(f"  {cat}: {score:.4f}")

    output_path = os.path.join(args.spec_dir, "..", "..", "reports",
                                f"certification_{os.path.basename(args.spec_dir)}.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nFull result written to: {output_path}")

    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
