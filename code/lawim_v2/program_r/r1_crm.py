from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class LeadClass(str, Enum):
    HOT = "HOT"
    WARM = "WARM"
    WARMISH = "WARMISH"
    COLD = "COLD"
    DEAD = "DEAD"


LEAD_CLASS_THRESHOLDS: dict[LeadClass, tuple[float, float]] = {
    LeadClass.HOT: (80, 100),
    LeadClass.WARM: (60, 79),
    LeadClass.WARMISH: (40, 59),
    LeadClass.COLD: (20, 39),
    LeadClass.DEAD: (0, 19),
}


class PipelineStage(str, Enum):
    LEAD_IN = "LEAD_IN"
    QUALIFICATION = "QUALIFICATION"
    PROPOSITION = "PROPOSITION"
    NEGOTIATION = "NEGOTIATION"
    CLOSING = "CLOSING"
    WON = "WON"
    LOST = "LOST"
    RECYCLED = "RECYCLED"


PIPELINE_ORDER: list[PipelineStage] = list(PipelineStage)


class LeadSLA(str, Enum):
    HOT_15M = "HOT_15M"
    WARM_1H = "WARM_1H"
    WARMISH_4H = "WARMISH_4H"
    COLD_24H = "COLD_24H"
    DEAD_48H = "DEAD_48H"


SLA_THRESHOLDS_MINUTES: dict[LeadSLA, int] = {
    LeadSLA.HOT_15M: 15,
    LeadSLA.WARM_1H: 60,
    LeadSLA.WARMISH_4H: 240,
    LeadSLA.COLD_24H: 1440,
    LeadSLA.DEAD_48H: 2880,
}


@dataclass
class LeadScore:
    score: float = 0.0
    base_score: float = 0.0
    boosters: dict[str, float] = field(default_factory=dict)
    penalties: dict[str, float] = field(default_factory=dict)

    def classify(self) -> LeadClass:
        for lc in [LeadClass.HOT, LeadClass.WARM, LeadClass.WARMISH, LeadClass.COLD, LeadClass.DEAD]:
            lo, hi = LEAD_CLASS_THRESHOLDS[lc]
            if lo <= self.score <= hi:
                return lc
        return LeadClass.DEAD

    def compute(self, base: float = 0.0, boosters: dict[str, float] | None = None,
                 penalties: dict[str, float] | None = None) -> LeadScore:
        self.base_score = base
        self.boosters = boosters or {}
        self.penalties = penalties or {}
        total = base + sum(self.boosters.values()) - sum(self.penalties.values())
        self.score = max(0.0, min(100.0, total))
        return self


BOOSTER_DEFINITIONS: list[dict[str, Any]] = [
    {"code": "budget_detected", "label": "Budget détecté", "value": 15},
    {"code": "city_detected", "label": "Ville détectée", "value": 10},
    {"code": "urgent_request", "label": "Demande urgente", "value": 20},
    {"code": "diaspora_detected", "label": "Profil diaspora", "value": 25},
    {"code": "cash_purchase", "label": "Achat comptant", "value": 15},
    {"code": "neighborhood_detected", "label": "Quartier précis", "value": 10},
    {"code": "visit_intent", "label": "Intention de visite", "value": 20},
    {"code": "property_type_match", "label": "Type de bien précis", "value": 10},
    {"code": "phone_provided", "label": "Téléphone fourni", "value": 5},
    {"code": "email_provided", "label": "Email fourni", "value": 5},
    {"code": "qualified_previously", "label": "Déjà qualifié", "value": 10},
    {"code": "high_value", "label": "Budget élevé", "value": 15},
    {"code": "multi_intent", "label": "Multi-intention", "value": 10},
]

PENALTY_DEFINITIONS: list[dict[str, Any]] = [
    {"code": "missing_budget", "label": "Budget manquant", "value": 10},
    {"code": "unclear_location", "label": "Localisation floue", "value": 10},
    {"code": "spam_like", "label": "Message suspect", "value": 50},
    {"code": "duplicate_request", "label": "Requête en double", "value": 20},
    {"code": "incomplete_profile", "label": "Profil incomplet", "value": 5},
    {"code": "no_contact_info", "label": "Sans coordonnées", "value": 15},
    {"code": "out_of_area", "label": "Hors zone couverte", "value": 25},
    {"code": "unrealistic_budget", "label": "Budget irréaliste", "value": 15},
]


@dataclass
class LeadScoringEngine:
    def score(self, base: float, signals: dict[str, bool]) -> LeadScore:
        boosters = {}
        penalties = {}
        for bd in BOOSTER_DEFINITIONS:
            if signals.get(bd["code"], False):
                boosters[bd["code"]] = float(bd["value"])
        for pd in PENALTY_DEFINITIONS:
            if signals.get(pd["code"], False):
                penalties[pd["code"]] = float(pd["value"])
        return LeadScore().compute(base, boosters, penalties)


@dataclass
class CRMRoutingEngine:
    def route(self, score: LeadScore, zone: str = "",
               agents_available: list[str] | None = None) -> dict[str, Any]:
        lc = score.classify()
        strategy = "round_robin"
        if lc == LeadClass.HOT:
            strategy = "immediate"
        elif lc in (LeadClass.WARM, LeadClass.WARMISH):
            strategy = "score_based"
        return {"strategy": strategy, "classification": lc.value, "score": score.score}


@dataclass
class PipelineItem:
    item_id: str = ""
    stage: PipelineStage = PipelineStage.LEAD_IN
    lead_id: str = ""
    score: float = 0.0

    def advance(self) -> PipelineStage:
        idx = PIPELINE_ORDER.index(self.stage)
        if idx < len(PIPELINE_ORDER) - 1:
            self.stage = PIPELINE_ORDER[idx + 1]
        return self.stage

    def can_advance(self) -> bool:
        return PIPELINE_ORDER.index(self.stage) < len(PIPELINE_ORDER) - 1
