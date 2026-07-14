from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class Filter(ABC):
    @abstractmethod
    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def to_query_param(self) -> dict[str, Any]:
        ...

    @property
    def name(self) -> str:
        return self.__class__.__name__


@dataclass
class BudgetRangeFilter(Filter):
    min_price: float | None = None
    max_price: float | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = list(items)
        if self.min_price is not None:
            result = [i for i in result if (i.get("price") or 0) >= self.min_price]
        if self.max_price is not None:
            result = [i for i in result if (i.get("price") or 0) <= self.max_price]
        return result

    def to_query_param(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.min_price is not None:
            params["price_min"] = self.min_price
        if self.max_price is not None:
            params["price_max"] = self.max_price
        return params


@dataclass
class LocationFilter(Filter):
    city: str | None = None
    district: str | None = None
    radius_km: float | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = list(items)
        if self.city:
            city_lower = self.city.lower().strip()
            result = [
                i for i in result
                if (i.get("city") or "").lower().strip() == city_lower
            ]
        if self.district:
            district_lower = self.district.lower().strip()
            result = [
                i for i in result
                if (i.get("district") or "").lower().strip() == district_lower
            ]
        return result

    def to_query_param(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.city is not None:
            params["city"] = self.city
        if self.district is not None:
            params["district"] = self.district
        return params


@dataclass
class PropertyTypeFilter(Filter):
    property_type: str | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not self.property_type:
            return list(items)
        target = self.property_type.lower().strip()
        return [
            i for i in items
            if (i.get("property_type") or "").lower().strip() == target
        ]

    def to_query_param(self) -> dict[str, Any]:
        return {"property_type": self.property_type} if self.property_type else {}


@dataclass
class BedroomsFilter(Filter):
    min_bedrooms: int | None = None
    max_bedrooms: int | None = None
    exact: int | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = list(items)
        if self.exact is not None:
            return [i for i in result if i.get("bedrooms") == self.exact]
        if self.min_bedrooms is not None:
            result = [i for i in result if (i.get("bedrooms") or 0) >= self.min_bedrooms]
        if self.max_bedrooms is not None:
            result = [i for i in result if (i.get("bedrooms") or 0) <= self.max_bedrooms]
        return result

    def to_query_param(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.exact is not None:
            params["bedrooms"] = self.exact
        else:
            if self.min_bedrooms is not None:
                params["bedrooms_min"] = self.min_bedrooms
            if self.max_bedrooms is not None:
                params["bedrooms_max"] = self.max_bedrooms
        return params


@dataclass
class SurfaceFilter(Filter):
    min_surface: float | None = None
    max_surface: float | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = list(items)
        if self.min_surface is not None:
            result = [i for i in result if (i.get("surface") or 0) >= self.min_surface]
        if self.max_surface is not None:
            result = [i for i in result if (i.get("surface") or 0) <= self.max_surface]
        return result

    def to_query_param(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if self.min_surface is not None:
            params["surface_min"] = self.min_surface
        if self.max_surface is not None:
            params["surface_max"] = self.max_surface
        return params


@dataclass
class TransactionTypeFilter(Filter):
    transaction_type: str | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not self.transaction_type:
            return list(items)
        target = self.transaction_type.lower().strip()
        return [
            i for i in items
            if (i.get("transaction_type") or "").lower().strip() == target
        ]

    def to_query_param(self) -> dict[str, Any]:
        return {"transaction_type": self.transaction_type} if self.transaction_type else {}


@dataclass
class PartnerTypeFilter(Filter):
    partner_type: str | None = None

    def apply(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        if not self.partner_type:
            return list(items)
        target = self.partner_type.lower().strip()
        return [
            i for i in items
            if (i.get("partner_type") or "").lower().strip() == target
        ]

    def to_query_param(self) -> dict[str, Any]:
        return {"partner_type": self.partner_type} if self.partner_type else {}


class FilterComposer:
    def __init__(self, filters: list[Filter] | None = None):
        self.filters: list[Filter] = list(filters) if filters else []

    def add(self, filter_: Filter) -> FilterComposer:
        self.filters.append(filter_)
        return self

    def apply_all(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = list(items)
        for f in self.filters:
            result = f.apply(result)
        return result

    def to_query_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {}
        for f in self.filters:
            params.update(f.to_query_param())
        return params

    @property
    def active_filter_count(self) -> int:
        return len(self.filters)
