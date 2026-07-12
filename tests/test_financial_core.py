from __future__ import annotations

from dataclasses import replace
import hmac
import json
import os
import sqlite3
import tempfile
import unittest
import uuid
from http import HTTPStatus
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

from lawim_v2.errors import ValidationError
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.persistence_adapter import resolve_persistence_adapter
from lawim_v2.financial.engines import FINANCIAL_ENGINE
from lawim_v2.financial.exceptions import (
    CommissionAlreadyPaid,
    InvoiceAlreadyPaid,
    PaymentAlreadyProcessed,
    RefundAmountExceeded,
    SubscriptionAlreadyRenewed,
)
from lawim_v2.financial.providers.campay import CampayProviderAdapter
from lawim_v2.services import LawimServices

from tests.lawim_harness import LawimTestHarness


def _table_names(repository) -> set[str]:
    return {row["name"] for row in repository.all("SELECT name FROM sqlite_master WHERE type='table'")}


class FinancialCoreSchemaTests(LawimTestHarness):
    def test_financial_tables_are_present_and_campay_is_seeded(self) -> None:
        names = _table_names(self.repository)
        expected_tables = {
            "financial_products",
            "financial_pricing_rules",
            "financial_quotes",
            "financial_quote_lines",
            "financial_invoices",
            "financial_invoice_lines",
            "financial_credit_notes",
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
        }
        for table in expected_tables:
            self.assertIn(table, names)
        providers = self.repository.list_payment_providers()
        self.assertEqual(len(providers), 1)
        self.assertEqual(str((providers[0].get("payload") or {}).get("provider_code")), "CAMPAY")


class FinancialCoreFlowTests(LawimTestHarness):
    def test_quote_invoice_payment_receipt_cycle(self) -> None:
        self.repository.create_financial_product(
            code="LAWIM-SVC-001",
            name="Mission 14 Service",
            description="Financial core validation service",
            category="service",
            unit="item",
            default_price_minor=1_500,
            currency="XAF",
            tax_rate_bps=0,
        )
        quote = self.repository.create_quote(
            actor_user_id=1,
            customer_user_id=1,
            organization_id=None,
            lines=[{"description": "Mission 14 Service", "quantity": 1, "unit_price_minor": 1_500}],
            currency="XAF",
            idempotency_key="quote-flow-001",
        )
        invoice = self.repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=int(quote["id"]),
            organization_id=None,
            lines=[{"description": "Mission 14 Service", "quantity": 1, "unit_price_minor": 1_500}],
            currency="XAF",
            idempotency_key="invoice-flow-001",
        )
        invoice = self.repository.issue_invoice(int(invoice["id"]))
        intent = self.repository.create_payment_intent(
            actor_user_id=1,
            customer_user_id=1,
            invoice_id=int(invoice["id"]),
            amount_minor=1_500,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237 677 000 111",
            idempotency_key="intent-flow-001",
        )
        self.assertEqual(intent["payload"]["phone_number_e164"], "+237677000111")
        attempt = self.repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 1_500},
            provider_reference="campay-flow-001",
            idempotency_key="attempt-flow-001",
        )
        result = self.repository.confirm_payment_intent(
            payment_intent_id=int(intent["id"]),
            payment_attempt_id=int(attempt["id"]),
            provider_reference="campay-flow-001",
            amount_minor=1_500,
            currency="XAF",
            actor_user_id=1,
        )
        self.assertEqual(result["payment_intent"]["status"], "SUCCEEDED")
        self.assertEqual(result["payment_transaction"]["status"], "SUCCESSFUL")
        self.assertEqual(result["invoice"]["status"], "PAID")
        self.assertEqual(result["receipt"]["status"], "GENERATED")
        dashboard = self.repository.financial_dashboard()
        self.assertEqual(dashboard["readiness"]["score"], 100.0)
        self.assertEqual(dashboard["summary"]["invoices"], 1)
        self.assertEqual(dashboard["summary"]["receipts"], 1)

    def test_payment_attempt_idempotency_reuses_existing_attempt(self) -> None:
        invoice = self.repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=None,
            organization_id=None,
            lines=[{"description": "Retryable payment", "quantity": 1, "unit_price_minor": 900}],
            currency="XAF",
            idempotency_key="invoice-idem-001",
        )
        invoice = self.repository.issue_invoice(int(invoice["id"]))
        intent = self.repository.create_payment_intent(
            actor_user_id=1,
            customer_user_id=1,
            invoice_id=int(invoice["id"]),
            amount_minor=900,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237677000111",
            idempotency_key="intent-idem-001",
        )
        attempt_1 = self.repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 900},
            provider_reference="campay-idem-001",
            idempotency_key="attempt-idem-001",
        )
        attempt_2 = self.repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 900},
            provider_reference="campay-idem-001",
            idempotency_key="attempt-idem-001",
        )
        self.assertEqual(attempt_1["id"], attempt_2["id"])
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM financial_payment_attempts"), 1)
        intent_snapshot = self.repository.get_payment_intent(int(intent["id"]))
        self.assertEqual(int(intent_snapshot["payload"]["attempt_count"]), 1)

    def test_mobile_money_number_normalization_and_rejection(self) -> None:
        self.assertEqual(FINANCIAL_ENGINE.normalize_mobile_money_number(" +237 677 000 111 "), "+237677000111")
        with self.assertRaises(ValidationError):
            FINANCIAL_ENGINE.normalize_mobile_money_number("12345")


class FinancialCoreApiTests(LawimTestHarness):
    def test_financial_dashboard_and_readiness_endpoints_work_for_admin(self) -> None:
        token = self.login(email="admin@lawim.local")
        dashboard = self.invoke("/api/v2/financial/dashboard", token=token)
        readiness = self.invoke("/api/v2/financial/readiness", token=token)
        self.assertEqual(dashboard.status, HTTPStatus.OK, msg=dashboard.body_text())
        self.assertEqual(readiness.status, HTTPStatus.OK, msg=readiness.body_text())
        self.assertIn("summary", dashboard.body_json())
        self.assertIn("readiness", dashboard.body_json())
        self.assertIn("score", readiness.body_json())

    def test_foreign_invoice_cannot_be_paid_by_another_user(self) -> None:
        invoice = self.repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=None,
            organization_id=None,
            lines=[{"description": "Private invoice", "quantity": 1, "unit_price_minor": 2_000}],
            currency="XAF",
            idempotency_key="invoice-foreign-001",
        )
        invoice = self.repository.issue_invoice(int(invoice["id"]))
        agent_token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/financial/payments/intents",
            method="POST",
            token=agent_token,
            body={
                "invoice_id": int(invoice["id"]),
                "amount_minor": 2_000,
                "currency": "XAF",
                "provider_code": "CAMPAY",
                "phone_number_e164": "+237677000111",
                "idempotency_key": "foreign-payment-001",
            },
        )
        self.assertEqual(response.status, HTTPStatus.FORBIDDEN, msg=response.body_text())

    def test_agent_only_sees_own_payment_attempts(self) -> None:
        agent_row = self.repository.one("SELECT id FROM users WHERE email = ?", ("agent@lawim.local",))
        self.assertIsNotNone(agent_row)
        agent_id = int(agent_row["id"])

        admin_invoice = self.repository.issue_invoice(
            int(
                self.repository.create_invoice(
                    actor_user_id=1,
                    customer_user_id=1,
                    quote_id=None,
                    organization_id=None,
                    lines=[{"description": "Admin-owned", "quantity": 1, "unit_price_minor": 1_000}],
                    currency="XAF",
                    idempotency_key="admin-owned-invoice",
                )["id"]
            )
        )
        admin_intent = self.repository.create_payment_intent(
            actor_user_id=1,
            customer_user_id=1,
            invoice_id=int(admin_invoice["id"]),
            amount_minor=1_000,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237677000111",
            idempotency_key="admin-intent-001",
        )
        self.repository.create_payment_attempt(
            payment_intent_id=int(admin_intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 1_000},
            provider_reference="campay-admin-001",
            idempotency_key="campay-admin-001",
        )

        agent_invoice = self.repository.issue_invoice(
            int(
                self.repository.create_invoice(
                    actor_user_id=1,
                    customer_user_id=agent_id,
                    quote_id=None,
                    organization_id=None,
                    lines=[{"description": "Agent-owned", "quantity": 1, "unit_price_minor": 1_100}],
                    currency="XAF",
                    idempotency_key="agent-owned-invoice",
                )["id"]
            )
        )
        agent_intent = self.repository.create_payment_intent(
            actor_user_id=agent_id,
            customer_user_id=agent_id,
            invoice_id=int(agent_invoice["id"]),
            amount_minor=1_100,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237677000111",
            idempotency_key="agent-intent-001",
        )
        self.repository.create_payment_attempt(
            payment_intent_id=int(agent_intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 1_100},
            provider_reference="campay-agent-001",
            idempotency_key="campay-agent-001",
        )

        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/financial/payments/attempts", token=token)
        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        body = response.body_json()
        attempts = body["payment_attempts"]
        self.assertEqual(len(attempts), 1)
        self.assertEqual(int(attempts[0]["parent_id"]), int(agent_intent["id"]))


class FinancialCoreCampayScaffoldTests(LawimTestHarness):
    def test_campay_adapter_is_disabled_by_default_and_masks_webhook_validation(self) -> None:
        adapter = CampayProviderAdapter(self.config)
        health = adapter.health_check().to_dict()
        self.assertEqual(health["code"], "CAMPAY")
        self.assertFalse(health["available"])
        self.assertFalse(adapter.validate_webhook(headers={}, payload=b"{}"))
        auth = adapter.authenticate()
        self.assertFalse(auth["ok"])
        self.assertEqual(auth["status"], "FAILED")
        self.assertEqual(auth["error_code"], "campay_error")


class FinancialCoreCampayBehaviorTests(LawimTestHarness):
    def test_campay_authentication_caches_token_and_creates_payments(self) -> None:
        config = replace(
            self.config,
            campay_enabled=True,
            campay_app_username="campay-user",
            campay_app_password="campay-pass",
            campay_webhook_secret="campay-webhook-secret",
        )
        adapter = CampayProviderAdapter(config)

        with patch.object(
            CampayProviderAdapter,
            "_request_json",
            side_effect=[
                {"ok": True, "payload": {"token": "campay-token-1", "expires_in": 3600}},
                {"ok": True, "payload": {"reference": "campay-ref-001", "status": "PENDING"}},
            ],
        ) as request_json:
            auth_1 = adapter.authenticate()
            auth_2 = adapter.authenticate()
            payment = adapter.create_payment(
                payload={
                    "amount_minor": 2_500,
                    "currency": "XAF",
                    "phone_number_e164": "+237677000111",
                    "description": "LAWIM validation",
                    "external_reference": "LAWIM-INTENT-001",
                }
            )

        self.assertTrue(auth_1["ok"])
        self.assertTrue(auth_2["ok"])
        self.assertEqual(request_json.call_count, 2)
        self.assertEqual(payment["status"], "PENDING")
        self.assertEqual(payment["provider_reference"], "campay-ref-001")

    @patch.object(
        CampayProviderAdapter,
        "create_payment",
        return_value={
            "ok": True,
            "provider": "CAMPAY",
            "provider_name": "Campay",
            "status": "PENDING",
            "provider_reference": "campay-service-001",
            "available": True,
            "response": {"reference": "campay-service-001", "status": "PENDING"},
        },
    )
    def test_service_initiates_campay_payment_intent(self, create_payment: object) -> None:
        config = replace(
            self.config,
            campay_enabled=True,
            campay_app_username="campay-user",
            campay_app_password="campay-pass",
            campay_webhook_secret="campay-webhook-secret",
        )
        services = LawimServices(self.repository, config)

        invoice = self.repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=None,
            organization_id=None,
            lines=[{"description": "Campay initiated invoice", "quantity": 1, "unit_price_minor": 2_500}],
            currency="XAF",
            idempotency_key="campay-service-invoice",
        )
        invoice = self.repository.issue_invoice(int(invoice["id"]))

        result = services.financial.create_payment_intent(
            actor={"id": 1, "role": "admin"},
            body={
                "invoice_id": int(invoice["id"]),
                "amount_minor": 2_500,
                "currency": "XAF",
                "provider_code": "CAMPAY",
                "channel": "mobile_money",
                "phone_number_e164": "+237677000111",
                "initiate": True,
                "idempotency_key": "campay-service-intent",
            },
        )

        self.assertEqual(create_payment.call_count, 1)
        self.assertEqual(result["payment_intent"]["status"], "PENDING")
        self.assertEqual(result["payment_attempt"]["provider_reference"], "campay-service-001")
        self.assertTrue(result["provider_available"])

    def test_campay_webhook_confirms_payment_and_is_idempotent(self) -> None:
        config = replace(
            self.config,
            campay_enabled=True,
            campay_webhook_secret="campay-webhook-secret",
        )
        services = LawimServices(self.repository, config)
        adapter = CampayProviderAdapter(config)

        invoice = self.repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=None,
            organization_id=None,
            lines=[{"description": "Campay webhook invoice", "quantity": 1, "unit_price_minor": 2_500}],
            currency="XAF",
            idempotency_key="campay-webhook-invoice",
        )
        invoice = self.repository.issue_invoice(int(invoice["id"]))
        intent = self.repository.create_payment_intent(
            actor_user_id=1,
            customer_user_id=1,
            invoice_id=int(invoice["id"]),
            amount_minor=2_500,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237677000111",
            idempotency_key="campay-webhook-intent",
        )
        self.repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 2_500, "currency": "XAF"},
            provider_reference="campay-webhook-001",
            idempotency_key="campay-webhook-attempt",
        )

        payload = json.dumps(
            {
                "event_id": "event-campay-001",
                "reference": "campay-webhook-001",
                "status": "SUCCESSFUL",
                "amount_minor": 2_500,
                "currency": "XAF",
                "event_type": "payment.successful",
                "idempotency_key": "event-campay-001",
                "correlation_id": "corr-campay-001",
            }
        ).encode("utf-8")
        signature = hmac.new(b"campay-webhook-secret", payload, sha256).hexdigest()
        headers = {"X-LAWIM-WEBHOOK-SIGNATURE": signature}

        self.assertTrue(adapter.validate_webhook(headers=headers, payload=payload))
        parsed = adapter.parse_webhook(payload=payload)
        self.assertTrue(parsed["ok"])
        self.assertEqual(parsed["provider_reference"], "campay-webhook-001")

        first = services.financial.process_campay_webhook(raw_body=payload, headers=headers, actor_user_id=1)
        second = services.financial.process_campay_webhook(raw_body=payload, headers=headers, actor_user_id=1)

        self.assertIn("payment_intent", first)
        self.assertEqual(first["payment_intent"]["status"], "SUCCEEDED")
        self.assertEqual(first["invoice"]["status"], "PAID")
        self.assertEqual(first["payment_transaction"]["status"], "SUCCESSFUL")
        self.assertEqual(first["provider_status"]["status"], "SUCCESSFUL")
        self.assertEqual(second["payment_intent"]["status"], "SUCCEEDED")
        self.assertEqual(len(self.repository.list_payment_transactions(payment_intent_id=int(intent["id"]))), 1)
        self.assertEqual(len(self.repository.list_receipts(invoice_id=int(invoice["id"]))), 1)

    def test_auto_initiated_payment_requires_mobile_money_number(self) -> None:
        config = replace(
            self.config,
            campay_enabled=True,
            campay_app_username="campay-user",
            campay_app_password="campay-pass",
        )
        services = LawimServices(self.repository, config)
        invoice = self.repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=None,
            organization_id=None,
            lines=[{"description": "Missing phone", "quantity": 1, "unit_price_minor": 1_500}],
            currency="XAF",
            idempotency_key="campay-phone-invoice",
        )
        invoice = self.repository.issue_invoice(int(invoice["id"]))

        with self.assertRaises(ValidationError):
            services.financial.create_payment_intent(
                actor={"id": 1, "role": "admin"},
                body={
                    "invoice_id": int(invoice["id"]),
                    "amount_minor": 1_500,
                    "currency": "XAF",
                    "provider_code": "CAMPAY",
                    "initiate": True,
                    "idempotency_key": "campay-phone-intent",
                },
            )


class PostgreSQLFinancialCoreIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dsn = os.getenv("LAWIM_TEST_POSTGRES_URL", "").strip()
        if not cls.dsn:
            raise unittest.SkipTest("LAWIM_TEST_POSTGRES_URL not set — PostgreSQL financial integration skipped")
        try:
            import pg8000  # noqa: F401
        except ImportError as exc:
            raise unittest.SkipTest("pg8000 not installed — pip install -r requirements-postgresql.txt") from exc

    def _create_repository(self):
        tempdir = tempfile.TemporaryDirectory(prefix="lawim-financial-postgres-")
        self.addCleanup(tempdir.cleanup)
        adapter = resolve_persistence_adapter(
            Path(tempdir.name) / "fallback.sqlite3",
            db_driver="postgresql",
            database_url=self.dsn,
            allow_sqlite_fallback=False,
        )
        repository = adapter.create_repository()
        self.addCleanup(repository.close)
        return repository

    def test_postgresql_financial_core_migrations_idempotence_and_constraints(self) -> None:
        repository = self._create_repository()
        run_token = uuid.uuid4().hex[:8]

        repository.initialize(seed_demo_data=True)
        repository.initialize(seed_demo_data=True)

        self.assertEqual(repository.driver, "postgresql")
        self.assertEqual(repository.schema_version(), APPLICATION_SCHEMA_VERSION)

        version_row = repository.one("SELECT version() AS version, current_database() AS database_name, current_user AS username, now() AS now")
        self.assertIsNotNone(version_row)
        self.assertIn("PostgreSQL 16.14", str(version_row["version"]))
        self.assertEqual(version_row["database_name"], "lawim_v2")
        self.assertEqual(version_row["username"], "lawim")

        table_rows = repository.all(
            """
            SELECT table_name AS name
            FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name LIKE 'financial_%'
            """
        )
        table_names = {str(row["name"]) for row in table_rows}
        expected_tables = {
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
        }
        self.assertTrue(expected_tables.issubset(table_names))
        self.assertEqual(len(repository.list_payment_providers()), 1)

        product = repository.create_financial_product(
            code=f"LAWIM-SVC-PG-{run_token}",
            name="PostgreSQL Validation Service",
            description="Real PostgreSQL financial core validation",
            category="service",
            unit="item",
            default_price_minor=2_500,
            currency="XAF",
            tax_rate_bps=0,
        )
        repository.create_pricing_rule(
            product_id=int(product["id"]),
            code=f"LAWIM-PRICING-PG-{run_token}",
            name="Base pricing rule",
            amount_minor=2_500,
            status="active",
        )
        quote = repository.create_quote(
            actor_user_id=1,
            customer_user_id=1,
            organization_id=None,
            lines=[{"description": "PostgreSQL Validation Service", "quantity": 1, "unit_price_minor": 2_500}],
            currency="XAF",
            idempotency_key=f"pg-quote-{run_token}",
        )
        invoice = repository.create_invoice(
            actor_user_id=1,
            customer_user_id=1,
            quote_id=int(quote["id"]),
            organization_id=None,
            lines=[{"description": "PostgreSQL Validation Service", "quantity": 1, "unit_price_minor": 2_500}],
            currency="XAF",
            idempotency_key=f"pg-invoice-{run_token}",
        )
        invoice = repository.issue_invoice(int(invoice["id"]))
        intent = repository.create_payment_intent(
            actor_user_id=1,
            customer_user_id=1,
            invoice_id=int(invoice["id"]),
            amount_minor=2_500,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237 677 000 111",
            idempotency_key=f"pg-payment-intent-{run_token}",
        )
        intent_dup = repository.create_payment_intent(
            actor_user_id=1,
            customer_user_id=1,
            invoice_id=int(invoice["id"]),
            amount_minor=2_500,
            currency="XAF",
            provider_code="CAMPAY",
            phone_number_e164="+237677000111",
            idempotency_key=f"pg-payment-intent-{run_token}",
        )
        self.assertEqual(int(intent["id"]), int(intent_dup["id"]))
        self.assertEqual(intent_dup["payload"]["phone_number_e164"], "+237677000111")

        attempt = repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 2_500, "currency": "XAF"},
            provider_reference=f"pg-campay-{run_token}",
            idempotency_key=f"pg-attempt-{run_token}",
        )
        attempt_dup = repository.create_payment_attempt(
            payment_intent_id=int(intent["id"]),
            provider_code="CAMPAY",
            request_json={"amount_minor": 2_500, "currency": "XAF"},
            provider_reference=f"pg-campay-{run_token}",
            idempotency_key=f"pg-attempt-{run_token}",
        )
        self.assertEqual(int(attempt["id"]), int(attempt_dup["id"]))

        confirmation = repository.confirm_payment_intent(
            payment_intent_id=int(intent["id"]),
            payment_attempt_id=int(attempt["id"]),
            provider_reference=f"pg-campay-{run_token}",
            amount_minor=2_500,
            currency="XAF",
            actor_user_id=1,
        )
        self.assertEqual(confirmation["payment_intent"]["status"], "SUCCEEDED")
        self.assertEqual(confirmation["payment_transaction"]["status"], "SUCCESSFUL")
        self.assertEqual(confirmation["invoice"]["status"], "PAID")
        self.assertEqual(confirmation["receipt"]["status"], "GENERATED")
        self.assertEqual(repository.list_receipts(invoice_id=int(invoice["id"]))[0]["status"], "GENERATED")
        with self.assertRaises(PaymentAlreadyProcessed):
            repository.confirm_payment_intent(
                payment_intent_id=int(intent["id"]),
                payment_attempt_id=int(attempt["id"]),
                provider_reference=f"pg-campay-{run_token}",
                amount_minor=2_500,
                currency="XAF",
                actor_user_id=1,
            )

        with self.assertRaises(RefundAmountExceeded):
            repository.request_refund(
                payment_transaction_id=int(confirmation["payment_transaction"]["id"]),
                invoice_id=int(invoice["id"]),
                amount_minor=2_501,
                reason="excess refund",
                requested_by_user_id=1,
            )

        refund = repository.request_refund(
            payment_transaction_id=int(confirmation["payment_transaction"]["id"]),
            invoice_id=int(invoice["id"]),
            amount_minor=500,
            reason="partial refund",
            requested_by_user_id=1,
        )
        refund = repository.approve_refund(int(refund["id"]), actor_user_id=1)
        refund = repository.process_refund(int(refund["id"]), provider_reference=f"pg-refund-{run_token}", actor_user_id=1)
        self.assertEqual(refund["status"], "SUCCEEDED")

        ledger_entry = repository.record_ledger_entry(
            debit_account_id=int(repository.list_ledger_accounts()[2]["id"]),
            credit_account_id=int(repository.list_ledger_accounts()[0]["id"]),
            source_type="payment",
            source_id=int(confirmation["payment_transaction"]["id"]),
            amount_minor=2_500,
            currency="XAF",
            transaction_id=int(confirmation["payment_transaction"]["id"]),
            description="Successful payment journal entry",
            actor_user_id=1,
        )
        self.assertEqual(ledger_entry["status"], "POSTED")
        self.assertEqual(repository.list_ledger_entries(transaction_id=int(confirmation["payment_transaction"]["id"]))[0]["status"], "POSTED")

        subscription_plan = repository.create_subscription_plan(
            code="LAWIM-PLAN-PG-001",
            name="PostgreSQL Monthly Plan",
            description="Integration test plan",
            price_minor=3_000,
            currency="XAF",
            frequency="MONTHLY",
            status="ACTIVE",
        )
        subscription = repository.create_subscription(
            plan_id=int(subscription_plan["id"]),
            actor_user_id=1,
            customer_user_id=1,
            organization_id=None,
            renewal_mode="automatic",
            status="ACTIVE",
        )
        renewal = repository.renew_subscription(
            int(subscription["id"]),
            actor_user_id=1,
            period_start="2026-07-01T00:00:00+00:00",
            period_end="2026-08-01T00:00:00+00:00",
            amount_minor=3_000,
            currency="XAF",
            due_at="2026-07-01T00:00:00+00:00",
        )
        self.assertEqual(renewal["subscription"]["status"], "ACTIVE")
        with self.assertRaises(SubscriptionAlreadyRenewed):
            repository.renew_subscription(
                int(subscription["id"]),
                actor_user_id=1,
                period_start="2026-08-01T00:00:00+00:00",
                period_end="2026-09-01T00:00:00+00:00",
                amount_minor=3_000,
                currency="XAF",
                due_at="2026-08-01T00:00:00+00:00",
            )

        commission_rule = repository.create_commission_rule(
            code="LAWIM-COMMISSION-PG-001",
            name="PostgreSQL commission rule",
            rate_bps=1_500,
            minimum_minor=100,
            status="ACTIVE",
        )
        commission = repository.calculate_commission(
            rule_id=int(commission_rule["id"]),
            source_object_type="payment",
            source_object_id=int(confirmation["payment_transaction"]["id"]),
            gross_amount_minor=2_500,
            currency="XAF",
            beneficiary_user_id=1,
            actor_user_id=1,
        )
        commission = repository.validate_commission(int(commission["id"]), actor_user_id=1)
        commission = repository.mark_commission_payable(int(commission["id"]), actor_user_id=1)
        commission = repository.pay_commission(
            int(commission["id"]),
            provider_code="MANUAL",
            provider_reference="pg-commission-001",
            actor_user_id=1,
        )
        self.assertEqual(commission["status"], "PAID")
        with self.assertRaises(CommissionAlreadyPaid):
            repository.pay_commission(
                int(commission["id"]),
                provider_code="MANUAL",
                provider_reference="pg-commission-001",
                actor_user_id=1,
            )

        reconciliation = repository.create_reconciliation_record(
            provider_code="CAMPAY",
            payment_intent_id=int(intent["id"]),
            payment_attempt_id=int(attempt["id"]),
            payment_transaction_id=int(confirmation["payment_transaction"]["id"]),
            invoice_id=int(invoice["id"]),
            receipt_id=int(confirmation["receipt"]["id"]),
            internal_amount_minor=2_500,
            provider_amount_minor=2_500,
            currency="XAF",
            conflict_type="amount_mismatch",
            status="CONFLICT",
        )
        reconciliation = repository.resolve_reconciliation(
            int(reconciliation["id"]),
            status="RESOLVED",
            resolution_note="Validated against PostgreSQL",
            resolved_by_user_id=1,
        )
        self.assertEqual(reconciliation["status"], "RESOLVED")

        duplicate_record_key = product["record_key"]
        with self.assertRaises(sqlite3.IntegrityError):
            with repository._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO financial_products (
                        record_key, name, kind, scope, status, payload_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        duplicate_record_key,
                        "Duplicate product",
                        "financial_product",
                        "service",
                        "active",
                        "{}",
                        "2026-07-12T00:00:00+00:00",
                        "2026-07-12T00:00:00+00:00",
                    ),
                )

        rollback_record_key = f"ledger-entry-rollback-pg-{run_token}"
        with self.assertRaises(RuntimeError):
            with repository._transaction() as conn:
                conn.execute(
                    """
                    INSERT INTO financial_ledger_entries (
                        record_key, name, kind, scope, status, payload_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        rollback_record_key,
                        "Rollback entry",
                        "ledger_entry",
                        "payment",
                        "posted",
                        "{}",
                        "2026-07-12T00:00:00+00:00",
                        "2026-07-12T00:00:00+00:00",
                    ),
                )
                raise RuntimeError("force rollback")
        self.assertEqual(
            int(repository.scalar("SELECT COUNT(*) FROM financial_ledger_entries WHERE record_key = ?", (rollback_record_key,)) or 0),
            0,
        )

        reopened = self._create_repository()
        reopened.initialize(seed_demo_data=True)
        self.assertEqual(reopened.schema_version(), APPLICATION_SCHEMA_VERSION)
        self.assertEqual(reopened.get_invoice(int(invoice["id"]))["status"], "PAID")
        self.assertEqual(reopened.get_receipt(int(confirmation["receipt"]["id"]))["status"], "GENERATED")
        self.assertEqual(reopened.get_payment_transaction(int(confirmation["payment_transaction"]["id"]))["status"], "SUCCESSFUL")
