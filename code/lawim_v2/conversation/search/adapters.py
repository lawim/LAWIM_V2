from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from .filters import FilterComposer
from .query import SearchQuery
from .results import SearchRequest, SearchResult, SearchResultItem


class DataAdapter(ABC):
    @abstractmethod
    def search(self, query: SearchQuery) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def count(self, query: SearchQuery) -> int:
        ...

    @property
    @abstractmethod
    def source_name(self) -> str:
        ...


@dataclass
class LawimRepositoryAdapter(DataAdapter):
    repository: Any = None
    _cache: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    @property
    def source_name(self) -> str:
        return "lawim_local"

    def _fetch_raw_data(self, source_type: str) -> list[dict[str, Any]]:
        if source_type in self._cache:
            return self._cache[source_type]
        if self.repository is not None:
            raw = self.repository.get_all(source_type=source_type)
        else:
            raw = []
        self._cache[source_type] = raw
        return raw

    def search(self, query: SearchQuery) -> list[dict[str, Any]]:
        raw = self._fetch_raw_data(query.source_type)
        filtered = query.filters.apply_all(raw)
        start = query.offset
        end = start + query.max_results
        return filtered[start:end]

    def count(self, query: SearchQuery) -> int:
        raw = self._fetch_raw_data(query.source_type)
        return len(query.filters.apply_all(raw))

    def invalidate_cache(self, source_type: str | None = None) -> None:
        if source_type:
            self._cache.pop(source_type, None)
        else:
            self._cache.clear()


class ResultAdapter:
    @staticmethod
    def to_result_item(raw: dict[str, Any], source_type: str) -> SearchResultItem:
        return SearchResultItem(
            item_id=str(raw.get("id", "")),
            source_type=source_type,
            title=raw.get("title", raw.get("name", "")),
            description=raw.get("description", ""),
            city=raw.get("city"),
            price=raw.get("price"),
            property_type=raw.get("property_type"),
            bedrooms=raw.get("bedrooms"),
            surface=raw.get("surface"),
            partner_name=raw.get("partner_name"),
            partner_id=raw.get("partner_id"),
            contact_info=raw.get("contact_info", {}),
            raw_data=raw,
        )

    @staticmethod
    def to_result_items(
        raw_list: list[dict[str, Any]], source_type: str
    ) -> list[SearchResultItem]:
        return [
            ResultAdapter.to_result_item(raw, source_type) for raw in raw_list
        ]


@dataclass
class CompositeAdapter(DataAdapter):
    adapters: list[DataAdapter] = field(default_factory=list)

    @property
    def source_name(self) -> str:
        return "composite"

    def add(self, adapter: DataAdapter) -> CompositeAdapter:
        self.adapters.append(adapter)
        return self

    def search(self, query: SearchQuery) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for adapter in self.adapters:
            results.extend(adapter.search(query))
        return results

    def count(self, query: SearchQuery) -> int:
        total = 0
        for adapter in self.adapters:
            total += adapter.count(query)
        return total
