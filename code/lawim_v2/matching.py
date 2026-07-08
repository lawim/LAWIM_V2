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
    target_type: str = "property"
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
    need: str | None = None
    need_type: str | None = None
    partner_type: str | None = None
    project_type: str | None = None
    specialty: str | None = None
    language: str | None = None
    rating_min: float | None = None
    deadline_days: int | None = None
    subject_type: str | None = None
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


def _normalized_text(value: object) -> str:
    return str(value or "").strip().lower()


def _contains_any(haystack: object, needles: Iterable[str]) -> bool:
    text = _normalized_text(haystack)
    return any(needle and needle in text for needle in needles)


def _grade_from_score(score: float) -> str:
    if score >= 70:
        return "excellent"
    if score >= 40:
        return "good"
    if score >= 20:
        return "fair"
    return "weak"


def _summarize_breakdown(breakdown: dict[str, float]) -> str:
    top_factors = sorted(breakdown.items(), key=lambda item: item[1], reverse=True)
    summary_parts = [f"{name} +{value}" for name, value in top_factors[:3] if value > 0]
    return "; ".join(summary_parts) if summary_parts else "No strong match signals"


def _score_property(property_row: dict[str, object], criteria: MatchCriteria, weights: MatchWeights) -> dict[str, object]:
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
    return {
        "property": property_row,
        "score": total,
        "score_percent": total,
        "grade": _grade_from_score(total),
        "summary": _summarize_breakdown(breakdown),
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


def _partner_metadata(partner_row: dict[str, object]) -> dict[str, object]:
    metadata = partner_row.get("metadata")
    return metadata if isinstance(metadata, dict) else {}


def _partner_languages(partner_row: dict[str, object]) -> list[str]:
    metadata = _partner_metadata(partner_row)
    languages = metadata.get("languages") or metadata.get("language") or []
    if isinstance(languages, str):
        languages = [languages]
    if not isinstance(languages, list):
        return []
    return [_normalized_text(language) for language in languages if _normalized_text(language)]


def _partner_price_bounds(partner_row: dict[str, object]) -> tuple[int | None, int | None]:
    metadata = _partner_metadata(partner_row)
    price_min = metadata.get("budget_min") or metadata.get("price_min") or metadata.get("min_price")
    price_max = metadata.get("budget_max") or metadata.get("price_max") or metadata.get("max_price")
    try:
        normalized_min = int(price_min) if price_min is not None else None
    except (TypeError, ValueError):
        normalized_min = None
    try:
        normalized_max = int(price_max) if price_max is not None else None
    except (TypeError, ValueError):
        normalized_max = None
    return normalized_min, normalized_max


def _partner_zone_match(partner_row: dict[str, object], criteria: MatchCriteria) -> tuple[float, list[str]]:
    zones = partner_row.get("zones") or []
    reasons: list[str] = []
    score = 0.0
    if not isinstance(zones, list):
        return score, reasons
    for zone in zones:
        if not isinstance(zone, dict):
            continue
        if criteria.city and _text_match(zone.get("city"), criteria.city):
            return 20.0, [f"city:{zone.get('city')}"]
        if criteria.region and _text_match(zone.get("region"), criteria.region):
            score = max(score, 12.0)
            reasons = [f"region:{zone.get('region')}"]
        if criteria.country and _text_match(zone.get("country"), criteria.country):
            score = max(score, 8.0)
            if not reasons:
                reasons = [f"country:{zone.get('country')}"]
    return score, reasons


def _partner_need_keywords(criteria: MatchCriteria) -> list[str]:
    keywords = [
        criteria.partner_type,
        criteria.need,
        criteria.need_type,
        criteria.specialty,
        criteria.project_type,
    ]
    return [_normalized_text(keyword) for keyword in keywords if _normalized_text(keyword)]


def _score_partner(partner_row: dict[str, object], criteria: MatchCriteria) -> dict[str, object]:
    breakdown: dict[str, float] = {}
    reasons: list[str] = []
    metadata = _partner_metadata(partner_row)

    target_status = criteria.status or "active"
    if str(partner_row.get("status", "")).lower() == target_status.lower():
        breakdown["status"] = 15.0
        reasons.append(f"status:{partner_row.get('status')}")

    location_score, location_reasons = _partner_zone_match(partner_row, criteria)
    if location_score:
        breakdown["location"] = location_score
        reasons.extend(location_reasons)

    need_score = 0.0
    need_terms = _partner_need_keywords(criteria)
    searchable_values = [
        partner_row.get("partner_type"),
        partner_row.get("display_name"),
        partner_row.get("description"),
        " ".join(str(item) for item in partner_row.get("specialties") or []),
        " ".join(str(item) for item in metadata.get("project_types") or []),
        " ".join(str(item) for item in metadata.get("service_modes") or []),
        " ".join(str(item) for item in metadata.get("tags") or []),
    ]
    if criteria.partner_type and _text_match(partner_row.get("partner_type"), criteria.partner_type):
        need_score = 25.0
        reasons.append(f"partner_type:{partner_row.get('partner_type')}")
    elif need_terms and any(_contains_any(value, need_terms) for value in searchable_values):
        need_score = 20.0
        if criteria.need:
            reasons.append(f"need:{criteria.need}")
        if criteria.project_type:
            reasons.append(f"project_type:{criteria.project_type}")
        if criteria.specialty:
            reasons.append(f"specialty:{criteria.specialty}")
    elif criteria.project_type and _contains_any(metadata.get("project_types") or [], [criteria.project_type.lower()]):
        need_score = 18.0
        reasons.append(f"project_type:{criteria.project_type}")
    if need_score:
        breakdown["need"] = need_score

    languages = _partner_languages(partner_row)
    if criteria.language and languages:
        if _normalized_text(criteria.language) in languages:
            breakdown["language"] = 10.0
            reasons.append(f"language:{criteria.language}")
    elif languages:
        breakdown["language"] = 4.0
        reasons.append(f"language:{languages[0]}")

    rating_score = 0.0
    rating_values: list[float] = []
    for key in ("trust_score", "quality_score", "satisfaction_score", "reliability_score"):
        raw = partner_row.get(key)
        try:
            rating_values.append(float(raw))
        except (TypeError, ValueError):
            continue
    if rating_values:
        average_rating = sum(rating_values) / len(rating_values)
        if criteria.rating_min is None:
            rating_score = min(10.0, max(0.0, (average_rating - 50.0) / 5.0))
        elif average_rating >= criteria.rating_min:
            rating_score = 10.0
        if rating_score:
            reasons.append(f"rating:{average_rating:.0f}")
    if rating_score:
        breakdown["rating"] = rating_score

    budget_score = 0.0
    budget_min = criteria.budget_min
    budget_max = criteria.budget_max
    price_min, price_max = _partner_price_bounds(partner_row)
    if budget_max is not None and price_min is not None and price_min <= budget_max:
        budget_score += 6.0
        reasons.append("budget ceiling compatible")
    if budget_min is not None and price_max is not None and price_max >= budget_min:
        budget_score += 4.0
        reasons.append("budget floor compatible")
    if budget_score:
        breakdown["budget"] = budget_score

    availability = _normalized_text(partner_row.get("availability_status"))
    if availability == "available":
        breakdown["availability"] = 5.0
        reasons.append("available")
    elif availability:
        breakdown["availability"] = 1.0

    deadline_score = 0.0
    if criteria.deadline_days is not None:
        completion_days = metadata.get("completion_days")
        response_hours = metadata.get("response_hours")
        try:
            completion_days_value = float(completion_days) if completion_days is not None else None
        except (TypeError, ValueError):
            completion_days_value = None
        try:
            response_hours_value = float(response_hours) if response_hours is not None else None
        except (TypeError, ValueError):
            response_hours_value = None
        if completion_days_value is not None and completion_days_value <= criteria.deadline_days:
            deadline_score = 5.0
            reasons.append(f"deadline:{completion_days_value:g}d")
        elif response_hours_value is not None and response_hours_value <= criteria.deadline_days * 24:
            deadline_score = 3.0
            reasons.append(f"response:{response_hours_value:g}h")
    if deadline_score:
        breakdown["deadline"] = deadline_score

    compatibility_score = 0.0
    if criteria.subject_type and _contains_any(partner_row.get("partner_type"), [criteria.subject_type.lower()]):
        compatibility_score += 5.0
    if criteria.project_type and _contains_any(metadata.get("project_types") or [], [criteria.project_type.lower()]):
        compatibility_score += 5.0
    if compatibility_score:
        reasons.append("project compatibility")
    if compatibility_score:
        breakdown["compatibility"] = compatibility_score

    total = round(sum(breakdown.values()), 1)
    return {
        "partner": partner_row,
        "score": total,
        "score_percent": total,
        "grade": _grade_from_score(total),
        "summary": _summarize_breakdown(breakdown),
        "eligible": total >= criteria.min_score,
        "breakdown": breakdown,
        "reasons": reasons,
        "distance_km": None,
        "weights": {
            "status": 15.0,
            "location": 20.0,
            "need": 25.0,
            "language": 10.0,
            "rating": 10.0,
            "budget": 10.0,
            "availability": 5.0,
            "deadline": 5.0,
        },
    }


def score_partner(partner_row: dict[str, object], criteria: MatchCriteria) -> dict[str, object]:
    return _score_partner(partner_row, criteria)


def score_property(property_row: dict[str, object], criteria: MatchCriteria) -> dict[str, object]:
    return _score_property(property_row, criteria, criteria.weights.normalized())


def rank_properties(properties: Iterable[dict[str, object]], criteria: MatchCriteria) -> list[dict[str, object]]:
    weights = criteria.weights.normalized()
    ranked: list[dict[str, object]] = []
    append = ranked.append
    for property_row in properties:
        scored = _score_property(property_row, criteria, weights)
        if float(scored["score"]) >= criteria.min_score:
            append(scored)
    ranked.sort(key=lambda item: (item["score"], item["property"].get("id", 0)), reverse=True)
    return ranked[: max(criteria.limit, 1)]


def rank_partners(partners: Iterable[dict[str, object]], criteria: MatchCriteria) -> list[dict[str, object]]:
    ranked: list[dict[str, object]] = []
    append = ranked.append
    for partner_row in partners:
        if criteria.status and str(partner_row.get("status", "")).lower() != criteria.status.lower():
            continue
        scored = _score_partner(partner_row, criteria)
        if float(scored["score"]) >= criteria.min_score:
            append(scored)
    ranked.sort(
        key=lambda item: (
            item["score"],
            float((item["partner"] or {}).get("trust_score") or 0) if isinstance(item.get("partner"), dict) else 0.0,
            item["partner"].get("id", 0) if isinstance(item.get("partner"), dict) else 0,
        ),
        reverse=True,
    )
    return ranked[: max(criteria.limit, 1)]


def rank_matches(
    items: Iterable[dict[str, object]],
    criteria: MatchCriteria,
) -> list[dict[str, object]]:
    target_type = _normalized_text(criteria.target_type) or "property"
    if target_type == "partner":
        return rank_partners(items, criteria)
    return rank_properties(items, criteria)
