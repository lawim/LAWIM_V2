from __future__ import annotations

import re
import unicodedata

from .errors import ValidationError


_COUNTRY_ALIASES: dict[str, str] = {
    "cm": "Cameroon",
    "cameroon": "Cameroon",
    "cameroun": "Cameroon",
    "fr": "France",
    "france": "France",
    "sn": "Senegal",
    "senegal": "Senegal",
    "sénégal": "Senegal",
}

_REGION_BY_CITY: dict[str, str] = {
    "douala": "Littoral",
    "yaounde": "Centre",
    "yaoundé": "Centre",
    "kribi": "South",
    "bonanjo": "Littoral",
    "bastos": "Centre",
    "akwa": "Littoral",
}


def _collapse_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def normalize_country(country: str) -> str:
    normalized = _collapse_whitespace(country)
    if not normalized:
        raise ValidationError("country is required")
    key = normalized.lower()
    return _COUNTRY_ALIASES.get(key, normalized.title())


def normalize_city(city: str) -> str:
    normalized = _collapse_whitespace(city)
    if not normalized:
        raise ValidationError("city is required")
    return normalized.title()


def normalize_region(region: str | None, *, city: str | None = None) -> str | None:
    if region is not None:
        normalized = _collapse_whitespace(region)
        return normalized.title() if normalized else None
    if city:
        inferred = _REGION_BY_CITY.get(city.lower())
        if inferred:
            return inferred
    return None


def normalize_postal_code(postal_code: str | None) -> str | None:
    if postal_code is None:
        return None
    normalized = _collapse_whitespace(postal_code).upper()
    return normalized or None


def normalize_address_line(address_line: str | None) -> str | None:
    if address_line is None:
        return None
    normalized = _collapse_whitespace(address_line)
    return normalized or None


def validate_coordinates(latitude: float | None, longitude: float | None) -> tuple[float | None, float | None]:
    if latitude is not None and not -90.0 <= latitude <= 90.0:
        raise ValidationError("latitude must be between -90 and 90")
    if longitude is not None and not -180.0 <= longitude <= 180.0:
        raise ValidationError("longitude must be between -180 and 180")
    if (latitude is None) ^ (longitude is None):
        raise ValidationError("latitude and longitude must be provided together")
    return latitude, longitude


def build_geo_dto(
    *,
    city: str,
    country: str,
    latitude: float | None = None,
    longitude: float | None = None,
    region: str | None = None,
    address_line: str | None = None,
    postal_code: str | None = None,
) -> dict[str, object]:
    normalized_city = normalize_city(city)
    normalized_country = normalize_country(country)
    normalized_region = normalize_region(region, city=normalized_city)
    normalized_address = normalize_address_line(address_line)
    normalized_postal = normalize_postal_code(postal_code)
    validate_coordinates(latitude, longitude)
    search_key = _search_key(normalized_city, normalized_country, normalized_region)
    return {
        "address_line": normalized_address,
        "city": normalized_city,
        "region": normalized_region,
        "postal_code": normalized_postal,
        "country": normalized_country,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "search_key": search_key,
    }


def _search_key(city: str, country: str, region: str | None) -> str:
    parts = [city, region or "", country]
    folded = "|".join(_fold(part) for part in parts if part)
    return folded


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    stripped = "".join(char for char in normalized if not unicodedata.combining(char))
    return stripped.lower().strip()


def location_matches_query(location: dict[str, object], query: str) -> bool:
    needle = _fold(query)
    haystack = _fold(
        " ".join(
            str(location.get(key, "") or "")
            for key in ("address_line", "city", "region", "postal_code", "country", "search_key")
        )
    )
    return needle in haystack
