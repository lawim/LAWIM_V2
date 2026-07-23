from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

PROPERTY_TYPES: dict[str, str] = {
    "studio": "STUDIO",
    "appartement": "APARTMENT",
    "appart": "APARTMENT",
    "duplex": "APARTMENT",
    "tdb": "APARTMENT",
    "tout doux beau": "APARTMENT",
    "maison": "HOUSE",
    "maison basse": "HOUSE",
    "maisonette": "HOUSE",
    "villa": "VILLA",
    "immeuble": "BUILDING",
    "terrain": "LAND",
    "parcelle": "LAND",
    "terrain nu": "LAND",
    "bureau": "COMMERCIAL",
    "local commercial": "COMMERCIAL",
    "magasin": "COMMERCIAL",
    "entrepot": "COMMERCIAL",
    "entrepôt": "COMMERCIAL",
    "garage": "COMMERCIAL",
    "chambre": "ROOM",
    "chambre a louer": "ROOM",
    "chambre meublee": "ROOM",
    "chambre meublée": "ROOM",
    "studio meuble": "STUDIO",
    "studios": "STUDIO",
    "appartements": "APARTMENT",
    "maisons": "HOUSE",
    "villas": "VILLA",
    "terrains": "LAND",
}

TRANSACTION_TYPES: dict[str, str] = {
    "acheter": "BUY",
    "achat": "BUY",
    "acquerir": "BUY",
    "acquérir": "BUY",
    "investir": "BUY",
    "louer": "RENT",
    "location": "RENT",
    "prendre en location": "RENT",
    "vendre": "SELL",
    "vente": "SELL",
    "mettre en location": "RENT_OUT",
    "louer mon bien": "RENT_OUT",
    "construire": "CONSTRUCT",
    "construction": "CONSTRUCT",
    "batir": "CONSTRUCT",
    "bâtir": "CONSTRUCT",
    "renover": "RENOVATE",
    "rénover": "RENOVATE",
}


@dataclass
class PropertyTypeResult:
    raw_value: str
    normalized_type: str | None = None
    confidence: float = 1.0

    def to_fact_dict(self) -> dict[str, Any]:
        return {
            "raw_value": self.raw_value,
            "normalized_type": self.normalized_type,
            "confidence": self.confidence,
        }


@dataclass
class TransactionTypeResult:
    raw_value: str
    normalized_type: str | None = None
    confidence: float = 1.0

    def to_fact_dict(self) -> dict[str, Any]:
        return {
            "raw_value": self.raw_value,
            "normalized_type": self.normalized_type,
            "confidence": self.confidence,
        }


def normalize_property_type(raw: str) -> PropertyTypeResult:
    cleaned = raw.strip().lower()
    if cleaned in PROPERTY_TYPES:
        return PropertyTypeResult(
            raw_value=raw,
            normalized_type=PROPERTY_TYPES[cleaned],
        )

    for key, value in PROPERTY_TYPES.items():
        if key in cleaned or cleaned in key:
            if key in ("chambre", "chambre meublee", "chambre meublée", "chambre a louer"):
                if re.search(r'\b(\d+|deux|trois|quatre|cinq|six|sept|huit|neuf|dix)\s+chambres?\b', cleaned):
                    continue

            return PropertyTypeResult(
                raw_value=raw,
                normalized_type=value,
                confidence=0.8,
            )

    return PropertyTypeResult(
        raw_value=raw,
        confidence=0.0,
    )


def normalize_transaction_type(raw: str) -> TransactionTypeResult:
    cleaned = raw.strip().lower()

    if cleaned in TRANSACTION_TYPES:
        return TransactionTypeResult(
            raw_value=raw,
            normalized_type=TRANSACTION_TYPES[cleaned],
        )

    for word in cleaned.split():
        if word in TRANSACTION_TYPES:
            return TransactionTypeResult(
                raw_value=raw,
                normalized_type=TRANSACTION_TYPES[word],
                confidence=0.8,
            )

    return TransactionTypeResult(
        raw_value=raw,
        confidence=0.0,
    )
