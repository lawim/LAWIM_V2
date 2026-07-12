from __future__ import annotations

from ..program_m_support import COMMON_TABLE_COLUMNS, build_postgresql_statements, build_sqlite_tables_script

FINANCIAL_TABLE_NAMES: tuple[str, ...] = (
    "financial_products",
    "financial_pricing_rules",
    "financial_quotes",
    "financial_quote_lines",
    "financial_invoices",
    "financial_invoice_lines",
    "financial_credit_notes",
    "financial_credit_note_lines",
    "financial_receipts",
    "financial_payment_providers",
    "financial_payment_intents",
    "financial_payment_attempts",
    "financial_payment_transactions",
    "financial_provider_events",
    "financial_refunds",
    "financial_subscription_plans",
    "financial_subscriptions",
    "financial_subscription_cycles",
    "financial_commission_rules",
    "financial_commissions",
    "financial_payouts",
    "financial_ledger_accounts",
    "financial_ledger_entries",
    "financial_reconciliation_records",
    "financial_audit_events",
)

FINANCIAL_TABLE_COLUMNS: tuple[str, ...] = COMMON_TABLE_COLUMNS

SQLITE_V20_TABLES_SCRIPT = build_sqlite_tables_script(FINANCIAL_TABLE_NAMES)
POSTGRESQL_V20_STATEMENTS = build_postgresql_statements(FINANCIAL_TABLE_NAMES)

