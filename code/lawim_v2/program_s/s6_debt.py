from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


# ── PostgreSQL / Database ──────────────────────────────────────────────────


@dataclass
class DatabaseMigration:
    migration_id: str = ""
    version: str = ""
    description: str = ""
    sql: str = ""
    rollback_sql: str = ""
    status: str = "PENDING"
    executed_at: str = ""
    duration_ms: int = 0
    checksum: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"migration_id": self.migration_id, "version": self.version,
                "status": self.status}


class MigrationRunner:
    def __init__(self):
        self._migrations: list[DatabaseMigration] = []
        self._executed: list[str] = []

    def add(self, m: DatabaseMigration) -> None:
        self._migrations.append(m)

    def run_all(self) -> list[DatabaseMigration]:
        results: list[DatabaseMigration] = []
        for m in sorted(self._migrations, key=lambda x: x.version):
            if m.version not in self._executed:
                m.status = "EXECUTED"
                m.executed_at = datetime.now(timezone.utc).isoformat()
                self._executed.append(m.version)
                results.append(m)
        return results

    def rollback(self, version: str) -> bool:
        if version in self._executed:
            self._executed.remove(version)
            return True
        return False


# ── RBAC ────────────────────────────────────────────────────────────────────


RBAC_PERMISSIONS: dict[str, list[str]] = {
    "admin": ["*"],
    "manager": ["read", "write", "manage_team"],
    "operator": ["read", "write"],
    "partner": ["read"],
    "user": ["read_own"],
    "tenant_admin": ["read", "write", "manage_tenant"],
    "agent": ["read", "write_conversation", "write_property"],
}


def check_permission(role: str, action: str, resource: str = "") -> bool:
    perms = RBAC_PERMISSIONS.get(role, [])
    if "*" in perms:
        return True
    return action in perms or f"{action}_{resource}" in perms


# ── CI/CD ───────────────────────────────────────────────────────────────────


@dataclass
class PipelineConfig:
    tests: bool = True
    lint: bool = True
    security_scan: bool = True
    build_artifacts: bool = True
    deploy_staging: bool = True
    run_migrations: bool = True
    notify: bool = True


# ── Frontend ────────────────────────────────────────────────────────────────


FRONTEND_REQUIREMENTS: list[str] = [
    "responsive_design", "api_integration", "error_handling",
    "loading_states", "empty_states", "role_based_views",
    "pagination", "search", "form_validation",
]


# ── Notifications ──────────────────────────────────────────────────────────


@dataclass
class NotificationChannel:
    channel: str = ""
    enabled: bool = False
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class NotificationPreference:
    user_id: int = 0
    whatsapp: bool = False
    telegram: bool = False
    email: bool = False
    sms: bool = False
    in_app: bool = True


# ── Technical Debt Item ────────────────────────────────────────────────────


@dataclass
class TechnicalDebtItem:
    debt_id: str = ""
    category: str = ""
    description: str = ""
    severity: str = "MEDIUM"
    status: str = "OPEN"
    resolved_at: str = ""
    evidence: str = ""

    def resolve(self, evidence: str = "") -> None:
        self.status = "RESOLVED"
        self.resolved_at = datetime.now(timezone.utc).isoformat()
        self.evidence = evidence
