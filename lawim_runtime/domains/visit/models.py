from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class VisitStatus(str, Enum):
    PENDING = "PENDING"
    AVAILABILITY_CHECKING = "AVAILABILITY_CHECKING"
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    NO_SHOW = "NO_SHOW"
    DOMAIN_PROVIDER_REQUIRED = "DOMAIN_PROVIDER_REQUIRED"
    SIMULATED = "SIMULATED"
    FAILED = "FAILED"

    @property
    def is_terminal(self) -> bool:
        return self in {
            VisitStatus.COMPLETED,
            VisitStatus.CANCELLED,
            VisitStatus.REJECTED,
            VisitStatus.NO_SHOW,
            VisitStatus.DOMAIN_PROVIDER_REQUIRED,
            VisitStatus.SIMULATED,
            VisitStatus.FAILED,
        }


@dataclass
class VisitRequestData:
    property_id: str = ""
    requester_name: str = ""
    requester_contact: str = ""
    preferred_dates: list[str] = field(default_factory=list)
    preferred_times: list[str] = field(default_factory=list)
    visit_type: str = "physical"
    notes: str = ""


@dataclass
class VisitRequest:
    request_id: str = ""
    action_code: str = ""
    data: VisitRequestData = field(default_factory=VisitRequestData)
    correlation_id: str = ""
    idempotency_key: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_request(self) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id=self.request_id,
            action_code=self.action_code,
            parameters={
                "property_id": self.data.property_id,
                "requester_name": self.data.requester_name,
                "requester_contact": self.data.requester_contact,
                "preferred_dates": self.data.preferred_dates,
                "preferred_times": self.data.preferred_times,
                "visit_type": self.data.visit_type,
                "notes": self.data.notes,
            },
            correlation_id=self.correlation_id,
            idempotency_key=self.idempotency_key,
            metadata=self.metadata,
        )


@dataclass
class VisitRecord:
    visit_id: str = field(default_factory=lambda: uuid4().hex[:16])
    property_id: str = ""
    requester: str = ""
    scheduled_date: str = ""
    status: VisitStatus = VisitStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class VisitResult:
    request_id: str = ""
    action_code: str = ""
    status: VisitStatus = VisitStatus.PENDING
    visit: VisitRecord | None = None
    visits: list[VisitRecord] = field(default_factory=list)
    availability: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            VisitStatus.PENDING: DomainRuntimeStatus.PENDING,
            VisitStatus.SCHEDULED: DomainRuntimeStatus.SUCCEEDED,
            VisitStatus.CONFIRMED: DomainRuntimeStatus.SUCCEEDED,
            VisitStatus.COMPLETED: DomainRuntimeStatus.SUCCEEDED,
            VisitStatus.CANCELLED: DomainRuntimeStatus.SUCCEEDED,
            VisitStatus.REJECTED: DomainRuntimeStatus.FAILED,
            VisitStatus.NO_SHOW: DomainRuntimeStatus.SUCCEEDED,
            VisitStatus.DOMAIN_PROVIDER_REQUIRED: DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED,
            VisitStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
            VisitStatus.FAILED: DomainRuntimeStatus.FAILED,
            VisitStatus.AVAILABILITY_CHECKING: DomainRuntimeStatus.RUNNING,
        }
        return DomainRuntimeResult(
            request_id=self.request_id,
            action_code=self.action_code,
            status=domain_status_map.get(self.status, DomainRuntimeStatus.PENDING),
            output={
                "status": self.status.value,
                "visit": {
                    "visit_id": self.visit.visit_id,
                    "property_id": self.visit.property_id,
                    "requester": self.visit.requester,
                    "scheduled_date": self.visit.scheduled_date,
                    "status": self.visit.status.value,
                    "created_at": self.visit.created_at,
                    "updated_at": self.visit.updated_at,
                } if self.visit else None,
                "visits": [
                    {
                        "visit_id": v.visit_id,
                        "property_id": v.property_id,
                        "requester": v.requester,
                        "scheduled_date": v.scheduled_date,
                        "status": v.status.value,
                        "created_at": v.created_at,
                        "updated_at": v.updated_at,
                    }
                    for v in self.visits
                ],
                "availability": self.availability,
            },
            error=self.error,
            metadata=self.metadata,
        )
