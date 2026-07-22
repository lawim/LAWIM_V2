from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class MatchingEventType(str, Enum):
    MATCHING_REQUESTED = "MATCHING_REQUESTED"
    MATCHING_STARTED = "MATCHING_STARTED"
    MATCHING_COMPLETED = "MATCHING_COMPLETED"
    MATCHING_REFINED = "MATCHING_REFINED"
    MATCHING_FAILED = "MATCHING_FAILED"


@dataclass(frozen=True)
class MatchingEvent:
    event_type: MatchingEventType = MatchingEventType.MATCHING_REQUESTED
    search_id: str = ""
    property_count: int = 0
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "matching", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "search_id": self.search_id,
                "property_count": self.property_count,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
