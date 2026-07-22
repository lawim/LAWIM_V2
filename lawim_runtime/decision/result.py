from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from .actions import ActionCategory, ActionDefinition


@dataclass
class DecisionResult:
    project_id: str = ""
    profile_type: str = ""
    selected_action: str = ""
    selected_category: ActionCategory = ActionCategory.INFORMATION
    selected_field: str = ""
    available_actions: list[str] = field(default_factory=list)
    human_required: bool = False
    human_reason: str = ""
    confidence: float = 1.0
    decision_id: str = ""
    decided_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def requires_human(self) -> bool:
        return self.human_required or self.selected_category in (
            ActionCategory.ESCALATION, ActionCategory.HANDOVER, ActionCategory.TRANSACTION,
        )
