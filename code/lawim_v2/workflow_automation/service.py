from __future__ import annotations

import time

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as wdto


class WorkflowAutomationService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    def list_workflows(self, *, actor: dict[str, object], domain: str | None = None, status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("workflow_definitions")
        return {"workflows": [wdto.workflow_definition_dto(r) for r in self.repository.list_automation_workflows(domain=domain, status=status)]}

    def get_workflow(self, *, actor: dict[str, object], workflow_key: str) -> dict[str, object]:
        self._require_auth(actor)
        return {"workflow": wdto.workflow_definition_dto(self.repository.get_automation_workflow(workflow_key))}

    def create_workflow(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        doc = self.repository.create_automation_workflow(body=body)
        METRICS.increment("workflow_created")
        return {"workflow": wdto.workflow_definition_dto(doc)}

    def duplicate_workflow(self, *, actor: dict[str, object], workflow_key: str) -> dict[str, object]:
        self._require_admin(actor)
        return {"workflow": wdto.workflow_definition_dto(self.repository.duplicate_automation_workflow(workflow_key))}

    def activate_workflow(self, *, actor: dict[str, object], workflow_key: str) -> dict[str, object]:
        self._require_admin(actor)
        return {"workflow": wdto.workflow_definition_dto(self.repository.set_automation_workflow_status(workflow_key, "active"))}

    def deactivate_workflow(self, *, actor: dict[str, object], workflow_key: str) -> dict[str, object]:
        self._require_admin(actor)
        return {"workflow": wdto.workflow_definition_dto(self.repository.set_automation_workflow_status(workflow_key, "paused"))}

    def list_templates(self, *, actor: dict[str, object], domain: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"templates": [wdto.template_dto(r) for r in self.repository.list_automation_templates(domain=domain)]}

    def create_template(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        return {"template": wdto.template_dto(self.repository.create_automation_template(body=body))}

    def list_executions(self, *, actor: dict[str, object], instance_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("process_executions")
        return {"executions": [wdto.execution_dto(r) for r in self.repository.list_automation_executions(instance_id=instance_id)]}

    def list_instances(self, *, actor: dict[str, object], project_id: int | None = None, status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        return {"instances": [wdto.instance_dto(r) for r in self.repository.list_automation_instances(project_id=project_id, status=status)]}

    def start_instance(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        project_id = body.get("project_id")
        if project_id is not None:
            self.projects._require_access(actor, int(project_id))
        started = time.perf_counter()
        instance = self.repository.start_automation_instance(
            workflow_key=str(body["workflow_key"]),
            project_id=int(project_id) if project_id is not None else None,
            context=dict(body.get("context") or {}),
            actor_id=int(actor["id"]) if actor.get("id") is not None else None,
            priority=str(body.get("priority") or "normal"),
        )
        METRICS.record_process_execution(duration_ms=(time.perf_counter() - started) * 1000)
        METRICS.increment("automation_started")
        return {"instance": wdto.instance_dto(instance)}

    def advance_instance(self, *, actor: dict[str, object], instance_id: int) -> dict[str, object]:
        self._require_auth(actor)
        actor_id = int(actor["id"]) if actor.get("id") is not None else None
        payload = self.repository.advance_automation_instance(instance_id, actor_id=actor_id)
        METRICS.increment("automation_events")
        return payload

    def list_tasks(self, *, actor: dict[str, object], instance_id: int | None = None, status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("task_list")
        return {"tasks": [wdto.task_dto(r) for r in self.repository.list_automation_tasks(instance_id=instance_id, status=status)]}

    def complete_task(self, *, actor: dict[str, object], task_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        task = self.repository.complete_automation_task(task_id, result=dict(body.get("result") or {}))
        METRICS.increment("task_completed")
        return {"task": wdto.task_dto(task)}

    def list_queues(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("queue_list")
        return {"queues": [wdto.queue_dto(r) for r in self.repository.list_automation_queues()]}

    def enqueue(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        item = self.repository.enqueue_automation_item(
            queue_key=str(body["queue_key"]),
            payload=dict(body.get("payload") or {}),
            priority=str(body.get("priority") or "normal"),
        )
        METRICS.increment("queue_enqueue")
        return {"item": item}

    def dequeue(self, *, actor: dict[str, object], queue_key: str) -> dict[str, object]:
        self._require_admin(actor)
        item = self.repository.dequeue_automation_item(queue_key)
        METRICS.increment("queue_dequeue")
        return {"item": item}

    def list_events(self, *, actor: dict[str, object], instance_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("event_list")
        return {"events": [wdto.event_dto(r) for r in self.repository.list_automation_events(instance_id=instance_id)]}

    def publish_event(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        event = self.repository.publish_automation_event(
            event_type=str(body["event_type"]),
            instance_id=int(body["instance_id"]) if body.get("instance_id") is not None else None,
            payload=dict(body.get("payload") or {}),
        )
        METRICS.increment("automation_events")
        return {"event": wdto.event_dto(event)}

    def list_approvals(self, *, actor: dict[str, object], instance_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("approval_list")
        return {"approvals": [wdto.approval_dto(r) for r in self.repository.list_automation_approvals(instance_id=instance_id)]}

    def create_approval(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        approval = self.repository.create_automation_approval(
            instance_id=int(body["instance_id"]),
            level=int(body.get("level") or 1),
            approver_id=int(body["approver_id"]) if body.get("approver_id") is not None else None,
        )
        METRICS.increment("approval_created")
        return {"approval": wdto.approval_dto(approval)}

    def decide_approval(self, *, actor: dict[str, object], approval_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        approval = self.repository.decide_automation_approval(approval_id, status=str(body["status"]), note=str(body.get("note") or ""))
        METRICS.increment("approval_decided")
        return {"approval": wdto.approval_dto(approval)}

    def list_rules(self, *, actor: dict[str, object], domain: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"rules": [wdto.rule_dto(r) for r in self.repository.list_automation_rules(domain=domain)]}

    def create_rule(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        rule = self.repository.create_automation_rule(body=body)
        return {"rule": wdto.rule_dto(rule)}

    def evaluate_rules(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        matched = self.repository.evaluate_automation_rules(context=dict(body.get("context") or {}), domain=body.get("domain"))
        return {"matched": matched}

    def list_schedules(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"schedules": [wdto.schedule_dto(r) for r in self.repository.list_automation_schedules()]}

    def list_timers(self, *, actor: dict[str, object], instance_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        return {"timers": [wdto.timer_dto(r) for r in self.repository.list_automation_timers(instance_id=instance_id)]}

    def create_timer(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        timer = self.repository.create_automation_timer(
            instance_id=int(body["instance_id"]),
            fire_at=str(body["fire_at"]),
            action=dict(body.get("action") or {}),
        )
        return {"timer": wdto.timer_dto(timer)}

    def list_notifications(self, *, actor: dict[str, object], instance_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("automation_notifications")
        return {"notifications": [wdto.notification_dto(r) for r in self.repository.list_automation_notifications(instance_id=instance_id)]}

    def send_notification(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        note = self.repository.send_automation_notification(
            title=str(body["title"]),
            body=str(body.get("body") or ""),
            recipient_id=int(body["recipient_id"]) if body.get("recipient_id") is not None else None,
            instance_id=int(body["instance_id"]) if body.get("instance_id") is not None else None,
        )
        METRICS.increment("notification_sent")
        return {"notification": wdto.notification_dto(note)}

    def history(self, *, actor: dict[str, object], instance_id: int) -> dict[str, object]:
        self._require_auth(actor)
        return {"history": [wdto.history_dto(r) for r in self.repository.list_automation_history(instance_id=instance_id)]}

    def audit(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        return {"audit": [wdto.audit_dto(r) for r in self.repository.list_automation_audit()]}

    def metrics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return {"metrics": self.repository.automation_stats()}

    def monitoring(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        return wdto.monitoring_dto(self.repository.automation_monitoring())

    def reindex_metrics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        return self.repository.snapshot_automation_metrics()

    def retry_execution(self, *, actor: dict[str, object], execution_id: int) -> dict[str, object]:
        self._require_admin(actor)
        execution = self.repository.retry_automation_execution(execution_id)
        METRICS.increment("automation_retry")
        return {"execution": wdto.execution_dto(execution)}

    def escalate(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        esc = self.repository.escalate_automation_instance(int(body["instance_id"]), reason=str(body.get("reason") or ""), level=int(body.get("level") or 1))
        METRICS.increment("automation_escalation")
        return {"escalation": esc}

    def ai_hook(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        project_id = int(body["project_id"]) if body.get("project_id") is not None else None
        if project_id is not None:
            self.projects._require_access(actor, project_id)
        return self.repository.invoke_automation_ai_hook(
            hook_type=str(body.get("hook_type") or "maintenance_intake"),
            query=str(body.get("query") or ""),
            project_id=project_id,
        )
