from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ── Property Families ──────────────────────────────────────────────────────


class PropertyFamily(str, Enum):
    RESIDENTIAL = "RESIDENTIAL"
    COMMERCIAL = "COMMERCIAL"
    LAND = "LAND"
    AGRICULTURAL = "AGRICULTURAL"
    HOTELIER = "HOTELIER"
    INVESTMENT = "INVESTMENT"
    PROJECT = "PROJECT"


@dataclass
class AgriculturalProperty:
    crop_types: list[str] = field(default_factory=list)
    land_use: str = ""
    soil_quality: str = ""
    irrigation: bool = False
    farm_size_hectares: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {"crop_types": self.crop_types, "land_use": self.land_use,
                "soil_quality": self.soil_quality, "farm_size_ha": self.farm_size_hectares}


@dataclass
class HotelProperty:
    star_rating: int = 0
    room_count: int = 0
    amenities: list[str] = field(default_factory=list)
    restaurant: bool = False
    pool: bool = False
    conference_rooms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"star_rating": self.star_rating, "room_count": self.room_count,
                "amenities": self.amenities}


@dataclass
class InvestmentProperty:
    investment_type: str = ""
    roi_target: float = 0.0
    investment_horizon_months: int = 0
    expected_monthly_income: float = 0.0
    exit_strategy: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"investment_type": self.investment_type, "roi_target": self.roi_target,
                "horizon_months": self.investment_horizon_months}


INVESTMENT_TYPES: tuple[str, ...] = (
    "buy_to_let", "fix_and_flip", "development",
    "commercial_investment", "land_banking",
)


# ── Property State Machine ─────────────────────────────────────────────────


class PropertyState(str, Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    PUBLISHED = "PUBLISHED"
    RESERVED = "RESERVED"
    UNDER_NEGOTIATION = "UNDER_NEGOTIATION"
    SOLD = "SOLD"
    RENTED = "RENTED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


PROPERTY_TRANSITIONS: dict[PropertyState, list[PropertyState]] = {
    PropertyState.DRAFT: [PropertyState.PENDING_REVIEW, PropertyState.ARCHIVED],
    PropertyState.PENDING_REVIEW: [PropertyState.PUBLISHED, PropertyState.DRAFT, PropertyState.ARCHIVED],
    PropertyState.PUBLISHED: [PropertyState.RESERVED, PropertyState.UNDER_NEGOTIATION, PropertyState.ARCHIVED],
    PropertyState.RESERVED: [PropertyState.UNDER_NEGOTIATION, PropertyState.PUBLISHED, PropertyState.SOLD, PropertyState.RENTED],
    PropertyState.UNDER_NEGOTIATION: [PropertyState.RESERVED, PropertyState.SOLD, PropertyState.RENTED, PropertyState.PUBLISHED],
    PropertyState.SOLD: [PropertyState.ARCHIVED],
    PropertyState.RENTED: [PropertyState.ARCHIVED],
    PropertyState.ARCHIVED: [PropertyState.DELETED],
    PropertyState.DELETED: [],
}


@dataclass
class PropertyStateMachine:
    current_state: PropertyState = PropertyState.DRAFT

    def can_transition(self, target: PropertyState) -> bool:
        return target in PROPERTY_TRANSITIONS.get(self.current_state, [])

    def transition(self, target: PropertyState) -> PropertyState:
        if not self.can_transition(target):
            raise ValueError(f"Cannot transition from {self.current_state.value} to {target.value}")
        self.current_state = target
        return self.current_state


# ── Availability State Machine ─────────────────────────────────────────────


class AvailabilityState(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNDER_OPTION = "UNDER_OPTION"
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    RENTED = "RENTED"
    UNAVAILABLE = "UNAVAILABLE"
    SEASONAL = "SEASONAL"


AVAILABILITY_TRANSITIONS: dict[AvailabilityState, list[AvailabilityState]] = {
    AvailabilityState.AVAILABLE: [AvailabilityState.UNDER_OPTION, AvailabilityState.RESERVED, AvailabilityState.UNAVAILABLE],
    AvailabilityState.UNDER_OPTION: [AvailabilityState.RESERVED, AvailabilityState.AVAILABLE],
    AvailabilityState.RESERVED: [AvailabilityState.SOLD, AvailabilityState.RENTED, AvailabilityState.AVAILABLE],
    AvailabilityState.SOLD: [AvailabilityState.UNAVAILABLE],
    AvailabilityState.RENTED: [AvailabilityState.UNAVAILABLE, AvailabilityState.AVAILABLE],
    AvailabilityState.UNAVAILABLE: [AvailabilityState.AVAILABLE, AvailabilityState.SEASONAL],
    AvailabilityState.SEASONAL: [AvailabilityState.AVAILABLE, AvailabilityState.UNAVAILABLE],
}


# ── Price Concepts ─────────────────────────────────────────────────────────


@dataclass
class PriceConcept:
    price_displayed: float = 0.0
    negotiable: bool = False
    price_negotiable: float | None = None
    price_suggestion: float | None = None
    hidden_price: bool = False
    pricing_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"price_displayed": self.price_displayed, "negotiable": self.negotiable,
                "hidden_price": self.hidden_price}


class PriceType(str, Enum):
    ASKING = "ASKING"
    SELLING = "SELLING"
    RENTAL = "RENTAL"
    MONTHLY_CHARGES = "MONTHLY_CHARGES"
    AGENCY_FEES = "AGENCY_FEES"
    NOTARY_FEES = "NOTARY_FEES"
    TAX = "TAX"


# ── Data Quality Scoring ───────────────────────────────────────────────────


@dataclass
class DataQualityScore:
    completeness: float = 0.0
    reliability: float = 0.0
    total_score: float = 0.0

    def compute(self, filled_fields: int, total_fields: int,
                 verified: bool = False, has_photos: bool = False,
                 has_price: bool = False) -> DataQualityScore:
        self.completeness = min(100.0, (filled_fields / max(total_fields, 1)) * 100)
        reliability_score = 0.0
        if verified:
            reliability_score += 40.0
        if has_photos:
            reliability_score += 30.0
        if has_price:
            reliability_score += 30.0
        self.reliability = min(100.0, reliability_score)
        self.total_score = round(self.completeness * 0.6 + self.reliability * 0.4, 2)
        return self


def data_quality_score(filled: int, total: int, verified: bool = False,
                        has_photos: bool = False, has_price: bool = False) -> DataQualityScore:
    return DataQualityScore().compute(filled, total, verified, has_photos, has_price)


# ── Property Type Schemas ──────────────────────────────────────────────────


@dataclass
class PropertyTypeSchema:
    family: str = ""
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)
    validation_rules: dict[str, Any] = field(default_factory=dict)

    def validate(self, data: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for field in self.required_fields:
            if field not in data or data.get(field) is None:
                errors.append(f"Missing required field: {field}")
        return errors


# ── Publication Rules ──────────────────────────────────────────────────────


class PublicationRuleType(str, Enum):
    REQUIRED_FIELDS = "REQUIRED_FIELDS"
    PHOTOS = "PHOTOS"
    PRICE = "PRICE"
    LOCATION = "LOCATION"
    OWNER_VERIFIED = "OWNER_VERIFIED"
    AGENT = "AGENT"
    FEE = "FEE"
    NO_DUPLICATE = "NO_DUPLICATE"


@dataclass
class PropertyPublicationRule:
    rule_type: PublicationRuleType = PublicationRuleType.REQUIRED_FIELDS
    message: str = ""
    passes: bool = False


def validate_publication_rules(property_data: dict[str, Any]) -> list[PropertyPublicationRule]:
    rules: list[PropertyPublicationRule] = []
    required = ["property_family", "property_type", "city", "price_displayed"]
    missing = [f for f in required if f not in property_data]
    rules.append(PropertyPublicationRule(
        rule_type=PublicationRuleType.REQUIRED_FIELDS,
        message=f"Missing: {', '.join(missing)}" if missing else "All required fields present",
        passes=len(missing) == 0,
    ))
    has_photos = bool(property_data.get("photos"))
    rules.append(PropertyPublicationRule(
        rule_type=PublicationRuleType.PHOTOS,
        message="Photos present" if has_photos else "At least one photo required",
        passes=has_photos,
    ))
    has_price = property_data.get("price_displayed", 0) > 0
    rules.append(PropertyPublicationRule(
        rule_type=PublicationRuleType.PRICE,
        message="Price set" if has_price else "Price must be > 0",
        passes=has_price,
    ))
    return rules
