from __future__ import annotations

import pytest

from lawim_runtime.execution.queue.queue import ExecutionQueue, QueueItem


class TestExecutionQueue:
    def test_enqueue(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
        assert q.size == 1

    def test_dequeue(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
        item = q.dequeue()
        assert item is not None
        assert q.size == 0

    def test_priority_order(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(priority=100, enqueued_at="2024-01-01T00:00:00"))
        q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
        first = q.dequeue()
        assert first.priority == 10

    def test_peek(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
        assert q.peek() is not None

    def test_cancel(self):
        q = ExecutionQueue()
        q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
        items = q.list_pending()
        assert q.cancel(items[0].item_id) is True
        assert q.size == 0

    def test_queue_full(self):
        q = ExecutionQueue()
        q._max_size = 1
        q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
        with pytest.raises(RuntimeError):
            q.enqueue(QueueItem(priority=10, enqueued_at="2024-01-01T00:00:00"))
