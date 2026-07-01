from __future__ import annotations

import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.workflow_automation.constants import (
    AI_HOOK_TYPES,
    APPROVAL_STATUSES,
    AUTOMATION_DOMAINS,
    DEFAULT_QUEUE_CAPACITY,
    DEFAULT_RETRY_MAX,
    DEFAULT_SLA_HOURS,
    EXECUTION_STATUSES,
    QUEUE_PRIORITIES,
    RULE_OPERATORS,
    TASK_STATUSES,
    WORKFLOW_STATUSES,
)
from lawim_v2.workflow_automation.engines import (
    AIIntegrationBridge,
    MetricsEngine,
    ProcessEngine,
    QueueManager,
    RetryEngine,
    RulesEngine,
    StateMachineEngine,
)
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramFPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v12(self) -> None:
        self.assertEqual(self.repository.schema_version(), 13)
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 13)

    def test_automation_tables_present(self) -> None:
        self.assertTrue(self.repository.automation_tables_present())

    def test_all_v12_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v11_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_automation_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM automation_workflow_definitions"), 6)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM automation_templates"), 6)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM automation_process_instances"), 1)

    def test_v11_to_v12_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / "v11.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES as V12

        for table in V12:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='11' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("automation_workflow_definitions", names)
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)


class ReleaseProgramFConstantsTests(LawimTestHarness):
    def test_automation_domains_immobilier(self) -> None:
        self.assertIn("achat", AUTOMATION_DOMAINS["immobilier"])

    def test_automation_domains_juridique(self) -> None:
        self.assertIn("contrats", AUTOMATION_DOMAINS["juridique"])

    def test_automation_domains_financement(self) -> None:
        self.assertIn("demande", AUTOMATION_DOMAINS["financement"])

    def test_automation_domains_administration(self) -> None:
        self.assertIn("support", AUTOMATION_DOMAINS["administration"])

    def test_automation_domains_ia(self) -> None:
        self.assertIn("assistant", AUTOMATION_DOMAINS["ia"])

    def test_workflow_statuses(self) -> None:
        self.assertIn("active", WORKFLOW_STATUSES)
        self.assertIn("draft", WORKFLOW_STATUSES)

    def test_execution_statuses(self) -> None:
        self.assertIn("running", EXECUTION_STATUSES)
        self.assertIn("completed", EXECUTION_STATUSES)

    def test_task_statuses(self) -> None:
        self.assertIn("pending", TASK_STATUSES)
        self.assertIn("escalated", TASK_STATUSES)

    def test_approval_statuses(self) -> None:
        self.assertIn("approved", APPROVAL_STATUSES)
        self.assertIn("rejected", APPROVAL_STATUSES)

    def test_queue_priorities(self) -> None:
        self.assertIn("critical", QUEUE_PRIORITIES)
        self.assertIn("normal", QUEUE_PRIORITIES)

    def test_rule_operators(self) -> None:
        self.assertIn("contains", RULE_OPERATORS)
        self.assertIn("eq", RULE_OPERATORS)

    def test_ai_hook_types(self) -> None:
        self.assertIn("knowledge_rag", AI_HOOK_TYPES)
        self.assertIn("assistant_chat", AI_HOOK_TYPES)

    def test_default_retry_max(self) -> None:
        self.assertEqual(DEFAULT_RETRY_MAX, 3)

    def test_default_sla_hours(self) -> None:
        self.assertEqual(DEFAULT_SLA_HOURS, 48)

    def test_default_queue_capacity(self) -> None:
        self.assertEqual(DEFAULT_QUEUE_CAPACITY, 500)


class ReleaseProgramFEngineTests(LawimTestHarness):
    def test_rules_engine_true(self) -> None:
        self.assertTrue(RulesEngine().evaluate("true", {}))

    def test_rules_engine_false(self) -> None:
        self.assertFalse(RulesEngine().evaluate("false", {}))

    def test_rules_engine_equality(self) -> None:
        self.assertTrue(RulesEngine().evaluate("$status == active", {"status": "active"}))

    def test_rules_engine_numeric_gt(self) -> None:
        self.assertTrue(RulesEngine().evaluate("$score > 10", {"score": 20}))

    def test_rules_engine_contains(self) -> None:
        self.assertTrue(RulesEngine().evaluate("contains('achat', text)", {"text": "guide achat immobilier"}))

    def test_state_machine_next_state(self) -> None:
        transitions = [
            {"from_state_key": "start", "to_state_key": "visite", "transition_key": "tr-1", "priority": 10, "condition_json": '{"expression": "true"}'},
        ]
        result = StateMachineEngine().next_state(
            current_state="start",
            transitions=transitions,
            context={},
            rules=RulesEngine(),
        )
        self.assertEqual(result["to_state_key"], "visite")

    def test_state_machine_no_transition(self) -> None:
        result = StateMachineEngine().next_state(
            current_state="end",
            transitions=[{"from_state_key": "start", "to_state_key": "visite", "priority": 0, "condition_json": "{}"}],
            context={},
            rules=RulesEngine(),
        )
        self.assertIsNone(result)

    def test_process_engine_advance(self) -> None:
        transitions = [
            {"from_state_key": "start", "to_state_key": "visite", "transition_key": "tr-adv", "priority": 10, "condition_json": '{"expression": "true"}'},
        ]
        payload = ProcessEngine().advance(current_state="start", transitions=transitions, context={})
        self.assertTrue(payload["advanced"])
        self.assertEqual(payload["to_state"], "visite")

    def test_process_engine_no_advance(self) -> None:
        payload = ProcessEngine().advance(current_state="done", transitions=[], context={})
        self.assertFalse(payload["advanced"])

    def test_queue_manager_priority_order(self) -> None:
        items = [{"priority": "low"}, {"priority": "critical"}, {"priority": "normal"}]
        ordered = QueueManager().enqueue_order(items)
        self.assertEqual(ordered[0]["priority"], "critical")

    def test_queue_manager_normal_rank(self) -> None:
        items = [{"priority": "normal"}, {"priority": "high"}]
        ordered = QueueManager().enqueue_order(items)
        self.assertEqual(ordered[0]["priority"], "high")

    def test_retry_engine_should_retry(self) -> None:
        self.assertTrue(RetryEngine().should_retry(1))
        self.assertFalse(RetryEngine().should_retry(DEFAULT_RETRY_MAX))

    def test_retry_engine_backoff(self) -> None:
        self.assertEqual(RetryEngine().schedule_backoff(1), 60)
        self.assertEqual(RetryEngine().schedule_backoff(2), 120)

    def test_metrics_engine_aggregate(self) -> None:
        metrics = MetricsEngine().aggregate(
            executions=[{"status": "completed", "duration_ms": 100}, {"status": "failed"}],
            tasks=[{"status": "pending"}],
            queues=[{"depth": 3}],
        )
        self.assertEqual(metrics["executions_total"], 2)
        self.assertEqual(metrics["executions_completed"], 1)
        self.assertEqual(metrics["queue_depth"], 3)

    def test_metrics_engine_success_rate(self) -> None:
        metrics = MetricsEngine().aggregate(
            executions=[{"status": "completed"}, {"status": "completed"}],
            tasks=[],
            queues=[],
        )
        self.assertEqual(metrics["success_rate"], 100.0)

    def test_ai_bridge_context(self) -> None:
        ctx = AIIntegrationBridge().build_ai_context(hook_type="knowledge_rag", query="compromis", project_id=1)
        self.assertEqual(ctx["hook_type"], "knowledge_rag")
        self.assertIn("knowledge_platform", ctx["sources"])

    def test_ai_bridge_resolve_assistant(self) -> None:
        endpoint = AIIntegrationBridge().resolve_hook_action("assistant_chat")
        self.assertIn("/api/v2/assistant/chat", endpoint)

    def test_ai_bridge_resolve_rag(self) -> None:
        endpoint = AIIntegrationBridge().resolve_hook_action("knowledge_rag")
        self.assertIn("/api/v2/knowledge/rag", endpoint)

    def test_ai_bridge_default_hook(self) -> None:
        endpoint = AIIntegrationBridge().resolve_hook_action("unknown_hook")
        self.assertIn("/api/v2/assistant/chat", endpoint)


class ReleaseProgramFRepositoryTests(LawimTestHarness):
    def test_list_automation_workflows(self) -> None:
        workflows = self.repository.list_automation_workflows()
        self.assertGreaterEqual(len(workflows), 6)

    def test_list_automation_workflows_by_domain(self) -> None:
        workflows = self.repository.list_automation_workflows(domain="immobilier")
        for row in workflows:
            self.assertEqual(row["domain"], "immobilier")

    def test_get_automation_workflow(self) -> None:
        wf = self.repository.get_automation_workflow("wf-immobilier-achat")
        self.assertEqual(wf["process_key"], "achat")

    def test_create_automation_workflow(self) -> None:
        doc = self.repository.create_automation_workflow(
            body={"domain": "technique", "process_key": "custom", "title": "Test workflow", "workflow_key": "wf-test-custom"},
        )
        self.assertEqual(doc["status"], "draft")

    def test_duplicate_automation_workflow(self) -> None:
        dup = self.repository.duplicate_automation_workflow("wf-immobilier-achat")
        self.assertIn("copie", str(dup["title"]))

    def test_activate_automation_workflow(self) -> None:
        created = self.repository.create_automation_workflow(
            body={"domain": "ia", "title": "Draft wf", "workflow_key": "wf-draft-activate"},
        )
        active = self.repository.set_automation_workflow_status(str(created["workflow_key"]), "active")
        self.assertEqual(active["status"], "active")

    def test_list_automation_templates(self) -> None:
        templates = self.repository.list_automation_templates()
        self.assertGreaterEqual(len(templates), 6)

    def test_create_automation_template(self) -> None:
        tpl = self.repository.create_automation_template(
            body={
                "workflow_key": "wf-immobilier-achat",
                "title": "Custom template",
                "domain": "immobilier",
                "template_key": "tpl-custom-test",
                "steps": [{"step_key": "start", "title": "Start"}],
            },
        )
        self.assertEqual(tpl["template_key"], "tpl-custom-test")

    def test_start_automation_instance(self) -> None:
        project_id = int(self.repository.one("SELECT id FROM projects LIMIT 1")["id"])
        inst = self.repository.start_automation_instance(workflow_key="wf-juridique-contrats", project_id=project_id)
        self.assertEqual(inst["status"], "running")

    def test_list_automation_instances(self) -> None:
        instances = self.repository.list_automation_instances()
        self.assertGreaterEqual(len(instances), 1)

    def test_advance_automation_instance(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        result = self.repository.advance_automation_instance(instance_id)
        self.assertIn("advanced", result)

    def test_list_automation_executions(self) -> None:
        executions = self.repository.list_automation_executions()
        self.assertGreaterEqual(len(executions), 1)

    def test_list_automation_tasks(self) -> None:
        tasks = self.repository.list_automation_tasks()
        self.assertGreaterEqual(len(tasks), 1)

    def test_complete_automation_task(self) -> None:
        task_id = int(self.repository.one("SELECT id FROM automation_tasks LIMIT 1")["id"])
        task = self.repository.complete_automation_task(task_id, result={"ok": True})
        self.assertEqual(task["status"], "completed")

    def test_list_automation_queues(self) -> None:
        queues = self.repository.list_automation_queues()
        self.assertGreaterEqual(len(queues), len(AUTOMATION_DOMAINS))

    def test_enqueue_automation_item(self) -> None:
        item = self.repository.enqueue_automation_item(queue_key="queue-immobilier", payload={"job": "test"}, priority="high")
        self.assertEqual(item["status"], "queued")

    def test_dequeue_automation_item(self) -> None:
        self.repository.enqueue_automation_item(queue_key="queue-juridique", payload={"job": "deq"}, priority="critical")
        item = self.repository.dequeue_automation_item("queue-juridique")
        self.assertIsNotNone(item)
        self.assertEqual(item["status"], "processing")

    def test_publish_automation_event(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        event = self.repository.publish_automation_event(event_type="custom_event", instance_id=instance_id, payload={"x": 1})
        self.assertEqual(event["event_type"], "custom_event")

    def test_list_automation_events(self) -> None:
        events = self.repository.list_automation_events()
        self.assertGreaterEqual(len(events), 1)

    def test_create_automation_approval(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        approval = self.repository.create_automation_approval(instance_id=instance_id, level=1)
        self.assertEqual(approval["status"], "pending")

    def test_decide_automation_approval(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        approval = self.repository.create_automation_approval(instance_id=instance_id, level=2)
        decided = self.repository.decide_automation_approval(int(approval["id"]), status="approved", note="ok")
        self.assertEqual(decided["status"], "approved")

    def test_list_automation_approvals(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        self.repository.create_automation_approval(instance_id=instance_id, level=1)
        approvals = self.repository.list_automation_approvals(instance_id=instance_id)
        self.assertGreaterEqual(len(approvals), 1)

    def test_list_automation_rules(self) -> None:
        rules = self.repository.list_automation_rules()
        self.assertGreaterEqual(len(rules), 1)

    def test_create_automation_rule(self) -> None:
        rule = self.repository.create_automation_rule(
            body={"title": "Test rule", "expression": "true", "domain": "general", "rule_key": "rule-test-repo"},
        )
        self.assertEqual(rule["rule_key"], "rule-test-repo")

    def test_evaluate_automation_rules(self) -> None:
        matched = self.repository.evaluate_automation_rules(context={"risk_score": 10})
        self.assertGreaterEqual(len(matched), 1)

    def test_list_automation_schedules(self) -> None:
        schedules = self.repository.list_automation_schedules()
        self.assertGreaterEqual(len(schedules), 1)

    def test_create_automation_timer(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        fire_at = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(microsecond=0).isoformat()
        timer = self.repository.create_automation_timer(instance_id=instance_id, fire_at=fire_at, action={"type": "remind"})
        self.assertEqual(timer["status"], "pending")

    def test_list_automation_timers(self) -> None:
        timers = self.repository.list_automation_timers()
        self.assertIsInstance(timers, list)

    def test_send_automation_notification(self) -> None:
        note = self.repository.send_automation_notification(title="Alert", body="Test", recipient_id=1, instance_id=None)
        self.assertEqual(note["status"], "sent")

    def test_list_automation_notifications(self) -> None:
        self.repository.send_automation_notification(title="List test", body="Body", recipient_id=1, instance_id=None)
        notifications = self.repository.list_automation_notifications()
        self.assertGreaterEqual(len(notifications), 1)

    def test_list_automation_history(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        history = self.repository.list_automation_history(instance_id=instance_id)
        self.assertIsInstance(history, list)

    def test_list_automation_audit(self) -> None:
        audit = self.repository.list_automation_audit()
        self.assertGreaterEqual(len(audit), 1)

    def test_automation_stats(self) -> None:
        stats = self.repository.automation_stats()
        self.assertGreaterEqual(stats["workflows"], 6)
        self.assertIn("success_rate", stats)

    def test_automation_monitoring(self) -> None:
        monitoring = self.repository.automation_monitoring()
        self.assertIn("stats", monitoring)
        self.assertIn("ai_hooks", monitoring)

    def test_invoke_automation_ai_hook(self) -> None:
        payload = self.repository.invoke_automation_ai_hook(hook_type="expert_search", query="achat", project_id=1)
        self.assertIn("endpoint", payload)

    def test_retry_automation_execution(self) -> None:
        execution_id = int(self.repository.one("SELECT id FROM automation_executions LIMIT 1")["id"])
        retried = self.repository.retry_automation_execution(execution_id)
        self.assertEqual(retried["status"], "running")

    def test_escalate_automation_instance(self) -> None:
        instance_id = int(self.repository.one("SELECT id FROM automation_process_instances LIMIT 1")["id"])
        esc = self.repository.escalate_automation_instance(instance_id, reason="SLA breach")
        self.assertEqual(esc["status"], "open")

    def test_snapshot_automation_metrics(self) -> None:
        snap = self.repository.snapshot_automation_metrics()
        self.assertIn("snapshot_key", snap)
        self.assertIn("metrics", snap)


class ReleaseProgramFApiTests(LawimTestHarness):
    def _project_id(self, token: str) -> int:
        return int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])

    def _instance_id(self, token: str) -> int:
        payload = self.invoke("/api/v2/workflows/instances", token=token).body_json()
        return int(payload["instances"][0]["id"])

    def test_workflow_definitions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/definitions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["workflows"]), 6)

    def test_workflow_definition_detail_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/definitions/wf-immobilier-achat", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("workflow", response.body_json())

    def test_workflow_templates_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/templates", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["templates"]), 6)

    def test_workflow_executions_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/executions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_instances_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/instances", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["instances"]), 1)

    def test_workflow_tasks_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/tasks", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_queues_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/queues", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_events_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/events", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_approvals_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/approvals", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_rules_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/rules", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_schedules_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/schedules", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_timers_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/timers", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_notifications_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/notifications", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_history_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        instance_id = self._instance_id(token)
        response = self.invoke(f"/api/v2/workflows/history?instance_id={instance_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_audit_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/workflows/audit", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_metrics_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/metrics", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("metrics", response.body_json())

    def test_workflow_monitoring_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/monitoring", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_create_definition_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/workflows/definitions",
            method="POST",
            token=token,
            body={"domain": "administration", "title": "API workflow", "process_key": "incidents"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_duplicate_definition_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/workflows/definitions/wf-immobilier-vente/duplicate", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_activate_definition_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        created = self.invoke(
            "/api/v2/workflows/definitions",
            method="POST",
            token=token,
            body={"domain": "ia", "title": "Activate me", "workflow_key": "wf-api-activate"},
        )
        wf_key = str(created.body_json()["workflow"]["workflow_key"])
        response = self.invoke(f"/api/v2/workflows/definitions/{wf_key}/activate", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.body_json()["workflow"]["status"], "active")

    def test_workflow_deactivate_definition_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/workflows/definitions/wf-immobilier-achat/deactivate", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_create_template_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/workflows/templates",
            method="POST",
            token=token,
            body={
                "workflow_key": "wf-financement-demande",
                "title": "API template",
                "domain": "financement",
                "template_key": "tpl-api-test",
            },
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_start_instance_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/workflows/instances",
            method="POST",
            token=token,
            body={"workflow_key": "wf-admin-support", "project_id": project_id, "context": {"source": "api"}},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_advance_instance_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        instance_id = self._instance_id(token)
        response = self.invoke(f"/api/v2/workflows/instances/{instance_id}/advance", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_complete_task_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        task_id = int(self.invoke("/api/v2/workflows/tasks", token=token).body_json()["tasks"][0]["id"])
        response = self.invoke(f"/api/v2/workflows/tasks/{task_id}/complete", method="POST", token=token, body={"result": {"done": True}})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_enqueue_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/workflows/queues/enqueue",
            method="POST",
            token=token,
            body={"queue_key": "queue-financement", "payload": {"task": "review"}, "priority": "high"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_dequeue_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke(
            "/api/v2/workflows/queues/enqueue",
            method="POST",
            token=token,
            body={"queue_key": "queue-ia", "payload": {"task": "dequeue"}, "priority": "normal"},
        )
        response = self.invoke("/api/v2/workflows/queues/dequeue", method="POST", token=token, body={"queue_key": "queue-ia"})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_publish_event_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        instance_id = self._instance_id(token)
        response = self.invoke(
            "/api/v2/workflows/events",
            method="POST",
            token=token,
            body={"event_type": "api_event", "instance_id": instance_id, "payload": {"k": "v"}},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_create_approval_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        instance_id = self._instance_id(token)
        response = self.invoke(
            "/api/v2/workflows/approvals",
            method="POST",
            token=token,
            body={"instance_id": instance_id, "level": 1},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_decide_approval_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        instance_id = self._instance_id(token)
        created = self.invoke(
            "/api/v2/workflows/approvals",
            method="POST",
            token=token,
            body={"instance_id": instance_id, "level": 3},
        )
        approval_id = int(created.body_json()["approval"]["id"])
        response = self.invoke(
            f"/api/v2/workflows/approvals/{approval_id}/decide",
            method="POST",
            token=token,
            body={"status": "approved", "note": "via api"},
        )
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_create_rule_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/workflows/rules",
            method="POST",
            token=token,
            body={"title": "API rule", "expression": "true", "domain": "general", "rule_key": "rule-api-test"},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_evaluate_rules_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke(
            "/api/v2/workflows/rules/evaluate",
            method="POST",
            token=token,
            body={"context": {"risk_score": 5}},
        )
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("matched", response.body_json())

    def test_workflow_create_timer_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        instance_id = self._instance_id(token)
        fire_at = (datetime.now(timezone.utc) + timedelta(hours=2)).replace(microsecond=0).isoformat()
        response = self.invoke(
            "/api/v2/workflows/timers",
            method="POST",
            token=token,
            body={"instance_id": instance_id, "fire_at": fire_at, "action": {"type": "notify"}},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_send_notification_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke(
            "/api/v2/workflows/notifications",
            method="POST",
            token=token,
            body={"title": "Workflow alert", "body": "Instance update", "recipient_id": 1},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_metrics_snapshot_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        response = self.invoke("/api/v2/workflows/metrics/snapshot", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_retry_execution_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        execution_id = int(self.invoke("/api/v2/workflows/executions", token=token).body_json()["executions"][0]["id"])
        response = self.invoke(f"/api/v2/workflows/executions/{execution_id}/retry", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_workflow_escalate_api(self) -> None:
        token = self.login(email="admin@lawim.local")
        instance_id = self._instance_id(token)
        response = self.invoke(
            "/api/v2/workflows/escalations",
            method="POST",
            token=token,
            body={"instance_id": instance_id, "reason": "blocked", "level": 2},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)

    def test_workflow_ai_hook_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = self._project_id(token)
        response = self.invoke(
            "/api/v2/workflows/ai-hook",
            method="POST",
            token=token,
            body={"hook_type": "cognition_decision", "query": "next step", "project_id": project_id},
        )
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("endpoint", response.body_json())

    def test_ecosystem_workflows_compat_api(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(response.body_json()["workflows"]), 8)


class ReleaseProgramFUiTests(LawimTestHarness):
    def test_index_has_workflow_automation_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Workflow automation", html.body_text())

    def test_app_js_references_workflow_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/workflows/metrics", js.body_text())
        self.assertIn("refreshWorkflowAdmin", js.body_text())


class ReleaseProgramFHealthTests(LawimTestHarness):
    def test_health_schema_v12(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 13)

    def test_migration_strategy_v12(self) -> None:
        self.assertEqual(migration_strategy_profile()["schema_version"], 13)

    def test_metrics_include_automation_counters(self) -> None:
        token = self.login(email="agent@lawim.local")
        self.invoke("/api/v2/workflows/definitions", token=token)
        admin = self.login(email="admin@lawim.local")
        self.invoke(
            "/api/v2/workflows/instances",
            method="POST",
            token=admin,
            body={"workflow_key": "wf-ia-assistant"},
        )
        metrics = self.invoke("/api/metrics", token=admin)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("workflow_definitions_total", 0), 1)
        self.assertGreaterEqual(snapshot.get("automation_started_total", 0), 1)


class ReleaseProgramFV12TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v12_table_workflow_definitions(self) -> None:
        self.assertIn("automation_workflow_definitions", self._table_names())

    def test_v12_table_templates(self) -> None:
        self.assertIn("automation_templates", self._table_names())

    def test_v12_table_process_instances(self) -> None:
        self.assertIn("automation_process_instances", self._table_names())

    def test_v12_table_executions(self) -> None:
        self.assertIn("automation_executions", self._table_names())

    def test_v12_table_states(self) -> None:
        self.assertIn("automation_states", self._table_names())

    def test_v12_table_transitions(self) -> None:
        self.assertIn("automation_transitions", self._table_names())

    def test_v12_table_tasks(self) -> None:
        self.assertIn("automation_tasks", self._table_names())

    def test_v12_table_queues(self) -> None:
        self.assertIn("automation_queues", self._table_names())

    def test_v12_table_queue_items(self) -> None:
        self.assertIn("automation_queue_items", self._table_names())

    def test_v12_table_events(self) -> None:
        self.assertIn("automation_events", self._table_names())

    def test_v12_table_schedules(self) -> None:
        self.assertIn("automation_schedules", self._table_names())

    def test_v12_table_timers(self) -> None:
        self.assertIn("automation_timers", self._table_names())

    def test_v12_table_retries(self) -> None:
        self.assertIn("automation_retries", self._table_names())

    def test_v12_table_escalations(self) -> None:
        self.assertIn("automation_escalations", self._table_names())

    def test_v12_table_approvals(self) -> None:
        self.assertIn("automation_approvals", self._table_names())

    def test_v12_table_rules(self) -> None:
        self.assertIn("automation_rules", self._table_names())

    def test_v12_table_rule_bindings(self) -> None:
        self.assertIn("automation_rule_bindings", self._table_names())

    def test_v12_table_notifications(self) -> None:
        self.assertIn("automation_notifications", self._table_names())

    def test_v12_table_audit_log(self) -> None:
        self.assertIn("automation_audit_log", self._table_names())

    def test_v12_table_history(self) -> None:
        self.assertIn("automation_history", self._table_names())

    def test_v12_table_sla_policies(self) -> None:
        self.assertIn("automation_sla_policies", self._table_names())

    def test_v12_table_metrics_snapshots(self) -> None:
        self.assertIn("automation_metrics_snapshots", self._table_names())


class ReleaseProgramFDomainCoverageTests(LawimTestHarness):
    def test_all_domains_have_queues(self) -> None:
        for domain in AUTOMATION_DOMAINS:
            count = self.repository.scalar("SELECT COUNT(*) FROM automation_queues WHERE domain = ?", (domain,))
            self.assertGreaterEqual(count, 1)

    def test_seeded_workflows_cover_domains(self) -> None:
        domains = {row["domain"] for row in self.repository.all("SELECT domain FROM automation_workflow_definitions")}
        for expected in ("immobilier", "juridique", "financement", "administration", "ia"):
            self.assertIn(expected, domains)

    def test_seeded_states_per_workflow(self) -> None:
        count = self.repository.scalar(
            "SELECT COUNT(*) FROM automation_states WHERE workflow_key = 'wf-immobilier-achat'"
        )
        self.assertGreaterEqual(count, 5)

    def test_seeded_transitions_exist(self) -> None:
        count = self.repository.scalar(
            "SELECT COUNT(*) FROM automation_transitions WHERE workflow_key = 'wf-financement-demande'"
        )
        self.assertGreaterEqual(count, 4)

    def test_sla_policies_seeded(self) -> None:
        count = self.repository.scalar("SELECT COUNT(*) FROM automation_sla_policies")
        self.assertGreaterEqual(count, 6)
