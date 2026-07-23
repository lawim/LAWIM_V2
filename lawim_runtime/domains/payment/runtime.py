from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .events import PaymentEvent, PaymentEventType
from .metrics import PaymentMetrics
from .models import PaymentData, PaymentIntent, PaymentStatus
from .repository import InMemoryPaymentRepository, PaymentRepository


class PaymentRuntime(DomainRuntime):
    runtime_name: str = "payment"
    supported_actions: list[str] = [
        "CREATE_PAYMENT_INTENT",
        "REQUEST_PAYMENT",
        "VERIFY_PAYMENT",
        "RECONCILE_PAYMENT",
        "CANCEL_PAYMENT",
        "REFUND_PAYMENT",
    ]

    def __init__(self, repository: PaymentRepository | None = None) -> None:
        self._repository = repository or InMemoryPaymentRepository()
        self._metrics = PaymentMetrics()

    @property
    def metrics(self) -> PaymentMetrics:
        return self._metrics

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "CREATE_PAYMENT_INTENT":
            return self._execute_create_payment_intent(params)
        elif action == "REQUEST_PAYMENT":
            return self._execute_request_payment(params)
        elif action == "VERIFY_PAYMENT":
            return self._execute_verify_payment(params)
        elif action == "RECONCILE_PAYMENT":
            return self._execute_reconcile_payment(params)
        elif action == "CANCEL_PAYMENT":
            return self._execute_cancel_payment(params)
        elif action == "REFUND_PAYMENT":
            return self._execute_refund_payment(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_create_payment_intent(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {"status": PaymentStatus.FAILED.value, "error": "project_id is required"}

        idempotency_key = params.get("idempotency_key", "")
        if idempotency_key:
            existing = self._repository.get_by_idempotency(idempotency_key)
            if existing:
                return {
                    "status": existing.status.value,
                    "payment_id": existing.payment_id,
                    "intent_id": "",
                    "project_id": existing.project_id,
                    "replayed": True,
                }

        intent = PaymentIntent(
            intent_id=uuid4().hex[:16],
            project_id=project_id,
            amount=params.get("amount", 0.0),
            currency=params.get("currency", "XAF"),
            idempotency_key=idempotency_key,
            status=PaymentStatus.CREATED,
        )
        self._repository.save_intent(intent)
        self._metrics.intents_created += 1
        return {
            "status": PaymentStatus.CREATED.value,
            "intent_id": intent.intent_id,
            "project_id": intent.project_id,
        }

    def _execute_request_payment(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        intent_id = params.get("intent_id", "")
        if not project_id:
            return {"status": PaymentStatus.FAILED.value, "error": "project_id is required"}
        if not intent_id:
            return {"status": PaymentStatus.FAILED.value, "error": "intent_id is required"}

        idempotency_key = params.get("idempotency_key", "")
        if idempotency_key:
            existing = self._repository.get_by_idempotency(idempotency_key)
            if existing:
                return {
                    "status": existing.status.value,
                    "payment_id": existing.payment_id,
                    "project_id": existing.project_id,
                    "replayed": True,
                }

        intent = self._repository.get_intent(intent_id)
        if not intent:
            return {"status": PaymentStatus.FAILED.value, "error": "intent not found"}

        payment = PaymentData(
            payment_id=uuid4().hex[:16],
            project_id=project_id,
            transaction_id=params.get("transaction_id", intent_id),
            amount=intent.amount,
            currency=intent.currency,
            provider=params.get("provider", ""),
            status=PaymentStatus.PENDING,
            idempotency_key=idempotency_key,
        )
        self._repository.save_payment(payment)
        return {
            "status": PaymentStatus.PENDING.value,
            "payment_id": payment.payment_id,
            "intent_id": intent_id,
            "project_id": project_id,
        }

    def _execute_verify_payment(self, params: dict[str, Any]) -> dict[str, Any]:
        payment_id = params.get("payment_id", "")
        payment = self._repository.get_payment(payment_id)
        if not payment:
            return {"status": PaymentStatus.FAILED.value, "error": "payment not found"}

        provider_status = params.get("provider_status", "SUCCEEDED")
        if provider_status == "SUCCEEDED":
            payment.status = PaymentStatus.SUCCEEDED
            self._metrics.payments_succeeded += 1
        elif provider_status == "FAILED":
            payment.status = PaymentStatus.FAILED
            self._metrics.payments_failed += 1
        elif provider_status == "PENDING":
            payment.status = PaymentStatus.PENDING_EXTERNAL_CONFIRMATION
        else:
            payment.status = PaymentStatus.UNKNOWN
            self._metrics.payments_unknown += 1

        self._repository.save_payment(payment)
        return {
            "status": payment.status.value,
            "payment_id": payment_id,
            "project_id": payment.project_id,
        }

    def _execute_reconcile_payment(self, params: dict[str, Any]) -> dict[str, Any]:
        payment_id = params.get("payment_id", "")
        payment = self._repository.get_payment(payment_id)
        if not payment:
            return {"status": PaymentStatus.FAILED.value, "error": "payment not found"}

        payment.status = PaymentStatus.SUCCEEDED
        self._repository.save_payment(payment)
        self._metrics.payments_reconciled += 1
        return {
            "status": PaymentStatus.SUCCEEDED.value,
            "payment_id": payment_id,
            "project_id": payment.project_id,
        }

    def _execute_cancel_payment(self, params: dict[str, Any]) -> dict[str, Any]:
        payment_id = params.get("payment_id", "")
        payment = self._repository.get_payment(payment_id)
        if not payment:
            return {"status": PaymentStatus.FAILED.value, "error": "payment not found"}

        payment.status = PaymentStatus.CANCELLED
        self._repository.save_payment(payment)
        return {
            "status": PaymentStatus.CANCELLED.value,
            "payment_id": payment_id,
            "project_id": payment.project_id,
        }

    def _execute_refund_payment(self, params: dict[str, Any]) -> dict[str, Any]:
        payment_id = params.get("payment_id", "")
        payment = self._repository.get_payment(payment_id)
        if not payment:
            return {"status": PaymentStatus.FAILED.value, "error": "payment not found"}

        payment.status = PaymentStatus.REFUNDED
        self._repository.save_payment(payment)
        self._metrics.payments_refunded += 1
        return {
            "status": PaymentStatus.REFUNDED.value,
            "payment_id": payment_id,
            "project_id": payment.project_id,
        }

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action == "CREATE_PAYMENT_INTENT":
            if not params.get("project_id"):
                errors.append("project_id is required")
        elif action == "REQUEST_PAYMENT":
            if not params.get("project_id"):
                errors.append("project_id is required")
            if not params.get("intent_id"):
                errors.append("intent_id is required")
        elif action in ("VERIFY_PAYMENT", "RECONCILE_PAYMENT", "CANCEL_PAYMENT", "REFUND_PAYMENT"):
            if not params.get("payment_id"):
                errors.append("payment_id is required")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        status = output.get("status")
        if status == PaymentStatus.FAILED.value:
            return "error" in output
        if status in (
            PaymentStatus.CREATED.value,
            PaymentStatus.PENDING.value,
            PaymentStatus.SUCCEEDED.value,
            PaymentStatus.CANCELLED.value,
            PaymentStatus.REFUNDED.value,
            PaymentStatus.UNKNOWN.value,
            PaymentStatus.PENDING_EXTERNAL_CONFIRMATION.value,
            PaymentStatus.SIMULATED.value,
        ):
            return "project_id" in output
        return False
