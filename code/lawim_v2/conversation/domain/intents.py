from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    RENT_APARTMENT = "rent_apartment"
    RENT_STUDIO = "rent_studio"
    RENT_ROOM = "rent_room"
    RENT_HOUSE = "rent_house"
    RENT_VILLA = "rent_villa"
    RENT_COMMERCIAL = "rent_commercial"
    BUY_LAND = "buy_land"
    BUY_HOUSE = "buy_house"
    BUY_APARTMENT = "buy_apartment"
    BUY_VILLA = "buy_villa"
    BUY_COMMERCIAL = "buy_commercial"
    BUY_BUILDING = "buy_building"
    SELL_LAND = "sell_land"
    SELL_HOUSE = "sell_house"
    SELL_APARTMENT = "sell_apartment"
    SELL_PROPERTY = "sell_property"
    RENT_OUT = "rent_out"
    CONSTRUCT = "construct"
    RENOVATE = "renovate"
    INVEST = "invest"
    FIND_ARCHITECT = "find_architect"
    FIND_ENGINEER = "find_engineer"
    FIND_TECHNICIAN = "find_technician"
    FIND_NOTARY = "find_notary"
    FIND_AGENT = "find_agent"
    FIND_CONTRACTOR = "find_contractor"
    FIND_LAWYER = "find_lawyer"
    DOCUMENTATION = "documentation"
    INFORMATION = "information"
    COMPLAINT = "complaint"
    HANDOVER = "handover"
    GREETING = "greeting"
    OTHER = "other"

    @classmethod
    def searchable(cls) -> set[Intent]:
        return {
            cls.RENT_APARTMENT,
            cls.RENT_STUDIO,
            cls.RENT_ROOM,
            cls.RENT_HOUSE,
            cls.RENT_VILLA,
            cls.RENT_COMMERCIAL,
            cls.BUY_LAND,
            cls.BUY_HOUSE,
            cls.BUY_APARTMENT,
            cls.BUY_VILLA,
            cls.BUY_COMMERCIAL,
            cls.BUY_BUILDING,
            cls.SELL_LAND,
            cls.SELL_HOUSE,
            cls.SELL_APARTMENT,
            cls.SELL_PROPERTY,
            cls.RENT_OUT,
            cls.CONSTRUCT,
            cls.RENOVATE,
            cls.INVEST,
            cls.FIND_ARCHITECT,
            cls.FIND_ENGINEER,
            cls.FIND_TECHNICIAN,
            cls.FIND_NOTARY,
            cls.FIND_AGENT,
            cls.FIND_CONTRACTOR,
            cls.FIND_LAWYER,
        }

    @classmethod
    def requires_property(cls) -> set[Intent]:
        return {
            cls.RENT_APARTMENT,
            cls.RENT_STUDIO,
            cls.RENT_ROOM,
            cls.RENT_HOUSE,
            cls.RENT_VILLA,
            cls.RENT_COMMERCIAL,
            cls.BUY_LAND,
            cls.BUY_HOUSE,
            cls.BUY_APARTMENT,
            cls.BUY_VILLA,
            cls.BUY_COMMERCIAL,
            cls.BUY_BUILDING,
        }

    @classmethod
    def requires_professional(cls) -> set[Intent]:
        return {
            cls.FIND_ARCHITECT,
            cls.FIND_ENGINEER,
            cls.FIND_TECHNICIAN,
            cls.FIND_NOTARY,
            cls.FIND_AGENT,
            cls.FIND_CONTRACTOR,
            cls.FIND_LAWYER,
        }


@dataclass(frozen=True)
class IntentCandidate:
    intent: Intent
    confidence: float
    source: str  # "explicit", "inferred", "llm_classification"
    raw_trigger: str | None = None

    def is_confident(self, threshold: float = 0.6) -> bool:
        return self.confidence >= threshold
