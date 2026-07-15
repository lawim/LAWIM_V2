from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Transaction:
    id: str
    name: str
    description: str
    transaction_type: str
    applicable_families: tuple[str, ...] = ()
    required_fields: tuple[str, ...] = ()
    optional_fields: tuple[str, ...] = ()
    status: str = "ACTIVE"
    sources: tuple[str, ...] = ()
