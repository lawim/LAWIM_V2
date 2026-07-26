#!/usr/bin/env python3
"""CanonicalComparator — compares expected and actual in canonical form."""

from typing import Any, Dict, List, Tuple

from tests.gold_corpus.certification.canonical.canonical_turn import (
    CanonicalTurn, CanonicalValue,
)


class CanonicalComparator:
    """Compares expected and actual canonical turns, producing violations."""

    def compare(self, expected: CanonicalTurn, actual: CanonicalTurn) -> Dict[str, Any]:
        violations = []

        v = self._compare_values(expected.intent, actual.intent, "intent")
        if v:
            violations.append(v)

        v = self._compare_values(expected.phase, actual.phase, "phase")
        if v:
            violations.append(v)

        v = self._compare_values(expected.pending_user_action,
                                   actual.pending_user_action, "pending_user_action")
        if v:
            violations.append(v)

        v = self._compare_values(expected.business_action,
                                   actual.business_action, "business_action")
        if v:
            violations.append(v)

        v = self._compare_values(expected.conversation_language,
                                   actual.conversation_language, "conversation_language")
        if v:
            violations.append(v)

        fact_vs = self._compare_facts(expected.facts, actual.facts)
        violations.extend(fact_vs)

        return {
            "violations": violations,
            "violation_count": len(violations),
            "passed": len(violations) == 0,
            "expected_intent": expected.intent.value,
            "actual_intent": actual.intent.value,
            "expected_phase": expected.phase.value,
            "actual_phase": actual.phase.value,
            "expected_pending": expected.pending_user_action.value,
            "actual_pending": actual.pending_user_action.value,
            "expected_business": expected.business_action.value,
            "actual_business": actual.business_action.value,
        }

    def _compare_values(self, exp: CanonicalValue, act: CanonicalValue,
                         field: str) -> Dict:
        if exp.value is None:
            return None
        exp_val = str(exp.value).lower().strip() if exp.value else ""
        act_val = str(act.value).lower().strip() if act.value else ""
        if exp_val == "unknown" or act_val == "unknown":
            return None
        if exp_val != act_val:
            return {
                "field": field,
                "expected": exp.value,
                "actual": act.value,
                "expected_source": exp.source,
                "actual_source": act.source,
                "expected_source_type": exp.source_type,
                "actual_source_type": act.source_type,
                "expected_inferred": exp.inferred,
                "actual_inferred": act.inferred,
                "expected_defaulted": exp.defaulted,
                "actual_defaulted": act.defaulted,
            }
        return None

    def _compare_facts(self, exp_facts: Dict[str, CanonicalValue],
                        act_facts: Dict[str, CanonicalValue]) -> List[Dict]:
        violations = []
        for key, exp_val in exp_facts.items():
            if exp_val.value is None:
                continue
            act_val = act_facts.get(key, CanonicalValue())
            norm_key = key.replace("_", "").replace(" ", "").lower()
            act_found = False
            for ak, av in act_facts.items():
                if ak.replace("_", "").replace(" ", "").lower() == norm_key:
                    act_val = av
                    act_found = True
                    break
            if not act_found:
                continue
            if str(exp_val.value).lower().strip() != str(act_val.value).lower().strip():
                violations.append({
                    "field": f"facts.{key}",
                    "expected": exp_val.value,
                    "actual": act_val.value,
                    "expected_source": exp_val.source,
                    "actual_source": act_val.source,
                })
        return violations
