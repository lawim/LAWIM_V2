from __future__ import annotations


def role_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "role_key": row.get("role_key"),
        "name": row.get("name"),
        "description": row.get("description"),
        "status": row.get("status"),
    }


def permission_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "permission_key": row.get("permission_key"),
        "name": row.get("name"),
        "resource": row.get("resource"),
        "action": row.get("action"),
    }


def user_role_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "user_id": row.get("user_id"),
        "role_id": row.get("role_id"),
        "assigned_at": row.get("assigned_at"),
        "expires_at": row.get("expires_at"),
    }


def group_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "group_key": row.get("group_key"),
        "name": row.get("name"),
        "description": row.get("description"),
        "organization_id": row.get("organization_id"),
        "status": row.get("status"),
    }


def team_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "team_key": row.get("team_key"),
        "name": row.get("name"),
        "description": row.get("description"),
        "organization_id": row.get("organization_id"),
        "leader_user_id": row.get("leader_user_id"),
        "status": row.get("status"),
    }


def access_policy_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "policy_key": row.get("policy_key"),
        "name": row.get("name"),
        "policy_type": row.get("policy_type"),
        "status": row.get("status"),
    }


def user_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "email": row.get("email"),
        "display_name": row.get("display_name") or row.get("full_name"),
        "role": row.get("role"),
        "organization_id": row.get("organization_id"),
        "status": row.get("status"),
    }


def session_record_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "session_key": row.get("session_key"),
        "user_id": row.get("user_id"),
        "device_id": row.get("device_id"),
        "ip_address": row.get("ip_address"),
        "status": row.get("status"),
        "started_at": row.get("started_at"),
        "expires_at": row.get("expires_at"),
        "revoked_at": row.get("revoked_at"),
    }


def device_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "device_key": row.get("device_key"),
        "user_id": row.get("user_id"),
        "device_type": row.get("device_type"),
        "device_name": row.get("device_name"),
        "trust_level": row.get("trust_level"),
        "status": row.get("status"),
        "last_seen_at": row.get("last_seen_at"),
    }


def api_key_dto(row: dict[str, object], *, include_secret: bool = False) -> dict[str, object]:
    payload = {
        "id": row.get("id"),
        "api_key_key": row.get("api_key_key"),
        "user_id": row.get("user_id"),
        "organization_id": row.get("organization_id"),
        "name": row.get("name"),
        "key_prefix": row.get("key_prefix"),
        "status": row.get("status"),
        "expires_at": row.get("expires_at"),
        "last_used_at": row.get("last_used_at"),
        "created_at": row.get("created_at"),
    }
    if include_secret and row.get("secret"):
        payload["secret"] = row.get("secret")
    return payload


def route_policy_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "route_key": row.get("route_key"),
        "path_pattern": row.get("path_pattern"),
        "policy_type": row.get("policy_type"),
        "status": row.get("status"),
    }


def audit_trail_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "entry_key": row.get("entry_key"),
        "event_type": row.get("event_type"),
        "actor_user_id": row.get("actor_user_id"),
        "resource_type": row.get("resource_type"),
        "resource_id": row.get("resource_id"),
        "action": row.get("action"),
        "severity": row.get("severity"),
        "checksum": row.get("checksum"),
        "created_at": row.get("created_at"),
    }


def audit_event_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "event_key": row.get("event_key"),
        "action": row.get("action"),
        "severity": row.get("severity"),
        "message": row.get("message"),
        "created_at": row.get("created_at"),
    }


def compliance_policy_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "policy_key": row.get("policy_key"),
        "name": row.get("name"),
        "framework": row.get("framework"),
        "status": row.get("status"),
        "effective_at": row.get("effective_at"),
    }


def compliance_consent_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "consent_key": row.get("consent_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "consent_type": row.get("consent_type"),
        "status": row.get("status"),
        "granted_at": row.get("granted_at"),
        "revoked_at": row.get("revoked_at"),
    }


def retention_rule_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "rule_key": row.get("rule_key"),
        "name": row.get("name"),
        "resource_type": row.get("resource_type"),
        "retention_days": row.get("retention_days"),
        "action_on_expiry": row.get("action_on_expiry"),
        "status": row.get("status"),
    }


def deletion_request_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "request_key": row.get("request_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "deletion_type": row.get("deletion_type"),
        "status": row.get("status"),
        "requested_at": row.get("requested_at"),
        "completed_at": row.get("completed_at"),
    }


def privacy_export_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "export_key": row.get("export_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "format": row.get("format"),
        "status": row.get("status"),
        "requested_at": row.get("requested_at"),
        "completed_at": row.get("completed_at"),
    }


def privacy_erasure_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "request_key": row.get("request_key"),
        "user_id": row.get("user_id"),
        "contact_id": row.get("contact_id"),
        "status": row.get("status"),
        "requested_at": row.get("requested_at"),
        "completed_at": row.get("completed_at"),
    }


def risk_signal_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "signal_key": row.get("signal_key"),
        "user_id": row.get("user_id"),
        "signal_type": row.get("signal_type"),
        "severity": row.get("severity"),
        "score_delta": row.get("score_delta"),
        "status": row.get("status"),
        "detected_at": row.get("detected_at"),
    }


def risk_score_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "user_id": row.get("user_id"),
        "score_key": row.get("score_key"),
        "score": row.get("score"),
        "level": row.get("level"),
        "computed_at": row.get("computed_at"),
    }


def risk_alert_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "alert_key": row.get("alert_key"),
        "user_id": row.get("user_id"),
        "signal_id": row.get("signal_id"),
        "level": row.get("level"),
        "title": row.get("title"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "resolved_at": row.get("resolved_at"),
    }


def incident_dto(row: dict[str, object]) -> dict[str, object]:
    return {
        "id": row.get("id"),
        "incident_key": row.get("incident_key"),
        "title": row.get("title"),
        "severity": row.get("severity"),
        "status": row.get("status"),
        "reported_by": row.get("reported_by"),
        "assigned_to": row.get("assigned_to"),
        "opened_at": row.get("opened_at"),
        "resolved_at": row.get("resolved_at"),
    }


def dashboard_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"dashboard": payload}


def analytics_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"analytics": payload}


def stats_dto(payload: dict[str, object]) -> dict[str, object]:
    return {"stats": payload}
