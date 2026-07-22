from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class TransactionEventType(str, Enum):
    TRANSACTION_PREPARED = "TRANSACTION_PREPARED"
    NEGOTIATION_STARTED = "NEGOTIATION_STARTED"
    NEGOTIATION_UPDATED = "NEGOTIATION_UPDATED"
    TRANSACTION_CONFIRMED = "TRANSACTION_CONFIRMED"
    TRANSACTION_COMPLETED = "TRANSACTION_COMPLETED"
    TRANSACTION_CANCELLED = "TRANSACTION_CANCELLED"
    TRANSACTION_FAILED = "TRANSACTION_FAILED"


@dataclass(frozen=True)
class TransactionEvent:
    event_type: TransactionEventType = TransactionEventType.TRANSACTION_PREPARED
    transaction_id: str = ""
    project_id: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "transaction", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "transaction_id": self.transaction_id,
                "project_id": self.project_id,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
