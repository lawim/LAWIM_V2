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


def _create_visit(runtime):
    return _execute(runtime, "CREATE_VISIT_REQUEST", {
        "property_id": "prop-001",
        "requester_name": "John Doe",
        "requester_contact": "john@test.com",
    })


def test_visit_create():
    runtime = VisitRuntime()
    result = _create_visit(runtime)
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == VisitStatus.PENDING.value
    assert result.output["visit_id"] != ""
    assert result.output["property_id"] == "prop-001"


def _schedule_visit(runtime, visit_id, date="2026-07-25T10:00"):
    return _execute(runtime, "SCHEDULE_VISIT", {
        "visit_id": visit_id,
        "scheduled_date": date,
        "property_id": "prop-001",
    })


def _cancel_visit(runtime, visit_id):
    return _execute(runtime, "CANCEL_VISIT", {"visit_id": visit_id})


def test_visit_full_lifecycle():
    runtime = VisitRuntime()

    create = _create_visit(runtime)
    visit_id = create.output["visit_id"]

    schedule = _schedule_visit(runtime, visit_id)
    assert schedule.output["status"] == VisitStatus.SCHEDULED.value

    confirm = _execute(runtime, "CONFIRM_VISIT", {"visit_id": visit_id})
    assert confirm.output["status"] == VisitStatus.CONFIRMED.value

    complete = _execute(runtime, "COMPLETE_VISIT", {"visit_id": visit_id})
    assert complete.output["status"] == VisitStatus.COMPLETED.value


def test_visit_cancel():
    runtime = VisitRuntime()
    create = _create_visit(runtime)
    visit_id = create.output["visit_id"]

    cancel = _cancel_visit(runtime, visit_id)
    assert cancel.output["status"] == VisitStatus.CANCELLED.value

    cancel_again = _cancel_visit(runtime, visit_id)
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


def test_visit_state_transition_scheduled_to_cancelled():
    runtime = VisitRuntime()
    create = _create_visit(runtime)
    visit_id = create.output["visit_id"]

    _schedule_visit(runtime, visit_id)
    cancel = _cancel_visit(runtime, visit_id)
    assert cancel.output["status"] == VisitStatus.CANCELLED.value


def test_visit_state_transition_invalid():
    runtime = VisitRuntime()
    create = _create_visit(runtime)
    visit_id = create.output["visit_id"]

    _schedule_visit(runtime, visit_id)
    _execute(runtime, "CONFIRM_VISIT", {"visit_id": visit_id})
    _execute(runtime, "COMPLETE_VISIT", {"visit_id": visit_id})

    cancel_after_complete = _cancel_visit(runtime, visit_id)
    assert cancel_after_complete.output["status"] == VisitStatus.FAILED.value

    schedule_after_complete = _execute(runtime, "SCHEDULE_VISIT", {
        "visit_id": visit_id,
        "scheduled_date": "2026-07-26",
        "property_id": "prop-001",
    })
    assert schedule_after_complete.output["status"] == VisitStatus.FAILED.value


def test_visit_no_show_transition():
    runtime = VisitRuntime()
    create = _create_visit(runtime)
    visit_id = create.output["visit_id"]

    _schedule_visit(runtime, visit_id)
    no_show = _execute(runtime, "NO_SHOW_VISIT", {"visit_id": visit_id})
    assert no_show.output["status"] == VisitStatus.NO_SHOW.value

    cancel_after_no_show = _cancel_visit(runtime, visit_id)
    assert cancel_after_no_show.output["status"] == VisitStatus.FAILED.value


def test_visit_event_produced():
    assert VisitEventType.VISIT_CREATED.value == "VISIT_CREATED"
    assert VisitEventType.VISIT_CANCELLED.value == "VISIT_CANCELLED"
    assert VisitEventType.VISIT_REQUESTED.value == "VISIT_REQUESTED"
    assert VisitEventType.VISIT_SCHEDULED.value == "VISIT_SCHEDULED"
    assert VisitEventType.VISIT_COMPLETED.value == "VISIT_COMPLETED"
    assert VisitEventType.VISIT_FAILED.value == "VISIT_FAILED"
    assert len(VisitEventType) == 9
