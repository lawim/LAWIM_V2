from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class SearchRequest:
    criteria: dict[str, Any] = field(default_factory=dict)
    city: str | None = None
    budget_min: float | None = None
    budget_max: float | None = None
    property_type: str | None = None
    bedrooms: int | None = None
    transaction_type: str | None = None
    surface_min: float | None = None
    surface_max: float | None = None
    partner_type: str | None = None
    project_id: int | None = None
    user_id: int | None = None
    create_alert: bool = False
    max_results: int = 20
    offset: int = 0

    def is_empty(self) -> bool:
        return not any([
            self.city, self.budget_min, self.budget_max,
            self.property_type, self.bedrooms, self.transaction_type,
            self.surface_min, self.surface_max, self.partner_type,
        ])

    def to_dict(self) -> dict[str, Any]:
        return {
            "city": self.city,
            "budget_min": self.budget_min,
            "budget_max": self.budget_max,
            "property_type": self.property_type,
            "bedrooms": self.bedrooms,
            "transaction_type": self.transaction_type,
            "surface_min": self.surface_min,
            "surface_max": self.surface_max,
            "partner_type": self.partner_type,
            "project_id": self.project_id,
            "user_id": self.user_id,
            "create_alert": self.create_alert,
            "max_results": self.max_results,
            "offset": self.offset,
        }


@dataclass
class SearchResultItem:
    item_id: str = ""
    source_type: str = ""  # "property", "listing", "partner_profile"
    title: str = ""
    description: str = ""
    city: str | None = None
    price: float | None = None
    property_type: str | None = None
    bedrooms: int | None = None
    surface: float | None = None
    partner_name: str | None = None
    partner_id: int | None = None
    contact_info: dict[str, Any] = field(default_factory=dict)
    raw_data: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "source_type": self.source_type,
            "title": self.title,
            "description": self.description,
            "city": self.city,
            "price": self.price,
            "property_type": self.property_type,
            "bedrooms": self.bedrooms,
            "surface": self.surface,
            "partner_name": self.partner_name,
            "partner_id": self.partner_id,
            "score": self.score,
        }


@dataclass
class SearchResult:
    request: SearchRequest | None = None
    items: list[SearchResultItem] = field(default_factory=list)
    total_count: int = 0
    returned_count: int = 0
    offset: int = 0
    execution_time_ms: float = 0.0
    source: str = "lawim_local"
    alert_created: bool = False
    alert_id: str | None = None
    error: str | None = None

    @property
    def has_results(self) -> bool:
        return self.total_count > 0

    @property
    def is_empty(self) -> bool:
        return self.total_count == 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "total_count": self.total_count,
            "returned_count": self.returned_count,
            "offset": self.offset,
            "has_results": self.has_results,
            "items": [item.to_dict() for item in self.items],
            "execution_time_ms": self.execution_time_ms,
            "source": self.source,
            "alert_created": self.alert_created,
            "error": self.error,
        }
