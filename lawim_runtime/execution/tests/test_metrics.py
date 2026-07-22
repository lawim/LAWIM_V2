from __future__ import annotations

from lawim_runtime.execution.metrics import MetricsCollector


class TestMetricsCollector:
    def test_initial_zeros(self):
        collector = MetricsCollector()
        metrics = collector.metrics
        assert metrics.executions_started == 0

    def test_record_started(self):
        collector = MetricsCollector()
        collector.record_started()
        assert collector.metrics.executions_started == 1
        assert collector.metrics.total_attempts == 1

    def test_record_succeeded(self):
        collector = MetricsCollector()
        collector.record_succeeded()
        assert collector.metrics.executions_succeeded == 1

    def test_record_failed(self):
        collector = MetricsCollector()
        collector.record_failed()
        assert collector.metrics.executions_failed == 1

    def test_snapshot(self):
        collector = MetricsCollector()
        collector.record_started()
        collector.record_succeeded()
        snap = collector.snapshot()
        assert snap["executions_started"] == 1
        assert snap["executions_succeeded"] == 1

    def test_reset(self):
        collector = MetricsCollector()
        collector.record_started()
        collector.reset()
        assert collector.metrics.executions_started == 0
