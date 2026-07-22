from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class VerificationStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY_VERIFIED"
    FAILED = "FAILED"
    INCONCLUSIVE = "INCONCLUSIVE"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    SIMULATED = "SIMULATED"


class CheckStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass
class VerificationCheck:
    check_id: str = ""
    check_type: str = ""
    status: str = CheckStatus.PENDING.value
    result: str = ""
    verified_by: str = ""
    verified_at: str = ""
    notes: str = ""


@dataclass
class VerificationData:
    verification_id: str = ""
    project_id: str = ""
    checks: list[VerificationCheck] = field(default_factory=list)
    global_status: str = VerificationStatus.NOT_STARTED.value
    started_at: str = ""
    completed_at: str = ""


@dataclass
class VerificationRequest:
    project_id: str = ""
    check_type: str = ""
    action_code: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_request(self) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id="",
            action_code=self.action_code,
            parameters={
                "project_id": self.project_id,
                "check_type": self.check_type,
                **self.metadata,
            },
        )


@dataclass
class VerificationResult:
    verification: VerificationData | None = None
    status: VerificationStatus = VerificationStatus.NOT_STARTED
    events: list[dict[str, Any]] = field(default_factory=list)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            VerificationStatus.NOT_STARTED: DomainRuntimeStatus.PENDING,
            VerificationStatus.IN_PROGRESS: DomainRuntimeStatus.RUNNING,
            VerificationStatus.VERIFIED: DomainRuntimeStatus.SUCCEEDED,
            VerificationStatus.PARTIALLY_VERIFIED: DomainRuntimeStatus.SUCCEEDED,
            VerificationStatus.FAILED: DomainRuntimeStatus.FAILED,
            VerificationStatus.INCONCLUSIVE: DomainRuntimeStatus.FAILED,
            VerificationStatus.HUMAN_REVIEW_REQUIRED: DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED,
            VerificationStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
        }
        return DomainRuntimeResult(
            request_id="",
            action_code="",
            status=domain_status_map.get(self.status, DomainRuntimeStatus.FAILED),
            output={
                "status": self.status.value,
                "verification_id": self.verification.verification_id if self.verification else "",
                "project_id": self.verification.project_id if self.verification else "",
                "global_status": self.verification.global_status if self.verification else "",
            },
            events=self.events,
        )
