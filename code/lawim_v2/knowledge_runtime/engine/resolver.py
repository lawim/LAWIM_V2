from __future__ import annotations

from typing import Any

from ..models.qualification import QualificationMatrix
from ..registry.matrix_registry import MatrixRegistry
from ..registry.question_rule_registry import QuestionRuleRegistry


class NextQuestionResolver:
    def __init__(
        self,
        question_registry: QuestionRuleRegistry,
        matrix_registry: MatrixRegistry,
    ) -> None:
        self._question_registry = question_registry
        self._matrix_registry = matrix_registry

    def resolve_next(
        self,
        known_fields: dict[str, Any],
        *,
        property_type: str | None = None,
        family: str | None = None,
        matrix_id: str | None = None,
    ) -> dict[str, Any]:
        always = self._question_registry.get_by_type("always_ask")
        always_fields = [r.field for r in always]

        for field in always_fields:
            if field not in known_fields:
                return {
                    "field": field,
                    "reason": "always_ask",
                    "priority": 0,
                    "rule_type": "always_ask",
                }

        if matrix_id:
            try:
                matrix = self._matrix_registry.get(matrix_id)
                return self._resolve_from_matrix(matrix, known_fields)
            except Exception:
                pass

        if property_type:
            candidates = self._matrix_registry.list_by_property_type(property_type)
            if candidates:
                matrix = candidates[0]
                return self._resolve_from_matrix(matrix, known_fields)

        if family:
            candidates = self._matrix_registry.list_by_family(family)
            if candidates:
                matrix = candidates[0]
                return self._resolve_from_matrix(matrix, known_fields)

        conditional = self._question_registry.get_by_type("conditional_ask")
        candidates = []
        for rule in conditional:
            if rule.field not in known_fields:
                candidates.append({
                    "field": rule.field,
                    "priority": rule.priority,
                    "reason": f"conditional_ask: {rule.condition or 'any'}",
                    "rule_type": "conditional_ask",
                })

        never_ask = {r.field for r in self._question_registry.get_by_type("never_ask")}

        deduced = {r.field for r in self._question_registry.get_by_type("deduce_from_context")}
        deferred = {r.field for r in self._question_registry.get_by_type("defer_ask")}

        candidates = [
            c for c in candidates
            if c["field"] not in never_ask
            and c["field"] not in deduced
            and c["field"] not in deferred
        ]

        if not candidates:
            for rule in conditional:
                if rule.field not in known_fields and rule.field not in never_ask:
                    candidates.append({
                        "field": rule.field,
                        "priority": rule.priority,
                        "reason": "conditional_ask",
                        "rule_type": "conditional_ask",
                    })
                    break

        if not candidates:
            return {"field": None, "reason": "all_fields_known", "priority": None, "rule_type": None}

        candidates.sort(key=lambda c: (c["priority"] if c["priority"] is not None else 999))
        return candidates[0]

    def _resolve_from_matrix(
        self,
        matrix: QualificationMatrix,
        known_fields: dict[str, Any],
    ) -> dict[str, Any]:
        never_ask = {r.field for r in self._question_registry.get_by_type("never_ask")}

        for field_group in (
            matrix.minimum_intake_fields,
            matrix.minimum_search_fields,
            matrix.minimum_matching_fields,
            matrix.minimum_introduction_fields,
            matrix.minimum_visit_fields,
            matrix.minimum_transaction_fields,
            matrix.recommended_fields,
            matrix.optional_fields,
        ):
            for field in field_group:
                if field not in known_fields and field not in never_ask:
                    return {
                        "field": field,
                        "reason": f"required_in_{field_group}",
                        "priority": 0,
                        "rule_type": "matrix_field",
                    }

        conditional = self._question_registry.get_by_type("conditional_ask")
        for rule in conditional:
            if rule.field not in known_fields and rule.field not in never_ask:
                return {
                    "field": rule.field,
                    "reason": f"conditional: {rule.condition or 'any'}",
                    "priority": rule.priority,
                    "rule_type": "conditional_ask",
                }

        return {"field": None, "reason": "all_fields_known", "priority": None, "rule_type": None}
