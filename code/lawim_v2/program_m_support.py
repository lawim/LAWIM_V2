from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from datetime import datetime, timezone
from dataclasses import dataclass
from typing import Any, Iterable


PROGRAM_M_SCHEMA_VERSION = 19

COMMON_TABLE_COLUMNS: tuple[str, ...] = (
    "id",
    "record_key",
    "name",
    "kind",
    "scope",
    "status",
    "parent_id",
    "reference_id",
    "secondary_id",
    "payload_json",
    "created_at",
    "updated_at",
)


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def json_loads(value: Any, fallback: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if value in (None, ""):
        return fallback
    try:
        return json.loads(str(value))
    except json.JSONDecodeError:
        return fallback


def make_key(prefix: str, *parts: object) -> str:
    payload = "|".join(str(part).strip() for part in parts if str(part).strip())
    if not payload:
        payload = uuid.uuid4().hex
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return f"{prefix}-{digest}"


def row_to_dict(row: dict[str, object], *, json_fields: dict[str, Any] | None = None) -> dict[str, object]:
    payload = dict(row)
    for field, fallback in (json_fields or {}).items():
        payload[field] = json_loads(payload.get(field), fallback)
    return payload


def build_sqlite_tables_script(table_names: Iterable[str]) -> str:
    statements: list[str] = []
    for table in table_names:
        statements.extend(
            [
                f"""
CREATE TABLE IF NOT EXISTS {table} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{{}}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
""".strip(),
                f"CREATE INDEX IF NOT EXISTS idx_{table}_status ON {table}(status, created_at);",
                f"CREATE INDEX IF NOT EXISTS idx_{table}_record_key ON {table}(record_key);",
            ]
        )
    return "\n".join(statements) + ("\n" if statements else "")


def build_postgresql_statements(table_names: Iterable[str]) -> tuple[str, ...]:
    statements: list[str] = []
    for table in table_names:
        statements.extend(
            [
                f"""
CREATE TABLE IF NOT EXISTS {table} (
    id SERIAL PRIMARY KEY,
    record_key TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL DEFAULT '',
    kind TEXT NOT NULL DEFAULT '',
    scope TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'active',
    parent_id INTEGER,
    reference_id INTEGER,
    secondary_id INTEGER,
    payload_json TEXT NOT NULL DEFAULT '{{}}',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
""".strip(),
                f"CREATE INDEX IF NOT EXISTS idx_{table}_status ON {table}(status, created_at)",
                f"CREATE INDEX IF NOT EXISTS idx_{table}_record_key ON {table}(record_key)",
            ]
        )
    return tuple(statements)


def tables_present(repository, table_names: Iterable[str]) -> bool:
    names = tuple(dict.fromkeys(str(name) for name in table_names))
    if not names:
        return True
    if str(getattr(repository, "driver", "sqlite")) == "postgresql":
        placeholders = ", ".join("?" for _ in names)
        rows = repository.all(
            f"SELECT table_name AS name FROM information_schema.tables WHERE table_schema = 'public' AND table_name IN ({placeholders})",
            names,
        )
    else:
        placeholders = ", ".join("?" for _ in names)
        rows = repository.all(
            f"SELECT name FROM sqlite_master WHERE type = 'table' AND name IN ({placeholders})",
            names,
        )
    present = {str(row.get("name") or row.get("table_name")) for row in rows}
    return len(present) == len(names)


def list_rows(repository, table: str, *, limit: int = 50, order_by: str = "id DESC") -> list[dict[str, object]]:
    return [dict(row) for row in repository.all(f"SELECT * FROM {table} ORDER BY {order_by} LIMIT ?", (limit,))]


def count_rows(repository, table: str, *, where: str = "", params: tuple[object, ...] = ()) -> int:
    sql = f"SELECT COUNT(*) FROM {table}"
    if where:
        sql += f" WHERE {where}"
    value = repository.scalar(sql, params)
    return int(value or 0)


def get_row(repository, table: str, *, record_id: int) -> dict[str, object]:
    row = repository.one(f"SELECT * FROM {table} WHERE id = ?", (record_id,))
    if row is None:
        from .errors import NotFoundError

        raise NotFoundError(f"{table[:-1].replace('_', ' ')} not found")
    return dict(row)


def get_row_by_key(repository, table: str, *, record_key: str) -> dict[str, object] | None:
    row = repository.one(f"SELECT * FROM {table} WHERE record_key = ?", (record_key,))
    return dict(row) if row is not None else None


def create_record(
    repository,
    table: str,
    *,
    name: str = "",
    kind: str = "",
    scope: str = "",
    status: str = "active",
    parent_id: int | None = None,
    reference_id: int | None = None,
    secondary_id: int | None = None,
    payload: dict[str, object] | None = None,
    record_key: str | None = None,
) -> dict[str, object]:
    key = record_key or make_key(table.replace("_", "-"), name, kind, scope, parent_id, reference_id, secondary_id)
    now = utcnow()
    with repository._transaction() as conn:  # noqa: SLF001 - shared Program M persistence helper
        conn.execute(
            f"""
            INSERT INTO {table} (
                record_key, name, kind, scope, status, parent_id, reference_id, secondary_id,
                payload_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                key,
                name,
                kind,
                scope,
                status,
                parent_id,
                reference_id,
                secondary_id,
                json_dumps(payload or {}),
                now,
                now,
            ),
        )
    row = repository.one(f"SELECT * FROM {table} WHERE record_key = ?", (key,))
    assert row is not None
    return dict(row)


def update_record(repository, table: str, record_id: int, **fields: object) -> dict[str, object]:
    allowed = {
        "record_key",
        "name",
        "kind",
        "scope",
        "status",
        "parent_id",
        "reference_id",
        "secondary_id",
        "payload",
        "payload_json",
    }
    updates: dict[str, object] = {key: value for key, value in fields.items() if key in allowed and value is not None}
    if "payload" in updates:
        updates["payload_json"] = json_dumps(updates.pop("payload"))
    if not updates:
        return get_row(repository, table, record_id=record_id)
    assignments = ", ".join(f"{column} = ?" for column in updates)
    params = tuple(updates.values()) + (utcnow(), record_id)
    with repository._transaction() as conn:  # noqa: SLF001 - shared Program M persistence helper
        conn.execute(
            f"UPDATE {table} SET {assignments}, updated_at = ? WHERE id = ?",
            params,
        )
    return get_row(repository, table, record_id=record_id)


def seed_records(repository, table: str, rows: Iterable[dict[str, object]]) -> int:
    created = 0
    for row in rows:
        record_key = str(row.get("record_key") or row.get("name") or make_key(table, row.get("kind"), row.get("scope")))
        if get_row_by_key(repository, table, record_key=record_key) is not None:
            continue
        create_record(
            repository,
            table,
            record_key=record_key,
            name=str(row.get("name") or ""),
            kind=str(row.get("kind") or ""),
            scope=str(row.get("scope") or ""),
            status=str(row.get("status") or "active"),
            parent_id=row.get("parent_id") if isinstance(row.get("parent_id"), int) else None,
            reference_id=row.get("reference_id") if isinstance(row.get("reference_id"), int) else None,
            secondary_id=row.get("secondary_id") if isinstance(row.get("secondary_id"), int) else None,
            payload=row.get("payload") if isinstance(row.get("payload"), dict) else {},
        )
        created += 1
    return created


def build_program_m_seed_rows(table_names: Iterable[str], *, package_name: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, table_name in enumerate(dict.fromkeys(str(name) for name in table_names)):
        label = table_name.replace("_", " ").title()
        rows.append(
            {
                "record_key": f"{package_name}:{table_name}",
                "name": label,
                "kind": table_name.split("_", 1)[0],
                "scope": package_name,
                "status": "active",
                "payload": {
                    "package": package_name,
                    "table": table_name,
                    "seeded": True,
                    "position": index,
                },
            }
        )
    return rows


def build_program_m_summary(repository, table_names: Iterable[str], *, package_name: str) -> dict[str, object]:
    names = tuple(dict.fromkeys(str(name) for name in table_names))
    counts = {name: count_rows(repository, name) for name in names}
    return {
        "package": package_name,
        "tables": len(names),
        "rows": sum(counts.values()),
        "counts": counts,
        "present": tables_present(repository, names),
    }


def build_program_m_dashboard(
    repository,
    table_names: Iterable[str],
    *,
    package_name: str,
    limit: int = 5,
) -> dict[str, object]:
    names = tuple(dict.fromkeys(str(name) for name in table_names))
    return {
        "package": package_name,
        "summary": build_program_m_summary(repository, names, package_name=package_name),
        "tables": [
            {
                "name": table_name,
                "count": count_rows(repository, table_name),
                "rows": [row_to_dict(row, json_fields={"payload_json": {}}) for row in repository.all(
                    f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT ?",
                    (limit,),
                )],
            }
            for table_name in names
        ],
    }


class ProgramMRepositoryMixinBase:
    program_m_package_name: str = "program-m"
    program_m_table_names: tuple[str, ...] = ()

    def program_m_tables_present(self, table_names: Iterable[str] | None = None) -> bool:
        return tables_present(self, table_names or self.program_m_table_names)

    def program_m_seed_catalog(self, table_names: Iterable[str] | None = None) -> dict[str, object]:
        names = tuple(dict.fromkeys(str(name) for name in (table_names or self.program_m_table_names)))
        created = 0
        for table_name in names:
            created += seed_records(
                self,
                table_name,
                build_program_m_seed_rows([table_name], package_name=self.program_m_package_name),
            )
        return {
            "package": self.program_m_package_name,
            "seeded": created,
            "tables": len(names),
        }

    def program_m_collection(self, table_name: str, *, limit: int = 50, order_by: str = "id DESC") -> list[dict[str, object]]:
        return [row_to_dict(row, json_fields={"payload_json": {}}) for row in list_rows(self, table_name, limit=limit, order_by=order_by)]

    def program_m_get(self, table_name: str, *, record_id: int) -> dict[str, object]:
        return row_to_dict(get_row(self, table_name, record_id=record_id), json_fields={"payload_json": {}})

    def program_m_get_by_key(self, table_name: str, *, record_key: str) -> dict[str, object] | None:
        row = get_row_by_key(self, table_name, record_key=record_key)
        return row_to_dict(row, json_fields={"payload_json": {}}) if row is not None else None

    def program_m_create(self, table_name: str, **fields: object) -> dict[str, object]:
        payload = fields.pop("payload", None)
        return row_to_dict(
            create_record(self, table_name, payload=payload if isinstance(payload, dict) else None, **fields),
            json_fields={"payload_json": {}},
        )

    def program_m_update(self, table_name: str, record_id: int, **fields: object) -> dict[str, object]:
        payload = fields.pop("payload", None)
        if isinstance(payload, dict):
            fields["payload"] = payload
        return row_to_dict(update_record(self, table_name, record_id, **fields), json_fields={"payload_json": {}})

    def program_m_status(self, table_names: Iterable[str] | None = None) -> dict[str, object]:
        names = tuple(dict.fromkeys(str(name) for name in (table_names or self.program_m_table_names)))
        summary = build_program_m_summary(self, names, package_name=self.program_m_package_name)
        missing = [name for name in names if not self.program_m_tables_present([name])]
        return {
            "package": self.program_m_package_name,
            "status": "ok" if not missing else "degraded",
            "summary": summary,
            "missing_tables": missing,
        }

    def program_m_dashboard(self, table_names: Iterable[str] | None = None, *, limit: int = 5) -> dict[str, object]:
        names = tuple(dict.fromkeys(str(name) for name in (table_names or self.program_m_table_names)))
        return build_program_m_dashboard(self, names, package_name=self.program_m_package_name, limit=limit)

    def program_m_metric_counts(self, table_names: Iterable[str] | None = None) -> dict[str, int]:
        names = tuple(dict.fromkeys(str(name) for name in (table_names or self.program_m_table_names)))
        return {name: count_rows(self, name) for name in names}


@dataclass(slots=True)
class ProgramMEngineBase:
    repository: ProgramMRepositoryMixinBase
    package_name: str
    table_names: tuple[str, ...]

    def status(self) -> dict[str, object]:
        return self.repository.program_m_status(self.table_names)

    def dashboard(self, *, limit: int = 5) -> dict[str, object]:
        return self.repository.program_m_dashboard(self.table_names, limit=limit)

    def snapshot(self, *, limit: int = 5) -> dict[str, object]:
        return self.dashboard(limit=limit)

    def health(self) -> dict[str, object]:
        return self.status()

    def readiness(self) -> dict[str, object]:
        return self.status()

    def list(self, table_name: str, *, limit: int = 50) -> list[dict[str, object]]:
        return self.repository.program_m_collection(table_name, limit=limit)


class ProgramMServiceBase:
    package_name: str = "program-m"
    resource_tables: dict[str, str] = {}
    resource_singulars: dict[str, str] = {}

    def __init__(self, repository, policy=None, project_service=None) -> None:
        self.repository = repository
        self.policy = policy
        self.project_service = project_service

    def _table(self, resource: str) -> str:
        return self.resource_tables[resource]

    def _singular(self, resource: str) -> str:
        return self.resource_singulars.get(resource, resource.rstrip("s"))

    def _list(self, resource: str, *, limit: int = 50) -> list[dict[str, object]]:
        return self.repository.program_m_collection(self._table(resource), limit=limit)

    def _create(
        self,
        resource: str,
        *,
        body: dict[str, object],
        actor: dict[str, object] | None = None,
        status: str = "active",
    ) -> dict[str, object]:
        payload = dict(body)
        name = str(
            body.get("name")
            or body.get("title")
            or body.get("label")
            or body.get("profile_name")
            or body.get("version")
            or self._singular(resource)
        )
        kind = str(body.get("kind") or resource)
        scope = str(body.get("scope") or self.package_name)
        created = self.repository.program_m_create(
            self._table(resource),
            name=name,
            kind=kind,
            scope=scope,
            status=str(body.get("status") or status),
            payload=payload,
            record_key=str(body.get("record_key")) if body.get("record_key") else None,
            parent_id=int(body["parent_id"]) if isinstance(body.get("parent_id"), int) else None,
            reference_id=int(body["reference_id"]) if isinstance(body.get("reference_id"), int) else None,
            secondary_id=int(body["secondary_id"]) if isinstance(body.get("secondary_id"), int) else None,
        )
        if actor is not None and isinstance(actor, dict):
            created["actor_id"] = actor.get("id")
        return created

    def _update(
        self,
        resource: str,
        *,
        record_id: int,
        body: dict[str, object],
    ) -> dict[str, object]:
        updates = dict(body)
        if "payload" in updates and not isinstance(updates["payload"], dict):
            updates.pop("payload")
        return self.repository.program_m_update(self._table(resource), record_id, **updates)

    def _collection_payload(self, resource: str, *, key: str | None = None, limit: int = 50) -> dict[str, object]:
        payload_key = key or resource
        return {payload_key: self._list(resource, limit=limit)}

    def _created_payload(self, resource: str, row: dict[str, object]) -> dict[str, object]:
        return {self._singular(resource): row}

    def __getattr__(self, name: str):
        if name in self.resource_tables:
            def _collection(*, limit: int = 50, actor: dict[str, object] | None = None):
                return self._collection_payload(name, limit=limit)

            return _collection

        if name.startswith("create_"):
            resource_name = name.removeprefix("create_")
            if resource_name in self.resource_tables:
                def _create(*, body: dict[str, object] | None = None, actor: dict[str, object] | None = None, status: str = "active"):
                    return self._created_payload(
                        resource_name,
                        self._create(resource_name, body=body or {}, actor=actor, status=status),
                    )

                return _create
            plural_name = f"{resource_name}s"
            if plural_name in self.resource_tables:
                def _create(*, body: dict[str, object] | None = None, actor: dict[str, object] | None = None, status: str = "active"):
                    return self._created_payload(
                        plural_name,
                        self._create(plural_name, body=body or {}, actor=actor, status=status),
                    )

                return _create

        raise AttributeError(name)
