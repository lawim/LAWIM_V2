from __future__ import annotations

import json
import re
from typing import Any

from .errors import ValidationError
from .geo_domain import build_geo_dto, normalize_country, normalize_city, validate_coordinates


PROPERTY_STATUSES = frozenset({"draft", "open", "closed", "published", "archived"})
AVAILABILITY_STATUSES = frozenset({"available", "reserved", "sold", "rented", "unavailable"})
SUPPORTED_CURRENCIES = frozenset({"XAF", "EUR", "USD", "GBP", "XOF"})

STATUS_TRANSITIONS: dict[str, frozenset[str]] = {
    "draft": frozenset({"draft", "open", "closed", "published", "archived"}),
    "open": frozenset({"open", "published", "closed", "archived"}),
    "published": frozenset({"published", "closed", "archived"}),
    "closed": frozenset({"closed", "archived"}),
    "archived": frozenset({"archived"}),
}


def normalize_currency(currency: str) -> str:
    normalized = currency.strip().upper()
    if normalized not in SUPPORTED_CURRENCIES:
        raise ValidationError(f"unsupported currency: {normalized}")
    return normalized


def normalize_property_type(property_type: str) -> str:
    normalized = property_type.strip().lower()
    if not normalized:
        raise ValidationError("property_type is required")
    return normalized


def normalize_availability(availability: str) -> str:
    normalized = availability.strip().lower()
    if normalized not in AVAILABILITY_STATUSES:
        raise ValidationError(f"unsupported availability: {normalized}")
    return normalized


def validate_price_range(price_min: int | None, price_max: int | None) -> None:
    if price_min is not None and price_min < 0:
        raise ValidationError("price_min must be non-negative")
    if price_max is not None and price_max < 0:
        raise ValidationError("price_max must be non-negative")
    if price_min is not None and price_max is not None and price_min > price_max:
        raise ValidationError("price_min cannot exceed price_max")


def validate_status_transition(current_status: str, next_status: str) -> None:
    current = current_status.lower()
    nxt = next_status.lower()
    allowed = STATUS_TRANSITIONS.get(current, frozenset({nxt}))
    if nxt not in allowed:
        raise ValidationError(f"invalid property status transition: {current} -> {nxt}")


def normalize_metadata(metadata: dict[str, Any] | str | None) -> str:
    if metadata is None:
        return "{}"
    if isinstance(metadata, str):
        try:
            parsed = json.loads(metadata)
        except json.JSONDecodeError as exc:
            raise ValidationError("metadata must be valid JSON") from exc
        if not isinstance(parsed, dict):
            raise ValidationError("metadata must be a JSON object")
        return json.dumps(parsed, ensure_ascii=False, sort_keys=True)
    if not isinstance(metadata, dict):
        raise ValidationError("metadata must be a JSON object")
    return json.dumps(metadata, ensure_ascii=False, sort_keys=True)


def metadata_dict(metadata_json: str | None) -> dict[str, object]:
    if not metadata_json:
        return {}
    try:
        parsed = json.loads(metadata_json)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def generate_listing_code(title: str, *, property_id: int | None = None) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:24] or "listing"
    suffix = f"-{property_id}" if property_id is not None else ""
    return f"lawim-{slug}{suffix}"


def build_property_input(
    *,
    title: str,
    summary: str,
    city: str,
    country: str,
    latitude: float | None = None,
    longitude: float | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    currency: str = "XAF",
    status: str = "draft",
    property_type: str = "apartment",
    availability: str = "available",
    address_line: str | None = None,
    region: str | None = None,
    postal_code: str | None = None,
    metadata: dict[str, Any] | str | None = None,
    bedrooms: int = 0,
    bathrooms: int = 0,
    area_sqm: float = 0,
) -> dict[str, object]:
    title = title.strip()
    summary = summary.strip()
    if not title:
        raise ValidationError("title is required")
    if not summary:
        raise ValidationError("summary is required")
    normalized_status = status.strip().lower()
    if normalized_status not in PROPERTY_STATUSES:
        raise ValidationError(f"unsupported property status: {normalized_status}")
    validate_price_range(price_min, price_max)
    validate_coordinates(latitude, longitude)
    geo = build_geo_dto(
        city=city,
        country=country,
        latitude=latitude,
        longitude=longitude,
        region=region,
        address_line=address_line,
        postal_code=postal_code,
    )
    if bedrooms < 0:
        raise ValidationError("bedrooms must be non-negative")
    if bathrooms < 0:
        raise ValidationError("bathrooms must be non-negative")
    if area_sqm < 0:
        raise ValidationError("area_sqm must be non-negative")
    return {
        "title": title,
        "summary": summary,
        "city": geo["city"],
        "country": geo["country"],
        "region": geo["region"],
        "address_line": geo["address_line"],
        "postal_code": geo["postal_code"],
        "latitude": geo["coordinates"]["latitude"],
        "longitude": geo["coordinates"]["longitude"],
        "search_key": geo["search_key"],
        "price_min": price_min,
        "price_max": price_max,
        "currency": normalize_currency(currency),
        "status": normalized_status,
        "property_type": normalize_property_type(property_type),
        "availability": normalize_availability(availability),
        "metadata_json": normalize_metadata(metadata),
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "area_sqm": area_sqm,
    }


def can_publish(property_row: dict[str, object]) -> bool:
    if property_row.get("deleted_at"):
        return False
    if not property_row.get("title") or not property_row.get("city"):
        return False
    if property_row.get("price_min") is None and property_row.get("price_max") is None:
        return False
    return True
