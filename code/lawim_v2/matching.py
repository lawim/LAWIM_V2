from __future__ import annotations

from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt
from typing import Iterable


@dataclass(frozen=True, slots=True)
class MatchWeights:
    status: float = 25.0
    city: float = 20.0
    region: float = 10.0
    budget: float = 20.0
    proximity: float = 20.0
    attributes: float = 10.0
    availability: float = 5.0

    def normalized(self) -> "MatchWeights":
        total = (
            self.status
            + self.city
            + self.region
            + self.budget
            + self.proximity
            + self.attributes
            + self.availability
        )
        if total <= 0:
            return MatchWeights()
        factor = 100.0 / total
        return MatchWeights(
            status=self.status * factor,
            city=self.city * factor,
            region=self.region * factor,
            budget=self.budget * factor,
            proximity=self.proximity * factor,
            attributes=self.attributes * factor,
            availability=self.availability * factor,
        )


DEFAULT_WEIGHTS = MatchWeights().normalized()


@dataclass(frozen=True, slots=True)
class MatchCriteria:
    city: str | None = None
    region: str | None = None
    country: str | None = None
    budget_min: int | None = None
    budget_max: int | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: str | None = None
    bedrooms_min: int | None = None
    availability: str | None = None
    status: str | None = "published"
    limit: int = 10
    min_score: float = 0.0
    weights: MatchWeights = field(default_factory=lambda: DEFAULT_WEIGHTS)


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


def _text_match(left: object, right: str | None) -> bool:
    if not right or left is None:
        return False
    return str(left).lower() == right.lower()


def score_property(property_row: dict[str, object], criteria: MatchCriteria) -> dict[str, object]:
    weights = criteria.weights.normalized()
    breakdown: dict[str, float] = {}
    reasons: list[str] = []
    distance_km: float | None = None

    target_status = criteria.status or "published"
    if str(property_row.get("status", "")).lower() == target_status.lower():
        breakdown["status"] = weights.status
        reasons.append(f"status:{property_row.get('status')}")

    if _text_match(property_row.get("city"), criteria.city):
        breakdown["city"] = weights.city
        reasons.append("city match")
    elif criteria.city:
        breakdown["city"] = 0.0

    if _text_match(property_row.get("region"), criteria.region):
        breakdown["region"] = weights.region
        reasons.append("region match")

    if _text_match(property_row.get("country"), criteria.country):
        breakdown.setdefault("region", 0.0)
        if "region match" not in reasons:
            reasons.append("country match")

    price_min = int(property_row.get("price_min") or 0)
    price_max = int(property_row.get("price_max") or price_min or 0)
    budget_score = 0.0
    target_min = criteria.budget_min or 0
    target_max = criteria.budget_max or 0
    if target_max and price_min and price_min <= target_max:
        budget_score += weights.budget * 0.6
        reasons.append("budget ceiling compatible")
    if target_min and price_max and price_max >= target_min:
        budget_score += weights.budget * 0.4
        reasons.append("budget floor compatible")
    if budget_score:
        breakdown["budget"] = round(budget_score, 2)

    prop_lat = property_row.get("latitude")
    prop_lon = property_row.get("longitude")
    if criteria.latitude is not None and criteria.longitude is not None and prop_lat is not None and prop_lon is not None:
        distance_km = haversine_km(float(criteria.latitude), float(criteria.longitude), float(prop_lat), float(prop_lon))
        closeness = max(0.0, weights.proximity - min(distance_km, weights.proximity))
        breakdown["proximity"] = round(closeness, 2)
        reasons.append(f"{distance_km:.1f}km away")

    attribute_score = 0.0
    if criteria.property_type and _text_match(property_row.get("property_type"), criteria.property_type):
        attribute_score += weights.attributes * 0.5
        reasons.append(f"type:{property_row.get('property_type')}")
    bedrooms = int(property_row.get("bedrooms") or 0)
    if criteria.bedrooms_min is not None and bedrooms >= criteria.bedrooms_min:
        attribute_score += weights.attributes * 0.5
        reasons.append(f"bedrooms>={criteria.bedrooms_min}")
    if attribute_score:
        breakdown["attributes"] = round(attribute_score, 2)

    if criteria.availability and _text_match(property_row.get("availability"), criteria.availability):
        breakdown["availability"] = weights.availability
        reasons.append(f"availability:{property_row.get('availability')}")
    elif str(property_row.get("availability", "available")).lower() == "available":
        breakdown["availability"] = weights.availability * 0.5
        reasons.append("available")

    total = round(sum(breakdown.values()), 1)
    grade = "excellent" if total >= 70 else "good" if total >= 40 else "fair" if total >= 20 else "weak"
    top_factors = sorted(breakdown.items(), key=lambda item: item[1], reverse=True)
    summary_parts = [f"{name} +{value}" for name, value in top_factors[:3] if value > 0]
    summary = "; ".join(summary_parts) if summary_parts else "No strong match signals"
    return {
        "property": property_row,
        "score": total,
        "score_percent": total,
        "grade": grade,
        "summary": summary,
        "eligible": total >= criteria.min_score,
        "breakdown": breakdown,
        "reasons": reasons,
        "distance_km": round(distance_km, 2) if distance_km is not None else None,
        "weights": {
            "status": weights.status,
            "city": weights.city,
            "region": weights.region,
            "budget": weights.budget,
            "proximity": weights.proximity,
            "attributes": weights.attributes,
            "availability": weights.availability,
        },
    }


def rank_properties(properties: Iterable[dict[str, object]], criteria: MatchCriteria) -> list[dict[str, object]]:
    ranked = [score_property(property_row, criteria) for property_row in properties]
    ranked = [item for item in ranked if float(item["score"]) >= criteria.min_score]
    ranked.sort(key=lambda item: (item["score"], item["property"].get("id", 0)), reverse=True)
    return ranked[: max(criteria.limit, 1)]
