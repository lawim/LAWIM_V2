from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class PaymentStatus(str, Enum):
    CREATED = "CREATED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    UNKNOWN = "UNKNOWN"
    PENDING_EXTERNAL_CONFIRMATION = "PENDING_EXTERNAL_CONFIRMATION"
    SIMULATED = "SIMULATED"


@dataclass
class PaymentData:
    payment_id: str = ""
    project_id: str = ""
    transaction_id: str = ""
    amount: float = 0.0
    currency: str = "XAF"
    provider: str = ""
    provider_payment_id: str = ""
    status: PaymentStatus = PaymentStatus.CREATED
    idempotency_key: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PaymentIntent:
    intent_id: str = ""
    project_id: str = ""
    amount: float = 0.0
    currency: str = "XAF"
    idempotency_key: str = ""
    status: PaymentStatus = PaymentStatus.CREATED
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PaymentRequest:
    request_id: str = ""
    action_code: str = ""
    project_id: str = ""
    payment_id: str = ""
    intent_id: str = ""
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
                "payment_id": self.payment_id,
                "intent_id": self.intent_id,
                **self.data,
            },
            correlation_id=self.correlation_id,
            idempotency_key=self.idempotency_key,
            metadata=self.metadata,
        )


@dataclass
class PaymentResult:
    request_id: str = ""
    action_code: str = ""
    status: PaymentStatus = PaymentStatus.FAILED
    payment: PaymentData | None = None
    intent: PaymentIntent | None = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            PaymentStatus.CREATED: DomainRuntimeStatus.PENDING,
            PaymentStatus.PENDING: DomainRuntimeStatus.RUNNING,
            PaymentStatus.PROCESSING: DomainRuntimeStatus.RUNNING,
            PaymentStatus.SUCCEEDED: DomainRuntimeStatus.SUCCEEDED,
            PaymentStatus.FAILED: DomainRuntimeStatus.FAILED,
            PaymentStatus.CANCELLED: DomainRuntimeStatus.FAILED,
            PaymentStatus.REFUNDED: DomainRuntimeStatus.SUCCEEDED,
            PaymentStatus.UNKNOWN: DomainRuntimeStatus.PENDING,
            PaymentStatus.PENDING_EXTERNAL_CONFIRMATION: DomainRuntimeStatus.PENDING,
            PaymentStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
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
