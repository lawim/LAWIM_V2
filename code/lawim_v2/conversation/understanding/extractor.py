from __future__ import annotations

import re
from typing import Any

from .geography import (
    normalize_location, KNOWN_NEIGHBORHOODS, KNOWN_CITIES,
    NEIGHBORHOOD_TO_CITY, CITY_TO_REGION,
)
from .money import normalize_amount
from .dates import normalize_date
from .property_types import normalize_property_type, normalize_transaction_type


def _scan_location(text: str) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    lower = text.lower()
    words = set(lower.split())
    multi_word = {"new bell", "tout doux beau"}

    for multi in multi_word:
        if multi in lower:
            words.add(multi)

    for word in words:
        if word in KNOWN_NEIGHBORHOODS:
            city = NEIGHBORHOOD_TO_CITY[word]
            region = CITY_TO_REGION.get(city)
            results.append({
                "field": "neighborhood", "raw_value": word,
                "normalized_value": KNOWN_NEIGHBORHOODS[word],
                "confidence": 0.9, "source_type": "inferred",
            })
            results.append({
                "field": "city", "raw_value": city,
                "normalized_value": city, "confidence": 0.9,
                "source_type": "inferred",
            })
            if region:
                results.append({
                    "field": "region", "raw_value": region,
                    "normalized_value": region, "confidence": 0.8,
                    "source_type": "inferred",
                })
        elif word in KNOWN_CITIES:
            city = KNOWN_CITIES[word]
            region = CITY_TO_REGION.get(city)
            results.append({
                "field": "city", "raw_value": word,
                "normalized_value": city, "confidence": 1.0,
                "source_type": "explicit",
            })
            if region:
                results.append({
                    "field": "region", "raw_value": region,
                    "normalized_value": region, "confidence": 0.9,
                    "source_type": "inferred",
                })
    return results


def extract_all(text: str) -> dict[str, Any]:
    results: dict[str, Any] = {
        "facts": [],
        "ambiguous": [],
    }

    # Scan for location keywords within text
    location_facts = _scan_location(text)
    for fact in location_facts:
        results["facts"].append(fact)

    surface = _extract_surface(text)
    if surface:
        results["facts"].append(surface)

    amount = normalize_amount(text)
    if amount.confidence > 0 and not amount.ambiguity:
        results["facts"].append({
            "field": "budget_max" if "acheter" in text.lower() or "buy" in text.lower()
                       else "budget" if "louer" in text.lower() or "rent" in text.lower()
                       else "budget_max",
            "raw_value": amount.raw_value,
            "normalized_value": amount.normalized_amount,
            "currency": amount.currency,
            "confidence": amount.confidence,
            "source_type": "explicit",
            "unit": amount.currency,
        })
    elif amount.ambiguity:
        results["ambiguous"].append({
            "field": "budget",
            "raw_value": amount.raw_value,
            "ambiguity_reason": amount.ambiguity_reason,
            "possible_values": amount.possible_values,
        })

    date = normalize_date(text)
    if date.confidence > 0 and not date.ambiguity:
        results["facts"].append({
            "field": "deadline",
            "raw_value": date.raw_value,
            "normalized_value": date.normalized_date,
            "confidence": date.confidence,
            "precision": date.precision,
            "source_type": "explicit",
        })
    elif date.ambiguity:
        results["ambiguous"].append({
            "field": "deadline",
            "raw_value": date.raw_value,
            "ambiguity": True,
        })

    prop = normalize_property_type(text)
    if prop.confidence > 0.3:
        results["facts"].append({
            "field": "property_type",
            "raw_value": prop.raw_value,
            "normalized_value": prop.normalized_type,
            "confidence": prop.confidence,
            "source_type": "explicit" if prop.confidence >= 1.0 else "inferred",
        })

    trans = normalize_transaction_type(text)
    if trans.confidence > 0.3:
        results["facts"].append({
            "field": "transaction_type",
            "raw_value": trans.raw_value,
            "normalized_value": trans.normalized_type,
            "confidence": trans.confidence,
            "source_type": "explicit" if trans.confidence >= 1.0 else "inferred",
        })

    bedroom = _extract_bedrooms(text)
    if bedroom:
        results["facts"].append(bedroom)

    bathroom = _extract_bathrooms(text)
    if bathroom:
        results["facts"].append(bathroom)

    return results


def _extract_bedrooms(text: str) -> dict[str, Any] | None:
    patterns = [
        re.compile(r"(\d+)\s*(?:chambres?|pieces?|pièces?)", re.IGNORECASE),
        re.compile(r"(?:chambres?|pieces?|pièces?)\s*(\d+)", re.IGNORECASE),
        re.compile(r"(\d+)\s*(?:br|bedrooms?)", re.IGNORECASE),
        re.compile(r"t(\d+)", re.IGNORECASE),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 50:
                return {
                    "field": "bedroom_count",
                    "raw_value": match.group(0),
                    "normalized_value": num,
                    "confidence": 1.0,
                    "source_type": "explicit",
                }
    return None


def _extract_bathrooms(text: str) -> dict[str, Any] | None:
    patterns = [
        re.compile(r"(\d+)\s*(?:salles?\s*d[''']?eaus?|sdb|douche)", re.IGNORECASE),
        re.compile(r"(?:salles?\s*d[''']?eaus?|sdb|douche)\s*(\d+)", re.IGNORECASE),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 20:
                return {
                    "field": "bathroom_count",
                    "raw_value": match.group(0),
                    "normalized_value": num,
                    "confidence": 1.0,
                    "source_type": "explicit",
                }
    return None


def _extract_surface(text: str) -> dict[str, Any] | None:
    patterns = [
        re.compile(r"(\d+)\s*(?:m[2²]|m\s*carres?|mètres?\s*carres?|metres?\s*carres?)", re.IGNORECASE),
        re.compile(r"(?:surface|superficie)\s*(?:de\s*)?(\d+)", re.IGNORECASE),
    ]
    for pattern in patterns:
        match = pattern.search(text)
        if match:
            num = int(match.group(1))
            if 5 <= num <= 100000:
                return {
                    "field": "surface_sqm",
                    "raw_value": match.group(0),
                    "normalized_value": num,
                    "confidence": 1.0,
                    "source_type": "explicit",
                }
    return None
