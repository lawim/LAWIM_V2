from __future__ import annotations

import sqlite3
import tempfile
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

from lawim_v2.crm.schema_v14_ddl import V14_TABLE_NAMES
from lawim_v2.knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES
from lawim_v2.marketplace.schema_v15_ddl import V15_TABLE_NAMES
from lawim_v2.persistence import APPLICATION_SCHEMA_VERSION
from lawim_v2.real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES
from lawim_v2.schema_ddl import SQLITE_INIT_SCRIPT
from lawim_v2.schema_migrations import apply_sqlite_legacy_migrations, migration_strategy_profile
from lawim_v2.security.constants import (
    ROLE_STATUSES,
    PERMISSION_ACTIONS,
    POLICY_TYPES,
    DEVICE_TYPES,
    DEVICE_TRUST_LEVELS,
    API_KEY_STATUSES,
    SESSION_STATUSES,
    MFA_TYPES,
    MFA_STATUSES,
    AUDIT_EVENT_TYPES,
    AUDIT_SEVERITIES,
    COMPLIANCE_FRAMEWORKS,
    CONSENT_TYPES,
    CONSENT_STATUSES,
    DELETION_TYPES,
    PRIVACY_EXPORT_FORMATS,
    PRIVACY_REQUEST_STATUSES,
    RISK_LEVELS,
    RISK_SIGNAL_TYPES,
    INCIDENT_SEVERITIES,
    INCIDENT_STATUSES,
)
from lawim_v2.security.engines import (
    AuditEngine,
    ComplianceEngine,
    PermissionEngine,
    PrivacyEngine,
    RiskEngine,
    SecurityPlatformEngine,
)
from lawim_v2.security.permissions import evaluate_permissions, matches_permission, permission_key
from lawim_v2.security.policies import evaluate_abac, evaluate_access_policy, evaluate_rbac
from lawim_v2.security.schema_v16_ddl import V16_TABLE_NAMES
from lawim_v2.workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

from tests.lawim_harness import LawimTestHarness


class ReleaseProgramJPersistenceTests(LawimTestHarness):
    def test_schema_version_is_v17(self) -> None:
        self.assertEqual(self.repository.schema_version(), 19)

    def test_application_schema_version_constant(self) -> None:
        self.assertEqual(APPLICATION_SCHEMA_VERSION, 19)

    def test_security_tables_present(self) -> None:
        self.assertTrue(self.repository.security_tables_present())

    def test_all_v16_tables_exist(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V16_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v15_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V15_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v14_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V14_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v13_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V13_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v12_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V12_TABLE_NAMES:
            self.assertIn(table, names)

    def test_v11_tables_still_present(self) -> None:
        names = {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}
        for table in V11_TABLE_NAMES:
            self.assertIn(table, names)

    def test_security_catalog_seeded(self) -> None:
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM iam_roles"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM iam_permissions"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM access_route_policies"), 1)
        self.assertGreaterEqual(self.repository.scalar("SELECT COUNT(*) FROM compliance_policies"), 1)

    def test_v15_to_v16_legacy_migration(self) -> None:
        db_path = Path(tempfile.mkdtemp()) / "v15.sqlite3"
        conn = sqlite3.connect(db_path)
        conn.executescript(SQLITE_INIT_SCRIPT)
        conn.execute("PRAGMA foreign_keys = OFF")
        for table in V16_TABLE_NAMES:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("UPDATE schema_meta SET value='15' WHERE key='schema_version'")
        apply_sqlite_legacy_migrations(conn)
        names = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        conn.close()
        self.assertIn("iam_roles", names)
        for table in V15_TABLE_NAMES:
            self.assertIn(table, names)


class ReleaseProgramJConstantsTests(LawimTestHarness):
    def test_role_statuses_active(self) -> None:
        self.assertIn("active", ROLE_STATUSES)

    def test_role_statuses_inactive(self) -> None:
        self.assertIn("inactive", ROLE_STATUSES)

    def test_role_statuses_archived(self) -> None:
        self.assertIn("archived", ROLE_STATUSES)

    def test_permission_actions_read(self) -> None:
        self.assertIn("read", PERMISSION_ACTIONS)

    def test_permission_actions_write(self) -> None:
        self.assertIn("write", PERMISSION_ACTIONS)

    def test_permission_actions_delete(self) -> None:
        self.assertIn("delete", PERMISSION_ACTIONS)

    def test_permission_actions_admin(self) -> None:
        self.assertIn("admin", PERMISSION_ACTIONS)

    def test_permission_actions_execute(self) -> None:
        self.assertIn("execute", PERMISSION_ACTIONS)

    def test_policy_types_rbac(self) -> None:
        self.assertIn("rbac", POLICY_TYPES)

    def test_policy_types_abac(self) -> None:
        self.assertIn("abac", POLICY_TYPES)

    def test_policy_types_hybrid(self) -> None:
        self.assertIn("hybrid", POLICY_TYPES)

    def test_device_types_browser(self) -> None:
        self.assertIn("browser", DEVICE_TYPES)

    def test_device_types_mobile(self) -> None:
        self.assertIn("mobile", DEVICE_TYPES)

    def test_device_types_desktop(self) -> None:
        self.assertIn("desktop", DEVICE_TYPES)

    def test_device_types_api(self) -> None:
        self.assertIn("api", DEVICE_TYPES)

    def test_device_types_other(self) -> None:
        self.assertIn("other", DEVICE_TYPES)

    def test_device_trust_levels_unknown(self) -> None:
        self.assertIn("unknown", DEVICE_TRUST_LEVELS)

    def test_device_trust_levels_low(self) -> None:
        self.assertIn("low", DEVICE_TRUST_LEVELS)

    def test_device_trust_levels_medium(self) -> None:
        self.assertIn("medium", DEVICE_TRUST_LEVELS)

    def test_device_trust_levels_high(self) -> None:
        self.assertIn("high", DEVICE_TRUST_LEVELS)

    def test_device_trust_levels_trusted(self) -> None:
        self.assertIn("trusted", DEVICE_TRUST_LEVELS)

    def test_api_key_statuses_active(self) -> None:
        self.assertIn("active", API_KEY_STATUSES)

    def test_api_key_statuses_revoked(self) -> None:
        self.assertIn("revoked", API_KEY_STATUSES)

    def test_api_key_statuses_expired(self) -> None:
        self.assertIn("expired", API_KEY_STATUSES)

    def test_session_statuses_active(self) -> None:
        self.assertIn("active", SESSION_STATUSES)

    def test_session_statuses_expired(self) -> None:
        self.assertIn("expired", SESSION_STATUSES)

    def test_session_statuses_revoked(self) -> None:
        self.assertIn("revoked", SESSION_STATUSES)

    def test_mfa_types_totp(self) -> None:
        self.assertIn("totp", MFA_TYPES)

    def test_mfa_types_sms(self) -> None:
        self.assertIn("sms", MFA_TYPES)

    def test_mfa_types_email(self) -> None:
        self.assertIn("email", MFA_TYPES)

    def test_mfa_types_webauthn(self) -> None:
        self.assertIn("webauthn", MFA_TYPES)

    def test_mfa_statuses_pending(self) -> None:
        self.assertIn("pending", MFA_STATUSES)

    def test_mfa_statuses_active(self) -> None:
        self.assertIn("active", MFA_STATUSES)

    def test_mfa_statuses_disabled(self) -> None:
        self.assertIn("disabled", MFA_STATUSES)

    def test_audit_event_types_system(self) -> None:
        self.assertIn("system", AUDIT_EVENT_TYPES)

    def test_audit_event_types_user(self) -> None:
        self.assertIn("user", AUDIT_EVENT_TYPES)

    def test_audit_event_types_admin(self) -> None:
        self.assertIn("admin", AUDIT_EVENT_TYPES)

    def test_audit_event_types_ai(self) -> None:
        self.assertIn("ai", AUDIT_EVENT_TYPES)

    def test_audit_event_types_security(self) -> None:
        self.assertIn("security", AUDIT_EVENT_TYPES)

    def test_audit_severities_debug(self) -> None:
        self.assertIn("debug", AUDIT_SEVERITIES)

    def test_audit_severities_info(self) -> None:
        self.assertIn("info", AUDIT_SEVERITIES)

    def test_audit_severities_warning(self) -> None:
        self.assertIn("warning", AUDIT_SEVERITIES)

    def test_audit_severities_error(self) -> None:
        self.assertIn("error", AUDIT_SEVERITIES)

    def test_audit_severities_critical(self) -> None:
        self.assertIn("critical", AUDIT_SEVERITIES)

    def test_compliance_frameworks_gdpr(self) -> None:
        self.assertIn("gdpr", COMPLIANCE_FRAMEWORKS)

    def test_compliance_frameworks_ccpa(self) -> None:
        self.assertIn("ccpa", COMPLIANCE_FRAMEWORKS)

    def test_compliance_frameworks_local(self) -> None:
        self.assertIn("local", COMPLIANCE_FRAMEWORKS)

    def test_compliance_frameworks_internal(self) -> None:
        self.assertIn("internal", COMPLIANCE_FRAMEWORKS)

    def test_consent_types_marketing(self) -> None:
        self.assertIn("marketing", CONSENT_TYPES)

    def test_consent_types_analytics(self) -> None:
        self.assertIn("analytics", CONSENT_TYPES)

    def test_consent_types_terms(self) -> None:
        self.assertIn("terms", CONSENT_TYPES)

    def test_consent_types_privacy(self) -> None:
        self.assertIn("privacy", CONSENT_TYPES)

    def test_consent_types_cookies(self) -> None:
        self.assertIn("cookies", CONSENT_TYPES)

    def test_consent_statuses_pending(self) -> None:
        self.assertIn("pending", CONSENT_STATUSES)

    def test_consent_statuses_granted(self) -> None:
        self.assertIn("granted", CONSENT_STATUSES)

    def test_consent_statuses_revoked(self) -> None:
        self.assertIn("revoked", CONSENT_STATUSES)

    def test_consent_statuses_expired(self) -> None:
        self.assertIn("expired", CONSENT_STATUSES)

    def test_deletion_types_soft_delete(self) -> None:
        self.assertIn("soft_delete", DELETION_TYPES)

    def test_deletion_types_hard_delete(self) -> None:
        self.assertIn("hard_delete", DELETION_TYPES)

    def test_deletion_types_anonymize(self) -> None:
        self.assertIn("anonymize", DELETION_TYPES)

    def test_privacy_export_formats_json(self) -> None:
        self.assertIn("json", PRIVACY_EXPORT_FORMATS)

    def test_privacy_export_formats_csv(self) -> None:
        self.assertIn("csv", PRIVACY_EXPORT_FORMATS)

    def test_privacy_export_formats_pdf(self) -> None:
        self.assertIn("pdf", PRIVACY_EXPORT_FORMATS)

    def test_privacy_request_statuses_pending(self) -> None:
        self.assertIn("pending", PRIVACY_REQUEST_STATUSES)

    def test_privacy_request_statuses_processing(self) -> None:
        self.assertIn("processing", PRIVACY_REQUEST_STATUSES)

    def test_privacy_request_statuses_completed(self) -> None:
        self.assertIn("completed", PRIVACY_REQUEST_STATUSES)

    def test_privacy_request_statuses_failed(self) -> None:
        self.assertIn("failed", PRIVACY_REQUEST_STATUSES)

    def test_privacy_request_statuses_cancelled(self) -> None:
        self.assertIn("cancelled", PRIVACY_REQUEST_STATUSES)

    def test_risk_levels_low(self) -> None:
        self.assertIn("low", RISK_LEVELS)

    def test_risk_levels_medium(self) -> None:
        self.assertIn("medium", RISK_LEVELS)

    def test_risk_levels_high(self) -> None:
        self.assertIn("high", RISK_LEVELS)

    def test_risk_levels_critical(self) -> None:
        self.assertIn("critical", RISK_LEVELS)

    def test_risk_signal_types_login_anomaly(self) -> None:
        self.assertIn("login_anomaly", RISK_SIGNAL_TYPES)

    def test_risk_signal_types_brute_force(self) -> None:
        self.assertIn("brute_force", RISK_SIGNAL_TYPES)

    def test_risk_signal_types_geo_anomaly(self) -> None:
        self.assertIn("geo_anomaly", RISK_SIGNAL_TYPES)

    def test_risk_signal_types_privilege_escalation(self) -> None:
        self.assertIn("privilege_escalation", RISK_SIGNAL_TYPES)

    def test_risk_signal_types_api_abuse(self) -> None:
        self.assertIn("api_abuse", RISK_SIGNAL_TYPES)

    def test_risk_signal_types_data_exfiltration(self) -> None:
        self.assertIn("data_exfiltration", RISK_SIGNAL_TYPES)

    def test_incident_severities_low(self) -> None:
        self.assertIn("low", INCIDENT_SEVERITIES)

    def test_incident_severities_medium(self) -> None:
        self.assertIn("medium", INCIDENT_SEVERITIES)

    def test_incident_severities_high(self) -> None:
        self.assertIn("high", INCIDENT_SEVERITIES)

    def test_incident_severities_critical(self) -> None:
        self.assertIn("critical", INCIDENT_SEVERITIES)

    def test_incident_statuses_open(self) -> None:
        self.assertIn("open", INCIDENT_STATUSES)

    def test_incident_statuses_investigating(self) -> None:
        self.assertIn("investigating", INCIDENT_STATUSES)

    def test_incident_statuses_contained(self) -> None:
        self.assertIn("contained", INCIDENT_STATUSES)

    def test_incident_statuses_resolved(self) -> None:
        self.assertIn("resolved", INCIDENT_STATUSES)

    def test_incident_statuses_closed(self) -> None:
        self.assertIn("closed", INCIDENT_STATUSES)


class ReleaseProgramJEnginesTests(LawimTestHarness):
    def test_permission_engine_build_grants(self) -> None:
        grants = PermissionEngine().build_grants(permissions=[{"resource": "users", "action": "read"}])
        self.assertIn("users:read", grants)

    def test_permission_engine_evaluate_rbac(self) -> None:
        allowed = PermissionEngine().evaluate(
            role_keys=["role-admin"],
            permission_grants=["security:admin"],
            policy={"policy_type": "rbac", "rules_json": '[{"role": "role-admin"}]'},
        )
        self.assertTrue(allowed)

    def test_permission_engine_user_has_permission(self) -> None:
        ok = PermissionEngine().user_has_permission(grants=["users:read"], resource="users", action="read")
        self.assertTrue(ok)

    def test_permission_engine_user_lacks_permission(self) -> None:
        ok = PermissionEngine().user_has_permission(grants=["users:read"], resource="users", action="delete")
        self.assertFalse(ok)

    def test_audit_engine_genesis_checksum(self) -> None:
        self.assertEqual(len(AuditEngine.GENESIS_CHECKSUM), 64)

    def test_audit_engine_compute_checksum(self) -> None:
        digest = AuditEngine().compute_checksum(
            entry_key="audit-1",
            event_type="system",
            action="init",
            payload={"ok": True},
            previous_checksum=AuditEngine.GENESIS_CHECKSUM,
            created_at="2026-01-01T00:00:00+00:00",
        )
        self.assertEqual(len(digest), 64)

    def test_audit_engine_verify_empty_chain(self) -> None:
        result = AuditEngine().verify_chain([])
        self.assertTrue(result["valid"])

    def test_audit_engine_verify_valid_chain(self) -> None:
        engine = AuditEngine()
        created_at = "2026-01-01T00:00:00+00:00"
        checksum = engine.compute_checksum(
            entry_key="audit-a",
            event_type="system",
            action="seed",
            payload={},
            previous_checksum=engine.GENESIS_CHECKSUM,
            created_at=created_at,
        )
        result = engine.verify_chain([
            {
                "entry_key": "audit-a",
                "event_type": "system",
                "action": "seed",
                "payload_json": "{}",
                "checksum": checksum,
                "created_at": created_at,
            }
        ])
        self.assertTrue(result["valid"])

    def test_compliance_engine_consent_valid(self) -> None:
        ok = ComplianceEngine().consent_valid(
            consent={"consent_type": "terms", "status": "granted"},
            consent_type="terms",
        )
        self.assertTrue(ok)

    def test_compliance_engine_consent_missing(self) -> None:
        ok = ComplianceEngine().consent_valid(consent=None, consent_type="terms")
        self.assertFalse(ok)

    def test_compliance_engine_retention_due(self) -> None:
        old = (datetime.now(timezone.utc) - timedelta(days=400)).replace(microsecond=0).isoformat()
        due = ComplianceEngine().retention_due(created_at=old, retention_days=365)
        self.assertTrue(due)

    def test_compliance_engine_retention_not_due(self) -> None:
        recent = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        due = ComplianceEngine().retention_due(created_at=recent, retention_days=365)
        self.assertFalse(due)

    def test_compliance_engine_check_policy_compliant(self) -> None:
        result = ComplianceEngine().check_policy(
            policy={"framework": "internal", "rules_json": '[{"field": "audit_trail", "required": true}]'},
            context={"audit_trail": True},
        )
        self.assertTrue(result["compliant"])

    def test_compliance_engine_check_policy_violation(self) -> None:
        result = ComplianceEngine().check_policy(
            policy={"framework": "gdpr", "rules_json": '[{"field": "consent", "required": true}]'},
            context={},
        )
        self.assertFalse(result["compliant"])

    def test_risk_engine_score_signal(self) -> None:
        scored = RiskEngine().score_signal(signal_type="brute_force", severity="high", base_score=40)
        self.assertEqual(scored["signal_type"], "brute_force")

    def test_risk_engine_auto_lock_threshold(self) -> None:
        self.assertEqual(RiskEngine.AUTO_LOCK_THRESHOLD, 80)

    def test_risk_engine_level_for_score_critical(self) -> None:
        self.assertEqual(RiskEngine().level_for_score(85), "critical")

    def test_risk_engine_level_for_score_low(self) -> None:
        self.assertEqual(RiskEngine().level_for_score(10), "low")

    def test_risk_engine_aggregate(self) -> None:
        result = RiskEngine().aggregate(signals=[{"signal_type": "login_anomaly", "score_delta": 15}], base_score=20)
        self.assertGreaterEqual(result["score"], 35)

    def test_risk_engine_aggregate_auto_lock(self) -> None:
        result = RiskEngine().aggregate(
            signals=[{"signal_type": "api_abuse", "score_delta": 50}, {"signal_type": "brute_force", "score_delta": 35}],
            base_score=0,
        )
        self.assertTrue(result["auto_lock"])

    def test_privacy_engine_default_scope(self) -> None:
        scope = PrivacyEngine().normalize_scope(None)
        self.assertIn("profile", scope)

    def test_privacy_engine_normalize_scope_filters(self) -> None:
        scope = PrivacyEngine().normalize_scope(["profile", "invalid"])
        self.assertEqual(scope, ["profile"])

    def test_privacy_engine_validate_erasure_valid(self) -> None:
        result = PrivacyEngine().validate_erasure(scope={"user_id": 1})
        self.assertTrue(result["valid"])

    def test_privacy_engine_validate_erasure_subject_required(self) -> None:
        result = PrivacyEngine().validate_erasure(scope={})
        self.assertIn("subject_required", result["errors"])

    def test_privacy_engine_export_payload(self) -> None:
        payload = PrivacyEngine().export_payload(scope=["profile"], data={"profile": {"id": 1}, "ignored": 2})
        self.assertIn("profile", payload)

    def test_platform_engine_has_subengines(self) -> None:
        engine = SecurityPlatformEngine()
        self.assertIsInstance(engine.permission, PermissionEngine)

    def test_platform_engine_has_audit_engine(self) -> None:
        engine = SecurityPlatformEngine()
        self.assertIsInstance(engine.audit, AuditEngine)

    def test_platform_engine_has_compliance_engine(self) -> None:
        engine = SecurityPlatformEngine()
        self.assertIsInstance(engine.compliance, ComplianceEngine)

    def test_platform_engine_has_risk_engine(self) -> None:
        engine = SecurityPlatformEngine()
        self.assertIsInstance(engine.risk, RiskEngine)

    def test_platform_engine_has_privacy_engine(self) -> None:
        engine = SecurityPlatformEngine()
        self.assertIsInstance(engine.privacy, PrivacyEngine)

    def test_platform_integration_sources(self) -> None:
        self.assertIn("marketplace", SecurityPlatformEngine().integration_sources())


class ReleaseProgramJPermissionsTests(LawimTestHarness):
    def test_permission_key_users_read(self) -> None:
        self.assertEqual(permission_key("users", "read"), "users:read")

    def test_permission_key_normalizes_resource(self) -> None:
        self.assertEqual(permission_key(" Users ", "read"), "users:read")

    def test_permission_key_invalid_action_defaults_read(self) -> None:
        self.assertEqual(permission_key("users", "invalid"), "users:read")

    def test_permission_key_wildcard_resource(self) -> None:
        self.assertEqual(permission_key("", "admin"), "*:admin")

    def test_matches_permission_exact(self) -> None:
        self.assertTrue(matches_permission(granted="users:read", required="users:read"))

    def test_matches_permission_wildcard_action(self) -> None:
        self.assertTrue(matches_permission(granted="users:admin", required="users:read"))

    def test_matches_permission_wildcard_resource(self) -> None:
        self.assertTrue(matches_permission(granted="*:read", required="users:read"))

    def test_matches_permission_denied(self) -> None:
        self.assertFalse(matches_permission(granted="users:read", required="roles:write"))

    def test_evaluate_permissions_all_required(self) -> None:
        ok = evaluate_permissions(grants=["users:read", "roles:write"], required=["users:read"])
        self.assertTrue(ok)

    def test_evaluate_permissions_missing_grant(self) -> None:
        ok = evaluate_permissions(grants=["users:read"], required=["users:read", "users:delete"])
        self.assertFalse(ok)

    def test_evaluate_permissions_empty_required(self) -> None:
        self.assertTrue(evaluate_permissions(grants=[], required=[]))

    def test_evaluate_rbac_role_match(self) -> None:
        self.assertTrue(evaluate_rbac(role_keys=["role-admin"], required_roles=["role-admin"]))

    def test_evaluate_rbac_role_prefix(self) -> None:
        self.assertTrue(evaluate_rbac(role_keys=["admin"], required_roles=["role-admin"]))

    def test_evaluate_rbac_no_match(self) -> None:
        self.assertFalse(evaluate_rbac(role_keys=["role-agent"], required_roles=["role-admin"]))

    def test_evaluate_abac_eq_pass(self) -> None:
        ok = evaluate_abac(attributes={"region": "Littoral"}, rules=[{"attribute": "region", "operator": "eq", "value": "Littoral"}])
        self.assertTrue(ok)

    def test_evaluate_abac_eq_fail(self) -> None:
        ok = evaluate_abac(attributes={"region": "Centre"}, rules=[{"attribute": "region", "operator": "eq", "value": "Littoral"}])
        self.assertFalse(ok)

    def test_evaluate_abac_in_pass(self) -> None:
        ok = evaluate_abac(attributes={"role": "admin"}, rules=[{"attribute": "role", "operator": "in", "value": ["admin", "agent"]}])
        self.assertTrue(ok)

    def test_evaluate_abac_gte_pass(self) -> None:
        ok = evaluate_abac(attributes={"score": 80}, rules=[{"attribute": "score", "operator": "gte", "value": 60}])
        self.assertTrue(ok)

    def test_evaluate_access_policy_rbac(self) -> None:
        ok = evaluate_access_policy(
            role_keys=["role-admin"],
            permission_grants=["security:admin"],
            attributes={},
            policy={"policy_type": "rbac", "rules_json": '[{"role": "role-admin", "permission": "security:admin"}]'},
        )
        self.assertTrue(ok)

    def test_evaluate_access_policy_abac(self) -> None:
        ok = evaluate_access_policy(
            role_keys=[],
            permission_grants=[],
            attributes={"clearance": "high"},
            policy={"policy_type": "abac", "rules_json": '[{"attribute": "clearance", "operator": "eq", "value": "high"}]'},
        )
        self.assertTrue(ok)

    def test_evaluate_access_policy_hybrid(self) -> None:
        ok = evaluate_access_policy(
            role_keys=["role-admin"],
            permission_grants=["security:admin"],
            attributes={"region": "Littoral"},
            policy={
                "policy_type": "hybrid",
                "rules_json": '[{"role": "role-admin"}, {"permission": "security:admin"}, {"attribute": "region", "operator": "eq", "value": "Littoral"}]',
            },
        )
        self.assertTrue(ok)

class ReleaseProgramJRepositoryTests(LawimTestHarness):
    def _user_id(self) -> int:
        return int(self.repository.one("SELECT id FROM users LIMIT 1")["id"])

    def _role_id(self) -> int:
        return int(self.repository.one("SELECT id FROM iam_roles LIMIT 1")["id"])

    def _permission_id(self) -> int:
        return int(self.repository.one("SELECT id FROM iam_permissions LIMIT 1")["id"])

    def test_list_iam_roles(self) -> None:
        rows = self.repository.list_iam_roles()
        self.assertIsInstance(rows, list)

    def test_create_iam_role(self) -> None:
        role = self.repository.create_iam_role(name="Repo Role", role_key="role-repo-test")
        self.assertEqual(role["name"], "Repo Role")

    def test_get_iam_role(self) -> None:
        role = self.repository.create_iam_role(name="Get Role", role_key="role-get-test")
        row = self.repository.get_iam_role(int(role["id"]))
        self.assertEqual(row["role_key"], "role-get-test")

    def test_update_iam_role(self) -> None:
        role = self.repository.create_iam_role(name="Update Role", role_key="role-upd-test")
        updated = self.repository.update_iam_role(int(role["id"]), name="Updated Role")
        self.assertEqual(updated["name"], "Updated Role")

    def test_list_iam_permissions(self) -> None:
        rows = self.repository.list_iam_permissions()
        self.assertGreaterEqual(len(rows), 1)

    def test_create_iam_permission(self) -> None:
        perm = self.repository.create_iam_permission(name="Repo Perm", resource="reports", action="read")
        self.assertEqual(perm["resource"], "reports")

    def test_get_iam_permission(self) -> None:
        perm = self.repository.create_iam_permission(name="Get Perm", permission_key="perm-get-test")
        row = self.repository.get_iam_permission(int(perm["id"]))
        self.assertEqual(row["permission_key"], "perm-get-test")

    def test_assign_user_role(self) -> None:
        assignment = self.repository.assign_user_role(user_id=self._user_id(), role_id=self._role_id())
        self.assertEqual(int(assignment["user_id"]), self._user_id())

    def test_list_user_roles(self) -> None:
        roles = self.repository.list_user_roles(user_id=self._user_id())
        self.assertIsInstance(roles, list)

    def test_grant_role_permission(self) -> None:
        grant = self.repository.grant_role_permission(role_id=self._role_id(), permission_id=self._permission_id())
        self.assertEqual(int(grant["role_id"]), self._role_id())

    def test_create_iam_group(self) -> None:
        group = self.repository.create_iam_group(name="Repo Group")
        self.assertIn("group_key", group)

    def test_add_group_member(self) -> None:
        group = self.repository.create_iam_group(name="Member Group")
        member = self.repository.add_group_member(group_id=int(group["id"]), user_id=self._user_id())
        self.assertEqual(int(member["user_id"]), self._user_id())

    def test_list_iam_groups(self) -> None:
        groups = self.repository.list_iam_groups()
        self.assertIsInstance(groups, list)

    def test_create_iam_team(self) -> None:
        team = self.repository.create_iam_team(name="Repo Team")
        self.assertIn("team_key", team)

    def test_add_team_member(self) -> None:
        team = self.repository.create_iam_team(name="Member Team")
        member = self.repository.add_team_member(team_id=int(team["id"]), user_id=self._user_id())
        self.assertEqual(int(member["user_id"]), self._user_id())

    def test_list_iam_teams(self) -> None:
        teams = self.repository.list_iam_teams()
        self.assertIsInstance(teams, list)

    def test_create_iam_access_policy(self) -> None:
        policy = self.repository.create_iam_access_policy(name="Repo Policy")
        self.assertIn("policy_key", policy)

    def test_list_iam_access_policies(self) -> None:
        policies = self.repository.list_iam_access_policies()
        self.assertGreaterEqual(len(policies), 1)

    def test_bind_iam_policy(self) -> None:
        policy = self.repository.create_iam_access_policy(name="Bind Policy")
        binding = self.repository.bind_iam_policy(policy_id=int(policy["id"]), binding_type="role", binding_id=self._role_id())
        self.assertEqual(int(binding["policy_id"]), int(policy["id"]))

    def test_list_access_route_policies(self) -> None:
        routes = self.repository.list_access_route_policies()
        self.assertGreaterEqual(len(routes), 1)

    def test_list_security_users(self) -> None:
        users = self.repository.list_security_users()
        self.assertGreaterEqual(len(users), 1)

    def test_get_security_user(self) -> None:
        user = self.repository.get_security_user(self._user_id())
        self.assertIn("iam_roles", user)

    def test_register_access_device(self) -> None:
        device = self.repository.register_access_device(user_id=self._user_id(), device_name="Repo Browser")
        self.assertEqual(device["device_name"], "Repo Browser")

    def test_list_access_devices(self) -> None:
        devices = self.repository.list_access_devices(user_id=self._user_id())
        self.assertIsInstance(devices, list)

    def test_update_access_device(self) -> None:
        device = self.repository.register_access_device(user_id=self._user_id())
        updated = self.repository.update_access_device(int(device["id"]), trust_level="high")
        self.assertEqual(updated["trust_level"], "high")

    def test_create_api_key(self) -> None:
        api_key = self.repository.create_api_key(user_id=self._user_id(), name="Repo Key")
        self.assertIn("secret", api_key)

    def test_list_access_api_keys(self) -> None:
        keys = self.repository.list_access_api_keys(user_id=self._user_id())
        self.assertIsInstance(keys, list)

    def test_revoke_api_key(self) -> None:
        api_key = self.repository.create_api_key(user_id=self._user_id(), name="Revoke Key")
        revoked = self.repository.revoke_api_key(int(api_key["id"]))
        self.assertEqual(revoked["status"], "revoked")

    def test_record_access_session(self) -> None:
        session = self.repository.record_access_session(user_id=self._user_id(), ip_address="127.0.0.1")
        self.assertEqual(session["status"], "active")

    def test_list_access_session_records(self) -> None:
        sessions = self.repository.list_access_session_records(user_id=self._user_id())
        self.assertIsInstance(sessions, list)

    def test_revoke_session_record(self) -> None:
        session = self.repository.record_access_session(user_id=self._user_id())
        revoked = self.repository.revoke_session_record(int(session["id"]))
        self.assertEqual(revoked["status"], "revoked")

    def test_record_audit_trail(self) -> None:
        entry = self.repository.record_audit_trail(action="repo_test", event_type="system")
        self.assertIn("entry_key", entry)

    def test_list_audit_trail(self) -> None:
        entries = self.repository.list_audit_trail(limit=5)
        self.assertIsInstance(entries, list)

    def test_verify_audit_trail(self) -> None:
        result = self.repository.verify_audit_trail(limit=20)
        self.assertIn("valid", result)

    def test_list_compliance_policies(self) -> None:
        policies = self.repository.list_compliance_policies()
        self.assertGreaterEqual(len(policies), 1)

    def test_grant_compliance_consent(self) -> None:
        consent = self.repository.grant_compliance_consent(user_id=self._user_id(), consent_type="terms")
        self.assertEqual(consent["status"], "granted")

    def test_list_compliance_consents(self) -> None:
        consents = self.repository.list_compliance_consents(user_id=self._user_id())
        self.assertIsInstance(consents, list)

    def test_list_compliance_retention_rules(self) -> None:
        rules = self.repository.list_compliance_retention_rules()
        self.assertGreaterEqual(len(rules), 1)

    def test_create_compliance_deletion_request(self) -> None:
        request = self.repository.create_compliance_deletion_request(user_id=self._user_id())
        self.assertEqual(request["status"], "pending")

    def test_list_compliance_deletion_requests(self) -> None:
        requests = self.repository.list_compliance_deletion_requests()
        self.assertIsInstance(requests, list)

    def test_create_privacy_export(self) -> None:
        export = self.repository.create_privacy_export(user_id=self._user_id())
        self.assertEqual(export["status"], "pending")

    def test_list_privacy_exports(self) -> None:
        exports = self.repository.list_privacy_exports(user_id=self._user_id())
        self.assertIsInstance(exports, list)

    def test_create_privacy_erasure_request(self) -> None:
        request = self.repository.create_privacy_erasure_request(user_id=self._user_id(), scope={"user_id": self._user_id()})
        self.assertIn(request["status"], {"pending", "failed"})

    def test_list_privacy_erasure_requests(self) -> None:
        requests = self.repository.list_privacy_erasure_requests()
        self.assertIsInstance(requests, list)

    def test_record_risk_signal(self) -> None:
        signal = self.repository.record_risk_signal(user_id=self._user_id(), signal_type="login_anomaly", severity="medium")
        self.assertIn("signal_key", signal)

    def test_list_risk_signals(self) -> None:
        signals = self.repository.list_risk_signals(user_id=self._user_id())
        self.assertIsInstance(signals, list)

    def test_compute_risk_score(self) -> None:
        score = self.repository.compute_risk_score(user_id=self._user_id())
        self.assertIn("score", score)

    def test_get_risk_score(self) -> None:
        score = self.repository.get_risk_score(self._user_id())
        self.assertIn("level", score)

    def test_list_risk_alerts(self) -> None:
        alerts = self.repository.list_risk_alerts()
        self.assertIsInstance(alerts, list)

    def test_create_security_incident(self) -> None:
        incident = self.repository.create_security_incident(title="Repo Incident")
        self.assertEqual(incident["status"], "open")

    def test_list_security_incidents(self) -> None:
        incidents = self.repository.list_security_incidents()
        self.assertIsInstance(incidents, list)

    def test_update_security_incident(self) -> None:
        incident = self.repository.create_security_incident(title="Update Incident")
        updated = self.repository.update_security_incident(int(incident["id"]), status="investigating")
        self.assertEqual(updated["status"], "investigating")

    def test_snapshot_security_analytics(self) -> None:
        metrics = self.repository.snapshot_security_analytics()
        self.assertIn("roles", metrics)

    def test_security_analytics(self) -> None:
        analytics = self.repository.security_analytics()
        self.assertIn("metrics", analytics)

    def test_security_dashboard(self) -> None:
        dashboard = self.repository.security_dashboard()
        self.assertIn("integrations", dashboard)

    def test_security_stats(self) -> None:
        stats = self.repository.security_stats()
        self.assertIn("active_roles", stats)

    def test_integration_sources(self) -> None:
        payload = self.repository.integration_sources()
        self.assertIn("programs", payload)

    def test_seed_security_catalog_idempotent(self) -> None:
        before = self.repository.scalar("SELECT COUNT(*) FROM iam_roles")
        self.repository.seed_security_catalog()
        after = self.repository.scalar("SELECT COUNT(*) FROM iam_roles")
        self.assertEqual(before, after)


class ReleaseProgramJApiTests(LawimTestHarness):
    def _admin_token(self) -> str:
        return self.login(email="admin@lawim.local")

    def _user_id(self) -> int:
        return int(self.repository.one("SELECT id FROM users LIMIT 1")["id"])

    def _role_id(self) -> int:
        return int(self.repository.one("SELECT id FROM iam_roles LIMIT 1")["id"])

    def test_integrations_api_no_auth(self) -> None:
        response = self.invoke("/api/v2/security/integrations")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("sources", response.body_json())

    def test_users_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/users", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("users", response.body_json())

    def test_roles_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/roles", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("roles", response.body_json())

    def test_permissions_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/permissions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("permissions", response.body_json())

    def test_policies_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/policies", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("policies", response.body_json())

    def test_sessions_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/sessions", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("sessions", response.body_json())

    def test_devices_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/devices", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("devices", response.body_json())

    def test_api_keys_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/api-keys", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("api_keys", response.body_json())

    def test_audit_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/audit", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("entries", response.body_json())

    def test_compliance_policies_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/compliance/policies", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("policies", response.body_json())

    def test_compliance_consents_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/compliance/consents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("consents", response.body_json())

    def test_compliance_retention_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/compliance/retention", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("rules", response.body_json())

    def test_privacy_exports_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/privacy/exports", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("exports", response.body_json())

    def test_privacy_erasure_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/privacy/erasure", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("requests", response.body_json())

    def test_risk_signals_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/risk/signals", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("signals", response.body_json())

    def test_risk_alerts_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/risk/alerts", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("alerts", response.body_json())

    def test_incidents_list_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/incidents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("incidents", response.body_json())

    def test_analytics_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/analytics", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("analytics", response.body_json())

    def test_stats_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/stats", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("stats", response.body_json())

    def test_dashboard_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/dashboard", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("dashboard", response.body_json())

    def test_user_detail_api(self) -> None:
        token = self._admin_token()
        token = self._admin_token()
        user_id = self._user_id()
        response = self.invoke(f"/api/v2/security/users/{user_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("user", response.body_json())

    def test_risk_score_api(self) -> None:
        token = self._admin_token()
        token = self._admin_token()
        user_id = self._user_id()
        response = self.invoke(f"/api/v2/security/risk/scores/{user_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("risk_score", response.body_json())

    def test_create_role_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/roles", method="POST", token=token, body={"name": "API Role"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("role", response.body_json())

    def test_create_permission_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/permissions", method="POST", token=token, body={"name": "API Permission", "resource": "audit", "action": "read"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("permission", response.body_json())

    def test_create_policy_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/policies", method="POST", token=token, body={"name": "API Policy"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("policy", response.body_json())

    def test_create_api_key_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/api-keys", method="POST", token=token, body={"name": "API Key"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("api_key", response.body_json())

    def test_record_audit_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/audit", method="POST", token=token, body={"action": "api_test"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("audit_entry", response.body_json())

    def test_create_deletion_request_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/compliance/deletion", method="POST", token=token, body={"deletion_type": "soft_delete"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("deletion_request", response.body_json())

    def test_create_privacy_export_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/privacy/exports", method="POST", token=token, body={"format": "json"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("export", response.body_json())

    def test_create_privacy_erasure_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/privacy/erasure", method="POST", token=token, body={"scope": {"user_id": 1}})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("request", response.body_json())

    def test_record_risk_signal_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/risk/signals", method="POST", token=token, body={"user_id": 1, "signal_type": "login_anomaly"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("signal", response.body_json())

    def test_create_incident_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/incidents", method="POST", token=token, body={"title": "API Incident"})
        self.assertEqual(response.status, HTTPStatus.CREATED)
        self.assertIn("incident", response.body_json())

    def test_seed_catalog_api(self) -> None:
        token = self._admin_token()
        response = self.invoke("/api/v2/security/seed", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("seeded", response.body_json())

    def test_assign_user_role_api(self) -> None:
        token = self._admin_token()
        token = self._admin_token()
        user_id = self._user_id()
        role_id = self._role_id()
        response = self.invoke(f"/api/v2/security/users/{user_id}/roles", method="POST", token=token, body={"role_id": role_id})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("user_role", response.body_json())

    def test_revoke_session_api(self) -> None:
        token = self._admin_token()
        token = self._admin_token()
        session = self.repository.record_access_session(user_id=self._user_id())
        session_id = int(session["id"])
        response = self.invoke(f"/api/v2/security/sessions/{session_id}/revoke", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("session", response.body_json())

    def test_revoke_api_key_api(self) -> None:
        token = self._admin_token()
        token = self._admin_token()
        api_key = self.repository.create_api_key(user_id=self._user_id(), name="Revoke API Key")
        api_key_id = int(api_key["id"])
        response = self.invoke(f"/api/v2/security/api-keys/{api_key_id}/revoke", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("api_key", response.body_json())

    def test_grant_consent_api(self) -> None:
        token = self._admin_token()
        consent = self.repository.grant_compliance_consent(user_id=self._user_id(), consent_type="privacy")
        consent_id = int(consent["id"])
        response = self.invoke(f"/api/v2/security/compliance/consents/{consent_id}/grant", method="POST", token=token, body={})
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertIn("consent", response.body_json())


class ReleaseProgramJUiTests(LawimTestHarness):
    def test_index_has_security_section(self) -> None:
        html = self.invoke("/")
        self.assertIn("Security &amp; Compliance", html.body_text())

    def test_app_js_references_refresh_security_admin(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("refreshSecurityAdmin", js.body_text())

    def test_app_js_references_security_stats_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/security/stats", js.body_text())

    def test_app_js_references_security_audit_api(self) -> None:
        js = self.invoke("/app.js")
        self.assertIn("/api/v2/security/audit", js.body_text())

    def test_index_has_security_admin_stats(self) -> None:
        html = self.invoke("/")
        self.assertIn('id="security-admin-stats"', html.body_text())


class ReleaseProgramJHealthTests(LawimTestHarness):
    def test_health_schema_v17(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.body_json()["database"]["schema_version"], 18)

    def test_migration_strategy_v17(self) -> None:
        self.assertEqual(migration_strategy_profile()["schema_version"], 18)

    def test_bootstrap_schema_v17(self) -> None:
        bootstrap = self.invoke("/api/bootstrap")
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        self.assertEqual(self.repository.schema_version(), 19)

    def test_metrics_include_security_counters(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/stats", token=token)
        metrics = self.invoke("/api/metrics", token=token)
        snapshot = metrics.body_json()["metrics"]
        self.assertGreaterEqual(snapshot.get("security_requests_total", 0), 1)


class ReleaseProgramJV16TableTests(LawimTestHarness):
    def _table_names(self) -> set[str]:
        return {row["name"] for row in self.repository.all("SELECT name FROM sqlite_master WHERE type='table'")}

    def test_v16_table_iam_roles(self) -> None:
        self.assertIn("iam_roles", self._table_names())

    def test_v16_table_iam_permissions(self) -> None:
        self.assertIn("iam_permissions", self._table_names())

    def test_v16_table_iam_role_permissions(self) -> None:
        self.assertIn("iam_role_permissions", self._table_names())

    def test_v16_table_iam_user_roles(self) -> None:
        self.assertIn("iam_user_roles", self._table_names())

    def test_v16_table_iam_groups(self) -> None:
        self.assertIn("iam_groups", self._table_names())

    def test_v16_table_iam_group_members(self) -> None:
        self.assertIn("iam_group_members", self._table_names())

    def test_v16_table_iam_teams(self) -> None:
        self.assertIn("iam_teams", self._table_names())

    def test_v16_table_iam_team_members(self) -> None:
        self.assertIn("iam_team_members", self._table_names())

    def test_v16_table_iam_access_policies(self) -> None:
        self.assertIn("iam_access_policies", self._table_names())

    def test_v16_table_iam_policy_bindings(self) -> None:
        self.assertIn("iam_policy_bindings", self._table_names())

    def test_v16_table_access_devices(self) -> None:
        self.assertIn("access_devices", self._table_names())

    def test_v16_table_access_api_keys(self) -> None:
        self.assertIn("access_api_keys", self._table_names())

    def test_v16_table_access_session_records(self) -> None:
        self.assertIn("access_session_records", self._table_names())

    def test_v16_table_access_route_policies(self) -> None:
        self.assertIn("access_route_policies", self._table_names())

    def test_v16_table_access_mfa_enrollments(self) -> None:
        self.assertIn("access_mfa_enrollments", self._table_names())

    def test_v16_table_access_token_rotations(self) -> None:
        self.assertIn("access_token_rotations", self._table_names())

    def test_v16_table_audit_trail_entries(self) -> None:
        self.assertIn("audit_trail_entries", self._table_names())

    def test_v16_table_audit_system_events(self) -> None:
        self.assertIn("audit_system_events", self._table_names())

    def test_v16_table_audit_user_events(self) -> None:
        self.assertIn("audit_user_events", self._table_names())

    def test_v16_table_audit_admin_events(self) -> None:
        self.assertIn("audit_admin_events", self._table_names())

    def test_v16_table_audit_ai_events(self) -> None:
        self.assertIn("audit_ai_events", self._table_names())

    def test_v16_table_compliance_policies(self) -> None:
        self.assertIn("compliance_policies", self._table_names())

    def test_v16_table_compliance_consents(self) -> None:
        self.assertIn("compliance_consents", self._table_names())

    def test_v16_table_compliance_retention_rules(self) -> None:
        self.assertIn("compliance_retention_rules", self._table_names())

    def test_v16_table_compliance_deletion_requests(self) -> None:
        self.assertIn("compliance_deletion_requests", self._table_names())

    def test_v16_table_privacy_data_exports(self) -> None:
        self.assertIn("privacy_data_exports", self._table_names())

    def test_v16_table_privacy_erasure_requests(self) -> None:
        self.assertIn("privacy_erasure_requests", self._table_names())

    def test_v16_table_risk_signals(self) -> None:
        self.assertIn("risk_signals", self._table_names())

    def test_v16_table_risk_scores(self) -> None:
        self.assertIn("risk_scores", self._table_names())

    def test_v16_table_risk_alerts(self) -> None:
        self.assertIn("risk_alerts", self._table_names())

    def test_v16_table_security_incidents(self) -> None:
        self.assertIn("security_incidents", self._table_names())

    def test_v16_table_security_analytics_snapshots(self) -> None:
        self.assertIn("security_analytics_snapshots", self._table_names())


class ReleaseProgramJIntegrationTests(LawimTestHarness):
    def test_program_a_projects_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/projects", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_b_partners_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/partners", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_c_decisions_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        project_id = int(self.invoke("/api/v2/projects?limit=1", token=token).body_json()["projects"][0]["id"])
        response = self.invoke(f"/api/v2/decisions?project_id={project_id}", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_d_assistant_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/assistant/agents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_e_knowledge_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/knowledge/documents", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_f_workflow_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/workflows/instances", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_g_rei_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/properties", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_h_crm_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/crm/contacts", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_program_i_marketplace_route_still_works(self) -> None:
        token = self.login(email="agent@lawim.local")
        response = self.invoke("/api/v2/marketplace/providers", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)

    def test_integration_sources_include_marketplace(self) -> None:
        payload = self.repository.integration_sources()
        self.assertTrue(payload["programs"]["marketplace"])

    def test_integration_sources_include_crm(self) -> None:
        payload = self.repository.integration_sources()
        self.assertTrue(payload["programs"]["crm"])

    def test_integration_sources_engine_sources(self) -> None:
        payload = self.repository.integration_sources()
        self.assertIn("marketplace", payload["sources"])

class ReleaseProgramJObservabilityTests(LawimTestHarness):
    def _admin_metrics(self) -> dict[str, object]:
        return self.invoke("/api/metrics", token=self.login(email="admin@lawim.local")).body_json()["metrics"]

    def test_security_stats_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/stats", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_roles_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/roles", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_permissions_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/permissions", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_sessions_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/sessions", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_audit_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/audit", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_dashboard_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/dashboard", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_analytics_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/analytics", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

    def test_security_incidents_counter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.invoke("/api/v2/security/incidents", token=token)
        metrics = self._admin_metrics()
        self.assertGreaterEqual(metrics.get("security_requests_total", 0), 1)

