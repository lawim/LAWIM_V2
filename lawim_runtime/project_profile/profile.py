from __future__ import annotations
from typing import Any
from .base import AbstractProjectProfile
from .values import FieldValue, FieldValueStatus
from .patch import ProfilePatch, PatchUpdate, PatchOperation
from .registry import FieldRegistry, FieldNotFoundError


class ProjectProfile(AbstractProjectProfile):
    def set_field(self, field_name: str, value: Any, confidence: float = 1.0, **kwargs) -> FieldValue:
        fv = FieldValue(
            field_name=field_name,
            value=value,
            normalized_value=value,
            confidence=confidence,
            status=FieldValueStatus.CANDIDATE,
            **{k: v for k, v in kwargs.items() if k in FieldValue.__dataclass_fields__},
        )
        self.fields[field_name] = fv
        self.updated_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
        return fv

    def remove_field(self, field_name: str) -> None:
        self.fields.pop(field_name, None)
        self.updated_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()
