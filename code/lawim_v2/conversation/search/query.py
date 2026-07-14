from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .filters import (
    BedroomsFilter,
    BudgetRangeFilter,
    FilterComposer,
    LocationFilter,
    PartnerTypeFilter,
    PropertyTypeFilter,
    SurfaceFilter,
    TransactionTypeFilter,
)
from .results import SearchRequest


@dataclass
class SearchQuery:
    source_type: str = "property"
    filters: FilterComposer = field(default_factory=FilterComposer)
    raw_criteria: dict[str, Any] = field(default_factory=dict)
    max_results: int = 20
    offset: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_type": self.source_type,
            "filters": self.filters.to_query_params(),
            "max_results": self.max_results,
            "offset": self.offset,
        }


class SearchQueryBuilder:
    def build(self, request: SearchRequest) -> SearchQuery:
        composer = FilterComposer()

        if request.city or request.criteria.get("district"):
            composer.add(
                LocationFilter(
                    city=request.city or request.criteria.get("city"),
                    district=request.criteria.get("district"),
                )
            )

        if request.budget_min is not None or request.budget_max is not None:
            composer.add(
                BudgetRangeFilter(
                    min_price=request.budget_min,
                    max_price=request.budget_max,
                )
            )

        if request.property_type:
            composer.add(PropertyTypeFilter(property_type=request.property_type))

        if request.bedrooms is not None:
            composer.add(BedroomsFilter(exact=request.bedrooms))

        if request.surface_min is not None or request.surface_max is not None:
            composer.add(
                SurfaceFilter(
                    min_surface=request.surface_min,
                    max_surface=request.surface_max,
                )
            )

        if request.transaction_type:
            composer.add(
                TransactionTypeFilter(transaction_type=request.transaction_type)
            )

        if request.partner_type:
            composer.add(PartnerTypeFilter(partner_type=request.partner_type))

        source_type = self._detect_source_type(request)

        return SearchQuery(
            source_type=source_type,
            filters=composer,
            raw_criteria=request.criteria,
            max_results=request.max_results,
            offset=request.offset,
        )

    def _detect_source_type(self, request: SearchRequest) -> str:
        if request.partner_type:
            return "partner_profile"
        if request.property_type or request.transaction_type:
            return "property"
        if request.criteria.get("service_type"):
            return "service"
        return "property"
