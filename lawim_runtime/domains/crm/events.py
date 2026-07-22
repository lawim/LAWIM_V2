from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class CRMEventType(str, Enum):
    CRM_LEAD_CREATED = "CRM_LEAD_CREATED"
    CRM_LEAD_UPDATED = "CRM_LEAD_UPDATED"
    CRM_OPPORTUNITY_CREATED = "CRM_OPPORTUNITY_CREATED"
    CRM_OPPORTUNITY_UPDATED = "CRM_OPPORTUNITY_UPDATED"
    CRM_HANDOVER_CREATED = "CRM_HANDOVER_CREATED"
    CRM_HANDOVER_RESOLVED = "CRM_HANDOVER_RESOLVED"
    CRM_CASE_CLOSED = "CRM_CASE_CLOSED"


@dataclass(frozen=True)
class CRMEvent:
    event_type: CRMEventType = CRMEventType.CRM_LEAD_CREATED
    project_id: str = ""
    lead_id: str = ""
    opportunity_id: str = ""
    handover_id: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "crm", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "project_id": self.project_id,
                "lead_id": self.lead_id,
                "opportunity_id": self.opportunity_id,
                "handover_id": self.handover_id,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
