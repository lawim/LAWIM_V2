from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MatchDimension(str, Enum):
    LOCATION = "location"
    BUDGET = "budget"
    PROPERTY_TYPE = "property_type"
    BEDROOMS = "bedrooms"
    SURFACE = "surface"
    TRANSACTION_TYPE = "transaction_type"
    AVAILABILITY = "availability"
    PARTNER_REPUTATION = "partner_reputation"
    SERVICE_TYPE = "service_type"
    PROXIMITY = "proximity"


@dataclass
class DimensionWeight:
    dimension: MatchDimension
    weight: float = 1.0

    def __post_init__(self) -> None:
        if self.weight < 0:
            self.weight = 0.0


DEFAULT_WEIGHTS: dict[MatchDimension, float] = {
    MatchDimension.LOCATION: 0.25,
    MatchDimension.BUDGET: 0.25,
    MatchDimension.PROPERTY_TYPE: 0.15,
    MatchDimension.BEDROOMS: 0.10,
    MatchDimension.SURFACE: 0.05,
    MatchDimension.TRANSACTION_TYPE: 0.10,
    MatchDimension.AVAILABILITY: 0.05,
    MatchDimension.PARTNER_REPUTATION: 0.03,
    MatchDimension.SERVICE_TYPE: 0.02,
}


@dataclass
class MatchingCriteria:
    dimensions: dict[MatchDimension, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))
    required_dimensions: set[MatchDimension] = field(default_factory=set)
    thresholds: dict[MatchDimension, float] = field(default_factory=dict)

    def set_weight(self, dimension: MatchDimension, weight: float) -> None:
        self.dimensions[dimension] = max(0.0, weight)

    def get_weight(self, dimension: MatchDimension) -> float:
        return self.dimensions.get(dimension, 1.0)

    def set_threshold(self, dimension: MatchDimension, threshold: float) -> None:
        self.thresholds[dimension] = max(0.0, min(1.0, threshold))

    def get_threshold(self, dimension: MatchDimension) -> float:
        return self.thresholds.get(dimension, 0.0)

    def require_dimension(self, dimension: MatchDimension) -> None:
        self.required_dimensions.add(dimension)

    def is_required(self, dimension: MatchDimension) -> bool:
        return dimension in self.required_dimensions

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimensions": {d.value: w for d, w in self.dimensions.items()},
            "required_dimensions": [d.value for d in self.required_dimensions],
            "thresholds": {d.value: t for d, t in self.thresholds.items()},
        }
