from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from ..project_profile.base import AbstractProjectProfile


@dataclass
class HandoverEvaluation:
    handover_required: bool = False
    reason: str = ""
    target_team: str = ""
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def requires_handover(self) -> bool:
        return self.handover_required


HANDOVER_TRIGGERS: tuple[str, ...] = (
    "agent",
    "humain",
    "operator",
    "parler à quelqu'un",
    "speak to a human",
    "escalate",
    "réclamation",
    "complaint",
    "litige",
    "dispute",
    "avocat",
    "lawyer",
)


class HumanHandoverEvaluator:
    def evaluate(self, profile: AbstractProjectProfile, user_message: str = "") -> HandoverEvaluation:
        trigger = self._find_trigger(user_message)
        if trigger:
            return HandoverEvaluation(
                handover_required=True,
                reason=f"User requested human handover (trigger: '{trigger}')",
                target_team="support",
            )
        if profile.conflict_status not in ("NONE", ""):
            return HandoverEvaluation(
                handover_required=True,
                reason=f"Profile conflict status: {profile.conflict_status}",
                target_team="operations",
            )
        if profile.validation_status == "FAILED":
            return HandoverEvaluation(
                handover_required=True,
                reason="Profile validation failed",
                target_team="operations",
            )
        return HandoverEvaluation(handover_required=False)

    def _find_trigger(self, message: str) -> str:
        lower = message.lower().strip()
        for trigger in HANDOVER_TRIGGERS:
            if trigger in lower:
                return trigger
        return ""
