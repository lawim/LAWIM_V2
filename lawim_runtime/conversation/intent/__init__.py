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


# Priority-based intent hierarchy. Higher priority intents are checked first
# and can override lower-priority matches.
INTENT_PRIORITY: list[tuple[str, set[str], str]] = [
    # Safety and privacy (highest priority)
    ("hacking", {"hack", "pirate", "crack", "steal", "breach", "intrusion",
                 "cyber", "attack", "malware", "virus", "ransomware"}, "SAFETY"),
    ("fraud_report", {"fraud", "scam", "spam", "fake", "cheat", "phishing",
                      "arnaque", "escroquerie", "fraude"}, "SAFETY"),
    ("privacy_request", {"private number", "personal data", "private info",
                         "privacy", "confidentialite", "private contact",
                         "proprietaire numero", "owner number", "owner phone",
                         "proprietaire telephone"}, "PRIVACY"),
    ("data_deletion", {"delete all", "remove all", "supprime toutes", "delete my account",
                       "remove my data", "erase my data", "supprime mon compte"}, "PRIVACY"),
    # Account and support
    ("account_delete", {"account delete", "delete account", "supprimer compte",
                        "close account", "fermer compte"}, "ACCOUNT"),
    ("support_request", {"help", "aide", "support", "assistance", "problem",
                         "probleme", "bug", "error", "erreur", "not working",
                         "ne marche pas", "ne fonctionne pas"}, "SUPPORT"),
    ("human_handover", {"parler a une personne", "talk to a person", "conseiller",
                        "advisor", "agent humain", "humain", "operator", "speak to"},
                        "SUPPORT"),
    # Visit and transaction
    ("visit_cancel", {"annuler visite", "cancel visit", "annulation visite",
                      "ne viendrai pas", "wont come"}, "VISIT"),
    ("visit_reschedule", {"reprogrammer", "reschedule", "decaler", "postposer",
                          "reporter visite", "change date"}, "VISIT"),
    ("visit_request", {"visit", "visite", "visiter", "see property",
                       "voir le bien", "voir la maison"}, "VISIT"),
    ("payment_question", {"pay", "payer", "payment", "paiement", "payer mon loyer",
                          "pay rent", "monthly payment", "mensualite"}, "PAYMENT"),
    # Document and legal
    ("document_request", {"document", "papier", "piece", "document needed",
                          "what documents", "quels documents", "documents requis"}, "DOCUMENT"),
    ("legal_question", {"legal", "juridique", "loi", "law", "contract", "contrat",
                        "bail", "lease", "droit", "droits"}, "DOCUMENT"),
    # Property owner
    ("owner_listing", {"publish", "publier", "owner", "proprietaire", "annonce",
                       "listing", "post property", "ajouter mon bien"}, "OWNER"),
    ("owner_listing_update", {"modifier annonce", "update listing", "edit property",
                              "changer prix", "change price", "modifier prix"}, "OWNER"),
    ("owner_listing_remove", {"remove listing", "supprimer annonce", "delete listing",
                              "retirer mon bien", "bien deja loue", "bien deja vendu",
                              "already rented", "already sold"}, "OWNER"),
    ("agent_registration", {"agent", "agence", "broker", "courtier", "register agent",
                            "inscription agent"}, "OWNER"),
    # Property search (broad, should not override higher priorities)
    ("property_search", {"rent", "buy", "invest", "cherche", "recherche",
        "location", "achat", "louer", "acheter", "appartement", "maison", "studio",
        "terrain", "villa", "chambre", "pieces", "f2", "f3", "f4", "logement",
        "appart", "bureau", "local", "commercial", "immeuble", "duplex",
        "veut", "veux", "voudrais", "besoin", "property", "flat",
        "apartment", "house", "rental", "looking", "search", "wan", "need",
        "i am looking", "i want", "je cherche", "je veux", "nous cherchons",
        "plot", "land", "shop place", "modern room", "i di find",
        "looking for", "for rent", "for sale", "a louer", "a vendre",
        "a acheter", "recherchons", "cherchons"}, "PROPERTY"),
    ("complaint", {"complaint", "plainte", "reclam", "reclamation",
                   "insatisfait", "dissatisfied", "tres mecontent"}, "GENERAL"),
    ("greeting", {"bonjour", "salut", "hello", "hi", "bonsoir", "good morning",
                  "bjr", "slt", "hey", "good evening"}, "GENERAL"),
]


class IntentEngine:

    def detect(self, text: str, context: dict[str, Any] | None = None) -> IntentResult:
        if not text or not text.strip():
            return IntentResult(intent="unknown", confidence=0.0)
        text_lower = text.lower().strip()

        best_intent = "unknown"
        best_category = ""
        best_score = 0.0

        for intent_name, keywords, category in INTENT_PRIORITY:
            if not keywords:
                continue
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches == 0:
                continue
            # Score based on matches and keyword set size
            norm = min(len(keywords), 8.0)
            score = matches / norm
            # Higher priority intents (earlier in list) get boost
            priority_levels = len(INTENT_PRIORITY)
            current_index = next(i for i, (n, _, _) in enumerate(INTENT_PRIORITY) if n == intent_name)
            priority_boost = 1.0 + (priority_levels - current_index) / priority_levels * 0.5
            adjusted_score = score * priority_boost

            if adjusted_score > best_score:
                best_score = adjusted_score
                best_intent = intent_name
                best_category = category
            elif adjusted_score == best_score and current_index < next(
                i for i, (n, _, _) in enumerate(INTENT_PRIORITY) if n == best_intent
            ):
                best_intent = intent_name
                best_category = category

        confidence = min(best_score * 1.2, 1.0)

        return IntentResult(
            intent=best_intent,
            sub_intent=best_category,
            confidence=confidence,
            needs_clarification=confidence < 0.2,
        )
