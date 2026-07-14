from __future__ import annotations

from enum import Enum
from typing import Any

from .matrices import QualificationMatrix


class ReadinessLevel(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PARTIAL = "PARTIAL"
    MINIMUM_READY = "MINIMUM_READY"
    SEARCH_READY = "SEARCH_READY"
    RELATIONSHIP_READY = "RELATIONSHIP_READY"
    VISIT_READY = "VISIT_READY"


DEFAULT_THRESHOLDS: dict[ReadinessLevel, float] = {
    ReadinessLevel.NOT_STARTED: 0.0,
    ReadinessLevel.PARTIAL: 0.25,
    ReadinessLevel.MINIMUM_READY: 0.5,
    ReadinessLevel.SEARCH_READY: 0.65,
    ReadinessLevel.RELATIONSHIP_READY: 0.8,
    ReadinessLevel.VISIT_READY: 0.95,
}


class ReadinessCalculator:
    def __init__(self, thresholds: dict[ReadinessLevel, float] | None = None):
        self._thresholds = dict(DEFAULT_THRESHOLDS)
        if thresholds:
            self._thresholds.update(thresholds)

    def get_threshold(self, level: ReadinessLevel) -> float:
        return self._thresholds.get(level, 0.0)

    def calculate(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> ReadinessLevel:
        from .matrices import get_readiness_score

        score = get_readiness_score(matrix, known_facts)
        return self.level_for_score(score, matrix)

    def level_for_score(self, score: float, matrix: QualificationMatrix | None = None) -> ReadinessLevel:
        threshold = matrix.readiness_threshold if matrix else DEFAULT_THRESHOLDS[ReadinessLevel.SEARCH_READY]

        if score >= self._thresholds[ReadinessLevel.VISIT_READY]:
            return ReadinessLevel.VISIT_READY
        if score >= self._thresholds[ReadinessLevel.RELATIONSHIP_READY]:
            return ReadinessLevel.RELATIONSHIP_READY
        if score >= max(threshold, self._thresholds[ReadinessLevel.SEARCH_READY]):
            return ReadinessLevel.SEARCH_READY
        if score >= self._thresholds[ReadinessLevel.MINIMUM_READY]:
            return ReadinessLevel.MINIMUM_READY
        if score >= self._thresholds[ReadinessLevel.PARTIAL]:
            return ReadinessLevel.PARTIAL
        return ReadinessLevel.NOT_STARTED

    def is_search_ready(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> bool:
        level = self.calculate(matrix, known_facts)
        return level in (
            ReadinessLevel.SEARCH_READY,
            ReadinessLevel.RELATIONSHIP_READY,
            ReadinessLevel.VISIT_READY,
        )

    def is_relationship_ready(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> bool:
        level = self.calculate(matrix, known_facts)
        return level in (ReadinessLevel.RELATIONSHIP_READY, ReadinessLevel.VISIT_READY)

    def required_fields_known(
        self,
        matrix: QualificationMatrix,
        known_facts: dict[str, Any],
    ) -> bool:
        return all(f in known_facts for f in matrix.required_fields)
