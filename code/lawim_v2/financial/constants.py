from __future__ import annotations

FINANCIAL_CURRENCIES: frozenset[str] = frozenset({"XAF"})

QUOTE_STATUSES: frozenset[str] = frozenset({"DRAFT", "ISSUED", "VIEWED", "ACCEPTED", "REJECTED", "EXPIRED", "CANCELLED", "CONVERTED"})
INVOICE_STATUSES: frozenset[str] = frozenset({"DRAFT", "ISSUED", "PARTIALLY_PAID", "PAID", "OVERDUE", "CANCELLED", "VOID", "REFUNDED", "PARTIALLY_REFUNDED"})
CREDIT_NOTE_STATUSES: frozenset[str] = frozenset({"DRAFT", "ISSUED", "VALIDATED", "CANCELLED"})
RECEIPT_STATUSES: frozenset[str] = frozenset({"DRAFT", "GENERATED", "ARCHIVED", "VOID"})
PAYMENT_INTENT_STATUSES: frozenset[str] = frozenset({"CREATED", "PENDING", "PROCESSING", "REQUIRES_ACTION", "SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED"})
PAYMENT_ATTEMPT_STATUSES: frozenset[str] = frozenset({"PENDING", "PROCESSING", "SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED"})
PAYMENT_TRANSACTION_STATUSES: frozenset[str] = frozenset({"PENDING", "PROCESSING", "SUCCESSFUL", "FAILED", "CANCELLED", "EXPIRED", "REVERSED", "PARTIALLY_REFUNDED", "REFUNDED"})
PAYMENT_TRANSACTION_TYPES: frozenset[str] = frozenset({"collection", "refund", "cancel", "adjustment", "payout", "fee", "commission", "charge"})
REFUND_STATUSES: frozenset[str] = frozenset({"REQUESTED", "UNDER_REVIEW", "APPROVED", "REJECTED", "PROCESSING", "SUCCEEDED", "FAILED", "CANCELLED"})
SUBSCRIPTION_PLAN_FREQUENCIES: frozenset[str] = frozenset({"DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "SEMI_ANNUAL", "ANNUAL", "CUSTOM"})
SUBSCRIPTION_STATUSES: frozenset[str] = frozenset({"PENDING", "TRIAL", "ACTIVE", "PAST_DUE", "SUSPENDED", "CANCELLED", "EXPIRED", "TERMINATED"})
SUBSCRIPTION_CYCLE_STATUSES: frozenset[str] = frozenset({"DRAFT", "INVOICE_CREATED", "PAYMENT_PENDING", "PAID", "FAILED", "EXPIRED", "CANCELLED"})
COMMISSION_STATUSES: frozenset[str] = frozenset({"CALCULATED", "PENDING_VALIDATION", "VALIDATED", "PAYABLE", "SCHEDULED", "PAID", "CANCELLED", "DISPUTED", "REVERSED"})
PAYOUT_STATUSES: frozenset[str] = frozenset({"DRAFT", "APPROVED", "PROCESSING", "PAID", "FAILED", "CANCELLED"})
RECONCILIATION_STATUSES: frozenset[str] = frozenset({"MATCHED", "PARTIALLY_MATCHED", "UNMATCHED", "CONFLICT", "MANUAL_REVIEW", "RESOLVED"})

PAYMENT_PROVIDER_CODES: frozenset[str] = frozenset({"CAMPAY", "MANUAL"})

FINANCIAL_LEDGER_ACCOUNT_CODES: tuple[tuple[str, str], ...] = (
    ("AR", "creances_clients"),
    ("PAYMENT_PENDING", "paiements_en_attente"),
    ("CASH_CONFIRMED", "encaissements_confirmes"),
    ("LAWIM_REVENUE", "revenus_lawim"),
    ("COMMISSIONS_PAYABLE", "commissions_a_payer"),
    ("PAYOUTS", "reversements"),
    ("REFUNDS", "remboursements"),
    ("PROVIDER_FEES", "frais_fournisseur"),
    ("TAXES", "taxes_collectees"),
    ("ADJUSTMENTS", "ajustements"),
    ("RECONCILIATION_LOSSES", "pertes_ecarts_rapprochement"),
)

FINANCIAL_EVENT_TYPES: tuple[str, ...] = (
    "quote.created",
    "quote.issued",
    "quote.accepted",
    "quote.rejected",
    "quote.expired",
    "invoice.created",
    "invoice.issued",
    "invoice.overdue",
    "invoice.paid",
    "payment.intent.created",
    "payment.pending",
    "payment.succeeded",
    "payment.failed",
    "payment.expired",
    "payment.refunded",
    "receipt.generated",
    "subscription.created",
    "subscription.activated",
    "subscription.renewed",
    "subscription.past_due",
    "subscription.suspended",
    "subscription.cancelled",
    "commission.calculated",
    "commission.validated",
    "commission.payable",
    "commission.paid",
    "reconciliation.conflict",
    "reconciliation.resolved",
    "refund.requested",
    "refund.approved",
    "refund.processed",
    "ledger.entry.created",
    "provider.event.received",
)
