from __future__ import annotations

from typing import Any

from ..errors import ValidationError
from ..user_roles import resolve_official_user_role
from .permissions import can_access_all, can_access_partner_scope, can_read_financial_object, can_manage_financial_object


class FinancialService:
    def __init__(self, repository, policy, config) -> None:
        self.repository = repository
        self.policy = policy
        self.config = config

    # ------------------------------------------------------------------
    # Access helpers
    # ------------------------------------------------------------------

    def _role(self, actor: dict[str, object] | None) -> str:
        return resolve_official_user_role(actor.get("role") if actor else None)

    def _is_admin(self, actor: dict[str, object] | None) -> bool:
        return can_access_all(actor)

    def _ensure_admin(self, actor: dict[str, object] | None) -> None:
        if not self._is_admin(actor):
            from ..services import PermissionDenied

            raise PermissionDenied("Only administrators can manage this financial resource")

    def _ensure_read_scope(self, actor: dict[str, object] | None, *, owner_id: int | None = None, owner_org_id: int | None = None) -> None:
        if not can_read_financial_object(actor, owner_id=owner_id, owner_org_id=owner_org_id):
            from ..services import PermissionDenied

            raise PermissionDenied("You are not allowed to access this financial resource")

    def _ensure_manage_scope(self, actor: dict[str, object] | None) -> None:
        if not can_manage_financial_object(actor):
            from ..services import PermissionDenied

            raise PermissionDenied("You are not allowed to manage this financial resource")

    # ------------------------------------------------------------------
    # Dashboard / readiness
    # ------------------------------------------------------------------

    def dashboard(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return self.repository.financial_dashboard()

    def readiness(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        dashboard = self.repository.financial_dashboard()
        return dashboard["readiness"]

    def provider_health(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        providers = self.repository.list_payment_providers(limit=100)
        campay = next((row for row in providers if str((row.get("payload") or {}).get("provider_code") or "").upper() == "CAMPAY"), None)
        if campay is None:
            return {"provider": None, "available": False}
        return {"provider": campay, "available": bool((campay.get("payload") or {}).get("health", {}).get("available", False))}

    # ------------------------------------------------------------------
    # Catalog
    # ------------------------------------------------------------------

    def list_products(self, *, actor: dict[str, object], status: str | None = None, limit: int = 100) -> dict[str, object]:
        items = self.repository.list_financial_products(status=status, limit=limit)
        return {"products": items}

    def create_product(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        product = self.repository.create_financial_product(
            code=str(body["code"]),
            name=str(body["name"]),
            description=str(body.get("description") or ""),
            category=str(body.get("category") or "service"),
            status=str(body.get("status") or "active"),
            unit=str(body.get("unit") or "item"),
            default_price_minor=int(body.get("default_price_minor") or 0),
            currency=str(body.get("currency") or "XAF"),
            tax_rate_bps=int(body.get("tax_rate_bps") or 0),
            duration_days=int(body["duration_days"]) if body.get("duration_days") is not None else None,
            billing_period=str(body["billing_period"]) if body.get("billing_period") is not None else None,
            eligible_roles=list(body.get("eligible_roles") or []),
            valid_from=str(body["valid_from"]) if body.get("valid_from") is not None else None,
            valid_until=str(body["valid_until"]) if body.get("valid_until") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"product": product}

    def list_pricing_rules(self, *, actor: dict[str, object], product_id: int | None = None, status: str | None = None, limit: int = 100) -> dict[str, object]:
        return {"pricing_rules": self.repository.list_pricing_rules(product_id=product_id, status=status, limit=limit)}

    def create_pricing_rule(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        rule = self.repository.create_pricing_rule(
            product_id=int(body["product_id"]) if body.get("product_id") is not None else None,
            code=str(body["code"]),
            name=str(body["name"]),
            rule_type=str(body.get("rule_type") or "fixed"),
            status=str(body.get("status") or "active"),
            amount_minor=int(body.get("amount_minor") or 0),
            amount_percent_bps=int(body.get("amount_percent_bps") or 0),
            fee_minor=int(body.get("fee_minor") or 0),
            tax_rate_bps=int(body.get("tax_rate_bps") or 0),
            scope=str(body.get("scope") or "global"),
            priority=int(body.get("priority") or 100),
            starts_at=str(body["starts_at"]) if body.get("starts_at") is not None else None,
            ends_at=str(body["ends_at"]) if body.get("ends_at") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"pricing_rule": rule}

    def calculate_price(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        line_items = body.get("line_items")
        if not isinstance(line_items, list):
            raise ValidationError("line_items must be a list")
        breakdown = self.repository.calculate_pricing(
            line_items=line_items,
            discount_minor=int(body.get("discount_minor") or 0),
            fee_minor=int(body.get("fee_minor") or 0),
            tax_rate_bps=int(body.get("tax_rate_bps") or 0),
            currency=str(body.get("currency") or "XAF"),
            context=body.get("context") if isinstance(body.get("context"), dict) else None,
        )
        return {"pricing_breakdown": breakdown}

    # ------------------------------------------------------------------
    # Quotes
    # ------------------------------------------------------------------

    def list_quotes(self, *, actor: dict[str, object], status: str | None = None, customer_user_id: int | None = None, organization_id: int | None = None, limit: int = 100) -> dict[str, object]:
        if not can_read_financial_object(actor, owner_id=customer_user_id, owner_org_id=organization_id) and not self._is_admin(actor):
            from ..services import PermissionDenied

            raise PermissionDenied("Cannot list quotes outside your scope")
        return {
            "quotes": self.repository.list_quotes(
                status=status,
                customer_user_id=customer_user_id if not self._is_admin(actor) else customer_user_id,
                organization_id=organization_id if not self._is_admin(actor) else organization_id,
                limit=limit,
            )
        }

    def get_quote(self, *, actor: dict[str, object], quote_id: int) -> dict[str, object]:
        quote = self.repository.get_quote(quote_id)
        self._ensure_read_scope(actor, owner_id=int((quote.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((quote.get("payload") or {}).get("organization_id") or 0) or None)
        return {"quote": quote}

    def create_quote(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        customer_user_id = int(body.get("customer_user_id") or actor["id"])
        organization_id = int(body["organization_id"]) if body.get("organization_id") is not None else int(actor.get("organization_id") or 0) or None
        quote = self.repository.create_quote(
            actor_user_id=int(actor["id"]),
            customer_user_id=customer_user_id,
            organization_id=organization_id,
            lines=list(body.get("lines") or []),
            currency=str(body.get("currency") or "XAF"),
            discount_minor=int(body.get("discount_minor") or 0),
            fee_minor=int(body.get("fee_minor") or 0),
            tax_rate_bps=int(body.get("tax_rate_bps") or 0),
            expires_at=str(body["expires_at"]) if body.get("expires_at") is not None else None,
            business_reference=str(body["business_reference"]) if body.get("business_reference") is not None else None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            source=str(body.get("source") or "internal"),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"quote": quote}

    def issue_quote(self, *, actor: dict[str, object], quote_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"quote": self.repository.issue_quote(quote_id)}

    def accept_quote(self, *, actor: dict[str, object], quote_id: int) -> dict[str, object]:
        quote = self.repository.get_quote(quote_id)
        self._ensure_read_scope(actor, owner_id=int((quote.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((quote.get("payload") or {}).get("organization_id") or 0) or None)
        return {"quote": self.repository.accept_quote(quote_id)}

    def reject_quote(self, *, actor: dict[str, object], quote_id: int) -> dict[str, object]:
        quote = self.repository.get_quote(quote_id)
        self._ensure_read_scope(actor, owner_id=int((quote.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((quote.get("payload") or {}).get("organization_id") or 0) or None)
        return {"quote": self.repository.reject_quote(quote_id)}

    def convert_quote(self, *, actor: dict[str, object], quote_id: int, body: dict[str, object]) -> dict[str, object]:
        quote = self.repository.get_quote(quote_id)
        self._ensure_read_scope(actor, owner_id=int((quote.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((quote.get("payload") or {}).get("organization_id") or 0) or None)
        invoice = self.repository.create_invoice(
            actor_user_id=int(actor["id"]),
            customer_user_id=int((quote.get("payload") or {}).get("customer_user_id") or actor["id"]),
            quote_id=quote_id,
            organization_id=int((quote.get("payload") or {}).get("organization_id") or 0) or None,
            lines=list((quote.get("payload") or {}).get("lines") or []),
            currency=str((quote.get("payload") or {}).get("currency") or body.get("currency") or "XAF"),
            amount_paid_minor=int(body.get("amount_paid_minor") or 0),
            business_reference=str(body["business_reference"]) if body.get("business_reference") is not None else None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            source="quote_conversion",
            status="DRAFT",
            due_at=str(body["due_at"]) if body.get("due_at") is not None else None,
            issued_at=str(body["issued_at"]) if body.get("issued_at") is not None else None,
            notes=str(body.get("notes") or ""),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        self.repository.issue_invoice(int(invoice["id"]))
        return {"invoice": invoice}

    # ------------------------------------------------------------------
    # Invoices / receipts
    # ------------------------------------------------------------------

    def list_invoices(self, *, actor: dict[str, object], status: str | None = None, customer_user_id: int | None = None, organization_id: int | None = None, limit: int = 100) -> dict[str, object]:
        if not can_read_financial_object(actor, owner_id=customer_user_id, owner_org_id=organization_id) and not self._is_admin(actor):
            from ..services import PermissionDenied

            raise PermissionDenied("Cannot list invoices outside your scope")
        return {"invoices": self.repository.list_invoices(status=status, customer_user_id=customer_user_id, organization_id=organization_id, limit=limit)}

    def get_invoice(self, *, actor: dict[str, object], invoice_id: int) -> dict[str, object]:
        invoice = self.repository.get_invoice(invoice_id)
        self._ensure_read_scope(actor, owner_id=int((invoice.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((invoice.get("payload") or {}).get("organization_id") or 0) or None)
        return {"invoice": invoice}

    def create_invoice(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        customer_user_id = int(body.get("customer_user_id") or actor["id"])
        organization_id = int(body["organization_id"]) if body.get("organization_id") is not None else int(actor.get("organization_id") or 0) or None
        invoice = self.repository.create_invoice(
            actor_user_id=int(actor["id"]),
            customer_user_id=customer_user_id,
            quote_id=int(body["quote_id"]) if body.get("quote_id") is not None else None,
            organization_id=organization_id,
            lines=list(body.get("lines") or []),
            currency=str(body.get("currency") or "XAF"),
            amount_paid_minor=int(body.get("amount_paid_minor") or 0),
            business_reference=str(body["business_reference"]) if body.get("business_reference") is not None else None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            source=str(body.get("source") or "internal"),
            status=str(body.get("status") or "DRAFT"),
            due_at=str(body["due_at"]) if body.get("due_at") is not None else None,
            issued_at=str(body["issued_at"]) if body.get("issued_at") is not None else None,
            notes=str(body.get("notes") or ""),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"invoice": invoice}

    def issue_invoice(self, *, actor: dict[str, object], invoice_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"invoice": self.repository.issue_invoice(invoice_id, issued_at=str(body["issued_at"]) if body.get("issued_at") is not None else None, due_at=str(body["due_at"]) if body.get("due_at") is not None else None)}

    def cancel_invoice(self, *, actor: dict[str, object], invoice_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"invoice": self.repository.cancel_invoice(invoice_id, reason=str(body.get("reason") or ""))}

    def create_credit_note(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        note = self.repository.apply_credit_note(
            invoice_id=int(body["invoice_id"]),
            amount_minor=int(body["amount_minor"]),
            reason=str(body.get("reason") or ""),
            actor_user_id=int(actor["id"]),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"credit_note": note}

    def list_receipts(self, *, actor: dict[str, object], invoice_id: int | None = None, status: str | None = None, limit: int = 100) -> dict[str, object]:
        items = self.repository.list_receipts(status=status, invoice_id=invoice_id, limit=limit)
        if not self._is_admin(actor):
            filtered: list[dict[str, object]] = []
            for item in items:
                payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
                if can_read_financial_object(actor, owner_id=int(payload.get("payer_user_id") or 0) or None, owner_org_id=int(payload.get("organization_id") or 0) or None):
                    filtered.append(item)
            items = filtered
        return {"receipts": items}

    def get_receipt(self, *, actor: dict[str, object], receipt_id: int) -> dict[str, object]:
        receipt = self.repository.get_receipt(receipt_id)
        self._ensure_read_scope(actor, owner_id=int((receipt.get("payload") or {}).get("payer_user_id") or 0) or None, owner_org_id=int((receipt.get("payload") or {}).get("organization_id") or 0) or None)
        return {"receipt": receipt}

    # ------------------------------------------------------------------
    # Payment providers / intents / attempts / transactions
    # ------------------------------------------------------------------

    def list_payment_providers(self, *, actor: dict[str, object], status: str | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payment_providers": self.repository.list_payment_providers(status=status, limit=limit)}

    def get_payment_provider(self, *, actor: dict[str, object], provider_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payment_provider": self.repository.get_payment_provider(provider_id)}

    def list_payment_intents(self, *, actor: dict[str, object], status: str | None = None, invoice_id: int | None = None, customer_user_id: int | None = None, provider_code: str | None = None, limit: int = 100) -> dict[str, object]:
        if not self._is_admin(actor):
            customer_user_id = int(actor["id"])
        return {
            "payment_intents": self.repository.list_payment_intents(
                status=status,
                invoice_id=invoice_id,
                customer_user_id=customer_user_id,
                provider_code=provider_code,
                limit=limit,
            )
        }

    def get_payment_intent(self, *, actor: dict[str, object], payment_intent_id: int) -> dict[str, object]:
        intent = self.repository.get_payment_intent(payment_intent_id)
        self._ensure_read_scope(actor, owner_id=int((intent.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((intent.get("payload") or {}).get("organization_id") or 0) or None)
        return {"payment_intent": intent}

    def create_payment_intent(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        invoice = self.repository.get_invoice(int(body["invoice_id"]))
        self._ensure_read_scope(
            actor,
            owner_id=int((invoice.get("payload") or {}).get("customer_user_id") or 0) or None,
            owner_org_id=int((invoice.get("payload") or {}).get("organization_id") or 0) or None,
        )
        customer_user_id = int(body.get("customer_user_id") or (invoice.get("payload") or {}).get("customer_user_id") or actor["id"])
        intent = self.repository.create_payment_intent(
            actor_user_id=int(actor["id"]),
            customer_user_id=customer_user_id,
            invoice_id=int(body["invoice_id"]),
            amount_minor=int(body["amount_minor"]),
            currency=str(body.get("currency") or "XAF"),
            description=str(body.get("description") or ""),
            provider_code=str(body.get("provider_code") or "CAMPAY"),
            channel=str(body.get("channel") or "mobile_money"),
            phone_number_e164=str(body["phone_number_e164"]) if body.get("phone_number_e164") is not None else None,
            expires_at=str(body["expires_at"]) if body.get("expires_at") is not None else None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            business_reference=str(body["business_reference"]) if body.get("business_reference") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"payment_intent": intent}

    def create_payment_attempt(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        attempt = self.repository.create_payment_attempt(
            payment_intent_id=payment_intent_id,
            provider_code=str(body.get("provider_code") or "CAMPAY"),
            request_json=body.get("request_json") if isinstance(body.get("request_json"), dict) else body,
            response_json=body.get("response_json") if isinstance(body.get("response_json"), dict) else None,
            provider_reference=str(body["provider_reference"]) if body.get("provider_reference") is not None else None,
            webhook_reference=str(body["webhook_reference"]) if body.get("webhook_reference") is not None else None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            error_code=str(body["error_code"]) if body.get("error_code") is not None else None,
            error_message=str(body["error_message"]) if body.get("error_message") is not None else None,
            status=str(body.get("status") or "PENDING"),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"payment_attempt": attempt}

    def confirm_payment(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return self.repository.confirm_payment_intent(
            payment_intent_id=payment_intent_id,
            payment_attempt_id=int(body["payment_attempt_id"]) if body.get("payment_attempt_id") is not None else None,
            provider_reference=str(body["provider_reference"]) if body.get("provider_reference") is not None else None,
            amount_minor=int(body["amount_minor"]) if body.get("amount_minor") is not None else None,
            currency=str(body["currency"]) if body.get("currency") is not None else None,
            provider_event_id=int(body["provider_event_id"]) if body.get("provider_event_id") is not None else None,
            actor_user_id=int(actor["id"]),
            proof=body.get("proof") if isinstance(body.get("proof"), dict) else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )

    def fail_payment(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payment_intent": self.repository.fail_payment_intent(payment_intent_id, error_code=str(body["error_code"]), error_message=str(body.get("error_message") or ""), actor_user_id=int(actor["id"]))}

    def expire_payment(self, *, actor: dict[str, object], payment_intent_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payment_intent": self.repository.expire_payment_intent(payment_intent_id, actor_user_id=int(actor["id"]))}

    def cancel_payment(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payment_intent": self.repository.cancel_payment_intent(payment_intent_id, actor_user_id=int(actor["id"]), reason=str(body.get("reason") or ""))}

    def list_payment_attempts(self, *, actor: dict[str, object], payment_intent_id: int | None = None, status: str | None = None, limit: int = 100) -> dict[str, object]:
        if self._is_admin(actor):
            return {"payment_attempts": self.repository.list_payment_attempts(payment_intent_id=payment_intent_id, status=status, limit=limit)}
        owned_intents = {int(row["id"]) for row in self.repository.list_payment_intents(customer_user_id=int(actor["id"]), limit=500)}
        if payment_intent_id is not None:
            if payment_intent_id not in owned_intents:
                return {"payment_attempts": []}
            owned_intents = {payment_intent_id}
        items = [row for row in self.repository.list_payment_attempts(status=status, limit=limit) if int(row.get("parent_id") or 0) in owned_intents]
        return {"payment_attempts": items}

    def list_payment_transactions(self, *, actor: dict[str, object], payment_intent_id: int | None = None, payment_attempt_id: int | None = None, invoice_id: int | None = None, status: str | None = None, limit: int = 100) -> dict[str, object]:
        if self._is_admin(actor):
            return {"payment_transactions": self.repository.list_payment_transactions(payment_intent_id=payment_intent_id, payment_attempt_id=payment_attempt_id, invoice_id=invoice_id, status=status, limit=limit)}
        owned_intents = {int(row["id"]) for row in self.repository.list_payment_intents(customer_user_id=int(actor["id"]), limit=500)}
        if payment_intent_id is not None:
            if payment_intent_id not in owned_intents:
                return {"payment_transactions": []}
            owned_intents = {payment_intent_id}
        items = [
            row
            for row in self.repository.list_payment_transactions(payment_attempt_id=payment_attempt_id, invoice_id=invoice_id, status=status, limit=limit)
            if int(row.get("parent_id") or 0) in owned_intents
        ]
        return {"payment_transactions": items}

    def list_provider_events(self, *, actor: dict[str, object], provider_code: str | None = None, status: str | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"provider_events": self.repository.list_provider_events(provider_code=provider_code, status=status, limit=limit)}

    # ------------------------------------------------------------------
    # Refunds
    # ------------------------------------------------------------------

    def list_refunds(self, *, actor: dict[str, object], payment_transaction_id: int | None = None, status: str | None = None, limit: int = 100) -> dict[str, object]:
        items = self.repository.list_refunds(payment_transaction_id=payment_transaction_id, status=status, limit=limit)
        if not self._is_admin(actor):
            filtered: list[dict[str, object]] = []
            for item in items:
                payload = item.get("payload") if isinstance(item.get("payload"), dict) else {}
                if can_read_financial_object(actor, owner_id=int(payload.get("requested_by_user_id") or 0) or None):
                    filtered.append(item)
            items = filtered
        return {"refunds": items}

    def request_refund(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        transaction = self.repository.get_payment_transaction(int(body["payment_transaction_id"]))
        invoice = self.repository.get_invoice(int(body["invoice_id"]))
        if int((transaction.get("payload") or {}).get("invoice_id") or 0) != int(invoice.get("id") or 0):
            raise ValidationError("Refund transaction must belong to the invoice")
        self._ensure_read_scope(
            actor,
            owner_id=int((invoice.get("payload") or {}).get("customer_user_id") or 0) or None,
            owner_org_id=int((invoice.get("payload") or {}).get("organization_id") or 0) or None,
        )
        refund = self.repository.request_refund(
            payment_transaction_id=int(body["payment_transaction_id"]),
            invoice_id=int(body["invoice_id"]),
            amount_minor=int(body["amount_minor"]),
            reason=str(body.get("reason") or ""),
            requested_by_user_id=int(actor["id"]),
            provider_code=str(body.get("provider_code") or "CAMPAY"),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"refund": refund}

    def approve_refund(self, *, actor: dict[str, object], refund_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"refund": self.repository.approve_refund(refund_id, actor_user_id=int(actor["id"]))}

    def process_refund(self, *, actor: dict[str, object], refund_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"refund": self.repository.process_refund(refund_id, provider_reference=str(body["provider_reference"]) if body.get("provider_reference") is not None else None, actor_user_id=int(actor["id"]), processed_amount_minor=int(body["processed_amount_minor"]) if body.get("processed_amount_minor") is not None else None)}

    # ------------------------------------------------------------------
    # Subscriptions
    # ------------------------------------------------------------------

    def list_subscription_plans(self, *, actor: dict[str, object], status: str | None = None, limit: int = 100) -> dict[str, object]:
        return {"subscription_plans": self.repository.list_subscription_plans(status=status, limit=limit)}

    def create_subscription_plan(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        plan = self.repository.create_subscription_plan(
            code=str(body["code"]),
            name=str(body["name"]),
            description=str(body.get("description") or ""),
            target=str(body.get("target") or "user"),
            price_minor=int(body.get("price_minor") or 0),
            currency=str(body.get("currency") or "XAF"),
            frequency=str(body.get("frequency") or "MONTHLY"),
            duration_days=int(body["duration_days"]) if body.get("duration_days") is not None else None,
            trial_days=int(body["trial_days"]) if body.get("trial_days") is not None else None,
            features=list(body.get("features") or []),
            limits=body.get("limits") if isinstance(body.get("limits"), dict) else None,
            conditions=body.get("conditions") if isinstance(body.get("conditions"), dict) else None,
            status=str(body.get("status") or "draft"),
            starts_at=str(body["starts_at"]) if body.get("starts_at") is not None else None,
            ends_at=str(body["ends_at"]) if body.get("ends_at") is not None else None,
            renewal_policy=body.get("renewal_policy") if isinstance(body.get("renewal_policy"), dict) else None,
            suspension_policy=body.get("suspension_policy") if isinstance(body.get("suspension_policy"), dict) else None,
            termination_policy=body.get("termination_policy") if isinstance(body.get("termination_policy"), dict) else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"subscription_plan": plan}

    def list_subscriptions(self, *, actor: dict[str, object], status: str | None = None, customer_user_id: int | None = None, organization_id: int | None = None, plan_id: int | None = None, limit: int = 100) -> dict[str, object]:
        if not self._is_admin(actor):
            customer_user_id = int(actor["id"])
        items = self.repository.list_subscriptions(status=status, customer_user_id=customer_user_id, organization_id=organization_id, plan_id=plan_id, limit=limit)
        return {"subscriptions": items}

    def get_subscription(self, *, actor: dict[str, object], subscription_id: int) -> dict[str, object]:
        subscription = self.repository.get_subscription(subscription_id)
        self._ensure_read_scope(actor, owner_id=int((subscription.get("payload") or {}).get("customer_user_id") or 0) or None, owner_org_id=int((subscription.get("payload") or {}).get("organization_id") or 0) or None)
        return {"subscription": subscription}

    def subscribe(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        subscription = self.repository.create_subscription(
            plan_id=int(body["plan_id"]),
            actor_user_id=int(actor["id"]),
            customer_user_id=int(body.get("customer_user_id") or actor["id"]),
            organization_id=int(body["organization_id"]) if body.get("organization_id") is not None else None,
            renewal_mode=str(body.get("renewal_mode") or "automatic"),
            preferred_payment_provider_code=str(body["preferred_payment_provider_code"]) if body.get("preferred_payment_provider_code") is not None else None,
            started_at=str(body["started_at"]) if body.get("started_at") is not None else None,
            current_period_start=str(body["current_period_start"]) if body.get("current_period_start") is not None else None,
            current_period_end=str(body["current_period_end"]) if body.get("current_period_end") is not None else None,
            next_billing_at=str(body["next_billing_at"]) if body.get("next_billing_at") is not None else None,
            status=str(body.get("status") or "PENDING"),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"subscription": subscription}

    def renew_subscription(self, *, actor: dict[str, object], subscription_id: int, body: dict[str, object]) -> dict[str, object]:
        return self.repository.renew_subscription(
            subscription_id,
            actor_user_id=int(actor["id"]),
            invoice_id=int(body["invoice_id"]) if body.get("invoice_id") is not None else None,
            payment_intent_id=int(body["payment_intent_id"]) if body.get("payment_intent_id") is not None else None,
            period_start=str(body["period_start"]) if body.get("period_start") is not None else None,
            period_end=str(body["period_end"]) if body.get("period_end") is not None else None,
            amount_minor=int(body["amount_minor"]) if body.get("amount_minor") is not None else None,
            currency=str(body["currency"]) if body.get("currency") is not None else None,
            due_at=str(body["due_at"]) if body.get("due_at") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )

    def change_subscription_plan(self, *, actor: dict[str, object], subscription_id: int, body: dict[str, object]) -> dict[str, object]:
        return {"subscription": self.repository.change_subscription_plan(subscription_id, new_plan_id=int(body["new_plan_id"]), actor_user_id=int(actor["id"]), immediate=bool(body.get("immediate")), prorata_minor=int(body.get("prorata_minor") or 0), metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None)}

    def suspend_subscription(self, *, actor: dict[str, object], subscription_id: int, body: dict[str, object]) -> dict[str, object]:
        return {"subscription": self.repository.suspend_subscription(subscription_id, actor_user_id=int(actor["id"]), reason=str(body.get("reason") or ""))}

    def cancel_subscription(self, *, actor: dict[str, object], subscription_id: int, body: dict[str, object]) -> dict[str, object]:
        return {"subscription": self.repository.cancel_subscription(subscription_id, actor_user_id=int(actor["id"]), reason=str(body.get("reason") or ""))}

    # ------------------------------------------------------------------
    # Commissions and payouts
    # ------------------------------------------------------------------

    def list_commission_rules(self, *, actor: dict[str, object], status: str | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"commission_rules": self.repository.list_commission_rules(status=status, limit=limit)}

    def create_commission_rule(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        rule = self.repository.create_commission_rule(
            code=str(body["code"]),
            name=str(body["name"]),
            actor_role=str(body.get("actor_role") or "partner"),
            service_code=str(body["service_code"]) if body.get("service_code") is not None else None,
            channel=str(body.get("channel") or "any"),
            amount_type=str(body.get("amount_type") or "percentage"),
            flat_amount_minor=int(body.get("flat_amount_minor") or 0),
            rate_bps=int(body.get("rate_bps") or 0),
            minimum_minor=int(body.get("minimum_minor") or 0),
            maximum_minor=int(body.get("maximum_minor") or 0),
            share=list(body.get("share") or []),
            priority=int(body.get("priority") or 100),
            starts_at=str(body["starts_at"]) if body.get("starts_at") is not None else None,
            ends_at=str(body["ends_at"]) if body.get("ends_at") is not None else None,
            status=str(body.get("status") or "active"),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"commission_rule": rule}

    def calculate_commission(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        commission = self.repository.calculate_commission(
            rule_id=int(body["rule_id"]),
            source_object_type=str(body["source_object_type"]),
            source_object_id=int(body["source_object_id"]),
            gross_amount_minor=int(body["gross_amount_minor"]),
            currency=str(body.get("currency") or "XAF"),
            beneficiary_user_id=int(body["beneficiary_user_id"]) if body.get("beneficiary_user_id") is not None else None,
            beneficiary_organization_id=int(body["beneficiary_organization_id"]) if body.get("beneficiary_organization_id") is not None else None,
            actor_user_id=int(actor["id"]),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"commission": commission}

    def list_commissions(self, *, actor: dict[str, object], status: str | None = None, beneficiary_user_id: int | None = None, beneficiary_organization_id: int | None = None, limit: int = 100) -> dict[str, object]:
        if not self._is_admin(actor) and beneficiary_user_id is None and beneficiary_organization_id is None:
            beneficiary_user_id = int(actor["id"])
        return {"commissions": self.repository.list_commissions(status=status, beneficiary_user_id=beneficiary_user_id, beneficiary_organization_id=beneficiary_organization_id, limit=limit)}

    def validate_commission(self, *, actor: dict[str, object], commission_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"commission": self.repository.validate_commission(commission_id, actor_user_id=int(actor["id"]))}

    def mark_commission_payable(self, *, actor: dict[str, object], commission_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"commission": self.repository.mark_commission_payable(commission_id, actor_user_id=int(actor["id"]))}

    def pay_commission(self, *, actor: dict[str, object], commission_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"commission": self.repository.pay_commission(commission_id, provider_code=str(body.get("provider_code") or "MANUAL"), provider_reference=str(body["provider_reference"]) if body.get("provider_reference") is not None else None, actor_user_id=int(actor["id"]), payout_id=int(body["payout_id"]) if body.get("payout_id") is not None else None, metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None)}

    def list_payouts(self, *, actor: dict[str, object], status: str | None = None, beneficiary_user_id: int | None = None, beneficiary_organization_id: int | None = None, limit: int = 100) -> dict[str, object]:
        if not self._is_admin(actor) and beneficiary_user_id is None and beneficiary_organization_id is None:
            beneficiary_user_id = int(actor["id"])
        return {"payouts": self.repository.list_payouts(status=status, beneficiary_user_id=beneficiary_user_id, beneficiary_organization_id=beneficiary_organization_id, limit=limit)}

    def create_payout(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        payout = self.repository.create_payout(
            beneficiary_user_id=int(body["beneficiary_user_id"]) if body.get("beneficiary_user_id") is not None else None,
            beneficiary_organization_id=int(body["beneficiary_organization_id"]) if body.get("beneficiary_organization_id") is not None else None,
            commission_ids=[int(item) for item in body.get("commission_ids") or []],
            gross_amount_minor=int(body["gross_amount_minor"]),
            retained_amount_minor=int(body.get("retained_amount_minor") or 0),
            fee_minor=int(body.get("fee_minor") or 0),
            currency=str(body.get("currency") or "XAF"),
            mode=str(body.get("mode") or "manual"),
            provider_code=str(body.get("provider_code") or "MANUAL"),
            scheduled_at=str(body["scheduled_at"]) if body.get("scheduled_at") is not None else None,
            actor_user_id=int(actor["id"]),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        return {"payout": payout}

    def approve_payout(self, *, actor: dict[str, object], payout_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payout": self.repository.approve_payout(payout_id, actor_user_id=int(actor["id"]))}

    def process_payout(self, *, actor: dict[str, object], payout_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"payout": self.repository.process_payout(payout_id, provider_reference=str(body["provider_reference"]) if body.get("provider_reference") is not None else None, actor_user_id=int(actor["id"]))}

    # ------------------------------------------------------------------
    # Ledger / reconciliation / audit
    # ------------------------------------------------------------------

    def list_ledger_accounts(self, *, actor: dict[str, object], status: str | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"ledger_accounts": self.repository.list_ledger_accounts(status=status, limit=limit)}

    def list_ledger_entries(self, *, actor: dict[str, object], source_type: str | None = None, source_id: int | None = None, transaction_id: int | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"ledger_entries": self.repository.list_ledger_entries(source_type=source_type, source_id=source_id, transaction_id=transaction_id, limit=limit)}

    def record_ledger_entry(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {
            "ledger_entry": self.repository.record_ledger_entry(
                debit_account_id=int(body["debit_account_id"]),
                credit_account_id=int(body["credit_account_id"]),
                source_type=str(body["source_type"]),
                source_id=int(body["source_id"]),
                amount_minor=int(body["amount_minor"]),
                currency=str(body.get("currency") or "XAF"),
                transaction_id=int(body["transaction_id"]) if body.get("transaction_id") is not None else None,
                description=str(body.get("description") or ""),
                effective_at=str(body["effective_at"]) if body.get("effective_at") is not None else None,
                posted_at=str(body["posted_at"]) if body.get("posted_at") is not None else None,
                actor_user_id=int(actor["id"]),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
            )
        }

    def list_reconciliation_records(self, *, actor: dict[str, object], status: str | None = None, provider_code: str | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"reconciliation_records": self.repository.list_reconciliation_records(status=status, provider_code=provider_code, limit=limit)}

    def create_reconciliation_record(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {
            "reconciliation_record": self.repository.create_reconciliation_record(
                provider_code=str(body["provider_code"]),
                payment_intent_id=int(body["payment_intent_id"]) if body.get("payment_intent_id") is not None else None,
                payment_attempt_id=int(body["payment_attempt_id"]) if body.get("payment_attempt_id") is not None else None,
                payment_transaction_id=int(body["payment_transaction_id"]) if body.get("payment_transaction_id") is not None else None,
                provider_event_id=int(body["provider_event_id"]) if body.get("provider_event_id") is not None else None,
                invoice_id=int(body["invoice_id"]) if body.get("invoice_id") is not None else None,
                receipt_id=int(body["receipt_id"]) if body.get("receipt_id") is not None else None,
                internal_amount_minor=int(body.get("internal_amount_minor") or 0),
                provider_amount_minor=int(body.get("provider_amount_minor") or 0),
                currency=str(body.get("currency") or "XAF"),
                conflict_type=str(body["conflict_type"]) if body.get("conflict_type") is not None else None,
                conflict_details=body.get("conflict_details") if isinstance(body.get("conflict_details"), dict) else None,
                status=str(body.get("status") or "UNMATCHED"),
                notes=str(body.get("notes") or ""),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
            )
        }

    def resolve_reconciliation(self, *, actor: dict[str, object], reconciliation_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {
            "reconciliation_record": self.repository.resolve_reconciliation(
                reconciliation_id,
                status=str(body.get("status") or "RESOLVED"),
                resolution_note=str(body.get("resolution_note") or ""),
                resolved_by_user_id=int(actor["id"]),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
            )
        }

    def list_audit_events(self, *, actor: dict[str, object], actor_user_id: int | None = None, object_type: str | None = None, limit: int = 100) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        return {"audit_events": self.repository.list_financial_audit_events(actor_user_id=actor_user_id, object_type=object_type, limit=limit)}
