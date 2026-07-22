from lawim_runtime.domains.matching import MatchingRuntime
from lawim_runtime.domains.matching.models import MatchingStatus
from lawim_runtime.domains.visit import VisitRuntime
from lawim_runtime.domains.visit.models import VisitStatus
from lawim_runtime.domains.crm import CRMRuntime
from lawim_runtime.domains.crm.models import CRMStatus
from lawim_runtime.domains.notification import NotificationRuntime
from lawim_runtime.domains.notification.models import NotificationStatus
from lawim_runtime.domains.document import DocumentRuntime
from lawim_runtime.domains.document.models import DocumentStatus
from lawim_runtime.domains.verification import VerificationRuntime
from lawim_runtime.domains.verification.models import VerificationStatus
from lawim_runtime.domains.transaction import TransactionRuntime
from lawim_runtime.domains.transaction.models import TransactionStatus
from lawim_runtime.domains.payment import PaymentRuntime
from lawim_runtime.domains.payment.models import PaymentStatus
from lawim_runtime.domains.registration import register_domain_runtimes
from lawim_runtime.domains.config import DomainRuntimeConfig
from lawim_runtime.execution.registry import ActionHandlerRegistry
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeStatus


def _exec(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        request_id="",
        action_code=action_code,
        parameters=params or {},
        correlation_id="test-integration",
    )
    return runtime.execute(req)


def _exec_op(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        request_id="",
        action_code=action_code,
        parameters=params or {},
        correlation_id="test-integration",
    )
    ctx = runtime._build_context(req)
    return runtime.execute_op(req, ctx)


def test_search_and_matching_scenario():
    runtime = MatchingRuntime()
    runtime.load_properties([
        {"property_id": "p1", "property_type": "apartment", "bedrooms": 2, "price": 150000, "city": "Douala", "district": "Bonamoussadi", "features": ["pool", "parking"]},
        {"property_id": "p2", "property_type": "apartment", "bedrooms": 3, "price": 250000, "city": "Douala", "district": "Bonamoussadi", "features": ["pool"]},
        {"property_id": "p3", "property_type": "house", "bedrooms": 4, "price": 400000, "city": "Yaounde", "district": "Mvan", "features": ["garden"]},
    ])

    result1 = _exec_op(runtime, "START_PRELIMINARY_MATCHING", {
        "property_type": "apartment",
        "city": "Douala",
    })
    assert result1["preliminary_count"] == 2
    assert result1["status"] == MatchingStatus.MATCH_FOUND.value

    result2 = _exec_op(runtime, "START_MATCHING", {
        "property_type": "apartment",
        "bedrooms": 2,
        "max_budget": 200000,
        "city": "Douala",
        "features": ["pool"],
    })
    assert result2["status"] == MatchingStatus.MATCH_FOUND.value
    assert result2["total_count"] >= 1
    for match in result2["matches"]:
        assert "property_id" in match
        assert "score" in match

    result3 = _exec_op(runtime, "REFINE_MATCHING", {"features": ["parking"]})
    if result3["status"] == MatchingStatus.MATCH_FOUND.value:
        assert result3["total_count"] >= 0

    result4 = _exec_op(runtime, "PRESENT_MATCHES", {})
    assert result4["status"] in (MatchingStatus.MATCH_FOUND.value, MatchingStatus.NO_MATCH.value)


def test_visit_scenario():
    visit_runtime = VisitRuntime()
    crm_runtime = CRMRuntime()
    notif_runtime = NotificationRuntime()

    visit_result = _exec(visit_runtime, "CREATE_VISIT_REQUEST", {
        "property_id": "prop-001",
        "requester_name": "John Doe",
        "requester_contact": "+237600000000",
        "preferred_dates": ["2026-07-25"],
    })
    assert visit_result.output["status"] == VisitStatus.PENDING.value
    visit_id = visit_result.output["visit_id"]

    crm_result = _exec(crm_runtime, "CREATE_OR_UPDATE_LEAD", {
        "project_id": "proj-visit-001",
        "contact_name": "John Doe",
        "contact_phone": "+237600000000",
        "source": "visit_request",
    })
    assert crm_result.output["status"] in (CRMStatus.LEAD_CREATED.value, CRMStatus.LEAD_UPDATED.value)

    notif_result = _exec(notif_runtime, "PREPARE_NOTIFICATION", {
        "project_id": "proj-visit-001",
        "template_name": "visit_confirmation",
        "recipient_type": "buyer",
        "channel": "whatsapp",
        "parameters": {"visit_id": visit_id},
    })
    assert notif_result.output["status"] == NotificationStatus.PREPARED.value

    cancel_result = _exec(visit_runtime, "CANCEL_VISIT", {"visit_id": visit_id})
    assert cancel_result.output["status"] == VisitStatus.CANCELLED.value


def test_document_verification_scenario():
    doc_runtime = DocumentRuntime()
    ver_runtime = VerificationRuntime()

    doc_result = _exec(doc_runtime, "REQUEST_DOCUMENT", {
        "project_id": "proj-doc-001",
        "document_type": "id_card",
    })
    assert doc_result.output["status"] == DocumentStatus.REQUESTED.value
    doc_id = doc_result.output["doc_id"]

    reg_result = _exec(doc_runtime, "REGISTER_DOCUMENT", {
        "project_id": "proj-doc-001",
        "document_type": "id_card",
        "file_reference": "s3://bucket/id_card.pdf",
    })
    assert reg_result.output["status"] == DocumentStatus.REGISTERED.value
    reg_doc_id = reg_result.output["doc_id"]

    ver_result = _exec(ver_runtime, "START_VERIFICATION", {"project_id": "proj-doc-001"})
    assert ver_result.output["status"] == VerificationStatus.IN_PROGRESS.value
    ver_id = ver_result.output["verification_id"]

    check_result = _exec(ver_runtime, "RUN_VERIFICATION_CHECK", {
        "verification_id": ver_id,
        "check_type": f"document_{reg_doc_id}",
    })
    assert check_result.output["status"] == "PASSED"

    complete_result = _exec(ver_runtime, "COMPLETE_VERIFICATION", {"verification_id": ver_id})
    assert complete_result.output["status"] in (
        VerificationStatus.VERIFIED.value,
        VerificationStatus.PARTIALLY_VERIFIED.value,
    )


def test_transaction_scenario():
    runtime = TransactionRuntime()

    prep_result = _exec(runtime, "PREPARE_TRANSACTION", {
        "project_id": "proj-txn-001",
        "property_id": "prop-001",
        "buyer_id": "buyer-001",
        "seller_id": "seller-001",
        "amount": 50000000,
    })
    assert prep_result.output["status"] == TransactionStatus.PREPARED.value
    txn_id = prep_result.output["transaction_id"]

    neg_result = _exec(runtime, "START_NEGOTIATION", {
        "transaction_id": txn_id,
        "party": "buyer",
        "offer_amount": 45000000,
    })
    assert neg_result.output["status"] == TransactionStatus.NEGOTIATING.value

    confirm_result = _exec(runtime, "CONFIRM_TRANSACTION", {"transaction_id": txn_id})
    assert confirm_result.output["status"] == TransactionStatus.CONFIRMED.value

    close_result = _exec(runtime, "CLOSE_PROJECT", {"project_id": "proj-txn-001"})
    assert close_result.output["status"] == TransactionStatus.COMPLETED.value
    assert close_result.output["completed_count"] >= 1


def test_idempotent_payment_scenario():
    runtime = PaymentRuntime()

    r1 = _exec(runtime, "CREATE_PAYMENT_INTENT", {
        "project_id": "proj-pay-001",
        "amount": 50000000,
    })
    assert r1.output["status"] == PaymentStatus.CREATED.value
    intent_id = r1.output["intent_id"]

    r2 = _exec(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-pay-001",
        "intent_id": intent_id,
        "provider": "test_provider",
        "idempotency_key": "idem-pay-scenario",
    })
    assert r2.output["status"] == PaymentStatus.PENDING.value

    r3 = _exec(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-pay-001",
        "intent_id": intent_id,
        "provider": "test_provider",
        "idempotency_key": "idem-pay-scenario",
    })
    assert r3.output.get("replayed") is True


def test_payment_timeout_scenario():
    runtime = PaymentRuntime()

    r1 = _exec(runtime, "CREATE_PAYMENT_INTENT", {"project_id": "proj-timeout", "amount": 25000})
    intent_id = r1.output["intent_id"]

    r2 = _exec(runtime, "REQUEST_PAYMENT", {
        "project_id": "proj-timeout",
        "intent_id": intent_id,
        "provider": "slow_provider",
    })
    payment_id = r2.output["payment_id"]

    r3 = _exec(runtime, "VERIFY_PAYMENT", {
        "payment_id": payment_id,
        "provider_status": "TIMEOUT",
    })
    assert r3.output["status"] == PaymentStatus.UNKNOWN.value

    r4 = _exec(runtime, "RECONCILE_PAYMENT", {"payment_id": payment_id})
    assert r4.output["status"] == PaymentStatus.SUCCEEDED.value
    assert r4.output["payment_id"] == payment_id


def test_shadow_mode_scenario():
    registry = ActionHandlerRegistry()
    config = DomainRuntimeConfig(shadow_mode=True)
    register_domain_runtimes(registry, config)
    assert registry.count() == 8

    handler = registry.resolve_handler("START_MATCHING")
    result = handler.execute(None)
    assert result["status"] == "SIMULATED"
    assert "shadow mode" in result.get("message", "")

    handler2 = registry.resolve_handler("CREATE_PAYMENT_INTENT")
    result2 = handler2.execute(None)
    assert result2["status"] == "SIMULATED"
    assert "shadow mode" in result2.get("message", "")
