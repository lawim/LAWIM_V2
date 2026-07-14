from __future__ import annotations

from datetime import datetime
from typing import Any

from ..domain.facts import Fact, FactCollection, FactStatus, CONFIRMED_STATUSES


class MemoryService:
    def __init__(self, repository):
        self.repository = repository

    def add_fact(
        self,
        field: str,
        raw_value: str,
        normalized_value: Any = None,
        source_message_id: str | None = None,
        source_channel: str | None = None,
        source_type: str = "explicit",
        confidence: float = 1.0,
        project_id: int | None = None,
        dossier_id: int | None = None,
        conversation_id: int | None = None,
        supersedes_fact_id: str | None = None,
    ) -> Fact:
        now = datetime.utcnow().isoformat()
        fact = Fact(
            field=field,
            raw_value=raw_value,
            normalized_value=normalized_value,
            source_message_id=source_message_id,
            source_channel=source_channel,
            source_type=source_type,
            confidence=confidence,
            confirmation_status=FactStatus.CONFIRMED if confidence >= 1.0
            else FactStatus(source_type.upper())
            if source_type.upper() in {"EXPLICIT", "INFERRED"}
            else FactStatus.EXPLICIT,
            project_id=project_id,
            dossier_id=dossier_id,
            conversation_id=conversation_id,
            supersedes_fact_id=supersedes_fact_id,
            valid_from=now,
            created_at=now,
            updated_at=now,
        )
        if supersedes_fact_id:
            self._supersede_fact(supersedes_fact_id, now)
        return self.repository.save_fact(fact)

    def _supersede_fact(self, fact_id: str, timestamp: str) -> None:
        self.repository.supersede_fact(fact_id, timestamp)

    def get_confirmed_facts(
        self,
        project_id: int | None = None,
        dossier_id: int | None = None,
        conversation_id: int | None = None,
    ) -> FactCollection:
        facts = self.repository.get_active_facts(
            project_id=project_id,
            dossier_id=dossier_id,
            conversation_id=conversation_id,
        )
        return FactCollection(facts=facts)

    def get_latest_confirmed(self, field: str, project_id: int | None = None) -> Fact | None:
        return self.repository.get_latest_confirmed_fact(field, project_id=project_id)

    def has_confirmed(self, field: str, project_id: int | None = None) -> bool:
        fact = self.get_latest_confirmed(field, project_id=project_id)
        return fact is not None and fact.is_confirmed()

    def handle_correction(
        self,
        field: str,
        old_fact_id: str,
        new_raw_value: str,
        new_normalized: Any = None,
        **kwargs,
    ) -> Fact:
        return self.add_fact(
            field=field,
            raw_value=new_raw_value,
            normalized_value=new_normalized,
            supersedes_fact_id=old_fact_id,
            **kwargs,
        )

    def mark_ambiguous(self, fact_id: str) -> None:
        self.repository.update_fact_status(fact_id, FactStatus.AMBIGUOUS)

    def mark_confirmed(self, fact_id: str) -> None:
        self.repository.update_fact_status(fact_id, FactStatus.CONFIRMED)

    def get_ambiguous_facts(self, project_id: int | None = None) -> list[Fact]:
        return self.repository.get_facts_by_status(FactStatus.AMBIGUOUS, project_id=project_id)

    def all_confirmed_as_dict(self, project_id: int | None = None) -> dict[str, Any]:
        fc = self.get_confirmed_facts(project_id=project_id)
        return fc.all_confirmed_fields()
