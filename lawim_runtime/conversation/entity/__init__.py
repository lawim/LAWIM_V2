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

CITIES = {"yaound\u00e9": "Yaounde", "yaounde": "Yaounde", "douala": "Douala", "bafoussam": "Bafoussam",
          "kribi": "Kribi", "limb\u00e9": "Limbe"}

DISTRICTS = {"mvan": "Mvan", "bastos": "Bastos", "odza": "Odza", "nlongkak": "Nlongkak",
             "tsinga": "Tsinga", "ngousso": "Ngousso", "essos": "Essos",
             "mendong": "Mendong", "biyem-assi": "Biyem-Assi", "biyem assi": "Biyem-Assi",
             "makepe": "Makepe", "bonanjo": "Bonanjo", "bonamoussadi": "Bonamoussadi",
             "akwa": "Akwa", "melen": "Melen", "ngoa": "Ngoa",
             "ngoa-ekellé": "Ngoa-Ekellé", "ngoa-ekelle": "Ngoa-Ekellé",
             "ekoumdoum": "Ekoumdoum", "mokolo": "Mokolo", "mimboman": "Mimboman",
             "nyalla": "Nyalla", "carrière": "Carrière", "carriere": "Carrière"}


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

        # City — try known cities first, then accept any capitalized word after "à"
        for fr_key, en_val in CITIES.items():
            if fr_key in lower:
                result.entities["city"] = en_val
                break
        if "city" not in result.entities:
            # Fallback: capture any word after "à" as city
            city_fallback = re.search(r"\ba\s+([A-Za-z\u00C0-\u024F][A-Za-z\u00C0-\u024F]+)", text)
            if city_fallback:
                raw = city_fallback.group(1)
                # Capitalize first letter
                result.entities["city"] = raw[0].upper() + raw[1:]
                result.entities["city_raw"] = raw

        # District
        for fr_key, en_val in DISTRICTS.items():
            if fr_key in lower:
                result.entities["district"] = en_val
                break

        # Preferred areas (multiple)
        preferred = self._extract_preferred_areas(text)
        if preferred:
            result.entities["preferred_areas"] = preferred

        # Budget
        budget = self._extract_budget(text)
        if budget:
            result.entities["budget_max"] = budget

        # Bedrooms
        bedrooms = self._extract_bedrooms(text)
        if bedrooms:
            result.entities["bedrooms"] = bedrooms

        # Move-in date
        move_in = self._extract_move_in_date(text)
        if move_in:
            result.entities["move_in_date"] = move_in

        # Determine missing info
        if "property_type" not in result.entities:
            result.missing.append("property_type")
        if "city" not in result.entities:
            result.missing.append("city")
        if "transaction_type" not in result.entities:
            result.missing.append("transaction_type")
        # Studio doesn't require bedrooms
        if result.entities.get("property_type") == "studio":
            result.missing = [m for m in result.missing if m != "bedrooms"]

        return result

    def _extract_budget(self, text: str) -> int | None:
        patterns = [
            (r"(\d[\d\s]*)\s*(?:millions?\s*(?:FCFA|fcfa|francs?)?)", 1_000_000),
            (r"(\d[\d\s]*)\s*(?:milliards?\s*(?:FCFA|fcfa|francs?)?)", 1_000_000_000),
            (r"(\d[\d\s]*)\s*(?:FCFA|fcfa|francs?|f\s*cfa|xaf|F)", 1),
            (r"(\d[\d\s]*)\s*(?:euros?|\u20ac|usd|\$)", 1),
            (r"(\d[\d\s]*)\s*(?:k|mille)(?:\s*FCFA|\s*fcfa|\s*francs?)?", 1000),
            (r"(?:budget|prix|jusqu['\u2019]?[a\u00e0]?|maximum|max|montant)\s*(?:de\s*)?(\d[\d\s]*)(?!\s*(?:ans|mois|jours?|heures?))", 1),
            (r"\b(\d{1,3}(?:\s\d{3})+)\b", 1),
        ]
        for pat, multiplier in patterns:
            m = re.search(pat, text)
            if m:
                cleaned = m.group(1).replace(" ", "")
                try:
                    return int(cleaned) * multiplier
                except ValueError:
                    pass
        # Word patterns for "mille" without digits
        amt_words = re.search(r"(\d+)\s*(?:cents?\s*)?mille", text)
        if amt_words:
            return int(amt_words.group(1)) * 1000
        amt_million = re.search(r"(?:deux|trois|quatre|cinq|six|sept|huit|neuf)\s*(?:cents?\s*)?(?:millions?|milliards?)", text)
        if amt_million:
            return 100_000_000
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

    FRENCH_MONTHS = r"(janvier|f\u00e9vrier|fevrier|mars|avril|mai|juin|juillet|ao\u00fbt|aout|septembre|octobre|novembre|d\u00e9cembre|decembre)"

    def _extract_move_in_date(self, text: str) -> str | None:
        patterns = [
            re.compile(rf"(?:pour|en|d\u00e8s|des|dans|d\u2019ici|avant)\s+(?:le\s+)?(?:mois\s+de\s+)?{self.FRENCH_MONTHS}(?:\s*\d{{4}})?(?:\b|$|\.|,)", re.IGNORECASE),
            re.compile(rf"(?:rentr\u00e9e?|entrer?|emm\u00e9nager?|commencer)\s+(?:d\u00e8s\s+|en\s+|pour\s+)?{self.FRENCH_MONTHS}(?:\s*\d{{4}})?(?:\b|$|\.|,)", re.IGNORECASE),
            re.compile(rf"\b{self.FRENCH_MONTHS}(?:\s*\d{{4}})?(?:\b|$|\.|,)", re.IGNORECASE),
        ]
        for pat in patterns:
            m = pat.search(text)
            if m:
                return m.group(0).strip()
        return None

    def _extract_preferred_areas(self, text: str) -> list[str] | None:
        lower = text.lower()
        known = sorted(
            [(k.lower(), v) for k, v in DISTRICTS.items()],
            key=lambda x: -len(x[0])
        )
        found: list[str] = []
        matched_regions: list[str] = []
        for raw_key, display_name in known:
            if raw_key in lower:
                # Avoid matching substrings already covered by longer matches
                already_covered = any(raw_key in mr for mr in matched_regions)
                if not already_covered:
                    found.append(display_name)
                    matched_regions.append(raw_key)
        if len(found) >= 2:
            return found
        return None
