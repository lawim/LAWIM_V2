from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class BusinessTransactionType(str, Enum):
    BUY = "BUY"
    RENT = "RENT"
    SELL = "SELL"
    INVEST = "INVEST"
    FINANCE = "FINANCE"
    FIND = "FIND"
    SERVICE = "SERVICE"
    SHORT_STAY = "SHORT_STAY"
    LEASE = "LEASE"
    COMMERCIAL_LEASE = "COMMERCIAL_LEASE"
    BUSINESS_TRANSFER = "BUSINESS_TRANSFER"


@dataclass
class IntentCandidate:
    intent: str = ""
    transaction_type: str = ""
    confidence: float = 0.0
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"intent": self.intent, "confidence": self.confidence, "source": self.source}


FR_KEYWORDS: dict[str, list[str]] = {
    "buy": ["acheter", "achat", "acquérir", "à acheter", "à vendre"],
    "rent": ["louer", "location", "locataire", "loyer", "à louer"],
    "sell": ["vendre", "vente", "vends"],
    "invest": ["investir", "investissement", "placement", "roi"],
    "finance": ["crédit", "prêt", "financement", "banque", "hypothèque"],
    "find": ["trouver", "professionnel", "notaire", "architecte", "artisan"],
    "service": ["service", "estimation", "expertise", "visite"],
}

EN_KEYWORDS: dict[str, list[str]] = {
    "buy": ["buy", "purchase", "looking for", "search"],
    "rent": ["rent", "lease", "tenant"],
    "sell": ["sell", "sale", "selling"],
    "invest": ["invest", "investment"],
    "finance": ["loan", "mortgage", "finance", "credit"],
    "find": ["find", "professional", "notary", "architect", "contractor"],
    "service": ["service", "valuation", "inspection"],
}


def _merged_keywords() -> dict[str, list[str]]:
    """Merge FR and EN keywords, combining lists for shared intent keys."""
    merged: dict[str, list[str]] = {}
    for k, v in FR_KEYWORDS.items():
        merged[k] = list(v)
    for k, v in EN_KEYWORDS.items():
        if k in merged:
            merged[k].extend(v)
        else:
            merged[k] = list(v)
    return merged

_ALL_KEYWORDS = _merged_keywords()


class IntentClassifier:
    def __init__(self, threshold: float = 0.70):
        self.threshold = threshold

    def classify(self, text: str) -> IntentCandidate:
        t = text.lower()
        for intent, keywords in _ALL_KEYWORDS.items():
            for kw in keywords:
                if kw in t:
                    return IntentCandidate(intent=intent, confidence=0.85, source="keyword")
        return IntentCandidate(intent="unknown", confidence=0.0, source="fallback")

    def classify_multi(self, text: str) -> list[IntentCandidate]:
        candidates: list[IntentCandidate] = []
        t = text.lower()
        for intent, keywords in _ALL_KEYWORDS.items():
            score = 0
            for kw in keywords:
                if kw in t:
                    score += 1
            if score > 0:
                confidence = min(0.95, 0.5 + score * 0.1)
                candidates.append(IntentCandidate(intent=intent, confidence=confidence, source="keyword"))
        return sorted(candidates, key=lambda c: c.confidence, reverse=True)


def classify_intent(text: str) -> str:
    return IntentClassifier().classify(text).intent


# ── Multi-Intent Handler ────────────────────────────────────────────────────


@dataclass
class MultiIntentHandler:
    primary: IntentCandidate | None = None
    secondary: list[IntentCandidate] = field(default_factory=list)

    def process(self, text: str) -> None:
        candidates = IntentClassifier().classify_multi(text)
        if candidates:
            self.primary = candidates[0]
            self.secondary = [c for c in candidates[1:] if c.confidence >= 0.40]


# ── Entity Extraction ──────────────────────────────────────────────────────


@dataclass
class EntityExtraction:
    budget_min: float | None = None
    budget_max: float | None = None
    city: str = ""
    property_type: str = ""
    surface_min: float | None = None
    bedrooms: int | None = None

    def extract(self, text: str) -> EntityExtraction:
        t = text.lower()
        amounts = re.findall(r'(\d+)\s*(million|millions|m|000)?', t)
        if amounts:
            num = float(amounts[0][0])
            suffix = amounts[0][1] if len(amounts[0]) > 1 else ""
            if suffix in ("million", "millions", "m"):
                val = num * 1_000_000
            else:
                val = num
            self.budget_max = val
        for city in ["douala", "yaounde", "bafoussam", "bamenda", "garoua"]:
            if city in t:
                self.city = city.capitalize()
                break
        types = {"appartement": "apartment", "maison": "house", "villa": "villa",
                 "terrain": "land", "studio": "studio", "bureau": "office"}
        for fr, en in types.items():
            if fr in t:
                self.property_type = en
                break
        return self


# ── Urgency Detector ───────────────────────────────────────────────────────


URGENCY_KEYWORDS: dict[str, float] = {
    "urgent": 0.9, "urgence": 0.9, "asap": 0.9, "rapidement": 0.8,
    "tout de suite": 0.9, "vite": 0.7, "pressé": 0.8, "dépêcher": 0.7,
}


@dataclass
class UrgencyDetector:
    score: float = 0.0
    level: str = "NORMAL"

    def detect(self, text: str) -> UrgencyDetector:
        t = text.lower()
        max_score = 0.0
        for keyword, score in URGENCY_KEYWORDS.items():
            if keyword in t:
                max_score = max(max_score, score)
        self.score = max_score
        if self.score >= 0.8:
            self.level = "HIGH"
        elif self.score >= 0.5:
            self.level = "MEDIUM"
        else:
            self.level = "NORMAL"
        return self


# ── Intent-to-Role Mapping ─────────────────────────────────────────────────


INTENT_ROLE_MAP: dict[str, str] = {
    "buy": "buyer", "rent": "tenant", "sell": "seller",
    "invest": "investor", "finance": "borrower",
    "find": "seeker", "service": "service_seeker",
}


@dataclass
class IntentRoleMapping:
    def map(self, intent: str) -> str:
        return INTENT_ROLE_MAP.get(intent.lower(), "unknown")
