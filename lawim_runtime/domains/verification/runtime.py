from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .events import VerificationEvent, VerificationEventType
from .metrics import VerificationMetrics
from .models import CheckStatus, VerificationCheck, VerificationData, VerificationStatus
from .repository import InMemoryVerificationRepository, VerificationRepository


class VerificationRuntime(DomainRuntime):
    runtime_name: str = "verification"
    supported_actions: list[str] = [
        "START_VERIFICATION",
        "RUN_VERIFICATION_CHECK",
        "COMPLETE_VERIFICATION",
        "ESCALATE_VERIFICATION",
    ]

    def __init__(self, repository: VerificationRepository | None = None) -> None:
        self._repository = repository or InMemoryVerificationRepository()
        self._metrics = VerificationMetrics()

    @property
    def metrics(self) -> VerificationMetrics:
        return self._metrics

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "START_VERIFICATION":
            return self._execute_start_verification(params)
        elif action == "RUN_VERIFICATION_CHECK":
            return self._execute_run_verification_check(params)
        elif action == "COMPLETE_VERIFICATION":
            return self._execute_complete_verification(params)
        elif action == "ESCALATE_VERIFICATION":
            return self._execute_escalate_verification(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_start_verification(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        if not project_id:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": "project_id is required",
            }

        verification = VerificationData(
            verification_id=uuid4().hex[:16],
            project_id=project_id,
            global_status=VerificationStatus.IN_PROGRESS.value,
            started_at=datetime.now(timezone.utc).isoformat(),
        )
        self._repository.save(verification)
        self._metrics.verifications_started += 1
        return {
            "status": VerificationStatus.IN_PROGRESS.value,
            "verification_id": verification.verification_id,
            "project_id": verification.project_id,
        }

    def _execute_run_verification_check(self, params: dict[str, Any]) -> dict[str, Any]:
        verification_id = params.get("verification_id", "")
        check_type = params.get("check_type", "")
        if not verification_id or not check_type:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": "verification_id and check_type are required",
            }

        verification = self._repository.get(verification_id)
        if not verification:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": f"verification not found: {verification_id}",
            }

        check = VerificationCheck(
            check_id=uuid4().hex[:16],
            check_type=check_type,
            status=CheckStatus.PASSED.value,
            verified_by="system",
            verified_at=datetime.now(timezone.utc).isoformat(),
            result="check simulated",
        )
        verification.checks.append(check)
        self._repository.update_check(verification_id, check)

        if verification.global_status == VerificationStatus.NOT_STARTED.value:
            verification.global_status = VerificationStatus.IN_PROGRESS.value

        self._metrics.verifications_passed += 1
        return {
            "status": check.status,
            "check_id": check.check_id,
            "check_type": check.check_type,
            "verification_id": verification_id,
            "project_id": verification.project_id,
        }

    def _execute_complete_verification(self, params: dict[str, Any]) -> dict[str, Any]:
        verification_id = params.get("verification_id", "")
        if not verification_id:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": "verification_id is required",
            }

        verification = self._repository.get(verification_id)
        if not verification:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": f"verification not found: {verification_id}",
            }

        total = len(verification.checks)
        passed = sum(1 for c in verification.checks if c.status == CheckStatus.PASSED.value)
        failed = sum(1 for c in verification.checks if c.status == CheckStatus.FAILED.value)

        if failed > 0:
            verification.global_status = VerificationStatus.FAILED.value
            self._metrics.verifications_failed += 1
        elif passed == total and total > 0:
            verification.global_status = VerificationStatus.VERIFIED.value
            self._metrics.verifications_completed += 1
        elif passed > 0:
            verification.global_status = VerificationStatus.PARTIALLY_VERIFIED.value
            self._metrics.verifications_completed += 1
        else:
            verification.global_status = VerificationStatus.INCONCLUSIVE.value
            self._metrics.verifications_failed += 1

        verification.completed_at = datetime.now(timezone.utc).isoformat()
        self._repository.save(verification)

        return {
            "status": verification.global_status,
            "verification_id": verification.verification_id,
            "project_id": verification.project_id,
            "total_checks": total,
            "passed": passed,
            "failed": failed,
        }

    def _execute_escalate_verification(self, params: dict[str, Any]) -> dict[str, Any]:
        verification_id = params.get("verification_id", "")
        if not verification_id:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": "verification_id is required",
            }

        verification = self._repository.get(verification_id)
        if not verification:
            return {
                "status": VerificationStatus.FAILED.value,
                "error": f"verification not found: {verification_id}",
            }

        verification.global_status = VerificationStatus.HUMAN_REVIEW_REQUIRED.value
        self._repository.save(verification)
        self._metrics.verifications_escalated += 1

        return {
            "status": VerificationStatus.HUMAN_REVIEW_REQUIRED.value,
            "verification_id": verification.verification_id,
            "project_id": verification.project_id,
        }

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action == "START_VERIFICATION":
            if not params.get("project_id"):
                errors.append("project_id is required")
        elif action == "RUN_VERIFICATION_CHECK":
            if not params.get("verification_id"):
                errors.append("verification_id is required")
            if not params.get("check_type"):
                errors.append("check_type is required")
        elif action in ("COMPLETE_VERIFICATION", "ESCALATE_VERIFICATION"):
            if not params.get("verification_id"):
                errors.append("verification_id is required")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        status = output.get("status")
        if status == VerificationStatus.FAILED.value:
            return "error" in output
        if status in (
            VerificationStatus.IN_PROGRESS.value,
            VerificationStatus.VERIFIED.value,
            VerificationStatus.PARTIALLY_VERIFIED.value,
            VerificationStatus.HUMAN_REVIEW_REQUIRED.value,
        ):
            return "verification_id" in output and "project_id" in output
        if status == CheckStatus.PASSED.value:
            return "check_id" in output and "verification_id" in output
        return "verification_id" in output
