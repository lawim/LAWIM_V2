from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from enum import Enum
from .status import ProjectStatus, ProjectType, ProjectStage, STAGE_MAP


def _enum_val(v: Any) -> str:
    return v.value if isinstance(v, Enum) else str(v)


@dataclass
class ProjectRuntime:
    project_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_type: ProjectType = ProjectType.OTHER
    status: ProjectStatus = ProjectStatus.DRAFT
    owner: str = ""
    profile: dict[str, Any] = field(default_factory=dict)
    qualification: dict[str, Any] = field(default_factory=dict)
    current_step: str = ""
    current_stage: ProjectStage = ProjectStage.INITIAL
    next_action: str = ""
    risk_level: str = "LOW"
    priority: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    version: int = 1

    @property
    def stage(self) -> ProjectStage:
        result = STAGE_MAP.get(self.status, ProjectStage.INITIAL)
        if isinstance(result, Enum):
            return result
        return ProjectStage.INITIAL

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_type": _enum_val(self.project_type),
            "status": _enum_val(self.status),
            "owner": self.owner,
            "profile": dict(self.profile),
            "qualification": dict(self.qualification),
            "current_step": self.current_step,
            "current_stage": _enum_val(self.current_stage),
            "next_action": self.next_action,
            "risk_level": self.risk_level,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
        }
