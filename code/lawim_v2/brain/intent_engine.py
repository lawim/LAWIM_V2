from __future__ import annotations

import re
from typing import Any

SPECIFIC_INTENTS: dict[str, tuple[str, ...]] = {
    "buy": (
        "acheter", "achat", "acquérir", "acquisition",
        "buy", "purchase", "acquire",
        "buyam", "buy-am", "buy am",
    ),
    "rent": (
        "louer", "location", "locataire", "loyer",
        "rent", "rental", "lease", "tenant",
        "hire", "apartment", "appartement",
    ),
    "sell": (
        "vendre", "vente", "mettre en vente",
        "sell", "sale", "listing",
        "sellam", "sell-am", "sell am",
    ),
    "invest": (
        "investir", "investissement", "placement", "rendement",
        "invest", "investment", "roi", "yield",
    ),
    "build": (
        "construire", "construction", "bâtir", "bâtiment", "édifier",
        "build", "construction", "edifice",
        "buildam", "build-am",
    ),
    "find_land": (
        "terrain", "parcelle", "foncier", "lot",
        "land", "plot", "parcel", "lot",
        "graound", "graun",
    ),
    "find_partner": (
        "notaire", "architecte", "géomètre", "agent immobilier", "avocat",
        "notary", "architect", "surveyor", "real estate agent", "lawyer", "broker",
        "expert", "professionnel",
    ),
    "find_funding": (
        "financement", "prêt", "crédit", "banque", "hypothèque",
        "funding", "loan", "credit", "bank", "mortgage", "financing",
        "money", "lend", "emprunt",
    ),
    "manage": (
        "gestion", "gérer", "administrer",
        "manage", "management", "property management",
    ),
}

GENERIC_INTENTS: dict[str, tuple[str, ...]] = {
    "find_property": (
        "recherche", "cherche", "trouver", "rechercher", "propriété",
        "search", "find", "looking", "property", "looking for",
        "dey find", "dey look",
    ),
}

REGION_CITIES: dict[str, tuple[str, ...]] = {
    "douala": ("douala", "deido", "bonanjo", "bonapriso", "akwa", "bepanda", "maképé", "bonamoussadi", "ndokotti", "logbaba", "yassa", "bonaberi"),
    "yaounde": ("yaoundé", "yaounde", "bastos", "mfoundi", "mvog-mbi", "mvan", "nlongkak", "omo", "biyem-assi", "mendong", "cité-verte", "ekounou"),
    "bafoussam": ("bafoussam", "djeleng", "kouogouo", "famla"),
    "garoua": ("garoua", "roumde-adja"),
    "bamenda": ("bamenda", "nkwen", "mankon", "bayelle"),
    "limbe": ("limbe", "bota", "down-beach"),
    "kribi": ("kribi", "mboamanga"),
    "maroua": ("maroua", "doualaré", "hardé"),
    "ngaoundere": ("ngaoundéré", "ngaoundere"),
}

PROPERTY_TYPES: tuple[str, ...] = (
    "maison", "villa", "appartement", "studio", "duplex",
    "house", "villa", "apartment", "studio", "duplex",
    "immeuble", "building",
    "terrain", "land", "parcelle",
    "bureau", "office",
    "commerce", "shop", "magasin", "entrepôt", "warehouse",
    "clinique", "clinic",
    "résidence", "residence",
)

BUDGET_PATTERN = re.compile(
    r"(\d+[\s]*[mM]illon[s]?|\d+[\s]*[mM]|\d+[\s]*[kK]F[Aa]?|\d+[\s]*(?:fois|FCFA|franc[s]?|XAF|EUR|USD|euro|dollar)s?|\d{4,})"
)

SURFACE_PATTERN = re.compile(r"(\d+)\s*m[²2]")

TEXT_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
                 "un": 1, "deux": 2, "trois": 3, "quatre": 4, "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10}

BEDROOM_PATTERN = re.compile(r"(\d+)\s*(?:-?\s*(?:chambr|pièce|room|bedroom|pièces|chambres))")
TEXT_BEDROOM_PATTERN = re.compile(r"(one|two|three|four|five|six|seven|eight|nine|ten|un|deux|trois|quatre|cinq)\s*(?:-?\s*(?:chambr|pièce|room|bedroom|pièces|chambres))")

LANGUAGE_PATTERNS: dict[str, tuple[str, str, ...]] = {
    "fr": (r"\bje\b", r"\bnous\b", r"\bvoudrais\b", r"\bveux\b", r"\bcherche\b", r"\bbonjour\b", r"\bsvp\b", r"\bs'il vous plaît\b"),
    "en": (r"\bi want\b", r"\bi would\b", r"\bi need\b", r"\bi am looking\b", r"\bhello\b", r"\bhi\b", r"\bplease\b"),
    "pcm": (r"\bi dey\b", r"\bwetin\b", r"\bmake i\b", r"\babi\b", r"\booh\b", r"\bno be\b", r"\bwuna\b", r"\bcome\b", r"\bna so\b", r"\bwey\b", r"\bdon\b"),
}

CONFIRMATION_PATTERNS: tuple[str, ...] = (
    "oui", "exact", "c'est ça", "correct",
    "yes", "that's right", "exactly", "yeah", "yep",
    "na so", "true-true", "yes ooh", # Pidgin
)

REJECTION_PATTERNS: tuple[str, ...] = (
    "non", "pas ça", "plutôt", "autre", "différent",
    "no", "not that", "rather", "different", "nope",
    "no be", "no bi dat", "different", # Pidgin
)


def _score_from_raw(raw: int, max_score: int = 100) -> int:
    return min(max_score, 10 + raw * 30)


def _normalize(text: str) -> str:
    return text.lower().strip()


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zàâäéèêëïîôùûüç0-9']+", text.lower())


def _detect_language(text: str) -> str:
    lowered = text.lower()
    scores: dict[str, int] = {"fr": 0, "en": 0, "pcm": 0}
    for lang, patterns in LANGUAGE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lowered):
                scores[lang] += 1
    if scores["pcm"] >= scores["en"] and scores["pcm"] > 0:
        return "pcm"
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "fr"


def _detect_cities(text: str) -> list[dict[str, Any]]:
    lowered = text.lower()
    found: list[dict[str, Any]] = []
    for city, aliases in REGION_CITIES.items():
        for alias in aliases:
            if alias in lowered:
                found.append({"city": city.capitalize(), "match": alias, "region": None})
                break
    return found


def _detect_budget(text: str) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for match in BUDGET_PATTERN.finditer(text):
        raw = match.group(0)
        value = _parse_budget_value(raw)
        if value is not None:
            found.append({"raw": raw.strip(), "value": value, "currency": _detect_currency(raw)})
    return found


def _parse_budget_value(raw: str) -> int | None:
    raw = raw.strip()
    multiplier = 1
    if "million" in raw or "millions" in raw:
        multiplier = 1_000_000
        raw = raw.replace("million", "").replace("millions", "").strip()
    elif raw.endswith("M") or raw.endswith("m"):
        multiplier = 1_000_000
        raw = raw[:-1].strip()
    elif raw.upper().endswith("K") or raw.upper().endswith("KFCFA"):
        multiplier = 1_000
        raw = raw[:-1].strip() if raw.upper().endswith("K") else raw[:-5].strip()
    digits = re.sub(r"[^0-9]", "", raw)
    if not digits:
        return None
    return int(digits) * multiplier


def _detect_currency(raw: str) -> str:
    upper = raw.upper()
    if "EUR" in upper or "EURO" in upper:
        return "EUR"
    if "USD" in upper or "DOLLAR" in upper:
        return "USD"
    return "XAF"


def _detect_property_types(text: str) -> list[str]:
    lowered = text.lower()
    found: list[str] = []
    for ptype in PROPERTY_TYPES:
        if ptype in lowered and ptype not in found:
            found.append(ptype)
    return found


def _detect_surface(text: str) -> list[int]:
    return [int(m.group(1)) for m in SURFACE_PATTERN.finditer(text)]


def _detect_bedrooms(text: str) -> list[int]:
    results = [int(m.group(1)) for m in BEDROOM_PATTERN.finditer(text)]
    for m in TEXT_BEDROOM_PATTERN.finditer(text.lower()):
        word = m.group(1).lower()
        if word in TEXT_NUMBERS:
            results.append(TEXT_NUMBERS[word])
    return results


def _parse_context_for_text(text: str) -> dict[str, Any]:
    lowered = text.lower()
    entities: dict[str, Any] = {}
    cities = _detect_cities(text)
    if cities:
        entities["cities"] = cities
    budgets = _detect_budget(text)
    if budgets:
        entities["budgets"] = budgets
    property_types = _detect_property_types(text)
    if property_types:
        entities["property_types"] = property_types
    surfaces = _detect_surface(text)
    if surfaces:
        entities["surfaces_m2"] = surfaces
    bedrooms = _detect_bedrooms(text)
    if bedrooms:
        entities["bedrooms"] = bedrooms
    language = _detect_language(text)
    entities["lang"] = language
    is_confirmation = any(p in lowered for p in CONFIRMATION_PATTERNS)
    is_rejection = any(p in lowered for p in REJECTION_PATTERNS)
    if is_confirmation and not is_rejection:
        entities["confirmation"] = True
    elif is_rejection and not is_confirmation:
        entities["rejection"] = True
    else:
        entities["confirmation"] = None
    return entities


def _match_intent(intent_key: str, keywords: tuple[str, ...], tokens: list[str], normalized: str) -> dict[str, Any]:
    score = 0
    first_pos = len(normalized)
    for keyword in keywords:
        kw_tokens = _tokenize(keyword)
        if len(kw_tokens) == 1 and kw_tokens[0] in tokens:
            pos = normalized.find(kw_tokens[0])
            if pos >= 0 and pos < first_pos:
                first_pos = pos
            score += 1
        elif len(kw_tokens) > 1 and keyword in normalized:
            pos = normalized.find(keyword)
            if pos >= 0 and pos < first_pos:
                first_pos = pos
            score += 2
    return {"score": score, "first_pos": first_pos}


def _intent_priority(intent_key: str) -> int:
    """Higher priority = more specific intent. Generic intents have lower priority."""
    generic = {"find_property", "other", "manage"}
    return 0 if intent_key in generic else 1


def detect_intents(text: str) -> list[dict[str, Any]]:
    normalized = _normalize(text)
    tokens = _tokenize(normalized)
    detected: list[dict[str, Any]] = []

    for intent_key, keywords in SPECIFIC_INTENTS.items():
        match = _match_intent(intent_key, keywords, tokens, normalized)
        if match["score"] > 0:
            detected.append({
                "intent": intent_key,
                "score": _score_from_raw(match["score"]),
                "confidence": match["score"],
                "priority": _intent_priority(intent_key),
                "first_pos": match["first_pos"],
            })

    if not detected:
        for intent_key, keywords in GENERIC_INTENTS.items():
            match = _match_intent(intent_key, keywords, tokens, normalized)
            if match["score"] > 0:
                detected.append({
                    "intent": intent_key,
                    "score": _score_from_raw(match["score"]),
                    "confidence": match["score"],
                    "priority": _intent_priority(intent_key),
                    "first_pos": match["first_pos"],
                })

    detected.sort(key=lambda x: (x["priority"], x["confidence"], -x["first_pos"]), reverse=True)
    if not detected:
        detected.append({"intent": "other", "score": 50, "confidence": 1, "priority": 0, "first_pos": 999})
    return detected


def analyze_message(message: str) -> dict[str, Any]:
    intents = detect_intents(message)
    entities = _parse_context_for_text(message)
    primary = intents[0] if intents else {"intent": "other", "score": 50, "confidence": 1}
    return {
        "intents": intents,
        "primary_intent": primary["intent"],
        "primary_score": primary["score"],
        "is_multi_intent": len([i for i in intents if i["confidence"] > 0]) > 1,
        "entities": entities,
        "language": entities.get("lang", "fr"),
        "is_confirmation": entities.get("confirmation"),
        "is_rejection": entities.get("rejection"),
        "raw_message": message,
    }


class IntentEngine:
    def analyze(self, message: str) -> dict[str, Any]:
        return analyze_message(message)

    def detect_language(self, message: str) -> str:
        return _detect_language(message)

    def is_confirmation(self, message: str) -> bool | None:
        lowered = message.lower()
        has_confirmation = any(p in lowered for p in CONFIRMATION_PATTERNS)
        has_rejection = any(p in lowered for p in REJECTION_PATTERNS)
        if has_confirmation and not has_rejection:
            return True
        if has_rejection and not has_confirmation:
            return False
        return None

    def extract_entities(self, message: str) -> dict[str, Any]:
        return _parse_context_for_text(message)
