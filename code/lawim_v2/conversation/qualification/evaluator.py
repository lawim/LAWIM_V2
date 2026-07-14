from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .matrices import QualificationMatrix, get_matrix, get_readiness_score, get_next_field
from .readiness import ReadinessLevel, ReadinessCalculator, DEFAULT_THRESHOLDS
from .priority import PriorityCalculator, FieldPriority
from .registry import MatrixRegistry, get_registry


@dataclass
class MissingField:
    field: str
    category: str = "required"
    priority: int = 999
    validation_rule: str | None = None
    clarification_rule: str | None = None


@dataclass
class EvaluationResult:
    intent: str
    transaction_type: str | None = None
    property_type: str | None = None
    readiness_level: ReadinessLevel = ReadinessLevel.NOT_STARTED
    readiness_score: float = 0.0
    missing_required_fields: list[MissingField] = field(default_factory=list)
    missing_recommended_fields: list[MissingField] = field(default_factory=list)
    next_field_to_ask: str | None = None
    next_field_priority: FieldPriority | None = None
    is_ready_for_search: bool = False
    is_relationship_ready: bool = False
    can_proceed: bool = False
    matrix: QualificationMatrix | None = None
    field_values: dict[str, Any] = field(default_factory=dict)


class QualificationEvaluator:
    def __init__(
        self,
        registry: MatrixRegistry | None = None,
        readiness_calculator: ReadinessCalculator | None = None,
        priority_calculator: PriorityCalculator | None = None,
    ):
        self._registry = registry or get_registry()
        self._readiness = readiness_calculator or ReadinessCalculator()
        self._priority = priority_calculator or PriorityCalculator()

    def evaluate(
        self,
        intent: str,
        known_facts: dict[str, Any],
        transaction_type: str | None = None,
        property_type: str | None = None,
    ) -> EvaluationResult:
        matrix = self._registry.get(intent, transaction_type, property_type)
        if matrix is None:
            matrix = get_matrix(intent, transaction_type, property_type)

        if matrix is None:
            return EvaluationResult(
                intent=intent,
                readiness_level=ReadinessLevel.NOT_STARTED,
                readiness_score=0.0,
                is_ready_for_search=False,
                is_relationship_ready=False,
                can_proceed=False,
                field_values=dict(known_facts),
            )

        readiness_score = get_readiness_score(matrix, known_facts)
        readiness_level = self._readiness.calculate(matrix, known_facts)
        is_search_ready = self._readiness.is_search_ready(matrix, known_facts)
        is_relationship_ready = self._readiness.is_relationship_ready(matrix, known_facts)

        missing_required = [
            MissingField(
                field=f,
                category="required",
                priority=matrix.get_field_priority(f),
                validation_rule=matrix.get_validation_rule(f),
                clarification_rule=matrix.get_clarification_rule(f),
            )
            for f in matrix.required_fields
            if f not in known_facts
        ]

        missing_recommended = [
            MissingField(
                field=f,
                category="recommended",
                priority=matrix.get_field_priority(f),
                validation_rule=matrix.get_validation_rule(f),
                clarification_rule=matrix.get_clarification_rule(f),
            )
            for f in matrix.recommended_fields
            if f not in known_facts
        ]

        missing_required.sort(key=lambda mf: mf.priority)
        missing_recommended.sort(key=lambda mf: mf.priority)

        next_priority = self._priority.get_next_question_field(matrix, known_facts)
        next_field = next_priority.field if next_priority else get_next_field(matrix, known_facts)

        can_proceed = readiness_score >= matrix.readiness_threshold

        return EvaluationResult(
            intent=intent,
            transaction_type=matrix.transaction_type,
            property_type=matrix.property_type,
            readiness_level=readiness_level,
            readiness_score=readiness_score,
            missing_required_fields=missing_required,
            missing_recommended_fields=missing_recommended,
            next_field_to_ask=next_field,
            next_field_priority=next_priority,
            is_ready_for_search=is_search_ready,
            is_relationship_ready=is_relationship_ready,
            can_proceed=can_proceed,
            matrix=matrix,
            field_values=dict(known_facts),
        )

    def validate_field_value(
        self,
        matrix: QualificationMatrix,
        field: str,
        value: Any,
    ) -> tuple[bool, str | None]:
        rule = matrix.get_validation_rule(field)
        if rule is None:
            return True, None

        if rule == "positive_integer":
            try:
                val = int(value)
                if val <= 0:
                    return False, f"{field} must be a positive integer"
            except (ValueError, TypeError):
                return False, f"{field} must be a positive integer"
            return True, None

        if rule == "non_negative_integer":
            try:
                val = int(value)
                if val < 0:
                    return False, f"{field} must be a non-negative integer"
            except (ValueError, TypeError):
                return False, f"{field} must be a non-negative integer"
            return True, None

        if rule == "positive_number":
            try:
                val = float(value)
                if val <= 0:
                    return False, f"{field} must be a positive number"
            except (ValueError, TypeError):
                return False, f"{field} must be a positive number"
            return True, None

        if rule == "known_city":
            if not value or not isinstance(value, str) or len(value.strip()) < 2:
                return False, f"{field} must be a valid city name"
            return True, None

        if rule == "percentage":
            try:
                val = float(value)
                if val < 0 or val > 100:
                    return False, f"{field} must be between 0 and 100"
            except (ValueError, TypeError):
                return False, f"{field} must be a valid percentage"
            return True, None

        return True, None

    def get_clarification_prompt(
        self,
        matrix: QualificationMatrix,
        field: str,
    ) -> str | None:
        return matrix.get_clarification_rule(field)

    def evaluate_multiple(
        self,
        evaluations: list[tuple[str, dict[str, Any], str | None, str | None]],
    ) -> list[EvaluationResult]:
        return [
            self.evaluate(intent=intent, known_facts=known_facts, transaction_type=transaction_type, property_type=property_type)
            for intent, known_facts, transaction_type, property_type in evaluations
        ]

    def best_candidate(
        self,
        evaluations: list[EvaluationResult],
    ) -> EvaluationResult | None:
        if not evaluations:
            return None
        return max(evaluations, key=lambda e: (e.readiness_score, len(e.missing_required_fields) == 0))
