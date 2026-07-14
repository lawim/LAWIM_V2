from __future__ import annotations

from typing import Any

from .criteria import MatchingCriteria
from .results import Match, MatchExplanation
from .scoring import ScoringEngine


class ResultRanker:
    def __init__(self, scoring_engine: ScoringEngine | None = None):
        self.scoring_engine = scoring_engine or ScoringEngine()

    def rank(
        self,
        items: list[dict[str, Any]],
        criteria: MatchingCriteria,
        request_criteria: dict[str, Any],
        min_global_score: float = 0.0,
    ) -> list[Match]:
        matches: list[Match] = []
        for item in items:
            explanations = self.scoring_engine.evaluate(item, criteria, request_criteria)
            match = self._build_match(item, explanations, criteria)
            if match.global_score >= min_global_score:
                matches.append(match)

        matches.sort(key=lambda m: m.global_score, reverse=True)
        return matches

    def _build_match(
        self,
        item: dict[str, Any],
        explanations: list[MatchExplanation],
        criteria: MatchingCriteria,
    ) -> Match:
        total_weight = sum(criteria.get_weight(dim) for dim in criteria.dimensions)
        if total_weight == 0:
            global_score = 0.0
        else:
            weighted_sum = sum(e.weighted_score for e in explanations)
            global_score = weighted_sum / total_weight

        matched_count = sum(1 for e in explanations if e.is_match)
        total_count = len(explanations)

        return Match(
            item_id=str(item.get("id", "")),
            title=item.get("title", item.get("name", "")),
            global_score=round(global_score, 4),
            explanations=explanations,
            matched_criteria_count=matched_count,
            total_criteria_count=total_count,
            raw_item=item,
        )

    def compute_stats(self, matches: list[Match]) -> dict[str, Any]:
        if not matches:
            return {
                "min_score": 0.0,
                "max_score": 0.0,
                "average_score": 0.0,
                "count": 0,
            }
        scores = [m.global_score for m in matches]
        return {
            "min_score": min(scores),
            "max_score": max(scores),
            "average_score": round(sum(scores) / len(scores), 4),
            "count": len(matches),
        }
