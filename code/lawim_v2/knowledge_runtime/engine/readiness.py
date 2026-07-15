from __future__ import annotations

from typing import Any

from ..models.readiness import ReadinessLevel
from ..registry.readiness_registry import ReadinessRegistry

_MATCH_RESULT_EXACT = "exact_match"
_MATCH_RESULT_NORMALIZED = "normalized_match"
_MATCH_RESULT_PARTIAL = "authorized_partial_match"
_MATCH_RESULT_AMBIGUITY = "ambiguity"
_MATCH_RESULT_GENERIC = "generic_family_match"
_MATCH_RESULT_NOT_FOUND = "not_found"


class ReadinessEvaluator:
    def __init__(self, registry: ReadinessRegistry) -> None:
        self._registry = registry

    def evaluate(
        self,
        known_fields: dict[str, Any],
        *,
        family: str | None = None,
    ) -> dict[str, Any]:
        all_levels = self._registry.all()
        current_level: ReadinessLevel | None = None
        current_score = 0.0
        total_levels = len(all_levels)
        missed_levels: list[str] = []
        missing_for_next: list[str] = []

        for i, level_def in enumerate(all_levels):
            req = set(level_def.required_fields)
            known = set(known_fields.keys())
            present = req & known
            ratio = len(present) / len(req) if req else 1.0

            if ratio >= 1.0:
                current_level = level_def.level
                current_score = (i + 1) / total_levels * 100.0
            else:
                if current_level is None and i == 0:
                    missed_levels.append(level_def.level.value)
                if current_level is not None and i == all_levels.index(
                    next((ld for ld in all_levels if ld.level == current_level), all_levels[-1])
                ) + 1:
                    missing_for_next = list(req - known)
                break
        else:
            current_level = all_levels[-1].level if all_levels else None
            current_score = 100.0

        next_level = None
        if current_level:
            current_idx = next(
                (j for j, ld in enumerate(all_levels) if ld.level == current_level),
                -1,
            )
            if current_idx < total_levels - 1:
                next_level = all_levels[current_idx + 1].level

        return {
            "current_level": current_level.value if current_level else None,
            "current_score": round(current_score, 1),
            "total_levels": total_levels,
            "next_level": next_level.value if next_level else None,
            "missing_fields_for_next": missing_for_next,
            "missed_levels": missed_levels,
        }

    def is_level_attained(self, level: ReadinessLevel, known_fields: dict[str, Any]) -> bool:
        level_def = self._registry.get(level)
        if level_def is None:
            return False
        required = set(level_def.required_fields)
        known = set(known_fields.keys())
        return required.issubset(known)

    def minimum_search_ready(self, known_fields: dict[str, Any]) -> bool:
        return self.is_level_attained(ReadinessLevel.MINIMUM_SEARCH_READY, known_fields)

    def readiness_summary(self, known_fields: dict[str, Any]) -> dict[str, Any]:
        result = self.evaluate(known_fields)
        return {
            "level": result["current_level"],
            "score": result["current_score"],
            "search_ready": self.minimum_search_ready(known_fields),
            "next_milestone": result["next_level"],
            "gaps": result["missing_fields_for_next"],
        }
