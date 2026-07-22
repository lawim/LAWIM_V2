from __future__ import annotations

from lawim_runtime.execution.events import EventCollector, ExecutionEvent, ExecutionEventType


class TestEventCollector:
    def test_record_event(self):
        collector = EventCollector()
        event = ExecutionEvent(
            event_id="e1",
            event_type=ExecutionEventType.EXECUTION_STARTED,
            execution_id="exec-1",
        )
        collector.record(event)
        assert collector.count() == 1

    def test_flush(self):
        collector = EventCollector()
        collector.record(ExecutionEvent(
            event_id="e1", event_type=ExecutionEventType.EXECUTION_STARTED, execution_id="exec-1"))
        flushed = collector.flush()
        assert len(flushed) == 1
        assert collector.count() == 0

    def test_list_all(self):
        collector = EventCollector()
        collector.record(ExecutionEvent(
            event_id="e1", event_type=ExecutionEventType.EXECUTION_STARTED, execution_id="exec-1"))
        assert len(collector.list_all()) == 1

    def test_clear(self):
        collector = EventCollector()
        collector.record(ExecutionEvent(
            event_id="e1", event_type=ExecutionEventType.EXECUTION_STARTED, execution_id="exec-1"))
        collector.clear()
        assert collector.count() == 0
