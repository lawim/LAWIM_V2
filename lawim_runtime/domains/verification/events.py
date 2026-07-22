from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class VerificationEventType(str, Enum):
    VERIFICATION_STARTED = "VERIFICATION_STARTED"
    VERIFICATION_CHECK_COMPLETED = "VERIFICATION_CHECK_COMPLETED"
    VERIFICATION_COMPLETED = "VERIFICATION_COMPLETED"
    VERIFICATION_FAILED = "VERIFICATION_FAILED"
    VERIFICATION_ESCALATED = "VERIFICATION_ESCALATED"
    VERIFICATION_INCONCLUSIVE = "VERIFICATION_INCONCLUSIVE"


@dataclass(frozen=True)
class VerificationEvent:
    event_type: VerificationEventType = VerificationEventType.VERIFICATION_STARTED
    verification_id: str = ""
    project_id: str = ""
    check_id: str = ""
    check_type: str = ""
    previous_status: str = ""
    new_status: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "verification", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "verification_id": self.verification_id,
                "project_id": self.project_id,
                "check_id": self.check_id,
                "check_type": self.check_type,
                "previous_status": self.previous_status,
                "new_status": self.new_status,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
