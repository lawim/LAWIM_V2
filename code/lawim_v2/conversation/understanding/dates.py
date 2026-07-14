from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

TIMEZONE = "Africa/Douala"

RELATIVE_DATE_PATTERNS = [
    (re.compile(r"aujourd'?hui", re.IGNORECASE), 0),
    (re.compile(r"(?:ce\s+)?soir", re.IGNORECASE), 0),
    (re.compile(r"cet?\s+apres[- ]?midi", re.IGNORECASE), 0),
    (re.compile(r"cet?\s+aprem", re.IGNORECASE), 0),
    (re.compile(r"maintenant", re.IGNORECASE), 0),
    (re.compile(r"demain\s*(?:matin|soir)?", re.IGNORECASE), 1),
    (re.compile(r"apres[- ]?demain", re.IGNORECASE), 2),
    (re.compile(r"(?:la\s+)?semaine\s+prochaine", re.IGNORECASE), 7),
    (re.compile(r"(?:le\s+)?mois\s+prochain", re.IGNORECASE), 30),
    (re.compile(r"dans\s+(\d+)\s*(?:jour|jours)", re.IGNORECASE), None),
    (re.compile(r"dans\s+(\d+)\s*(?:semaine|semaines)", re.IGNORECASE), None),
    (re.compile(r"dans\s+(\d+)\s*(?:mois)", re.IGNORECASE), None),
    (re.compile(r"dans\s+(\d+)\s*(?:an|ans|annee|annees)", re.IGNORECASE), None),
    (re.compile(r"(?:avant|avant\s+le)\s*(?:(\d+)\s*)?(?:janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)", re.IGNORECASE), None),
    (re.compile(r"(?:en|au\s+mois\s+de)\s*(?:janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)", re.IGNORECASE), None),
]

MONTH_NAMES = {
    "janvier": 1, "fevrier": 2, "février": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "aout": 8, "août": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12, "décembre": 12,
}


@dataclass
class DateResult:
    raw_value: str
    normalized_date: str | None = None
    timezone: str = TIMEZONE
    precision: str = "day"
    confidence: float = 1.0
    ambiguity: bool = False

    def to_fact_dict(self) -> dict[str, Any]:
        return {
            "raw_value": self.raw_value,
            "normalized_date": self.normalized_date,
            "timezone": self.timezone,
            "precision": self.precision,
            "confidence": self.confidence,
            "ambiguity": self.ambiguity,
        }


def normalize_date(raw: str) -> DateResult:
    now = datetime.utcnow()
    cleaned = raw.strip()

    for pattern, days_offset in RELATIVE_DATE_PATTERNS:
        match = pattern.search(cleaned)
        if match:
            if days_offset is not None:
                target = now + timedelta(days=days_offset)
                precision = "day"
                return DateResult(
                    raw_value=raw,
                    normalized_date=target.strftime("%Y-%m-%d"),
                    precision=precision,
                )
            if match.lastindex and match.group(1):
                num = int(match.group(1))
                text = cleaned.lower()
                if "jour" in text:
                    target = now + timedelta(days=num)
                elif "semaine" in text:
                    target = now + timedelta(weeks=num)
                elif "mois" in text:
                    target = now + timedelta(days=num * 30)
                elif "an" in text or "anne" in text:
                    target = now + timedelta(days=num * 365)
                else:
                    continue
                return DateResult(
                    raw_value=raw,
                    normalized_date=target.strftime("%Y-%m-%d"),
                )
            for month_name, month_num in MONTH_NAMES.items():
                if month_name in cleaned.lower():
                    year = now.year
                    if month_num < now.month:
                        year += 1
                    if "avant" in cleaned.lower() or "avant le" in cleaned.lower():
                        day_match = re.search(r"(\d+)", cleaned)
                        day = int(day_match.group(1)) if day_match else 1
                    else:
                        day = 1
                    target = datetime(year, month_num, day)
                    return DateResult(
                        raw_value=raw,
                        normalized_date=target.strftime("%Y-%m-%d"),
                        precision="month",
                    )

    date_patterns = [
        re.compile(r"(\d{1,2})\s*[-/]\s*(\d{1,2})\s*[-/]\s*(\d{2,4})"),
        re.compile(r"(\d{4})\s*[-/]\s*(\d{1,2})\s*[-/]\s*(\d{1,2})"),
        re.compile(r"(\d{1,2})\s*(?:er)?\s*(janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre)", re.IGNORECASE),
    ]

    for pattern in date_patterns:
        match = pattern.search(cleaned)
        if match:
            groups = match.groups()
            if len(groups) == 3:
                if groups[0].isdigit() and int(groups[0]) > 31:
                    year, month, day = int(groups[0]), int(groups[1]), int(groups[2])
                elif groups[2].isdigit() and len(groups[2]) in (2, 4):
                    day, month_str, year_str = groups[0], groups[1], groups[2]
                    day = int(day)
                    month = int(month_str)
                    year = int(year_str)
                    if year < 100:
                        year += 2000
                else:
                    day = int(groups[0])
                    month_name = groups[1].lower()
                    month = MONTH_NAMES.get(month_name, 1)
                    year = now.year
                    if month < now.month or (month == now.month and day < now.day):
                        year += 1
                try:
                    target = datetime(year, month, day)
                    return DateResult(
                        raw_value=raw,
                        normalized_date=target.strftime("%Y-%m-%d"),
                    )
                except ValueError:
                    continue

    return DateResult(
        raw_value=raw,
        ambiguity=True,
        confidence=0.0,
    )
