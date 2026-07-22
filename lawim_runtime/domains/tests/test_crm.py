from lawim_runtime.domains.crm import CRMHandler, CRMRuntime
from lawim_runtime.domains.crm.models import CRMStatus
from lawim_runtime.domains.crm.events import CRMEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-crm",
    )
    return runtime.execute(req)


def test_crm_create_lead():
    runtime = CRMRuntime()
    result = _execute(runtime, "CREATE_OR_UPDATE_LEAD", {
        "project_id": "proj-001",
        "contact_name": "Alice",
        "contact_phone": "+237600000000",
        "contact_email": "alice@test.com",
        "source": "whatsapp",
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == CRMStatus.LEAD_CREATED.value
    assert result.output["lead_id"] != ""
    assert result.output["project_id"] == "proj-001"
    assert result.output["is_new"] is True


def test_crm_update_lead():
    runtime = CRMRuntime()
    _execute(runtime, "CREATE_OR_UPDATE_LEAD", {
        "project_id": "proj-001",
        "contact_name": "Alice",
        "source": "whatsapp",
    })
    result = _execute(runtime, "CREATE_OR_UPDATE_LEAD", {
        "project_id": "proj-001",
        "contact_name": "Alice Updated",
        "contact_phone": "+237600000001",
    })
    assert result.output["status"] == CRMStatus.LEAD_UPDATED.value
    assert result.output["is_new"] is False


def test_crm_create_handover():
    runtime = CRMRuntime()
    result = _execute(runtime, "ESCALATE_TO_HUMAN", {
        "project_id": "proj-001",
        "reason": "client request",
        "target_team": "legal",
    })
    assert result.output["status"] == CRMStatus.HANDOVER_CREATED.value
    assert result.output["handover_id"] != ""
    assert result.output["project_id"] == "proj-001"


def test_crm_duplicate_detection():
    runtime = CRMRuntime()
    r1 = _execute(runtime, "CREATE_OR_UPDATE_LEAD", {
        "project_id": "proj-002",
        "contact_name": "Bob",
    })
    assert r1.output["status"] == CRMStatus.LEAD_CREATED.value

    r2 = _execute(runtime, "CREATE_OR_UPDATE_LEAD", {
        "project_id": "proj-002",
        "contact_name": "Bob Updated",
    })
    assert r2.output["status"] == CRMStatus.LEAD_UPDATED.value
    assert r2.output["is_new"] is False


def test_crm_event_produced():
    assert CRMEventType.CRM_LEAD_CREATED.value == "CRM_LEAD_CREATED"
    assert CRMEventType.CRM_LEAD_UPDATED.value == "CRM_LEAD_UPDATED"
    assert CRMEventType.CRM_HANDOVER_CREATED.value == "CRM_HANDOVER_CREATED"
    assert CRMEventType.CRM_HANDOVER_RESOLVED.value == "CRM_HANDOVER_RESOLVED"
    assert CRMEventType.CRM_CASE_CLOSED.value == "CRM_CASE_CLOSED"
    assert len(CRMEventType) == 7
