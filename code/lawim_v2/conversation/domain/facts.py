from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class FactStatus(str, Enum):
    EXPLICIT = "EXPLICIT"
    INFERRED = "INFERRED"
    AMBIGUOUS = "AMBIGUOUS"
    CONFIRMED = "CONFIRMED"
    CONFLICTING = "CONFLICTING"
    SUPERSEDED = "SUPERSEDED"
    REVOKED = "REVOKED"


CONFIRMED_STATUSES = {FactStatus.CONFIRMED, FactStatus.EXPLICIT}
ACTIVE_STATUSES = {FactStatus.CONFIRMED, FactStatus.EXPLICIT, FactStatus.INFERRED, FactStatus.AMBIGUOUS}


@dataclass
class Fact:
    fact_id: str | None = None
    field: str = ""
    raw_value: str = ""
    normalized_value: Any = None
    source_message_id: str | None = None
    source_channel: str | None = None
    source_type: str = "explicit"
    confidence: float = 1.0
    confirmation_status: FactStatus = FactStatus.EXPLICIT
    project_id: int | None = None
    dossier_id: int | None = None
    conversation_id: int | None = None
    valid_from: str | None = None
    valid_to: str | None = None
    supersedes_fact_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    def is_confirmed(self) -> bool:
        return self.confirmation_status in CONFIRMED_STATUSES

    def is_active(self) -> bool:
        return self.confirmation_status in ACTIVE_STATUSES and self.valid_to is None

    def supersede(self) -> Fact:
        return Fact(
            field=self.field,
            raw_value=self.raw_value,
            normalized_value=self.normalized_value,
            confirmation_status=FactStatus.SUPERSEDED,
            project_id=self.project_id,
            dossier_id=self.dossier_id,
            supersedes_fact_id=self.fact_id,
            valid_to=datetime.utcnow().isoformat(),
        )


@dataclass
class FactCollection:
    facts: list[Fact] = field(default_factory=list)

    def get_active(self, field: str | None = None) -> list[Fact]:
        result = [f for f in self.facts if f.is_active()]
        if field:
            result = [f for f in result if f.field == field]
        return result

    def get_confirmed(self, field: str | None = None) -> list[Fact]:
        result = [f for f in self.facts if f.is_confirmed() and f.is_active()]
        if field:
            result = [f for f in result if f.field == field]
        return result

    def get_latest_confirmed(self, field: str) -> Fact | None:
        confirmed = self.get_confirmed(field)
        if not confirmed:
            return None
        return max(confirmed, key=lambda f: f.created_at or "")

    def get_ambiguous(self) -> list[Fact]:
        return [f for f in self.facts if f.confirmation_status == FactStatus.AMBIGUOUS and f.is_active()]

    def add_fact(self, fact: Fact) -> None:
        if fact.supersedes_fact_id:
            for existing in self.facts:
                if existing.fact_id == fact.supersedes_fact_id:
                    existing.valid_to = fact.created_at
                    existing.confirmation_status = FactStatus.SUPERSEDED
        self.facts.append(fact)

    def has_field(self, field: str) -> bool:
        return any(f.field == field and f.is_confirmed() and f.is_active() for f in self.facts)

    def all_confirmed_fields(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for f in self.facts:
            if f.is_confirmed() and f.is_active():
                result[f.field] = f.normalized_value if f.normalized_value is not None else f.raw_value
        return result

    def to_dict(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "confirmed": [
                {"field": f.field, "value": f.normalized_value or f.raw_value, "source": f.source_type}
                for f in self.facts
                if f.is_confirmed() and f.is_active()
            ],
            "ambiguous": [
                {"field": f.field, "raw_value": f.raw_value}
                for f in self.facts
                if f.confirmation_status == FactStatus.AMBIGUOUS and f.is_active()
            ],
            "pending": [
                {"field": f.field, "raw_value": f.raw_value}
                for f in self.facts
                if f.confirmation_status == FactStatus.INFERRED and f.is_active()
            ],
        }
