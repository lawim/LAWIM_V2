from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .adapters import DataAdapter, LawimRepositoryAdapter, ResultAdapter
from .query import SearchQueryBuilder
from .results import SearchRequest, SearchResult, SearchResultItem


@dataclass
class SearchService:
    adapter: DataAdapter = field(default_factory=LawimRepositoryAdapter)
    query_builder: SearchQueryBuilder = field(default_factory=SearchQueryBuilder)

    def search(self, request: SearchRequest) -> SearchResult:
        start_time = time.time()

        if request.is_empty():
            return SearchResult(
                request=request,
                total_count=0,
                returned_count=0,
                execution_time_ms=0.0,
                error="Empty search request: no criteria provided",
            )

        query = self.query_builder.build(request)
        raw_items = self.adapter.search(query)
        total_count = self.adapter.count(query)

        items = ResultAdapter.to_result_items(raw_items, query.source_type)

        execution_time_ms = (time.time() - start_time) * 1000

        result = SearchResult(
            request=request,
            items=items,
            total_count=total_count,
            returned_count=len(items),
            offset=request.offset,
            execution_time_ms=execution_time_ms,
            source=self.adapter.source_name,
        )

        if request.create_alert and not result.is_empty:
            alert_id = self._create_alert(request)
            result.alert_created = True
            result.alert_id = alert_id

        return result

    def search_by_criteria(self, criteria: dict[str, Any]) -> SearchResult:
        request = SearchRequest(
            criteria=criteria,
            city=criteria.get("city"),
            budget_min=criteria.get("budget_min"),
            budget_max=criteria.get("budget_max"),
            property_type=criteria.get("property_type"),
            bedrooms=criteria.get("bedrooms"),
            transaction_type=criteria.get("transaction_type"),
            surface_min=criteria.get("surface_min"),
            surface_max=criteria.get("surface_max"),
            partner_type=criteria.get("partner_type"),
            project_id=criteria.get("project_id"),
            user_id=criteria.get("user_id"),
            create_alert=criteria.get("create_alert", False),
            max_results=criteria.get("max_results", 20),
            offset=criteria.get("offset", 0),
        )
        return self.search(request)

    def _create_alert(self, request: SearchRequest) -> str:
        import uuid
        alert_id = f"alert_{uuid.uuid4().hex[:12]}"
        return alert_id
