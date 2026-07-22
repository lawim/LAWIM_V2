from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ConflictType(str, Enum):
    VALUE_MISMATCH = "VALUE_MISMATCH"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    LOW_CONFIDENCE_OVERRIDE = "LOW_CONFIDENCE_OVERRIDE"
    BUSINESS_RULE_CONFLICT = "BUSINESS_RULE_CONFLICT"
    GEOGRAPHIC_CONFLICT = "GEOGRAPHIC_CONFLICT"
    TEMPORAL_CONFLICT = "TEMPORAL_CONFLICT"
    CONCURRENT_UPDATE = "CONCURRENT_UPDATE"
    VERSION_CONFLICT = "VERSION_CONFLICT"


@dataclass
class ConflictRecord:
    conflict_id: str = ""
    field_name: str = ""
    conflict_type: ConflictType = ConflictType.VALUE_MISMATCH
    current_value: Any = None
    candidate_value: Any = None
    current_confidence: float = 0.0
    candidate_confidence: float = 0.0
    reason: str = ""
    resolved: bool = False
    resolution: str = ""


@dataclass
class ConflictResolution:
    status: str = ""
    resolution: str = ""
    resolved_value: Any = None
