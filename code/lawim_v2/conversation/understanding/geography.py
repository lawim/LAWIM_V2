from __future__ import annotations

from dataclasses import dataclass
from typing import Any


HIERARCHY: dict[str, dict[str, Any]] = {
    "cameroon": {
        "type": "country",
        "regions": {
            "littoral": {
                "type": "region",
                "cities": {
                    "douala": {
                        "type": "city",
                        "districts": {
                            "douala 1": {"type": "district"},
                            "douala 2": {"type": "district"},
                            "douala 3": {"type": "district"},
                            "douala 4": {"type": "district"},
                            "douala 5": {"type": "district"},
                            "douala 6": {"type": "district"},
                        },
                        "neighborhoods": {
                            "makepe": {"type": "neighborhood"},
                            "bonamoussadi": {"type": "neighborhood"},
                            "akwa": {"type": "neighborhood"},
                            "bonapriso": {"type": "neighborhood"},
                            "bonanjo": {"type": "neighborhood"},
                            "deido": {"type": "neighborhood"},
                            "bali": {"type": "neighborhood"},
                            "ndogpassi": {"type": "neighborhood"},
                            "ndokoti": {"type": "neighborhood"},
                            "new bell": {"type": "neighborhood"},
                            "bonaberi": {"type": "neighborhood"},
                            "logbaba": {"type": "neighborhood"},
                            "kotto": {"type": "neighborhood"},
                            "bonadibong": {"type": "neighborhood"},
                            "ndogbong": {"type": "neighborhood"},
                            "bonamikano": {"type": "neighborhood"},
                        },
                    }
                },
            },
            "centre": {
                "type": "region",
                "cities": {
                    "yaounde": {
                        "type": "city",
                        "neighborhoods": {
                            "odza": {"type": "neighborhood"},
                            "bastos": {"type": "neighborhood"},
                            "mvan": {"type": "neighborhood"},
                            "mendong": {"type": "neighborhood"},
                            "mokolo": {"type": "neighborhood"},
                            "nlongkak": {"type": "neighborhood"},
                            "omnisport": {"type": "neighborhood"},
                            "mfoundi": {"type": "neighborhood"},
                            "ngousso": {"type": "neighborhood"},
                            "briqueterie": {"type": "neighborhood"},
                            "ekounou": {"type": "neighborhood"},
                            "nkolbisson": {"type": "neighborhood"},
                            "nkoabang": {"type": "neighborhood"},
                            "nsimeyong": {"type": "neighborhood"},
                            "messassi": {"type": "neighborhood"},
                            "essos": {"type": "neighborhood"},
                            "mvog-mbi": {"type": "neighborhood"},
                            "biyem-assi": {"type": "neighborhood"},
                        },
                    }
                },
            },
        },
    },
}

KNOWN_CITIES: dict[str, str] = {
    "douala": "Douala",
    "yaounde": "Yaoundé",
    "garoua": "Garoua",
    "bafoussam": "Bafoussam",
    "bamenda": "Bamenda",
    "maroua": "Maroua",
    "nkongsamba": "Nkongsamba",
    "kumba": "Kumba",
    "limbe": "Limbe",
    "buea": "Buéa",
    "ebolowa": "Ebolowa",
    "sangmelima": "Sangmélima",
    "bertoua": "Bertoua",
    "ngaoundere": "Ngaoundéré",
    "mbalmayo": "Mbalmayo",
    "edea": "Edéa",
    "kribi": "Kribi",
    "foumban": "Foumban",
    "dchang": "Dschang",
    "bafang": "Bafang",
    "mbouda": "Mbouda",
    "yagoua": "Yagoua",
    "kaele": "Kaélé",
    "tibati": "Tibati",
    "mora": "Mora",
    "mokolo": "Mokolo",
    "bogo": "Bogo",
}

KNOWN_NEIGHBORHOODS: dict[str, str] = {
    "makepe": "Makepe",
    "bonamoussadi": "Bonamoussadi",
    "akwa": "Akwa",
    "bonapriso": "Bonapriso",
    "bonanjo": "Bonanjo",
    "deido": "Deïdo",
    "bali": "Bali",
    "ndogpassi": "Ndogpassi",
    "ndokoti": "Ndogbong",
    "new bell": "New Bell",
    "bonaberi": "Bonabéri",
    "logbaba": "Logbaba",
    "kotto": "Kotto",
    "odza": "Odza",
    "bastos": "Bastos",
    "mvan": "Mvan",
    "mendong": "Mendong",
    "mokolo": "Mokolo",
    "nlongkak": "Nlongkak",
    "omnisport": "Omnisport",
    "mfoundi": "Mfoundi",
    "ngousso": "Ngousso",
    "briqueterie": "Briqueterie",
    "ekounou": "Ekounou",
    "nkolbisson": "Nkolbisson",
}

NEIGHBORHOOD_TO_CITY: dict[str, str] = {
    "makepe": "Douala",
    "bonamoussadi": "Douala",
    "akwa": "Douala",
    "bonapriso": "Douala",
    "bonanjo": "Douala",
    "deido": "Douala",
    "bali": "Douala",
    "ndogpassi": "Douala",
    "ndokoti": "Douala",
    "new bell": "Douala",
    "bonaberi": "Douala",
    "logbaba": "Douala",
    "kotto": "Douala",
    "odza": "Yaoundé",
    "bastos": "Yaoundé",
    "mvan": "Yaoundé",
    "mendong": "Yaoundé",
    "mokolo": "Yaoundé",
    "nlongkak": "Yaoundé",
    "omnisport": "Yaoundé",
    "mfoundi": "Yaoundé",
    "ngousso": "Yaoundé",
    "briqueterie": "Yaoundé",
    "ekounou": "Yaoundé",
    "nkolbisson": "Yaoundé",
}

CITY_TO_REGION: dict[str, str] = {
    "Douala": "Littoral",
    "Yaoundé": "Centre",
    "Garoua": "Nord",
    "Bafoussam": "Ouest",
    "Bamenda": "Nord-Ouest",
    "Maroua": "Extrême-Nord",
    "Nkongsamba": "Littoral",
    "Kumba": "Sud-Ouest",
    "Limbe": "Sud-Ouest",
    "Buéa": "Sud-Ouest",
    "Ebolowa": "Sud",
    "Sangmélima": "Sud",
    "Bertoua": "Est",
    "Ngaoundéré": "Adamaoua",
    "Bafang": "Ouest",
    "Foumban": "Ouest",
    "Dschang": "Ouest",
}


@dataclass
class GeoResult:
    raw_value: str
    normalized_value: str | None = None
    match_type: str | None = None
    city: str | None = None
    region: str | None = None
    country: str = "Cameroun"
    confidence: float = 0.0
    is_foreign: bool = False
    ambiguity: bool = False

    def to_fact_dict(self) -> dict:
        return {
            "raw_value": self.raw_value,
            "normalized_value": self.normalized_value,
            "match_type": self.match_type,
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "confidence": self.confidence,
            "is_foreign": self.is_foreign,
        }


def normalize_location(raw: str) -> GeoResult:
    cleaned = raw.strip().lower()

    if cleaned in KNOWN_NEIGHBORHOODS:
        normalized = KNOWN_NEIGHBORHOODS[cleaned]
        city = NEIGHBORHOOD_TO_CITY[cleaned]
        region = CITY_TO_REGION.get(city)
        return GeoResult(
            raw_value=raw,
            normalized_value=normalized,
            match_type="neighborhood",
            city=city,
            region=region,
            confidence=0.9,
        )

    if cleaned in KNOWN_CITIES:
        normalized = KNOWN_CITIES[cleaned]
        region = CITY_TO_REGION.get(normalized)
        return GeoResult(
            raw_value=raw,
            normalized_value=normalized,
            match_type="city",
            city=normalized,
            region=region,
            confidence=1.0,
        )

    if cleaned in NEIGHBORHOOD_TO_CITY:
        normalized = KNOWN_NEIGHBORHOODS.get(cleaned, cleaned.capitalize())
        city = NEIGHBORHOOD_TO_CITY[cleaned]
        return GeoResult(
            raw_value=raw,
            normalized_value=normalized,
            match_type="neighborhood",
            city=city,
            confidence=0.8,
        )

    if cleaned in CITY_TO_REGION:
        return GeoResult(
            raw_value=raw,
            normalized_value=cleaned.capitalize(),
            match_type="city",
            city=cleaned.capitalize(),
            region=CITY_TO_REGION[cleaned],
            confidence=1.0,
        )

    return GeoResult(
        raw_value=raw,
        match_type="unknown",
        confidence=0.0,
        ambiguity=True,
    )
