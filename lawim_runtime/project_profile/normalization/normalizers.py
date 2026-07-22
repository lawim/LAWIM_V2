from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizationResult:
    normalized_value: Any = None
    raw_value: str = ""
    success: bool = True


class MoneyNormalizer:
    def normalize(self, raw: str) -> NormalizationResult:
        text = raw.lower().strip()
        text = re.sub(r"(fcf\s*a|francs|cfa|xaf)\s*$", "", text, flags=re.IGNORECASE).strip()
        text = re.sub(r"mille", "000", text)
        text = re.sub(r"[\s.]", "", text)
        word_map: dict[str, str] = {"cent": "00", "cinq": "500", "dix": "10"}
        for word, replacement in word_map.items():
            if text == word:
                text = replacement
                break
        try:
            val = int(text)
            return NormalizationResult(normalized_value=val, raw_value=raw, success=True)
        except ValueError:
            return NormalizationResult(normalized_value=None, raw_value=raw, success=False)


class CityNormalizer:
    MAP: dict[str, str] = {
        "yaounde": "Yaoundé",
        "douala": "Douala",
        "bafoussam": "Bafoussam",
        "bamenda": "Bamenda",
        "garoua": "Garoua",
        "maroua": "Maroua",
        "nkongsamba": "Nkongsamba",
        "kribi": "Kribi",
        "limbe": "Limbe",
        "buea": "Buea",
    }

    def normalize(self, raw: str) -> NormalizationResult:
        key = raw.lower().strip()
        val = self.MAP.get(key)
        if val:
            return NormalizationResult(normalized_value=val, raw_value=raw, success=True)
        return NormalizationResult(normalized_value=raw.title(), raw_value=raw, success=True)


class DistrictNormalizer:
    MAP: dict[str, str] = {
        "biyem assi": "Biyem-Assi",
        "biyemassi": "Biyem-Assi",
        "bonamoussadi": "Bonamoussadi",
        "makepe": "Makepe",
        "bastos": "Bastos",
        "mendong": "Mendong",
        "akwa": "Akwa",
        "bonanjo": "Bonanjo",
        "bonapriso": "Bonapriso",
        "deido": "Deido",
        "ndokoti": "Nkoti",
        "bassa": "Bassa",
        "logbaba": "Logbaba",
        "bepanda": "Bepanda",
        "nkolbisson": "Nkolbisson",
        "omnisports": "Omnisports",
        "tsinga": "Tsinga",
        "mfoundi": "Mfoundi",
    }

    def normalize(self, raw: str) -> NormalizationResult:
        key = raw.lower().strip()
        val = self.MAP.get(key)
        if val:
            return NormalizationResult(normalized_value=val, raw_value=raw, success=True)
        return NormalizationResult(normalized_value=raw.title(), raw_value=raw, success=True)


class PropertyTypeNormalizer:
    MAP: dict[str, str] = {
        "appartement": "APARTMENT",
        "appt": "APARTMENT",
        "apartment": "APARTMENT",
        "studio": "STUDIO",
        "maison": "HOUSE",
        "house": "HOUSE",
        "villa": "VILLA",
        "terrain": "LAND",
        "land": "LAND",
        "bureau": "OFFICE",
        "office": "OFFICE",
        "local": "COMMERCIAL",
        "commercial": "COMMERCIAL",
        "entrepôt": "WAREHOUSE",
        "entrepot": "WAREHOUSE",
        "garage": "GARAGE",
        "parking": "PARKING",
    }

    def normalize(self, raw: str) -> NormalizationResult:
        key = raw.lower().strip()
        val = self.MAP.get(key)
        if val:
            return NormalizationResult(normalized_value=val, raw_value=raw, success=True)
        return NormalizationResult(normalized_value=raw.upper(), raw_value=raw, success=True)


class BooleanNormalizer:
    TRUE_VALUES: set[str] = {
        "oui", "yes", "yeah", "d'accord", "d accord", "ok",
        "meublé", "meuble", "furnished", "vrai", "true", "1",
    }
    FALSE_VALUES: set[str] = {
        "non", "no", "nope",
        "pas meublé", "pas meuble", "non meublé", "non meuble",
        "vide", "unfurnished", "faux", "false", "0",
    }

    def normalize(self, raw: str) -> NormalizationResult:
        key = raw.lower().strip()
        if key in self.TRUE_VALUES:
            return NormalizationResult(normalized_value=True, raw_value=raw, success=True)
        if key in self.FALSE_VALUES:
            return NormalizationResult(normalized_value=False, raw_value=raw, success=True)
        return NormalizationResult(normalized_value=None, raw_value=raw, success=False)
