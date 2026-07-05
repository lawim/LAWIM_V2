from __future__ import annotations

import hashlib
import os
from typing import Protocol, runtime_checkable
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from .errors import ValidationError
from .geo_domain import build_geo_dto
from .geo_reference import reference_city_coordinates, resolve_reference_location


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

    _FALLBACK_COORDS = {
        "douala": (4.05, 9.7),
        "yaounde": (3.867, 11.516),
        "yaoundé": (3.867, 11.516),
        "kribi": (2.938, 9.907),
    }

    def _fallback_anchor(self, city: str) -> tuple[float, float]:
        return self._FALLBACK_COORDS.get(city.lower(), (4.0, 9.5))

    def _deterministic_offsets(self, seed: str) -> tuple[float, float]:
        digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
        lat_offset = ((int(digest[:8], 16) % 2_000) / 100_000.0) - 0.01
        lon_offset = ((int(digest[8:16], 16) % 2_000) / 100_000.0) - 0.01
        return lat_offset, lon_offset

    def geocode(
        self,
        *,
        city: str,
        country: str,
        region: str | None = None,
        address_line: str | None = None,
        postal_code: str | None = None,
    ) -> dict[str, object]:
        reference = resolve_reference_location(
            city=city,
            region=region,
            address_line=address_line,
            postal_code=postal_code,
        )
        anchor_city = str(reference.get("city") or city) if reference is not None else city
        if reference is not None and isinstance(reference.get("region"), str) and reference.get("region"):
            anchor_region = str(reference.get("region"))
        else:
            anchor_region = region
        reference_coords = None
        if reference is not None:
            lat = reference.get("latitude")
            lon = reference.get("longitude")
            if lat is not None and lon is not None:
                reference_coords = (float(lat), float(lon))
            else:
                reference_coords = reference_city_coordinates(anchor_city)
        if reference_coords is not None:
            base_lat, base_lon = reference_coords
            confidence = 0.9 if reference.get("kind") == "city" else 0.86
        else:
            base_lat, base_lon = self._fallback_anchor(anchor_city)
            confidence = 0.55
        seed = "|".join(
            part
            for part in (
                (address_line or "").lower(),
                anchor_city.lower(),
                (anchor_region or "").lower(),
                (postal_code or "").lower(),
                country.lower(),
            )
            if part
        )
        lat_offset, lon_offset = self._deterministic_offsets(seed)
        location = build_geo_dto(
            city=anchor_city,
            country=country,
            region=anchor_region,
            address_line=address_line,
            postal_code=postal_code,
            latitude=round(base_lat + lat_offset, 6),
            longitude=round(base_lon + lon_offset, 6),
        )
        payload: dict[str, object] = {
            "location": location,
            "provider": self.name,
            "confidence": confidence,
            "deterministic": True,
        }
        if reference is not None:
            payload["reference"] = {
                "kind": reference.get("kind"),
                "name": reference.get("name"),
                "city": reference.get("city"),
                "region": reference.get("region"),
                "sources": reference.get("sources", []),
                "confidence": reference.get("confidence"),
                "match_score": reference.get("match_score"),
            }
        return payload


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
