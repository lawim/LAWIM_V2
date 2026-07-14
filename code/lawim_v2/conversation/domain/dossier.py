from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DossierStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    MATCHED = "MATCHED"
    CONTACTED = "CONTACTED"
    CLOSED = "CLOSED"


@dataclass
class DossierInfo:
    dossier_id: int | None = None
    project_id: int | None = None
    user_id: int | None = None
    status: DossierStatus = DossierStatus.PENDING
    search_criteria: dict[str, Any] = field(default_factory=dict)
    property_type: str | None = None
    budget_min: float | None = None
    budget_max: float | None = None
    city: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
