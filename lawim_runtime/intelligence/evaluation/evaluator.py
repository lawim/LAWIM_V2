from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

logger = logging.getLogger(__name__)


class EvaluationCategory(str, Enum):
    EXTRACTION_ACCURACY = "EXTRACTION_ACCURACY"
    FIELD_PRECISION = "FIELD_PRECISION"
    FIELD_RECALL = "FIELD_RECALL"
    INTENT_ACCURACY = "INTENT_ACCURACY"
    NEGATION_ACCURACY = "NEGATION_ACCURACY"
    CORRECTION_ACCURACY = "CORRECTION_ACCURACY"
    REFERENCE_RESOLUTION = "REFERENCE_RESOLUTION"
    SCHEMA_COMPLIANCE = "SCHEMA_COMPLIANCE"
    HALLUCINATION = "HALLUCINATION"
    PLAN_COMPLIANCE = "PLAN_COMPLIANCE"
    SAFETY = "SAFETY"
    LANGUAGE_QUALITY = "LANGUAGE_QUALITY"
    CITATION_ACCURACY = "CITATION_ACCURACY"
    LATENCY = "LATENCY"
    COST = "COST"
    FALLBACK_RELIABILITY = "FALLBACK_RELIABILITY"


@dataclass
class EvaluationMetric:
    category: EvaluationCategory = EvaluationCategory.EXTRACTION_ACCURACY
    value: float = 0.0
    count: int = 0
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationCase:
    case_id: str = field(default_factory=lambda: uuid4().hex[:16])
    input_text: str = ""
    expected_intent: str = ""
    expected_candidates: list[dict[str, Any]] = field(default_factory=list)
    forbidden_candidates: list[str] = field(default_factory=list)
    expected_ambiguities: list[str] = field(default_factory=list)
    expected_response_type: str = ""
    expected_safety_status: str = "safe"
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluationResult:
    result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    case_id: str = ""
    actual_intent: str = ""
    actual_candidates: list[dict[str, Any]] = field(default_factory=list)
    actual_response_type: str = ""
    actual_safety_status: str = ""
    is_correct: bool = False
    errors: list[str] = field(default_factory=list)
    metrics: list[EvaluationMetric] = field(default_factory=list)


class AIEvaluator:
    def __init__(self) -> None:
        self._cases: list[EvaluationCase] = []
        self._results: list[EvaluationResult] = []

    def register_case(self, case: EvaluationCase) -> None:
        self._cases.append(case)

    def evaluate(self, extraction_fn: Any) -> list[EvaluationResult]:
        results: list[EvaluationResult] = []
        for case in self._cases:
            result = EvaluationResult(case_id=case.case_id)
            try:
                output = extraction_fn(case.input_text)
                result.actual_intent = getattr(output, "intent", "")
                result.is_correct = result.actual_intent == case.expected_intent
            except Exception as e:
                result.errors.append(str(e))
            self._results.append(result)
            results.append(result)
        return results

    def summary(self) -> dict[str, float]:
        if not self._results:
            return {}
        total = len(self._results)
        correct = sum(1 for r in self._results if r.is_correct)
        return {
            "total_cases": total,
            "correct": correct,
            "accuracy": correct / total if total > 0 else 0.0,
        }
