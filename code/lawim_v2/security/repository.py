from __future__ import annotations

import hashlib
import json
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from ..repository_introspection import table_exists
from .constants import (
    API_KEY_STATUSES,
    AUDIT_EVENT_TYPES,
    AUDIT_SEVERITIES,
    COMPLIANCE_FRAMEWORKS,
    CONSENT_TYPES,
    DEFAULT_PERMISSIONS,
    DEFAULT_ROLES,
    DEVICE_TYPES,
    INCIDENT_SEVERITIES,
    INCIDENT_STATUSES,
    MFA_TYPES,
    PRIVACY_EXPORT_FORMATS,
    PRIVACY_REQUEST_STATUSES,
    ROLE_STATUSES,
    RISK_SIGNAL_TYPES,
    SESSION_STATUSES,
)
from .engines import SecurityPlatformEngine


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


class SecurityRepositoryMixin:
    def security_tables_present(self) -> bool:
        return table_exists(self, "iam_roles")

    def seed_security_catalog(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM iam_roles") > 0:
            return
        engine = SecurityPlatformEngine()
        now = _utcnow()
        with self._transaction() as conn:
            role_ids: dict[str, int] = {}
            for role_key, name, description in DEFAULT_ROLES:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO iam_roles (role_key, name, description, status, created_at, updated_at)
                    VALUES (?, ?, ?, 'active', ?, ?)
                    """,
                    (role_key, name, description, now, now),
                )
                row = self.one("SELECT id FROM iam_roles WHERE role_key = ?", (role_key,))
                if row:
                    role_ids[role_key] = int(row["id"])
            perm_ids: dict[str, int] = {}
            for perm_key, name, resource, action in DEFAULT_PERMISSIONS:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO iam_permissions (permission_key, name, resource, action, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (perm_key, name, resource, action, now),
                )
                row = self.one("SELECT id FROM iam_permissions WHERE permission_key = ?", (perm_key,))
                if row:
                    perm_ids[perm_key] = int(row["id"])
            admin_role_id = role_ids.get("role-security-admin") or role_ids.get("role-admin")
            if admin_role_id:
                for perm_id in perm_ids.values():
                    conn.execute(
                        """
                        INSERT OR IGNORE INTO iam_role_permissions (role_id, permission_id, granted_at)
                        VALUES (?, ?, ?)
                        """,
                        (admin_role_id, perm_id, now),
                    )
            route_policies = [
                (
                    "route-security-admin",
                    "/api/v2/security/*",
                    '["GET", "POST", "PUT", "DELETE"]',
                    '["role-security-admin", "role-admin"]',
                    '["perm-security-admin"]',
                ),
                (
                    "route-security-audit",
                    "/api/v2/security/audit/*",
                    '["GET"]',
                    '["role-auditor", "role-security-admin"]',
                    '["perm-audit-read"]',
                ),
                (
                    "route-security-privacy",
                    "/api/v2/security/privacy/*",
                    '["GET", "POST"]',
                    '["role-admin", "role-security-admin"]',
                    '["perm-privacy-export"]',
                ),
                (
                    "route-backup-read",
                    "/api/v2/backup/*",
                    '["GET"]',
                    '["role-admin"]',
                    '["perm-backup-read"]',
                ),
                (
                    "route-backup-run",
                    "/api/v2/backup/run",
                    '["POST"]',
                    '["role-admin"]',
                    '["perm-backup-write"]',
                ),
                (
                    "route-backup-test",
                    "/api/v2/backup/test",
                    '["POST"]',
                    '["role-admin"]',
                    '["perm-backup-write"]',
                ),
                (
                    "route-backup-retry",
                    "/api/v2/backup/retry",
                    '["POST"]',
                    '["role-admin"]',
                    '["perm-backup-write"]',
                ),
                (
                    "route-backup-restore",
                    "/api/v2/backup/restore",
                    '["POST"]',
                    '["role-admin"]',
                    '["perm-backup-restore"]',
                ),
                (
                    "route-backup-provider-test",
                    "/api/v2/backup/provider/test",
                    '["POST"]',
                    '["role-admin"]',
                    '["perm-backup-write"]',
                ),
                (
                    "route-backup-config",
                    "/api/v2/backup/config",
                    '["PATCH"]',
                    '["role-admin"]',
                    '["perm-backup-admin"]',
                ),
                (
                    "route-financial-catalog",
                    "/api/v2/financial/catalog/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager", "role-operator", "role-partner", "role-user"]',
                    '["perm-financial-catalog-read"]',
                ),
                (
                    "route-financial-pricing",
                    "/api/v2/financial/pricing/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager", "role-operator"]',
                    '["perm-financial-pricing-read"]',
                ),
                (
                    "route-financial-quotes",
                    "/api/v2/financial/quotes/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager", "role-operator", "role-partner", "role-user"]',
                    '["perm-financial-quote-create"]',
                ),
                (
                    "route-financial-invoices",
                    "/api/v2/financial/invoices/*",
                    '["GET", "POST", "PATCH", "DELETE"]',
                    '["role-admin", "role-manager", "role-operator", "role-partner", "role-user"]',
                    '["perm-financial-invoice-read"]',
                ),
                (
                    "route-financial-payments",
                    "/api/v2/financial/payments/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager", "role-operator", "role-partner", "role-user"]',
                    '["perm-financial-payment-read"]',
                ),
                (
                    "route-financial-refunds",
                    "/api/v2/financial/refunds/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager", "role-operator"]',
                    '["perm-financial-refund-request"]',
                ),
                (
                    "route-financial-subscriptions",
                    "/api/v2/financial/subscriptions/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager", "role-operator", "role-user"]',
                    '["perm-financial-subscription-manage"]',
                ),
                (
                    "route-financial-commissions",
                    "/api/v2/financial/commissions/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager"]',
                    '["perm-financial-commission-read"]',
                ),
                (
                    "route-financial-payouts",
                    "/api/v2/financial/payouts/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager"]',
                    '["perm-financial-payout-manage"]',
                ),
                (
                    "route-financial-ledger",
                    "/api/v2/financial/ledger/*",
                    '["GET", "POST"]',
                    '["role-admin"]',
                    '["perm-financial-ledger-read"]',
                ),
                (
                    "route-financial-reconciliation",
                    "/api/v2/financial/reconciliation/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager"]',
                    '["perm-financial-reconciliation-manage"]',
                ),
                (
                    "route-financial-providers",
                    "/api/v2/financial/providers/*",
                    '["GET", "POST", "PATCH"]',
                    '["role-admin", "role-manager"]',
                    '["perm-financial-provider-manage"]',
                ),
            ]
            for route_key, path, methods, roles, perms in route_policies:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO access_route_policies (
                        route_key, path_pattern, methods_json, required_roles_json,
                        required_permissions_json, policy_type, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, 'rbac', 'active', ?, ?)
                    """,
                    (route_key, path, methods, roles, perms, now, now),
                )
            compliance_policies = [
                (
                    "compliance-gdpr-default",
                    "Politique GDPR LAWIM",
                    "gdpr",
                    '[{"field": "consent", "required": true}, {"field": "retention", "required": true}]',
                ),
                (
                    "compliance-internal-default",
                    "Politique interne LAWIM",
                    "internal",
                    '[{"field": "audit_trail", "required": true}]',
                ),
            ]
            for policy_key, name, framework, rules in compliance_policies:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO compliance_policies (
                        policy_key, name, framework, rules_json, status, effective_at, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, 'active', ?, ?, ?)
                    """,
                    (policy_key, name, framework, rules, now, now, now),
                )
            retention_rules = [
                ("retention-audit", "Conservation journaux audit", "audit", 365, "archive"),
                ("retention-sessions", "Conservation sessions", "session", 90, "delete"),
                ("retention-api-keys", "Conservation clés API révoquées", "api_key", 30, "delete"),
            ]
            for rule_key, name, resource_type, days, action in retention_rules:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO compliance_retention_rules (
                        rule_key, name, resource_type, retention_days, action_on_expiry, status, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                    """,
                    (rule_key, name, resource_type, days, action, now, now),
                )
            conn.execute(
                """
                INSERT OR IGNORE INTO iam_access_policies (
                    policy_key, name, policy_type, rules_json, status, created_at, updated_at
                ) VALUES (
                    'policy-default-rbac',
                    'Politique RBAC LAWIM par défaut',
                    'rbac',
                    '[{"role": "role-admin", "permission": "security:admin"}]',
                    'active',
                    ?, ?
                )
                """,
                (now, now),
            )
        self.record_event("security_catalog_seeded", {"roles": len(DEFAULT_ROLES), "permissions": len(DEFAULT_PERMISSIONS)})
        self.snapshot_security_analytics()

    def integration_sources(self) -> dict[str, object]:
        engine = SecurityPlatformEngine()
        payload: dict[str, object] = {"sources": engine.integration_sources()}
        checks = {
            "intelligent_core": hasattr(self, "get_intelligent_decision"),
            "ecosystem": hasattr(self, "get_service_catalog_item"),
            "cognition": hasattr(self, "cognition_query"),
            "maintenance": hasattr(self, "create_maintenance_message"),
            "knowledge_platform": hasattr(self, "expert_rag_query"),
            "workflow_automation": hasattr(self, "start_automation_instance"),
            "real_estate_intelligence": hasattr(self, "get_rei_property_bundle"),
            "crm": hasattr(self, "get_crm_contact"),
            "marketplace": hasattr(self, "get_marketplace_provider"),
        }
        payload["programs"] = {key: bool(value) for key, value in checks.items()}
        return payload

    # --- IAM roles ---

    def create_iam_role(self, *, name: str, role_key: str | None = None, description: str = "", status: str = "active") -> dict[str, object]:
        if status not in ROLE_STATUSES:
            status = "active"
        now = _utcnow()
        key = role_key or f"role-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO iam_roles (role_key, name, description, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (key, name, description, status, now, now),
            )
        return dict(self.one("SELECT * FROM iam_roles WHERE role_key = ?", (key,)))

    def get_iam_role(self, role_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM iam_roles WHERE id = ?", (role_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("role not found")
        return dict(row)

    def list_iam_roles(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all("SELECT * FROM iam_roles WHERE status = ? ORDER BY id ASC LIMIT ?", (status, limit))
        else:
            rows = self.all("SELECT * FROM iam_roles ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_iam_role(self, role_id: int, **fields: object) -> dict[str, object]:
        allowed = {"name", "description", "status", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if "metadata" in fields and fields["metadata"] is not None:
            updates["metadata_json"] = _json(fields["metadata"])
        if not updates:
            return self.get_iam_role(role_id)
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE iam_roles SET {cols} WHERE id = ?", (*updates.values(), role_id))
        return self.get_iam_role(role_id)

    # --- IAM permissions ---

    def create_iam_permission(
        self,
        *,
        name: str,
        resource: str = "*",
        action: str = "read",
        permission_key: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = permission_key or f"perm-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO iam_permissions (permission_key, name, resource, action, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (key, name, resource, action, now),
            )
        return dict(self.one("SELECT * FROM iam_permissions WHERE permission_key = ?", (key,)))

    def get_iam_permission(self, permission_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM iam_permissions WHERE id = ?", (permission_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("permission not found")
        return dict(row)

    def list_iam_permissions(self, *, limit: int = 100) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM iam_permissions ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def assign_user_role(self, *, user_id: int, role_id: int, assigned_by: int | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO iam_user_roles (user_id, role_id, assigned_by, assigned_at)
                VALUES (?, ?, ?, ?)
                """,
                (user_id, role_id, assigned_by, now),
            )
        row = self.one("SELECT * FROM iam_user_roles WHERE user_id = ? AND role_id = ?", (user_id, role_id))
        return dict(row)

    def list_user_roles(self, *, user_id: int) -> list[dict[str, object]]:
        rows = self.all(
            """
            SELECT ur.*, r.role_key, r.name AS role_name
            FROM iam_user_roles ur
            JOIN iam_roles r ON r.id = ur.role_id
            WHERE ur.user_id = ?
            ORDER BY ur.assigned_at DESC
            """,
            (user_id,),
        )
        return [dict(r) for r in rows]

    def grant_role_permission(self, *, role_id: int, permission_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO iam_role_permissions (role_id, permission_id, granted_at)
                VALUES (?, ?, ?)
                """,
                (role_id, permission_id, now),
            )
        row = self.one(
            "SELECT * FROM iam_role_permissions WHERE role_id = ? AND permission_id = ?",
            (role_id, permission_id),
        )
        return dict(row)

    # --- Groups & teams ---

    def create_iam_group(self, *, name: str, organization_id: int | None = None, description: str = "") -> dict[str, object]:
        now = _utcnow()
        key = f"group-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO iam_groups (group_key, name, description, organization_id, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, name, description, organization_id, now, now),
            )
        return dict(self.one("SELECT * FROM iam_groups WHERE group_key = ?", (key,)))

    def add_group_member(self, *, group_id: int, user_id: int, role_in_group: str = "member") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO iam_group_members (group_id, user_id, role_in_group, joined_at)
                VALUES (?, ?, ?, ?)
                """,
                (group_id, user_id, role_in_group, now),
            )
        row = self.one("SELECT * FROM iam_group_members WHERE group_id = ? AND user_id = ?", (group_id, user_id))
        return dict(row)

    def list_iam_groups(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM iam_groups ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def create_iam_team(
        self,
        *,
        name: str,
        organization_id: int | None = None,
        leader_user_id: int | None = None,
        description: str = "",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"team-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO iam_teams (
                    team_key, name, description, organization_id, leader_user_id, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, name, description, organization_id, leader_user_id, now, now),
            )
        return dict(self.one("SELECT * FROM iam_teams WHERE team_key = ?", (key,)))

    def add_team_member(self, *, team_id: int, user_id: int, role_in_team: str = "member") -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO iam_team_members (team_id, user_id, role_in_team, joined_at)
                VALUES (?, ?, ?, ?)
                """,
                (team_id, user_id, role_in_team, now),
            )
        row = self.one("SELECT * FROM iam_team_members WHERE team_id = ? AND user_id = ?", (team_id, user_id))
        return dict(row)

    def list_iam_teams(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM iam_teams ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    # --- Access policies ---

    def create_iam_access_policy(
        self,
        *,
        name: str,
        policy_type: str = "rbac",
        rules: list[dict[str, object]] | None = None,
        policy_key: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = policy_key or f"policy-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO iam_access_policies (
                    policy_key, name, policy_type, rules_json, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, name, policy_type, _json(rules or []), now, now),
            )
        return dict(self.one("SELECT * FROM iam_access_policies WHERE policy_key = ?", (key,)))

    def list_iam_access_policies(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM iam_access_policies ORDER BY id ASC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def bind_iam_policy(self, *, policy_id: int, binding_type: str, binding_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO iam_policy_bindings (policy_id, binding_type, binding_id, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (policy_id, binding_type, binding_id, now),
            )
        row = self.one(
            "SELECT * FROM iam_policy_bindings WHERE policy_id = ? AND binding_type = ? AND binding_id = ?",
            (policy_id, binding_type, binding_id),
        )
        return dict(row)

    def list_access_route_policies(self) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM access_route_policies WHERE status = 'active' ORDER BY id ASC")
        return [dict(r) for r in rows]

    # --- Users (from users table) ---

    def list_security_users(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all(
            "SELECT id, email, full_name AS display_name, role, organization_id, 'active' AS status FROM users ORDER BY id ASC LIMIT ?",
            (limit,),
        )
        return [dict(r) for r in rows]

    def get_security_user(self, user_id: int) -> dict[str, object]:
        row = self.one(
            "SELECT id, email, full_name AS display_name, role, organization_id, 'active' AS status FROM users WHERE id = ?",
            (user_id,),
        )
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("user not found")
        user = dict(row)
        user["iam_roles"] = self.list_user_roles(user_id=user_id)
        return user

    # --- Devices ---

    def register_access_device(
        self,
        *,
        user_id: int,
        device_type: str = "browser",
        device_name: str = "",
        fingerprint: str = "",
        trust_level: str = "unknown",
    ) -> dict[str, object]:
        if device_type not in DEVICE_TYPES:
            device_type = "browser"
        now = _utcnow()
        key = f"device-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO access_devices (
                    device_key, user_id, device_type, device_name, fingerprint, trust_level,
                    last_seen_at, status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, user_id, device_type, device_name, fingerprint, trust_level, now, now, now),
            )
        return dict(self.one("SELECT * FROM access_devices WHERE device_key = ?", (key,)))

    def list_access_devices(self, *, user_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM access_devices WHERE user_id = ? ORDER BY last_seen_at DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM access_devices ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_access_device(self, device_id: int, **fields: object) -> dict[str, object]:
        allowed = {"device_name", "trust_level", "status", "metadata_json"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not updates:
            row = self.one("SELECT * FROM access_devices WHERE id = ?", (device_id,))
            if row is None:
                from ..errors import NotFoundError
                raise NotFoundError("device not found")
            return dict(row)
        updates["last_seen_at"] = _utcnow()
        updates["updated_at"] = _utcnow()
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE access_devices SET {cols} WHERE id = ?", (*updates.values(), device_id))
        row = self.one("SELECT * FROM access_devices WHERE id = ?", (device_id,))
        return dict(row)

    # --- API keys ---

    def create_api_key(
        self,
        *,
        user_id: int,
        name: str,
        organization_id: int | None = None,
        scopes: list[str] | None = None,
        expires_in_days: int | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"apikey-{uuid.uuid4().hex[:10]}"
        secret = f"lawim_{secrets.token_urlsafe(32)}"
        prefix = secret[:12]
        key_hash = hashlib.sha256(secret.encode("utf-8")).hexdigest()
        expires_at = None
        if expires_in_days is not None:
            expires_at = (datetime.now(timezone.utc) + timedelta(days=expires_in_days)).replace(microsecond=0).isoformat()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO access_api_keys (
                    api_key_key, user_id, organization_id, name, key_prefix, key_hash,
                    scopes_json, status, expires_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, user_id, organization_id, name, prefix, key_hash, _json(scopes or []), expires_at, now),
            )
        row = dict(self.one("SELECT * FROM access_api_keys WHERE api_key_key = ?", (key,)))
        row["secret"] = secret
        return row

    def list_access_api_keys(self, *, user_id: int | None = None, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM access_api_keys WHERE 1=1"
        params: list[object] = []
        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        rows = self.all(query, tuple(params))
        return [dict(r) for r in rows]

    def revoke_api_key(self, api_key_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE access_api_keys SET status = 'revoked', revoked_at = ? WHERE id = ?",
                (now, api_key_id),
            )
        row = self.one("SELECT * FROM access_api_keys WHERE id = ?", (api_key_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("api key not found")
        return dict(row)

    # --- Session records ---

    def record_access_session(
        self,
        *,
        user_id: int,
        session_token: str | None = None,
        device_id: int | None = None,
        ip_address: str = "",
        user_agent: str = "",
        expires_at: str | None = None,
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"session-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO access_session_records (
                    session_key, user_id, session_token, device_id, ip_address, user_agent,
                    status, started_at, expires_at
                ) VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?)
                """,
                (key, user_id, session_token, device_id, ip_address, user_agent, now, expires_at),
            )
        return dict(self.one("SELECT * FROM access_session_records WHERE session_key = ?", (key,)))

    def list_access_session_records(
        self,
        *,
        user_id: int | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        query = "SELECT * FROM access_session_records WHERE 1=1"
        params: list[object] = []
        if user_id is not None:
            query += " AND user_id = ?"
            params.append(user_id)
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY started_at DESC LIMIT ?"
        params.append(limit)
        rows = self.all(query, tuple(params))
        return [dict(r) for r in rows]

    def revoke_session_record(self, session_record_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE access_session_records SET status = 'revoked', revoked_at = ? WHERE id = ?",
                (now, session_record_id),
            )
        row = self.one("SELECT * FROM access_session_records WHERE id = ?", (session_record_id,))
        if row is None:
            from ..errors import NotFoundError
            raise NotFoundError("session record not found")
        return dict(row)

    # --- Audit ---

    def record_audit_trail(
        self,
        *,
        event_type: str = "system",
        action: str,
        actor_user_id: int | None = None,
        resource_type: str = "",
        resource_id: int | None = None,
        severity: str = "info",
        payload: dict[str, Any] | None = None,
        ip_address: str = "",
    ) -> dict[str, object]:
        engine = SecurityPlatformEngine()
        if event_type not in AUDIT_EVENT_TYPES:
            event_type = "system"
        if severity not in AUDIT_SEVERITIES:
            severity = "info"
        now = _utcnow()
        entry_key = f"audit-{uuid.uuid4().hex[:12]}"
        latest = self.one("SELECT checksum FROM audit_trail_entries ORDER BY id DESC LIMIT 1")
        previous = str(latest["checksum"]) if latest and latest.get("checksum") else engine.audit.GENESIS_CHECKSUM
        payload_data = payload or {}
        checksum = engine.audit.compute_checksum(
            entry_key=entry_key,
            event_type=event_type,
            action=action,
            payload=payload_data,
            previous_checksum=previous,
            created_at=now,
        )
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO audit_trail_entries (
                    entry_key, event_type, actor_user_id, resource_type, resource_id, action,
                    severity, payload_json, checksum, previous_checksum, ip_address, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    entry_key,
                    event_type,
                    actor_user_id,
                    resource_type,
                    resource_id,
                    action,
                    severity,
                    _json(payload_data),
                    checksum,
                    previous,
                    ip_address,
                    now,
                ),
            )
            trail = self.one("SELECT id FROM audit_trail_entries WHERE entry_key = ?", (entry_key,))
            trail_id = int(trail["id"]) if trail else None
            event_key = f"evt-{uuid.uuid4().hex[:10]}"
            if event_type == "user" and actor_user_id:
                conn.execute(
                    """
                    INSERT INTO audit_user_events (event_key, trail_entry_id, user_id, action, payload_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (event_key, trail_id, actor_user_id, action, _json(payload_data), now),
                )
            elif event_type == "admin" and actor_user_id:
                conn.execute(
                    """
                    INSERT INTO audit_admin_events (event_key, trail_entry_id, admin_user_id, action, payload_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (event_key, trail_id, actor_user_id, action, _json(payload_data), now),
                )
            elif event_type == "ai":
                conn.execute(
                    """
                    INSERT INTO audit_ai_events (event_key, trail_entry_id, action, payload_json, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (event_key, trail_id, action, _json(payload_data), now),
                )
            else:
                conn.execute(
                    """
                    INSERT INTO audit_system_events (event_key, trail_entry_id, component, message, severity, payload_json, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (event_key, trail_id, resource_type or "platform", action, severity, _json(payload_data), now),
                )
        return dict(self.one("SELECT * FROM audit_trail_entries WHERE entry_key = ?", (entry_key,)))

    def list_audit_trail(
        self,
        *,
        event_type: str | None = None,
        actor_user_id: int | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        query = "SELECT * FROM audit_trail_entries WHERE 1=1"
        params: list[object] = []
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        if actor_user_id is not None:
            query += " AND actor_user_id = ?"
            params.append(actor_user_id)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        rows = self.all(query, tuple(params))
        return [dict(r) for r in rows]

    def verify_audit_trail(self, *, limit: int = 100) -> dict[str, object]:
        engine = SecurityPlatformEngine()
        rows = self.all("SELECT * FROM audit_trail_entries ORDER BY id ASC LIMIT ?", (limit,))
        entries = [dict(r) for r in rows]
        return engine.audit.verify_chain(entries)

    # --- Compliance ---

    def list_compliance_policies(self) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM compliance_policies WHERE status = 'active' ORDER BY id ASC")
        return [dict(r) for r in rows]

    def grant_compliance_consent(
        self,
        *,
        consent_type: str = "terms",
        user_id: int | None = None,
        contact_id: int | None = None,
    ) -> dict[str, object]:
        if consent_type not in CONSENT_TYPES:
            consent_type = "terms"
        now = _utcnow()
        key = f"consent-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO compliance_consents (
                    consent_key, user_id, contact_id, consent_type, status, granted_at, created_at
                ) VALUES (?, ?, ?, ?, 'granted', ?, ?)
                """,
                (key, user_id, contact_id, consent_type, now, now),
            )
        return dict(self.one("SELECT * FROM compliance_consents WHERE consent_key = ?", (key,)))

    def grant_compliance_consent_by_id(self, consent_id: int) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                UPDATE compliance_consents
                SET status = 'granted', granted_at = ?
                WHERE id = ?
                """,
                (now, consent_id),
            )
        row = self.one("SELECT * FROM compliance_consents WHERE id = ?", (consent_id,))
        if row is None:
            raise ValueError("Consent not found")
        return dict(row)

    def list_compliance_consents(self, *, user_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM compliance_consents WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM compliance_consents ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def list_compliance_retention_rules(self) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM compliance_retention_rules WHERE status = 'active' ORDER BY id ASC")
        return [dict(r) for r in rows]

    def create_compliance_deletion_request(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        deletion_type: str = "soft_delete",
    ) -> dict[str, object]:
        now = _utcnow()
        key = f"del-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO compliance_deletion_requests (
                    request_key, user_id, contact_id, deletion_type, status, requested_at
                ) VALUES (?, ?, ?, ?, 'pending', ?)
                """,
                (key, user_id, contact_id, deletion_type, now),
            )
        return dict(self.one("SELECT * FROM compliance_deletion_requests WHERE request_key = ?", (key,)))

    def list_compliance_deletion_requests(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM compliance_deletion_requests WHERE status = ? ORDER BY id DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM compliance_deletion_requests ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    # --- Privacy ---

    def create_privacy_export(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        format: str = "json",
        scope: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = SecurityPlatformEngine()
        if format not in PRIVACY_EXPORT_FORMATS:
            format = "json"
        scope_list = engine.privacy.normalize_scope(list(scope.keys()) if scope else None)
        now = _utcnow()
        key = f"export-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO privacy_data_exports (
                    export_key, user_id, contact_id, format, scope_json, status, requested_at
                ) VALUES (?, ?, ?, ?, ?, 'pending', ?)
                """,
                (key, user_id, contact_id, format, _json({"scopes": scope_list}), now),
            )
        return dict(self.one("SELECT * FROM privacy_data_exports WHERE export_key = ?", (key,)))

    def list_privacy_exports(self, *, user_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM privacy_data_exports WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM privacy_data_exports ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def create_privacy_erasure_request(
        self,
        *,
        user_id: int | None = None,
        contact_id: int | None = None,
        scope: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = SecurityPlatformEngine()
        active_sessions = 0
        if user_id is not None:
            active_sessions = self.scalar(
                "SELECT COUNT(*) FROM access_session_records WHERE user_id = ? AND status = 'active'",
                (user_id,),
            )
        validation = engine.privacy.validate_erasure(
            scope=scope or {"user_id": user_id, "contact_id": contact_id},
            has_active_sessions=active_sessions > 0,
        )
        now = _utcnow()
        key = f"erase-{uuid.uuid4().hex[:10]}"
        status = "pending" if validation["valid"] else "failed"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO privacy_erasure_requests (
                    request_key, user_id, contact_id, scope_json, status, requested_at, validation_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (key, user_id, contact_id, _json(scope or {}), status, now, _json(validation)),
            )
        return dict(self.one("SELECT * FROM privacy_erasure_requests WHERE request_key = ?", (key,)))

    def list_privacy_erasure_requests(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM privacy_erasure_requests ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    # --- Risk ---

    def record_risk_signal(
        self,
        *,
        user_id: int | None = None,
        signal_type: str = "login_anomaly",
        severity: str = "medium",
        source: str = "platform",
        payload: dict[str, Any] | None = None,
    ) -> dict[str, object]:
        engine = SecurityPlatformEngine()
        if signal_type not in RISK_SIGNAL_TYPES:
            signal_type = "login_anomaly"
        scored = engine.risk.score_signal(signal_type=signal_type, severity=severity)
        now = _utcnow()
        key = f"signal-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO risk_signals (
                    signal_key, user_id, signal_type, severity, score_delta, source,
                    payload_json, detected_at, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open')
                """,
                (key, user_id, signal_type, severity, scored["score_delta"], source, _json(payload or {}), now),
            )
        signal = dict(self.one("SELECT * FROM risk_signals WHERE signal_key = ?", (key,)))
        if user_id is not None:
            self.compute_risk_score(user_id=user_id)
        return signal

    def compute_risk_score(self, *, user_id: int, score_key: str = "overall") -> dict[str, object]:
        engine = SecurityPlatformEngine()
        signals = self.all(
            "SELECT * FROM risk_signals WHERE user_id = ? AND status = 'open' ORDER BY detected_at DESC LIMIT 20",
            (user_id,),
        )
        result = engine.risk.aggregate(signals=[dict(s) for s in signals])
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO risk_scores (user_id, score_key, score, level, factors_json, computed_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, score_key) DO UPDATE SET
                    score = excluded.score,
                    level = excluded.level,
                    factors_json = excluded.factors_json,
                    computed_at = excluded.computed_at
                """,
                (user_id, score_key, result["score"], result["level"], _json(result["factors"]), now),
            )
            if result["auto_lock"]:
                alert_key = f"alert-{uuid.uuid4().hex[:10]}"
                conn.execute(
                    """
                    INSERT OR IGNORE INTO risk_alerts (alert_key, user_id, level, title, status, created_at)
                    VALUES (?, ?, ?, ?, 'open', ?)
                    """,
                    (alert_key, user_id, result["level"], "Seuil de risque élevé — verrouillage recommandé", now),
                )
        row = self.one("SELECT * FROM risk_scores WHERE user_id = ? AND score_key = ?", (user_id, score_key))
        payload = dict(row)
        payload["auto_lock"] = result["auto_lock"]
        return payload

    def list_risk_signals(self, *, user_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if user_id is not None:
            rows = self.all(
                "SELECT * FROM risk_signals WHERE user_id = ? ORDER BY detected_at DESC LIMIT ?",
                (user_id, limit),
            )
        else:
            rows = self.all("SELECT * FROM risk_signals ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def list_risk_alerts(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM risk_alerts WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM risk_alerts ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def get_risk_score(self, user_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM risk_scores WHERE user_id = ? AND score_key = 'overall'", (user_id,))
        if row is None:
            return self.compute_risk_score(user_id=user_id)
        return dict(row)

    # --- Incidents ---

    def create_security_incident(
        self,
        *,
        title: str,
        severity: str = "medium",
        description: str = "",
        reported_by: int | None = None,
        assigned_to: int | None = None,
    ) -> dict[str, object]:
        if severity not in INCIDENT_SEVERITIES:
            severity = "medium"
        now = _utcnow()
        key = f"incident-{uuid.uuid4().hex[:10]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO security_incidents (
                    incident_key, title, severity, status, reported_by, assigned_to,
                    description, opened_at, created_at, updated_at
                ) VALUES (?, ?, ?, 'open', ?, ?, ?, ?, ?, ?)
                """,
                (key, title, severity, reported_by, assigned_to, description, now, now, now),
            )
        return dict(self.one("SELECT * FROM security_incidents WHERE incident_key = ?", (key,)))

    def list_security_incidents(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if status:
            rows = self.all(
                "SELECT * FROM security_incidents WHERE status = ? ORDER BY opened_at DESC LIMIT ?",
                (status, limit),
            )
        else:
            rows = self.all("SELECT * FROM security_incidents ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

    def update_security_incident(self, incident_id: int, **fields: object) -> dict[str, object]:
        allowed = {"title", "severity", "status", "assigned_to", "description", "resolution"}
        updates = {k: v for k, v in fields.items() if k in allowed and v is not None}
        if not updates:
            row = self.one("SELECT * FROM security_incidents WHERE id = ?", (incident_id,))
            if row is None:
                from ..errors import NotFoundError
                raise NotFoundError("incident not found")
            return dict(row)
        now = _utcnow()
        updates["updated_at"] = now
        if updates.get("status") in {"resolved", "closed"}:
            updates["resolved_at"] = now
        cols = ", ".join(f"{k} = ?" for k in updates)
        with self._transaction() as conn:
            conn.execute(f"UPDATE security_incidents SET {cols} WHERE id = ?", (*updates.values(), incident_id))
        row = self.one("SELECT * FROM security_incidents WHERE id = ?", (incident_id,))
        return dict(row)

    # --- Analytics ---

    def snapshot_security_analytics(self) -> dict[str, object]:
        metrics = {
            "roles": self.scalar("SELECT COUNT(*) FROM iam_roles"),
            "permissions": self.scalar("SELECT COUNT(*) FROM iam_permissions"),
            "active_sessions": self.scalar("SELECT COUNT(*) FROM access_session_records WHERE status = 'active'"),
            "api_keys": self.scalar("SELECT COUNT(*) FROM access_api_keys WHERE status = 'active'"),
            "audit_entries": self.scalar("SELECT COUNT(*) FROM audit_trail_entries"),
            "open_incidents": self.scalar("SELECT COUNT(*) FROM security_incidents WHERE status = 'open'"),
            "open_risk_alerts": self.scalar("SELECT COUNT(*) FROM risk_alerts WHERE status = 'open'"),
            "pending_privacy_exports": self.scalar("SELECT COUNT(*) FROM privacy_data_exports WHERE status = 'pending'"),
        }
        now = _utcnow()
        key = f"snap-{uuid.uuid4().hex[:8]}"
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO security_analytics_snapshots (snapshot_key, scope, metrics_json, created_at)
                VALUES (?, 'global', ?, ?)
                """,
                (key, _json(metrics), now),
            )
        return metrics

    def security_analytics(self) -> dict[str, object]:
        latest = self.one("SELECT * FROM security_analytics_snapshots ORDER BY id DESC LIMIT 1")
        if latest is None:
            metrics = self.snapshot_security_analytics()
            return {"metrics": metrics, "snapshot": None}
        return {"metrics": _parse_json(str(latest.get("metrics_json"))) or {}, "snapshot": dict(latest)}

    def security_dashboard(self) -> dict[str, object]:
        analytics = self.security_analytics()
        return {
            "summary": analytics.get("metrics") or {},
            "recent_audit": self.list_audit_trail(limit=5),
            "open_incidents": self.list_security_incidents(status="open", limit=5),
            "open_risk_alerts": self.list_risk_alerts(status="open", limit=5),
            "integrations": self.integration_sources(),
        }

    def security_stats(self) -> dict[str, object]:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).replace(microsecond=0).isoformat()
        return {
            "active_roles": self.scalar("SELECT COUNT(*) FROM iam_roles WHERE status = 'active'"),
            "active_api_keys": self.scalar("SELECT COUNT(*) FROM access_api_keys WHERE status = 'active'"),
            "active_sessions": self.scalar("SELECT COUNT(*) FROM access_session_records WHERE status = 'active'"),
            "audit_entries_24h": self.scalar(
                "SELECT COUNT(*) FROM audit_trail_entries WHERE created_at >= ?",
                (cutoff,),
            ),
            "open_incidents": self.scalar("SELECT COUNT(*) FROM security_incidents WHERE status IN ('open', 'investigating')"),
            "high_risk_users": self.scalar("SELECT COUNT(*) FROM risk_scores WHERE level IN ('high', 'critical')"),
        }
