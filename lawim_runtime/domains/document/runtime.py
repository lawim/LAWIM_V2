from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .events import DocumentEvent, DocumentEventType
from .metrics import DocumentMetrics
from .models import DocumentData, DocumentStatus
from .repository import DocumentRepository, InMemoryDocumentRepository


class DocumentRuntime(DomainRuntime):
    runtime_name: str = "document"
    supported_actions: list[str] = [
        "REQUEST_DOCUMENT",
        "REGISTER_DOCUMENT",
        "START_DOCUMENT_ANALYSIS",
        "UPDATE_DOCUMENT_STATUS",
    ]

    def __init__(self, repository: DocumentRepository | None = None) -> None:
        self._repository = repository or InMemoryDocumentRepository()
        self._metrics = DocumentMetrics()

    @property
    def metrics(self) -> DocumentMetrics:
        return self._metrics

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "REQUEST_DOCUMENT":
            return self._execute_request_document(params)
        elif action == "REGISTER_DOCUMENT":
            return self._execute_register_document(params)
        elif action == "START_DOCUMENT_ANALYSIS":
            return self._execute_start_document_analysis(params)
        elif action == "UPDATE_DOCUMENT_STATUS":
            return self._execute_update_document_status(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_request_document(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        document_type = params.get("document_type", "")
        if not project_id or not document_type:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": "project_id and document_type are required",
            }

        doc = DocumentData(
            doc_id=uuid4().hex[:16],
            project_id=project_id,
            document_type=document_type,
            status=DocumentStatus.REQUESTED.value,
        )
        self._repository.save(doc)
        self._metrics.documents_requested += 1
        return {
            "status": DocumentStatus.REQUESTED.value,
            "doc_id": doc.doc_id,
            "project_id": doc.project_id,
            "document_type": doc.document_type,
        }

    def _execute_register_document(self, params: dict[str, Any]) -> dict[str, Any]:
        project_id = params.get("project_id", "")
        document_type = params.get("document_type", "")
        file_reference = params.get("file_reference", "")
        if not project_id or not document_type or not file_reference:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": "project_id, document_type, and file_reference are required",
            }

        doc = DocumentData(
            doc_id=uuid4().hex[:16],
            project_id=project_id,
            document_type=document_type,
            file_reference=file_reference,
            status=DocumentStatus.REGISTERED.value,
        )
        self._repository.save(doc)
        self._metrics.documents_registered += 1
        return {
            "status": DocumentStatus.REGISTERED.value,
            "doc_id": doc.doc_id,
            "project_id": doc.project_id,
            "file_reference": doc.file_reference,
        }

    def _execute_start_document_analysis(self, params: dict[str, Any]) -> dict[str, Any]:
        doc_id = params.get("doc_id", "")
        if not doc_id:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": "doc_id is required",
            }

        doc = self._repository.get(doc_id)
        if not doc:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": f"document not found: {doc_id}",
            }

        doc.status = DocumentStatus.PENDING_ANALYSIS.value
        doc.updated_at = datetime.now(timezone.utc).isoformat()
        self._repository.save(doc)
        self._metrics.documents_analyzed += 1
        return {
            "status": DocumentStatus.PENDING_ANALYSIS.value,
            "doc_id": doc.doc_id,
            "project_id": doc.project_id,
        }

    def _execute_update_document_status(self, params: dict[str, Any]) -> dict[str, Any]:
        doc_id = params.get("doc_id", "")
        new_status = params.get("status", "")
        if not doc_id or not new_status:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": "doc_id and status are required",
            }

        try:
            DocumentStatus(new_status)
        except ValueError:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": f"invalid document status: {new_status}",
            }

        doc = self._repository.get(doc_id)
        if not doc:
            return {
                "status": DocumentStatus.FAILED.value,
                "error": f"document not found: {doc_id}",
            }

        doc.status = new_status
        doc.updated_at = datetime.now(timezone.utc).isoformat()
        self._repository.save(doc)

        if new_status == DocumentStatus.HUMAN_REVIEW_REQUIRED.value:
            self._metrics.documents_review_required += 1

        return {
            "status": new_status,
            "doc_id": doc.doc_id,
            "project_id": doc.project_id,
        }

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action == "REQUEST_DOCUMENT":
            if not params.get("project_id"):
                errors.append("project_id is required")
            if not params.get("document_type"):
                errors.append("document_type is required")
        elif action == "REGISTER_DOCUMENT":
            if not params.get("project_id"):
                errors.append("project_id is required")
            if not params.get("document_type"):
                errors.append("document_type is required")
            if not params.get("file_reference"):
                errors.append("file_reference is required")
        elif action == "START_DOCUMENT_ANALYSIS":
            if not params.get("doc_id"):
                errors.append("doc_id is required")
        elif action == "UPDATE_DOCUMENT_STATUS":
            if not params.get("doc_id"):
                errors.append("doc_id is required")
            if not params.get("status"):
                errors.append("status is required")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        status = output.get("status")
        if status == DocumentStatus.FAILED.value:
            return "error" in output
        if status in (
            DocumentStatus.REQUESTED.value,
            DocumentStatus.REGISTERED.value,
            DocumentStatus.PENDING_ANALYSIS.value,
        ):
            return "doc_id" in output and "project_id" in output
        return "doc_id" in output
