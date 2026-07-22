from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class PaymentEventType(str, Enum):
    PAYMENT_INTENT_CREATED = "PAYMENT_INTENT_CREATED"
    PAYMENT_PENDING = "PAYMENT_PENDING"
    PAYMENT_PROCESSING = "PAYMENT_PROCESSING"
    PAYMENT_SUCCEEDED = "PAYMENT_SUCCEEDED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAYMENT_CANCELLED = "PAYMENT_CANCELLED"
    PAYMENT_REFUNDED = "PAYMENT_REFUNDED"
    PAYMENT_STATUS_UNKNOWN = "PAYMENT_STATUS_UNKNOWN"
    PAYMENT_RECONCILED = "PAYMENT_RECONCILED"
    PAYMENT_COMPENSATED = "PAYMENT_COMPENSATED"


@dataclass(frozen=True)
class PaymentEvent:
    event_type: PaymentEventType = PaymentEventType.PAYMENT_INTENT_CREATED
    payment_id: str = ""
    intent_id: str = ""
    project_id: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "payment", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "payment_id": self.payment_id,
                "intent_id": self.intent_id,
                "project_id": self.project_id,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
