from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ActionExecutionRequest:
    execution_request_id: str = field(default_factory=lambda: uuid4().hex[:16])
    decision_id: str = ""
    project_id: str = ""
    profile_id: str = ""
    profile_version: str = ""
    action_code: str = ""
    action_parameters: dict[str, Any] = field(default_factory=dict)
    current_stage: str = ""
    target_stage: str = ""
    priority: int = 100
    requested_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    requested_by: str = "system"
    correlation_id: str = ""
    causation_id: str = ""
    idempotency_key: str = ""
    policy_version: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def create_idempotency_key(
        project_id: str,
        action_code: str,
        decision_id: str = "",
    ) -> str:
        raw = f"{project_id}:{action_code}:{decision_id or uuid4().hex[:16]}"
        import hashlib
        return hashlib.sha256(raw.encode()).hexdigest()[:32]
