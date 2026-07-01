from __future__ import annotations

from typing import Callable


def partner_profile_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "organization_id": row.get("organization_id"),
        "partner_type": row.get("partner_type"),
        "display_name": row.get("display_name"),
        "legal_name": row.get("legal_name"),
        "description": row.get("description"),
        "status": row.get("status"),
        "quality_score": row.get("quality_score"),
        "trust_score": row.get("trust_score"),
        "completion_rate": row.get("completion_rate"),
        "reliability_score": row.get("reliability_score"),
        "response_time_hours": row.get("response_time_hours"),
        "satisfaction_score": row.get("satisfaction_score"),
        "incident_count": row.get("incident_count"),
        "specialties": row.get("specialties") or [],
        "zones": row.get("zones") or [],
        "skills": row.get("skills") or [],
        "certifications": row.get("certifications") or [],
        "availability_status": row.get("availability_status"),
        "sla": row.get("sla"),
        "services": row.get("services") or [],
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
    }


def service_catalog_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "service_key": row.get("service_key"),
        "category": row.get("category"),
        "title": row.get("title"),
        "description": row.get("description"),
        "conditions": row.get("conditions"),
        "pricing": {
            "min": row.get("indicative_price_min"),
            "max": row.get("indicative_price_max"),
            "currency": row.get("currency"),
        },
        "estimated_duration_days": row.get("estimated_duration_days"),
        "documents": row.get("documents") or [],
        "prerequisites": row.get("prerequisites") or [],
        "deliverables": row.get("deliverables") or [],
        "status": row.get("status"),
        "partners": row.get("partners") or [],
    }


def match_result_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "match_type": row.get("match_type"),
        "score": row.get("score"),
        "confidence": row.get("confidence"),
        "priority": row.get("priority"),
        "rationale": row.get("rationale") or [],
        "status": row.get("status"),
        "partner_profile_id": row.get("partner_profile_id"),
        "service_catalog_id": row.get("service_catalog_id"),
        "partner": partner_profile_dto(row["partner"]) if row.get("partner") else None,
        "service": service_catalog_dto(row["service"]) if row.get("service") else None,
    }


def workflow_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "workflow_key": row.get("workflow_key"),
        "workflow_type": row.get("workflow_type"),
        "title": row.get("title"),
        "description": row.get("description"),
        "status": row.get("status"),
        "steps": row.get("steps") or [],
    }


def workflow_instance_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "workflow_id": row.get("workflow_id"),
        "status": row.get("status"),
        "current_step_key": row.get("current_step_key"),
        "progress_percent": row.get("progress_percent"),
        "started_at": row.get("started_at"),
        "completed_at": row.get("completed_at"),
        "workflow": workflow_dto(row["workflow"]) if row.get("workflow") else None,
        "instance_steps": row.get("instance_steps") or [],
    }


def reputation_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "subject_type": row.get("subject_type"),
        "subject_id": row.get("subject_id"),
        "trust_score": row.get("trust_score"),
        "quality_score": row.get("quality_score"),
        "completion_rate": row.get("completion_rate"),
        "reliability": row.get("reliability"),
        "avg_response_hours": row.get("avg_response_hours"),
        "satisfaction": row.get("satisfaction"),
        "incident_count": row.get("incident_count"),
        "computed_at": row.get("computed_at"),
    }


def ecosystem_notification_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "kind": row.get("kind"),
        "title": row.get("title"),
        "body": row.get("body"),
        "channel": row.get("channel"),
        "status": row.get("status"),
        "scheduled_at": row.get("scheduled_at"),
        "delivered_at": row.get("delivered_at"),
        "created_at": row.get("created_at"),
    }


def ecosystem_event_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "user_id": row.get("user_id"),
        "event_type": row.get("event_type"),
        "title": row.get("title"),
        "occurred_at": row.get("occurred_at"),
        "created_at": row.get("created_at"),
    }


def service_order_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "service_catalog_id": row.get("service_catalog_id"),
        "partner_profile_id": row.get("partner_profile_id"),
        "status": row.get("status"),
        "cost_estimate": row.get("cost_estimate"),
        "currency": row.get("currency"),
        "scheduled_at": row.get("scheduled_at"),
        "completed_at": row.get("completed_at"),
        "created_at": row.get("created_at"),
    }


def intervention_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "project_id": row.get("project_id"),
        "partner_profile_id": row.get("partner_profile_id"),
        "service_order_id": row.get("service_order_id"),
        "intervention_type": row.get("intervention_type"),
        "title": row.get("title"),
        "status": row.get("status"),
        "scheduled_at": row.get("scheduled_at"),
        "completed_at": row.get("completed_at"),
        "cost_actual": row.get("cost_actual"),
        "currency": row.get("currency"),
    }


def matching_payload_dto(payload: dict[str, object]) -> dict[str, object]:
    return {
        "goal_key": payload.get("goal_key"),
        "journey_status": payload.get("journey_status"),
        "partner_matches": payload.get("partner_matches") or [],
        "service_matches": payload.get("service_matches") or [],
    }
