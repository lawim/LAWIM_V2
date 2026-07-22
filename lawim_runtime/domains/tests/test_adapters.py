from lawim_runtime.domains.adapters import (
    V2MatchingAdapter,
    V2PaymentAdapter,
    V2VisitAdapter,
    V2CRMAdapter,
    V2NotificationAdapter,
    V2DocumentAdapter,
    V2VerificationAdapter,
    V2TransactionAdapter,
)
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


def test_matching_adapter_transform():
    adapter = V2MatchingAdapter()
    v2_payload = {
        "request_id": "req-001",
        "action_code": "START_MATCHING",
        "data": {
            "property_type": "apartment",
            "bedrooms": 2,
            "min_budget": 100000,
            "max_budget": 200000,
            "city": "Douala",
            "district": "Bonamoussadi",
            "features": ["pool"],
            "criteria": {"furnished": True},
        },
        "correlation_id": "corr-1",
        "idempotency_key": "idem-1",
        "metadata": {"source": "test"},
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.request_id == "req-001"
    assert req.action_code == "START_MATCHING"
    assert req.parameters["property_type"] == "apartment"
    assert req.parameters["bedrooms"] == 2
    assert req.parameters["min_budget"] == 100000.0
    assert req.parameters["max_budget"] == 200000.0
    assert req.parameters["city"] == "Douala"
    assert req.parameters["district"] == "Bonamoussadi"
    assert req.parameters["features"] == ["pool"]
    assert req.parameters["criteria"] == {"furnished": True}
    assert req.correlation_id == "corr-1"
    assert req.idempotency_key == "idem-1"

    domain_result = DomainRuntimeResult(
        request_id="req-001",
        action_code="START_MATCHING",
        status=DomainRuntimeStatus.SUCCEEDED,
        output={"matches": []},
    )
    mapped = adapter.from_domain_result(domain_result)
    assert mapped["request_id"] == "req-001"
    assert mapped["action_code"] == "START_MATCHING"
    assert mapped["status"] == "SUCCEEDED"
    assert mapped["output"] == {"matches": []}


def test_payment_adapter_transform():
    adapter = V2PaymentAdapter()
    v2_payload = {
        "request_id": "pay-001",
        "action_code": "CREATE_PAYMENT_INTENT",
        "project_id": "proj-001",
        "data": {
            "amount": 50000000,
            "currency": "XAF",
        },
        "correlation_id": "corr-pay",
        "idempotency_key": "idem-pay",
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.request_id == "pay-001"
    assert req.action_code == "CREATE_PAYMENT_INTENT"
    assert req.parameters["project_id"] == "proj-001"
    assert req.parameters["amount"] == 50000000
    assert req.parameters["currency"] == "XAF"

    domain_result = DomainRuntimeResult(
        request_id="pay-001",
        action_code="CREATE_PAYMENT_INTENT",
        status=DomainRuntimeStatus.SUCCEEDED,
        output={"intent_id": "int-001"},
    )
    mapped = adapter.from_domain_result(domain_result)
    assert mapped["status"] == "SUCCEEDED"
    assert mapped["output"]["intent_id"] == "int-001"


def test_divergence_recording():
    adapter = V2MatchingAdapter()
    v2_result = {"status": "MATCH_FOUND", "matches": [{"property_id": "p1"}]}
    v3_result = {
        "status": {"status": "NO_MATCH"},
        "output": {"matches": []},
    }

    adapter.record_divergence(v2_result, v3_result)

    no_divergence_v3 = {"status": "MATCH_FOUND", "output": {"matches": [{"property_id": "p1"}]}}
    adapter.record_divergence(v2_result, no_divergence_v3)


def test_visit_adapter_transform():
    adapter = V2VisitAdapter()
    v2_payload = {
        "request_id": "vis-001",
        "action_code": "CREATE_VISIT_REQUEST",
        "data": {
            "property_id": "prop-001",
            "requester_name": "John",
            "requester_contact": "+237600000",
            "preferred_dates": ["2026-07-25"],
            "preferred_times": ["10:00"],
            "visit_type": "physical",
            "notes": "afternoon preferred",
        },
        "correlation_id": "corr-vis",
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.action_code == "CREATE_VISIT_REQUEST"
    assert req.parameters["property_id"] == "prop-001"
    assert req.parameters["requester_name"] == "John"
    assert req.parameters["visit_type"] == "physical"


def test_crm_adapter_transform():
    adapter = V2CRMAdapter()
    v2_payload = {
        "request_id": "crm-001",
        "action_code": "CREATE_OR_UPDATE_LEAD",
        "project_id": "proj-001",
        "data": {
            "contact_name": "Alice",
            "contact_phone": "+237600000",
            "source": "whatsapp",
        },
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.parameters["project_id"] == "proj-001"
    assert req.parameters["contact_name"] == "Alice"
    assert req.parameters["source"] == "whatsapp"


def test_notification_adapter_transform():
    adapter = V2NotificationAdapter()
    v2_payload = {
        "request_id": "not-001",
        "action_code": "PREPARE_NOTIFICATION",
        "data": {
            "project_id": "proj-001",
            "template_name": "confirmation",
            "recipient_type": "buyer",
            "channel": "whatsapp",
            "parameters": {"date": "2026-07-25"},
            "priority": 1,
        },
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.parameters["project_id"] == "proj-001"
    assert req.parameters["template_name"] == "confirmation"
    assert req.parameters["channel"] == "whatsapp"


def test_document_adapter_transform():
    adapter = V2DocumentAdapter()
    v2_payload = {
        "request_id": "doc-001",
        "action_code": "REQUEST_DOCUMENT",
        "project_id": "proj-001",
        "document_type": "id_card",
        "metadata": {"notes": "urgent"},
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.parameters["project_id"] == "proj-001"
    assert req.parameters["document_type"] == "id_card"


def test_verification_adapter_transform():
    adapter = V2VerificationAdapter()
    v2_payload = {
        "request_id": "ver-001",
        "action_code": "START_VERIFICATION",
        "project_id": "proj-001",
        "metadata": {"priority": "high"},
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.parameters["project_id"] == "proj-001"


def test_transaction_adapter_transform():
    adapter = V2TransactionAdapter()
    v2_payload = {
        "request_id": "txn-001",
        "action_code": "PREPARE_TRANSACTION",
        "project_id": "proj-001",
        "data": {
            "property_id": "prop-001",
            "amount": 50000000,
        },
    }
    req = adapter.to_domain_request(v2_payload)
    assert req.parameters["project_id"] == "proj-001"
    assert req.parameters["property_id"] == "prop-001"
    assert req.parameters["amount"] == 50000000
