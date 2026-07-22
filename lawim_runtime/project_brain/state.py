from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProjectBrainState:
    project_id: str = ""
    profile_id: str = ""
    project_type: str = ""
    project_status: str = ""
    project_stage: str = ""
    profile_version: int = 0
    qualification_score: float = 0.0
    qualification_level: str = "UNQUALIFIED"
    completion_score: float = 0.0
    confidence_score: float = 0.0
    risk_level: str = "LOW"
    conflict_status: str = "NONE"
    blocking_reasons: list[str] = field(default_factory=list)
    ready_actions: list[str] = field(default_factory=list)
    selected_action: str = ""
    selected_field: str = ""
    human_required: bool = False
    waiting_reason: str = ""
    last_decision_id: str = ""
    evaluated_at: str = ""
    version: int = 1
    checksum: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
