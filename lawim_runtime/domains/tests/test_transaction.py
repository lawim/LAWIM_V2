from lawim_runtime.domains.transaction import TransactionHandler, TransactionRuntime
from lawim_runtime.domains.transaction.models import TransactionStatus
from lawim_runtime.domains.transaction.events import TransactionEventType
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _execute(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-txn",
    )
    return runtime.execute(req)


def test_transaction_prepare():
    runtime = TransactionRuntime()
    result = _execute(runtime, "PREPARE_TRANSACTION", {
        "project_id": "proj-001",
        "property_id": "prop-001",
        "buyer_id": "buyer-001",
        "seller_id": "seller-001",
        "amount": 50000000,
    })
    assert result.status == DomainRuntimeStatus.SUCCEEDED
    assert result.output["status"] == TransactionStatus.PREPARED.value
    assert result.output["transaction_id"] != ""
    assert result.output["project_id"] == "proj-001"


def test_transaction_negotiation():
    runtime = TransactionRuntime()
    prep = _execute(runtime, "PREPARE_TRANSACTION", {
        "project_id": "proj-001",
        "property_id": "prop-001",
        "buyer_id": "buyer-001",
        "seller_id": "seller-001",
        "amount": 50000000,
    })
    txn_id = prep.output["transaction_id"]

    neg = _execute(runtime, "START_NEGOTIATION", {
        "transaction_id": txn_id,
        "party": "buyer",
        "offer_amount": 45000000,
    })
    assert neg.output["status"] == TransactionStatus.NEGOTIATING.value
    assert neg.output["entry_id"] != ""
    assert neg.output["transaction_id"] == txn_id


def test_transaction_confirm():
    runtime = TransactionRuntime()
    prep = _execute(runtime, "PREPARE_TRANSACTION", {
        "project_id": "proj-001",
        "property_id": "prop-001",
        "buyer_id": "buyer-001",
        "seller_id": "seller-001",
        "amount": 50000000,
    })
    txn_id = prep.output["transaction_id"]

    confirm = _execute(runtime, "CONFIRM_TRANSACTION", {"transaction_id": txn_id})
    assert confirm.output["status"] == TransactionStatus.CONFIRMED.value
    assert confirm.output["transaction_id"] == txn_id


def test_transaction_cancel():
    runtime = TransactionRuntime()
    prep = _execute(runtime, "PREPARE_TRANSACTION", {
        "project_id": "proj-001",
        "property_id": "prop-001",
        "buyer_id": "buyer-001",
        "seller_id": "seller-001",
        "amount": 50000000,
    })
    txn_id = prep.output["transaction_id"]

    cancel = _execute(runtime, "CANCEL_TRANSACTION", {"transaction_id": txn_id})
    assert cancel.output["status"] == TransactionStatus.CANCELLED.value
    assert cancel.output["transaction_id"] == txn_id
