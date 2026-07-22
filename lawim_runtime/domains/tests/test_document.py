from lawim_runtime.domains.document import DocumentHandler, DocumentRuntime
from lawim_runtime.domains.document.models import DocumentStatus
from lawim_runtime.domains.document.events import DocumentEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-doc",
    )
    return runtime.execute(req)


def test_document_request():
    runtime = DocumentRuntime()
    result = _execute(runtime, "REQUEST_DOCUMENT", {
        "project_id": "proj-001",
        "document_type": "id_card",
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == DocumentStatus.REQUESTED.value
    assert result.output["doc_id"] != ""
    assert result.output["project_id"] == "proj-001"
    assert result.output["document_type"] == "id_card"


def test_document_register():
    runtime = DocumentRuntime()
    result = _execute(runtime, "REGISTER_DOCUMENT", {
        "project_id": "proj-001",
        "document_type": "id_card",
        "file_reference": "s3://bucket/id_card.pdf",
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == DocumentStatus.REGISTERED.value
    assert result.output["doc_id"] != ""
    assert result.output["file_reference"] == "s3://bucket/id_card.pdf"


def test_document_status_update():
    runtime = DocumentRuntime()
    req_result = _execute(runtime, "REQUEST_DOCUMENT", {
        "project_id": "proj-001",
        "document_type": "contract",
    })
    doc_id = req_result.output["doc_id"]

    update_result = _execute(runtime, "UPDATE_DOCUMENT_STATUS", {
        "doc_id": doc_id,
        "status": "VALID",
    })
    assert update_result.output["status"] == "VALID"
    assert update_result.output["doc_id"] == doc_id


def test_document_invalid_request():
    runtime = DocumentRuntime()
    req = DomainRuntimeRequest(action_code="UNKNOWN_ACTION")
    errors = runtime.validate(req)
    assert len(errors) > 0
    assert "UNKNOWN_ACTION" in errors[0]
