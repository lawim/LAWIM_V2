from __future__ import annotations

from lawim_runtime.execution.adapters.decision_adapter import DecisionAdapter
from lawim_runtime.execution.adapters.workflow_adapter import WorkflowAdapter
from lawim_runtime.execution.adapters.v2_task_adapter import V2TaskAdapter


class TestDecisionAdapter:
    def test_to_execution_request(self):
        adapter = DecisionAdapter()
        req = adapter.to_execution_request("dec-1", "proj-1", "action-1", {"key": "val"}, priority=50)
        assert req.decision_id == "dec-1"
        assert req.project_id == "proj-1"
        assert req.action_code == "action-1"
        assert req.action_parameters == {"key": "val"}
        assert req.priority == 50

    def test_from_execution_request(self):
        adapter = DecisionAdapter()
        req = adapter.to_execution_request("dec-1", "proj-1", "action-1", {"key": "val"})
        data = adapter.from_execution_request(req)
        assert data["decision_id"] == "dec-1"
        assert data["action_code"] == "action-1"


class TestWorkflowAdapter:
    def test_to_execution_request(self):
        adapter = WorkflowAdapter()
        req = adapter.to_execution_request("wf-1", "task-1", "action-1", {"key": "val"})
        assert req.decision_id == "wf-1"
        assert req.project_id == "task-1"
        assert req.action_code == "action-1"


class TestV2TaskAdapter:
    def test_to_execution_request(self):
        adapter = V2TaskAdapter()
        req = adapter.to_execution_request("task_type", {
            "project_id": "proj-1",
            "decision_id": "dec-1",
            "correlation_id": "corr-1",
        })
        assert req.action_code == "task_type"
        assert req.project_id == "proj-1"
        assert req.correlation_id == "corr-1"
