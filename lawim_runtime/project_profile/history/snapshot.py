from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..base import AbstractProjectProfile
from ..values import FieldValue, FieldValueStatus


@dataclass
class ProfileSnapshot:
    snapshot_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    profile_id: str = ""
    profile_version: int = 0
    schema_version: str = "1.0"
    fields: dict[str, Any] = field(default_factory=dict)
    completion_score: float = 0.0
    confidence_score: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str = ""
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def create(profile: AbstractProjectProfile, correlation_id: str = "") -> ProfileSnapshot:
        fields_ser = {
            k: v.value if hasattr(v, "value") else v
            for k, v in profile.fields.items()
            if hasattr(v, "status") and v.status not in (FieldValueStatus.REJECTED, FieldValueStatus.SUPERSEDED)
        }
        raw = json.dumps(fields_ser, sort_keys=True, default=str)
        snapshot = ProfileSnapshot(
            project_id=profile.project_id,
            profile_id=profile.profile_id,
            profile_version=profile.version,
            schema_version=profile.schema_version,
            fields=fields_ser,
            completion_score=profile.completion_score,
            confidence_score=profile.confidence_score,
            correlation_id=correlation_id,
            checksum=hashlib.sha256(raw.encode()).hexdigest()[:16],
        )
        return snapshot
