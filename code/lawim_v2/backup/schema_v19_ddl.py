from __future__ import annotations

from ..program_m_support import build_postgresql_statements, build_sqlite_tables_script

BACKUP_TABLE_NAMES: tuple[str, ...] = (
    "backup_configurations",
    "backup_destinations",
    "backup_jobs",
    "backup_artifacts",
    "backup_events",
    "backup_alerts",
    "restore_jobs",
    "restore_results",
    "backup_metrics",
)

SQLITE_BACKUP_TABLES_SCRIPT = build_sqlite_tables_script(BACKUP_TABLE_NAMES)
POSTGRESQL_BACKUP_STATEMENTS = build_postgresql_statements(BACKUP_TABLE_NAMES)

