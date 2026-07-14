from __future__ import annotations

import json
from typing import Any

from .constants import (
    PARTNER_TYPE_ALIASES,
    PARTNER_TYPES,
    WORKFLOW_STEP_TEMPLATES,
    WORKFLOW_TYPES,
)


class TrustReputationEngine:
    def compute(self, *, profile: dict[str, object], orders: list[dict[str, object]], incidents: int = 0) -> dict[str, object]:
        completed = [order for order in orders if str(order.get("status")) == "completed"]
        total = len(orders) or 1
        completion_rate = round(len(completed) / total, 2)
        quality = int(profile.get("quality_score") or 70)
        trust = int(profile.get("trust_score") or 70)
        reliability = int(profile.get("reliability_score") or 75)
        response = float(profile.get("response_time_hours") or 24)
        satisfaction = int(profile.get("satisfaction_score") or 80)
        incident_penalty = min(30, incidents * 5)
        trust_score = max(20, min(100, trust + int(completion_rate * 15) - incident_penalty))
        quality_score = max(20, min(100, quality + len(completed) * 2 - incident_penalty))
        return {
            "trust_score": trust_score,
            "quality_score": quality_score,
            "completion_rate": completion_rate,
            "reliability": reliability,
            "avg_response_hours": response,
            "satisfaction": satisfaction,
            "incident_count": incidents,
        }

    def compute_project_trust(
        self,
        *,
        partner_matches: list[dict[str, object]],
        service_matches: list[dict[str, object]],
        workflow_progress: float,
    ) -> dict[str, object]:
        partner_avg = 0
        if partner_matches:
            partner_avg = sum(int(m.get("confidence") or 0) for m in partner_matches) / len(partner_matches)
        service_avg = 0
        if service_matches:
            service_avg = sum(int(m.get("confidence") or 0) for m in service_matches) / len(service_matches)
        base = (partner_avg + service_avg) / 2 if partner_matches or service_matches else 50
        score = int(min(100, base * 0.7 + workflow_progress * 0.3))
        return {"score": score, "subject_type": "project_ecosystem", "factors": {"partners": partner_avg, "services": service_avg}}


class WorkflowEngine:
    def template_for(self, workflow_type: str) -> list[dict[str, str]]:
        if workflow_type not in WORKFLOW_TYPES:
            workflow_type = "buy"
        return list(WORKFLOW_STEP_TEMPLATES.get(workflow_type, WORKFLOW_STEP_TEMPLATES["buy"]))

    def resolve_workflow_type(self, project: dict[str, object], goals: list[dict[str, object]]) -> str:
        goal_key = str(goals[0]["goal_key"]) if goals else str(project.get("project_type") or "buy")
        mapping = {
            "buy": "buy",
            "rent": "rent",
            "sell": "sell",
            "build": "build",
            "invest": "invest",
            "relocation": "relocation",
            "succession": "succession",
        }
        project_type = str(project.get("project_type") or "")
        if project_type == "build":
            return "build"
        if project_type == "invest":
            return "invest"
        return mapping.get(goal_key, mapping.get(project_type, "buy"))

    def advance_step(self, *, steps: list[dict[str, object]], current_step_key: str | None) -> dict[str, object]:
        ordered = sorted(steps, key=lambda row: str(row.get("step_key")))
        if not current_step_key:
            next_step = ordered[0] if ordered else None
            return {"current_step_key": next_step.get("step_key") if next_step else None, "completed": False}
        for index, step in enumerate(ordered):
            if str(step.get("step_key")) == current_step_key:
                if str(step.get("status")) != "completed":
                    return {"current_step_key": current_step_key, "completed": False}
                if index + 1 < len(ordered):
                    return {"current_step_key": ordered[index + 1].get("step_key"), "completed": False}
                return {"current_step_key": current_step_key, "completed": True}
        return {"current_step_key": current_step_key, "completed": False}

    def progress_percent(self, steps: list[dict[str, object]]) -> int:
        if not steps:
            return 0
        completed = sum(1 for step in steps if str(step.get("status")) == "completed")
        return int(round(completed / len(steps) * 100))


class NotificationEventEngine:
    def build_notifications(
        self,
        *,
        event: dict[str, object],
        user_id: int,
        channels: tuple[str, ...] = ("in_app",),
    ) -> list[dict[str, object]]:
        notifications: list[dict[str, object]] = []
        title = str(event.get("title"))
        event_type = str(event.get("event_type"))
        for channel in channels:
            notifications.append(
                {
                    "user_id": user_id,
                    "project_id": event.get("project_id"),
                    "event_id": event.get("id"),
                    "kind": event_type,
                    "title": title,
                    "body": self._body_for(event_type, title),
                    "channel": channel,
                    "status": "pending" if channel != "in_app" else "delivered",
                    "payload_json": event.get("payload_json") or "{}",
                }
            )
        return notifications

    def _body_for(self, event_type: str, title: str) -> str:
        mapping = {
            "match_refreshed": f"Nouvelles recommandations disponibles : {title}",
            "workflow_step_due": f"Échéance workflow : {title}",
            "service_order_created": f"Commande de service : {title}",
            "partner_assigned": f"Partenaire mobilisé : {title}",
        }
        return mapping.get(event_type, title)

    def reminder_for_step(self, *, step: dict[str, object], project_id: int, user_id: int) -> dict[str, object]:
        return {
            "project_id": project_id,
            "user_id": user_id,
            "event_type": "workflow_step_due",
            "title": f"Étape {step.get('title')} à traiter",
            "payload_json": json.dumps({"step_key": step.get("step_key")}, ensure_ascii=False),
        }


class ResourceOrchestrationEngine:
    def assemble(
        self,
        *,
        project: dict[str, object],
        partner_matches: list[dict[str, object]],
        service_matches: list[dict[str, object]],
        orders: list[dict[str, object]],
        interventions: list[dict[str, object]],
        resources: list[dict[str, object]],
        workflow_instance: dict[str, object] | None,
        workflow_steps: list[dict[str, object]],
    ) -> dict[str, object]:
        total_cost = sum(int(row.get("cost_estimate") or 0) for row in orders)
        actual_cost = sum(int(row.get("cost_actual") or 0) for row in interventions if row.get("cost_actual"))
        planned = [row for row in interventions if str(row.get("status")) in {"planned", "in_progress"}]
        return {
            "project_id": project.get("id"),
            "partners_engaged": len({m.get("partner_profile_id") for m in partner_matches if m.get("partner_profile_id")}),
            "services_recommended": len(service_matches),
            "active_orders": len([o for o in orders if str(o.get("status")) not in {"completed", "cancelled"}]),
            "interventions_planned": len(planned),
            "resources_linked": len(resources),
            "cost_summary": {
                "estimated": total_cost,
                "actual": actual_cost,
                "currency": project.get("currency") or "XAF",
            },
            "workflow": {
                "instance_id": workflow_instance.get("id") if workflow_instance else None,
                "status": workflow_instance.get("status") if workflow_instance else None,
                "current_step_key": workflow_instance.get("current_step_key") if workflow_instance else None,
                "progress_percent": WorkflowEngine().progress_percent(workflow_steps),
            },
            "planning": [
                {"type": "intervention", "title": row.get("title"), "scheduled_at": row.get("scheduled_at"), "status": row.get("status")}
                for row in sorted(interventions, key=lambda r: str(r.get("scheduled_at") or ""))[:10]
            ],
        }


def normalize_partner_type(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in PARTNER_TYPES:
        return normalized
    if normalized in PARTNER_TYPE_ALIASES:
        return PARTNER_TYPE_ALIASES[normalized]
    if normalized == "notaire":
        return "notary"
    raise ValueError(f"unsupported partner_type: {value}")


def parse_json_list(value: str | None) -> list[Any]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return []
    return parsed if isinstance(parsed, list) else []
