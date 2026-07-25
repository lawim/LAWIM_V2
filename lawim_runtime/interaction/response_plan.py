from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class ResponseType(str, Enum):
    GREETING = "GREETING"
    ASK_MISSING_FIELD = "ASK_MISSING_FIELD"
    ASK_CONFIRMATION = "ASK_CONFIRMATION"
    PRESENT_RESULTS = "PRESENT_RESULTS"
    WAIT = "WAIT"
    HANDOVER = "HANDOVER"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    SAFE_FALLBACK = "SAFE_FALLBACK"
    NO_RESPONSE = "NO_RESPONSE"


@dataclass
class InteractionResponsePlan:
    response_plan_id: str = field(default_factory=lambda: uuid4().hex[:16])
    project_id: str = ""
    decision_id: str = ""
    action_code: str = ""
    response_type: ResponseType = ResponseType.NO_RESPONSE
    language: str = "fr"
    identity_required: bool = False
    summary_required: bool = False
    selected_field: str = ""
    structured_facts: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    handover: bool = False
    handover_reason: str = ""
    handover_target_team: str = ""
    channel_constraints: dict[str, Any] = field(default_factory=dict)
    writer_instruction: str = ""
    correlation_id: str = ""
    causation_id: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)

    def is_empty(self) -> bool:
        return self.response_type == ResponseType.NO_RESPONSE
