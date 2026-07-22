from lawim_runtime.domains.visit import VisitHandler, VisitRuntime
from lawim_runtime.domains.visit.models import VisitStatus
from lawim_runtime.domains.visit.events import VisitEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-visit",
    )
    return runtime.execute(req)


def test_visit_create():
    runtime = VisitRuntime()
    result = _execute(runtime, "CREATE_VISIT_REQUEST", {
        "property_id": "prop-001",
        "requester_name": "John Doe",
        "requester_contact": "john@test.com",
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == VisitStatus.PENDING.value
    assert result.output["visit_id"] != ""
    assert result.output["property_id"] == "prop-001"


def test_visit_cancel():
    runtime = VisitRuntime()
    create = _execute(runtime, "CREATE_VISIT_REQUEST", {
        "property_id": "prop-001",
        "requester_name": "John Doe",
        "requester_contact": "john@test.com",
    })
    visit_id = create.output["visit_id"]

    cancel = _execute(runtime, "CANCEL_VISIT", {"visit_id": visit_id})
    assert cancel.output["status"] == VisitStatus.CANCELLED.value

    cancel_again = _execute(runtime, "CANCEL_VISIT", {"visit_id": visit_id})
    assert cancel_again.output["status"] == VisitStatus.FAILED.value


def test_visit_duplicate_detection():
    runtime = VisitRuntime()
    params = {
        "property_id": "prop-001",
        "requester_name": "Jane Doe",
        "requester_contact": "jane@test.com",
    }
    r1 = _execute(runtime, "CREATE_VISIT_REQUEST", params)
    assert r1.output["status"] == VisitStatus.PENDING.value

    r2 = _execute(runtime, "CREATE_VISIT_REQUEST", params)
    assert r2.output["status"] == VisitStatus.FAILED.value
    assert "duplicate" in r2.output.get("error", "").lower()


def test_visit_invalid_request():
    runtime = VisitRuntime()
    req = DomainRuntimeRequest(action_code="UNKNOWN_ACTION")
    errors = runtime.validate(req)
    assert len(errors) > 0
    assert "UNKNOWN_ACTION" in errors[0]


def test_visit_event_produced():
    assert VisitEventType.VISIT_CREATED.value == "VISIT_CREATED"
    assert VisitEventType.VISIT_CANCELLED.value == "VISIT_CANCELLED"
    assert VisitEventType.VISIT_REQUESTED.value == "VISIT_REQUESTED"
    assert VisitEventType.VISIT_SCHEDULED.value == "VISIT_SCHEDULED"
    assert VisitEventType.VISIT_COMPLETED.value == "VISIT_COMPLETED"
    assert VisitEventType.VISIT_FAILED.value == "VISIT_FAILED"
    assert len(VisitEventType) == 9
