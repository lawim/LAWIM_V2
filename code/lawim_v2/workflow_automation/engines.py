from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from typing import Any

from .constants import DEFAULT_RETRY_MAX, DEFAULT_SLA_HOURS, RULE_OPERATORS


class RulesEngine:
    def evaluate(self, expression: str, context: dict[str, Any]) -> bool:
        expr = expression.strip()
        if not expr or expr == "true":
            return True
        if expr == "false":
            return False
        for op in ("==", "!=", ">=", "<=", ">", "<"):
            if op in expr:
                left, right = [part.strip() for part in expr.split(op, 1)]
                lv = self._resolve(left, context)
                rv = self._resolve(right, context)
                if op == "==":
                    return str(lv) == str(rv)
                if op == "!=":
                    return str(lv) != str(rv)
                try:
                    lv_num, rv_num = float(lv), float(rv)
                except (TypeError, ValueError):
                    return False
                if op == ">=":
                    return lv_num >= rv_num
                if op == "<=":
                    return lv_num <= rv_num
                if op == ">":
                    return lv_num > rv_num
                if op == "<":
                    return lv_num < rv_num
        if expr.startswith("contains(") and expr.endswith(")"):
            inner = expr[len("contains(") : -1]
            needle, haystack_key = [p.strip().strip("'\"") for p in inner.split(",", 1)]
            haystack = str(context.get(haystack_key.strip(), ""))
            return needle in haystack
        return bool(context.get(expr.lstrip("$")))

    def _resolve(self, token: str, context: dict[str, Any]) -> Any:
        token = token.strip().strip("'\"")
        if token.startswith("$"):
            return context.get(token[1:], "")
        return token


class StateMachineEngine:
    def next_state(
        self,
        *,
        current_state: str,
        transitions: list[dict[str, object]],
        context: dict[str, Any],
        rules: RulesEngine,
    ) -> dict[str, object] | None:
        candidates = [
            t
            for t in sorted(transitions, key=lambda row: int(row.get("priority", 0)), reverse=True)
            if str(t.get("from_state_key")) == current_state
        ]
        for transition in candidates:
            condition = transition.get("condition_json")
            if isinstance(condition, str):
                try:
                    condition = json.loads(condition)
                except json.JSONDecodeError:
                    condition = {}
            expression = str((condition or {}).get("expression") or "true")
            if rules.evaluate(expression, context):
                return transition
        return None


class TaskEngine:
    def build_task(self, *, title: str, task_type: str, payload: dict[str, Any]) -> dict[str, object]:
        return {"title": title, "task_type": task_type, "payload": payload, "status": "pending"}

    def can_complete(self, status: str) -> bool:
        return status in {"pending", "assigned", "in_progress"}


class QueueManager:
    def enqueue_order(self, items: list[dict[str, object]]) -> list[dict[str, object]]:
        priority_rank = {"critical": 4, "high": 3, "normal": 2, "low": 1}

        def rank(row: dict[str, object]) -> int:
            return priority_rank.get(str(row.get("priority", "normal")), 2)

        return sorted(items, key=rank, reverse=True)


class SchedulerEngine:
    def next_daily_run(self, *, from_time: datetime | None = None) -> str:
        base = from_time or datetime.now(timezone.utc)
        nxt = base + timedelta(days=1)
        return nxt.replace(microsecond=0).isoformat()


class RetryEngine:
    def schedule_backoff(self, attempt: int, *, base_seconds: int = 60) -> int:
        return min(base_seconds * (2 ** max(0, attempt - 1)), 3600)

    def should_retry(self, attempt: int, *, max_attempts: int = DEFAULT_RETRY_MAX) -> bool:
        return attempt < max_attempts


class TimeoutEngine:
    def is_sla_breached(self, *, started_at: str, target_hours: int = DEFAULT_SLA_HOURS) -> bool:
        try:
            started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        except ValueError:
            return False
        deadline = started + timedelta(hours=target_hours)
        return datetime.now(timezone.utc) >= deadline


class EscalationEngine:
    def next_level(self, current: int) -> int:
        return min(current + 1, 5)


class ApprovalEngine:
    def all_approved(self, approvals: list[dict[str, object]], *, required_levels: int) -> bool:
        approved = {int(a.get("level", 0)) for a in approvals if str(a.get("status")) == "approved"}
        return all(level in approved for level in range(1, required_levels + 1))


class NotificationEngine:
    def compose(self, *, title: str, body: str, channel: str = "in_app") -> dict[str, object]:
        return {"title": title, "body": body, "channel": channel, "status": "pending"}


class AuditEngine:
    def entry(self, *, action: str, resource_type: str, resource_id: int | None, detail: dict[str, Any]) -> dict[str, object]:
        key = hashlib.sha256(f"{action}:{resource_type}:{resource_id}:{json.dumps(detail, sort_keys=True)}".encode()).hexdigest()[:16]
        return {"audit_key": f"audit-{key}", "action": action, "resource_type": resource_type, "resource_id": resource_id, "detail": detail}


class MetricsEngine:
    def aggregate(
        self,
        *,
        executions: list[dict[str, object]],
        tasks: list[dict[str, object]],
        queues: list[dict[str, object]],
    ) -> dict[str, object]:
        completed = [e for e in executions if str(e.get("status")) == "completed"]
        failed = [e for e in executions if str(e.get("status")) == "failed"]
        durations = [int(e.get("duration_ms", 0)) for e in completed if e.get("duration_ms")]
        avg_ms = round(sum(durations) / len(durations), 2) if durations else 0
        total_exec = len(executions) or 1
        return {
            "executions_total": len(executions),
            "executions_completed": len(completed),
            "executions_failed": len(failed),
            "success_rate": round(len(completed) / total_exec * 100, 2),
            "avg_duration_ms": avg_ms,
            "tasks_open": len([t for t in tasks if str(t.get("status")) not in {"completed", "failed"}]),
            "queue_depth": sum(int(q.get("depth", 0)) for q in queues),
            "throughput": len(completed),
        }


class ProcessEngine:
    def __init__(self) -> None:
        self.rules = RulesEngine()
        self.state_machine = StateMachineEngine()
        self.tasks = TaskEngine()
        self.queues = QueueManager()
        self.scheduler = SchedulerEngine()
        self.retry = RetryEngine()
        self.timeout = TimeoutEngine()
        self.escalation = EscalationEngine()
        self.approval = ApprovalEngine()
        self.notifications = NotificationEngine()
        self.audit = AuditEngine()
        self.metrics = MetricsEngine()

    def advance(
        self,
        *,
        current_state: str,
        transitions: list[dict[str, object]],
        context: dict[str, Any],
    ) -> dict[str, object]:
        transition = self.state_machine.next_state(
            current_state=current_state,
            transitions=transitions,
            context=context,
            rules=self.rules,
        )
        if transition is None:
            return {"advanced": False, "current_state": current_state}
        return {
            "advanced": True,
            "from_state": current_state,
            "to_state": str(transition.get("to_state_key")),
            "transition_key": transition.get("transition_key"),
        }


class AIIntegrationBridge:
    """Hooks vers Programs D/E/C — sans LLM obligatoire."""

    def build_ai_context(self, *, hook_type: str, query: str, project_id: int | None) -> dict[str, object]:
        return {
            "hook_type": hook_type,
            "query": query,
            "project_id": project_id,
            "sources": ["maintenance", "knowledge_platform", "cognition", "source_intelligence"],
        }

    def resolve_hook_action(self, hook_type: str) -> str:
        mapping = {
            "maintenance_message": "/api/v2/maintenance/messages",
            "knowledge_rag": "/api/v2/knowledge/rag",
            "cognition_decision": "/api/v2/decisions",
            "expert_search": "/api/v2/knowledge/search",
            "enrichment": "/api/v2/knowledge/import",
            "recommendation": "/api/v2/next-actions",
        }
        return mapping.get(hook_type, "/api/v2/maintenance/messages")
