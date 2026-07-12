from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

from ..errors import NotFoundError, ValidationError
from ..repository_introspection import table_exists
from ..user_roles import resolve_official_user_role
from .constants import (
    COMMISSION_STATUSES,
    CREDIT_NOTE_STATUSES,
    FINANCIAL_CURRENCIES,
    FINANCIAL_EVENT_TYPES,
    FINANCIAL_LEDGER_ACCOUNT_CODES,
    INVOICE_STATUSES,
    PAYMENT_ATTEMPT_STATUSES,
    PAYMENT_INTENT_STATUSES,
    PAYMENT_PROVIDER_CODES,
    PAYMENT_TRANSACTION_STATUSES,
    PAYMENT_TRANSACTION_TYPES,
    PAYOUT_STATUSES,
    QUOTE_STATUSES,
    RECEIPT_STATUSES,
    RECONCILIATION_STATUSES,
    REFUND_STATUSES,
    SUBSCRIPTION_CYCLE_STATUSES,
    SUBSCRIPTION_PLAN_FREQUENCIES,
    SUBSCRIPTION_STATUSES,
)
from .engines import FINANCIAL_ENGINE
from .exceptions import (
    CommissionAlreadyPaid,
    CommissionNotPayable,
    CurrencyMismatch,
    DuplicateIdempotencyKey,
    InvalidPaymentTransition,
    InvoiceAlreadyPaid,
    InvoiceNotPayable,
    PaymentAmountMismatch,
    PaymentAlreadyProcessed,
    PaymentProviderUnavailable,
    QuoteExpired,
    ReconciliationConflict,
    RefundAmountExceeded,
    SubscriptionAlreadyRenewed,
    SubscriptionNotEligible,
)
from .schema_v20_ddl import FINANCIAL_TABLE_NAMES


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None, fallback: Any) -> Any:
    if value in (None, ""):
        return fallback
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return fallback


def _normalize_code(value: object, *, default: str = "") -> str:
    text = str(value or "").strip().upper()
    return text or default


def _normalize_currency(value: object | None) -> str:
    currency = _normalize_code(value, default="XAF")
    if currency not in FINANCIAL_CURRENCIES:
        raise CurrencyMismatch(f"Unsupported currency: {currency}")
    return currency


def _document_number(prefix: str, record_id: int, created_at: str) -> str:
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    except ValueError:
        created = datetime.now(timezone.utc)
    return f"{prefix}-{created.astimezone(timezone.utc).year}-{record_id:06d}"


def _record_key(prefix: str, *parts: object) -> str:
    payload = "|".join(str(part).strip() for part in parts if str(part).strip())
    if not payload:
        payload = uuid.uuid4().hex
    digest = FINANCIAL_ENGINE.build_reference(prefix, payload).split("-", 1)[-1]
    return f"{prefix}-{digest}"


def _safe_role(actor: dict[str, object] | None) -> str:
    if actor is None:
        return ""
    return resolve_official_user_role(actor.get("role"))


class FinancialRepositoryMixin:
    def financial_tables_present(self) -> bool:
        return table_exists(self, "financial_products")

    # ------------------------------------------------------------------
    # Generic helpers
    # ------------------------------------------------------------------

    def _financial_row(self, row: dict[str, object] | None) -> dict[str, object] | None:
        if row is None:
            return None
        payload = _parse_json(str(row.get("payload_json") or "{}"), {})
        enriched = dict(row)
        enriched["payload"] = payload if isinstance(payload, dict) else {}
        if isinstance(payload, dict):
            for key, value in payload.items():
                enriched.setdefault(key, value)
        return enriched

    def _financial_rows(self, rows: list[dict[str, object]]) -> list[dict[str, object]]:
        return [row for row in (self._financial_row(row) for row in rows) if row is not None]

    def _financial_get(self, table: str, *, record_id: int | None = None, record_key: str | None = None) -> dict[str, object]:
        if record_id is not None:
            row = self.one(f"SELECT * FROM {table} WHERE id = ?", (record_id,))
        elif record_key is not None:
            row = self.one(f"SELECT * FROM {table} WHERE record_key = ?", (record_key,))
        else:
            row = None
        enriched = self._financial_row(row)
        if enriched is None:
            raise NotFoundError(f"{table.replace('_', ' ')} not found")
        return enriched

    def _financial_list(
        self,
        table: str,
        *,
        status: str | None = None,
        limit: int = 50,
        parent_id: int | None = None,
        reference_id: int | None = None,
        secondary_id: int | None = None,
        owner_user_id: int | None = None,
        organization_id: int | None = None,
        payload_filters: dict[str, object] | None = None,
    ) -> list[dict[str, object]]:
        rows = self.all(f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?", (limit,))
        items = self._financial_rows(rows)
        if status is not None:
            items = [row for row in items if _normalize_code(row.get("status")) == _normalize_code(status)]
        if parent_id is not None:
            items = [row for row in items if int(row.get("parent_id") or 0) == int(parent_id)]
        if reference_id is not None:
            items = [row for row in items if int(row.get("reference_id") or 0) == int(reference_id)]
        if secondary_id is not None:
            items = [row for row in items if int(row.get("secondary_id") or 0) == int(secondary_id)]
        if owner_user_id is not None:
            items = [row for row in items if int((row.get("payload") or {}).get("owner_user_id") or 0) == int(owner_user_id)]
        if organization_id is not None:
            items = [row for row in items if int((row.get("payload") or {}).get("organization_id") or 0) == int(organization_id)]
        if payload_filters:
            filtered: list[dict[str, object]] = []
            for row in items:
                payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
                if all(payload.get(key) == value for key, value in payload_filters.items()):
                    filtered.append(row)
            items = filtered
        return items

    def _insert_financial_record(
        self,
        table: str,
        *,
        name: str,
        kind: str,
        scope: str,
        status: str,
        payload: dict[str, object] | None = None,
        record_key: str | None = None,
        parent_id: int | None = None,
        reference_id: int | None = None,
        secondary_id: int | None = None,
        number_prefix: str | None = None,
    ) -> dict[str, object]:
        key = record_key or _record_key(table.replace("_", "-"), name, kind, scope, status, parent_id, reference_id, secondary_id, payload or {})
        payload_data = dict(payload or {})
        payload_data.setdefault("idempotency_key", payload_data.get("idempotency_key"))
        now = _utcnow()
        with self._transaction() as conn:
            existing = self.one(f"SELECT * FROM {table} WHERE record_key = ?", (key,))
            if existing is not None:
                return self._financial_row(existing) or dict(existing)
            conn.execute(
                f"""
                INSERT INTO {table} (
                    record_key, name, kind, scope, status, parent_id, reference_id, secondary_id,
                    payload_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    name,
                    kind,
                    scope,
                    status,
                    parent_id,
                    reference_id,
                    secondary_id,
                    _json(payload_data),
                    now,
                    now,
                ),
            )
            row = self.one(f"SELECT * FROM {table} WHERE record_key = ?", (key,))
            assert row is not None
            if number_prefix:
                number = _document_number(number_prefix, int(row["id"]), str(row["created_at"]))
                payload_data["number"] = number
                payload_data.setdefault("document_number", number)
                conn.execute(
                    f"UPDATE {table} SET name = ?, payload_json = ?, updated_at = ? WHERE id = ?",
                    (number, _json(payload_data), _utcnow(), int(row["id"])),
                )
                row = self.one(f"SELECT * FROM {table} WHERE id = ?", (int(row["id"]),))
                assert row is not None
        enriched = self._financial_row(row)
        assert enriched is not None
        return enriched

    def _update_financial_record(self, table: str, record_id: int, **fields: object) -> dict[str, object]:
        record = self._financial_get(table, record_id=record_id)
        payload = dict(record.get("payload") or {})
        for key, value in fields.items():
            if key == "payload" and isinstance(value, dict):
                payload.update(value)
            elif key in {"name", "kind", "scope", "status", "parent_id", "reference_id", "secondary_id"}:
                record[key] = value
            elif value is not None:
                payload[key] = value
        updated_name = str(record.get("name") or payload.get("number") or "")
        updated_kind = str(record.get("kind") or "")
        updated_scope = str(record.get("scope") or "")
        updated_status = _normalize_code(record.get("status"), default="ACTIVE")
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                f"""
                UPDATE {table}
                SET name = ?, kind = ?, scope = ?, status = ?, parent_id = ?, reference_id = ?, secondary_id = ?,
                    payload_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    updated_name,
                    updated_kind,
                    updated_scope,
                    updated_status,
                    record.get("parent_id"),
                    record.get("reference_id"),
                    record.get("secondary_id"),
                    _json(payload),
                    now,
                    record_id,
                ),
            )
        return self._financial_get(table, record_id=record_id)

    def _set_number(self, table: str, record_id: int, prefix: str) -> dict[str, object]:
        record = self._financial_get(table, record_id=record_id)
        payload = dict(record.get("payload") or {})
        number = _document_number(prefix, int(record["id"]), str(record["created_at"]))
        payload["number"] = number
        with self._transaction() as conn:
            conn.execute(
                f"UPDATE {table} SET name = ?, payload_json = ?, updated_at = ? WHERE id = ?",
                (number, _json(payload), _utcnow(), record_id),
            )
        return self._financial_get(table, record_id=record_id)

    def _ensure_currency(self, currency: object | None) -> str:
        return _normalize_currency(currency)

    def _get_payload_amount(self, row: dict[str, object]) -> int:
        payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
        amount = payload.get("amount_minor")
        if amount is None:
            amount = payload.get("total_minor")
        if amount is None:
            amount = payload.get("gross_amount_minor")
        return int(amount or 0)

    def _record_audit(self, action: str, *, actor_user_id: int | None, object_type: str, object_id: int | None, previous_state: dict[str, object] | None, new_state: dict[str, object] | None, reason: str = "", result: str = "success", correlation_id: str | None = None) -> dict[str, object]:
        payload = {
            "action": action,
            "actor_user_id": actor_user_id,
            "object_type": object_type,
            "object_id": object_id,
            "previous_state": previous_state or {},
            "new_state": new_state or {},
            "reason": reason,
            "result": result,
            "correlation_id": correlation_id,
        }
        return self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action=action,
            object_type=object_type,
            object_id=object_id,
            previous_state=previous_state or {},
            new_state=new_state or {},
            reason=reason,
            result=result,
            correlation_id=correlation_id,
            payload=payload,
        )

    # ------------------------------------------------------------------
    # Seeding
    # ------------------------------------------------------------------

    def seed_financial_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM financial_payment_providers") > 0:
            return
        now = _utcnow()
        with self._transaction() as conn:
            for account_code, label in FINANCIAL_LEDGER_ACCOUNT_CODES:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO financial_ledger_accounts (
                        record_key, name, kind, scope, status, payload_json, created_at, updated_at
                    ) VALUES (?, ?, 'ledger_account', 'system', 'active', ?, ?, ?)
                    """,
                    (
                        f"ledger-account:{account_code}",
                        label,
                        _json({"account_code": account_code, "currency": "XAF", "balance_minor": 0}),
                        now,
                        now,
                    ),
                )
            conn.execute(
                """
                INSERT OR IGNORE INTO financial_payment_providers (
                    record_key, name, kind, scope, status, payload_json, created_at, updated_at
                ) VALUES (?, ?, 'payment_provider', 'sandbox', 'inactive', ?, ?, ?)
                """,
                (
                    "provider:CAMPAY",
                    "Campay",
                    _json(
                        {
                            "provider_code": "CAMPAY",
                            "environment": "sandbox",
                            "supported_currencies": ["XAF"],
                            "supported_channels": ["mobile_money"],
                            "supports_collection": True,
                            "supports_refund": False,
                            "supports_status_query": True,
                            "supports_webhook": True,
                            "supports_payout": True,
                            "priority": 10,
                            "configuration_state": "disabled",
                            "last_health_check": None,
                            "details": {"sandbox_only": True},
                        }
                    ),
                    now,
                    now,
                ),
            )
        self.record_event("financial_catalog_seeded", {"ledger_accounts": len(FINANCIAL_LEDGER_ACCOUNT_CODES), "providers": 1})

    # ------------------------------------------------------------------
    # Catalog and pricing
    # ------------------------------------------------------------------

    def create_financial_product(
        self,
        *,
        code: str,
        name: str,
        description: str = "",
        category: str = "service",
        status: str = "active",
        unit: str = "item",
        default_price_minor: int = 0,
        currency: str = "XAF",
        tax_rate_bps: int = 0,
        duration_days: int | None = None,
        billing_period: str | None = None,
        eligible_roles: list[str] | None = None,
        valid_from: str | None = None,
        valid_until: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = {
            "code": code,
            "description": description,
            "category": category,
            "unit": unit,
            "default_price_minor": max(0, int(default_price_minor)),
            "currency": self._ensure_currency(currency),
            "tax_rate_bps": max(0, int(tax_rate_bps)),
            "duration_days": duration_days,
            "billing_period": billing_period,
            "eligible_roles": eligible_roles or [],
            "valid_from": valid_from,
            "valid_until": valid_until,
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_products",
            name=name,
            kind="financial_product",
            scope=category,
            status=status.upper() if status.isupper() else status,
            payload=payload,
            record_key=f"financial-product:{code.lower()}",
            number_prefix="PROD",
        )

    def list_financial_products(self, *, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_products", status=status, limit=limit)

    def get_financial_product(self, product_id: int) -> dict[str, object]:
        return self._financial_get("financial_products", record_id=product_id)

    def create_pricing_rule(
        self,
        *,
        product_id: int | None = None,
        code: str,
        name: str,
        rule_type: str = "fixed",
        status: str = "active",
        amount_minor: int = 0,
        amount_percent_bps: int = 0,
        fee_minor: int = 0,
        tax_rate_bps: int = 0,
        scope: str = "global",
        priority: int = 100,
        starts_at: str | None = None,
        ends_at: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = {
            "code": code,
            "product_id": product_id,
            "rule_type": rule_type,
            "amount_minor": max(0, int(amount_minor)),
            "amount_percent_bps": max(0, int(amount_percent_bps)),
            "fee_minor": max(0, int(fee_minor)),
            "tax_rate_bps": max(0, int(tax_rate_bps)),
            "priority": int(priority),
            "starts_at": starts_at,
            "ends_at": ends_at,
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_pricing_rules",
            name=name,
            kind=rule_type,
            scope=scope,
            status=status,
            payload=payload,
            parent_id=product_id,
            record_key=f"pricing-rule:{code.lower()}",
            number_prefix="TAR",
        )

    def list_pricing_rules(self, *, product_id: int | None = None, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_pricing_rules", status=status, limit=limit, parent_id=product_id)

    def calculate_pricing(
        self,
        *,
        line_items: list[dict[str, object]] | None = None,
        discount_minor: int = 0,
        fee_minor: int = 0,
        tax_rate_bps: int = 0,
        currency: str = "XAF",
        context: dict[str, object] | None = None,
    ) -> dict[str, object]:
        breakdown = FINANCIAL_ENGINE.calculate_breakdown(
            line_items=line_items,
            discount_minor=discount_minor,
            fee_minor=fee_minor,
            tax_rate_bps=tax_rate_bps,
            currency=currency,
            context=context,
        )
        return breakdown.to_dict()

    # ------------------------------------------------------------------
    # Quotes and invoices
    # ------------------------------------------------------------------

    def create_quote(
        self,
        *,
        actor_user_id: int | None,
        customer_user_id: int | None,
        organization_id: int | None,
        lines: list[dict[str, object]],
        currency: str = "XAF",
        discount_minor: int = 0,
        fee_minor: int = 0,
        tax_rate_bps: int = 0,
        expires_at: str | None = None,
        business_reference: str | None = None,
        idempotency_key: str | None = None,
        source: str = "internal",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        normalized_currency = self._ensure_currency(currency)
        breakdown = self.calculate_pricing(
            line_items=lines,
            discount_minor=discount_minor,
            fee_minor=fee_minor,
            tax_rate_bps=tax_rate_bps,
            currency=normalized_currency,
            context={"source": source},
        )
        payload = {
            "number": None,
            "actor_user_id": actor_user_id,
            "customer_user_id": customer_user_id,
            "organization_id": organization_id,
            "owner_user_id": customer_user_id,
            "owner_org_id": organization_id,
            "currency": normalized_currency,
            "lines": lines,
            "breakdown": breakdown,
            "discount_minor": discount_minor,
            "fee_minor": fee_minor,
            "tax_rate_bps": tax_rate_bps,
            "expires_at": expires_at,
            "business_reference": business_reference,
            "idempotency_key": idempotency_key,
            "source": source,
            "metadata": metadata or {},
        }
        record_key = _record_key("quote", idempotency_key or business_reference or uuid.uuid4().hex, actor_user_id, customer_user_id, organization_id, normalized_currency, breakdown.get("total_minor"))
        quote = self._insert_financial_record(
            "financial_quotes",
            name="Quote",
            kind="quote",
            scope=source,
            status="DRAFT",
            payload=payload,
            parent_id=customer_user_id,
            reference_id=organization_id,
            secondary_id=actor_user_id,
            record_key=record_key,
            number_prefix="DEV",
        )
        quote = self._financial_get("financial_quotes", record_id=int(quote["id"]))
        quote = self._update_quote_lines(int(quote["id"]), lines=lines)
        return quote

    def _update_quote_lines(self, quote_id: int, *, lines: list[dict[str, object]]) -> dict[str, object]:
        quote = self._financial_get("financial_quotes", record_id=quote_id)
        payload = dict(quote.get("payload") or {})
        payload["lines"] = lines
        payload["line_count"] = len(lines)
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_quotes SET payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), quote_id),
            )
            conn.execute("DELETE FROM financial_quote_lines WHERE parent_id = ?", (quote_id,))
            for position, line in enumerate(lines, start=1):
                line_payload = {
                    "quote_id": quote_id,
                    "position": position,
                    "description": str(line.get("description") or line.get("name") or ""),
                    "service_code": line.get("service_code"),
                    "quantity": int(line.get("quantity") or 1),
                    "unit": str(line.get("unit") or "item"),
                    "unit_price_minor": int(line.get("unit_price_minor") or 0),
                    "discount_minor": int(line.get("discount_minor") or 0),
                    "fee_minor": int(line.get("fee_minor") or 0),
                    "tax_minor": int(line.get("tax_minor") or 0),
                    "total_minor": int(line.get("total_minor") or 0),
                    "business_reference": line.get("business_reference"),
                    "metadata": line.get("metadata") if isinstance(line.get("metadata"), dict) else {},
                }
                conn.execute(
                    """
                    INSERT INTO financial_quote_lines (
                        record_key, name, kind, scope, status, parent_id, reference_id, secondary_id,
                        payload_json, created_at, updated_at
                    ) VALUES (?, ?, 'quote_line', 'quote', 'active', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        _record_key("quote-line", quote_id, position, line_payload.get("description")),
                        line_payload["description"],
                        quote_id,
                        int(line_payload.get("service_code") is not None),
                        position,
                        _json(line_payload),
                        _utcnow(),
                        _utcnow(),
                    ),
                )
        return self._financial_get("financial_quotes", record_id=quote_id)

    def list_quotes(self, *, status: str | None = None, customer_user_id: int | None = None, organization_id: int | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_quotes", status=status, limit=limit, owner_user_id=customer_user_id, organization_id=organization_id)

    def get_quote(self, quote_id: int) -> dict[str, object]:
        quote = self._financial_get("financial_quotes", record_id=quote_id)
        lines = self._financial_list("financial_quote_lines", parent_id=quote_id, limit=200)
        quote["lines"] = [row.get("payload") or {} for row in sorted(lines, key=lambda row: int((row.get("payload") or {}).get("position") or 0))]
        return quote

    def issue_quote(self, quote_id: int) -> dict[str, object]:
        quote = self._financial_get("financial_quotes", record_id=quote_id)
        if _normalize_code(quote.get("status")) not in {"DRAFT", "VIEWED"}:
            raise InvalidPaymentTransition(f"Quote cannot move from {quote.get('status')} to ISSUED")
        quote = self._update_financial_record("financial_quotes", quote_id, status="ISSUED")
        return quote

    def mark_quote_viewed(self, quote_id: int) -> dict[str, object]:
        return self._update_financial_record("financial_quotes", quote_id, status="VIEWED")

    def accept_quote(self, quote_id: int) -> dict[str, object]:
        quote = self._financial_get("financial_quotes", record_id=quote_id)
        if _normalize_code(quote.get("status")) in {"EXPIRED", "REJECTED", "CANCELLED"}:
            raise QuoteExpired("Quote is not accept-able")
        return self._update_financial_record("financial_quotes", quote_id, status="ACCEPTED")

    def reject_quote(self, quote_id: int) -> dict[str, object]:
        return self._update_financial_record("financial_quotes", quote_id, status="REJECTED")

    def expire_quotes(self, *, older_than: str | None = None) -> int:
        rows = self._financial_list("financial_quotes", status="ISSUED", limit=1000)
        updated = 0
        for row in rows:
            expires_at = str((row.get("payload") or {}).get("expires_at") or "")
            if older_than is not None and expires_at and expires_at > older_than:
                continue
            self._update_financial_record("financial_quotes", int(row["id"]), status="EXPIRED")
            updated += 1
        return updated

    def create_invoice(
        self,
        *,
        actor_user_id: int | None,
        customer_user_id: int | None,
        quote_id: int | None = None,
        organization_id: int | None = None,
        lines: list[dict[str, object]],
        currency: str = "XAF",
        amount_paid_minor: int = 0,
        business_reference: str | None = None,
        idempotency_key: str | None = None,
        source: str = "internal",
        status: str = "DRAFT",
        due_at: str | None = None,
        issued_at: str | None = None,
        notes: str = "",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        normalized_currency = self._ensure_currency(currency)
        quote = self._financial_get("financial_quotes", record_id=quote_id) if quote_id else None
        quote_breakdown = dict(quote.get("payload", {}).get("breakdown", {})) if quote else {}
        breakdown = self.calculate_pricing(
            line_items=lines,
            discount_minor=int(quote_breakdown.get("discount_minor") or 0),
            fee_minor=int(quote_breakdown.get("fee_minor") or 0),
            tax_rate_bps=int(quote_breakdown.get("tax_rate_bps") or 0),
            currency=normalized_currency,
            context={"source": source, "quote_id": quote_id},
        )
        if quote_breakdown.get("total_minor") is not None and int(quote_breakdown.get("total_minor") or 0) != int(breakdown.get("total_minor") or 0):
            breakdown["quoted_total_minor"] = int(quote_breakdown.get("total_minor") or 0)
        payload = {
            "actor_user_id": actor_user_id,
            "customer_user_id": customer_user_id,
            "quote_id": quote_id,
            "organization_id": organization_id,
            "owner_user_id": customer_user_id,
            "owner_org_id": organization_id,
            "currency": normalized_currency,
            "lines": lines,
            "breakdown": breakdown,
            "amount_paid_minor": int(amount_paid_minor),
            "balance_minor": max(0, int(breakdown.get("total_minor") or 0) - int(amount_paid_minor)),
            "business_reference": business_reference,
            "idempotency_key": idempotency_key,
            "source": source,
            "due_at": due_at,
            "issued_at": issued_at,
            "notes": notes,
            "metadata": metadata or {},
        }
        record_key = _record_key("invoice", idempotency_key or business_reference or uuid.uuid4().hex, actor_user_id, customer_user_id, quote_id, organization_id, normalized_currency, breakdown.get("total_minor"))
        invoice = self._insert_financial_record(
            "financial_invoices",
            name="Invoice",
            kind="invoice",
            scope=source,
            status=status,
            payload=payload,
            parent_id=quote_id,
            reference_id=customer_user_id,
            secondary_id=organization_id,
            record_key=record_key,
            number_prefix="FAC",
        )
        invoice = self._update_invoice_lines(int(invoice["id"]), lines=lines)
        return invoice

    def _update_invoice_lines(self, invoice_id: int, *, lines: list[dict[str, object]]) -> dict[str, object]:
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        payload = dict(invoice.get("payload") or {})
        payload["lines"] = lines
        payload["line_count"] = len(lines)
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_invoices SET payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), invoice_id),
            )
            conn.execute("DELETE FROM financial_invoice_lines WHERE parent_id = ?", (invoice_id,))
            for position, line in enumerate(lines, start=1):
                line_payload = {
                    "invoice_id": invoice_id,
                    "position": position,
                    "description": str(line.get("description") or line.get("name") or ""),
                    "service_code": line.get("service_code"),
                    "quantity": int(line.get("quantity") or 1),
                    "unit": str(line.get("unit") or "item"),
                    "unit_price_minor": int(line.get("unit_price_minor") or 0),
                    "discount_minor": int(line.get("discount_minor") or 0),
                    "fee_minor": int(line.get("fee_minor") or 0),
                    "tax_minor": int(line.get("tax_minor") or 0),
                    "subtotal_minor": int(line.get("subtotal_minor") or 0),
                    "total_minor": int(line.get("total_minor") or 0),
                    "business_reference": line.get("business_reference"),
                    "metadata": line.get("metadata") if isinstance(line.get("metadata"), dict) else {},
                }
                conn.execute(
                    """
                    INSERT INTO financial_invoice_lines (
                        record_key, name, kind, scope, status, parent_id, reference_id, secondary_id,
                        payload_json, created_at, updated_at
                    ) VALUES (?, ?, 'invoice_line', 'invoice', 'active', ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        _record_key("invoice-line", invoice_id, position, line_payload.get("description")),
                        line_payload["description"],
                        invoice_id,
                        int(line_payload.get("service_code") is not None),
                        position,
                        _json(line_payload),
                        _utcnow(),
                        _utcnow(),
                    ),
                )
        return self._financial_get("financial_invoices", record_id=invoice_id)

    def list_invoices(
        self,
        *,
        status: str | None = None,
        customer_user_id: int | None = None,
        organization_id: int | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        return self._financial_list("financial_invoices", status=status, limit=limit, owner_user_id=customer_user_id, organization_id=organization_id)

    def get_invoice(self, invoice_id: int) -> dict[str, object]:
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        lines = self._financial_list("financial_invoice_lines", parent_id=invoice_id, limit=200)
        invoice["lines"] = [row.get("payload") or {} for row in sorted(lines, key=lambda row: int((row.get("payload") or {}).get("position") or 0))]
        return invoice

    def issue_invoice(self, invoice_id: int, *, issued_at: str | None = None, due_at: str | None = None) -> dict[str, object]:
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        status = _normalize_code(invoice.get("status"))
        if status not in {"DRAFT", "CANCELLED"}:
            if status in {"ISSUED", "PARTIALLY_PAID", "PAID", "OVERDUE", "VOID", "REFUNDED", "PARTIALLY_REFUNDED"}:
                return invoice
            raise InvoiceNotPayable(f"Invoice cannot move from {status} to ISSUED")
        payload = dict(invoice.get("payload") or {})
        payload["issued_at"] = issued_at or payload.get("issued_at") or _utcnow()
        payload["due_at"] = due_at or payload.get("due_at")
        payload["balance_minor"] = max(0, int(payload.get("breakdown", {}).get("total_minor") or 0) - int(payload.get("amount_paid_minor") or 0))
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_invoices SET status = 'ISSUED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), invoice_id),
            )
        return self._financial_get("financial_invoices", record_id=invoice_id)

    def cancel_invoice(self, invoice_id: int, *, reason: str = "") -> dict[str, object]:
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        payload = dict(invoice.get("payload") or {})
        payload["cancel_reason"] = reason
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_invoices SET status = 'CANCELLED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), invoice_id),
            )
        return self._financial_get("financial_invoices", record_id=invoice_id)

    def apply_credit_note(
        self,
        *,
        invoice_id: int,
        amount_minor: int,
        reason: str,
        actor_user_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        if amount_minor <= 0:
            raise ValidationError("credit note amount must be positive")
        payload = {
            "invoice_id": invoice_id,
            "currency": invoice.get("payload", {}).get("currency") or "XAF",
            "amount_minor": int(amount_minor),
            "reason": reason,
            "actor_user_id": actor_user_id,
            "metadata": metadata or {},
        }
        note = self._insert_financial_record(
            "financial_credit_notes",
            name="Credit Note",
            kind="credit_note",
            scope="invoice",
            status="ISSUED",
            payload=payload,
            parent_id=invoice_id,
            reference_id=actor_user_id,
            record_key=_record_key("credit-note", invoice_id, amount_minor, reason, actor_user_id),
            number_prefix="AVR",
        )
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE financial_invoices
                SET payload_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    _json({
                        **dict(invoice.get("payload") or {}),
                        "credit_note_id": int(note["id"]),
                    }),
                    _utcnow(),
                    invoice_id,
                ),
            )
        return note

    def list_credit_notes(self, *, status: str | None = None, invoice_id: int | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_credit_notes", status=status, limit=limit, parent_id=invoice_id)

    def list_credit_note_lines(self, *, credit_note_id: int, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_credit_note_lines", parent_id=credit_note_id, limit=limit)

    # ------------------------------------------------------------------
    # Payments
    # ------------------------------------------------------------------

    def register_payment_provider(
        self,
        *,
        provider_code: str,
        name: str,
        status: str = "inactive",
        environment: str = "sandbox",
        supported_currencies: list[str] | None = None,
        supported_channels: list[str] | None = None,
        supports_collection: bool = True,
        supports_refund: bool = False,
        supports_status_query: bool = True,
        supports_webhook: bool = False,
        supports_payout: bool = False,
        priority: int = 0,
        configuration_state: str = "partial",
        last_health_check: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        code = _normalize_code(provider_code)
        if code not in PAYMENT_PROVIDER_CODES and code != "CAMPAY":
            raise ValidationError(f"unsupported provider: {code}")
        payload = {
            "provider_code": code,
            "environment": environment,
            "supported_currencies": supported_currencies or ["XAF"],
            "supported_channels": supported_channels or [],
            "supports_collection": bool(supports_collection),
            "supports_refund": bool(supports_refund),
            "supports_status_query": bool(supports_status_query),
            "supports_webhook": bool(supports_webhook),
            "supports_payout": bool(supports_payout),
            "priority": int(priority),
            "configuration_state": configuration_state,
            "last_health_check": last_health_check,
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_payment_providers",
            name=name,
            kind="payment_provider",
            scope=environment,
            status=status,
            payload=payload,
            record_key=f"provider:{code}",
            number_prefix="PRV",
        )

    def list_payment_providers(self, *, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_payment_providers", status=status, limit=limit)

    def get_payment_provider(self, provider_id: int) -> dict[str, object]:
        return self._financial_get("financial_payment_providers", record_id=provider_id)

    def upsert_payment_provider_health(self, *, provider_code: str, health: dict[str, object]) -> dict[str, object]:
        provider = next(
            (
                row
                for row in self._financial_list("financial_payment_providers", limit=100)
                if _normalize_code((row.get("payload") or {}).get("provider_code")) == _normalize_code(provider_code)
            ),
            None,
        )
        if provider is None:
            raise NotFoundError("payment provider not found")
        payload = dict(provider.get("payload") or {})
        payload["last_health_check"] = health.get("checked_at") or _utcnow()
        payload["health"] = health
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_payment_providers SET payload_json = ?, updated_at = ?, status = ? WHERE id = ?",
                (_json(payload), _utcnow(), "active" if health.get("available") else "inactive", int(provider["id"])),
            )
        return self._financial_get("financial_payment_providers", record_id=int(provider["id"]))

    def create_payment_intent(
        self,
        *,
        actor_user_id: int | None,
        customer_user_id: int | None,
        invoice_id: int,
        amount_minor: int,
        currency: str,
        description: str = "",
        provider_code: str = "CAMPAY",
        channel: str = "mobile_money",
        phone_number_e164: str | None = None,
        expires_at: str | None = None,
        idempotency_key: str | None = None,
        business_reference: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        invoice_payload = dict(invoice.get("payload") or {})
        invoice_currency = self._ensure_currency(invoice_payload.get("currency") or currency)
        normalized_currency = self._ensure_currency(currency)
        normalized_phone = FINANCIAL_ENGINE.normalize_mobile_money_number(phone_number_e164) if phone_number_e164 else None
        if normalized_currency != invoice_currency:
            raise CurrencyMismatch("payment currency does not match invoice currency")
        balance_minor = int(invoice_payload.get("balance_minor") or 0)
        if amount_minor <= 0:
            raise PaymentAmountMismatch("payment amount must be positive")
        if amount_minor > balance_minor and balance_minor > 0:
            raise PaymentAmountMismatch("payment amount exceeds invoice balance")
        if _normalize_code(invoice.get("status")) in {"PAID", "VOID", "CANCELLED"}:
            raise InvoiceAlreadyPaid("Invoice is not payable")
        provider = next(
            (
                row
                for row in self._financial_list("financial_payment_providers", limit=100)
                if _normalize_code((row.get("payload") or {}).get("provider_code")) == _normalize_code(provider_code)
            ),
            None,
        )
        if provider is None or _normalize_code(provider.get("status")) not in {"ACTIVE", "INACTIVE"}:
            raise PaymentProviderUnavailable("Payment provider is unavailable")
        payload = {
            "actor_user_id": actor_user_id,
            "customer_user_id": customer_user_id,
            "invoice_id": invoice_id,
            "amount_minor": int(amount_minor),
            "currency": normalized_currency,
            "owner_user_id": customer_user_id,
            "owner_org_id": invoice_payload.get("organization_id"),
            "description": description,
            "provider_code": _normalize_code(provider_code),
            "channel": channel,
            "phone_number_e164": normalized_phone,
            "status": "CREATED",
            "expires_at": expires_at,
            "idempotency_key": idempotency_key,
            "business_reference": business_reference,
            "attempt_count": 0,
            "metadata": metadata or {},
        }
        record_key = _record_key("payment-intent", idempotency_key or business_reference or uuid.uuid4().hex, invoice_id, amount_minor, normalized_currency, provider_code)
        existing = self.one("SELECT * FROM financial_payment_intents WHERE record_key = ?", (record_key,))
        if existing is not None:
            return self._financial_row(existing) or dict(existing)
        intent = self._insert_financial_record(
            "financial_payment_intents",
            name="Payment Intent",
            kind="payment_intent",
            scope=channel,
            status="CREATED",
            payload=payload,
            parent_id=invoice_id,
            reference_id=customer_user_id,
            secondary_id=actor_user_id,
            record_key=record_key,
            number_prefix="PAY",
        )
        self.record_event("payment_intent_created", {"id": intent["id"], "invoice_id": invoice_id, "amount_minor": amount_minor, "provider_code": provider_code})
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payment.intent.created",
            object_type="payment_intent",
            object_id=int(intent["id"]),
            previous_state={},
            new_state=intent,
            reason="payment intent created",
            payload={"payment_intent": intent},
        )
        return intent

    def list_payment_intents(
        self,
        *,
        status: str | None = None,
        invoice_id: int | None = None,
        customer_user_id: int | None = None,
        provider_code: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_payment_intents", status=status, limit=limit, parent_id=invoice_id, owner_user_id=customer_user_id)
        if provider_code:
            items = [row for row in items if _normalize_code((row.get("payload") or {}).get("provider_code")) == _normalize_code(provider_code)]
        return items

    def get_payment_intent(self, payment_intent_id: int) -> dict[str, object]:
        intent = self._financial_get("financial_payment_intents", record_id=payment_intent_id)
        attempts = self.list_payment_attempts(payment_intent_id=payment_intent_id, limit=100)
        intent["attempts"] = attempts
        return intent

    def update_payment_intent(self, payment_intent_id: int, **fields: object) -> dict[str, object]:
        return self._update_financial_record("financial_payment_intents", payment_intent_id, **fields)

    def update_payment_attempt(self, payment_attempt_id: int, **fields: object) -> dict[str, object]:
        return self._update_financial_record("financial_payment_attempts", payment_attempt_id, **fields)

    def create_payment_attempt(
        self,
        *,
        payment_intent_id: int,
        provider_code: str,
        request_json: dict[str, object],
        response_json: dict[str, object] | None = None,
        provider_reference: str | None = None,
        webhook_reference: str | None = None,
        idempotency_key: str | None = None,
        error_code: str | None = None,
        error_message: str | None = None,
        status: str = "PENDING",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        intent = self._financial_get("financial_payment_intents", record_id=payment_intent_id)
        payload = dict(intent.get("payload") or {})
        attempt_no = int(payload.get("attempt_count") or 0) + 1
        payload["attempt_count"] = attempt_no
        payload["status"] = status
        record_key = _record_key(
            "payment-attempt",
            payment_intent_id,
            provider_code,
            idempotency_key or provider_reference or webhook_reference or _json(request_json),
        )
        existing = self.one("SELECT * FROM financial_payment_attempts WHERE record_key = ?", (record_key,))
        if existing is not None:
            return self._financial_row(existing) or dict(existing)
        attempt_payload = {
            "payment_intent_id": payment_intent_id,
            "provider_code": _normalize_code(provider_code),
            "attempt_no": attempt_no,
            "request_json": request_json,
            "response_json": response_json or {},
            "provider_reference": provider_reference,
            "webhook_reference": webhook_reference,
            "idempotency_key": idempotency_key,
            "error_code": error_code,
            "error_message": error_message,
            "status": status,
            "metadata": metadata or {},
        }
        attempt = self._insert_financial_record(
            "financial_payment_attempts",
            name="Payment Attempt",
            kind="payment_attempt",
            scope=provider_code,
            status=status,
            payload=attempt_payload,
            parent_id=payment_intent_id,
            record_key=record_key,
            number_prefix="PAY",
        )
        self._update_financial_record("financial_payment_intents", payment_intent_id, payload=payload)
        return attempt

    def list_payment_attempts(self, *, payment_intent_id: int | None = None, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_payment_attempts", status=status, limit=limit, parent_id=payment_intent_id)

    def get_payment_attempt(self, attempt_id: int) -> dict[str, object]:
        return self._financial_get("financial_payment_attempts", record_id=attempt_id)

    def list_payment_transactions(
        self,
        *,
        payment_intent_id: int | None = None,
        payment_attempt_id: int | None = None,
        invoice_id: int | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_payment_transactions", status=status, limit=limit, parent_id=payment_intent_id, reference_id=payment_attempt_id, secondary_id=invoice_id)
        return items

    def get_payment_transaction(self, transaction_id: int) -> dict[str, object]:
        return self._financial_get("financial_payment_transactions", record_id=transaction_id)

    def record_payment_transaction(
        self,
        *,
        payment_intent_id: int,
        payment_attempt_id: int | None,
        invoice_id: int,
        provider_code: str,
        provider_reference: str,
        transaction_type: str,
        direction: str,
        status: str,
        amount_minor: int,
        currency: str,
        effective_at: str | None = None,
        posted_at: str | None = None,
        payer_user_id: int | None = None,
        payee_user_id: int | None = None,
        reconciliation_status: str = "UNMATCHED",
        proof: dict[str, object] | None = None,
        audit: dict[str, object] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        normalized_currency = self._ensure_currency(currency)
        if _normalize_code(transaction_type, default="COLLECTION") not in {kind.upper() for kind in PAYMENT_TRANSACTION_TYPES}:
            transaction_type = "collection"
        payload = {
            "payment_intent_id": payment_intent_id,
            "payment_attempt_id": payment_attempt_id,
            "invoice_id": invoice_id,
            "provider_code": _normalize_code(provider_code),
            "provider_reference": provider_reference,
            "transaction_type": transaction_type,
            "direction": direction,
            "status": status,
            "amount_minor": int(amount_minor),
            "currency": normalized_currency,
            "effective_at": effective_at or _utcnow(),
            "posted_at": posted_at or _utcnow(),
            "payer_user_id": payer_user_id,
            "payee_user_id": payee_user_id,
            "reconciliation_status": reconciliation_status,
            "proof": proof or {},
            "audit": audit or {},
            "metadata": metadata or {},
        }
        record_key = _record_key("payment-transaction", payment_intent_id, payment_attempt_id or 0, provider_reference, transaction_type, amount_minor, normalized_currency)
        existing = self.one("SELECT * FROM financial_payment_transactions WHERE record_key = ?", (record_key,))
        if existing is not None:
            return self._financial_row(existing) or dict(existing)
        transaction = self._insert_financial_record(
            "financial_payment_transactions",
            name="Payment Transaction",
            kind=transaction_type,
            scope=provider_code,
            status=status,
            payload=payload,
            parent_id=payment_intent_id,
            reference_id=payment_attempt_id,
            secondary_id=invoice_id,
            record_key=record_key,
            number_prefix="PAY",
        )
        return transaction

    def confirm_payment_intent(
        self,
        *,
        payment_intent_id: int,
        payment_attempt_id: int | None = None,
        provider_reference: str | None = None,
        amount_minor: int | None = None,
        currency: str | None = None,
        provider_event_id: int | None = None,
        actor_user_id: int | None = None,
        proof: dict[str, object] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        intent = self._financial_get("financial_payment_intents", record_id=payment_intent_id)
        intent_payload = dict(intent.get("payload") or {})
        invoice = self._financial_get("financial_invoices", record_id=int(intent_payload.get("invoice_id")))
        invoice_payload = dict(invoice.get("payload") or {})
        if _normalize_code(intent.get("status")) in {"SUCCEEDED"}:
            raise PaymentAlreadyProcessed("Payment already confirmed")
        payment_currency = self._ensure_currency(currency or intent_payload.get("currency") or invoice_payload.get("currency") or "XAF")
        invoice_currency = self._ensure_currency(invoice_payload.get("currency") or payment_currency)
        if payment_currency != invoice_currency:
            raise CurrencyMismatch("Payment currency does not match invoice currency")
        payment_amount = int(amount_minor if amount_minor is not None else intent_payload.get("amount_minor") or 0)
        if payment_amount <= 0:
            raise PaymentAmountMismatch("Payment amount must be positive")
        invoice_balance = int(invoice_payload.get("balance_minor") or 0)
        if payment_amount > invoice_balance and invoice_balance > 0:
            raise PaymentAmountMismatch("Payment amount exceeds invoice balance")
        if payment_attempt_id is not None:
            attempt = self._financial_get("financial_payment_attempts", record_id=payment_attempt_id)
            if int(attempt.get("parent_id") or 0) != int(payment_intent_id):
                raise ValidationError("payment attempt does not belong to payment intent")
            if _normalize_code(attempt.get("status")) in {"SUCCEEDED"}:
                pass
        previous_intent = dict(intent)
        payload = dict(intent_payload)
        payload["status"] = "SUCCEEDED"
        payload["provider_reference"] = provider_reference or payload.get("provider_reference")
        payload["confirmed_at"] = _utcnow()
        payload["amount_minor"] = payment_amount
        payload["currency"] = payment_currency
        payload["provider_event_id"] = provider_event_id
        payload["proof"] = proof or payload.get("proof") or {}
        payload["metadata"] = metadata or payload.get("metadata") or {}
        transaction = self.record_payment_transaction(
            payment_intent_id=payment_intent_id,
            payment_attempt_id=payment_attempt_id,
            invoice_id=int(invoice["id"]),
            provider_code=str(intent_payload.get("provider_code") or "CAMPAY"),
            provider_reference=provider_reference or str(intent_payload.get("provider_reference") or ""),
            transaction_type="collection",
            direction="credit",
            status="SUCCESSFUL",
            amount_minor=payment_amount,
            currency=payment_currency,
            payer_user_id=int(intent_payload.get("customer_user_id") or 0) or None,
            payee_user_id=int(intent_payload.get("actor_user_id") or 0) or None,
            reconciliation_status="MATCHED",
            proof=proof,
            audit={"provider_event_id": provider_event_id},
            metadata=metadata,
        )
        invoice_payload["amount_paid_minor"] = int(invoice_payload.get("amount_paid_minor") or 0) + payment_amount
        invoice_payload["balance_minor"] = max(0, int(invoice_payload.get("breakdown", {}).get("total_minor") or 0) - invoice_payload["amount_paid_minor"])
        if invoice_payload["balance_minor"] <= 0:
            invoice_status = "PAID"
        else:
            invoice_status = "PARTIALLY_PAID"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_payment_intents SET status = 'SUCCEEDED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), payment_intent_id),
            )
            if payment_attempt_id is not None:
                attempt_row = self._financial_get("financial_payment_attempts", record_id=payment_attempt_id)
                attempt_payload = dict(attempt_row.get("payload") or {})
                attempt_payload["status"] = "SUCCEEDED"
                attempt_payload["payment_intent_id"] = payment_intent_id
                attempt_payload["provider_reference"] = provider_reference or attempt_payload.get("provider_reference")
                conn.execute(
                    "UPDATE financial_payment_attempts SET payload_json = ?, updated_at = ? WHERE id = ?",
                    (_json(attempt_payload), _utcnow(), payment_attempt_id),
                )
            conn.execute(
                "UPDATE financial_invoices SET status = ?, payload_json = ?, updated_at = ? WHERE id = ?",
                (
                    invoice_status,
                    _json(invoice_payload),
                    _utcnow(),
                    int(invoice["id"]),
                ),
            )
        receipt = self.generate_receipt(
            payment_transaction_id=int(transaction["id"]),
            invoice_id=int(invoice["id"]),
            actor_user_id=actor_user_id,
        )
        self.record_event("payment_succeeded", {"payment_intent_id": payment_intent_id, "invoice_id": int(invoice["id"]), "transaction_id": int(transaction["id"])})
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payment.succeeded",
            object_type="payment_intent",
            object_id=payment_intent_id,
            previous_state=previous_intent,
            new_state=self._financial_get("financial_payment_intents", record_id=payment_intent_id),
            reason="payment confirmed",
            payload={"transaction": transaction, "receipt": receipt},
        )
        return {
            "payment_intent": self._financial_get("financial_payment_intents", record_id=payment_intent_id),
            "payment_transaction": transaction,
            "receipt": receipt,
            "invoice": self._financial_get("financial_invoices", record_id=int(invoice["id"])),
        }

    def fail_payment_intent(self, payment_intent_id: int, *, error_code: str, error_message: str = "", actor_user_id: int | None = None) -> dict[str, object]:
        intent = self._financial_get("financial_payment_intents", record_id=payment_intent_id)
        if _normalize_code(intent.get("status")) in {"SUCCEEDED"}:
            raise PaymentAlreadyProcessed("Payment already processed")
        payload = dict(intent.get("payload") or {})
        payload["status"] = "FAILED"
        payload["error_code"] = error_code
        payload["error_message"] = error_message
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_payment_intents SET status = 'FAILED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), payment_intent_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payment.failed",
            object_type="payment_intent",
            object_id=payment_intent_id,
            previous_state=intent,
            new_state=self._financial_get("financial_payment_intents", record_id=payment_intent_id),
            reason=error_message or error_code,
            result="failure",
            payload={"error_code": error_code},
        )
        return self._financial_get("financial_payment_intents", record_id=payment_intent_id)

    def expire_payment_intent(self, payment_intent_id: int, *, actor_user_id: int | None = None) -> dict[str, object]:
        intent = self._financial_get("financial_payment_intents", record_id=payment_intent_id)
        payload = dict(intent.get("payload") or {})
        payload["status"] = "EXPIRED"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_payment_intents SET status = 'EXPIRED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), payment_intent_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payment.expired",
            object_type="payment_intent",
            object_id=payment_intent_id,
            previous_state=intent,
            new_state=self._financial_get("financial_payment_intents", record_id=payment_intent_id),
            reason="intent expired",
            result="success",
        )
        return self._financial_get("financial_payment_intents", record_id=payment_intent_id)

    def cancel_payment_intent(self, payment_intent_id: int, *, actor_user_id: int | None = None, reason: str = "") -> dict[str, object]:
        intent = self._financial_get("financial_payment_intents", record_id=payment_intent_id)
        if _normalize_code(intent.get("status")) in {"SUCCEEDED"}:
            raise PaymentAlreadyProcessed("Payment already processed")
        payload = dict(intent.get("payload") or {})
        payload["status"] = "CANCELLED"
        payload["cancel_reason"] = reason
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_payment_intents SET status = 'CANCELLED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), payment_intent_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payment.cancelled",
            object_type="payment_intent",
            object_id=payment_intent_id,
            previous_state=intent,
            new_state=self._financial_get("financial_payment_intents", record_id=payment_intent_id),
            reason=reason,
        )
        return self._financial_get("financial_payment_intents", record_id=payment_intent_id)

    # ------------------------------------------------------------------
    # Receipts, refunds, provider events
    # ------------------------------------------------------------------

    def generate_receipt(
        self,
        *,
        payment_transaction_id: int,
        invoice_id: int,
        actor_user_id: int | None = None,
        status: str = "GENERATED",
    ) -> dict[str, object]:
        transaction = self._financial_get("financial_payment_transactions", record_id=payment_transaction_id)
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        tx_payload = dict(transaction.get("payload") or {})
        invoice_payload = dict(invoice.get("payload") or {})
        if _normalize_code(transaction.get("status")) != "SUCCESSFUL":
            raise PaymentAlreadyProcessed("Receipt can only be generated from successful payment")
        payload = {
            "payment_transaction_id": payment_transaction_id,
            "payment_intent_id": int(transaction.get("parent_id") or 0) or None,
            "invoice_id": invoice_id,
            "amount_minor": int(tx_payload.get("amount_minor") or 0),
            "currency": tx_payload.get("currency") or invoice_payload.get("currency") or "XAF",
            "payer_user_id": tx_payload.get("payer_user_id"),
            "payee_user_id": tx_payload.get("payee_user_id"),
            "payment_method": tx_payload.get("provider_code") or "CAMPAY",
            "provider_reference": tx_payload.get("provider_reference"),
            "invoice_number": invoice_payload.get("number"),
            "transaction_reference": tx_payload.get("provider_reference"),
            "proof": tx_payload.get("proof") or {},
            "status": status,
            "metadata": {"generated_from": "payment_transaction"},
        }
        existing = self.one("SELECT * FROM financial_receipts WHERE reference_id = ? AND secondary_id = ?", (payment_transaction_id, invoice_id))
        if existing is not None:
            return self._financial_row(existing) or dict(existing)
        receipt = self._insert_financial_record(
            "financial_receipts",
            name="Receipt",
            kind="receipt",
            scope="payment",
            status=status,
            payload=payload,
            parent_id=payment_transaction_id,
            reference_id=invoice_id,
            secondary_id=actor_user_id,
            record_key=_record_key("receipt", payment_transaction_id, invoice_id, tx_payload.get("provider_reference"), tx_payload.get("amount_minor")),
            number_prefix="REC",
        )
        return receipt

    def list_receipts(self, *, status: str | None = None, invoice_id: int | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_receipts", status=status, limit=limit, reference_id=invoice_id)

    def get_receipt(self, receipt_id: int) -> dict[str, object]:
        return self._financial_get("financial_receipts", record_id=receipt_id)

    def request_refund(
        self,
        *,
        payment_transaction_id: int,
        invoice_id: int,
        amount_minor: int,
        reason: str,
        requested_by_user_id: int | None = None,
        provider_code: str = "CAMPAY",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        transaction = self._financial_get("financial_payment_transactions", record_id=payment_transaction_id)
        invoice = self._financial_get("financial_invoices", record_id=invoice_id)
        tx_payload = dict(transaction.get("payload") or {})
        invoice_payload = dict(invoice.get("payload") or {})
        if amount_minor <= 0:
            raise RefundAmountExceeded("refund amount must be positive")
        paid_amount = int(tx_payload.get("amount_minor") or 0)
        refunded_total = sum(
            int((row.get("payload") or {}).get("requested_amount_minor") or 0)
            for row in self.list_refunds(payment_transaction_id=payment_transaction_id, status=None, limit=500)
            if _normalize_code(row.get("status")) in {"APPROVED", "PROCESSING", "SUCCEEDED"}
        )
        if refunded_total + amount_minor > paid_amount:
            raise RefundAmountExceeded("refund amount exceeds paid amount")
        payload = {
            "payment_transaction_id": payment_transaction_id,
            "payment_intent_id": int(transaction.get("parent_id") or 0) or None,
            "invoice_id": invoice_id,
            "amount_minor": int(amount_minor),
            "requested_amount_minor": int(amount_minor),
            "refunded_amount_minor": 0,
            "currency": tx_payload.get("currency") or "XAF",
            "owner_user_id": requested_by_user_id,
            "owner_org_id": invoice_payload.get("organization_id"),
            "reason": reason,
            "provider_code": _normalize_code(provider_code),
            "requested_by_user_id": requested_by_user_id,
            "metadata": metadata or {},
        }
        refund = self._insert_financial_record(
            "financial_refunds",
            name="Refund",
            kind="refund",
            scope=provider_code,
            status="REQUESTED",
            payload=payload,
            parent_id=payment_transaction_id,
            reference_id=invoice_id,
            secondary_id=requested_by_user_id,
            record_key=_record_key("refund", payment_transaction_id, invoice_id, amount_minor, reason),
            number_prefix="RMB",
        )
        self.record_event("refund_requested", {"refund_id": refund["id"], "payment_transaction_id": payment_transaction_id})
        return refund

    def list_refunds(
        self,
        *,
        payment_transaction_id: int | None = None,
        status: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        return self._financial_list("financial_refunds", status=status, limit=limit, parent_id=payment_transaction_id)

    def get_refund(self, refund_id: int) -> dict[str, object]:
        return self._financial_get("financial_refunds", record_id=refund_id)

    def approve_refund(self, refund_id: int, *, actor_user_id: int | None = None) -> dict[str, object]:
        refund = self._financial_get("financial_refunds", record_id=refund_id)
        if _normalize_code(refund.get("status")) not in {"REQUESTED", "UNDER_REVIEW"}:
            return refund
        refund = self._update_financial_record("financial_refunds", refund_id, status="APPROVED")
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="refund.approved",
            object_type="refund",
            object_id=refund_id,
            previous_state={},
            new_state=refund,
            reason="refund approved",
        )
        return refund

    def process_refund(
        self,
        refund_id: int,
        *,
        provider_reference: str | None = None,
        actor_user_id: int | None = None,
        processed_amount_minor: int | None = None,
    ) -> dict[str, object]:
        refund = self._financial_get("financial_refunds", record_id=refund_id)
        if _normalize_code(refund.get("status")) not in {"APPROVED", "PROCESSING"}:
            raise RefundAmountExceeded("refund is not approved")
        payload = dict(refund.get("payload") or {})
        amount_minor = int(processed_amount_minor or payload.get("requested_amount_minor") or payload.get("amount_minor") or 0)
        payload["provider_reference"] = provider_reference or payload.get("provider_reference")
        payload["refunded_amount_minor"] = amount_minor
        payload["processed_at"] = _utcnow()
        payload["status"] = "SUCCEEDED"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_refunds SET status = 'SUCCEEDED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), refund_id),
            )
        self.record_event("refund_succeeded", {"refund_id": refund_id, "provider_reference": provider_reference})
        return self._financial_get("financial_refunds", record_id=refund_id)

    def record_provider_event(
        self,
        *,
        provider_code: str,
        event_type: str,
        provider_event_id: str,
        payload: dict[str, object],
        headers: dict[str, object] | None = None,
        source_reference: str | None = None,
        correlation_id: str | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, object]:
        record_key = _record_key("provider-event", provider_code, provider_event_id, idempotency_key or source_reference or correlation_id or payload)
        existing = self.one("SELECT * FROM financial_provider_events WHERE record_key = ?", (record_key,))
        if existing is not None:
            return self._financial_row(existing) or dict(existing)
        event_payload = {
            "provider_code": _normalize_code(provider_code),
            "event_type": event_type,
            "provider_event_id": provider_event_id,
            "payload": payload,
            "headers": headers or {},
            "source_reference": source_reference,
            "correlation_id": correlation_id,
            "idempotency_key": idempotency_key,
            "payload_hash": FINANCIAL_ENGINE.build_reference("hash", provider_code, provider_event_id, _json(payload)),
        }
        event = self._insert_financial_record(
            "financial_provider_events",
            name="Provider Event",
            kind=event_type,
            scope=provider_code,
            status="RECEIVED",
            payload=event_payload,
            record_key=record_key,
            number_prefix="EVT",
        )
        return event

    def list_provider_events(self, *, provider_code: str | None = None, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        items = self._financial_list("financial_provider_events", status=status, limit=limit)
        if provider_code:
            items = [row for row in items if _normalize_code((row.get("payload") or {}).get("provider_code")) == _normalize_code(provider_code)]
        return items

    # ------------------------------------------------------------------
    # Subscription plans and subscriptions
    # ------------------------------------------------------------------

    def create_subscription_plan(
        self,
        *,
        code: str,
        name: str,
        description: str = "",
        target: str = "user",
        price_minor: int = 0,
        currency: str = "XAF",
        frequency: str = "MONTHLY",
        duration_days: int | None = None,
        trial_days: int | None = None,
        features: list[str] | None = None,
        limits: dict[str, object] | None = None,
        conditions: dict[str, object] | None = None,
        status: str = "draft",
        starts_at: str | None = None,
        ends_at: str | None = None,
        renewal_policy: dict[str, object] | None = None,
        suspension_policy: dict[str, object] | None = None,
        termination_policy: dict[str, object] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        if _normalize_code(frequency) not in SUBSCRIPTION_PLAN_FREQUENCIES:
            raise ValidationError("unsupported subscription frequency")
        payload = {
            "code": code,
            "description": description,
            "target": target,
            "price_minor": int(price_minor),
            "currency": self._ensure_currency(currency),
            "frequency": _normalize_code(frequency),
            "duration_days": duration_days,
            "trial_days": trial_days,
            "features": features or [],
            "limits": limits or {},
            "conditions": conditions or {},
            "starts_at": starts_at,
            "ends_at": ends_at,
            "renewal_policy": renewal_policy or {},
            "suspension_policy": suspension_policy or {},
            "termination_policy": termination_policy or {},
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_subscription_plans",
            name=name,
            kind="subscription_plan",
            scope=target,
            status=status.upper() if status.isupper() else status,
            payload=payload,
            record_key=f"subscription-plan:{code.lower()}",
            number_prefix="PLN",
        )

    def list_subscription_plans(self, *, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_subscription_plans", status=status, limit=limit)

    def get_subscription_plan(self, plan_id: int) -> dict[str, object]:
        return self._financial_get("financial_subscription_plans", record_id=plan_id)

    def create_subscription(
        self,
        *,
        plan_id: int,
        actor_user_id: int | None,
        customer_user_id: int | None,
        organization_id: int | None = None,
        renewal_mode: str = "automatic",
        preferred_payment_provider_code: str | None = None,
        started_at: str | None = None,
        current_period_start: str | None = None,
        current_period_end: str | None = None,
        next_billing_at: str | None = None,
        status: str = "PENDING",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        plan = self.get_subscription_plan(plan_id)
        if _normalize_code(plan.get("status")) not in {"ACTIVE", "DRAFT"}:
            raise SubscriptionNotEligible("plan is not active")
        payload = {
            "plan_id": plan_id,
            "actor_user_id": actor_user_id,
            "customer_user_id": customer_user_id,
            "organization_id": organization_id,
            "owner_user_id": customer_user_id,
            "owner_org_id": organization_id,
            "renewal_mode": renewal_mode,
            "preferred_payment_provider_code": preferred_payment_provider_code,
            "started_at": started_at or _utcnow(),
            "current_period_start": current_period_start or started_at or _utcnow(),
            "current_period_end": current_period_end,
            "next_billing_at": next_billing_at,
            "ended_at": None,
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_subscriptions",
            name="Subscription",
            kind="subscription",
            scope=renewal_mode,
            status=status,
            payload=payload,
            parent_id=customer_user_id,
            reference_id=organization_id,
            secondary_id=plan_id,
            record_key=_record_key("subscription", plan_id, customer_user_id, organization_id, renewal_mode),
            number_prefix="SUB",
        )

    def list_subscriptions(
        self,
        *,
        status: str | None = None,
        customer_user_id: int | None = None,
        organization_id: int | None = None,
        plan_id: int | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_subscriptions", status=status, limit=limit, owner_user_id=customer_user_id, organization_id=organization_id)
        if plan_id is not None:
            items = [row for row in items if int((row.get("payload") or {}).get("plan_id") or 0) == int(plan_id)]
        return items

    def get_subscription(self, subscription_id: int) -> dict[str, object]:
        subscription = self._financial_get("financial_subscriptions", record_id=subscription_id)
        cycles = self.list_subscription_cycles(subscription_id=subscription_id, limit=100)
        subscription["cycles"] = cycles
        return subscription

    def create_subscription_cycle(
        self,
        *,
        subscription_id: int,
        plan_id: int,
        amount_minor: int,
        currency: str,
        period_start: str,
        period_end: str,
        renewal_kind: str = "scheduled",
        status: str = "DRAFT",
        invoice_id: int | None = None,
        payment_intent_id: int | None = None,
        due_at: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = {
            "subscription_id": subscription_id,
            "plan_id": plan_id,
            "invoice_id": invoice_id,
            "payment_intent_id": payment_intent_id,
            "amount_minor": int(amount_minor),
            "currency": self._ensure_currency(currency),
            "period_start": period_start,
            "period_end": period_end,
            "renewal_kind": renewal_kind,
            "due_at": due_at,
            "metadata": metadata or {},
        }
        cycle = self._insert_financial_record(
            "financial_subscription_cycles",
            name="Subscription Cycle",
            kind="subscription_cycle",
            scope=renewal_kind,
            status=status,
            payload=payload,
            parent_id=subscription_id,
            reference_id=plan_id,
            secondary_id=invoice_id,
            record_key=_record_key("subscription-cycle", subscription_id, period_start, period_end, renewal_kind),
            number_prefix="CYC",
        )
        return cycle

    def list_subscription_cycles(self, *, subscription_id: int | None = None, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_subscription_cycles", status=status, limit=limit, parent_id=subscription_id)

    def renew_subscription(
        self,
        subscription_id: int,
        *,
        actor_user_id: int | None,
        invoice_id: int | None = None,
        payment_intent_id: int | None = None,
        period_start: str | None = None,
        period_end: str | None = None,
        amount_minor: int | None = None,
        currency: str | None = None,
        due_at: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        subscription = self._financial_get("financial_subscriptions", record_id=subscription_id)
        payload = dict(subscription.get("payload") or {})
        if _normalize_code(subscription.get("status")) in {"CANCELLED", "TERMINATED", "EXPIRED"}:
            raise SubscriptionNotEligible("subscription cannot be renewed")
        current_period_end = str(payload.get("current_period_end") or "")
        if current_period_end and period_start and current_period_end == period_start:
            raise SubscriptionAlreadyRenewed("subscription already renewed for period")
        plan = self.get_subscription_plan(int(payload.get("plan_id") or 0))
        amount_minor = int(amount_minor if amount_minor is not None else (plan.get("payload") or {}).get("price_minor") or 0)
        currency = self._ensure_currency(currency or (plan.get("payload") or {}).get("currency") or "XAF")
        cycle = self.create_subscription_cycle(
            subscription_id=subscription_id,
            plan_id=int(payload.get("plan_id") or 0),
            amount_minor=amount_minor,
            currency=currency,
            period_start=period_start or _utcnow(),
            period_end=period_end or _utcnow(),
            renewal_kind="renewal",
            status="PAYMENT_PENDING",
            invoice_id=invoice_id,
            payment_intent_id=payment_intent_id,
            due_at=due_at,
            metadata=metadata,
        )
        payload["current_period_start"] = period_start or payload.get("current_period_start")
        payload["current_period_end"] = period_end or payload.get("current_period_end")
        payload["next_billing_at"] = due_at or payload.get("next_billing_at")
        payload["status"] = "ACTIVE"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_subscriptions SET status = 'ACTIVE', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), subscription_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="subscription.renewed",
            object_type="subscription",
            object_id=subscription_id,
            previous_state=subscription,
            new_state=self._financial_get("financial_subscriptions", record_id=subscription_id),
            reason="subscription renewed",
            payload={"cycle": cycle},
        )
        return {"subscription": self._financial_get("financial_subscriptions", record_id=subscription_id), "cycle": cycle}

    def change_subscription_plan(
        self,
        subscription_id: int,
        *,
        new_plan_id: int,
        actor_user_id: int | None = None,
        immediate: bool = False,
        prorata_minor: int = 0,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        subscription = self._financial_get("financial_subscriptions", record_id=subscription_id)
        plan = self.get_subscription_plan(new_plan_id)
        payload = dict(subscription.get("payload") or {})
        payload["plan_id"] = new_plan_id
        payload["prorata_minor"] = int(prorata_minor)
        payload["plan_change_mode"] = "immediate" if immediate else "next_cycle"
        payload["metadata"] = metadata or {}
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_subscriptions SET secondary_id = ?, payload_json = ?, updated_at = ? WHERE id = ?",
                (new_plan_id, _json(payload), _utcnow(), subscription_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="subscription.plan_changed",
            object_type="subscription",
            object_id=subscription_id,
            previous_state=subscription,
            new_state=self._financial_get("financial_subscriptions", record_id=subscription_id),
            reason=str(plan.get("name") or ""),
        )
        return self._financial_get("financial_subscriptions", record_id=subscription_id)

    def suspend_subscription(self, subscription_id: int, *, actor_user_id: int | None = None, reason: str = "") -> dict[str, object]:
        subscription = self._financial_get("financial_subscriptions", record_id=subscription_id)
        payload = dict(subscription.get("payload") or {})
        payload["suspension_reason"] = reason
        payload["status"] = "SUSPENDED"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_subscriptions SET status = 'SUSPENDED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), subscription_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="subscription.suspended",
            object_type="subscription",
            object_id=subscription_id,
            previous_state=subscription,
            new_state=self._financial_get("financial_subscriptions", record_id=subscription_id),
            reason=reason,
        )
        return self._financial_get("financial_subscriptions", record_id=subscription_id)

    def cancel_subscription(self, subscription_id: int, *, actor_user_id: int | None = None, reason: str = "") -> dict[str, object]:
        subscription = self._financial_get("financial_subscriptions", record_id=subscription_id)
        payload = dict(subscription.get("payload") or {})
        payload["cancellation_reason"] = reason
        payload["status"] = "CANCELLED"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_subscriptions SET status = 'CANCELLED', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), subscription_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="subscription.cancelled",
            object_type="subscription",
            object_id=subscription_id,
            previous_state=subscription,
            new_state=self._financial_get("financial_subscriptions", record_id=subscription_id),
            reason=reason,
        )
        return self._financial_get("financial_subscriptions", record_id=subscription_id)

    # ------------------------------------------------------------------
    # Commissions and payouts
    # ------------------------------------------------------------------

    def create_commission_rule(
        self,
        *,
        code: str,
        name: str,
        actor_role: str = "partner",
        service_code: str | None = None,
        channel: str = "any",
        amount_type: str = "percentage",
        flat_amount_minor: int = 0,
        rate_bps: int = 0,
        minimum_minor: int = 0,
        maximum_minor: int = 0,
        share: list[dict[str, object]] | None = None,
        priority: int = 100,
        starts_at: str | None = None,
        ends_at: str | None = None,
        status: str = "active",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = {
            "code": code,
            "actor_role": actor_role,
            "service_code": service_code,
            "channel": channel,
            "amount_type": amount_type,
            "flat_amount_minor": int(flat_amount_minor),
            "rate_bps": int(rate_bps),
            "minimum_minor": int(minimum_minor),
            "maximum_minor": int(maximum_minor),
            "share": share or [],
            "priority": int(priority),
            "starts_at": starts_at,
            "ends_at": ends_at,
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_commission_rules",
            name=name,
            kind="commission_rule",
            scope=actor_role,
            status=status,
            payload=payload,
            record_key=f"commission-rule:{code.lower()}",
            number_prefix="RLE",
        )

    def list_commission_rules(self, *, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_commission_rules", status=status, limit=limit)

    def calculate_commission(
        self,
        *,
        rule_id: int,
        source_object_type: str,
        source_object_id: int,
        gross_amount_minor: int,
        currency: str = "XAF",
        beneficiary_user_id: int | None = None,
        beneficiary_organization_id: int | None = None,
        actor_user_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        rule = self._financial_get("financial_commission_rules", record_id=rule_id)
        if _normalize_code(rule.get("status")) not in {"ACTIVE", "VALIDATED", "CALCULATED"}:
            raise CommissionNotPayable("commission rule is not active")
        rule_payload = dict(rule.get("payload") or {})
        rate_bps = int(rule_payload.get("rate_bps") or 0)
        flat_amount_minor = int(rule_payload.get("flat_amount_minor") or 0)
        amount_minor = max(0, int((Decimal(gross_amount_minor) * Decimal(rate_bps) / Decimal(10_000)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) + flat_amount_minor)
        amount_minor = max(int(rule_payload.get("minimum_minor") or 0), amount_minor)
        maximum_minor = int(rule_payload.get("maximum_minor") or 0)
        if maximum_minor > 0:
            amount_minor = min(amount_minor, maximum_minor)
        payload = {
            "rule_id": rule_id,
            "source_object_type": source_object_type,
            "source_object_id": source_object_id,
            "gross_amount_minor": int(gross_amount_minor),
            "currency": self._ensure_currency(currency),
            "amount_minor": amount_minor,
            "beneficiary_user_id": beneficiary_user_id,
            "beneficiary_organization_id": beneficiary_organization_id,
            "owner_user_id": beneficiary_user_id,
            "owner_org_id": beneficiary_organization_id,
            "actor_user_id": actor_user_id,
            "metadata": metadata or {},
            "rule": rule_payload,
        }
        commission = self._insert_financial_record(
            "financial_commissions",
            name="Commission",
            kind="commission",
            scope=rule_payload.get("actor_role") or "partner",
            status="CALCULATED",
            payload=payload,
            parent_id=rule_id,
            reference_id=source_object_id,
            secondary_id=beneficiary_user_id or beneficiary_organization_id,
            record_key=_record_key("commission", rule_id, source_object_type, source_object_id, beneficiary_user_id, beneficiary_organization_id),
            number_prefix="COM",
        )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="commission.calculated",
            object_type="commission",
            object_id=int(commission["id"]),
            previous_state={},
            new_state=commission,
            reason="commission calculated",
            payload=payload,
        )
        return commission

    def list_commissions(
        self,
        *,
        status: str | None = None,
        beneficiary_user_id: int | None = None,
        beneficiary_organization_id: int | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_commissions", status=status, limit=limit)
        if beneficiary_user_id is not None:
            items = [row for row in items if int((row.get("payload") or {}).get("beneficiary_user_id") or 0) == int(beneficiary_user_id)]
        if beneficiary_organization_id is not None:
            items = [row for row in items if int((row.get("payload") or {}).get("beneficiary_organization_id") or 0) == int(beneficiary_organization_id)]
        return items

    def get_commission(self, commission_id: int) -> dict[str, object]:
        return self._financial_get("financial_commissions", record_id=commission_id)

    def validate_commission(self, commission_id: int, *, actor_user_id: int | None = None) -> dict[str, object]:
        commission = self._financial_get("financial_commissions", record_id=commission_id)
        if _normalize_code(commission.get("status")) in {"PAID"}:
            raise CommissionAlreadyPaid("Commission already paid")
        return self._update_financial_record("financial_commissions", commission_id, status="VALIDATED", payload={"validated_at": _utcnow(), "validated_by_user_id": actor_user_id})

    def mark_commission_payable(self, commission_id: int, *, actor_user_id: int | None = None) -> dict[str, object]:
        commission = self._financial_get("financial_commissions", record_id=commission_id)
        if _normalize_code(commission.get("status")) == "PAID":
            raise CommissionAlreadyPaid("Commission already paid")
        return self._update_financial_record("financial_commissions", commission_id, status="PAYABLE", payload={"payable_at": _utcnow(), "payable_by_user_id": actor_user_id})

    def pay_commission(
        self,
        commission_id: int,
        *,
        provider_code: str = "MANUAL",
        provider_reference: str | None = None,
        actor_user_id: int | None = None,
        payout_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        commission = self._financial_get("financial_commissions", record_id=commission_id)
        if _normalize_code(commission.get("status")) == "PAID":
            raise CommissionAlreadyPaid("Commission already paid")
        if _normalize_code(commission.get("status")) not in {"PAYABLE", "VALIDATED", "SCHEDULED", "CALCULATED"}:
            raise CommissionNotPayable("Commission not payable")
        payload = dict(commission.get("payload") or {})
        payload["status"] = "PAID"
        payload["provider_code"] = _normalize_code(provider_code)
        payload["provider_reference"] = provider_reference
        payload["paid_at"] = _utcnow()
        payload["payout_id"] = payout_id
        payload["metadata"] = metadata or {}
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_commissions SET status = 'PAID', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), commission_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="commission.paid",
            object_type="commission",
            object_id=commission_id,
            previous_state=commission,
            new_state=self._financial_get("financial_commissions", record_id=commission_id),
            reason="commission paid",
        )
        return self._financial_get("financial_commissions", record_id=commission_id)

    def create_payout(
        self,
        *,
        beneficiary_user_id: int | None,
        beneficiary_organization_id: int | None,
        commission_ids: list[int],
        gross_amount_minor: int,
        retained_amount_minor: int = 0,
        fee_minor: int = 0,
        currency: str = "XAF",
        mode: str = "manual",
        provider_code: str = "MANUAL",
        scheduled_at: str | None = None,
        actor_user_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        if gross_amount_minor <= 0:
            raise ValidationError("gross amount must be positive")
        net_amount_minor = max(0, gross_amount_minor - retained_amount_minor - fee_minor)
        payload = {
            "beneficiary_user_id": beneficiary_user_id,
            "beneficiary_organization_id": beneficiary_organization_id,
            "owner_user_id": beneficiary_user_id,
            "owner_org_id": beneficiary_organization_id,
            "commission_ids": commission_ids,
            "gross_amount_minor": int(gross_amount_minor),
            "retained_amount_minor": int(retained_amount_minor),
            "fee_minor": int(fee_minor),
            "net_amount_minor": int(net_amount_minor),
            "currency": self._ensure_currency(currency),
            "mode": mode,
            "provider_code": _normalize_code(provider_code),
            "scheduled_at": scheduled_at or _utcnow(),
            "processed_at": None,
            "metadata": metadata or {},
        }
        payout = self._insert_financial_record(
            "financial_payouts",
            name="Payout",
            kind="payout",
            scope=provider_code,
            status="DRAFT",
            payload=payload,
            reference_id=beneficiary_user_id,
            secondary_id=beneficiary_organization_id,
            record_key=_record_key("payout", beneficiary_user_id, beneficiary_organization_id, commission_ids, gross_amount_minor, currency),
            number_prefix="REV",
        )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payout.created",
            object_type="payout",
            object_id=int(payout["id"]),
            previous_state={},
            new_state=payout,
            reason="payout created",
        )
        return payout

    def list_payouts(
        self,
        *,
        status: str | None = None,
        beneficiary_user_id: int | None = None,
        beneficiary_organization_id: int | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_payouts", status=status, limit=limit, owner_user_id=beneficiary_user_id, organization_id=beneficiary_organization_id)
        return items

    def approve_payout(self, payout_id: int, *, actor_user_id: int | None = None) -> dict[str, object]:
        payout = self._financial_get("financial_payouts", record_id=payout_id)
        if _normalize_code(payout.get("status")) == "PAID":
            return payout
        return self._update_financial_record("financial_payouts", payout_id, status="APPROVED", payload={"approved_at": _utcnow(), "approved_by_user_id": actor_user_id})

    def process_payout(self, payout_id: int, *, provider_reference: str | None = None, actor_user_id: int | None = None) -> dict[str, object]:
        payout = self._financial_get("financial_payouts", record_id=payout_id)
        payload = dict(payout.get("payload") or {})
        payload["provider_reference"] = provider_reference or payload.get("provider_reference")
        payload["processed_at"] = _utcnow()
        payload["status"] = "PAID"
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_payouts SET status = 'PAID', payload_json = ?, updated_at = ? WHERE id = ?",
                (_json(payload), _utcnow(), payout_id),
            )
        self.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="payout.paid",
            object_type="payout",
            object_id=payout_id,
            previous_state=payout,
            new_state=self._financial_get("financial_payouts", record_id=payout_id),
            reason="payout processed",
        )
        return self._financial_get("financial_payouts", record_id=payout_id)

    # ------------------------------------------------------------------
    # Ledger
    # ------------------------------------------------------------------

    def list_ledger_accounts(self, *, status: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        return self._financial_list("financial_ledger_accounts", status=status, limit=limit)

    def get_ledger_account(self, account_id: int) -> dict[str, object]:
        return self._financial_get("financial_ledger_accounts", record_id=account_id)

    def create_ledger_account(
        self,
        *,
        account_code: str,
        name: str,
        account_type: str = "asset",
        currency: str = "XAF",
        status: str = "active",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = {
            "account_code": account_code,
            "account_type": account_type,
            "currency": self._ensure_currency(currency),
            "balance_minor": 0,
            "metadata": metadata or {},
        }
        return self._insert_financial_record(
            "financial_ledger_accounts",
            name=name,
            kind="ledger_account",
            scope=account_type,
            status=status,
            payload=payload,
            record_key=f"ledger-account:{account_code.lower()}",
            number_prefix="LED",
        )

    def record_ledger_entry(
        self,
        *,
        debit_account_id: int,
        credit_account_id: int,
        source_type: str,
        source_id: int,
        amount_minor: int,
        currency: str = "XAF",
        transaction_id: int | None = None,
        description: str = "",
        effective_at: str | None = None,
        posted_at: str | None = None,
        actor_user_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        if amount_minor <= 0:
            raise ValidationError("ledger amount must be positive")
        payload = {
            "debit_account_id": debit_account_id,
            "credit_account_id": credit_account_id,
            "source_type": source_type,
            "source_id": source_id,
            "transaction_id": transaction_id,
            "amount_minor": int(amount_minor),
            "currency": self._ensure_currency(currency),
            "description": description,
            "effective_at": effective_at or _utcnow(),
            "posted_at": posted_at or _utcnow(),
            "actor_user_id": actor_user_id,
            "metadata": metadata or {},
        }
        entry = self._insert_financial_record(
            "financial_ledger_entries",
            name="Ledger Entry",
            kind="ledger_entry",
            scope=source_type,
            status="POSTED",
            payload=payload,
            parent_id=debit_account_id,
            reference_id=credit_account_id,
            secondary_id=transaction_id,
            record_key=_record_key("ledger-entry", debit_account_id, credit_account_id, source_type, source_id, amount_minor, transaction_id),
            number_prefix="JRN",
        )
        return entry

    def list_ledger_entries(
        self,
        *,
        source_type: str | None = None,
        source_id: int | None = None,
        transaction_id: int | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_ledger_entries", limit=limit, secondary_id=transaction_id)
        if source_type:
            items = [row for row in items if str((row.get("payload") or {}).get("source_type") or "").lower() == source_type.lower()]
        if source_id is not None:
            items = [row for row in items if int((row.get("payload") or {}).get("source_id") or 0) == int(source_id)]
        return items

    # ------------------------------------------------------------------
    # Reconciliation and audit
    # ------------------------------------------------------------------

    def create_reconciliation_record(
        self,
        *,
        provider_code: str,
        payment_intent_id: int | None = None,
        payment_attempt_id: int | None = None,
        payment_transaction_id: int | None = None,
        provider_event_id: int | None = None,
        invoice_id: int | None = None,
        receipt_id: int | None = None,
        internal_amount_minor: int = 0,
        provider_amount_minor: int = 0,
        currency: str = "XAF",
        conflict_type: str | None = None,
        conflict_details: dict[str, object] | None = None,
        status: str = "UNMATCHED",
        notes: str = "",
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        payload = {
            "provider_code": _normalize_code(provider_code),
            "payment_intent_id": payment_intent_id,
            "payment_attempt_id": payment_attempt_id,
            "payment_transaction_id": payment_transaction_id,
            "provider_event_id": provider_event_id,
            "invoice_id": invoice_id,
            "receipt_id": receipt_id,
            "internal_amount_minor": int(internal_amount_minor),
            "provider_amount_minor": int(provider_amount_minor),
            "currency": self._ensure_currency(currency),
            "conflict_type": conflict_type,
            "conflict_details": conflict_details or {},
            "notes": notes,
            "metadata": metadata or {},
        }
        record_status = _normalize_code(status)
        if record_status not in RECONCILIATION_STATUSES:
            record_status = "UNMATCHED"
        return self._insert_financial_record(
            "financial_reconciliation_records",
            name="Reconciliation",
            kind="reconciliation",
            scope=provider_code,
            status=record_status,
            payload=payload,
            parent_id=payment_intent_id,
            reference_id=payment_attempt_id,
            secondary_id=payment_transaction_id,
            record_key=_record_key("reconciliation", provider_code, payment_intent_id, payment_attempt_id, payment_transaction_id, provider_event_id, invoice_id, receipt_id),
            number_prefix="RCP",
        )

    def list_reconciliation_records(self, *, status: str | None = None, provider_code: str | None = None, limit: int = 100) -> list[dict[str, object]]:
        items = self._financial_list("financial_reconciliation_records", status=status, limit=limit)
        if provider_code:
            items = [row for row in items if _normalize_code((row.get("payload") or {}).get("provider_code")) == _normalize_code(provider_code)]
        return items

    def resolve_reconciliation(
        self,
        reconciliation_id: int,
        *,
        status: str = "RESOLVED",
        resolution_note: str = "",
        resolved_by_user_id: int | None = None,
        metadata: dict[str, object] | None = None,
    ) -> dict[str, object]:
        record = self._financial_get("financial_reconciliation_records", record_id=reconciliation_id)
        if _normalize_code(record.get("status")) == "RESOLVED":
            return record
        if _normalize_code(status) not in RECONCILIATION_STATUSES:
            raise ReconciliationConflict("unsupported reconciliation resolution")
        payload = dict(record.get("payload") or {})
        payload["resolved_at"] = _utcnow()
        payload["resolved_by_user_id"] = resolved_by_user_id
        payload["resolution_note"] = resolution_note
        payload["metadata"] = metadata or payload.get("metadata") or {}
        with self._transaction() as conn:
            conn.execute(
                "UPDATE financial_reconciliation_records SET status = ?, payload_json = ?, updated_at = ? WHERE id = ?",
                (_normalize_code(status), _json(payload), _utcnow(), reconciliation_id),
            )
        return self._financial_get("financial_reconciliation_records", record_id=reconciliation_id)

    def create_financial_audit_event(
        self,
        *,
        actor_user_id: int | None,
        action: str,
        object_type: str,
        object_id: int | None,
        previous_state: dict[str, object] | None,
        new_state: dict[str, object] | None,
        reason: str = "",
        result: str = "success",
        correlation_id: str | None = None,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        event_type = action if action in FINANCIAL_EVENT_TYPES else action
        data = {
            "action": action,
            "actor_user_id": actor_user_id,
            "object_type": object_type,
            "object_id": object_id,
            "previous_state": previous_state or {},
            "new_state": new_state or {},
            "reason": reason,
            "result": result,
            "correlation_id": correlation_id,
            "payload": payload or {},
            "event_type": event_type,
        }
        return self._insert_financial_record(
            "financial_audit_events",
            name="Financial Audit Event",
            kind=event_type,
            scope=object_type,
            status=result.upper() if result else "SUCCESS",
            payload=data,
            reference_id=object_id,
            secondary_id=actor_user_id,
            record_key=_record_key("financial-audit", action, object_type, object_id, actor_user_id, correlation_id, reason, result),
            number_prefix="AUD",
        )

    def list_financial_audit_events(
        self,
        *,
        actor_user_id: int | None = None,
        object_type: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        items = self._financial_list("financial_audit_events", limit=limit, secondary_id=actor_user_id)
        if object_type:
            items = [row for row in items if str((row.get("payload") or {}).get("object_type") or "").lower() == object_type.lower()]
        return items

    # ------------------------------------------------------------------
    # Dashboard and utilities
    # ------------------------------------------------------------------

    def financial_dashboard(self) -> dict[str, object]:
        providers = self.list_payment_providers(limit=100)
        payment_intents = self.list_payment_intents(limit=500)
        invoices = self.list_invoices(limit=500)
        receipts = self.list_receipts(limit=500)
        refunds = self.list_refunds(limit=500)
        subscriptions = self.list_subscriptions(limit=500)
        commissions = self.list_commissions(limit=500)
        payouts = self.list_payouts(limit=500)
        reconciliation = self.list_reconciliation_records(limit=500)
        summary = {
            "catalog_items": len(self.list_financial_products(limit=500)),
            "payment_providers": len(providers),
            "payment_intents": len(payment_intents),
            "invoices": len(invoices),
            "receipts": len(receipts),
            "refunds": len(refunds),
            "subscriptions": len(subscriptions),
            "commissions": len(commissions),
            "payouts": len(payouts),
            "reconciliation_conflicts": len([row for row in reconciliation if _normalize_code(row.get("status")) in {"CONFLICT", "MANUAL_REVIEW"}]),
            "total_invoiced_minor": sum(int((row.get("payload") or {}).get("breakdown", {}).get("total_minor") or 0) for row in invoices),
            "total_paid_minor": sum(int((row.get("payload") or {}).get("amount_paid_minor") or 0) for row in invoices),
            "total_receipted_minor": sum(int((row.get("payload") or {}).get("amount_minor") or 0) for row in receipts),
        }
        score_signals = [
            {"name": "provider_configured", "passed": any(_normalize_code((row.get("payload") or {}).get("provider_code")) == "CAMPAY" for row in providers), "weight": 15, "detail": "Campay provider configured"},
            {"name": "payment_status_known", "passed": any(_normalize_code(row.get("status")) == "SUCCEEDED" for row in payment_intents), "weight": 15, "detail": "At least one successful payment"},
            {"name": "invoice_settled", "passed": any(_normalize_code(row.get("status")) == "PAID" for row in invoices), "weight": 15, "detail": "At least one invoice paid"},
            {"name": "receipt_generated", "passed": len(receipts) > 0, "weight": 15, "detail": "Receipt generated"},
            {"name": "reconciliation_clear", "passed": all(_normalize_code(row.get("status")) in {"MATCHED", "RESOLVED"} for row in reconciliation) if reconciliation else True, "weight": 20, "detail": "No open reconciliation conflicts"},
            {"name": "refund_controlled", "passed": all(int((row.get("payload") or {}).get("requested_amount_minor") or 0) >= int((row.get("payload") or {}).get("refunded_amount_minor") or 0) for row in refunds) if refunds else True, "weight": 20, "detail": "Refund totals are controlled"},
        ]
        readiness = FINANCIAL_ENGINE.build_readiness_score(signals=score_signals)
        return {
            "summary": summary,
            "readiness": readiness,
            "providers": providers,
            "signals": score_signals,
        }
