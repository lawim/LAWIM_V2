from lawim_runtime.domains.verification import VerificationHandler, VerificationRuntime
from lawim_runtime.domains.verification.models import VerificationStatus
from lawim_runtime.domains.verification.events import VerificationEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-ver",
    )
    return runtime.execute(req)


def test_verification_start():
    runtime = VerificationRuntime()
    result = _execute(runtime, "START_VERIFICATION", {"project_id": "proj-001"})
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == VerificationStatus.IN_PROGRESS.value
    assert result.output["verification_id"] != ""
    assert result.output["project_id"] == "proj-001"


def test_verification_run_check():
    runtime = VerificationRuntime()
    start_result = _execute(runtime, "START_VERIFICATION", {"project_id": "proj-001"})
    ver_id = start_result.output["verification_id"]

    check_result = _execute(runtime, "RUN_VERIFICATION_CHECK", {
        "verification_id": ver_id,
        "check_type": "identity",
    })
    assert check_result.status == DomainRuntimeStatus.SUCCEEDED
    assert check_result.output["status"] == "PASSED"
    assert check_result.output["check_id"] != ""
    assert check_result.output["verification_id"] == ver_id
    assert check_result.output["check_type"] == "identity"


def test_verification_complete():
    runtime = VerificationRuntime()
    start = _execute(runtime, "START_VERIFICATION", {"project_id": "proj-001"})
    ver_id = start.output["verification_id"]

    _execute(runtime, "RUN_VERIFICATION_CHECK", {
        "verification_id": ver_id,
        "check_type": "identity",
    })

    complete = _execute(runtime, "COMPLETE_VERIFICATION", {"verification_id": ver_id})
    assert complete.output["status"] == VerificationStatus.VERIFIED.value
    assert complete.output["total_checks"] >= 1
    assert complete.output["passed"] >= 1


def test_verification_escalate():
    runtime = VerificationRuntime()
    start = _execute(runtime, "START_VERIFICATION", {"project_id": "proj-001"})
    ver_id = start.output["verification_id"]

    esc = _execute(runtime, "ESCALATE_VERIFICATION", {"verification_id": ver_id})
    assert esc.output["status"] == VerificationStatus.HUMAN_REVIEW_REQUIRED.value
    assert esc.output["verification_id"] == ver_id
