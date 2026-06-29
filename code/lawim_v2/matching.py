from __future__ import annotations

from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt
from typing import Iterable


@dataclass(frozen=True, slots=True)
class MatchCriteria:
    city: str | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    limit: int = 10


def haversine_km(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    radius_km = 6371.0
    lat1 = radians(latitude_1)
    lon1 = radians(longitude_1)
    lat2 = radians(latitude_2)
    lon2 = radians(longitude_2)
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 2 * radius_km * asin(sqrt(a))


def score_property(property_row: dict[str, object], criteria: MatchCriteria) -> dict[str, object]:
    score = 0.0
    reasons: list[str] = []

    if property_row.get("status") == "published":
        score += 25
        reasons.append("published")

    if criteria.city and property_row.get("city") and str(property_row["city"]).lower() == criteria.city.lower():
        score += 25
        reasons.append("city match")

    price_min = int(property_row.get("price_min") or 0)
    price_max = int(property_row.get("price_max") or price_min or 0)
    target_min = criteria.budget_min or 0
    target_max = criteria.budget_max or 0
    if target_max and price_min and price_min <= target_max:
        score += 15
        reasons.append("budget compatible")
    if target_min and price_max and price_max >= target_min:
        score += 10
        reasons.append("budget floor compatible")

    prop_lat = property_row.get("latitude")
    prop_lon = property_row.get("longitude")
    if (
        criteria.latitude is not None
        and criteria.longitude is not None
        and prop_lat is not None
        and prop_lon is not None
    ):
        distance = haversine_km(float(criteria.latitude), float(criteria.longitude), float(prop_lat), float(prop_lon))
        closeness = max(0.0, 20.0 - min(distance, 20.0))
        score += closeness
        reasons.append(f"{distance:.1f}km away")

    if property_row.get("property_type"):
        score += 5
        reasons.append(str(property_row["property_type"]))

    return {
        "property": property_row,
        "score": round(score, 1),
        "reasons": reasons,
    }


def rank_properties(properties: Iterable[dict[str, object]], criteria: MatchCriteria) -> list[dict[str, object]]:
    ranked = [score_property(property_row, criteria) for property_row in properties]
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[: max(criteria.limit, 1)]
