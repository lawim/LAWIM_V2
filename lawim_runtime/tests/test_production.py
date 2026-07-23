import pytest
from lawim_runtime.production.config import ProductionConfig, AppEnvironment, load_from_env
from lawim_runtime.production.health import HealthChecker, db_health_check
from lawim_runtime.production.resilience import CircuitBreaker, CircuitBreakerConfig, CircuitState, RetryPolicy, RateLimiter


def test_production_config_defaults():
    cfg = ProductionConfig()
    assert cfg.env == AppEnvironment.DEVELOPMENT
    assert not cfg.ai_intelligence_enabled
    assert cfg.ai_shadow_mode


def test_production_config_validation_passes():
    cfg = ProductionConfig(env=AppEnvironment.DEVELOPMENT, public_base_url="http://localhost")
    errors = cfg.validate()
    assert len(errors) == 0


def test_production_config_production_validation():
    cfg = ProductionConfig(
        env=AppEnvironment.PRODUCTION,
        public_base_url="http://insecure.local",
        ai_provider_calls_enabled=True,
        ai_budget_monthly_cents=0,
    )
    errors = cfg.validate()
    assert any("HTTPS" in e for e in errors)
    assert any("budget" in e for e in errors)


def test_health_checker():
    hc = HealthChecker(version="test")
    hc.register_check("always_ok", lambda: "ok")
    result = hc.check()
    assert result.status == "ok"
    assert result.version == "test"
    assert result.uptime_seconds >= 0
    assert result.checks["always_ok"] == "ok"


def test_health_checker_degraded():
    hc = HealthChecker()
    hc.register_check("failing", lambda: "error: db down")
    result = hc.check()
    assert result.status == "degraded"


def test_health_checker_is_ready():
    hc = HealthChecker()
    hc.register_check("ok", lambda: "ok")
    assert hc.is_ready()
    assert hc.is_live()


def test_circuit_breaker_closed():
    cb = CircuitBreaker("test")
    assert cb.state == CircuitState.CLOSED
    assert cb.call(lambda: "ok") == "ok"
    assert cb.state == CircuitState.CLOSED


def test_circuit_breaker_opens_on_failures():
    cb = CircuitBreaker("test2", CircuitBreakerConfig(failure_threshold=2, recovery_timeout_seconds=999))
    with pytest.raises(ValueError):
        cb.call(lambda: (_ for _ in ()).throw(ValueError("fail")))
    assert cb.state == CircuitState.CLOSED
    with pytest.raises(ValueError):
        cb.call(lambda: (_ for _ in ()).throw(ValueError("fail")))
    assert cb.state == CircuitState.OPEN


def test_circuit_breaker_open_rejects():
    cb = CircuitBreaker("test3", CircuitBreakerConfig(failure_threshold=1, recovery_timeout_seconds=999))
    with pytest.raises(ValueError):
        cb.call(lambda: (_ for _ in ()).throw(ValueError("fail")))
    assert cb.state == CircuitState.OPEN
    with pytest.raises(RuntimeError):
        cb.call(lambda: "should not reach")


def test_retry_policy_success():
    rp = RetryPolicy(max_retries=2, base_delay_seconds=0)
    assert rp.execute(lambda: "ok") == "ok"


def test_retry_policy_fails_after_retries():
    rp = RetryPolicy(max_retries=1, base_delay_seconds=0)
    calls = []

    def fail():
        calls.append(1)
        raise ValueError("fail")

    with pytest.raises(ValueError):
        rp.execute(fail)
    assert len(calls) == 2


def test_rate_limiter():
    rl = RateLimiter(max_per_second=1000, burst=1000)
    assert rl.acquire()
    assert rl.acquire()
