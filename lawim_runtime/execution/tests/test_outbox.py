from __future__ import annotations

from lawim_runtime.execution.outbox import ExecutionOutbox, OutboxStatus


class TestExecutionOutbox:
    def test_publish(self):
        outbox = ExecutionOutbox()
        msg = outbox.publish("topic-1", "key-1", {"data": "test"})
        assert msg.status == OutboxStatus.PUBLISHED
        assert outbox.count() == 1

    def test_enqueue_pending(self):
        outbox = ExecutionOutbox()
        msg = outbox.enqueue("topic-1", "key-1", {"data": "test"})
        assert msg.status == OutboxStatus.PENDING

    def test_mark_published(self):
        outbox = ExecutionOutbox()
        msg = outbox.enqueue("t", "k", {"d": "v"})
        assert outbox.mark_published(msg.message_id) is True
        assert msg.status == OutboxStatus.PUBLISHED

    def test_mark_failed(self):
        outbox = ExecutionOutbox()
        msg = outbox.enqueue("t", "k", {"d": "v"})
        assert outbox.mark_failed(msg.message_id, "error") is True
        assert msg.status == OutboxStatus.FAILED

    def test_list_pending(self):
        outbox = ExecutionOutbox()
        outbox.enqueue("t", "k", {"d": "v"})
        outbox.publish("t2", "k2", {"d": "v"})
        assert len(outbox.list_pending()) == 1

    def test_list_published(self):
        outbox = ExecutionOutbox()
        outbox.publish("t", "k", {"d": "v"})
        assert len(outbox.list_published()) == 1

    def test_clear(self):
        outbox = ExecutionOutbox()
        outbox.publish("t", "k", {"d": "v"})
        outbox.clear()
        assert outbox.count() == 0
