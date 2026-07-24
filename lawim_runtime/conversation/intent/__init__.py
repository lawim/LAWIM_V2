from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntentResult:
    intent: str = ""
    confidence: float = 0.0
    sub_intent: str = ""
    entities: dict[str, Any] = field(default_factory=dict)
    needs_clarification: bool = False


REAL_ESTATE_INTENTS = {
    "property_search": {
        "rent", "buy", "invest", "find", "cherche", "recherche", "location", "achat",
        "louer", "acheter", "appartement", "maison", "studio", "terrain", "villa",
        "chambre", "pieces", "f2", "f3", "f4", "t2", "t3", "t4", "logement",
        "appart", "bureau", "local", "commercial", "immeuble", "duplex",
        "recherch", "recherchons", "cherchons", "veut", "veux", "voudrais",
        "besoin", "recherche", "property", "flat", "apartment", "house", "rental",
        "looking", "search", "wan", "find", "need", "looking for", "looking", "for rent",
        "for sale", "i am looking", "i want", "je cherche", "je veux", "nous cherchons",
    },
    "visit_request": {"visit", "visite", "voir", "visiter", "visit_request"},
    "payment": {"pay", "payer", "payment", "paiement", "paiement"},
    "estimate": {"estimate", "estim", "evalu", "evaluer", "prix", "combien"},
    "support": {"help", "aide", "support", "assistance", "problem", "probleme", "bug"},
    "owner_registration": {"owner", "proprietaire", "publish", "publier", "owner_registration"},
    "agent_registration": {"agent", "agence", "broker", "courtier"},
    "complaint": {"complaint", "plainte", "reclam", "reclamation"},
    "information": {"info", "information", "question", "renseignement"},
    "greeting": {"bonjour", "salut", "hello", "hi", "bonsoir", "good morning", "bjr", "slt"},
}


class IntentEngine:

    def detect(self, text: str, context: dict[str, Any] | None = None) -> IntentResult:
        if not text or not text.strip():
            return IntentResult(intent="unknown", confidence=0.0)
        text_lower = text.lower().strip()
        words = set(text_lower.split())
        best_intent = "unknown"
        best_score = 0.0
        # Normalize by fixed denominator to avoid penalizing rich keyword sets
        norm = 5.0
        for intent, keywords in REAL_ESTATE_INTENTS.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            score = min(matches / norm, 1.0)
            # Apply small discount for greeting to avoid overshadowing business intents
            if intent == "greeting":
                score *= 0.8
            if score > best_score:
                best_score = score
                best_intent = intent
        return IntentResult(
            intent=best_intent,
            confidence=min(best_score * 1.5, 1.0),
            needs_clarification=best_score < 0.15,
        )
