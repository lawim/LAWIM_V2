from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .events import TransactionEvent, TransactionEventType
from .metrics import TransactionMetrics
from .models import NegotiationEntry, TransactionData, TransactionStatus
from .repository import InMemoryTransactionRepository, TransactionRepository


class TransactionRuntime(DomainRuntime):
    runtime_name: str = "transaction"
    supported_actions: list[str] = [
        "PREPARE_TRANSACTION",
        "START_NEGOTIATION",
        "UPDATE_NEGOTIATION",
        "CONFIRM_TRANSACTION",
        "CANCEL_TRANSACTION",
        "CLOSE_PROJECT",
    ]

    def __init__(self, repository: TransactionRepository | None = None) -> None:
        self._repository = repository or InMemoryTransactionRepository()
        self._metrics = TransactionMetrics()

    @property
    def metrics(self) -> TransactionMetrics:
        return self._metrics

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "PREPARE_TRANSACTION":
            return self._execute_prepare_transaction(params)
        elif action == "START_NEGOTIATION":
            return self._execute_start_negotiation(params)
        elif action == "UPDATE_NEGOTIATION":
            return self._execute_update_negotiation(params)
        elif action == "CONFIRM_TRANSACTION":
            return self._execute_confirm_transaction(params)
        elif action == "CANCEL_TRANSACTION":
            return self._execute_cancel_transaction(params)
        elif action == "CLOSE_PROJECT":
            return self._execute_close_project(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_prepare_transaction(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {"status": TransactionStatus.FAILED.value, "error": "project_id is required"}

        transaction = TransactionData(
            transaction_id=uuid4().hex[:16],
            project_id=project_id,
            property_id=params.get("property_id", ""),
            buyer_id=params.get("buyer_id", ""),
            seller_id=params.get("seller_id", ""),
            amount=params.get("amount", 0.0),
            currency=params.get("currency", "XAF"),
            stage="prepared",
            status=TransactionStatus.PREPARED,
            terms=params.get("terms", {}),
        )
        self._repository.save(transaction)
        self._metrics.transactions_prepared += 1
        return {
            "status": TransactionStatus.PREPARED.value,
            "transaction_id": transaction.transaction_id,
            "project_id": transaction.project_id,
        }

    def _execute_start_negotiation(self, params: dict[str, Any]) -> dict[str, Any]:
        transaction_id = params.get("transaction_id", "")
        transaction = self._repository.get(transaction_id)
        if not transaction:
            return {"status": TransactionStatus.FAILED.value, "error": "transaction not found"}

        entry = NegotiationEntry(
            entry_id=uuid4().hex[:16],
            party=params.get("party", ""),
            offer_amount=params.get("offer_amount", transaction.amount),
            terms=params.get("terms", {}),
            status="proposed",
        )
        self._repository.add_negotiation_entry(transaction_id, entry)
        transaction.status = TransactionStatus.NEGOTIATING
        transaction.stage = "negotiating"
        self._repository.save(transaction)
        self._metrics.negotiations_started += 1
        return {
            "status": TransactionStatus.NEGOTIATING.value,
            "transaction_id": transaction_id,
            "entry_id": entry.entry_id,
            "project_id": transaction.project_id,
        }

    def _execute_update_negotiation(self, params: dict[str, Any]) -> dict[str, Any]:
        transaction_id = params.get("transaction_id", "")
        transaction = self._repository.get(transaction_id)
        if not transaction:
            return {"status": TransactionStatus.FAILED.value, "error": "transaction not found"}

        entry = NegotiationEntry(
            entry_id=uuid4().hex[:16],
            party=params.get("party", ""),
            offer_amount=params.get("offer_amount", transaction.amount),
            terms=params.get("terms", {}),
            status=params.get("entry_status", "updated"),
        )
        self._repository.add_negotiation_entry(transaction_id, entry)
        return {
            "status": TransactionStatus.NEGOTIATING.value,
            "transaction_id": transaction_id,
            "entry_id": entry.entry_id,
            "project_id": transaction.project_id,
        }

    def _execute_confirm_transaction(self, params: dict[str, Any]) -> dict[str, Any]:
        transaction_id = params.get("transaction_id", "")
        transaction = self._repository.get(transaction_id)
        if not transaction:
            return {"status": TransactionStatus.FAILED.value, "error": "transaction not found"}

        preconditions = self._check_preconditions(transaction)
        if preconditions:
            transaction.status = TransactionStatus.PRECONDITIONS_CHECKING
            self._repository.save(transaction)
            return {
                "status": TransactionStatus.PRECONDITIONS_CHECKING.value,
                "transaction_id": transaction_id,
                "project_id": transaction.project_id,
                "preconditions": preconditions,
            }

        transaction.status = TransactionStatus.CONFIRMED
        transaction.stage = "confirmed"
        self._repository.save(transaction)
        self._metrics.transactions_confirmed += 1
        return {
            "status": TransactionStatus.CONFIRMED.value,
            "transaction_id": transaction_id,
            "project_id": transaction.project_id,
        }

    def _execute_cancel_transaction(self, params: dict[str, Any]) -> dict[str, Any]:
        transaction_id = params.get("transaction_id", "")
        transaction = self._repository.get(transaction_id)
        if not transaction:
            return {"status": TransactionStatus.FAILED.value, "error": "transaction not found"}

        transaction.status = TransactionStatus.CANCELLED
        transaction.stage = "cancelled"
        self._repository.save(transaction)
        self._metrics.transactions_cancelled += 1
        return {
            "status": TransactionStatus.CANCELLED.value,
            "transaction_id": transaction_id,
            "project_id": transaction.project_id,
        }

    def _execute_close_project(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {"status": TransactionStatus.FAILED.value, "error": "project_id is required"}

        transactions = self._repository.list_by_project(project_id)
        completed = 0
        for t in transactions:
            if t.status == TransactionStatus.CONFIRMED:
                t.status = TransactionStatus.COMPLETED
                t.stage = "completed"
                self._repository.save(t)
                completed += 1

        self._metrics.transactions_completed += completed
        return {
            "status": TransactionStatus.COMPLETED.value,
            "project_id": project_id,
            "completed_count": completed,
        }

    def _check_preconditions(self, transaction: TransactionData) -> list[str]:
        preconditions: list[str] = []
        if not transaction.buyer_id:
            preconditions.append("buyer_id is required")
        if not transaction.seller_id:
            preconditions.append("seller_id is required")
        if not transaction.property_id:
            preconditions.append("property_id is required")
        if transaction.amount <= 0:
            preconditions.append("amount must be positive")
        return preconditions

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action == "PREPARE_TRANSACTION":
            if not params.get("project_id"):
                errors.append("project_id is required")
        elif action in ("START_NEGOTIATION", "UPDATE_NEGOTIATION", "CONFIRM_TRANSACTION", "CANCEL_TRANSACTION"):
            if not params.get("transaction_id"):
                errors.append("transaction_id is required")
        elif action == "CLOSE_PROJECT":
            if not params.get("project_id"):
                errors.append("project_id is required")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        status = output.get("status")
        if status == TransactionStatus.FAILED.value:
            return "error" in output
        if status in (
            TransactionStatus.PREPARED.value,
            TransactionStatus.NEGOTIATING.value,
            TransactionStatus.CONFIRMED.value,
            TransactionStatus.CANCELLED.value,
            TransactionStatus.COMPLETED.value,
            TransactionStatus.SIMULATED.value,
        ):
            return "project_id" in output
        return False
