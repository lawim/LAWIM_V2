from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .criteria import DEFAULT_WEIGHTS, MatchDimension, MatchingCriteria
from .explanation import ExplanationGenerator
from .ranking import ResultRanker
from .results import Match, MatchResult

from ..search.results import SearchResult, SearchResultItem


@dataclass
class MatchingService:
    ranker: ResultRanker = field(default_factory=ResultRanker)
    explanation_generator: ExplanationGenerator = field(default_factory=ExplanationGenerator)
    criteria: MatchingCriteria = field(default_factory=MatchingCriteria)

    def match(
        self,
        search_result: SearchResult,
        project_criteria: dict[str, Any] | None = None,
    ) -> MatchResult:
        if search_result.is_empty:
            return MatchResult(total_evaluated=0)

        request_criteria = self._build_criteria_dict(search_result, project_criteria)

        raw_items = [item.raw_data for item in search_result.items if item.raw_data]
        if not raw_items:
            raw_items = [self._item_to_dict(item) for item in search_result.items]

        matches = self.ranker.rank(
            items=raw_items,
            criteria=self.criteria,
            request_criteria=request_criteria,
        )

        stats = self.ranker.compute_stats(matches)

        criteria_used = list(self.criteria.dimensions.keys())

        return MatchResult(
            matches=matches,
            total_evaluated=len(raw_items),
            min_score=stats["min_score"],
            max_score=stats["max_score"],
            average_score=stats["average_score"],
            criteria_used=[d.value for d in criteria_used],
        )

    def match_single(
        self,
        item: SearchResultItem,
        project_criteria: dict[str, Any] | None = None,
    ) -> Match | None:
        request_criteria = project_criteria or {}
        raw = item.raw_data or self._item_to_dict(item)

        matches = self.ranker.rank(
            items=[raw],
            criteria=self.criteria,
            request_criteria=request_criteria,
        )
        return matches[0] if matches else None

    def get_explanation(self, match: Match, detailed: bool = False) -> str:
        if detailed:
            return self.explanation_generator.generate_detailed(match)
        return self.explanation_generator.generate(match)

    def _build_criteria_dict(
        self,
        search_result: SearchResult,
        project_criteria: dict[str, Any] | None,
    ) -> dict[str, Any]:
        criteria: dict[str, Any] = dict(project_criteria or {})

        request = search_result.request
        if request:
            if request.city and "city" not in criteria:
                criteria["city"] = request.city
            if request.budget_min is not None and "budget_min" not in criteria:
                criteria["budget_min"] = request.budget_min
            if request.budget_max is not None and "budget_max" not in criteria:
                criteria["budget_max"] = request.budget_max
            if request.property_type and "property_type" not in criteria:
                criteria["property_type"] = request.property_type
            if request.bedrooms is not None and "bedrooms" not in criteria:
                criteria["bedrooms"] = request.bedrooms
            if request.transaction_type and "transaction_type" not in criteria:
                criteria["transaction_type"] = request.transaction_type
            if request.surface_min is not None and "surface_min" not in criteria:
                criteria["surface_min"] = request.surface_min
            if request.surface_max is not None and "surface_max" not in criteria:
                criteria["surface_max"] = request.surface_max

        return criteria

    @staticmethod
    def _item_to_dict(item: SearchResultItem) -> dict[str, Any]:
        return {
            "id": item.item_id,
            "title": item.title,
            "description": item.description,
            "city": item.city,
            "price": item.price,
            "property_type": item.property_type,
            "bedrooms": item.bedrooms,
            "surface": item.surface,
            "partner_name": item.partner_name,
            "partner_id": item.partner_id,
        }
