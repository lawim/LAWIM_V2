from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ServiceOrderStatus(str, Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    DISPUTED = "DISPUTED"
    ARCHIVED = "ARCHIVED"


SERVICE_ORDER_TRANSITIONS: dict[ServiceOrderStatus, list[ServiceOrderStatus]] = {
    ServiceOrderStatus.CREATED: [ServiceOrderStatus.CONFIRMED, ServiceOrderStatus.CANCELLED],
    ServiceOrderStatus.CONFIRMED: [ServiceOrderStatus.IN_PROGRESS, ServiceOrderStatus.CANCELLED],
    ServiceOrderStatus.IN_PROGRESS: [ServiceOrderStatus.COMPLETED, ServiceOrderStatus.CANCELLED, ServiceOrderStatus.DISPUTED],
    ServiceOrderStatus.COMPLETED: [ServiceOrderStatus.ARCHIVED, ServiceOrderStatus.REFUNDED, ServiceOrderStatus.DISPUTED],
    ServiceOrderStatus.CANCELLED: [ServiceOrderStatus.ARCHIVED, ServiceOrderStatus.REFUNDED],
    ServiceOrderStatus.REFUNDED: [ServiceOrderStatus.ARCHIVED],
    ServiceOrderStatus.DISPUTED: [ServiceOrderStatus.IN_PROGRESS, ServiceOrderStatus.REFUNDED, ServiceOrderStatus.COMPLETED],
    ServiceOrderStatus.ARCHIVED: [],
}


class PaymentState(str, Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    REFUNDED = "REFUNDED"
    EXPIRED = "EXPIRED"
    DISPUTED = "DISPUTED"
    ARCHIVED = "ARCHIVED"


PAYMENT_TRANSITIONS: dict[PaymentState, list[PaymentState]] = {
    PaymentState.INITIATED: [PaymentState.PENDING, PaymentState.CANCELLED],
    PaymentState.PENDING: [PaymentState.PROCESSING, PaymentState.CANCELLED, PaymentState.EXPIRED],
    PaymentState.PROCESSING: [PaymentState.CONFIRMED, PaymentState.FAILED, PaymentState.DISPUTED],
    PaymentState.CONFIRMED: [PaymentState.REFUNDED, PaymentState.ARCHIVED],
    PaymentState.FAILED: [PaymentState.INITIATED, PaymentState.ARCHIVED],
    PaymentState.CANCELLED: [PaymentState.ARCHIVED],
    PaymentState.REFUNDED: [PaymentState.ARCHIVED],
    PaymentState.EXPIRED: [PaymentState.INITIATED, PaymentState.ARCHIVED],
    PaymentState.DISPUTED: [PaymentState.REFUNDED, PaymentState.CONFIRMED],
    PaymentState.ARCHIVED: [],
}


class VisitStatus(str, Enum):
    REQUESTED = "REQUESTED"
    SCHEDULED = "SCHEDULED"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


VISIT_TRANSITIONS: dict[VisitStatus, list[VisitStatus]] = {
    VisitStatus.REQUESTED: [VisitStatus.SCHEDULED, VisitStatus.CANCELLED],
    VisitStatus.SCHEDULED: [VisitStatus.CONFIRMED, VisitStatus.CANCELLED],
    VisitStatus.CONFIRMED: [VisitStatus.COMPLETED, VisitStatus.NO_SHOW, VisitStatus.CANCELLED],
    VisitStatus.COMPLETED: [],
    VisitStatus.CANCELLED: [],
    VisitStatus.NO_SHOW: [VisitStatus.SCHEDULED],
}


@dataclass
class ServiceOrder:
    order_id: str = ""
    service_type: str = ""
    status: ServiceOrderStatus = ServiceOrderStatus.CREATED
    property_id: int | None = None
    provider_id: int | None = None
    requester_id: int | None = None
    price: float = 0.0
    currency: str = "XAF"
    payment_state: PaymentState = PaymentState.INITIATED

    def can_transition(self, target: ServiceOrderStatus) -> bool:
        return target in SERVICE_ORDER_TRANSITIONS.get(self.status, [])

    def transition(self, target: ServiceOrderStatus) -> ServiceOrderStatus:
        if self.can_transition(target):
            self.status = target
        return self.status


@dataclass
class Visit:
    visit_id: str = ""
    property_id: int = 0
    requester_id: int = 0
    agent_id: int | None = None
    status: VisitStatus = VisitStatus.REQUESTED
    scheduled_at: str = ""
    is_counter_visit: bool = False
    original_visit_id: str = ""

    def can_transition(self, target: VisitStatus) -> bool:
        return target in VISIT_TRANSITIONS.get(self.status, [])

    def transition(self, target: VisitStatus) -> VisitStatus:
        if self.can_transition(target):
            self.status = target
        return self.status


@dataclass
class BoostPurchase:
    days: int = 7
    price: float = 2000
    boost_level: int = 1
    expires_at: str = ""


@dataclass
class PremiumListing:
    is_premium: bool = False
    price: float = 10000
    badge: str = "PREMIUM"
    ranking_boost: float = 1.5
    expires_at: str = ""


@dataclass
class LeadPurchase:
    purchase_id: str = ""
    tier: str = "bronze"
    count: int = 1
    price: float = 500
    agent_id: int = 0

    @staticmethod
    def pack_options() -> list[dict[str, Any]]:
        return [
            {"tier": "bronze", "count": 1, "price": 500},
            {"tier": "silver", "count": 5, "price": 1500},
            {"tier": "gold", "count": 15, "price": 3000},
        ]
