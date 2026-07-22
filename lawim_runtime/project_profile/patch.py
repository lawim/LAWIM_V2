from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class PatchOperation(str, Enum):
    SET = "SET"
    REPLACE = "REPLACE"
    REMOVE = "REMOVE"
    APPEND = "APPEND"
    MERGE = "MERGE"
    CONFIRM = "CONFIRM"
    REJECT = "REJECT"


@dataclass(frozen=True)
class PatchUpdate:
    operation: PatchOperation = PatchOperation.SET
    field_name: str = ""
    value: Any = None
    confidence: float = 1.0


@dataclass(frozen=True)
class ProfilePatch:
    patch_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    profile_id: str = ""
    base_version: int = 0
    updates: tuple[PatchUpdate, ...] = ()
    source: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)
