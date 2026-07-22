from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .score import QualificationScore, QualificationLevel


@dataclass(frozen=True)
class QualificationResult:
    result_id: str = ""
    project_id: str = ""
    profile_id: str = ""
    profile_version: int = 0
    policy_id: str = ""
    policy_version: int = 0
    score: QualificationScore = field(default_factory=QualificationScore)
    level: QualificationLevel = QualificationLevel.UNQUALIFIED
    status: str = "UNQUALIFIED"
    required_present: int = 0
    required_missing: list[str] = field(default_factory=list)
    important_missing: list[str] = field(default_factory=list)
    optional_missing: list[str] = field(default_factory=list)
    invalid_fields: list[str] = field(default_factory=list)
    conflicted_fields: list[str] = field(default_factory=list)
    low_confidence_fields: list[str] = field(default_factory=list)
    confirmation_required_fields: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    ready_stages: list[str] = field(default_factory=list)
    ready_actions: list[str] = field(default_factory=list)
    not_ready_actions: list[str] = field(default_factory=list)
    evaluated_at: str = ""
    correlation_id: str = ""
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def missing_fields(self) -> list[str]:
        return self.required_missing + self.important_missing + self.optional_missing
