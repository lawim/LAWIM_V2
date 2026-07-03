from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from typing import Any

from .constants import AUTOMATION_DOMAINS, DEFAULT_QUEUE_CAPACITY, DEFAULT_SLA_HOURS
from .engines import AIIntegrationBridge, ProcessEngine


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


class WorkflowAutomationRepositoryMixin:
    def automation_tables_present(self) -> bool:
        row = self.one("SELECT name FROM sqlite_master WHERE type='table' AND name='automation_workflow_definitions'")
        return row is not None

    def seed_automation_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM automation_workflow_definitions") > 0:
            return
        now = _utcnow()
        engine = ProcessEngine()
        samples = (
            ("immobilier", "achat", "wf-immobilier-achat", "Parcours achat immobilier", ["start", "visite", "offre", "compromis", "acte"]),
            ("immobilier", "vente", "wf-immobilier-vente", "Parcours vente immobilier", ["start", "estimation", "mandat", "visites", "signature"]),
            ("juridique", "contrats", "wf-juridique-contrats", "Validation contractuelle", ["start", "relecture", "approbation", "signature", "archivage"]),
            ("financement", "demande", "wf-financement-demande", "Demande de financement", ["start", "etude", "scoring", "validation", "decaissement"]),
            ("administration", "support", "wf-admin-support", "Ticket support", ["start", "qualification", "traitement", "cloture"]),
            ("ia", "assistant", "wf-ia-assistant", "Orchestration assistant IA", ["start", "contexte", "rag", "reponse", "cloture"]),
        )
        with self._transaction() as conn:
            for domain, process_key, workflow_key, title, states in samples:
                conn.execute(
                    """
                    INSERT INTO automation_workflow_definitions (
                        workflow_key, domain, process_key, title, description, version, status,
                        definition_json, metadata_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, 1, 'active', ?, '{}', ?, ?)
                    """,
                    (
                        workflow_key,
                        domain,
                        process_key,
                        title,
                        f"Workflow {domain} — {process_key}",
                        _json({"states": states, "parallel_allowed": True}),
                        now,
                        now,
                    ),
                )
                template_key = f"tpl-{workflow_key}"
                steps = [{"step_key": s, "title": s.replace("_", " ").title()} for s in states]
                conn.execute(
                    """
                    INSERT INTO automation_templates (
                        template_key, workflow_key, title, domain, status, steps_json, variables_json, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, '{}', ?, ?)
                    """,
                    (template_key, workflow_key, f"Template {title}", domain, _json(steps), now, now),
                )
                for idx, state_key in enumerate(states):
                    conn.execute(
                        """
                        INSERT INTO automation_states (workflow_key, state_key, title, state_type, is_terminal, metadata_json, created_at)
                        VALUES (?, ?, ?, ?, ?, '{}', ?)
                        """,
                        (workflow_key, state_key, state_key.title(), "task", 1 if idx == len(states) - 1 else 0, now),
                    )
                    if idx < len(states) - 1:
                        conn.execute(
                            """
                            INSERT INTO automation_transitions (
                                workflow_key, transition_key, from_state_key, to_state_key, condition_json, priority, created_at
                            ) VALUES (?, ?, ?, ?, ?, 10, ?)
                            """,
                            (
                                workflow_key,
                                f"tr-{workflow_key}-{state_key}",
                                state_key,
                                states[idx + 1],
                                _json({"expression": "true"}),
                                now,
                            ),
                        )
                conn.execute(
                    """
                    INSERT INTO automation_sla_policies (policy_key, workflow_key, step_key, target_hours, escalation_level, status, created_at)
                    VALUES (?, ?, NULL, ?, 1, 'active', ?)
                    """,
                    (f"sla-{workflow_key}", workflow_key, DEFAULT_SLA_HOURS, now),
                )
            for domain in AUTOMATION_DOMAINS:
                queue_key = f"queue-{domain}"
                conn.execute(
                    """
                    INSERT INTO automation_queues (queue_key, title, domain, status, capacity, depth, metadata_json, created_at, updated_at)
                    VALUES (?, ?, ?, 'active', ?, 0, '{}', ?, ?)
                    """,
                    (queue_key, f"Queue {domain}", domain, DEFAULT_QUEUE_CAPACITY, now, now),
                )
            conn.execute(
                """
                INSERT INTO automation_rules (rule_key, workflow_key, title, domain, expression, action_json, priority, status, created_at, updated_at)
                VALUES ('rule-auto-approve-low-risk', NULL, 'Auto validation risque faible', 'general', '$risk_score < 30', ?, 5, 'active', ?, ?)
                """,
                (_json({"action": "approve", "level": 1}), now, now),
            )
            conn.execute(
                """
                INSERT INTO automation_schedules (schedule_key, workflow_key, cron_expr, status, next_run_at, metadata_json, created_at, updated_at)
                VALUES ('sched-daily-review', 'wf-admin-support', '@daily', 'active', ?, '{}', ?, ?)
                """,
                (engine.scheduler.next_daily_run(), now, now),
            )
        project = self.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")
        if project:
            self.start_automation_instance(
                workflow_key="wf-immobilier-achat",
                project_id=int(project["id"]),
                context={"source": "seed"},
                actor_id=None,
            )
        self.record_event("automation_catalog_seeded", {"workflows": len(samples)})

    def list_automation_workflows(self, *, domain: str | None = None, status: str | None = None) -> list[dict[str, object]]:
        query = "SELECT * FROM automation_workflow_definitions WHERE 1=1"
        params: list[object] = []
        if domain:
            query += " AND domain = ?"
            params.append(domain)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY domain, title ASC"
        return [dict(r) for r in self.all(query, tuple(params))]

    def get_automation_workflow(self, workflow_key: str) -> dict[str, object]:
        row = self.one("SELECT * FROM automation_workflow_definitions WHERE workflow_key = ?", (workflow_key,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("workflow not found")
        return dict(row)

    def create_automation_workflow(self, *, body: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        workflow_key = str(body.get("workflow_key") or f"wf-{uuid.uuid4().hex[:8]}")
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_workflow_definitions (
                    workflow_key, domain, process_key, title, description, version, status,
                    definition_json, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 1, 'draft', ?, '{}', ?, ?)
                """,
                (
                    workflow_key,
                    str(body["domain"]),
                    str(body.get("process_key") or "custom"),
                    str(body["title"]),
                    str(body.get("description") or ""),
                    _json(body.get("definition") or {}),
                    now,
                    now,
                ),
            )
        return self.get_automation_workflow(workflow_key)

    def duplicate_automation_workflow(self, workflow_key: str) -> dict[str, object]:
        source = self.get_automation_workflow(workflow_key)
        new_key = f"{workflow_key}-copy-{uuid.uuid4().hex[:4]}"
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_workflow_definitions (
                    workflow_key, domain, process_key, title, description, version, status,
                    definition_json, metadata_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 1, 'draft', ?, ?, ?, ?)
                """,
                (
                    new_key,
                    source["domain"],
                    source["process_key"],
                    f"{source['title']} (copie)",
                    source.get("description") or "",
                    source.get("definition_json") or "{}",
                    source.get("metadata_json") or "{}",
                    now,
                    now,
                ),
            )
        return self.get_automation_workflow(new_key)

    def set_automation_workflow_status(self, workflow_key: str, status: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE automation_workflow_definitions SET status = ?, updated_at = ? WHERE workflow_key = ?",
                (status, now, workflow_key),
            )
        return self.get_automation_workflow(workflow_key)

    def list_automation_templates(self, *, domain: str | None = None) -> list[dict[str, object]]:
        if domain:
            rows = self.all("SELECT * FROM automation_templates WHERE domain = ? ORDER BY title ASC", (domain,))
        else:
            rows = self.all("SELECT * FROM automation_templates ORDER BY domain, title ASC")
        return [dict(r) for r in rows]

    def create_automation_template(self, *, body: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        template_key = str(body.get("template_key") or f"tpl-{uuid.uuid4().hex[:8]}")
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_templates (
                    template_key, workflow_key, title, domain, status, steps_json, variables_json, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', ?, ?, ?, ?)
                """,
                (
                    template_key,
                    str(body["workflow_key"]),
                    str(body["title"]),
                    str(body["domain"]),
                    _json(body.get("steps") or []),
                    _json(body.get("variables") or {}),
                    now,
                    now,
                ),
            )
        row = self.one("SELECT * FROM automation_templates WHERE template_key = ?", (template_key,))
        return dict(row)

    def start_automation_instance(
        self,
        *,
        workflow_key: str,
        project_id: int | None = None,
        context: dict[str, Any] | None = None,
        actor_id: int | None = None,
        priority: str = "normal",
    ) -> dict[str, object]:
        self.get_automation_workflow(workflow_key)
        now = _utcnow()
        instance_key = f"inst-{uuid.uuid4().hex}"
        engine = ProcessEngine()
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO automation_process_instances (
                    instance_key, workflow_key, project_id, current_state_key, status, context_json,
                    priority, started_at, created_at, updated_at
                ) VALUES (?, ?, ?, 'start', 'running', ?, ?, ?, ?, ?)
                """,
                (instance_key, workflow_key, project_id, _json(context or {}), priority, now, now, now),
            )
            instance_id = int(cursor.lastrowid)
            exec_key = f"exec-{uuid.uuid4().hex}"
            conn.execute(
                """
                INSERT INTO automation_executions (
                    execution_key, instance_id, workflow_key, status, current_step_key, context_json, started_at, created_at
                ) VALUES (?, ?, ?, 'running', 'start', ?, ?, ?)
                """,
                (exec_key, instance_id, workflow_key, _json(context or {}), now, now),
            )
            task_key = f"task-{uuid.uuid4().hex[:8]}"
            conn.execute(
                """
                INSERT INTO automation_tasks (
                    task_key, instance_id, title, task_type, status, priority, payload_json, created_at, updated_at
                ) VALUES (?, ?, ?, 'system', 'pending', ?, ?, ?, ?)
                """,
                (task_key, instance_id, f"Démarrer {workflow_key}", priority, _json({"workflow_key": workflow_key}), now, now),
            )
            event_key = f"evt-{uuid.uuid4().hex[:8]}"
            conn.execute(
                """
                INSERT INTO automation_events (event_key, instance_id, event_type, source, payload_json, created_at)
                VALUES (?, ?, 'instance_started', 'engine', ?, ?)
                """,
                (event_key, instance_id, _json({"workflow_key": workflow_key}), now),
            )
            audit = engine.audit.entry(action="start_instance", resource_type="instance", resource_id=instance_id, detail={"workflow_key": workflow_key})
            conn.execute(
                """
                INSERT INTO automation_audit_log (audit_key, actor_id, action, resource_type, resource_id, detail_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (audit["audit_key"], actor_id, audit["action"], audit["resource_type"], instance_id, _json(audit["detail"]), now),
            )
        return self.get_automation_instance(instance_id)

    def get_automation_instance(self, instance_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM automation_process_instances WHERE id = ?", (instance_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("instance not found")
        return dict(row)

    def list_automation_instances(self, *, project_id: int | None = None, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM automation_process_instances WHERE 1=1"
        params: list[object] = []
        if project_id is not None:
            query += " AND project_id = ?"
            params.append(project_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.all(query, tuple(params))]

    def advance_automation_instance(self, instance_id: int, *, actor_id: int | None = None) -> dict[str, object]:
        instance = self.get_automation_instance(instance_id)
        workflow_key = str(instance["workflow_key"])
        transitions = [dict(r) for r in self.all("SELECT * FROM automation_transitions WHERE workflow_key = ?", (workflow_key,))]
        context = _parse_json(str(instance.get("context_json"))) or {}
        engine = ProcessEngine()
        started = time.perf_counter()
        result = engine.advance(current_state=str(instance["current_state_key"]), transitions=transitions, context=context)
        now = _utcnow()
        if not result.get("advanced"):
            return {"instance": instance, "advanced": False}
        to_state = str(result["to_state"])
        terminal = self.one(
            "SELECT is_terminal FROM automation_states WHERE workflow_key = ? AND state_key = ?",
            (workflow_key, to_state),
        )
        status = "completed" if terminal and int(terminal["is_terminal"]) else "running"
        duration_ms = int((time.perf_counter() - started) * 1000)
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE automation_process_instances
                SET current_state_key = ?, status = ?, updated_at = ?, completed_at = ?
                WHERE id = ?
                """,
                (to_state, status, now, now if status == "completed" else None, instance_id),
            )
            conn.execute(
                """
                INSERT INTO automation_history (instance_id, from_state_key, to_state_key, transition_key, actor_id, note, created_at)
                VALUES (?, ?, ?, ?, ?, 'auto advance', ?)
                """,
                (instance_id, result.get("from_state"), to_state, result.get("transition_key"), actor_id, now),
            )
            conn.execute(
                """
                UPDATE automation_executions SET current_step_key = ?, status = ?, duration_ms = ?, finished_at = ?
                WHERE instance_id = ? AND status = 'running'
                """,
                (to_state, status, duration_ms, now if status == "completed" else None, instance_id),
            )
            conn.execute(
                """
                INSERT INTO automation_events (event_key, instance_id, event_type, source, payload_json, created_at)
                VALUES (?, ?, 'state_transition', 'engine', ?, ?)
                """,
                (f"evt-{uuid.uuid4().hex[:8]}", instance_id, _json(result), now),
            )
        return {"instance": self.get_automation_instance(instance_id), "advanced": True, "transition": result}

    def list_automation_executions(self, *, instance_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if instance_id is not None:
            rows = self.all(
                "SELECT * FROM automation_executions WHERE instance_id = ? ORDER BY id DESC LIMIT ?",
                (instance_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM automation_executions ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def list_automation_tasks(self, *, instance_id: int | None = None, status: str | None = None) -> list[dict[str, object]]:
        query = "SELECT * FROM automation_tasks WHERE 1=1"
        params: list[object] = []
        if instance_id is not None:
            query += " AND instance_id = ?"
            params.append(instance_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT 100"
        return [dict(r) for r in self.all(query, tuple(params))]

    def complete_automation_task(self, task_id: int, *, result: dict[str, Any] | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE automation_tasks SET status = 'completed', result_json = ?, completed_at = ?, updated_at = ? WHERE id = ?",
                (_json(result or {}), now, now, task_id),
            )
        row = self.one("SELECT * FROM automation_tasks WHERE id = ?", (task_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("task not found")
        return dict(row)

    def list_automation_queues(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM automation_queues ORDER BY domain, title ASC")]

    def enqueue_automation_item(self, *, queue_key: str, payload: dict[str, Any], priority: str = "normal") -> dict[str, object]:
        now = _utcnow()
        item_key = f"qitem-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_queue_items (queue_key, item_key, priority, status, payload_json, created_at)
                VALUES (?, ?, ?, 'queued', ?, ?)
                """,
                (queue_key, item_key, priority, _json(payload), now),
            )
            conn.execute(
                "UPDATE automation_queues SET depth = depth + 1, updated_at = ? WHERE queue_key = ?",
                (now, queue_key),
            )
        row = self.one("SELECT * FROM automation_queue_items WHERE item_key = ?", (item_key,))
        return dict(row)

    def dequeue_automation_item(self, queue_key: str) -> dict[str, object] | None:
        engine = ProcessEngine()
        rows = [dict(r) for r in self.all("SELECT * FROM automation_queue_items WHERE queue_key = ? AND status = 'queued'", (queue_key,))]
        ordered = engine.queues.enqueue_order(rows)
        if not ordered:
            return None
        item = ordered[0]
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE automation_queue_items SET status = 'processing', processed_at = ?, attempts = attempts + 1 WHERE id = ?",
                (now, item["id"]),
            )
            conn.execute(
                "UPDATE automation_queues SET depth = CASE WHEN depth > 0 THEN depth - 1 ELSE 0 END, updated_at = ? WHERE queue_key = ?",
                (now, queue_key),
            )
        return self.one("SELECT * FROM automation_queue_items WHERE id = ?", (item["id"],))

    def publish_automation_event(self, *, event_type: str, instance_id: int | None, payload: dict[str, Any]) -> dict[str, object]:
        now = _utcnow()
        event_key = f"evt-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_events (event_key, instance_id, event_type, source, payload_json, created_at)
                VALUES (?, ?, ?, 'api', ?, ?)
                """,
                (event_key, instance_id, event_type, _json(payload), now),
            )
        row = self.one("SELECT * FROM automation_events WHERE event_key = ?", (event_key,))
        return dict(row)

    def list_automation_events(self, *, instance_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if instance_id is not None:
            rows = self.all(
                "SELECT * FROM automation_events WHERE instance_id = ? ORDER BY id DESC LIMIT ?",
                (instance_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM automation_events ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def create_automation_approval(self, *, instance_id: int, level: int = 1, approver_id: int | None = None) -> dict[str, object]:
        now = _utcnow()
        approval_key = f"appr-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_approvals (approval_key, instance_id, level, approver_id, status, created_at)
                VALUES (?, ?, ?, ?, 'pending', ?)
                """,
                (approval_key, instance_id, level, approver_id, now),
            )
        row = self.one("SELECT * FROM automation_approvals WHERE approval_key = ?", (approval_key,))
        return dict(row)

    def decide_automation_approval(self, approval_id: int, *, status: str, note: str = "") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE automation_approvals SET status = ?, note = ?, decided_at = ? WHERE id = ?",
                (status, note, now, approval_id),
            )
        row = self.one("SELECT * FROM automation_approvals WHERE id = ?", (approval_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("approval not found")
        return dict(row)

    def list_automation_approvals(self, *, instance_id: int | None = None) -> list[dict[str, object]]:
        if instance_id is not None:
            rows = self.all("SELECT * FROM automation_approvals WHERE instance_id = ? ORDER BY level ASC", (instance_id,))
        else:
            rows = self.all("SELECT * FROM automation_approvals ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in rows]

    def list_automation_rules(self, *, domain: str | None = None) -> list[dict[str, object]]:
        if domain:
            rows = self.all("SELECT * FROM automation_rules WHERE domain = ? ORDER BY priority DESC", (domain,))
        else:
            rows = self.all("SELECT * FROM automation_rules ORDER BY priority DESC")
        return [dict(r) for r in rows]

    def create_automation_rule(self, *, body: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        rule_key = str(body.get("rule_key") or f"rule-{uuid.uuid4().hex[:8]}")
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_rules (rule_key, workflow_key, title, domain, expression, action_json, priority, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (
                    rule_key,
                    body.get("workflow_key"),
                    str(body["title"]),
                    str(body.get("domain") or "general"),
                    str(body.get("expression") or "true"),
                    _json(body.get("action") or {}),
                    int(body.get("priority") or 0),
                    now,
                    now,
                ),
            )
        row = self.one("SELECT * FROM automation_rules WHERE rule_key = ?", (rule_key,))
        return dict(row)

    def evaluate_automation_rules(self, *, context: dict[str, Any], domain: str | None = None) -> list[dict[str, object]]:
        engine = ProcessEngine()
        rules = self.list_automation_rules(domain=domain)
        matched: list[dict[str, object]] = []
        for rule in rules:
            if str(rule.get("status")) != "active":
                continue
            if engine.rules.evaluate(str(rule.get("expression") or "true"), context):
                matched.append({"rule_key": rule["rule_key"], "title": rule["title"], "action": _parse_json(str(rule.get("action_json")))})
        return matched

    def list_automation_schedules(self) -> list[dict[str, object]]:
        return [dict(r) for r in self.all("SELECT * FROM automation_schedules ORDER BY id ASC")]

    def list_automation_timers(self, *, instance_id: int | None = None) -> list[dict[str, object]]:
        if instance_id is not None:
            rows = self.all("SELECT * FROM automation_timers WHERE instance_id = ? ORDER BY fire_at ASC", (instance_id,))
        else:
            rows = self.all("SELECT * FROM automation_timers WHERE status = 'pending' ORDER BY fire_at ASC LIMIT 100")
        return [dict(r) for r in rows]

    def create_automation_timer(self, *, instance_id: int, fire_at: str, action: dict[str, Any]) -> dict[str, object]:
        now = _utcnow()
        timer_key = f"timer-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_timers (timer_key, instance_id, fire_at, status, action_json, created_at)
                VALUES (?, ?, ?, 'pending', ?, ?)
                """,
                (timer_key, instance_id, fire_at, _json(action), now),
            )
        row = self.one("SELECT * FROM automation_timers WHERE timer_key = ?", (timer_key,))
        return dict(row)

    def list_automation_notifications(self, *, instance_id: int | None = None) -> list[dict[str, object]]:
        if instance_id is not None:
            rows = self.all("SELECT * FROM automation_notifications WHERE instance_id = ? ORDER BY id DESC", (instance_id,))
        else:
            rows = self.all("SELECT * FROM automation_notifications ORDER BY id DESC LIMIT 100")
        return [dict(r) for r in rows]

    def send_automation_notification(self, *, title: str, body: str, recipient_id: int | None, instance_id: int | None) -> dict[str, object]:
        engine = ProcessEngine()
        payload = engine.notifications.compose(title=title, body=body)
        now = _utcnow()
        notification_key = f"autonotif-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_notifications (
                    notification_key, instance_id, channel, recipient_id, title, body, status, sent_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'sent', ?, ?)
                """,
                (notification_key, instance_id, payload["channel"], recipient_id, payload["title"], payload["body"], now, now),
            )
        row = self.one("SELECT * FROM automation_notifications WHERE notification_key = ?", (notification_key,))
        return dict(row)

    def list_automation_history(self, *, instance_id: int) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM automation_history WHERE instance_id = ? ORDER BY id ASC", (instance_id,))
        return [dict(r) for r in rows]

    def list_automation_audit(self, *, limit: int = 100) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM automation_audit_log ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def retry_automation_execution(self, execution_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM automation_executions WHERE id = ?", (execution_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("execution not found")
        engine = ProcessEngine()
        attempt = int(row.get("attempt") or 1) + 1
        if not engine.retry.should_retry(attempt):
            raise ValueError("max retries exceeded")
        now = _utcnow()
        backoff = engine.retry.schedule_backoff(attempt)
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_retries (execution_id, attempt, status, backoff_seconds, scheduled_at, created_at)
                VALUES (?, ?, 'pending', ?, ?, ?)
                """,
                (execution_id, attempt, backoff, now, now),
            )
            conn.execute(
                "UPDATE automation_executions SET status = 'running', attempt = ?, error_message = NULL WHERE id = ?",
                (attempt, execution_id),
            )
        return dict(self.one("SELECT * FROM automation_executions WHERE id = ?", (execution_id,)))

    def escalate_automation_instance(self, instance_id: int, *, reason: str, level: int = 1) -> dict[str, object]:
        now = _utcnow()
        escalation_key = f"esc-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_escalations (escalation_key, instance_id, level, reason, status, created_at)
                VALUES (?, ?, ?, ?, 'open', ?)
                """,
                (escalation_key, instance_id, level, reason, now),
            )
        row = self.one("SELECT * FROM automation_escalations WHERE escalation_key = ?", (escalation_key,))
        return dict(row)

    def automation_stats(self) -> dict[str, object]:
        engine = ProcessEngine()
        executions = [dict(r) for r in self.all("SELECT * FROM automation_executions")]
        tasks = [dict(r) for r in self.all("SELECT * FROM automation_tasks")]
        queues = [dict(r) for r in self.all("SELECT * FROM automation_queues")]
        metrics = engine.metrics.aggregate(executions=executions, tasks=tasks, queues=queues)
        return {
            "workflows": self.scalar("SELECT COUNT(*) FROM automation_workflow_definitions"),
            "instances": self.scalar("SELECT COUNT(*) FROM automation_process_instances"),
            "executions": self.scalar("SELECT COUNT(*) FROM automation_executions"),
            "tasks": self.scalar("SELECT COUNT(*) FROM automation_tasks"),
            "queues": self.scalar("SELECT COUNT(*) FROM automation_queues"),
            "events": self.scalar("SELECT COUNT(*) FROM automation_events"),
            **metrics,
        }

    def automation_monitoring(self) -> dict[str, object]:
        stats = self.automation_stats()
        bridge = AIIntegrationBridge()
        return {
            "stats": stats,
            "sla_policies": self.scalar("SELECT COUNT(*) FROM automation_sla_policies"),
            "pending_approvals": self.scalar("SELECT COUNT(*) FROM automation_approvals WHERE status = 'pending'"),
            "open_escalations": self.scalar("SELECT COUNT(*) FROM automation_escalations WHERE status = 'open'"),
            "pending_timers": self.scalar("SELECT COUNT(*) FROM automation_timers WHERE status = 'pending'"),
            "ai_hooks": list(bridge.resolve_hook_action(h) for h in ("assistant_chat", "knowledge_rag", "cognition_decision")),
        }

    def invoke_automation_ai_hook(self, *, hook_type: str, query: str, project_id: int | None) -> dict[str, object]:
        bridge = AIIntegrationBridge()
        return {
            "hook_type": hook_type,
            "endpoint": bridge.resolve_hook_action(hook_type),
            "context": bridge.build_ai_context(hook_type=hook_type, query=query, project_id=project_id),
        }

    def snapshot_automation_metrics(self) -> dict[str, object]:
        stats = self.automation_stats()
        now = _utcnow()
        key = f"snapshot-{now}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO automation_metrics_snapshots (snapshot_key, scope, metrics_json, created_at)
                VALUES (?, 'global', ?, ?)
                """,
                (key, _json(stats), now),
            )
        return {"snapshot_key": key, "metrics": stats}
