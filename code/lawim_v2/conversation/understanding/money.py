from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


AMOUNT_PATTERNS = [
    re.compile(r"(\d+)\s*(?:millions?|mio|m)\s*(?:f\s*cfa|fca|xaf)?", re.IGNORECASE),
    re.compile(r"(\d+)\s*(?:milliers?\s*)?(?:de\s*)?(?:f\s*cfa|fcfa|francs?\s*cfa|xaf)", re.IGNORECASE),
    re.compile(r"(\d+[.,]\d+)\s*(?:millions?|m)\s*(?:f\s*cfa|fca|xaf)?", re.IGNORECASE),
    re.compile(r"(\d+(?:\s*\d+)*)\s*(?:f\s*cfa|fcfa|francs?\s*cfa|xaf)", re.IGNORECASE),
    re.compile(r"(\d+[.,]\d+)\s*(?:f\s*cfa|fcfa|francs?\s*cfa|xaf)", re.IGNORECASE),
    re.compile(r"(\d+(?:\s*\d+)*)\s*(?:euros?|\u20ac|usd|\$)", re.IGNORECASE),
    re.compile(r"(\d+)\s*(?:millions?|m)\s*(?:frs?)?", re.IGNORECASE),
    re.compile(r"(\d+)\s*(?:k|mille| mille)\s*(?:f\s*cfa|fca|xaf|francs?)?", re.IGNORECASE),
    re.compile(r"(\d+)\s*(?:cent|centaines?\s*de\s*milles?)\s*(?:f\s*cfa|fcfa|francs?\s*cfa|xaf)?", re.IGNORECASE),
    re.compile(r"(\d+[.,]\d+)\s*(?:millions?|m)\s*(?:frs?)?", re.IGNORECASE),
]

AMOUNT_WORDS = {
    "mille": 1_000,
    "million": 1_000_000,
    "millions": 1_000_000,
    "milliard": 1_000_000_000,
    "milliards": 1_000_000_000,
    "cent": 100,
    "cinquante": 50,
    "cent mille": 100_000,
    "cinq cents": 500,
}

AMBIGUOUS_PATTERNS = [
    re.compile(r"(\d+)\s*mil\s*$", re.IGNORECASE),
    re.compile(r"(\d+)\s*m\s*$", re.IGNORECASE),
]


@dataclass
class AmountResult:
    raw_value: str
    normalized_amount: int | None = None
    currency: str = "XAF"
    confidence: float = 1.0
    ambiguity: bool = False
    ambiguity_reason: str | None = None
    possible_values: list[int] | None = None

    def to_fact_dict(self) -> dict[str, Any]:
        return {
            "raw_value": self.raw_value,
            "normalized_amount": self.normalized_amount,
            "currency": self.currency,
            "confidence": self.confidence,
            "ambiguity": self.ambiguity,
            "ambiguity_reason": self.ambiguity_reason,
            "possible_values": self.possible_values,
        }


def _parse_number(text: str) -> int | None:
    text = text.strip().replace(" ", "").replace(",", ".").replace("\u202f", "")
    try:
        if "." in text:
            return int(float(text))
        return int(text)
    except ValueError:
        return None


def _detect_currency(text: str) -> str:
    lower = text.lower()
    if "euro" in lower or "\u20ac" in lower:
        return "EUR"
    if "usd" in lower or "$" in lower:
        return "USD"
    return "XAF"


def normalize_amount(raw: str) -> AmountResult:
    cleaned = raw.strip()

    for pattern in AMBIGUOUS_PATTERNS:
        match = pattern.search(cleaned)
        if match:
            num = _parse_number(match.group(1))
            if num is not None:
                if num < 1000:
                    return AmountResult(
                        raw_value=raw,
                        ambiguity=True,
                        ambiguity_reason=f"{num} {match.group(1)} pourrait etre {num} ou {num} millions",
                        possible_values=[num, num * 1_000_000],
                    )
                return AmountResult(
                    raw_value=raw,
                    normalized_amount=num,
                    confidence=1.0,
                    currency=_detect_currency(cleaned),
                )

    for pattern in AMOUNT_PATTERNS:
        match = pattern.search(cleaned)
        if match:
            raw_num = match.group(1).replace(" ", "")
            num = _parse_number(raw_num)
            if num is None:
                continue
            lower_cleaned = cleaned.lower()
            if "million" in lower_cleaned or "millions" in lower_cleaned or "mio" in lower_cleaned:
                num *= 1_000_000
            elif "milliard" in lower_cleaned or "milliards" in lower_cleaned:
                num *= 1_000_000_000
            elif "mille" in lower_cleaned or "k" in lower_cleaned:
                if "cent mille" in lower_cleaned:
                    num *= 100_000
                elif num < 100:
                    num *= 1_000
            elif "cent" in lower_cleaned and "cent mille" not in lower_cleaned:
                pass

            currency = _detect_currency(cleaned)

            if "cent" in lower_cleaned and num < 10:
                num *= 100

            return AmountResult(
                raw_value=raw,
                normalized_amount=num,
                currency=currency,
                confidence=1.0,
            )

    for word, value in sorted(AMOUNT_WORDS.items(), key=lambda x: -len(x[0])):
        if word in cleaned.lower():
            return AmountResult(
                raw_value=raw,
                normalized_amount=value,
                currency=_detect_currency(cleaned),
                confidence=0.8,
            )

    num = _parse_number(cleaned)
    if num is not None:
        return AmountResult(
            raw_value=raw,
            normalized_amount=num,
            currency=_detect_currency(cleaned),
            confidence=0.9,
        )

    return AmountResult(
        raw_value=raw,
        ambiguity=True,
        ambiguity_reason="Impossible de normaliser le montant",
    )
