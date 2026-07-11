from __future__ import annotations

ROLE_STATUSES: frozenset[str] = frozenset({"active", "inactive", "archived"})
PERMISSION_ACTIONS: frozenset[str] = frozenset({"read", "write", "delete", "admin", "execute"})
POLICY_TYPES: frozenset[str] = frozenset({"rbac", "abac", "hybrid"})
DEVICE_TYPES: frozenset[str] = frozenset({"browser", "mobile", "desktop", "api", "other"})
DEVICE_TRUST_LEVELS: frozenset[str] = frozenset({"unknown", "low", "medium", "high", "trusted"})
API_KEY_STATUSES: frozenset[str] = frozenset({"active", "revoked", "expired"})
SESSION_STATUSES: frozenset[str] = frozenset({"active", "expired", "revoked"})
MFA_TYPES: frozenset[str] = frozenset({"totp", "sms", "email", "webauthn"})
MFA_STATUSES: frozenset[str] = frozenset({"pending", "active", "disabled"})
AUDIT_EVENT_TYPES: frozenset[str] = frozenset({"system", "user", "admin", "ai", "security"})
AUDIT_SEVERITIES: frozenset[str] = frozenset({"debug", "info", "warning", "error", "critical"})
COMPLIANCE_FRAMEWORKS: frozenset[str] = frozenset({"gdpr", "ccpa", "local", "internal"})
CONSENT_TYPES: frozenset[str] = frozenset({"marketing", "analytics", "terms", "privacy", "cookies"})
CONSENT_STATUSES: frozenset[str] = frozenset({"pending", "granted", "revoked", "expired"})
DELETION_TYPES: frozenset[str] = frozenset({"soft_delete", "hard_delete", "anonymize"})
PRIVACY_EXPORT_FORMATS: frozenset[str] = frozenset({"json", "csv", "pdf"})
PRIVACY_REQUEST_STATUSES: frozenset[str] = frozenset({"pending", "processing", "completed", "failed", "cancelled"})
RISK_LEVELS: frozenset[str] = frozenset({"low", "medium", "high", "critical"})
RISK_SIGNAL_TYPES: frozenset[str] = frozenset(
    {"login_anomaly", "brute_force", "geo_anomaly", "privilege_escalation", "api_abuse", "data_exfiltration"}
)
INCIDENT_SEVERITIES: frozenset[str] = frozenset({"low", "medium", "high", "critical"})
INCIDENT_STATUSES: frozenset[str] = frozenset({"open", "investigating", "contained", "resolved", "closed"})

DEFAULT_ROLES: tuple[tuple[str, str, str], ...] = (
    ("role-admin", "Administrator", "Full platform administration"),
    ("role-agent", "Agent", "Operational agent access"),
    ("role-owner", "Owner", "Property owner access"),
    ("role-auditor", "Auditor", "Read-only audit and compliance"),
    ("role-security-admin", "Security Admin", "Security and IAM management"),
)

DEFAULT_PERMISSIONS: tuple[tuple[str, str, str, str], ...] = (
    ("perm-users-read", "Read Users", "users", "read"),
    ("perm-users-write", "Write Users", "users", "write"),
    ("perm-roles-read", "Read Roles", "roles", "read"),
    ("perm-roles-write", "Write Roles", "roles", "write"),
    ("perm-audit-read", "Read Audit", "audit", "read"),
    ("perm-compliance-read", "Read Compliance", "compliance", "read"),
    ("perm-compliance-write", "Write Compliance", "compliance", "write"),
    ("perm-security-admin", "Security Admin", "security", "admin"),
    ("perm-api-keys-manage", "Manage API Keys", "api_keys", "write"),
    ("perm-privacy-export", "Privacy Export", "privacy", "execute"),
    ("perm-backup-read", "Read Backup", "backup", "read"),
    ("perm-backup-write", "Run Backup", "backup", "write"),
    ("perm-backup-restore", "Restore Backup", "backup", "execute"),
    ("perm-backup-admin", "Manage Backup", "backup", "admin"),
)
