from __future__ import annotations

from typing import Any

from ..errors import ValidationError
from ..user_roles import resolve_official_user_role
from .exceptions import PaymentAlreadyProcessed
from ..observability import METRICS
from .permissions import can_access_all, can_access_partner_scope, can_read_financial_object, can_manage_financial_object
from .providers.registry import PaymentProviderRegistry, build_default_provider_registry


class FinancialService:
    def __init__(self, repository, policy, config, provider_registry: PaymentProviderRegistry | None = None) -> None:
        self.repository = repository
        self.policy = policy
        self.config = config
        self.provider_registry = provider_registry or build_default_provider_registry(config)

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

    def _provider_adapter(self, provider_code: str | None):
        if not provider_code:
            return None
        if self.provider_registry is None:
            return None
        return self.provider_registry.get(str(provider_code))

    def _campay_adapter(self):
        return self._provider_adapter("CAMPAY")

    def _ledger_account_id(self, account_code: str) -> int:
        for row in self.repository.list_ledger_accounts(limit=100):
            payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
            if str(payload.get("account_code") or "").upper() == account_code.upper():
                return int(row["id"])
        raise ValidationError(f"Ledger account {account_code} is missing")

    def _update_attempt_status(
        self,
        *,
        payment_intent_id: int,
        status: str,
        provider_reference: str | None = None,
        response_json: dict[str, object] | None = None,
        error_code: str | None = None,
        error_message: str | None = None,
    ) -> dict[str, object] | None:
        attempts = self.repository.list_payment_attempts(payment_intent_id=payment_intent_id, limit=1)
        if not attempts:
            return None
        attempt = attempts[0]
        payload = dict(attempt.get("payload") or {})
        payload["status"] = status
        if provider_reference is not None:
            payload["provider_reference"] = provider_reference
        if response_json is not None:
            payload["response_json"] = response_json
        if error_code is not None:
            payload["error_code"] = error_code
        if error_message is not None:
            payload["error_message"] = error_message
        return self.repository.update_payment_attempt(int(attempt["id"]), status=status, payload=payload)

    def _record_payment_ledger(
        self,
        *,
        payment_transaction: dict[str, object],
        invoice: dict[str, object],
        actor_user_id: int | None,
        reason: str = "payment settled",
    ) -> dict[str, object]:
        debit_account_id = self._ledger_account_id("CASH_CONFIRMED")
        credit_account_id = self._ledger_account_id("AR")
        payload = payment_transaction.get("payload") if isinstance(payment_transaction.get("payload"), dict) else {}
        amount_minor = int(payload.get("amount_minor") or 0)
        currency = str(payload.get("currency") or "XAF")
        if amount_minor <= 0:
            raise ValidationError("payment transaction amount is required for ledger posting")
        entry = self.repository.record_ledger_entry(
            debit_account_id=debit_account_id,
            credit_account_id=credit_account_id,
            source_type="payment_transaction",
            source_id=int(payment_transaction["id"]),
            amount_minor=amount_minor,
            currency=currency,
            transaction_id=int(payment_transaction["id"]),
            description=f"{reason}: invoice {invoice.get('name') or invoice.get('number') or invoice.get('id')}",
            effective_at=str(payload.get("effective_at") or payload.get("posted_at") or ""),
            posted_at=str(payload.get("posted_at") or ""),
            actor_user_id=actor_user_id,
            metadata={
                "invoice_id": int(invoice["id"]),
                "payment_intent_id": int(payload.get("payment_intent_id") or 0),
                "payment_attempt_id": int(payload.get("payment_attempt_id") or 0) if payload.get("payment_attempt_id") is not None else None,
                "provider_reference": payload.get("provider_reference"),
            },
        )
        self.repository.create_financial_audit_event(
            actor_user_id=actor_user_id,
            action="ledger.entry.created",
            object_type="ledger_entry",
            object_id=int(entry["id"]),
            previous_state={},
            new_state=entry,
            reason=reason,
            payload={"payment_transaction_id": int(payment_transaction["id"]), "invoice_id": int(invoice["id"])},
        )
        return entry

    def _latest_payment_attempt(self, payment_intent_id: int) -> dict[str, object] | None:
        attempts = self.repository.list_payment_attempts(payment_intent_id=payment_intent_id, limit=1)
        return attempts[0] if attempts else None

    def _payment_reference_candidates(self, intent: dict[str, object]) -> set[str]:
        payload = intent.get("payload") if isinstance(intent.get("payload"), dict) else {}
        candidates = {
            str(intent.get("number") or "").strip(),
            str(payload.get("provider_reference") or "").strip(),
            str(payload.get("business_reference") or "").strip(),
            str(payload.get("external_reference") or "").strip(),
            str(payload.get("number") or "").strip(),
            str(payload.get("idempotency_key") or "").strip(),
        }
        attempts = intent.get("attempts") if isinstance(intent.get("attempts"), list) else []
        for attempt in attempts:
            attempt_payload = attempt.get("payload") if isinstance(attempt.get("payload"), dict) else {}
            candidates.update(
                {
                    str(attempt_payload.get("provider_reference") or "").strip(),
                    str(attempt_payload.get("webhook_reference") or "").strip(),
                    str(attempt_payload.get("idempotency_key") or "").strip(),
                    str(attempt_payload.get("reference") or "").strip(),
                }
            )
        return {candidate for candidate in candidates if candidate}

    def _find_payment_intent_by_provider_reference(self, provider_reference: str) -> dict[str, object] | None:
        candidate = str(provider_reference or "").strip()
        if not candidate:
            return None
        for intent in self.repository.list_payment_intents(provider_code="CAMPAY", limit=500):
            if candidate in self._payment_reference_candidates(intent):
                return intent
        return None

    def _find_payment_attempt_by_provider_reference(self, provider_reference: str) -> dict[str, object] | None:
        candidate = str(provider_reference or "").strip()
        if not candidate:
            return None
        for attempt in self.repository.list_payment_attempts(limit=500):
            payload = attempt.get("payload") if isinstance(attempt.get("payload"), dict) else {}
            attempt_candidates = {
                str(payload.get("provider_reference") or "").strip(),
                str(payload.get("webhook_reference") or "").strip(),
                str(payload.get("reference") or "").strip(),
                str(payload.get("idempotency_key") or "").strip(),
            }
            if candidate in {value for value in attempt_candidates if value}:
                return attempt
        return None

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
        adapter = self._campay_adapter()
        if adapter is None:
            providers = self.repository.list_payment_providers(limit=100)
            campay = next((row for row in providers if str((row.get("payload") or {}).get("provider_code") or "").upper() == "CAMPAY"), None)
            return {"provider": campay, "available": bool((campay.get("payload") or {}).get("health", {}).get("available", False)) if campay else False}
        health = adapter.health_check()
        provider_row = self.repository.upsert_payment_provider_health(provider_code="CAMPAY", health=health.to_dict())
        return {"provider": provider_row, "available": health.available, "health": health.to_dict()}

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
        invoice_payload = invoice.get("payload") or {}
        amount_minor = int(body.get("amount_minor") or int(invoice_payload.get("balance_minor") or invoice_payload.get("breakdown", {}).get("total_minor") or 0))
        currency = str(body.get("currency") or invoice_payload.get("currency") or "XAF")
        initiate = bool(body.get("initiate") or body.get("send_to_provider") or body.get("auto_initiate"))
        phone_number = str(body.get("phone_number_e164") or invoice_payload.get("phone_number_e164") or "").strip()
        if initiate and not phone_number:
            raise ValidationError("phone_number_e164 is required to initiate Campay payment")
        intent = self.repository.create_payment_intent(
            actor_user_id=int(actor["id"]),
            customer_user_id=customer_user_id,
            invoice_id=int(body["invoice_id"]),
            amount_minor=amount_minor,
            currency=currency,
            description=str(body.get("description") or ""),
            provider_code=str(body.get("provider_code") or "CAMPAY"),
            channel=str(body.get("channel") or "mobile_money"),
            phone_number_e164=phone_number or None,
            expires_at=str(body["expires_at"]) if body.get("expires_at") is not None else None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            business_reference=str(body["business_reference"]) if body.get("business_reference") is not None else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        if not initiate:
            return {"payment_intent": self.repository.get_payment_intent(int(intent["id"]))}

        provider_code = str(body.get("provider_code") or "CAMPAY")
        adapter = self._provider_adapter(provider_code)
        if adapter is None:
            self.repository.update_payment_intent(
                int(intent["id"]),
                status="PENDING",
                payload={
                    "status": "PENDING",
                    "provider_status": "UNAVAILABLE",
                    "provider_error": {"error_code": "provider_unavailable", "error_message": "Payment provider is unavailable"},
                    "initiation_requested": True,
                },
            )
            return {
                "payment_intent": self.repository.get_payment_intent(int(intent["id"])),
                "provider_available": False,
            }

        intent_payload = dict((self.repository.get_payment_intent(int(intent["id"])) or {}).get("payload") or {})
        phone_number = str(body.get("phone_number_e164") or intent_payload.get("phone_number_e164") or phone_number or "").strip()
        external_reference = str(
            body.get("external_reference")
            or intent_payload.get("number")
            or intent_payload.get("business_reference")
            or f"LAWIM-{intent['id']}"
        )
        provider_payload = {
            "amount_minor": amount_minor,
            "currency": currency,
            "phone_number_e164": phone_number,
            "description": str(body.get("description") or intent_payload.get("description") or ""),
            "external_reference": external_reference,
            "reference": external_reference,
            "business_reference": intent_payload.get("business_reference") or external_reference,
            "callback_url": str(body.get("callback_url") or getattr(self.config, "campay_webhook_url", "") or ""),
            "redirect_url": str(body.get("redirect_url") or getattr(self.config, "campay_redirect_url", "") or ""),
            "metadata": body.get("metadata") if isinstance(body.get("metadata"), dict) else intent_payload.get("metadata") or {},
        }
        provider_response = adapter.create_payment(payload=provider_payload)
        provider_status = str(provider_response.get("status") or "PENDING").upper()
        provider_reference = str(provider_response.get("provider_reference") or provider_response.get("reference") or external_reference)
        attempt_status = provider_status if provider_status in {"PENDING", "PROCESSING", "REQUIRES_ACTION", "SUCCEEDED", "FAILED", "CANCELLED", "EXPIRED"} else "PENDING"
        attempt = self.repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code=provider_code,
            request_json=provider_payload,
            response_json=provider_response if isinstance(provider_response, dict) else {"provider_response": provider_response},
            provider_reference=provider_reference,
            webhook_reference=None,
            idempotency_key=str(body["idempotency_key"]) if body.get("idempotency_key") is not None else None,
            error_code=str(provider_response.get("error_code")) if isinstance(provider_response, dict) and provider_response.get("error_code") is not None else None,
            error_message=str(provider_response.get("error_message") or "") if isinstance(provider_response, dict) else None,
            status=attempt_status,
            metadata={"provider_response": provider_response} if isinstance(provider_response, dict) else {"provider_response": provider_response},
        )
        self.repository.update_payment_intent(
            int(intent["id"]),
            status=attempt_status,
            payload={
                "status": attempt_status,
                "provider_reference": provider_reference,
                "provider_attempt_id": int(attempt["id"]),
                "provider_response": provider_response,
                "initiation_requested": True,
            },
        )
        if not isinstance(provider_response, dict) or not provider_response.get("ok", True):
            self.repository.update_payment_intent(
                int(intent["id"]),
                status="PENDING",
                payload={
                    "status": "PENDING",
                    "provider_error": provider_response if isinstance(provider_response, dict) else {"provider_response": provider_response},
                },
            )
            return {
                "payment_intent": self.repository.get_payment_intent(int(intent["id"])),
                "payment_attempt": self.repository.get_payment_attempt(int(attempt["id"])),
                "provider_available": False,
                "provider_response": provider_response,
            }

        if provider_status == "SUCCESSFUL":
            try:
                confirmation = self.confirm_payment(
                    actor={"id": int(actor["id"]), "role": "admin"},
                    payment_intent_id=int(intent["id"]),
                    body={
                        "payment_attempt_id": int(attempt["id"]),
                        "provider_reference": provider_reference,
                        "amount_minor": amount_minor,
                        "currency": currency,
                        "provider_event_id": None,
                        "proof": {"provider_response": provider_response},
                        "metadata": {"provider_response": provider_response},
                    },
                )
            except PaymentAlreadyProcessed:
                transactions = self.repository.list_payment_transactions(payment_intent_id=int(intent["id"]), limit=1)
                confirmation = {
                    "payment_intent": self.repository.get_payment_intent(int(intent["id"])),
                    "payment_transaction": transactions[0] if transactions else None,
                    "invoice": self.repository.get_invoice(int(intent["parent_id"])) if intent.get("parent_id") else None,
                }
            confirmation["provider_available"] = True
            confirmation["provider_response"] = provider_response
            confirmation["payment_attempt"] = self.repository.get_payment_attempt(int(attempt["id"]))
            return confirmation

        return {
            "payment_intent": self.repository.get_payment_intent(int(intent["id"])),
            "payment_attempt": self.repository.get_payment_attempt(int(attempt["id"])),
            "provider_available": True,
            "provider_response": provider_response,
        }

    def create_payment_attempt(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        intent = self.repository.get_payment_intent(payment_intent_id)
        payload = intent.get("payload") or {}
        if self._is_admin(actor):
            pass
        else:
            self._ensure_read_scope(
                actor,
                owner_id=int(payload.get("customer_user_id") or 0) or None,
                owner_org_id=int(payload.get("organization_id") or 0) or None,
            )
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
        payment_attempt_id = int(body["payment_attempt_id"]) if body.get("payment_attempt_id") is not None else None
        if payment_attempt_id is None:
            attempts = self.repository.list_payment_attempts(payment_intent_id=payment_intent_id, limit=1)
            if attempts:
                payment_attempt_id = int(attempts[0]["id"])
        result = self.repository.confirm_payment_intent(
            payment_intent_id=payment_intent_id,
            payment_attempt_id=payment_attempt_id,
            provider_reference=str(body["provider_reference"]) if body.get("provider_reference") is not None else None,
            amount_minor=int(body["amount_minor"]) if body.get("amount_minor") is not None else None,
            currency=str(body["currency"]) if body.get("currency") is not None else None,
            provider_event_id=int(body["provider_event_id"]) if body.get("provider_event_id") is not None else None,
            actor_user_id=int(actor["id"]),
            proof=body.get("proof") if isinstance(body.get("proof"), dict) else None,
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        payment_transaction = result.get("payment_transaction")
        invoice = result.get("invoice")
        if isinstance(payment_transaction, dict) and isinstance(invoice, dict):
            ledger_entry = self._record_payment_ledger(
                payment_transaction=payment_transaction,
                invoice=invoice,
                actor_user_id=int(actor["id"]),
            )
            result["ledger_entry"] = ledger_entry
        return result

    def fail_payment(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        intent = self.repository.fail_payment_intent(payment_intent_id, error_code=str(body["error_code"]), error_message=str(body.get("error_message") or ""), actor_user_id=int(actor["id"]))
        self._update_attempt_status(
            payment_intent_id=payment_intent_id,
            status="FAILED",
            provider_reference=str(body.get("provider_reference") or intent.get("payload", {}).get("provider_reference") or ""),
            error_code=str(body["error_code"]),
            error_message=str(body.get("error_message") or ""),
        )
        return {"payment_intent": intent}

    def expire_payment(self, *, actor: dict[str, object], payment_intent_id: int) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        intent = self.repository.expire_payment_intent(payment_intent_id, actor_user_id=int(actor["id"]))
        self._update_attempt_status(payment_intent_id=payment_intent_id, status="EXPIRED", provider_reference=str(intent.get("payload", {}).get("provider_reference") or ""))
        return {"payment_intent": intent}

    def cancel_payment(self, *, actor: dict[str, object], payment_intent_id: int, body: dict[str, object]) -> dict[str, object]:
        self._ensure_manage_scope(actor)
        intent = self.repository.cancel_payment_intent(payment_intent_id, actor_user_id=int(actor["id"]), reason=str(body.get("reason") or ""))
        self._update_attempt_status(payment_intent_id=payment_intent_id, status="CANCELLED", provider_reference=str(intent.get("payload", {}).get("provider_reference") or ""))
        return {"payment_intent": intent}

    def get_payment_status(self, *, actor: dict[str, object], payment_intent_id: int) -> dict[str, object]:
        intent = self.repository.get_payment_intent(payment_intent_id)
        self._ensure_read_scope(
            actor,
            owner_id=int((intent.get("payload") or {}).get("customer_user_id") or 0) or None,
            owner_org_id=int((intent.get("payload") or {}).get("organization_id") or 0) or None,
        )
        provider_code = str((intent.get("payload") or {}).get("provider_code") or "CAMPAY")
        provider_reference = ""
        payload = intent.get("payload") if isinstance(intent.get("payload"), dict) else {}
        if payload:
            provider_reference = str(payload.get("provider_reference") or payload.get("external_reference") or payload.get("business_reference") or "").strip()
        if not provider_reference:
            latest_attempt = self._latest_payment_attempt(payment_intent_id)
            if latest_attempt is not None:
                attempt_payload = latest_attempt.get("payload") if isinstance(latest_attempt.get("payload"), dict) else {}
                provider_reference = str(attempt_payload.get("provider_reference") or attempt_payload.get("reference") or attempt_payload.get("webhook_reference") or "").strip()
        provider = self._provider_adapter(provider_code)
        if provider is None or not provider_reference:
            return {"payment_intent": intent, "provider_available": False, "provider_status": None}
        status_result = provider.get_payment_status(provider_reference=provider_reference)
        if not status_result.get("ok", True):
            self.repository.record_provider_event(
                provider_code=provider_code,
                event_type="status_check",
                provider_event_id=str(status_result.get("status_code") or status_result.get("error_code") or provider_reference),
                payload={"status_result": status_result, "provider_reference": provider_reference},
                headers={},
                source_reference=provider_reference,
                correlation_id=str((intent.get("payload") or {}).get("correlation_id") or ""),
                idempotency_key=str((intent.get("payload") or {}).get("idempotency_key") or provider_reference),
            )
            return {"payment_intent": intent, "provider_available": False, "provider_status": status_result}

        provider_status = str(status_result.get("status") or "UNKNOWN").upper()
        amount_minor = int(status_result.get("amount_minor") or (intent.get("payload") or {}).get("amount_minor") or 0)
        currency = str(status_result.get("currency") or (intent.get("payload") or {}).get("currency") or "XAF")
        provider_reference = str(status_result.get("provider_reference") or provider_reference)
        latest_attempt = self._find_payment_attempt_by_provider_reference(provider_reference) or self._latest_payment_attempt(payment_intent_id)
        if provider_status == "SUCCESSFUL":
            try:
                confirmation = self.confirm_payment(
                    actor={"id": int(actor["id"]), "role": "admin"},
                    payment_intent_id=payment_intent_id,
                    body={
                        "payment_attempt_id": int(latest_attempt["id"]) if latest_attempt else None,
                        "provider_reference": provider_reference,
                        "amount_minor": amount_minor,
                        "currency": currency,
                        "provider_event_id": None,
                        "proof": {"provider_status": status_result},
                        "metadata": {"provider_status": status_result},
                    },
                )
            except PaymentAlreadyProcessed:
                transactions = self.repository.list_payment_transactions(payment_intent_id=payment_intent_id, limit=1)
                confirmation = {
                    "payment_intent": self.repository.get_payment_intent(payment_intent_id),
                    "payment_transaction": transactions[0] if transactions else None,
                    "invoice": self.repository.get_invoice(int(intent.get("parent_id"))) if intent.get("parent_id") else None,
                }
            confirmation["provider_status"] = status_result
            confirmation["provider_available"] = True
            return confirmation
        if provider_status in {"FAILED", "CANCELLED"}:
            failed = self.fail_payment(
                actor={"id": int(actor["id"]), "role": "admin"},
                payment_intent_id=payment_intent_id,
                body={
                    "error_code": provider_status.lower(),
                    "error_message": str(status_result.get("raw") or ""),
                    "provider_reference": provider_reference,
                },
            )
            failed["provider_status"] = status_result
            failed["provider_available"] = True
            return failed
        if provider_status == "EXPIRED":
            expired = self.expire_payment(actor={"id": int(actor["id"]), "role": "admin"}, payment_intent_id=payment_intent_id)
            expired["provider_status"] = status_result
            expired["provider_available"] = True
            return expired

        self.repository.update_payment_intent(
            payment_intent_id,
            status="PROCESSING" if provider_status == "PROCESSING" else "PENDING",
            payload={
                "status": "PROCESSING" if provider_status == "PROCESSING" else "PENDING",
                "provider_reference": provider_reference,
                "last_status_check": status_result,
            },
        )
        if latest_attempt is not None:
            self.repository.update_payment_attempt(
                int(latest_attempt["id"]),
                status="PROCESSING" if provider_status == "PROCESSING" else "PENDING",
                payload={**(latest_attempt.get("payload") or {}), "provider_status": status_result, "provider_reference": provider_reference},
            )
        return {
            "payment_intent": self.repository.get_payment_intent(payment_intent_id),
            "provider_status": status_result,
            "provider_available": True,
        }

    def process_campay_webhook(self, *, raw_body: bytes, headers: dict[str, str], actor_user_id: int | None = None) -> dict[str, object]:
        adapter = self._campay_adapter()
        if adapter is None:
            METRICS.increment("campay_webhook_rejected_total")
            raise ValidationError("Campay provider is unavailable")
        if not adapter.validate_webhook(headers=headers, payload=raw_body):
            METRICS.increment("campay_webhook_rejected_total")
            raise ValidationError("Invalid Campay webhook signature")

        parsed = adapter.parse_webhook(payload=raw_body)
        if not parsed.get("ok", True):
            METRICS.increment("campay_webhook_rejected_total")
            raise ValidationError(str(parsed.get("error_message") or "Invalid Campay webhook payload"))

        provider_event_id = str(parsed.get("provider_event_id") or parsed.get("payload_hash") or parsed.get("provider_reference") or "campay-webhook")
        provider_reference = str(parsed.get("provider_reference") or "").strip()
        duplicate_before = any(
            str((row.get("payload") or {}).get("provider_event_id") or "") == provider_event_id
            for row in self.repository.list_provider_events(provider_code="CAMPAY", limit=500)
        )
        if duplicate_before:
            METRICS.increment("campay_webhook_duplicate_total")
        else:
            METRICS.increment("campay_webhook_received_total")

        safe_headers = {
            key: ("[redacted]" if "signature" in key.lower() or "authorization" in key.lower() else str(value))
            for key, value in headers.items()
        }
        provider_event = self.repository.record_provider_event(
            provider_code="CAMPAY",
            event_type=str(parsed.get("event_type") or parsed.get("status") or "webhook"),
            provider_event_id=provider_event_id,
            payload=parsed.get("raw") if isinstance(parsed.get("raw"), dict) else {"raw": parsed.get("raw")},
            headers=safe_headers,
            source_reference=provider_reference or provider_event_id,
            correlation_id=str(parsed.get("correlation_id") or ""),
            idempotency_key=str(parsed.get("idempotency_key") or provider_event_id),
        )

        attempt = self._find_payment_attempt_by_provider_reference(provider_reference)
        intent = self._find_payment_intent_by_provider_reference(provider_reference)
        if intent is None and attempt is not None and attempt.get("parent_id") is not None:
            intent = self.repository.get_payment_intent(int(attempt["parent_id"]))
        if intent is None:
            reconciliation = self.repository.create_reconciliation_record(
                provider_code="CAMPAY",
                provider_event_id=int(provider_event["id"]),
                internal_amount_minor=0,
                provider_amount_minor=int(parsed.get("amount_minor") or 0),
                currency=str(parsed.get("currency") or "XAF"),
                conflict_type="orphan_transaction",
                conflict_details={
                    "provider_reference": provider_reference,
                    "event_type": parsed.get("event_type"),
                    "payload_hash": parsed.get("payload_hash"),
                },
                status="UNMATCHED",
                notes="Campay webhook could not be matched to an internal payment intent",
                metadata={"provider_event_id": provider_event_id},
            )
            return {"provider_event": provider_event, "reconciliation_record": reconciliation, "provider_status": parsed}

        intent_payload = intent.get("payload") if isinstance(intent.get("payload"), dict) else {}
        attempt = attempt or self._latest_payment_attempt(int(intent["id"]))
        amount_minor = int(parsed.get("amount_minor") or intent_payload.get("amount_minor") or 0)
        currency = str(parsed.get("currency") or intent_payload.get("currency") or "XAF")
        expected_amount = int(intent_payload.get("amount_minor") or 0)
        expected_currency = str(intent_payload.get("currency") or "XAF")

        if ((amount_minor and expected_amount and amount_minor != expected_amount) or currency.upper() != expected_currency.upper()):
            reconciliation = self.repository.create_reconciliation_record(
                provider_code="CAMPAY",
                payment_intent_id=int(intent["id"]),
                payment_attempt_id=int(attempt["id"]) if attempt is not None else None,
                provider_event_id=int(provider_event["id"]),
                invoice_id=int(intent.get("parent_id") or 0) or None,
                internal_amount_minor=expected_amount,
                provider_amount_minor=amount_minor,
                currency=currency,
                conflict_type="amount_mismatch" if amount_minor != expected_amount else "currency_mismatch",
                conflict_details={
                    "provider_reference": provider_reference,
                    "expected_amount_minor": expected_amount,
                    "expected_currency": expected_currency,
                    "actual_amount_minor": amount_minor,
                    "actual_currency": currency,
                },
                status="CONFLICT",
                notes="Campay webhook amount or currency did not match the internal intent",
                metadata={"provider_event_id": provider_event_id},
            )
            METRICS.increment("campay_status_conflict_total")
            return {"provider_event": provider_event, "reconciliation_record": reconciliation, "provider_status": parsed}

        provider_status = str(parsed.get("status") or "UNKNOWN").upper()
        if provider_status == "SUCCESSFUL":
            try:
                confirmation = self.confirm_payment(
                    actor={"id": actor_user_id or 0, "role": "admin"},
                    payment_intent_id=int(intent["id"]),
                    body={
                        "payment_attempt_id": int(attempt["id"]) if attempt is not None else None,
                        "provider_reference": provider_reference,
                        "amount_minor": amount_minor or expected_amount,
                        "currency": currency or expected_currency,
                        "provider_event_id": int(provider_event["id"]),
                        "proof": {"webhook": parsed, "provider_event_id": provider_event_id},
                        "metadata": {"webhook": parsed, "provider_event_id": provider_event_id},
                    },
                )
            except PaymentAlreadyProcessed:
                confirmation = {
                    "payment_intent": self.repository.get_payment_intent(int(intent["id"])),
                    "payment_transaction": self.repository.list_payment_transactions(payment_intent_id=int(intent["id"]), limit=1)[0] if self.repository.list_payment_transactions(payment_intent_id=int(intent["id"]), limit=1) else None,
                    "invoice": self.repository.get_invoice(int(intent.get("parent_id"))) if intent.get("parent_id") else None,
                }
            confirmation["provider_event"] = provider_event
            confirmation["provider_status"] = parsed
            return confirmation

        if provider_status in {"FAILED", "CANCELLED"}:
            failure = self.fail_payment(
                actor={"id": actor_user_id or 0, "role": "admin"},
                payment_intent_id=int(intent["id"]),
                body={
                    "error_code": provider_status.lower(),
                    "error_message": str(parsed.get("raw") or ""),
                    "provider_reference": provider_reference,
                },
            )
            failure["provider_event"] = provider_event
            failure["provider_status"] = parsed
            return failure

        if provider_status == "EXPIRED":
            expiry = self.expire_payment(actor={"id": actor_user_id or 0, "role": "admin"}, payment_intent_id=int(intent["id"]))
            expiry["provider_event"] = provider_event
            expiry["provider_status"] = parsed
            return expiry

        self.repository.update_payment_intent(
            int(intent["id"]),
            status="PROCESSING" if provider_status == "PROCESSING" else "PENDING",
            payload={
                "status": "PROCESSING" if provider_status == "PROCESSING" else "PENDING",
                "provider_reference": provider_reference or intent_payload.get("provider_reference"),
                "last_webhook": parsed,
            },
        )
        if attempt is not None:
            self.repository.update_payment_attempt(
                int(attempt["id"]),
                status="PROCESSING" if provider_status == "PROCESSING" else "PENDING",
                payload={**(attempt.get("payload") or {}), "provider_status": parsed, "provider_reference": provider_reference},
            )
        return {
            "payment_intent": self.repository.get_payment_intent(int(intent["id"])),
            "provider_event": provider_event,
            "provider_status": parsed,
        }

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
