from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class TransactionStatus(str, Enum):
    DRAFT = "DRAFT"
    PREPARED = "PREPARED"
    PRECONDITIONS_CHECKING = "PRECONDITIONS_CHECKING"
    NEGOTIATING = "NEGOTIATING"
    AGREED = "AGREED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"
    SIMULATED = "SIMULATED"


@dataclass
class NegotiationEntry:
    entry_id: str = ""
    party: str = ""
    offer_amount: float = 0.0
    terms: dict[str, Any] = field(default_factory=dict)
    proposed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: str = ""


@dataclass
class TransactionData:
    transaction_id: str = ""
    project_id: str = ""
    property_id: str = ""
    buyer_id: str = ""
    seller_id: str = ""
    amount: float = 0.0
    currency: str = "XAF"
    stage: str = ""
    status: TransactionStatus = TransactionStatus.DRAFT
    negotiation_history: list[NegotiationEntry] = field(default_factory=list)
    terms: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class TransactionRequest:
    request_id: str = ""
    action_code: str = ""
    project_id: str = ""
    transaction_id: str = ""
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
                "transaction_id": self.transaction_id,
                **self.data,
            },
            correlation_id=self.correlation_id,
            idempotency_key=self.idempotency_key,
            metadata=self.metadata,
        )


@dataclass
class TransactionResult:
    request_id: str = ""
    action_code: str = ""
    status: TransactionStatus = TransactionStatus.FAILED
    transaction: TransactionData | None = None
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            TransactionStatus.DRAFT: DomainRuntimeStatus.PENDING,
            TransactionStatus.PREPARED: DomainRuntimeStatus.SUCCEEDED,
            TransactionStatus.PRECONDITIONS_CHECKING: DomainRuntimeStatus.RUNNING,
            TransactionStatus.NEGOTIATING: DomainRuntimeStatus.RUNNING,
            TransactionStatus.AGREED: DomainRuntimeStatus.SUCCEEDED,
            TransactionStatus.CONFIRMED: DomainRuntimeStatus.SUCCEEDED,
            TransactionStatus.COMPLETED: DomainRuntimeStatus.SUCCEEDED,
            TransactionStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
            TransactionStatus.FAILED: DomainRuntimeStatus.FAILED,
            TransactionStatus.CANCELLED: DomainRuntimeStatus.FAILED,
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
