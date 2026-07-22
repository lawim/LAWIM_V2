from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.registry import DomainRuntimeRegistry
from lawim_runtime.domains.base.errors import DomainNotFoundError
from lawim_runtime.domains.base.events import DomainEvent, EventCollector
from lawim_runtime.domains.base.metrics import MetricsCollector, DomainMetrics
from lawim_runtime.domains.matching.runtime import MatchingRuntime


def test_domain_runtime_request_creation():
    req = DomainRuntimeRequest(
        request_id="req-001",
        action_code="START_MATCHING",
        parameters={"city": "Douala"},
        correlation_id="corr-1",
        causation_id="cause-1",
        idempotency_key="idem-1",
        metadata={"source": "test"},
    )
    assert req.request_id == "req-001"
    assert req.action_code == "START_MATCHING"
    assert req.parameters == {"city": "Douala"}
    assert req.correlation_id == "corr-1"
    assert req.causation_id == "cause-1"
    assert req.idempotency_key == "idem-1"
    assert req.metadata == {"source": "test"}
    assert isinstance(req, object)


def test_domain_runtime_result_creation():
    res = DomainRuntimeResult(
        request_id="req-001",
        action_code="START_MATCHING",
        status=DomainRuntimeStatus.SUCCEEDED,
        output={"matches": [{"property_id": "p1"}]},
        events=[{"event_type": "test"}],
        error="",
        metrics={"duration_ms": 100},
        metadata={"source": "test"},
    )
    assert res.request_id == "req-001"
    assert res.action_code == "START_MATCHING"
    assert res.status == DomainRuntimeStatus.SUCCEEDED
    assert res.output == {"matches": [{"property_id": "p1"}]}
    assert res.events == [{"event_type": "test"}]
    assert res.error == ""
    assert res.metrics == {"duration_ms": 100}
    assert res.metadata == {"source": "test"}


def test_domain_runtime_status_enum():
    assert DomainRuntimeStatus.PENDING.value == "PENDING"
    assert DomainRuntimeStatus.RUNNING.value == "RUNNING"
    assert DomainRuntimeStatus.SUCCEEDED.value == "SUCCEEDED"
    assert DomainRuntimeStatus.FAILED.value == "FAILED"
    assert DomainRuntimeStatus.SKIPPED.value == "SKIPPED"
    assert DomainRuntimeStatus.SIMULATED.value == "SIMULATED"
    assert DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED.value == "DOMAIN_PROVIDER_REQUIRED"
    assert DomainRuntimeStatus.HANDLER_NOT_IMPLEMENTED.value == "HANDLER_NOT_IMPLEMENTED"

    assert DomainRuntimeStatus.SUCCEEDED.is_terminal is True
    assert DomainRuntimeStatus.FAILED.is_terminal is True
    assert DomainRuntimeStatus.PENDING.is_terminal is False
    assert DomainRuntimeStatus.RUNNING.is_terminal is False

    assert DomainRuntimeStatus.SUCCEEDED.is_success is True
    assert DomainRuntimeStatus.PENDING.is_success is False

    assert DomainRuntimeStatus.FAILED.is_failure is True
    assert DomainRuntimeStatus.SUCCEEDED.is_failure is False

    all_terminal = {s for s in DomainRuntimeStatus if s.is_terminal}
    assert DomainRuntimeStatus.SUCCEEDED in all_terminal
    assert DomainRuntimeStatus.FAILED in all_terminal
    assert DomainRuntimeStatus.SKIPPED in all_terminal
    assert DomainRuntimeStatus.SIMULATED in all_terminal
    assert DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED in all_terminal
    assert DomainRuntimeStatus.HANDLER_NOT_IMPLEMENTED in all_terminal

    all_failure = {s for s in DomainRuntimeStatus if s.is_failure}
    assert DomainRuntimeStatus.FAILED in all_failure
    assert DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED in all_failure
    assert DomainRuntimeStatus.HANDLER_NOT_IMPLEMENTED in all_failure
    assert DomainRuntimeStatus.SUCCEEDED not in all_failure


def test_domain_runtime_context_creation():
    req = DomainRuntimeRequest(request_id="req-001", action_code="START_MATCHING")
    ctx = DomainRuntimeContext(
        request=req,
        runtime_name="matching",
        services={"db": "in_memory"},
        attempt_number=1,
        metadata={"env": "test"},
    )
    assert ctx.request.request_id == "req-001"
    assert ctx.runtime_name == "matching"
    assert ctx.services == {"db": "in_memory"}
    assert ctx.attempt_number == 1
    assert ctx.metadata == {"env": "test"}
    assert ctx.started_at != ""


def test_domain_registry_register_and_resolve():
    registry = DomainRuntimeRegistry()
    runtime = MatchingRuntime()
    registry.register(runtime)

    resolved = registry.resolve("START_MATCHING")
    assert resolved is runtime
    assert resolved.runtime_name == "matching"

    runtimes = registry.list_runtimes()
    assert len(runtimes) == 1
    assert runtimes[0] is runtime

    assert registry.count() == 1


def test_domain_registry_resolve_not_found_raises():
    registry = DomainRuntimeRegistry()
    try:
        registry.resolve("NONEXISTENT_ACTION")
        assert False, "expected DomainNotFoundError"
    except DomainNotFoundError as e:
        assert "NONEXISTENT_ACTION" in str(e)


def test_domain_event_creation():
    event = DomainEvent(
        event_id="evt-001",
        event_type="MATCHING_STARTED",
        runtime_name="matching",
        execution_id="exec-1",
        action_code="START_MATCHING",
        data={"property_type": "apartment"},
        correlation_id="corr-1",
    )
    assert event.event_id == "evt-001"
    assert event.event_type == "MATCHING_STARTED"
    assert event.runtime_name == "matching"
    assert event.execution_id == "exec-1"
    assert event.action_code == "START_MATCHING"
    assert event.data == {"property_type": "apartment"}
    assert event.correlation_id == "corr-1"
    assert event.timestamp != ""
    assert isinstance(event, object)


def test_domain_metrics_record():
    collector = MetricsCollector()

    collector.record_started()
    collector.record_succeeded()
    collector.record_duration(150.0)

    snapshot = collector.snapshot()
    assert snapshot["executions_started"] == 1
    assert snapshot["executions_succeeded"] == 1
    assert snapshot["executions_failed"] == 0
    assert snapshot["total_duration_ms"] == 150.0

    collector.record_failed()
    snapshot = collector.snapshot()
    assert snapshot["executions_failed"] == 1

    metrics = collector.metrics
    assert isinstance(metrics, DomainMetrics)
    assert metrics.executions_started == 1

    collector.reset()
    snapshot = collector.snapshot()
    assert snapshot["executions_started"] == 0
    assert snapshot["executions_succeeded"] == 0
    assert snapshot["executions_failed"] == 0
    assert snapshot["total_duration_ms"] == 0.0
