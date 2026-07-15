from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MobilityMode(str, Enum):
    WALKING = "WALKING"
    CAR = "CAR"
    PUBLIC_TRANSIT = "PUBLIC_TRANSIT"
    ANY = "ANY"


MOBILITY_RADIUS_MULTIPLIER: dict[MobilityMode, float] = {
    MobilityMode.WALKING: 1.0,
    MobilityMode.CAR: 5.0,
    MobilityMode.PUBLIC_TRANSIT: 3.0,
    MobilityMode.ANY: 10.0,
}


def mobility_adjusted_radius(base_radius_km: float, mode: MobilityMode = MobilityMode.WALKING) -> float:
    return base_radius_km * MOBILITY_RADIUS_MULTIPLIER.get(mode, 1.0)


@dataclass
class GeographicRelation:
    relation_type: str = ""
    source_geo_id: str = ""
    target_geo_id: str = ""
    distance_km: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {"relation_type": self.relation_type, "source": self.source_geo_id,
                "target": self.target_geo_id, "distance_km": self.distance_km}


@dataclass
class MarketEquivalent:
    source_market: str = ""
    target_market: str = ""
    confidence: float = 0.0
    factors: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"source": self.source_market, "target": self.target_market,
                "confidence": self.confidence}


_KNOWN_EQUIVALENTS: dict[str, list[dict[str, Any]]] = {
    "douala": [{"market": "yaounde", "confidence": 0.8}],
    "yaounde": [{"market": "douala", "confidence": 0.8}],
}


def market_equivalent_for(market: str) -> list[dict[str, Any]]:
    return _KNOWN_EQUIVALENTS.get(market.lower(), [])


# ── Progressive Search Expansion ───────────────────────────────────────────


EXPANSION_STAGES: list[dict[str, Any]] = [
    {"level": 0, "name": "Exact", "description": "Exact location and criteria"},
    {"level": 1, "name": "Location+", "description": "Neighboring areas"},
    {"level": 2, "name": "City+", "description": "Same city, wider area"},
    {"level": 3, "name": "Budget+20%", "description": "Budget increased by 20%"},
    {"level": 4, "name": "Budget+50%", "description": "Budget increased by 50%"},
    {"level": 5, "name": "Type Relax", "description": "Similar property types"},
    {"level": 6, "name": "Family Relax", "description": "Same family, any type"},
    {"level": 7, "name": "Feature Relax", "description": "Optional features ignored"},
    {"level": 8, "name": "Maximal", "description": "All constraints relaxed"},
]


class ProgressiveSearchExpansion:
    def __init__(self, current_level: int = 0):
        self.current_level = current_level

    def can_expand(self) -> bool:
        return self.current_level < len(EXPANSION_STAGES) - 1

    def expand(self) -> dict[str, Any]:
        if self.can_expand():
            self.current_level += 1
        return self.current_stage()

    def current_stage(self) -> dict[str, Any]:
        return EXPANSION_STAGES[self.current_level]

    def reset(self) -> None:
        self.current_level = 0


def expansion_stage_for(level: int) -> dict[str, Any]:
    return EXPANSION_STAGES[level] if 0 <= level < len(EXPANSION_STAGES) else EXPANSION_STAGES[-1]


# ── Geography Constraints Engine ───────────────────────────────────────────


@dataclass
class GeoConstraintEngine:
    def valid_transaction_types(self, geo_level: str) -> list[str]:
        mapping = {
            "country": ["buy", "rent", "invest", "finance", "find", "service"],
            "region": ["buy", "rent", "invest"],
            "city": ["buy", "rent"],
            "neighborhood": ["buy", "rent"],
        }
        return mapping.get(geo_level.lower(), ["buy", "rent"])

    def valid_property_types(self, geo_level: str) -> list[str]:
        mapping = {
            "country": ["residential", "commercial", "land", "agricultural", "hotelier", "investment", "project"],
            "region": ["residential", "commercial", "land", "agricultural"],
            "city": ["residential", "commercial", "land"],
            "neighborhood": ["residential"],
        }
        return mapping.get(geo_level.lower(), ["residential"])


# ── Geo Reference Engine ───────────────────────────────────────────────────


@dataclass
class GeoReferenceEngine:
    def countries(self) -> list[dict[str, Any]]:
        return [{"code": "CM", "name": "Cameroon"}]

    def regions(self, country: str = "CM") -> list[dict[str, Any]]:
        return [{"code": r, "name": r} for r in ["Littoral", "Centre", "Yaounde"]]

    def cities(self, region: str = "") -> list[dict[str, Any]]:
        return [{"code": "DLA", "name": "Douala"}, {"code": "YDE", "name": "Yaounde"}]


# ── Geo Autocomplete Engine ────────────────────────────────────────────────


@dataclass
class GeoAutocompleteEngine:
    def search(self, query: str) -> list[dict[str, Any]]:
        results = []
        q = query.lower()
        known = {"douala": ("DLA", "city"), "yaounde": ("YDE", "city"),
                 "bonanjo": ("BNJ", "neighborhood"), "bonapriso": ("BPR", "neighborhood")}
        for name, (code, level) in known.items():
            if q in name:
                results.append({"code": code, "name": name.capitalize(), "level": level})
        return results[:10]
