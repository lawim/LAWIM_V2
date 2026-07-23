from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ExtractionMethod(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    LLM = "LLM"
    HYBRID = "HYBRID"
    USER_PROVIDED = "USER_PROVIDED"
    INFERRED = "INFERRED"


@dataclass(frozen=True)
class ExtractionEvidence:
    source_text: str = ""
    source_message_id: str = ""
    source_interaction_id: str = ""
    extraction_method: ExtractionMethod = ExtractionMethod.DETERMINISTIC
    provider: str = ""
    model: str = ""
    prompt_version: str = ""
    confidence: float = 1.0
    char_start: int = -1
    char_end: int = -1
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass(frozen=True)
class ExtractionWarning:
    warning_id: str = field(default_factory=lambda: uuid4().hex[:16])
    code: str = ""
    message: str = ""
    field_name: str = ""
    severity: str = "info"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExtractionCandidate:
    candidate_id: str = field(default_factory=lambda: uuid4().hex[:16])
    field_name: str = ""
    value: Any = None
    raw_value: str = ""
    normalized_value: Any = None
    confidence: float = 1.0
    evidence: ExtractionEvidence | None = None
    is_negation: bool = False
    is_correction: bool = False
    is_ambiguous: bool = False
    previous_value: Any = None
    correction_of: str = ""
    provenance: list[ExtractionEvidence] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
