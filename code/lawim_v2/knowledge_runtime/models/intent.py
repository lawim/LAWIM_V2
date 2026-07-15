from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Intent:
    id: str
    name: str
    description: str
    transaction_types: tuple[str, ...] = ()
    detection_keywords: tuple[str, ...] = ()
    confidence_threshold: float = 0.7
    status: str = "ACTIVE"
    sources: tuple[str, ...] = ()
