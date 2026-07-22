from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .models import MatchingResultItem


@dataclass
class SearchRecord:
    search_id: str = field(default_factory=lambda: uuid4().hex[:16])
    parameters: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ResultRecord:
    result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    search_id: str = ""
    matches: list[MatchingResultItem] = field(default_factory=list)
    status: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class MatchingRepository(ABC):

    @abstractmethod
    def save_search(self, search: SearchRecord) -> None:
        ...

    @abstractmethod
    def get_search(self, search_id: str) -> SearchRecord | None:
        ...

    @abstractmethod
    def save_result(self, result: ResultRecord) -> None:
        ...

    @abstractmethod
    def get_results(self, search_id: str) -> list[ResultRecord]:
        ...

    @abstractmethod
    def list_recent(self, limit: int = 10) -> list[SearchRecord]:
        ...


class InMemoryMatchingRepository(MatchingRepository):

    def __init__(self) -> None:
        self._searches: dict[str, SearchRecord] = {}
        self._results: dict[str, list[ResultRecord]] = {}

    def save_search(self, search: SearchRecord) -> None:
        self._searches[search.search_id] = search

    def get_search(self, search_id: str) -> SearchRecord | None:
        return self._searches.get(search_id)

    def save_result(self, result: ResultRecord) -> None:
        self._results.setdefault(result.search_id, []).append(result)

    def get_results(self, search_id: str) -> list[ResultRecord]:
        return list(self._results.get(search_id, []))

    def list_recent(self, limit: int = 10) -> list[SearchRecord]:
        sorted_searches = sorted(
            self._searches.values(),
            key=lambda s: s.created_at,
            reverse=True,
        )
        return sorted_searches[:limit]
