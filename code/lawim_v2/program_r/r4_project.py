from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class DossierState(str, Enum):
    DRAFT = "DRAFT"
    QUALIFYING = "QUALIFYING"
    MATCHING = "MATCHING"
    PROPOSED = "PROPOSED"
    NEGOTIATING = "NEGOTIATING"
    TRANSACTING = "TRANSACTING"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"


DOSSIER_TRANSITIONS: dict[DossierState, list[DossierState]] = {
    DossierState.DRAFT: [DossierState.QUALIFYING, DossierState.ARCHIVED],
    DossierState.QUALIFYING: [DossierState.MATCHING, DossierState.DRAFT, DossierState.ARCHIVED],
    DossierState.MATCHING: [DossierState.PROPOSED, DossierState.QUALIFYING, DossierState.ARCHIVED],
    DossierState.PROPOSED: [DossierState.NEGOTIATING, DossierState.MATCHING, DossierState.CLOSED],
    DossierState.NEGOTIATING: [DossierState.TRANSACTING, DossierState.PROPOSED, DossierState.CLOSED],
    DossierState.TRANSACTING: [DossierState.CLOSED, DossierState.NEGOTIATING],
    DossierState.CLOSED: [DossierState.ARCHIVED],
    DossierState.ARCHIVED: [],
}


@dataclass
class Dossier:
    dossier_id: str = ""
    project_id: int | None = None
    parent_dossier_id: str = ""
    is_multi_dossier: bool = False
    state: DossierState = DossierState.DRAFT
    holder_id: int | None = None
    demandeur_id: int | None = None
    property_id: int | None = None

    def can_transition(self, target: DossierState) -> bool:
        return target in DOSSIER_TRANSITIONS.get(self.state, [])

    def transition(self, target: DossierState) -> DossierState:
        if self.can_transition(target):
            self.state = target
        return self.state


@dataclass
class DoubleConsent:
    dossier_id: str = ""
    c1_demandeur: bool = False
    c1_at: str = ""
    c2_holder: bool = False
    c2_at: str = ""
    both_required: bool = True
    deadline: str = ""

    def is_complete(self) -> bool:
        if self.both_required:
            return self.c1_demandeur and self.c2_holder
        return self.c1_demandeur


@dataclass
class HolderDecision:
    decision: str = "PENDING"
    favorable: bool = False
    decided_at: str = ""
    deadline: str = ""
    notes: str = ""


@dataclass
class DossierRematch:
    count: int = 0
    max_rematches: int = 3
    reasons: list[str] = field(default_factory=list)

    def can_rematch(self) -> bool:
        return self.count < self.max_rematches

    def rematch(self, reason: str) -> bool:
        if not self.can_rematch():
            return False
        self.count += 1
        self.reasons.append(reason)
        return True


@dataclass
class DossierParticipant:
    participant_id: str = ""
    dossier_id: str = ""
    actor_id: str = ""
    role: str = ""
    joined_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"participant_id": self.participant_id, "role": self.role}


@dataclass
class DossierHealthScore:
    completeness: float = 0.0
    freshness: float = 0.0
    total: float = 0.0

    def compute(self, filled_fields: int, total_fields: int,
                 last_activity_days: int) -> DossierHealthScore:
        self.completeness = min(100, (filled_fields / max(total_fields, 1)) * 100)
        self.freshness = max(0, 100 - last_activity_days * 5)
        self.total = round(self.completeness * 0.6 + self.freshness * 0.4, 2)
        return self


@dataclass
class PublicationRule:
    field: str = ""
    message: str = ""
    passes: bool = False


@dataclass
class DossierDataScope:
    scope: str = "STANDARD"
    privacy_controls: dict[str, bool] = field(default_factory=dict)
    documents_required: list[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        return all(v for v in self.privacy_controls.values())
