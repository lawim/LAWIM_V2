from __future__ import annotations

from unittest.mock import MagicMock

from lawim_runtime.execution.recovery import (
    ExecutionRecoveryService,
    RecoveryActionType,
)


class TestExecutionRecoveryService:
    def test_recover_all_empty_without_components(self):
        service = ExecutionRecoveryService()
        actions = service.recover_all()
        assert actions == []

    def test_detect_orphaned_with_empty_repo(self):
        repo = MagicMock()
        repo.list_executions.return_value = []
        service = ExecutionRecoveryService(repository=repo)
        actions = service.detect_orphaned()
        assert actions == []

    def test_detect_orphaned_with_active_executions(self):
        repo = MagicMock()
        repo.list_executions.return_value = [
            {"execution_id": "e1", "state": "RUNNING"},
        ]
        service = ExecutionRecoveryService(repository=repo)
        actions = service.detect_orphaned()
        assert len(actions) == 1
        assert actions[0].action_type == RecoveryActionType.ORPHAN_DETECTED

    def test_detect_pending_retries(self):
        repo = MagicMock()
        repo.list_executions.return_value = [
            {"execution_id": "e1", "state": "RETRYING"},
        ]
        service = ExecutionRecoveryService(repository=repo)
        actions = service.detect_pending_retries()
        assert len(actions) == 1
        assert actions[0].action_type == RecoveryActionType.RETRY_PENDING

    def test_detect_unfinished_compensations(self):
        repo = MagicMock()
        repo.list_executions.return_value = [
            {"execution_id": "e1", "state": "COMPENSATING"},
        ]
        service = ExecutionRecoveryService(repository=repo)
        actions = service.detect_unfinished_compensations()
        assert len(actions) == 1
        assert actions[0].action_type == RecoveryActionType.COMPENSATION_UNFINISHED

    def test_detect_expired_leases_without_manager(self):
        service = ExecutionRecoveryService()
        actions = service.detect_expired_leases()
        assert actions == []

    def test_detect_expired_leases(self):
        lease_mgr = MagicMock()
        lease = MagicMock()
        lease.lease_id = "lease-1"
        lease.resource_key = "resource-1"
        lease.owner = "worker-1"
        lease.acquired_at.isoformat.return_value = "2024-01-01T00:00:00"
        lease_mgr.recover_expired.return_value = [lease]
        service = ExecutionRecoveryService(lease_manager=lease_mgr)
        actions = service.detect_expired_leases()
        assert len(actions) == 1
        assert actions[0].action_type == RecoveryActionType.LEASE_EXPIRED

    def test_detect_dead_letter_review(self):
        dlq = MagicMock()
        record = MagicMock()
        record.dead_letter_id = "dl-1"
        record.execution_id = "exec-1"
        dlq.list.return_value = [record]
        service = ExecutionRecoveryService(dead_letter_queue=dlq)
        actions = service.detect_dead_letter_review()
        assert len(actions) == 1
        assert actions[0].action_type == RecoveryActionType.DEAD_LETTER_REVIEW

    def test_recover_all_with_multiple_sources(self):
        repo = MagicMock()
        repo.list_executions.return_value = [
            {"execution_id": "e1", "state": "RUNNING"},
            {"execution_id": "e2", "state": "RETRYING"},
        ]
        service = ExecutionRecoveryService(repository=repo)
        actions = service.recover_all()
        assert len(actions) >= 2

    def test_orphaned_only_active_states(self):
        repo = MagicMock()
        repo.list_executions.return_value = [
            {"execution_id": "e1", "state": "SUCCEEDED"},
            {"execution_id": "e2", "state": "FAILED"},
        ]
        service = ExecutionRecoveryService(repository=repo)
        actions = service.detect_orphaned()
        assert actions == []

    def test_repo_exception_graceful(self):
        repo = MagicMock()
        repo.list_executions.side_effect = RuntimeError("db down")
        service = ExecutionRecoveryService(repository=repo)
        actions = service.detect_orphaned()
        assert actions == []
