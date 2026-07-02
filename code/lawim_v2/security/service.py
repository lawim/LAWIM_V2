from __future__ import annotations

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as sdto
from .engines import SecurityPlatformEngine


class IamService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = SecurityPlatformEngine()

    def list_roles(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_iam_roles(**kwargs)

    def create_role(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_iam_role(**kwargs)

    def update_role(self, role_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.update_iam_role(role_id, **kwargs)

    def list_permissions(self) -> list[dict[str, object]]:
        return self.repository.list_iam_permissions()

    def create_permission(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_iam_permission(**kwargs)

    def assign_user_role(self, **kwargs: object) -> dict[str, object]:
        return self.repository.assign_user_role(**kwargs)

    def list_policies(self) -> list[dict[str, object]]:
        return self.repository.list_iam_access_policies()

    def create_policy(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_iam_access_policy(**kwargs)

    def list_users(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_security_users(**kwargs)

    def get_user(self, user_id: int) -> dict[str, object]:
        return self.repository.get_security_user(user_id)

    def evaluate_access(
        self,
        *,
        user_id: int,
        policy_id: int,
        attributes: dict[str, object] | None = None,
    ) -> dict[str, object]:
        policy_row = self.repository.one("SELECT * FROM iam_access_policies WHERE id = ?", (policy_id,))
        roles = self.repository.list_user_roles(user_id=user_id)
        role_keys = [str(r.get("role_key") or "") for r in roles]
        perm_rows = self.repository.all(
            """
            SELECT p.* FROM iam_permissions p
            JOIN iam_role_permissions rp ON rp.permission_id = p.id
            JOIN iam_user_roles ur ON ur.role_id = rp.role_id
            WHERE ur.user_id = ?
            """,
            (user_id,),
        )
        grants = self.engine.permission.build_grants(permissions=[dict(p) for p in perm_rows])
        allowed = self.engine.permission.evaluate(
            role_keys=role_keys,
            permission_grants=grants,
            policy=dict(policy_row) if policy_row else {},
            attributes=attributes,
        )
        return {"allowed": allowed, "role_keys": role_keys, "grants": grants}


class AccessService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_sessions(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_access_session_records(**kwargs)

    def record_session(self, **kwargs: object) -> dict[str, object]:
        return self.repository.record_access_session(**kwargs)

    def revoke_session(self, session_record_id: int) -> dict[str, object]:
        return self.repository.revoke_session_record(session_record_id)

    def list_devices(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_access_devices(**kwargs)

    def register_device(self, **kwargs: object) -> dict[str, object]:
        return self.repository.register_access_device(**kwargs)

    def list_api_keys(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_access_api_keys(**kwargs)

    def create_api_key(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_api_key(**kwargs)

    def revoke_api_key(self, api_key_id: int) -> dict[str, object]:
        return self.repository.revoke_api_key(api_key_id)

    def list_route_policies(self) -> list[dict[str, object]]:
        return self.repository.list_access_route_policies()


class AuditService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def record(self, **kwargs: object) -> dict[str, object]:
        return self.repository.record_audit_trail(**kwargs)

    def list_trail(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_audit_trail(**kwargs)

    def verify_chain(self, *, limit: int = 100) -> dict[str, object]:
        return self.repository.verify_audit_trail(limit=limit)


class ComplianceService:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.engine = SecurityPlatformEngine()

    def list_policies(self) -> list[dict[str, object]]:
        return self.repository.list_compliance_policies()

    def list_consents(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_compliance_consents(**kwargs)

    def grant_consent(self, **kwargs: object) -> dict[str, object]:
        return self.repository.grant_compliance_consent(**kwargs)

    def list_retention_rules(self) -> list[dict[str, object]]:
        return self.repository.list_compliance_retention_rules()

    def create_deletion_request(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_compliance_deletion_request(**kwargs)

    def list_deletion_requests(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_compliance_deletion_requests(**kwargs)

    def check_policy(self, *, policy_id: int, context: dict[str, object]) -> dict[str, object]:
        row = self.repository.one("SELECT * FROM compliance_policies WHERE id = ?", (policy_id,))
        if row is None:
            return {"compliant": False, "violations": ["policy_not_found"]}
        return self.engine.compliance.check_policy(policy=dict(row), context=context)


class PrivacyService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_exports(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_privacy_exports(**kwargs)

    def create_export(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_privacy_export(**kwargs)

    def list_erasure_requests(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_privacy_erasure_requests(**kwargs)

    def create_erasure_request(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_privacy_erasure_request(**kwargs)


class RiskService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_signals(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_risk_signals(**kwargs)

    def record_signal(self, **kwargs: object) -> dict[str, object]:
        return self.repository.record_risk_signal(**kwargs)

    def compute_score(self, *, user_id: int) -> dict[str, object]:
        return self.repository.compute_risk_score(user_id=user_id)

    def get_score(self, user_id: int) -> dict[str, object]:
        return self.repository.get_risk_score(user_id)

    def list_alerts(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_risk_alerts(**kwargs)


class IncidentService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def list_incidents(self, **kwargs: object) -> list[dict[str, object]]:
        return self.repository.list_security_incidents(**kwargs)

    def create_incident(self, **kwargs: object) -> dict[str, object]:
        return self.repository.create_security_incident(**kwargs)

    def update_incident(self, incident_id: int, **kwargs: object) -> dict[str, object]:
        return self.repository.update_security_incident(incident_id, **kwargs)


class SecurityAnalyticsService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def analytics(self) -> dict[str, object]:
        return self.repository.security_analytics()

    def dashboard(self) -> dict[str, object]:
        return self.repository.security_dashboard()

    def stats(self) -> dict[str, object]:
        return self.repository.security_stats()

    def snapshot(self) -> dict[str, object]:
        return self.repository.snapshot_security_analytics()


class SecurityService:
    def __init__(self, repository, project_service: ProjectService, policy) -> None:
        self.repository = repository
        self.projects = project_service
        self.policy = policy
        self.engine = SecurityPlatformEngine()
        self.iam = IamService(repository)
        self.access = AccessService(repository)
        self.audit = AuditService(repository)
        self.compliance = ComplianceService(repository)
        self.privacy = PrivacyService(repository)
        self.risk = RiskService(repository)
        self.incidents = IncidentService(repository)
        self.analytics_service = SecurityAnalyticsService(repository)

    def _require_auth(self, actor: dict[str, object] | None) -> None:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")

    def _require_admin(self, actor: dict[str, object]) -> None:
        if not self.policy.is_admin(actor):
            raise ProjectPermissionDenied("Admin required")

    # --- IAM ---

    def list_roles(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("security_role_list")
        METRICS.increment("iam_role_list")
        METRICS.increment("role_list")
        return {"roles": [sdto.role_dto(r) for r in self.iam.list_roles(status=status)]}

    def create_role(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        role = self.iam.create_role(
            name=str(body["name"]),
            role_key=str(body["role_key"]) if body.get("role_key") else None,
            description=str(body.get("description") or ""),
            status=str(body.get("status") or "active"),
        )
        METRICS.increment("security_role_created")
        METRICS.increment("iam_role_created")
        METRICS.increment("role_created")
        self.audit.record(
            event_type="admin",
            action="role_created",
            actor_user_id=int(actor["id"]) if actor.get("id") is not None else None,
            resource_type="iam_role",
            resource_id=int(role["id"]),
        )
        return {"role": sdto.role_dto(role)}

    def update_role(self, *, actor: dict[str, object], role_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        role = self.iam.update_role(role_id, **body)
        METRICS.increment("role_updated")
        return {"role": sdto.role_dto(role)}

    def list_permissions(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("security_permission_list")
        METRICS.increment("iam_permission_list")
        METRICS.increment("permission_list")
        return {"permissions": [sdto.permission_dto(r) for r in self.iam.list_permissions()]}

    def create_permission(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        perm = self.iam.create_permission(
            name=str(body["name"]),
            resource=str(body.get("resource") or "*"),
            action=str(body.get("action") or "read"),
            permission_key=str(body["permission_key"]) if body.get("permission_key") else None,
        )
        METRICS.increment("security_permission_created")
        METRICS.increment("permission_created")
        return {"permission": sdto.permission_dto(perm)}

    def list_policies(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("iam_policy_list")
        return {"policies": [sdto.access_policy_dto(r) for r in self.iam.list_policies()]}

    def create_policy(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        policy = self.iam.create_policy(
            name=str(body["name"]),
            policy_type=str(body.get("policy_type") or "rbac"),
            rules=list(body.get("rules") or []),
            policy_key=str(body["policy_key"]) if body.get("policy_key") else None,
        )
        METRICS.increment("iam_policy_created")
        return {"policy": sdto.access_policy_dto(policy)}

    def assign_user_role(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        assigned_by = int(actor["id"]) if actor.get("id") is not None else None
        assignment = self.iam.assign_user_role(
            user_id=int(body["user_id"]),
            role_id=int(body["role_id"]),
            assigned_by=assigned_by,
        )
        METRICS.increment("iam_user_role_assigned")
        return {"user_role": sdto.user_role_dto(assignment)}

    def list_users(self, *, actor: dict[str, object], limit: int = 50) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("security_user_list")
        return {"users": [sdto.user_dto(r) for r in self.iam.list_users(limit=limit)]}

    def get_user(self, *, actor: dict[str, object], user_id: int) -> dict[str, object]:
        self._require_admin(actor)
        return {"user": sdto.user_dto(self.iam.get_user(user_id))}

    def evaluate_access(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        result = self.iam.evaluate_access(
            user_id=int(body["user_id"]),
            policy_id=int(body["policy_id"]),
            attributes=dict(body.get("attributes") or {}),
        )
        METRICS.increment("iam_access_evaluated")
        return {"evaluation": result}

    # --- Access ---

    def list_sessions(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("security_session_list")
        METRICS.increment("access_session_list")
        METRICS.increment("session_list")
        return {"sessions": [sdto.session_record_dto(r) for r in self.access.list_sessions(user_id=user_id)]}

    def revoke_session(self, *, actor: dict[str, object], session_record_id: int) -> dict[str, object]:
        self._require_admin(actor)
        session = self.access.revoke_session(session_record_id)
        METRICS.increment("security_session_revoked")
        METRICS.increment("session_revoked")
        return {"session": sdto.session_record_dto(session)}

    def list_devices(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("access_device_list")
        return {"devices": [sdto.device_dto(r) for r in self.access.list_devices(user_id=user_id)]}

    def register_device(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(body.get("user_id") or actor.get("id") or 0)
        device = self.access.register_device(
            user_id=user_id,
            device_type=str(body.get("device_type") or "browser"),
            device_name=str(body.get("device_name") or ""),
            fingerprint=str(body.get("fingerprint") or ""),
            trust_level=str(body.get("trust_level") or "unknown"),
        )
        METRICS.increment("access_device_registered")
        return {"device": sdto.device_dto(device)}

    def list_api_keys(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("access_api_key_list")
        return {"api_keys": [sdto.api_key_dto(r) for r in self.access.list_api_keys(user_id=user_id)]}

    def create_api_key(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(body.get("user_id") or actor.get("id") or 0)
        api_key = self.access.create_api_key(
            user_id=user_id,
            name=str(body["name"]),
            organization_id=int(body["organization_id"]) if body.get("organization_id") is not None else None,
            scopes=list(body.get("scopes") or []),
            expires_in_days=int(body["expires_in_days"]) if body.get("expires_in_days") is not None else None,
        )
        METRICS.increment("security_api_key_created")
        METRICS.increment("access_api_key_created")
        return {"api_key": sdto.api_key_dto(api_key, include_secret=True)}

    def revoke_api_key(self, *, actor: dict[str, object], api_key_id: int) -> dict[str, object]:
        self._require_auth(actor)
        api_key = self.access.revoke_api_key(api_key_id)
        METRICS.increment("access_api_key_revoked")
        return {"api_key": sdto.api_key_dto(api_key)}

    def list_route_policies(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        return {"route_policies": [sdto.route_policy_dto(r) for r in self.access.list_route_policies()]}

    # --- Audit ---

    def record_audit(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        actor_id = int(actor["id"]) if actor.get("id") is not None else None
        entry = self.audit.record(
            event_type=str(body.get("event_type") or "user"),
            action=str(body["action"]),
            actor_user_id=actor_id,
            resource_type=str(body.get("resource_type") or ""),
            resource_id=int(body["resource_id"]) if body.get("resource_id") is not None else None,
            severity=str(body.get("severity") or "info"),
            payload=dict(body.get("payload") or {}),
            ip_address=str(body.get("ip_address") or ""),
        )
        METRICS.increment("security_audit_recorded")
        METRICS.increment("audit_trail_recorded")
        return {"audit_entry": sdto.audit_trail_dto(entry)}

    def list_audit_trail(self, *, actor: dict[str, object], event_type: str | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("security_audit_list")
        METRICS.increment("audit_trail_list")
        return {"entries": [sdto.audit_trail_dto(r) for r in self.audit.list_trail(event_type=event_type)]}

    def verify_audit_trail(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("audit_trail_verified")
        return {"verification": self.audit.verify_chain()}

    # --- Compliance ---

    def list_compliance_policies(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("compliance_policy_list")
        return {"policies": [sdto.compliance_policy_dto(r) for r in self.compliance.list_policies()]}

    def list_compliance_consents(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("compliance_consent_list")
        return {"consents": [sdto.compliance_consent_dto(r) for r in self.compliance.list_consents(user_id=user_id)]}

    def grant_compliance_consent(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(body.get("user_id") or actor.get("id") or 0) or None
        consent = self.compliance.grant_consent(
            consent_type=str(body.get("consent_type") or "terms"),
            user_id=user_id,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
        )
        METRICS.increment("compliance_consent_granted")
        return {"consent": sdto.compliance_consent_dto(consent)}

    def grant_consent_by_id(self, *, actor: dict[str, object], consent_id: int) -> dict[str, object]:
        self._require_admin(actor)
        consent = self.repository.grant_compliance_consent_by_id(consent_id)
        METRICS.increment("compliance_consent_granted")
        return {"consent": sdto.compliance_consent_dto(consent)}

    def list_retention_rules(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("compliance_retention_list")
        return {"rules": [sdto.retention_rule_dto(r) for r in self.compliance.list_retention_rules()]}

    def create_deletion_request(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(body.get("user_id") or actor.get("id") or 0) or None
        request = self.compliance.create_deletion_request(
            user_id=user_id,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
            deletion_type=str(body.get("deletion_type") or "soft_delete"),
        )
        METRICS.increment("compliance_deletion_requested")
        return {"deletion_request": sdto.deletion_request_dto(request)}

    # --- Privacy ---

    def list_privacy_exports(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("privacy_export_list")
        return {"exports": [sdto.privacy_export_dto(r) for r in self.privacy.list_exports(user_id=user_id)]}

    def create_privacy_export(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(body.get("user_id") or actor.get("id") or 0) or None
        export = self.privacy.create_export(
            user_id=user_id,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
            format=str(body.get("format") or "json"),
            scope=dict(body.get("scope") or {}),
        )
        METRICS.increment("security_privacy_export_created")
        METRICS.increment("privacy_export_created")
        return {"export": sdto.privacy_export_dto(export)}

    def list_privacy_erasure_requests(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("privacy_erasure_list")
        return {"requests": [sdto.privacy_erasure_dto(r) for r in self.privacy.list_erasure_requests()]}

    def create_privacy_erasure_request(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        user_id = int(body.get("user_id") or actor.get("id") or 0) or None
        request = self.privacy.create_erasure_request(
            user_id=user_id,
            contact_id=int(body["contact_id"]) if body.get("contact_id") is not None else None,
            scope=dict(body.get("scope") or {}),
        )
        METRICS.increment("privacy_erasure_requested")
        return {"request": sdto.privacy_erasure_dto(request)}

    # --- Risk ---

    def list_risk_signals(self, *, actor: dict[str, object], user_id: int | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("risk_signal_list")
        return {"signals": [sdto.risk_signal_dto(r) for r in self.risk.list_signals(user_id=user_id)]}

    def record_risk_signal(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        signal = self.risk.record_signal(
            user_id=int(body["user_id"]) if body.get("user_id") is not None else None,
            signal_type=str(body.get("signal_type") or "login_anomaly"),
            severity=str(body.get("severity") or "medium"),
            source=str(body.get("source") or "platform"),
            payload=dict(body.get("payload") or {}),
        )
        METRICS.increment("security_risk_signal_recorded")
        METRICS.increment("risk_signal_recorded")
        return {"signal": sdto.risk_signal_dto(signal)}

    def compute_risk_score(self, *, actor: dict[str, object], user_id: int) -> dict[str, object]:
        self._require_admin(actor)
        score = self.risk.compute_score(user_id=user_id)
        METRICS.increment("risk_score_computed")
        return {"risk_score": sdto.risk_score_dto(score)}

    def list_risk_alerts(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("risk_alert_list")
        return {"alerts": [sdto.risk_alert_dto(r) for r in self.risk.list_alerts(status=status)]}

    # --- Incidents ---

    def list_incidents(self, *, actor: dict[str, object], status: str | None = None) -> dict[str, object]:
        self._require_admin(actor)
        METRICS.increment("security_incident_list")
        return {"incidents": [sdto.incident_dto(r) for r in self.incidents.list_incidents(status=status)]}

    def create_incident(self, *, actor: dict[str, object], body: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        reporter_id = int(actor["id"]) if actor.get("id") is not None else None
        incident = self.incidents.create_incident(
            title=str(body["title"]),
            severity=str(body.get("severity") or "medium"),
            description=str(body.get("description") or ""),
            reported_by=reporter_id,
            assigned_to=int(body["assigned_to"]) if body.get("assigned_to") is not None else None,
        )
        METRICS.increment("security_incident_created")
        return {"incident": sdto.incident_dto(incident)}

    def update_incident(self, *, actor: dict[str, object], incident_id: int, body: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        incident = self.incidents.update_incident(incident_id, **body)
        METRICS.increment("security_incident_updated")
        return {"incident": sdto.incident_dto(incident)}

    # --- Analytics / Dashboard ---

    def analytics(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("security_analytics")
        return sdto.analytics_dto(self.analytics_service.analytics())

    def dashboard(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("security_dashboard")
        return sdto.dashboard_dto(self.analytics_service.dashboard())

    def stats(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_auth(actor)
        METRICS.increment("security_stats")
        return sdto.stats_dto(self.analytics_service.stats())

    def integration_sources(self, *, actor: dict[str, object] | None = None) -> dict[str, object]:
        if actor is not None:
            self._require_auth(actor)
        return {"sources": self.engine.integration_sources(), "integrations": self.repository.integration_sources()}

    def seed_catalog(self, *, actor: dict[str, object]) -> dict[str, object]:
        self._require_admin(actor)
        self.repository.seed_security_catalog()
        METRICS.increment("security_catalog_seeded")
        return {"seeded": True}
