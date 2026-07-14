from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MatchExplanation:
    dimension: str = ""
    score: float = 0.0
    weight: float = 1.0
    details: str = ""
    is_match: bool = True

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "score": self.score,
            "weight": self.weight,
            "weighted_score": self.weighted_score,
            "details": self.details,
            "is_match": self.is_match,
        }


@dataclass
class Match:
    item_id: str = ""
    title: str = ""
    global_score: float = 0.0
    explanations: list[MatchExplanation] = field(default_factory=list)
    matched_criteria_count: int = 0
    total_criteria_count: int = 0
    raw_item: dict[str, Any] = field(default_factory=dict)

    @property
    def match_percentage(self) -> float:
        if self.total_criteria_count == 0:
            return 0.0
        return (self.matched_criteria_count / self.total_criteria_count) * 100

    @property
    def top_explanations(self) -> list[MatchExplanation]:
        return sorted(self.explanations, key=lambda e: e.weighted_score, reverse=True)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "global_score": self.global_score,
            "match_percentage": self.match_percentage,
            "matched_criteria_count": self.matched_criteria_count,
            "total_criteria_count": self.total_criteria_count,
            "explanations": [e.to_dict() for e in self.top_explanations],
        }


@dataclass
class MatchResult:
    matches: list[Match] = field(default_factory=list)
    total_evaluated: int = 0
    min_score: float = 0.0
    max_score: float = 0.0
    average_score: float = 0.0
    criteria_used: list[str] = field(default_factory=list)

    @property
    def has_matches(self) -> bool:
        return len(self.matches) > 0

    @property
    def top_match(self) -> Match | None:
        return self.matches[0] if self.matches else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "matches": [m.to_dict() for m in self.matches],
            "total_evaluated": self.total_evaluated,
            "min_score": self.min_score,
            "max_score": self.max_score,
            "average_score": self.average_score,
            "criteria_used": self.criteria_used,
            "has_matches": self.has_matches,
        }
