from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QualificationLevel(str, Enum):
    UNQUALIFIED = "UNQUALIFIED"
    PARTIALLY_QUALIFIED = "PARTIALLY_QUALIFIED"
    QUALIFIED = "QUALIFIED"
    ACTION_READY = "ACTION_READY"


SCORE_THRESHOLDS: dict[QualificationLevel, tuple[float, float]] = {
    QualificationLevel.UNQUALIFIED: (0, 39),
    QualificationLevel.PARTIALLY_QUALIFIED: (40, 69),
    QualificationLevel.QUALIFIED: (70, 89),
    QualificationLevel.ACTION_READY: (90, 100),
}


@dataclass(frozen=True)
class QualificationScore:
    required_fields_score: float = 0.0
    important_fields_score: float = 0.0
    optional_fields_score: float = 0.0
    validation_score: float = 0.0
    confidence_score: float = 0.0
    conflict_penalty: float = 0.0
    risk_penalty: float = 0.0
    confirmation_penalty: float = 0.0
    stage_adjustment: float = 0.0
    action_adjustment: float = 0.0
    final_score: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {k: round(v, 2) for k, v in self.__dict__.items()}
