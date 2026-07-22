from __future__ import annotations

from .v2_matching import V2MatchingAdapter
from .v2_visit import V2VisitAdapter
from .v2_crm import V2CRMAdapter
from .v2_notification import V2NotificationAdapter
from .v2_document import V2DocumentAdapter
from .v2_verification import V2VerificationAdapter
from .v2_transaction import V2TransactionAdapter
from .v2_payment import V2PaymentAdapter

__all__ = [
    "V2MatchingAdapter",
    "V2VisitAdapter",
    "V2CRMAdapter",
    "V2NotificationAdapter",
    "V2DocumentAdapter",
    "V2VerificationAdapter",
    "V2TransactionAdapter",
    "V2PaymentAdapter",
]
