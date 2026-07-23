from lawim_runtime.intelligence.observability import AIMetrics


def test_metrics_defaults():
    m = AIMetrics()
    snap = m.snapshot()
    assert snap["ai_request_total"] == 0
    assert snap["ai_success_total"] == 0


def test_metrics_increment():
    m = AIMetrics()
    m.ai_request_total = 10
    m.ai_success_total = 8
    m.ai_failure_total = 1
    m.ai_fallback_total = 1
    m.ai_prompt_injection_detected_total = 2

    snap = m.snapshot()
    assert snap["ai_request_total"] == 10
    assert snap["ai_success_total"] == 8
    assert snap["ai_prompt_injection_detected_total"] == 2


def test_metrics_reset():
    m = AIMetrics()
    m.ai_request_total = 10
    m.reset()
    assert m.ai_request_total == 0
