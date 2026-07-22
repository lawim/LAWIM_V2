from lawim_runtime.domains.matching import MatchingHandler, MatchingRuntime
from lawim_runtime.domains.matching.policy import MATCHING_POLICY
from lawim_runtime.domains.matching.events import MatchingEventType
from lawim_runtime.domains.matching.metrics import MatchingMetrics
from lawim_runtime.domains.matching.models import (
    MatchingRequestData,
    MatchingRequest,
    MatchingResult,
    MatchingResultItem,
    MatchingStatus,
)
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


def _execute_op(runtime, action_code, params=None):
    req = DomainRuntimeRequest(
        action_code=action_code,
        parameters=params or {},
        correlation_id="corr-matching",
    )
    ctx = runtime._build_context(req)
    return runtime.execute_op(req, ctx)


def test_matching_request_validation():
    runtime = MatchingRuntime()
    req = DomainRuntimeRequest(action_code="START_MATCHING", parameters={})
    errors = runtime.validate(req)
    assert len(errors) > 0
    assert "property_type" in errors[0] or "city" in errors[0]


def test_matching_execute_success():
    runtime = MatchingRuntime()
    runtime.load_properties([
        {"property_id": "p1", "property_type": "apartment", "bedrooms": 2, "price": 150000, "city": "Douala", "district": "Bonamoussadi", "features": ["pool"]},
        {"property_id": "p2", "property_type": "house", "bedrooms": 3, "price": 250000, "city": "Yaounde", "district": "Mvan", "features": ["garden"]},
    ])
    result = _execute_op(runtime, "START_MATCHING", {
        "property_type": "apartment",
        "city": "Douala",
        "max_budget": 200000,
    })
    assert result["status"] == MatchingStatus.MATCH_FOUND.value
    assert result["total_count"] == 1
    assert len(result["matches"]) == 1
    assert result["matches"][0]["property_id"] == "p1"


def test_matching_no_match():
    runtime = MatchingRuntime()
    runtime.load_properties([
        {"property_id": "p1", "property_type": "apartment", "bedrooms": 2, "price": 300000, "city": "Douala"},
        {"property_id": "p2", "property_type": "studio", "bedrooms": 1, "price": 80000, "city": "Yaounde"},
    ])
    result = _execute_op(runtime, "START_MATCHING", {
        "property_type": "house",
    })
    assert result["status"] == MatchingStatus.NO_MATCH.value
    assert result["total_count"] == 0
    assert result["matches"] == []


def test_matching_invalid_request():
    runtime = MatchingRuntime()
    req = DomainRuntimeRequest(action_code="UNKNOWN_ACTION", parameters={})
    errors = runtime.validate(req)
    assert len(errors) > 0
    assert "UNKNOWN_ACTION" in errors[0]


def test_matching_handler_registration():
    handler = MatchingHandler()
    assert handler.can_handle("START_MATCHING") is True
    assert handler.can_handle("START_PRELIMINARY_MATCHING") is True
    assert handler.can_handle("REFINE_MATCHING") is True
    assert handler.can_handle("PRESENT_MATCHES") is True
    assert handler.can_handle("UNKNOWN") is False
    assert handler.handler_name == "matching_handler"


def test_matching_event_produced():
    assert MatchingEventType.MATCHING_STARTED.value == "MATCHING_STARTED"
    assert MatchingEventType.MATCHING_REQUESTED.value == "MATCHING_REQUESTED"
    assert MatchingEventType.MATCHING_COMPLETED.value == "MATCHING_COMPLETED"
    assert MatchingEventType.MATCHING_REFINED.value == "MATCHING_REFINED"
    assert MatchingEventType.MATCHING_FAILED.value == "MATCHING_FAILED"
    assert len(MatchingEventType) == 5


def test_matching_metrics_recorded():
    metrics = MatchingMetrics()
    assert metrics.snapshot()["searches_started"] == 0
    assert metrics.snapshot()["matches_found"] == 0
    metrics.searches_started += 1
    metrics.matches_found += 2
    metrics.no_match_count += 1
    metrics.searches_completed += 1
    snap = metrics.snapshot()
    assert snap["searches_started"] == 1
    assert snap["matches_found"] == 2
    assert snap["no_match_count"] == 1
    assert snap["searches_completed"] == 1
    metrics.reset()
    assert metrics.snapshot()["searches_started"] == 0


def test_matching_policy_defaults():
    assert MATCHING_POLICY.idempotent is True
    assert MATCHING_POLICY.max_attempts == 2
    assert MATCHING_POLICY.timeout_seconds == 120
    assert MATCHING_POLICY.shadow_mode is True
