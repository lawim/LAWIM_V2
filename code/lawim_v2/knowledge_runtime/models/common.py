"""Common data models shared across the Knowledge Runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


class KnowledgeIdentifier(str):
    """A non-empty, case-stable identifier string for knowledge entities."""

    def __init__(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("KnowledgeIdentifier must be non-empty")
        super().__init__()

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> KnowledgeIdentifier:
        if isinstance(value, KnowledgeIdentifier):
            return value
        if not isinstance(value, str):
            raise TypeError(f"Expected str, got {type(value).__name__}")
        stripped = value.strip()
        if not stripped:
            raise ValueError("KnowledgeIdentifier must be non-empty")
        return cls(stripped)


@dataclass(frozen=True, slots=True)
class KnowledgeSource:
    """Describes a single knowledge source file that was loaded."""

    path: str
    section: str
    domain: str
    version: str
    checksum: str
    record_count: int
    status: str


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    """A single validation finding."""

    severity: str
    code: str
    message: str
    source: str
    identifier: str | None = None


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Aggregate validation result."""

    total_issues: int = 0
    errors: list[ValidationIssue] = field(default_factory=list)
    warnings: list[ValidationIssue] = field(default_factory=list)
    passed: bool = True


@dataclass(frozen=True, slots=True)
class RegistryMetadata:
    """Metadata tracked per registry."""

    name: str
    version: str
    record_count: int
    loaded_at: datetime
    checksum: str
