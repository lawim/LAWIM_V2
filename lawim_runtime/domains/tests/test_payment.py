from lawim_runtime.domains.payment import PaymentHandler, PaymentRuntime
from lawim_runtime.domains.payment.models import PaymentStatus
from lawim_runtime.domains.payment.events import PaymentEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-pay",
    )
    return runtime.execute(req)


def test_payment_create_intent():
    runtime = PaymentRuntime()
    result = _execute(runtime, "CREATE_PAYMENT_INTENT", {
        "project_id": "proj-001",
        "amount": 50000000,
        "currency": "XAF",
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == PaymentStatus.CREATED.value
    assert result.output["intent_id"] != ""
    assert result.output["project_id"] == "proj-001"


def test_payment_idempotency_same_key():
    runtime = PaymentRuntime()
    intent = _execute(runtime, "CREATE_PAYMENT_INTENT", {
        "project_id": "proj-001",
        "amount": 50000000,
    })
    intent_id = intent.output["intent_id"]

    r1 = _execute(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-001",
        "intent_id": intent_id,
        "provider": "test_provider",
        "idempotency_key": "idem-pay-req-001",
    })
    assert r1.output["status"] == PaymentStatus.PENDING.value

    r2 = _execute(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-001",
        "intent_id": intent_id,
        "provider": "test_provider",
        "idempotency_key": "idem-pay-req-001",
    })
    assert r2.output.get("replayed") is True


def test_payment_timeout_goes_to_unknown():
    runtime = PaymentRuntime()
    intent = _execute(runtime, "CREATE_PAYMENT_INTENT", {
        "project_id": "proj-001",
        "amount": 100000,
    })
    intent_id = intent.output["intent_id"]

    req = _execute(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-001",
        "intent_id": intent_id,
        "provider": "test_provider",
    })
    payment_id = req.output["payment_id"]

    verify = _execute(runtime, "VERIFY_PAYMENT", {
        "payment_id": payment_id,
        "provider_status": "TIMEOUT",
    })
    assert verify.output["status"] == PaymentStatus.UNKNOWN.value


def test_payment_reconcile():
    runtime = PaymentRuntime()
    intent = _execute(runtime, "CREATE_PAYMENT_INTENT", {
        "project_id": "proj-001",
        "amount": 100000,
    })
    intent_id = intent.output["intent_id"]

    req = _execute(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-001",
        "intent_id": intent_id,
        "provider": "test_provider",
    })
    payment_id = req.output["payment_id"]

    reconcile = _execute(runtime, "RECONCILE_PAYMENT", {"payment_id": payment_id})
    assert reconcile.output["status"] == PaymentStatus.SUCCEEDED.value
    assert reconcile.output["payment_id"] == payment_id


def test_payment_cancel():
    runtime = PaymentRuntime()
    intent = _execute(runtime, "CREATE_PAYMENT_INTENT", {
        "project_id": "proj-001",
        "amount": 100000,
    })
    intent_id = intent.output["intent_id"]

    req = _execute(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-001",
        "intent_id": intent_id,
        "provider": "test_provider",
    })
    payment_id = req.output["payment_id"]

    cancel = _execute(runtime, "CANCEL_PAYMENT", {"payment_id": payment_id})
    assert cancel.output["status"] == PaymentStatus.CANCELLED.value
    assert cancel.output["payment_id"] == payment_id
