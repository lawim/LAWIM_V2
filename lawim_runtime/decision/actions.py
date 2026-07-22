from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ActionCategory(str, Enum):
    INFORMATION = "INFORMATION"
    QUALIFICATION = "QUALIFICATION"
    COLLECTION = "COLLECTION"
    CONFIRMATION = "CONFIRMATION"
    MATCHING = "MATCHING"
    VISIT = "VISIT"
    DOCUMENT = "DOCUMENT"
    TRANSACTION = "TRANSACTION"
    ESCALATION = "ESCALATION"
    HANDOVER = "HANDOVER"
    COMPLETION = "COMPLETION"


_REQUIRES_HUMAN: set[ActionCategory] = {
    ActionCategory.ESCALATION,
    ActionCategory.HANDOVER,
    ActionCategory.TRANSACTION,
}


@dataclass(frozen=True)
class ActionDefinition:
    action_name: str = ""
    category: ActionCategory = ActionCategory.INFORMATION
    description: str = ""
    requires_human: bool = False
    priority: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.category in _REQUIRES_HUMAN and not self.requires_human:
            object.__setattr__(self, "requires_human", True)
