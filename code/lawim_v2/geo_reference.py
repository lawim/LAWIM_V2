from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from .errors import ValidationError


_CATALOG_FILE = Path(__file__).resolve().parent / "data" / "cameroon_locations.json"
_TEXT_FIELDS = (
    "name",
    "city",
    "region",
    "department",
    "aliases",
    "typos",
    "landmarks",
    "informal_references",
    "related_zones",
    "target",
    "common_property_types",
)


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(char for char in normalized if not unicodedata.combining(char))
    return _collapse_whitespace(stripped).lower()


def _text_list(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValidationError("geo reference list fields must be arrays")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise ValidationError("geo reference list fields must contain strings")
        normalized = _collapse_whitespace(item)
        if normalized:
            result.append(normalized)
    return result


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"geo reference field '{field}' must be a string")
    normalized = _collapse_whitespace(value)
    if not normalized:
        raise ValidationError(f"geo reference field '{field}' is required")
    return normalized


def _optional_text(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValidationError("geo reference text fields must be strings")
    normalized = _collapse_whitespace(value)
    return normalized or None


def _optional_float(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValidationError("geo reference coordinates must be numeric")
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("geo reference coordinates must be numeric") from exc


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValidationError("geo reference integers must be numeric")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError("geo reference integers must be numeric") from exc


def _catalog_path() -> Path:
    return _CATALOG_FILE


@lru_cache(maxsize=1)
def load_geo_reference_catalog() -> dict[str, object]:
    try:
        raw = json.loads(_catalog_path().read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValidationError(f"geo reference catalog unavailable: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"geo reference catalog is invalid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError("geo reference catalog must be a JSON object")
    country = _require_text(raw.get("country"), "country")
    cities = raw.get("cities")
    neighborhoods = raw.get("neighborhoods")
    if not isinstance(cities, list):
        raise ValidationError("geo reference catalog must define a cities array")
    if not isinstance(neighborhoods, list):
        raise ValidationError("geo reference catalog must define a neighborhoods array")
    raw["country"] = country
    raw["cities"] = cities
    raw["neighborhoods"] = neighborhoods
    return raw


def _normalize_entry(entry: dict[str, object], *, kind: str, country: str) -> dict[str, object]:
    normalized_kind = _require_text(entry.get("kind", kind), "kind").lower()
    if normalized_kind not in {"city", "neighborhood"}:
        raise ValidationError(f"unsupported geo reference kind: {normalized_kind}")
    name = _require_text(entry.get("name"), "name")
    city = _require_text(entry.get("city", name), "city")
    region = _optional_text(entry.get("region"))
    department = _optional_text(entry.get("department"))
    aliases = _text_list(entry.get("aliases"))
    typos = _text_list(entry.get("typos"))
    landmarks = _text_list(entry.get("landmarks"))
    informal_references = _text_list(entry.get("informal_references"))
    related_zones = _text_list(entry.get("related_zones"))
    target = _text_list(entry.get("target"))
    common_property_types = _text_list(entry.get("common_property_types"))
    sources = _text_list(entry.get("sources"))
    if not sources:
        raise ValidationError("geo reference entries must declare at least one source")
    priority_rank = _optional_int(entry.get("priority_rank"))
    latitude = _optional_float(entry.get("latitude"))
    longitude = _optional_float(entry.get("longitude"))
    confidence = float(entry.get("confidence", 0.0) or 0.0)
    if not 0.0 <= confidence <= 1.0:
        raise ValidationError("geo reference confidence must be between 0 and 1")
    payload: dict[str, object] = {
        "kind": normalized_kind,
        "name": name,
        "city": city,
        "region": region,
        "department": department,
        "country": country,
        "aliases": aliases,
        "typos": typos,
        "landmarks": landmarks,
        "informal_references": informal_references,
        "related_zones": related_zones,
        "target": target,
        "common_property_types": common_property_types,
        "sources": sources,
        "confidence": confidence,
    }
    if priority_rank is not None:
        payload["priority_rank"] = priority_rank
    if latitude is not None:
        payload["latitude"] = latitude
    if longitude is not None:
        payload["longitude"] = longitude
    if normalized_kind == "city" and city != name:
        payload["city"] = name
    return payload


@lru_cache(maxsize=1)
def _normalized_entries() -> tuple[dict[str, object], ...]:
    catalog = load_geo_reference_catalog()
    country = str(catalog["country"])
    entries: list[dict[str, object]] = []
    for item in catalog["cities"]:
        if not isinstance(item, dict):
            raise ValidationError("geo reference city entries must be objects")
        entries.append(_normalize_entry(item, kind="city", country=country))
    for item in catalog["neighborhoods"]:
        if not isinstance(item, dict):
            raise ValidationError("geo reference neighborhood entries must be objects")
        entries.append(_normalize_entry(item, kind="neighborhood", country=country))
    return tuple(entries)


def _entry_text_blob(entry: dict[str, object]) -> str:
    fields: list[str] = []
    for key in _TEXT_FIELDS:
        value = entry.get(key)
        if isinstance(value, str):
            fields.append(value)
        elif isinstance(value, list):
            fields.extend(item for item in value if isinstance(item, str))
    return _fold(" ".join(fields))


def _query_tokens(query: str | None) -> list[str]:
    if query is None:
        return []
    folded = _fold(query)
    if not folded:
        return []
    return [token for token in re.split(r"[\s,;/|]+", folded) if token]


def _score_entry(entry: dict[str, object], tokens: list[str]) -> float:
    if not tokens:
        score = float(entry.get("confidence", 0.0)) * 100.0
        if entry.get("kind") == "city":
            priority_rank = int(entry.get("priority_rank") or 999)
            score += max(0.0, 120.0 - (priority_rank * 8.0))
        else:
            score += 20.0
        return score

    name = _fold(str(entry.get("name") or ""))
    city = _fold(str(entry.get("city") or ""))
    region = _fold(str(entry.get("region") or ""))
    department = _fold(str(entry.get("department") or ""))
    aliases = [_fold(item) for item in entry.get("aliases", []) if isinstance(item, str)]
    typos = [_fold(item) for item in entry.get("typos", []) if isinstance(item, str)]
    landmarks = [_fold(item) for item in entry.get("landmarks", []) if isinstance(item, str)]
    informal = [_fold(item) for item in entry.get("informal_references", []) if isinstance(item, str)]
    related = [_fold(item) for item in entry.get("related_zones", []) if isinstance(item, str)]
    target = [_fold(item) for item in entry.get("target", []) if isinstance(item, str)]
    common = [_fold(item) for item in entry.get("common_property_types", []) if isinstance(item, str)]
    blob = _entry_text_blob(entry)

    score = 0.0
    for token in tokens:
        token_score = 0.0
        if token == name:
            token_score += 240.0
        if token == city:
            token_score += 220.0 if entry.get("kind") == "city" else 170.0
        if token == region and region:
            token_score += 100.0
        if token == department and department:
            token_score += 80.0
        if token in aliases:
            token_score += 190.0
        if token in typos:
            token_score += 150.0
        if token in landmarks:
            token_score += 70.0
        if token in informal:
            token_score += 85.0
        if token in related:
            token_score += 60.0
        if token in target:
            token_score += 25.0
        if token in common:
            token_score += 25.0
        if token in blob:
            token_score += 40.0
        if entry.get("kind") == "city":
            priority_rank = int(entry.get("priority_rank") or 999)
            token_score += max(0.0, 60.0 - (priority_rank * 4.0))
        score += token_score
    score += float(entry.get("confidence", 0.0)) * 10.0
    return score


def _clone_entry(entry: dict[str, object], *, match_score: float | None = None) -> dict[str, object]:
    cloned = dict(entry)
    if match_score is not None:
        cloned["match_score"] = round(match_score, 2)
    return cloned


def search_reference_locations(*, query: str | None = None, limit: int = 20) -> list[dict[str, object]]:
    if limit < 1:
        raise ValidationError("limit must be positive")
    tokens = _query_tokens(query)
    scored = [(_score_entry(entry, tokens), entry) for entry in _normalized_entries()]
    scored.sort(
        key=lambda item: (
            item[0],
            item[1].get("kind") == "city",
            -(int(item[1].get("priority_rank") or 999)),
            str(item[1].get("name") or ""),
        ),
        reverse=True,
    )
    results = [_clone_entry(entry, match_score=score) for score, entry in scored if score > 0 or not tokens]
    return results[:limit]


def resolve_reference_city(value: str | None) -> dict[str, object] | None:
    if value is None:
        return None
    needle = _fold(value)
    if not needle:
        return None
    for entry in _normalized_entries():
        if entry.get("kind") != "city":
            continue
        name = _fold(str(entry.get("name") or ""))
        if needle == name:
            return _clone_entry(entry)
        aliases = [_fold(item) for item in entry.get("aliases", []) if isinstance(item, str)]
        typos = [_fold(item) for item in entry.get("typos", []) if isinstance(item, str)]
        if needle in aliases or needle in typos:
            return _clone_entry(entry)
    return None


def reference_city_coordinates(value: str | None) -> tuple[float, float] | None:
    city = resolve_reference_city(value)
    if city is None:
        return None
    latitude = city.get("latitude")
    longitude = city.get("longitude")
    if latitude is None or longitude is None:
        return None
    return float(latitude), float(longitude)


def resolve_reference_location(
    *,
    city: str | None = None,
    region: str | None = None,
    address_line: str | None = None,
    postal_code: str | None = None,
) -> dict[str, object] | None:
    city_entry = resolve_reference_city(city)
    address_entry: dict[str, object] | None = None
    if address_line is not None:
        address_hits = search_reference_locations(query=address_line, limit=10)
        for hit in address_hits:
            if hit.get("kind") == "neighborhood":
                address_entry = hit
                break
        if address_entry is None:
            for hit in address_hits:
                if hit.get("kind") == "city":
                    address_entry = hit
                    break
    combined_query = " ".join(part for part in (city, region, address_line, postal_code) if part)
    combined_hits = search_reference_locations(query=combined_query or city or address_line or region or postal_code, limit=10)
    combined_entry = combined_hits[0] if combined_hits else None

    if address_entry is not None:
        if city_entry is None or _fold(str(address_entry.get("city") or "")) == _fold(str(city_entry.get("city") or "")):
            return address_entry
        return _clone_entry(city_entry)
    if city_entry is not None:
        return city_entry
    if combined_entry is not None:
        return combined_entry
    return None
