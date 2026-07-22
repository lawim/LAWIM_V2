from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class FieldValueStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    VALIDATED = "VALIDATED"
    REJECTED = "REJECTED"
    CONFLICTED = "CONFLICTED"
    SUPERSEDED = "SUPERSEDED"
    CONFIRMED = "CONFIRMED"
    UNKNOWN = "UNKNOWN"


class ExtractionMethod(str, Enum):
    DETERMINISTIC = "DETERMINISTIC"
    RULE_BASED = "RULE_BASED"
    LLM = "LLM"
    USER_CONFIRMED = "USER_CONFIRMED"
    OPERATOR = "OPERATOR"
    IMPORT = "IMPORT"
    API = "API"
    SYSTEM = "SYSTEM"


@dataclass
class FieldValue:
    field_name: str = ""
    value: Any = None
    normalized_value: Any = None
    confidence: float = 1.0
    status: FieldValueStatus = FieldValueStatus.CANDIDATE
    source_type: ExtractionMethod = ExtractionMethod.DETERMINISTIC
    source_id: str = ""
    source_message_id: str = ""
    actor_id: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    validated_at: str = ""
    validator_results: list[dict[str, Any]] = field(default_factory=list)
    version: int = 1
    previous_value: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
