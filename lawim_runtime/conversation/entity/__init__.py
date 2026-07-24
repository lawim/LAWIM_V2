from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EntityResult:
    entities: dict[str, Any] = field(default_factory=dict)
    missing: list[str] = field(default_factory=list)
    raw_text: str = ""


FRENCH_NUMBERS = {
    "z\u00e9ro": 0, "un": 1, "une": 1, "deux": 2, "trois": 3, "quatre": 4,
    "cinq": 5, "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
    "onze": 11, "douze": 12, "treize": 13, "quatorze": 14, "quinze": 15,
}

PROPERTY_TYPES = {
    "appartement": "apartment", "appart": "apartment", "studio": "studio",
    "maison": "house", "villa": "villa", "terrain": "land", "bureau": "office",
    "local": "commercial", "entrep\u00f4t": "warehouse", "duplex": "duplex",
}

TRANSACTION_TYPES = {
    "location": "rent", "louer": "rent", "achat": "buy", "acheter": "buy",
    "vente": "sell", "vendre": "sell", "investir": "invest",
}

CITIES = {"yaound\u00e9": "Yaounde", "douala": "Douala", "bafoussam": "Bafoussam",
          "kribi": "Kribi", "limb\u00e9": "Limbe"}

DISTRICTS = {"mvan": "Mvan", "bastos": "Bastos", "odza": "Odza", "nlongkak": "Nlongkak",
             "tsinga": "Tsinga", "ngousso": "Ngousso", "essos": "Essos",
             "mendong": "Mendong", "biyem-assi": "Biyem-Assi", "biyem assi": "Biyem-Assi",
             "makepe": "Makepe", "bonanjo": "Bonanjo", "bonamoussadi": "Bonamoussadi",
             "akwa": "Akwa"}


class EntityExtractionEngine:

    def extract(self, text: str) -> EntityResult:
        result = EntityResult(raw_text=text)
        if not text:
            return result
        lower = text.lower()

        # Property type
        for fr, en in PROPERTY_TYPES.items():
            if fr in lower:
                result.entities["property_type"] = en
                break

        # Transaction type
        for fr, en in TRANSACTION_TYPES.items():
            if fr in lower:
                result.entities["transaction_type"] = en
                break

        # City
        for fr_key, en_val in CITIES.items():
            if fr_key in lower:
                result.entities["city"] = en_val
                break

        # District
        for fr_key, en_val in DISTRICTS.items():
            if fr_key in lower:
                result.entities["district"] = en_val
                break

        # Budget
        budget = self._extract_budget(text)
        if budget:
            result.entities["budget_max"] = budget

        # Bedrooms
        bedrooms = self._extract_bedrooms(text)
        if bedrooms:
            result.entities["bedrooms"] = bedrooms

        # Determine missing info
        if "property_type" not in result.entities:
            result.missing.append("property_type")
        if "city" not in result.entities:
            result.missing.append("city")
        if "transaction_type" not in result.entities:
            result.missing.append("transaction_type")

        return result

    def _extract_budget(self, text: str) -> int | None:
        patterns = [
            (r"(\d[\d\s]*)\s*(?:FCFA|fcfa|francs?|f\s*cfa|xaf|F)", 1),
            (r"(\d[\d\s]*)\s*(?:euros?|\u20ac|usd|\$)", 1),
            (r"(\d[\d\s]*)\s*(?:k|mille)", 1000),
            (r"(?:budget|prix|jusqu['\u2019]?[a\u00e0]?|maximum|max|montant)\s*(?:de\s*)?(\d[\d\s]*)(?!\s*(?:ans|mois|jours?|heures?))", 1),
        ]
        for pat, multiplier in patterns:
            m = re.search(pat, text)
            if m:
                cleaned = m.group(1).replace(" ", "")
                try:
                    return int(cleaned) * multiplier
                except ValueError:
                    pass
        amt_words = re.search(r"(?:deux|trois|quatre|cinq|six|sept|huit|neuf)\s*(?:cents?\s*)?mille", text)
        if amt_words:
            return 100_000
        return None

    def _extract_bedrooms(self, text: str) -> int | None:
        m = re.search(r"(\d+)\s*(?:chambres?|pi[e\u00e8]ces?)", text)
        if m:
            return int(m.group(1))
        for word, num in FRENCH_NUMBERS.items():
            pat = rf"{word}\s*(?:chambres?|pi[e\u00e8]ces?)"
            if re.search(pat, text, re.IGNORECASE):
                return num
        return None
