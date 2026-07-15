from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class QuestionPriority(str, Enum):
    MANDATORY = "MANDATORY"
    IMPORTANT = "IMPORTANT"
    OPTIONAL = "OPTIONAL"


@dataclass
class FieldRoleAssignment:
    field_code: str = ""
    matching_role: str = ""
    weight: float = 0.0
    priority: QuestionPriority = QuestionPriority.OPTIONAL

    def to_dict(self) -> dict[str, Any]:
        return {"field_code": self.field_code, "matching_role": self.matching_role,
                "weight": self.weight, "priority": self.priority.value}


@dataclass
class FieldDictionary:
    fields: dict[str, FieldRoleAssignment] = field(default_factory=dict)

    def register(self, assignment: FieldRoleAssignment) -> None:
        self.fields[assignment.field_code] = assignment

    def get(self, code: str) -> FieldRoleAssignment | None:
        return self.fields.get(code)

    def count(self) -> int:
        return len(self.fields)


# ── Priority Engine ────────────────────────────────────────────────────────


class PriorityEngine:
    def order_fields(self, fields: list[FieldRoleAssignment]) -> list[FieldRoleAssignment]:
        priority_order = {QuestionPriority.MANDATORY: 0, QuestionPriority.IMPORTANT: 1,
                          QuestionPriority.OPTIONAL: 2}
        return sorted(fields, key=lambda f: (priority_order.get(f.priority, 99), f.field_code))

    def mandatory_only(self, fields: list[FieldRoleAssignment]) -> list[FieldRoleAssignment]:
        return [f for f in fields if f.priority == QuestionPriority.MANDATORY]


# ── Channel Adapter ────────────────────────────────────────────────────────

DEFAULT_CHANNEL_LIMITS: dict[str, dict[str, int]] = {
    "whatsapp": {"mandatory": 1, "important": 0, "optional": 0},
    "telegram": {"mandatory": 2, "important": 1, "optional": 0},
    "dashboard": {"mandatory": 20, "important": 20, "optional": 20},
    "web": {"mandatory": 5, "important": 3, "optional": 2},
}


@dataclass
class ChannelAdapter:
    channel: str = "dashboard"
    limits: dict[str, int] = field(default_factory=lambda: dict(DEFAULT_CHANNEL_LIMITS.get("dashboard", {})))

    def questions_per_interaction(self, priority: QuestionPriority) -> int:
        return self.limits.get(priority.value.lower(), 1)

    def can_ask(self, priority: QuestionPriority, asked_in_step: int = 0) -> bool:
        limit = self.questions_per_interaction(priority)
        return asked_in_step < limit


def channel_limits_for(channel: str) -> dict[str, int]:
    return dict(DEFAULT_CHANNEL_LIMITS.get(channel, DEFAULT_CHANNEL_LIMITS["dashboard"]))


# ── Qualification Step Machine ─────────────────────────────────────────────


class StepStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"
    ABANDONED = "ABANDONED"


@dataclass
class QualificationStepMachine:
    current_step: int = 1
    max_step: int = 10
    status: StepStatus = StepStatus.PENDING
    step_statuses: dict[int, StepStatus] = field(default_factory=dict)

    def can_advance(self) -> bool:
        return self.current_step < self.max_step and self.status != StepStatus.ABANDONED

    def advance(self) -> int:
        if self.can_advance():
            self.step_statuses[self.current_step] = StepStatus.COMPLETED
            self.current_step += 1
            self.step_statuses[self.current_step] = StepStatus.ACTIVE
        return self.current_step

    def abandon(self) -> None:
        self.status = StepStatus.ABANDONED
        if self.current_step in self.step_statuses:
            self.step_statuses[self.current_step] = StepStatus.ABANDONED

    def resume(self, step: int) -> None:
        self.current_step = step
        self.status = StepStatus.ACTIVE
        self.step_statuses[step] = StepStatus.ACTIVE
