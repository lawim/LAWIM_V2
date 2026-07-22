import time
from ..telemetry.metrics import RuntimeMetrics


def test_metrics_counters():
    m = RuntimeMetrics()
    m.record_event_received("TEST")
    m.record_event_received("TEST")
    m.record_engine_executed("qualification")
    assert m.events_received["TEST"] == 2
    assert m.engines_executed["qualification"] == 1
    assert m.get_summary()["total_events"] == 2


def test_metrics_measure():
    m = RuntimeMetrics()
    with m.measure("LATENCY_TEST"):
        time.sleep(0.001)
    assert len(m.event_latency["LATENCY_TEST"]) == 1
    assert m.event_latency["LATENCY_TEST"][0] > 0


def test_metrics_summary():
    m = RuntimeMetrics()
    m.record_event_received("A")
    m.record_event_received("B")
    m.record_transition()
    s = m.get_summary()
    assert s["total_events"] == 2
    assert s["transitions"] == 1
