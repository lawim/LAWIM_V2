from __future__ import annotations

from lawim_runtime.execution.queue.dead_letter import DeadLetterQueue, DeadLetterReason, DeadLetterRecord


class TestDeadLetterQueue:
    def test_add_record(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(execution_id="exec-1", reason=DeadLetterReason.PERMANENT_FAILURE))
        assert dlq.count() == 1

    def test_list(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(execution_id="exec-1"))
        assert len(dlq.list()) == 1

    def test_list_unreviewed(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(execution_id="exec-1"))
        dlq.add(DeadLetterRecord(execution_id="exec-2", reason=DeadLetterReason.TIMEOUT))
        assert len(dlq.list_unreviewed()) == 2

    def test_mark_reviewed(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(execution_id="exec-1"))
        records = dlq.list()
        assert dlq.mark_reviewed(records[0].dead_letter_id, "resolved") is True
        assert dlq.list_unreviewed() == []

    def test_get_record(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(execution_id="exec-1"))
        records = dlq.list()
        found = dlq.get(records[0].dead_letter_id)
        assert found is not None

    def test_get_nonexistent(self):
        dlq = DeadLetterQueue()
        assert dlq.get("ghost") is None

    def test_remove(self):
        dlq = DeadLetterQueue()
        dlq.add(DeadLetterRecord(execution_id="exec-1"))
        records = dlq.list()
        assert dlq.remove(records[0].dead_letter_id) is True
        assert dlq.count() == 0
