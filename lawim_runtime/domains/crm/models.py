from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class CRMStatus(str, Enum):
    LEAD_CREATED = "LEAD_CREATED"
    LEAD_UPDATED = "LEAD_UPDATED"
    OPPORTUNITY_CREATED = "OPPORTUNITY_CREATED"
    OPPORTUNITY_UPDATED = "OPPORTUNITY_UPDATED"
    HANDOVER_CREATED = "HANDOVER_CREATED"
    HANDOVER_RESOLVED = "HANDOVER_RESOLVED"
    SIMULATED = "SIMULATED"
    FAILED = "FAILED"


@dataclass
class LeadData:
    lead_id: str = ""
    project_id: str = ""
    contact_name: str = ""
    contact_phone: str = ""
    contact_email: str = ""
    source: str = ""
    status: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class OpportunityData:
    opportunity_id: str = ""
    project_id: str = ""
    lead_id: str = ""
    stage: str = ""
    value: float = 0.0
    probability: float = 0.0
    expected_close_date: str = ""


@dataclass
class HandoverData:
    handover_id: str = ""
    project_id: str = ""
    reason: str = ""
    target_team: str = ""
    status: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: str = ""


@dataclass
class CRMRequest:
    request_id: str = ""
    action_code: str = ""
    project_id: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    correlation_id: str = ""
    idempotency_key: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_request(self) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id=self.request_id,
            action_code=self.action_code,
            parameters={
                "project_id": self.project_id,
                **self.data,
            },
            correlation_id=self.correlation_id,
            idempotency_key=self.idempotency_key,
            metadata=self.metadata,
        )


@dataclass
class CRMResult:
    request_id: str = ""
    action_code: str = ""
    status: CRMStatus = CRMStatus.FAILED
    lead: LeadData | None = None
    opportunity: OpportunityData | None = None
    handover: HandoverData | None = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            CRMStatus.LEAD_CREATED: DomainRuntimeStatus.SUCCEEDED,
            CRMStatus.LEAD_UPDATED: DomainRuntimeStatus.SUCCEEDED,
            CRMStatus.OPPORTUNITY_CREATED: DomainRuntimeStatus.SUCCEEDED,
            CRMStatus.OPPORTUNITY_UPDATED: DomainRuntimeStatus.SUCCEEDED,
            CRMStatus.HANDOVER_CREATED: DomainRuntimeStatus.SUCCEEDED,
            CRMStatus.HANDOVER_RESOLVED: DomainRuntimeStatus.SUCCEEDED,
            CRMStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
            CRMStatus.FAILED: DomainRuntimeStatus.FAILED,
        }
        return DomainRuntimeResult(
            request_id=self.request_id,
            action_code=self.action_code,
            status=domain_status_map.get(self.status, DomainRuntimeStatus.FAILED),
            output={
                "status": self.status.value,
                "error": self.error,
            },
            error=self.error,
            metadata=self.metadata,
        )
