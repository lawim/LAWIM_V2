from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QualificationLevel(str, Enum):
    INITIAL = "INITIAL"
    INCOMPLETE = "INCOMPLETE"
    PARTIAL = "PARTIAL"
    QUALIFIED = "QUALIFIED"
    READY_FOR_DECISION = "READY_FOR_DECISION"


REQUIRED_FIELDS_BY_INTENT: dict[str, list[str]] = {
    "property_search": ["transaction_type", "property_type", "city", "budget_max"],
    "visit_request": ["property_type", "city", "bedrooms"],
    "owner_registration": ["property_type", "city", "budget_max"],
}


@dataclass
class QualificationResult:
    level: QualificationLevel = QualificationLevel.INITIAL
    missing_fields: list[str] = field(default_factory=list)
    score: float = 0.0


class QualificationEngine:

    def evaluate(
        self,
        intent: str,
        entities: dict[str, Any],
        context: dict[str, Any] | None = None,
    ) -> QualificationResult:
        required = REQUIRED_FIELDS_BY_INTENT.get(intent, [])
        missing = [f for f in required if f not in entities]
        if not required:
            return QualificationResult(level=QualificationLevel.QUALIFIED, score=100.0)
        if not entities:
            return QualificationResult(level=QualificationLevel.INCOMPLETE, missing_fields=required, score=0.0)
        if missing:
            score = max(0.0, (len(required) - len(missing)) / len(required) * 100)
            level = QualificationLevel.PARTIAL if score >= 50 else QualificationLevel.INCOMPLETE
            return QualificationResult(level=level, missing_fields=missing, score=round(score, 1))
        return QualificationResult(level=QualificationLevel.READY_FOR_DECISION, score=100.0)
