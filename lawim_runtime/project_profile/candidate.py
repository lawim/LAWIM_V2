from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from .values import ExtractionMethod


@dataclass(frozen=True)
class CandidateUpdate:
    candidate_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    profile_id: str = ""
    field_name: str = ""
    raw_value: str = ""
    proposed_value: Any = None
    confidence: float = 1.0
    source_type: ExtractionMethod = ExtractionMethod.DETERMINISTIC
    source_id: str = ""
    source_message_id: str = ""
    actor_id: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    extraction_method: str = "DETERMINISTIC"
    metadata: dict[str, Any] = field(default_factory=dict)
