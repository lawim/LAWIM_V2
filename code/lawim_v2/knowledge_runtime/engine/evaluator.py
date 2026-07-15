from __future__ import annotations

from typing import Any

from ..service import KnowledgeService
from .readiness import ReadinessEvaluator
from .resolver import NextQuestionResolver


class QualificationEngine:
    def __init__(self, service: KnowledgeService) -> None:
        self._service = service
        self._readiness = ReadinessEvaluator(service.readiness_registry)
        self._resolver = NextQuestionResolver(
            service.question_rule_registry,
            service.matrix_registry,
        )

    def evaluate(
        self,
        known_fields: dict[str, Any],
        *,
        property_type: str | None = None,
        family: str | None = None,
        matrix_id: str | None = None,
    ) -> dict[str, Any]:
        readiness = self._readiness.evaluate(known_fields, family=family)
        next_q = self._resolver.resolve_next(
            known_fields,
            property_type=property_type,
            family=family,
            matrix_id=matrix_id,
        )

        return {
            "readiness": readiness,
            "next_question": next_q,
            "known_field_count": len(known_fields),
        }

    def readiness_summary(self, known_fields: dict[str, Any]) -> dict[str, Any]:
        return self._readiness.readiness_summary(known_fields)

    def next_question(
        self,
        known_fields: dict[str, Any],
        *,
        property_type: str | None = None,
        family: str | None = None,
        matrix_id: str | None = None,
    ) -> dict[str, Any]:
        return self._resolver.resolve_next(
            known_fields,
            property_type=property_type,
            family=family,
            matrix_id=matrix_id,
        )
