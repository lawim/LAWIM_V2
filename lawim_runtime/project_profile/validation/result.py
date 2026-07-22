from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    UNKNOWN = "UNKNOWN"
    REQUIRES_CONFIRMATION = "REQUIRES_CONFIRMATION"


@dataclass
class ValidationIssue:
    field_name: str = ""
    status: ValidationStatus = ValidationStatus.VALID
    message: str = ""
    code: str = ""
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    status: ValidationStatus = ValidationStatus.VALID
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.status == ValidationStatus.VALID and not any(
            i.status == ValidationStatus.INVALID for i in self.issues
        )
