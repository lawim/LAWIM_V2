from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    PREPARED = "PREPARED"
    SCHEDULED = "SCHEDULED"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    READ = "READ"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    SIMULATED = "SIMULATED"


@dataclass
class NotificationData:
    notification_id: str = ""
    project_id: str = ""
    recipient_type: str = ""
    channel: str = ""
    template_name: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    priority: int = 0
    scheduled_at: str = ""
    status: NotificationStatus = NotificationStatus.PENDING


@dataclass
class NotificationRequest:
    request_id: str = ""
    action_code: str = ""
    data: NotificationData = field(default_factory=NotificationData)
    correlation_id: str = ""
    idempotency_key: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_request(self) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id=self.request_id,
            action_code=self.action_code,
            parameters={
                "notification_id": self.data.notification_id,
                "project_id": self.data.project_id,
                "recipient_type": self.data.recipient_type,
                "channel": self.data.channel,
                "template_name": self.data.template_name,
                "parameters": self.data.parameters,
                "priority": self.data.priority,
                "scheduled_at": self.data.scheduled_at,
                "status": self.data.status.value if self.data.status else NotificationStatus.PENDING.value,
            },
            correlation_id=self.correlation_id,
            idempotency_key=self.idempotency_key,
            metadata=self.metadata,
        )


@dataclass
class NotificationResult:
    request_id: str = ""
    action_code: str = ""
    status: NotificationStatus = NotificationStatus.PENDING
    notification_id: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            NotificationStatus.PENDING: DomainRuntimeStatus.PENDING,
            NotificationStatus.PREPARED: DomainRuntimeStatus.SUCCEEDED,
            NotificationStatus.SCHEDULED: DomainRuntimeStatus.SUCCEEDED,
            NotificationStatus.SENT: DomainRuntimeStatus.SUCCEEDED,
            NotificationStatus.DELIVERED: DomainRuntimeStatus.SUCCEEDED,
            NotificationStatus.READ: DomainRuntimeStatus.SUCCEEDED,
            NotificationStatus.FAILED: DomainRuntimeStatus.FAILED,
            NotificationStatus.CANCELLED: DomainRuntimeStatus.SUCCEEDED,
            NotificationStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
        }
        return DomainRuntimeResult(
            request_id=self.request_id,
            action_code=self.action_code,
            status=domain_status_map.get(self.status, DomainRuntimeStatus.FAILED),
            output={
                "status": self.status.value,
                "notification_id": self.notification_id,
            },
            error=self.error,
            metadata=self.metadata,
        )
