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
    "appartement": "apartment", "appart": "apartment",
    "studio": "studio",
    "maison": "house", "villa": "villa",
    "terrain": "land", "bureau": "office",
    "local": "commercial", "entrep\u00f4t": "warehouse", "duplex": "duplex",
    # English
    "house": "house", "apartment": "apartment", "flat": "apartment",
    "land": "land", "plot": "land", "office": "office",
    "commercial": "commercial", "warehouse": "warehouse", "building": "building",
    "shop": "commercial", "store": "commercial",
    # Pidgin (avoid "room" which falsely matches "bedroom")
    "shop place": "commercial",
    "self-contained": "studio",
}

TRANSACTION_TYPES = {
    "location": "rent", "louer": "rent", "achat": "buy", "acheter": "buy",
    "vente": "sell", "vendre": "sell", "investir": "invest",
    # English
    "rent": "rent", "buy": "buy", "sell": "sell", "purchase": "buy",
    "lease": "rent", "for rent": "rent", "for sale": "sell", "for buy": "buy",
    # Pidgin
    "na rent": "rent", "na buy": "buy", "make i rent": "rent",
    "wan rent": "rent", "wan buy": "buy",
}

CITIES = {"yaound\u00e9": "Yaounde", "yaounde": "Yaounde", "douala": "Douala", "bafoussam": "Bafoussam",
          "bafang": "Bafang", "bamenda": "Bamenda", "buea": "Buea",
          "limbe": "Limbe", "limb\u00e9": "Limbe", "kribi": "Kribi", "ebolowa": "Ebolowa",
          "bertoua": "Bertoua", "garoua": "Garoua", "maroua": "Maroua",
          "ngaound\u00e9r\u00e9": "Ngaoundere", "ngaoundere": "Ngaoundere",
          "mbalmayo": "Mbalmayo", "ed\u00e9a": "Edea", "edea": "Edea",
          "nkongsamba": "Nkongsamba", "foumban": "Foumban", "dschang": "Dschang",
          "kumba": "Kumba", "sangm\u00e9lima": "Sangmelima", "sangmelima": "Sangmelima"}

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

        # Property type (check longest keys first to avoid substring false matches)
        sorted_pt = sorted(PROPERTY_TYPES.items(), key=lambda x: -len(x[0]))
        for fr, en in sorted_pt:
            if fr in lower:
                result.entities["property_type"] = en
                break

        # Transaction type (check longest keys first)
        sorted_tt = sorted(TRANSACTION_TYPES.items(), key=lambda x: -len(x[0]))
        for fr, en in sorted_tt:
            if fr in lower:
                result.entities["transaction_type"] = en
                break

        # City — try known cities first
        for fr_key, en_val in CITIES.items():
            if fr_key in lower:
                result.entities["city"] = en_val
                break
        if "city" not in result.entities:
            # Try "à Paris" or "in Limbe" patterns — but filter non-city terms
            city_fallback = re.search(r"\b(?:à|a|in)\s+([A-Za-z\u00C0-\u024F]{3,})", text)
            if city_fallback:
                raw = city_fallback.group(1)
                raw_lower = raw.lower()
                # Reject if it's a known non-city word
                NON_CITIES = {"house","apartment","studio","villa","land","plot","office","commercial",
                "space","warehouse","modern","room","person","owner","property","building","shop",
                "flat","store","home","rent","buy","sale","need","want","look","find","search",
                "town","city","place","area","zone","sector","quarter","neighborhood","region",
                "this","that","these","those","some","any","every","each","both","all","few",
                "many","much","more","less","most","least","here","there","where","what","which",
                "your","their","our","its","his","her","our","my","your","good","nice","best",
                "new","old","big","small","large","small","great","real","first","last","next","same",
                "living","dining","bath","kitchen","bedroom","bedrooms","balcony","terrace","garden",
                "yard","garage","parking","basement","attic","entrance","exit","door","window",
                "floor","level","storey","office","workspace","studio","loft","cellar"}
                # Also skip known districts to avoid city/district confusion
                known_districts = {k.lower() for k in DISTRICTS}
                if raw_lower in NON_CITIES or raw_lower in known_districts:
                    pass  # Don't extract non-cities or districts as cities
                else:
                    result.entities["city"] = raw[0].upper() + raw[1:]
                    result.entities["city_raw"] = raw
        if "city" not in result.entities:
            # Try matching after known French prepositions for city context
            city_fallback2 = re.search(r"\b(?:ville\s+de|pres\s+de|a\s+cote\s+de|dans\s+(?:le\s+)?)\s*([A-Za-z\u00C0-\u024F]{3,})", text)
            if city_fallback2:
                raw = city_fallback2.group(1)
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
            (r"(\d[\d\s]*)\s*(?:k|mille|thousand|thousands)(?:\s*FCFA|\s*francs?|\s*fcfa)?", 1000),
            (r"(?:budget|prix|jusqu['\u2019]?[a\u00e0]?|maximum|max|montant|ma budget|ma budget na|ma money)\s*(?:de\s*)?(\d[\d\s]*)(?!\s*(?:ans|mois|jours?|heures?|years?|months?))", 1),
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
        m = re.search(r"(\d+)\s*(?:chambres?|pi[e\u00e8]ces?|bedrooms?|rooms?)", text)
        if m:
            return int(m.group(1))
        # English/Pidgin: "two bedroom", "three rooms"
        for word, num in FRENCH_NUMBERS.items():
            pat = rf"{word}\s*(?:chambres?|pi[e\u00e8]ces?|bedrooms?|rooms?)"
            if re.search(pat, text, re.IGNORECASE):
                return num
        # "one bedroom", "two-bedroom"
        for eng_word in [("one",1),("two",2),("three",3),("four",4),("five",5),("six",6)]:
            pat = rf"{eng_word[0]}[\s-]?(?:bedroom|room)"
            if re.search(pat, text, re.IGNORECASE):
                return eng_word[1]
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
