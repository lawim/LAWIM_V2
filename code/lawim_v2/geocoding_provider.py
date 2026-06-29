from __future__ import annotations

import hashlib
import os
from typing import Protocol, runtime_checkable
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from .errors import ValidationError
from .geo_domain import build_geo_dto


@runtime_checkable
class GeocodingProvider(Protocol):
    name: str

    def geocode(
        self,
        *,
        city: str,
        country: str,
        region: str | None = None,
        address_line: str | None = None,
        postal_code: str | None = None,
    ) -> dict[str, object]: ...


class LocalGeocodingProvider:
    name = "local"

    def geocode(
        self,
        *,
        city: str,
        country: str,
        region: str | None = None,
        address_line: str | None = None,
        postal_code: str | None = None,
    ) -> dict[str, object]:
        seed = "|".join(
            part
            for part in (
                (address_line or "").lower(),
                city.lower(),
                (region or "").lower(),
                (postal_code or "").lower(),
                country.lower(),
            )
            if part
        )
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        lat_offset = (int(digest[:8], 16) % 10_000) / 100_000.0
        lon_offset = (int(digest[8:16], 16) % 10_000) / 100_000.0
        base_coords = {
            "douala": (4.05, 9.7),
            "yaounde": (3.867, 11.516),
            "yaoundé": (3.867, 11.516),
            "kribi": (2.938, 9.907),
        }
        base_lat, base_lon = base_coords.get(city.lower(), (4.0, 9.5))
        location = build_geo_dto(
            city=city,
            country=country,
            region=region,
            address_line=address_line,
            postal_code=postal_code,
            latitude=round(base_lat + lat_offset, 6),
            longitude=round(base_lon + lon_offset, 6),
        )
        return {
            "location": location,
            "provider": self.name,
            "confidence": 0.55,
            "deterministic": True,
        }


class ExternalGeocodingProvider:
    name = "external"

    def __init__(self, *, base_url: str, api_key: str | None = None, timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def geocode(
        self,
        *,
        city: str,
        country: str,
        region: str | None = None,
        address_line: str | None = None,
        postal_code: str | None = None,
    ) -> dict[str, object]:
        query = ", ".join(part for part in (address_line, city, region, postal_code, country) if part)
        if not query.strip():
            raise ValidationError("geocoding query is required")
        params = f"q={quote_plus(query)}&format=json&limit=1"
        if self.api_key:
            params = f"{params}&key={quote_plus(self.api_key)}"
        url = f"{self.base_url}?{params}"
        request = Request(url, headers={"User-Agent": "LAWIM_V2/0.1"})
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read()
        except OSError as exc:
            raise ValidationError(f"external geocoding unavailable: {exc}") from exc
        import json

        try:
            data = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValidationError("external geocoding returned invalid JSON") from exc
        if not isinstance(data, list) or not data:
            raise ValidationError("external geocoding returned no results")
        hit = data[0]
        latitude = float(hit.get("lat"))
        longitude = float(hit.get("lon"))
        location = build_geo_dto(
            city=city,
            country=country,
            region=region or hit.get("display_name"),
            address_line=address_line,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude,
        )
        return {
            "location": location,
            "provider": self.name,
            "confidence": 0.85,
            "deterministic": False,
        }


def resolve_geocoding_provider(
    *,
    provider_name: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> GeocodingProvider:
    normalized = (provider_name or os.getenv("LAWIM_GEOCODING_PROVIDER", "local")).strip().lower()
    if normalized == "external":
        resolved_base = base_url or os.getenv("LAWIM_GEOCODING_BASE_URL", "https://nominatim.openstreetmap.org/search")
        resolved_key = api_key or os.getenv("LAWIM_GEOCODING_API_KEY")
        return ExternalGeocodingProvider(base_url=resolved_base, api_key=resolved_key)
    return LocalGeocodingProvider()
