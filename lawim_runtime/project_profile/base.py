from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from .values import FieldValue, FieldValueStatus
from .patch import ProfilePatch


@dataclass
class AbstractProjectProfile(ABC):
    profile_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    profile_type: str = ""
    schema_version: str = "1.0"
    status: str = "DRAFT"
    fields: dict[str, FieldValue] = field(default_factory=dict)
    completion_score: float = 0.0
    confidence_score: float = 1.0
    validation_status: str = "UNKNOWN"
    conflict_status: str = "NONE"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1
    metadata: dict[str, Any] = field(default_factory=dict)

    def get_field(self, field_name: str) -> FieldValue | None:
        return self.fields.get(field_name)

    def has_field(self, field_name: str) -> bool:
        return field_name in self.fields

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "project_id": self.project_id,
            "profile_type": self.profile_type,
            "schema_version": self.schema_version,
            "status": self.status,
            "fields": {k: v.value for k, v in self.fields.items() if v.status not in (FieldValueStatus.REJECTED, FieldValueStatus.SUPERSEDED)},
            "completion_score": self.completion_score,
            "confidence_score": self.confidence_score,
            "validation_status": self.validation_status,
            "conflict_status": self.conflict_status,
            "version": self.version,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
