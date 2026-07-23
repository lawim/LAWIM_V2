from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DataClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    PERSONAL = "PERSONAL"
    FINANCIAL = "FINANCIAL"
    LEGAL = "LEGAL"
    SECRET = "SECRET"


SENSITIVE_CLASSIFICATIONS = {
    DataClassification.PERSONAL,
    DataClassification.FINANCIAL,
    DataClassification.LEGAL,
    DataClassification.SECRET,
}


@dataclass
class DataHandlingPolicy:
    classification: DataClassification = DataClassification.INTERNAL
    allow_persist: bool = True
    allow_llm_send: bool = True
    require_redaction: bool = False
    retention_days: int = 90
    max_log_detail: str = "masked"
    metadata: dict[str, Any] = field(default_factory=dict)
