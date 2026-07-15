from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ScoringDimension(str, Enum):
    LOCATION = "LOCATION"
    BUDGET = "BUDGET"
    PROPERTY_TYPE = "PROPERTY_TYPE"
    FEATURES = "FEATURES"
    AGENT_QUALITY = "AGENT_QUALITY"


DEFAULT_DIMENSION_WEIGHTS: dict[ScoringDimension, float] = {
    ScoringDimension.LOCATION: 0.25,
    ScoringDimension.BUDGET: 0.25,
    ScoringDimension.PROPERTY_TYPE: 0.20,
    ScoringDimension.FEATURES: 0.15,
    ScoringDimension.AGENT_QUALITY: 0.15,
}


class GeoScoringTier(str, Enum):
    SAME_NEIGHBORHOOD = "SAME_NEIGHBORHOOD"
    SAME_CITY = "SAME_CITY"
    SAME_REGION = "SAME_REGION"
    SAME_COUNTRY = "SAME_COUNTRY"
    INTERNATIONAL = "INTERNATIONAL"


GEO_TIER_SCORES: dict[GeoScoringTier, float] = {
    GeoScoringTier.SAME_NEIGHBORHOOD: 100,
    GeoScoringTier.SAME_CITY: 80,
    GeoScoringTier.SAME_REGION: 50,
    GeoScoringTier.SAME_COUNTRY: 20,
    GeoScoringTier.INTERNATIONAL: 0,
}


class CompatibilityLevel(str, Enum):
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    AVERAGE = "AVERAGE"
    LOW = "LOW"


COMPATIBILITY_THRESHOLDS: dict[CompatibilityLevel, float] = {
    CompatibilityLevel.EXCELLENT: 85,
    CompatibilityLevel.GOOD: 70,
    CompatibilityLevel.AVERAGE: 50,
    CompatibilityLevel.LOW: 0,
}


class MatchingRole(str, Enum):
    DEMANDEUR = "DEMANDEUR"
    HOLDER = "HOLDER"
    AGENT_DEMANDEUR = "AGENT_DEMANDEUR"
    AGENT_HOLDER = "AGENT_HOLDER"
    AGENCY_ADMIN = "AGENCY_ADMIN"
    SUPERVISOR = "SUPERVISOR"
    MEDIATOR = "MEDIATOR"
    EXPERT = "EXPERT"
    SYSTEM = "SYSTEM"


@dataclass
class ExclusionRule:
    rule_code: str = ""
    description: str = ""
    applies: bool = False

    def evaluate(self, demand: dict[str, Any], offer: dict[str, Any]) -> bool:
        if self.rule_code == "already_contacted":
            return False
        if self.rule_code == "same_owner":
            return str(demand.get("owner_id")) == str(offer.get("owner_id"))
        if self.rule_code == "budget_mismatch":
            budget_min = demand.get("budget_min", 0)
            price = offer.get("price", 0)
            if budget_min and price:
                return abs(price - budget_min) / max(budget_min, 1) > 0.5
            return False
        return False


@dataclass
class MatchingResult:
    score: float = 0.0
    dimension_scores: dict[str, float] = field(default_factory=dict)
    compatibility: CompatibilityLevel = CompatibilityLevel.LOW
    exclusions: list[str] = field(default_factory=list)
    rank: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {"score": round(self.score, 1), "compatibility": self.compatibility.value,
                "rank": self.rank, "exclusions": self.exclusions}


def compute_compatibility(score: float) -> CompatibilityLevel:
    for level in [CompatibilityLevel.EXCELLENT, CompatibilityLevel.GOOD,
                  CompatibilityLevel.AVERAGE, CompatibilityLevel.LOW]:
        if score >= COMPATIBILITY_THRESHOLDS[level]:
            return level
    return CompatibilityLevel.LOW


def compute_score(dim_scores: dict[str, float],
                   weights: dict[ScoringDimension, float] | None = None) -> float:
    w = weights or DEFAULT_DIMENSION_WEIGHTS
    total = 0.0
    for dim, val in dim_scores.items():
        try:
            d = ScoringDimension(dim.upper())
            total += val * w.get(d, 0)
        except ValueError:
            total += val * 0.1
    return min(100.0, total)


@dataclass
class ScoringDimensionScore:
    dimension: ScoringDimension = ScoringDimension.LOCATION
    score: float = 0.0
    weight: float = 0.0
    weighted: float = 0.0


@dataclass
class TransactionSuccessScore:
    score: float = 0.0
    sample_size: int = 0

    def compute(self, historical_successes: int, historical_total: int) -> TransactionSuccessScore:
        if historical_total == 0:
            self.score = 0.0
            self.sample_size = 0
        else:
            self.score = min(100.0, (historical_successes / historical_total) * 100)
            self.sample_size = historical_total
        return self


# ── Matching Engine ─────────────────────────────────────────────────────────


class MatchingEngine:
    def __init__(self, weights: dict[ScoringDimension, float] | None = None):
        self.weights = weights or DEFAULT_DIMENSION_WEIGHTS
        self.exclusion_rules: list[ExclusionRule] = []

    def add_exclusion_rule(self, rule: ExclusionRule) -> None:
        self.exclusion_rules.append(rule)

    def match(self, demand: dict[str, Any], offers: list[dict[str, Any]]) -> list[MatchingResult]:
        results: list[MatchingResult] = []
        for offer in offers:
            exclusions = self._check_exclusions(demand, offer)
            if exclusions:
                results.append(MatchingResult(score=0, exclusions=exclusions))
                continue
            dim_scores = self._score_dimensions(demand, offer)
            total = compute_score(dim_scores, self.weights)
            comp = compute_compatibility(total)
            results.append(MatchingResult(score=total, dimension_scores=dim_scores,
                                           compatibility=comp))
        results.sort(key=lambda r: r.score, reverse=True)
        for i, r in enumerate(results):
            r.rank = i + 1
        return results[:10]

    def _check_exclusions(self, demand: dict[str, Any], offer: dict[str, Any]) -> list[str]:
        active: list[str] = []
        for rule in self.exclusion_rules:
            if rule.evaluate(demand, offer):
                active.append(rule.rule_code)
        return active

    def _score_dimensions(self, demand: dict[str, Any], offer: dict[str, Any]) -> dict[str, float]:
        scores: dict[str, float] = {}
        ds = demand.get("city", "").lower()
        os = offer.get("city", "").lower()
        if ds and os and ds == os:
            scores["LOCATION"] = GEO_TIER_SCORES[GeoScoringTier.SAME_CITY]
        else:
            scores["LOCATION"] = GEO_TIER_SCORES[GeoScoringTier.SAME_COUNTRY]
        db = demand.get("budget_max", 0)
        op = offer.get("price", 0)
        if db and op:
            ratio = min(op, db) / max(op, db, 1)
            scores["BUDGET"] = ratio * 100
        else:
            scores["BUDGET"] = 0
        dt = demand.get("property_type", "").lower()
        ot = offer.get("property_type", "").lower()
        scores["PROPERTY_TYPE"] = 100.0 if dt and ot and dt == ot else 0.0
        scores["FEATURES"] = 50.0
        scores["AGENT_QUALITY"] = 50.0
        return scores


# ── Rematching Engine ───────────────────────────────────────────────────────


@dataclass
class RematchingEngine:
    rematch_count: int = 0
    max_rematches: int = 3
    reasons: list[str] = field(default_factory=list)

    def can_rematch(self) -> bool:
        return self.rematch_count < self.max_rematches

    def rematch(self, reason: str) -> bool:
        if not self.can_rematch():
            return False
        self.rematch_count += 1
        self.reasons.append(reason)
        return True


# ── Market Tension Index ────────────────────────────────────────────────────


def compute_market_tension(demand_count: int, supply_count: int) -> float:
    if supply_count == 0:
        return 100.0 if demand_count > 0 else 0.0
    return min(100.0, (demand_count / supply_count) * 100)
