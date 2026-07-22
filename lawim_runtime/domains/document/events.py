from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.events import DomainEvent


class DocumentEventType(str, Enum):
    DOCUMENT_REQUESTED = "DOCUMENT_REQUESTED"
    DOCUMENT_REGISTERED = "DOCUMENT_REGISTERED"
    DOCUMENT_ANALYSIS_STARTED = "DOCUMENT_ANALYSIS_STARTED"
    DOCUMENT_STATUS_CHANGED = "DOCUMENT_STATUS_CHANGED"
    DOCUMENT_ANALYSIS_REQUIRED = "DOCUMENT_ANALYSIS_REQUIRED"
    DOCUMENT_HUMAN_REVIEW_REQUIRED = "DOCUMENT_HUMAN_REVIEW_REQUIRED"


@dataclass(frozen=True)
class DocumentEvent:
    event_type: DocumentEventType = DocumentEventType.DOCUMENT_REQUESTED
    doc_id: str = ""
    project_id: str = ""
    previous_status: str = ""
    new_status: str = ""
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_event(self, runtime_name: str = "document", correlation_id: str = "") -> DomainEvent:
        return DomainEvent(
            event_type=self.event_type.value,
            runtime_name=runtime_name,
            data={
                "doc_id": self.doc_id,
                "project_id": self.project_id,
                "previous_status": self.previous_status,
                "new_status": self.new_status,
                "error": self.error,
                **self.metadata,
            },
            correlation_id=correlation_id,
        )
