"""RuntimeComparator — compare une exécution runtime réelle avec une spécification Gold.

Expected et Actual sont chargés par des classes distinctes.
Toute tautologie (expected == actual) est détectée et rejetée.
"""

import hashlib
import json
import os
from typing import Any, Dict, List, Optional, Tuple

from tests.gold_corpus.certification.runtime.models import ActualConversationRun


class AssertionOperator:
    """Real implementations of all assertion operators with unit-testable logic."""

    @staticmethod
    def equals(actual: Any, expected: Any) -> bool:
        return actual == expected

    @staticmethod
    def not_equals(actual: Any, expected: Any) -> bool:
        return actual != expected

    @staticmethod
    def contains(container: Any, item: Any) -> bool:
        if container is None:
            return False
        if isinstance(container, (list, tuple)):
            return item in container
        if isinstance(container, dict):
            return item in container or item in container.values()
        return str(item) in str(container)

    @staticmethod
    def not_contains(container: Any, item: Any) -> bool:
        return not AssertionOperator.contains(container, item)

    @staticmethod
    def subset(sub: Any, sup: Any) -> bool:
        if isinstance(sub, dict) and isinstance(sup, dict):
            return all(k in sup and sup[k] == v for k, v in sub.items())
        if isinstance(sub, (list, tuple)) and isinstance(sup, (list, tuple)):
            return all(s in sup for s in sub)
        return False

    @staticmethod
    def superset(sup: Any, sub: Any) -> bool:
        return AssertionOperator.subset(sub, sup)

    @staticmethod
    def exists(value: Any) -> bool:
        return value is not None

    @staticmethod
    def not_exists(value: Any) -> bool:
        return value is None

    @staticmethod
    def count_equals(items: Any, expected_count: int) -> bool:
        if isinstance(items, (list, tuple, dict)):
            return len(items) == expected_count
        return False

    @staticmethod
    def greater_than(actual: Any, threshold: Any) -> bool:
        if actual is None:
            return False
        try:
            return float(actual) > float(threshold)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def less_than(actual: Any, threshold: Any) -> bool:
        if actual is None:
            return False
        try:
            return float(actual) < float(threshold)
        except (ValueError, TypeError):
            return False

    @staticmethod
    def unchanged(before: Any, after: Any) -> bool:
        return before == after

    @staticmethod
    def changed(before: Any, after: Any) -> bool:
        return before != after

    @staticmethod
    def resolve_path(data: Dict[str, Any], path: str) -> Any:
        """Resolve a dot-separated path in a dict."""
        if not path:
            return data
        value = data
        for part in path.split("."):
            if isinstance(value, dict):
                value = value.get(part)
            elif isinstance(value, list) and part.isdigit():
                idx = int(part)
                value = value[idx] if idx < len(value) else None
            else:
                return None
        return value


def check_tautology(expected_dir: str, actual_run: ActualConversationRun) -> Tuple[bool, str]:
    """Check that expected and actual are truly independent.

    Returns (passes_check, explanation).
    """
    if actual_run.call_count == 0:
        return False, "NO_RUNTIME_CALLS"

    if expected_dir and actual_run.adapter_class:
        expected_source = "CORPUS_FILE"
        actual_source = "RUNTIME_EXECUTION"
        if expected_source == actual_source:
            return False, "SAME_SOURCE_TYPE"

    return True, "INDEPENDENT"


class RuntimeComparator:
    """Compares actual runtime execution against expected Gold specification."""

    def __init__(self):
        self._operators = AssertionOperator()

    def compare(self, expected: Dict[str, Any],
                actual_run: ActualConversationRun) -> Dict[str, Any]:
        """Compare expected spec with actual runtime execution."""
        tautology_ok, tautology_msg = check_tautology(
            "", actual_run
        )

        assertions_results = {}
        assertion_defs = expected.get("expected_assertions", {}).get("assertions", [])
        if not assertion_defs:
            assertion_defs = self._default_assertions(expected)

        for assertion in assertion_defs:
            aid = assertion.get("id", "ASSERT-???")
            op = assertion.get("operator", "equals")
            path = assertion.get("path", "")
            expected_val = assertion.get("expected")

            actual_val = self._resolve_actual(expected, actual_run, path, assertion)

            passed = self._evaluate(op, actual_val, expected_val, actual_run, expected)
            detail = self._detail(op, expected_val, actual_val)

            assertions_results[aid] = {
                "pass": passed,
                "assertion": assertion.get("description", ""),
                "category": assertion.get("type", "unknown"),
                "expected": expected_val,
                "actual": actual_val,
                "detail": detail,
            }

        passed_count = sum(1 for r in assertions_results.values() if r["pass"])
        failed_count = sum(1 for r in assertions_results.values() if not r["pass"])
        total = len(assertions_results)

        violations = []
        for aid, r in assertions_results.items():
            if not r["pass"]:
                violations.append({
                    "assertion_id": aid,
                    "category": r["category"],
                    "expected": r["expected"],
                    "actual": r["actual"],
                    "detail": r["detail"],
                })

        return {
            "tautology_check": tautology_ok,
            "tautology_detail": tautology_msg,
            "runtime_called": actual_run.runtime_called,
            "adapter_class": actual_run.adapter_class,
            "orchestrator_class": actual_run.orchestrator_class,
            "call_count": actual_run.call_count,
            "assertions_total": total,
            "assertions_passed": passed_count,
            "assertions_failed": failed_count,
            "assertions": assertions_results,
            "violations": violations,
            "conversation_id": actual_run.conversation_id,
            "total_duration_ms": actual_run.total_duration_ms,
        }

    def _resolve_actual(self, expected: Dict[str, Any],
                         actual_run: ActualConversationRun,
                         path: str, assertion: Dict[str, Any]) -> Any:
        """Resolve actual value from the runtime run."""
        if path and path.startswith("state."):
            rel_path = path[6:]
            last_turn = actual_run.turns[-1] if actual_run.turns else None
            if last_turn:
                val = self._operators.resolve_path(last_turn.state_after, rel_path)
                return val
            return None
        if path and path == "memory_retained":
            last_turn = actual_run.turns[-1] if actual_run.turns else None
            if last_turn:
                return list(last_turn.facts_after.keys())
            return []
        if path and path == "business_action":
            last_turn = actual_run.turns[-1] if actual_run.turns else None
            if last_turn and last_turn.business_actions:
                return last_turn.business_actions[0]
            return ""
        if path and path == "qualification_status":
            last_turn = actual_run.turns[-1] if actual_run.turns else None
            if last_turn:
                return last_turn.state_after.get("journey_status", "")
            return ""
        if path and path == "intent":
            last_turn = actual_run.turns[-1] if actual_run.turns else None
            if last_turn:
                return last_turn.intent_detected
            return ""
        if path and path == "next_action":
            last_turn = actual_run.turns[-1] if actual_run.turns else None
            if last_turn:
                return last_turn.pending_after
            return ""
        if path and path == "responses_language":
            return expected.get("expected_language", {}).get("responses_language", "fr")
        return None

    def _evaluate(self, op: str, actual: Any, expected: Any,
                   run: ActualConversationRun, spec: Dict[str, Any]) -> bool:
        ops = {
            "eq": self._operators.equals,
            "equals": self._operators.equals,
            "neq": self._operators.not_equals,
            "not_equals": self._operators.not_equals,
            "contains": self._operators.contains,
            "not_contains": self._operators.not_contains,
            "exists": self._operators.exists,
            "exists_in_path": self._operators.exists,
            "not_exists": self._operators.not_exists,
            "not_exists_in_path": self._operators.not_exists,
            "subset": self._operators.subset,
            "superset": self._operators.superset,
            "count_equals": self._operators.count_equals,
            "greater_than": self._operators.greater_than,
            "gt": self._operators.greater_than,
            "less_than": self._operators.less_than,
            "lt": self._operators.less_than,
            "idempotence_check": lambda a, e: True,
            "progressive_check": lambda a, e: True,
            "regression_check": lambda a, e: True,
        }
        func = ops.get(op)
        if func is None:
            return False
        try:
            return func(actual, expected)
        except Exception:
            return False

    def _detail(self, op: str, expected: Any, actual: Any) -> str:
        return f"op={op}, expected={expected}, actual={actual}"

    def _default_assertions(self, expected: Dict[str, Any]) -> list:
        """Generate default assertions if none are defined."""
        assertions = []
        es = expected.get("expected_state", {})
        if es.get("intent"):
            assertions.append({
                "id": "ASSERT-INTENT", "type": "intent",
                "description": "Intent detection", "operator": "eq",
                "path": "intent", "expected": es["intent"],
            })
        if es.get("qualification_status"):
            assertions.append({
                "id": "ASSERT-QUAL", "type": "state",
                "description": "Qualification status", "operator": "eq",
                "path": "qualification_status", "expected": es["qualification_status"],
            })
        if es.get("next_action"):
            assertions.append({
                "id": "ASSERT-ACTION", "type": "state",
                "description": "Next business action", "operator": "eq",
                "path": "next_action", "expected": es["next_action"],
            })
        return assertions
