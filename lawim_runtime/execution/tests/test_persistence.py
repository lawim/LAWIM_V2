from __future__ import annotations

from lawim_runtime.execution.persistence.memory import InMemoryExecutionRepository
from lawim_runtime.execution.result import ActionExecutionResult, ExecutionStatus


class TestInMemoryExecutionRepository:
    def test_save_and_get(self):
        repo = InMemoryExecutionRepository()
        execution = ActionExecutionResult(execution_id="e1", action_code="test")
        repo.save(execution)
        fetched = repo.get_execution("e1")
        assert fetched is execution

    def test_get_nonexistent(self):
        repo = InMemoryExecutionRepository()
        assert repo.get_execution("ghost") is None

    def test_update_status(self):
        repo = InMemoryExecutionRepository()
        execution = ActionExecutionResult(execution_id="e1", action_code="test")
        repo.save(execution)
        repo.update_status("e1", ExecutionStatus.RUNNING)
        assert repo.get_execution("e1").status == ExecutionStatus.RUNNING

    def test_list_executions(self):
        repo = InMemoryExecutionRepository()
        repo.save(ActionExecutionResult(execution_id="e1", action_code="a1"))
        repo.save(ActionExecutionResult(execution_id="e2", action_code="a2"))
        assert len(repo.list_executions()) == 2

    def test_delete(self):
        repo = InMemoryExecutionRepository()
        repo.save(ActionExecutionResult(execution_id="e1", action_code="test"))
        assert repo.delete("e1") is True
        assert repo.get_execution("e1") is None

    def test_delete_nonexistent(self):
        repo = InMemoryExecutionRepository()
        assert repo.delete("ghost") is False

    def test_count(self):
        repo = InMemoryExecutionRepository()
        repo.save(ActionExecutionResult(execution_id="e1", action_code="a1"))
        repo.save(ActionExecutionResult(execution_id="e2", action_code="a2"))
        assert repo.count() == 2
