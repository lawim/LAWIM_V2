from __future__ import annotations

from ..errors import ConflictError, NotFoundError, RepositoryError, ValidationError


class FinancialError(RepositoryError):
    code = "financial_error"


class FinancialNotFound(NotFoundError):
    code = "financial_not_found"


class InvoiceAlreadyPaid(ConflictError):
    code = "invoice_already_paid"


class InvoiceNotPayable(ValidationError):
    code = "invoice_not_payable"


class PaymentAmountMismatch(ValidationError):
    code = "payment_amount_mismatch"


class PaymentAlreadyProcessed(ConflictError):
    code = "payment_already_processed"


class InvalidPaymentTransition(ConflictError):
    code = "invalid_payment_transition"


class PaymentProviderUnavailable(ValidationError):
    code = "payment_provider_unavailable"


class RefundAmountExceeded(ValidationError):
    code = "refund_amount_exceeded"


class SubscriptionAlreadyRenewed(ConflictError):
    code = "subscription_already_renewed"


class SubscriptionNotEligible(ValidationError):
    code = "subscription_not_eligible"


class CommissionAlreadyPaid(ConflictError):
    code = "commission_already_paid"


class CommissionNotPayable(ValidationError):
    code = "commission_not_payable"


class QuoteExpired(ValidationError):
    code = "quote_expired"


class DuplicateIdempotencyKey(ConflictError):
    code = "duplicate_idempotency_key"


class ReconciliationConflict(ConflictError):
    code = "reconciliation_conflict"


class CurrencyMismatch(ValidationError):
    code = "currency_mismatch"


class PermissionDenied(ValidationError):
    code = "permission_denied"
