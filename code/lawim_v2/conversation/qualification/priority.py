from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from .matrices import QualificationMatrix


class FieldUrgency(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    NOT_NEEDED = "NOT_NEEDED"


@dataclass(frozen=True)
class FieldPriority:
    field: str
    urgency: FieldUrgency
    priority_score: int
    reason: str = ""


class PriorityCalculator:
    REQUIRED_BASE_PRIORITY = 100
    RECOMMENDED_BASE_PRIORITY = 50
    OPTIONAL_BASE_PRIORITY = 10

    def calculate_field_priority(
        self,
        matrix: QualificationMatrix,
        field: str,
        known_facts: dict[str, Any],
    ) -> FieldPriority:
        if field in known_facts:
            return FieldPriority(
                field=field,
                urgency=FieldUrgency.NOT_NEEDED,
                priority_score=0,
                reason="already_known",
            )

        matrix_priority = matrix.get_field_priority(field)

        if matrix.is_field_required(field):
            urgency = FieldUrgency.CRITICAL
            score = self.REQUIRED_BASE_PRIORITY + (100 - matrix_priority)
        elif matrix.is_field_recommended(field):
            urgency = FieldUrgency.HIGH
            score = self.RECOMMENDED_BASE_PRIORITY + (100 - matrix_priority)
        elif field in matrix.optional_fields:
            urgency = FieldUrgency.MEDIUM
            score = self.OPTIONAL_BASE_PRIORITY + (100 - matrix_priority)
        else:
            return FieldPriority(
                field=field,
                urgency=FieldUrgency.NOT_NEEDED,
                priority_score=0,
                reason="not_in_matrix",
            )

        return FieldPriority(field=field, urgency=urgency, priority_score=score, reason="")

    def get_next_question_field(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> FieldPriority | None:
        candidates: list[FieldPriority] = []
        for field in matrix.all_fields:
            fp = self.calculate_field_priority(matrix, field, known_facts)
            if fp.urgency != FieldUrgency.NOT_NEEDED:
                candidates.append(fp)

        if not candidates:
            return None

        candidates.sort(key=lambda fp: (-fp.priority_score, fp.field))
        return candidates[0]

    def get_priority_ordered_fields(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> list[FieldPriority]:
        result: list[FieldPriority] = []
        for field in matrix.all_fields:
            fp = self.calculate_field_priority(matrix, field, known_facts)
            result.append(fp)

        result.sort(key=lambda fp: (-fp.priority_score, fp.field))
        return result

    def get_missing_critical_fields(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> list[str]:
        return [f for f in matrix.required_fields if f not in known_facts]

    def get_missing_high_priority_fields(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> list[str]:
        missing = []
        for field in matrix.required_fields:
            if field not in known_facts:
                missing.append(field)
        for field in matrix.recommended_fields:
            if field not in known_facts:
                missing.append(field)
        return missing
