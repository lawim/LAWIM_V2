from __future__ import annotations

from typing import Any

from ..candidate import CandidateUpdate
from ..patch import PatchOperation, PatchUpdate, ProfilePatch
from ..values import ExtractionMethod


class ConversationStateToProfileAdapter:
    def to_candidates(
        self,
        known_slots: dict[str, Any],
        actor_id: str = "",
        correlation_id: str = "",
    ) -> list[CandidateUpdate]:
        candidates: list[CandidateUpdate] = []
        for field_name, value in known_slots.items():
            candidates.append(
                CandidateUpdate(
                    field_name=field_name,
                    proposed_value=value,
                    raw_value=str(value),
                    source_type=ExtractionMethod.DETERMINISTIC,
                    actor_id=actor_id,
                    correlation_id=correlation_id,
                )
            )
        return candidates

    def to_patch(
        self,
        known_slots: dict[str, Any],
        project_id: str = "",
        profile_id: str = "",
        base_version: int = 1,
        source: str = "conversation_engine",
    ) -> ProfilePatch:
        updates: list[PatchUpdate] = []
        for field_name, value in known_slots.items():
            updates.append(
                PatchUpdate(
                    operation=PatchOperation.SET,
                    field_name=field_name,
                    value=value,
                )
            )
        return ProfilePatch(
            project_id=project_id,
            profile_id=profile_id,
            base_version=base_version,
            updates=tuple(updates),
            source=source,
        )
