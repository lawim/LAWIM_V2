from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


class DocumentStatus(str, Enum):
    REQUESTED = "REQUESTED"
    RECEIVED = "RECEIVED"
    REGISTERED = "REGISTERED"
    PENDING_ANALYSIS = "PENDING_ANALYSIS"
    ANALYSIS_REQUIRED = "ANALYSIS_REQUIRED"
    ANALYZED = "ANALYZED"
    VALID = "VALID"
    INVALID = "INVALID"
    INVALID_FORMAT = "INVALID_FORMAT"
    MISSING = "MISSING"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"
    SIMULATED = "SIMULATED"
    FAILED = "FAILED"


@dataclass
class DocumentData:
    doc_id: str = ""
    project_id: str = ""
    document_type: str = ""
    file_reference: str = ""
    status: str = DocumentStatus.REQUESTED.value
    classification: str = ""
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class DocumentRequest:
    project_id: str = ""
    document_type: str = ""
    action_code: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_request(self) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id="",
            action_code=self.action_code,
            parameters={
                "project_id": self.project_id,
                "document_type": self.document_type,
                **self.metadata,
            },
        )


@dataclass
class DocumentResult:
    document: DocumentData | None = None
    status: DocumentStatus = DocumentStatus.FAILED
    events: list[dict[str, Any]] = field(default_factory=list)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            DocumentStatus.REQUESTED: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.RECEIVED: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.REGISTERED: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.PENDING_ANALYSIS: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.ANALYSIS_REQUIRED: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.ANALYZED: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.VALID: DomainRuntimeStatus.SUCCEEDED,
            DocumentStatus.INVALID: DomainRuntimeStatus.FAILED,
            DocumentStatus.INVALID_FORMAT: DomainRuntimeStatus.FAILED,
            DocumentStatus.MISSING: DomainRuntimeStatus.FAILED,
            DocumentStatus.HUMAN_REVIEW_REQUIRED: DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED,
            DocumentStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
            DocumentStatus.FAILED: DomainRuntimeStatus.FAILED,
        }
        return DomainRuntimeResult(
            request_id="",
            action_code="",
            status=domain_status_map.get(self.status, DomainRuntimeStatus.FAILED),
            output={
                "status": self.status.value,
                "doc_id": self.document.doc_id if self.document else "",
                "project_id": self.document.project_id if self.document else "",
                "document_type": self.document.document_type if self.document else "",
            },
            events=self.events,
        )
