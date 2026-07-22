from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class VisitEventType(str, Enum):
    VISIT_AVAILABILITY_REQUESTED = "VISIT_AVAILABILITY_REQUESTED"
    VISIT_REQUESTED = "VISIT_REQUESTED"
    VISIT_CREATED = "VISIT_CREATED"
    VISIT_SCHEDULED = "VISIT_SCHEDULED"
    VISIT_CONFIRMED = "VISIT_CONFIRMED"
    VISIT_CANCELLED = "VISIT_CANCELLED"
    VISIT_COMPLETED = "VISIT_COMPLETED"
    VISIT_NO_SHOW = "VISIT_NO_SHOW"
    VISIT_FAILED = "VISIT_FAILED"


@dataclass(frozen=True)
class VisitEvent:
    event_type: VisitEventType = VisitEventType.VISIT_REQUESTED
    visit_id: str = ""
    property_id: str = ""
    requester: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "visit", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "visit_id": self.visit_id,
                "property_id": self.property_id,
                "requester": self.requester,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
