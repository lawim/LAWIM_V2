from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

from .errors import ConflictError, NotFoundError, RepositoryError, ValidationError
from .persistence import (
    APPLICATION_SCHEMA_VERSION,
    build_application_schema_manifest,
    build_demo_seed_blueprint,
    build_migration_profile,
    build_persistence_profile,
    build_schema_fingerprint,
    build_seed_profile,
)
from .api_query import ListQuery, build_media_query, build_property_query, pagination_meta
from .geo_domain import build_geo_dto, location_matches_query
from .media_domain import build_thumbnail_url, normalize_kind, normalize_metadata as normalize_media_metadata, validate_media_url
from .property_domain import (
    build_property_input,
    can_publish,
    generate_listing_code,
    normalize_metadata as normalize_property_metadata,
    validate_status_transition,
)
from .matching import MatchCriteria, rank_properties
from .security import create_session_token, hash_password, verify_password


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL DEFAULT 'agency' CHECK (kind IN ('agency', 'partner', 'owner')),
    city TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('admin', 'agent', 'owner')),
    organization_id INTEGER,
    password_salt TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_code TEXT UNIQUE,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    address_line TEXT,
    city TEXT NOT NULL,
    region TEXT,
    postal_code TEXT,
    country TEXT NOT NULL,
    search_key TEXT,
    latitude REAL,
    longitude REAL,
    price_min INTEGER CHECK (price_min IS NULL OR price_min >= 0),
    price_max INTEGER CHECK (price_max IS NULL OR price_max >= 0),
    currency TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('draft', 'open', 'closed', 'published', 'archived')),
    availability TEXT NOT NULL DEFAULT 'available' CHECK (availability IN ('available', 'reserved', 'sold', 'rented', 'unavailable')),
    property_type TEXT NOT NULL,
    owner_organization_id INTEGER,
    bedrooms INTEGER NOT NULL DEFAULT 0 CHECK (bedrooms >= 0),
    bathrooms INTEGER NOT NULL DEFAULT 0 CHECK (bathrooms >= 0),
    area_sqm REAL NOT NULL DEFAULT 0 CHECK (area_sqm >= 0),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    published_at TEXT,
    deleted_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (owner_organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    kind TEXT NOT NULL CHECK (kind <> ''),
    url TEXT NOT NULL CHECK (url <> ''),
    caption TEXT NOT NULL CHECK (caption <> ''),
    storage_path TEXT,
    mime_type TEXT,
    size_bytes INTEGER CHECK (size_bytes IS NULL OR size_bytes >= 0),
    thumbnail_url TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    position INTEGER NOT NULL DEFAULT 0 CHECK (position >= 0),
    version INTEGER NOT NULL DEFAULT 1 CHECK (version >= 1),
    deleted_at TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'closed', 'archived')),
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id INTEGER NOT NULL,
    sender_user_id INTEGER NOT NULL,
    body TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    payload TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_properties_status_city ON properties(status, city);
CREATE INDEX IF NOT EXISTS idx_properties_search_key ON properties(search_key);
CREATE INDEX IF NOT EXISTS idx_properties_deleted_at ON properties(deleted_at);
CREATE INDEX IF NOT EXISTS idx_media_property_position ON media(property_id, position);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at);
"""


SCHEMA_VERSION = APPLICATION_SCHEMA_VERSION


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    stripped = value.strip()
    if not stripped:
        raise ValidationError(f"{field} is required")
    return stripped

@dataclass(frozen=True, slots=True)
class DemoSeed:
    admin_password: str = "lawim-demo"


__all__ = [
    "ConflictError",
    "DemoSeed",
    "LawimRepository",
    "NotFoundError",
    "RepositoryError",
    "ValidationError",
]


class LawimRepository:
    def __init__(self, db_path: Path, seed: DemoSeed | None = None) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30.0)
        self.lock = threading.RLock()
        self.seed = seed or DemoSeed()
        self._configure_connection()

    def _configure_connection(self) -> None:
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = NORMAL")
        self.connection.execute("PRAGMA busy_timeout = 5000")

    def close(self) -> None:
        with self.lock:
            self.connection.close()

    @contextmanager
    def _transaction(self):
        with self.lock:
            with self.connection:
                yield self.connection

    def initialize(self, seed_demo_data: bool = True) -> None:
        with self._transaction() as conn:
            conn.executescript(SCHEMA)
            self._apply_migrations(conn)
            metadata = {
                "schema_version": str(SCHEMA_VERSION),
                "schema_manifest": json.dumps(self.schema_manifest(), ensure_ascii=False, sort_keys=True),
                "schema_fingerprint": self.schema_fingerprint(),
                "migration_profile": json.dumps(self.migration_profile(), ensure_ascii=False, sort_keys=True),
                "seed_profile": json.dumps(self.seed_profile(), ensure_ascii=False, sort_keys=True),
            }
            for key, value in metadata.items():
                conn.execute("INSERT OR REPLACE INTO schema_meta (key, value) VALUES (?, ?)", (key, value))
        if seed_demo_data:
            self.seed_demo_data()

    def _table_columns(self, conn: sqlite3.Connection, table: str) -> set[str]:
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        return {str(row[1]) for row in rows}

    def _ensure_column(self, conn: sqlite3.Connection, table: str, column: str, definition: str) -> None:
        if column not in self._table_columns(conn, table):
            conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    def _apply_migrations(self, conn: sqlite3.Connection) -> None:
        property_columns = {
            "listing_code": "TEXT",
            "address_line": "TEXT",
            "region": "TEXT",
            "postal_code": "TEXT",
            "search_key": "TEXT",
            "availability": "TEXT NOT NULL DEFAULT 'available'",
            "metadata_json": "TEXT NOT NULL DEFAULT '{}'",
            "version": "INTEGER NOT NULL DEFAULT 1",
            "published_at": "TEXT",
            "deleted_at": "TEXT",
        }
        for column, definition in property_columns.items():
            self._ensure_column(conn, "properties", column, definition)

        media_columns = {
            "storage_path": "TEXT",
            "mime_type": "TEXT",
            "size_bytes": "INTEGER",
            "thumbnail_url": "TEXT",
            "metadata_json": "TEXT NOT NULL DEFAULT '{}'",
            "position": "INTEGER NOT NULL DEFAULT 0",
            "version": "INTEGER NOT NULL DEFAULT 1",
            "deleted_at": "TEXT",
        }
        for column, definition in media_columns.items():
            self._ensure_column(conn, "media", column, definition)

        conn.execute(
            """
            UPDATE properties
            SET availability = 'available'
            WHERE availability IS NULL OR TRIM(availability) = ''
            """
        )
        conn.execute(
            """
            UPDATE properties
            SET metadata_json = '{}'
            WHERE metadata_json IS NULL OR TRIM(metadata_json) = ''
            """
        )
        conn.execute(
            """
            UPDATE properties
            SET version = 1
            WHERE version IS NULL OR version < 1
            """
        )
        conn.execute(
            """
            UPDATE media
            SET metadata_json = '{}'
            WHERE metadata_json IS NULL OR TRIM(metadata_json) = ''
            """
        )
        conn.execute(
            """
            UPDATE media
            SET version = 1
            WHERE version IS NULL OR version < 1
            """
        )
        conn.execute(
            """
            UPDATE media
            SET position = 0
            WHERE position IS NULL OR position < 0
            """
        )
        conn.execute(
            """
            UPDATE properties
            SET search_key = LOWER(city || '|' || COALESCE(region, '') || '|' || country)
            WHERE search_key IS NULL OR TRIM(search_key) = ''
            """
        )
        conn.execute(
            """
            UPDATE properties
            SET published_at = created_at
            WHERE status = 'published' AND (published_at IS NULL OR TRIM(published_at) = '')
            """
        )
        conn.execute(
            """
            UPDATE properties
            SET listing_code = 'lawim-' || id
            WHERE listing_code IS NULL OR TRIM(listing_code) = ''
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_properties_search_key ON properties(search_key)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_properties_deleted_at ON properties(deleted_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_media_property_position ON media(property_id, position)")

    def schema_version(self) -> int:
        row = self.one("SELECT value FROM schema_meta WHERE key = 'schema_version'")
        if row is None:
            return 0
        try:
            return int(str(row["value"]))
        except (TypeError, ValueError):
            return 0

    def backend_profile(self) -> dict[str, object]:
        return build_persistence_profile(self.db_path, self.schema_version())

    def schema_manifest(self) -> dict[str, object]:
        return build_application_schema_manifest()

    def schema_fingerprint(self) -> str:
        return build_schema_fingerprint(self.schema_manifest())

    def migration_profile(self) -> dict[str, object]:
        return build_migration_profile()

    def seed_profile(self) -> dict[str, object]:
        return build_seed_profile()

    def seed_demo_data(self) -> dict[str, object]:
        if self.scalar("SELECT COUNT(*) FROM organizations") > 0:
            return {
                "profile": "demo",
                "seeded": False,
                "schema_version": self.schema_version(),
                "schema_fingerprint": self.schema_fingerprint(),
                "summary": self.summary(),
            }

        blueprint = build_demo_seed_blueprint()

        organization_ids: dict[str, int] = {}
        for organization in blueprint["organizations"]:
            seeded_organization = self.create_organization(**organization)
            organization_ids[str(seeded_organization["slug"])] = int(seeded_organization["id"])

        user_ids: dict[str, int] = {}
        for user in blueprint["users"]:
            seeded_user = self.create_user(
                email=str(user["email"]),
                full_name=str(user["full_name"]),
                role=str(user["role"]),
                password=self.seed.admin_password,
                organization_id=organization_ids[str(user["organization_slug"])],
            )
            user_ids[str(seeded_user["email"])] = int(seeded_user["id"])

        property_ids: dict[str, int] = {}
        for property_row in blueprint["properties"]:
            owner_organization_id = organization_ids[str(property_row["owner_organization_slug"])]
            seeded_property = self.create_property(
                title=str(property_row["title"]),
                summary=str(property_row["summary"]),
                city=str(property_row["city"]),
                country=str(property_row["country"]),
                address_line=property_row.get("address_line"),
                region=property_row.get("region"),
                postal_code=property_row.get("postal_code"),
                latitude=property_row.get("latitude"),
                longitude=property_row.get("longitude"),
                price_min=property_row.get("price_min"),
                price_max=property_row.get("price_max"),
                currency=str(property_row.get("currency", "XAF")),
                status=str(property_row.get("status", "published")),
                availability=str(property_row.get("availability", "available")),
                property_type=str(property_row.get("property_type", "apartment")),
                owner_organization_id=owner_organization_id,
                bedrooms=int(property_row.get("bedrooms", 0)),
                bathrooms=int(property_row.get("bathrooms", 0)),
                area_sqm=float(property_row.get("area_sqm", 0)),
                metadata=property_row.get("metadata"),
            )
            property_ids[str(seeded_property["title"])] = int(seeded_property["id"])

        for media_row in blueprint["media"]:
            self.create_media(
                property_id=property_ids[str(media_row["property_title"])],
                kind=str(media_row["kind"]),
                url=str(media_row["url"]),
                caption=str(media_row["caption"]),
                thumbnail_url=build_thumbnail_url(str(media_row["url"]), str(media_row["property_title"])),
            )

        conversation_row = blueprint["conversation"]
        conversation = self.create_conversation(
            user_id=user_ids[str(conversation_row["user_email"])],
            property_id=property_ids[str(conversation_row["property_title"])],
            subject=str(conversation_row["subject"]),
            status=str(conversation_row["status"]),
            initial_message=str(conversation_row["initial_message"]),
            sender_user_id=user_ids[str(conversation_row["sender_email"])],
        )
        for message_row in conversation_row["follow_up_messages"]:
            self.add_message(
                conversation["id"],
                user_ids[str(message_row["sender_email"])],
                str(message_row["body"]),
            )

        report = {
            "profile": "demo",
            "seeded": True,
            "schema_version": self.schema_version(),
            "schema_fingerprint": self.schema_fingerprint(),
            "summary": self.summary(),
        }
        self.record_event("bootstrap_seeded", report)
        return report

    def scalar(self, sql: str, params: tuple[object, ...] = ()) -> int:
        row = self.one(sql, params)
        if row is None:
            return 0
        value = next(iter(row.values()))
        return int(value or 0)

    def one(self, sql: str, params: tuple[object, ...] = ()) -> dict[str, object] | None:
        with self.lock:
            cursor = self.connection.execute(sql, params)
            row = cursor.fetchone()
        return dict(row) if row is not None else None

    def all(self, sql: str, params: tuple[object, ...] = ()) -> list[dict[str, object]]:
        with self.lock:
            cursor = self.connection.execute(sql, params)
            rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def record_event(self, kind: str, payload: dict[str, object]) -> None:
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO events (kind, payload, created_at) VALUES (?, ?, ?)",
                (kind, json.dumps(payload, ensure_ascii=False), utcnow()),
            )

    def get_organization_by_id(self, organization_id: int) -> dict[str, object]:
        organization = self.one("SELECT * FROM organizations WHERE id = ?", (organization_id,))
        if organization is None:
            raise NotFoundError(f"unknown organization id: {organization_id}")
        return organization

    def get_organization_by_slug(self, slug: str) -> dict[str, object]:
        organization = self.one("SELECT * FROM organizations WHERE slug = ?", (slug,))
        if organization is None:
            raise NotFoundError(f"unknown organization slug: {slug}")
        return organization

    def get_user_by_id(self, user_id: int) -> dict[str, object]:
        user = self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE u.id = ?
            """,
            (user_id,),
        )
        if user is None:
            raise NotFoundError(f"unknown user id: {user_id}")
        return user

    def get_user_by_email(self, email: str) -> dict[str, object]:
        user = self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE LOWER(u.email) = LOWER(?)
            """,
            (email,),
        )
        if user is None:
            raise NotFoundError(f"unknown user email: {email}")
        return user

    def create_organization(self, *, name: str, slug: str, kind: str = "agency", city: str | None = None) -> dict[str, object]:
        name = _require_text(name, "organization name")
        slug = _require_text(slug, "organization slug").lower()
        kind = _require_text(kind, "organization kind").lower()
        if kind not in {"agency", "partner", "owner"}:
            raise ValidationError(f"unsupported organization kind: {kind}")
        with self._transaction() as conn:
            try:
                cursor = conn.execute(
                    "INSERT INTO organizations (name, slug, kind, city, created_at) VALUES (?, ?, ?, ?, ?)",
                    (name, slug, kind, city, utcnow()),
                )
            except sqlite3.IntegrityError as exc:
                raise ConflictError("organization already exists") from exc
        organization = self.one("SELECT * FROM organizations WHERE id = ?", (cursor.lastrowid,))
        assert organization is not None
        self.record_event("organization_created", organization)
        return organization

    def update_organization(
        self,
        organization_id: int,
        *,
        name: str | None = None,
        slug: str | None = None,
        kind: str | None = None,
        city: str | None = None,
    ) -> dict[str, object]:
        current = self.get_organization_by_id(organization_id)
        changes: dict[str, object] = {}
        if name is not None:
            changes["name"] = _require_text(name, "organization name")
        if slug is not None:
            changes["slug"] = _require_text(slug, "organization slug").lower()
        if kind is not None:
            normalized_kind = _require_text(kind, "organization kind").lower()
            if normalized_kind not in {"agency", "partner", "owner"}:
                raise ValidationError(f"unsupported organization kind: {normalized_kind}")
            changes["kind"] = normalized_kind
        if city is not None:
            changes["city"] = _require_text(city, "organization city")
        if not changes:
            return current
        assignments = ", ".join(f"{column} = ?" for column in changes)
        params = tuple(changes.values()) + (organization_id,)
        with self._transaction() as conn:
            try:
                conn.execute(f"UPDATE organizations SET {assignments} WHERE id = ?", params)
            except sqlite3.IntegrityError as exc:
                raise ConflictError("organization already exists") from exc
        updated = self.get_organization_by_id(organization_id)
        self.record_event("organization_updated", {"id": organization_id, "changes": changes})
        return updated

    def list_organizations(self, limit: int = 50) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        return self.all(
            """
            SELECT o.*, COUNT(u.id) AS user_count
            FROM organizations o
            LEFT JOIN users u ON u.organization_id = o.id
            GROUP BY o.id
            ORDER BY o.created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

    def create_user(
        self,
        *,
        email: str,
        full_name: str,
        role: str,
        password: str,
        organization_id: int | None = None,
    ) -> dict[str, object]:
        email = _require_text(email, "email").lower()
        full_name = _require_text(full_name, "full_name")
        password = _require_text(password, "password")
        role = _require_text(role, "role").lower()
        if role not in {"admin", "agent", "owner"}:
            raise ValidationError(f"unsupported user role: {role}")
        if organization_id is not None:
            self.get_organization_by_id(organization_id)
        password_record = hash_password(password)
        with self._transaction() as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO users
                        (email, full_name, role, organization_id, password_salt, password_hash, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        email,
                        full_name,
                        role,
                        organization_id,
                        password_record.salt,
                        password_record.hash,
                        utcnow(),
                    ),
                )
            except sqlite3.IntegrityError as exc:
                raise ConflictError("user already exists") from exc
        user = self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE u.id = ?
            """,
            (cursor.lastrowid,),
        )
        assert user is not None
        self.record_event("user_created", {"email": email, "role": role, "organization_id": organization_id})
        return user

    def update_user(
        self,
        user_id: int,
        *,
        email: str | None = None,
        full_name: str | None = None,
        role: str | None = None,
        password: str | None = None,
        organization_id: int | None = None,
    ) -> dict[str, object]:
        current = self.get_user_by_id(user_id)
        changes: dict[str, object] = {}
        if email is not None:
            changes["email"] = _require_text(email, "email").lower()
        if full_name is not None:
            changes["full_name"] = _require_text(full_name, "full_name")
        if role is not None:
            normalized_role = _require_text(role, "role").lower()
            if normalized_role not in {"admin", "agent", "owner"}:
                raise ValidationError(f"unsupported user role: {normalized_role}")
            changes["role"] = normalized_role
        if organization_id is not None:
            self.get_organization_by_id(organization_id)
            changes["organization_id"] = organization_id
        if password is not None:
            password_record = hash_password(_require_text(password, "password"))
            changes["password_salt"] = password_record.salt
            changes["password_hash"] = password_record.hash
        if not changes:
            return current
        assignments = ", ".join(f"{column} = ?" for column in changes)
        params = tuple(changes.values()) + (user_id,)
        with self._transaction() as conn:
            try:
                conn.execute(f"UPDATE users SET {assignments} WHERE id = ?", params)
            except sqlite3.IntegrityError as exc:
                raise ConflictError("user already exists") from exc
        updated = self.get_user_by_id(user_id)
        self.record_event(
            "user_updated",
            {
                "id": user_id,
                "changes": {key: value for key, value in changes.items() if key not in {"password_salt", "password_hash"}},
            },
        )
        return updated

    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if self.scalar("SELECT COUNT(*) FROM conversations WHERE user_id = ?", (user_id,)) > 0:
            raise ConflictError("user has conversations")
        if self.scalar("SELECT COUNT(*) FROM messages WHERE sender_user_id = ?", (user_id,)) > 0:
            raise ConflictError("user has messages")
        with self._transaction() as conn:
            conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.record_event("user_deleted", {"id": user_id, "email": user["email"]})

    def list_users(self, limit: int = 50) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        return self.all(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            ORDER BY u.created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

    def authenticate(self, *, email: str, password: str) -> dict[str, object] | None:
        user = self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE LOWER(u.email) = LOWER(?)
            """,
            (email,),
        )
        if user is None:
            return None
        if not verify_password(password, str(user["password_salt"]), str(user["password_hash"])):
            return None
        return user

    def create_session(self, *, user_id: int, ttl_seconds: int) -> dict[str, object]:
        self.get_user_by_id(user_id)
        token = create_session_token()
        now = datetime.now(timezone.utc)
        expires = now + timedelta(seconds=ttl_seconds)
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (token, user_id, now.replace(microsecond=0).isoformat(), expires.replace(microsecond=0).isoformat()),
            )
        return self.get_session(token) or {"token": token, "user_id": user_id, "expires_at": expires.isoformat()}

    def delete_session(self, token: str) -> None:
        with self._transaction() as conn:
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))

    def get_session(self, token: str) -> dict[str, object] | None:
        session = self.one("SELECT * FROM sessions WHERE token = ?", (token,))
        if session is None:
            return None
        expires_at = datetime.fromisoformat(str(session["expires_at"]))
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            self.delete_session(token)
            return None
        return session

    def get_user_by_session(self, token: str) -> dict[str, object] | None:
        session = self.get_session(token)
        if session is None:
            return None
        user = self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE u.id = ?
            """,
            (session["user_id"],),
        )
        return user

    def create_property(
        self,
        *,
        title: str,
        summary: str,
        city: str,
        country: str,
        latitude: float | None = None,
        longitude: float | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        currency: str = "XAF",
        status: str = "draft",
        availability: str = "available",
        property_type: str = "apartment",
        owner_organization_id: int | None = None,
        address_line: str | None = None,
        region: str | None = None,
        postal_code: str | None = None,
        metadata: dict[str, object] | str | None = None,
        bedrooms: int = 0,
        bathrooms: int = 0,
        area_sqm: float = 0,
        listing_code: str | None = None,
    ) -> dict[str, object]:
        payload = build_property_input(
            title=title,
            summary=summary,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude,
            price_min=price_min,
            price_max=price_max,
            currency=currency,
            status=status,
            availability=availability,
            property_type=property_type,
            address_line=address_line,
            region=region,
            postal_code=postal_code,
            metadata=metadata,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area_sqm=area_sqm,
        )
        if owner_organization_id is not None:
            self.get_organization_by_id(owner_organization_id)
        published_at = utcnow() if payload["status"] == "published" else None
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO properties
                    (listing_code, title, summary, address_line, city, region, postal_code, country, search_key,
                     latitude, longitude, price_min, price_max, currency, status, availability, property_type,
                     owner_organization_id, bedrooms, bathrooms, area_sqm, metadata_json, version, published_at, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)
                """,
                (
                    listing_code,
                    payload["title"],
                    payload["summary"],
                    payload["address_line"],
                    payload["city"],
                    payload["region"],
                    payload["postal_code"],
                    payload["country"],
                    payload["search_key"],
                    payload["latitude"],
                    payload["longitude"],
                    payload["price_min"],
                    payload["price_max"],
                    payload["currency"],
                    payload["status"],
                    payload["availability"],
                    payload["property_type"],
                    owner_organization_id,
                    payload["bedrooms"],
                    payload["bathrooms"],
                    payload["area_sqm"],
                    payload["metadata_json"],
                    published_at,
                    utcnow(),
                ),
            )
            property_id = int(cursor.lastrowid)
            resolved_listing_code = listing_code or generate_listing_code(str(payload["title"]), property_id=property_id)
            conn.execute(
                "UPDATE properties SET listing_code = ? WHERE id = ?",
                (resolved_listing_code, property_id),
            )
        property_row = self.get_property(property_id)
        self.record_event(
            "property_created",
            {"id": property_row["id"], "listing_code": property_row.get("listing_code"), "title": title, "city": payload["city"]},
        )
        return property_row

    def update_property(
        self,
        property_id: int,
        *,
        title: str | None = None,
        summary: str | None = None,
        city: str | None = None,
        country: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        currency: str | None = None,
        status: str | None = None,
        availability: str | None = None,
        property_type: str | None = None,
        owner_organization_id: int | None = None,
        address_line: str | None = None,
        region: str | None = None,
        postal_code: str | None = None,
        metadata: dict[str, object] | str | None = None,
        bedrooms: int | None = None,
        bathrooms: int | None = None,
        area_sqm: float | None = None,
        version: int | None = None,
    ) -> dict[str, object]:
        current = self.get_property(property_id)
        changes: dict[str, object] = {}
        if title is not None:
            changes["title"] = _require_text(title, "title")
        if summary is not None:
            changes["summary"] = _require_text(summary, "summary")
        if city is not None:
            changes["city"] = _require_text(city, "city")
        if country is not None:
            changes["country"] = _require_text(country, "country")
        if address_line is not None:
            changes["address_line"] = _require_text(address_line, "address_line")
        if region is not None:
            changes["region"] = _require_text(region, "region")
        if postal_code is not None:
            changes["postal_code"] = _require_text(postal_code, "postal_code")
        if latitude is not None or longitude is not None:
            next_lat = latitude if latitude is not None else current.get("latitude")
            next_lon = longitude if longitude is not None else current.get("longitude")
            build_geo_dto(
                city=str(changes.get("city", current["city"])),
                country=str(changes.get("country", current["country"])),
                latitude=next_lat,  # type: ignore[arg-type]
                longitude=next_lon,  # type: ignore[arg-type]
                region=str(changes.get("region", current.get("region"))) if changes.get("region", current.get("region")) else None,
                address_line=str(changes.get("address_line", current.get("address_line"))) if changes.get("address_line", current.get("address_line")) else None,
                postal_code=str(changes.get("postal_code", current.get("postal_code"))) if changes.get("postal_code", current.get("postal_code")) else None,
            )
            if latitude is not None:
                changes["latitude"] = latitude
            if longitude is not None:
                changes["longitude"] = longitude
        if price_min is not None:
            changes["price_min"] = price_min
        if price_max is not None:
            changes["price_max"] = price_max
        if currency is not None:
            changes["currency"] = _require_text(currency, "currency").upper()
        if availability is not None:
            from .property_domain import normalize_availability

            changes["availability"] = normalize_availability(availability)
        if status is not None:
            normalized_status = _require_text(status, "status").lower()
            validate_status_transition(str(current["status"]).lower(), normalized_status)
            changes["status"] = normalized_status
            if normalized_status == "published" and not current.get("published_at"):
                changes["published_at"] = utcnow()
        if property_type is not None:
            changes["property_type"] = _require_text(property_type, "property_type").lower()
        if owner_organization_id is not None:
            self.get_organization_by_id(owner_organization_id)
            changes["owner_organization_id"] = owner_organization_id
        if bedrooms is not None:
            changes["bedrooms"] = bedrooms
        if bathrooms is not None:
            changes["bathrooms"] = bathrooms
        if area_sqm is not None:
            changes["area_sqm"] = area_sqm
        if metadata is not None:
            changes["metadata_json"] = normalize_property_metadata(metadata)
        merged_price_min = changes.get("price_min", current["price_min"])
        merged_price_max = changes.get("price_max", current["price_max"])
        if merged_price_min is not None and merged_price_max is not None and int(merged_price_min) > int(merged_price_max):
            raise ValidationError("price_min cannot exceed price_max")
        if any(key in changes for key in ("city", "country", "region")):
            geo = build_geo_dto(
                city=str(changes.get("city", current["city"])),
                country=str(changes.get("country", current["country"])),
                latitude=changes.get("latitude", current.get("latitude")),  # type: ignore[arg-type]
                longitude=changes.get("longitude", current.get("longitude")),  # type: ignore[arg-type]
                region=str(changes.get("region", current.get("region"))) if changes.get("region", current.get("region")) else None,
                address_line=str(changes.get("address_line", current.get("address_line"))) if changes.get("address_line", current.get("address_line")) else None,
                postal_code=str(changes.get("postal_code", current.get("postal_code"))) if changes.get("postal_code", current.get("postal_code")) else None,
            )
            changes["city"] = geo["city"]
            changes["country"] = geo["country"]
            changes["region"] = geo["region"]
            changes["search_key"] = geo["search_key"]
        if not changes:
            return current
        expected_version = int(version) if version is not None else int(current.get("version") or 1)
        changes["version"] = expected_version + 1
        assignments = ", ".join(f"{column} = ?" for column in changes)
        params = tuple(changes.values()) + (property_id, expected_version)
        with self._transaction() as conn:
            cursor = conn.execute(
                f"UPDATE properties SET {assignments} WHERE id = ? AND version = ?",
                params,
            )
            if cursor.rowcount == 0:
                raise ConflictError("property version conflict")
        updated = self.get_property(property_id)
        self.record_event("property_updated", {"id": property_id, "changes": {key: value for key, value in changes.items() if key != "version"}})
        return updated

    def publish_property(self, property_id: int, *, version: int | None = None) -> dict[str, object]:
        current = self.get_property(property_id)
        if not can_publish(current):
            raise ValidationError("property cannot be published in its current state")
        return self.update_property(property_id, status="published", version=version or int(current.get("version") or 1))

    def delete_property(self, property_id: int, *, hard: bool = False) -> dict[str, object]:
        property_row = self.get_property(property_id, include_deleted=True)
        if property_row.get("deleted_at") and not hard:
            return {"deleted": True, "property_id": property_id, "soft": True}
        if self.scalar("SELECT COUNT(*) FROM conversations WHERE property_id = ?", (property_id,)) > 0:
            if hard:
                raise ConflictError("property has conversations")
            with self._transaction() as conn:
                conn.execute(
                    "UPDATE properties SET deleted_at = ?, status = 'archived', version = version + 1 WHERE id = ?",
                    (utcnow(), property_id),
                )
            self.record_event("property_soft_deleted", {"id": property_id, "title": property_row["title"]})
            return {"deleted": True, "property_id": property_id, "soft": True}
        with self._transaction() as conn:
            conn.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        self.record_event("property_deleted", {"id": property_id, "title": property_row["title"]})
        return {"deleted": True, "property_id": property_id, "soft": False}

    def get_property(self, property_id: int, *, include_deleted: bool = False) -> dict[str, object]:
        clauses = ["p.id = ?"]
        params: list[object] = [property_id]
        if not include_deleted:
            clauses.append("p.deleted_at IS NULL")
        property_row = self.one(
            f"""
            SELECT p.*, o.name AS owner_organization_name, o.slug AS owner_organization_slug,
                   (SELECT COUNT(*) FROM media m WHERE m.property_id = p.id AND m.deleted_at IS NULL) AS media_count,
                   (SELECT COUNT(*) FROM conversations c WHERE c.property_id = p.id) AS conversation_count
            FROM properties p
            LEFT JOIN organizations o ON o.id = p.owner_organization_id
            WHERE {' AND '.join(clauses)}
            """,
            tuple(params),
        )
        if property_row is None:
            raise NotFoundError(f"unknown property id: {property_id}")
        return property_row

    def list_properties(
        self,
        *,
        city: str | None = None,
        country: str | None = None,
        region: str | None = None,
        status: str | None = None,
        availability: str | None = None,
        property_type: str | None = None,
        owner_organization_id: int | None = None,
        include_deleted: bool = False,
        search: str | None = None,
        limit: int = 50,
        page: int = 1,
        sort: str = "created_at",
        order: str = "desc",
    ) -> dict[str, object]:
        query = build_property_query(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            city=city,
            country=country,
            region=region,
            status=status,
            availability=availability,
            property_type=property_type,
            owner_organization_id=owner_organization_id,
            include_deleted=include_deleted,
            search=search,
        )
        return self._list_properties(query)

    def _list_properties(self, query: ListQuery) -> dict[str, object]:
        clauses = ["1 = 1"]
        params: list[object] = []
        if not query.include_deleted:
            clauses.append("p.deleted_at IS NULL")
        if query.city:
            clauses.append("LOWER(p.city) = LOWER(?)")
            params.append(query.city)
        if query.country:
            clauses.append("LOWER(p.country) = LOWER(?)")
            params.append(query.country)
        if query.region:
            clauses.append("LOWER(p.region) = LOWER(?)")
            params.append(query.region)
        if query.status:
            clauses.append("LOWER(p.status) = LOWER(?)")
            params.append(query.status)
        if query.availability:
            clauses.append("LOWER(p.availability) = LOWER(?)")
            params.append(query.availability)
        if query.property_type:
            clauses.append("LOWER(p.property_type) = LOWER(?)")
            params.append(query.property_type)
        if query.owner_organization_id is not None:
            clauses.append("p.owner_organization_id = ?")
            params.append(query.owner_organization_id)
        if query.search:
            clauses.append(
                "(LOWER(p.title) LIKE ? OR LOWER(p.summary) LIKE ? OR LOWER(p.search_key) LIKE ? OR LOWER(p.listing_code) LIKE ?)"
            )
            needle = f"%{query.search.lower()}%"
            params.extend([needle, needle, needle, needle])
        where = " AND ".join(clauses)
        sort_column = {
            "created_at": "p.created_at",
            "title": "p.title",
            "price_min": "p.price_min",
            "city": "p.city",
            "status": "p.status",
        }[query.sort]
        order = "ASC" if query.order == "asc" else "DESC"
        total = self.scalar(f"SELECT COUNT(*) FROM properties p WHERE {where}", tuple(params))
        rows = self.all(
            f"""
            SELECT p.*, o.name AS owner_organization_name, o.slug AS owner_organization_slug,
                   (SELECT COUNT(*) FROM media m WHERE m.property_id = p.id AND m.deleted_at IS NULL) AS media_count,
                   (SELECT COUNT(*) FROM conversations c WHERE c.property_id = p.id) AS conversation_count
            FROM properties p
            LEFT JOIN organizations o ON o.id = p.owner_organization_id
            WHERE {where}
            ORDER BY {sort_column} {order}, p.id DESC
            LIMIT ? OFFSET ?
            """,
            tuple(params + [query.limit, query.offset]),
        )
        return {
            "items": rows,
            "pagination": pagination_meta(
                page=query.page,
                limit=query.limit,
                total=total,
                sort=query.sort,
                order=query.order,
            ).to_dict(),
        }

    def search_locations(self, *, query: str | None = None, limit: int = 20) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        rows = self.all(
            """
            SELECT city, region, country, search_key, COUNT(*) AS property_count
            FROM properties
            WHERE deleted_at IS NULL
            GROUP BY city, region, country, search_key
            ORDER BY property_count DESC, city ASC
            """
        )
        if query:
            rows = [row for row in rows if location_matches_query(row, query)]
        return rows[:limit]

    def normalize_location(
        self,
        *,
        city: str,
        country: str,
        region: str | None = None,
        address_line: str | None = None,
        postal_code: str | None = None,
    ) -> dict[str, object]:
        return build_geo_dto(
            city=city,
            country=country,
            region=region,
            address_line=address_line,
            postal_code=postal_code,
        )

    def list_media(
        self,
        property_id: int | None = None,
        *,
        kind: str | None = None,
        include_deleted: bool = False,
        limit: int = 50,
        page: int = 1,
        sort: str = "created_at",
        order: str = "desc",
    ) -> dict[str, object]:
        query = build_media_query(
            page=page,
            limit=limit,
            sort=sort,
            order=order,
            property_id=property_id,
            kind=kind,
            include_deleted=include_deleted,
        )
        return self._list_media(query)

    def _list_media(self, query: ListQuery) -> dict[str, object]:
        clauses = ["1 = 1"]
        params: list[object] = []
        if query.property_id is not None:
            self.get_property(query.property_id)
            clauses.append("m.property_id = ?")
            params.append(query.property_id)
        if query.kind:
            clauses.append("LOWER(m.kind) = LOWER(?)")
            params.append(query.kind)
        if not query.include_deleted:
            clauses.append("m.deleted_at IS NULL")
        where = " AND ".join(clauses)
        sort_column = {"created_at": "m.created_at", "position": "m.position", "kind": "m.kind"}[query.sort]
        order = "ASC" if query.order == "asc" else "DESC"
        total = self.scalar(
            f"""
            SELECT COUNT(*)
            FROM media m
            JOIN properties p ON p.id = m.property_id
            WHERE {where}
            """,
            tuple(params),
        )
        rows = self.all(
            f"""
            SELECT m.*, p.title AS property_title
            FROM media m
            JOIN properties p ON p.id = m.property_id
            WHERE {where}
            ORDER BY {sort_column} {order}, m.id DESC
            LIMIT ? OFFSET ?
            """,
            tuple(params + [query.limit, query.offset]),
        )
        return {
            "items": rows,
            "pagination": pagination_meta(
                page=query.page,
                limit=query.limit,
                total=total,
                sort=query.sort,
                order=query.order,
            ).to_dict(),
        }

    def create_media(
        self,
        *,
        property_id: int,
        kind: str,
        url: str,
        caption: str,
        storage_path: str | None = None,
        mime_type: str | None = None,
        size_bytes: int | None = None,
        thumbnail_url: str | None = None,
        metadata: dict[str, object] | str | None = None,
        position: int | None = None,
    ) -> dict[str, object]:
        kind = normalize_kind(kind)
        url = validate_media_url(url)
        caption = _require_text(caption, "caption")
        metadata_json = normalize_media_metadata(metadata)
        self.get_property(property_id)
        if position is None:
            position = self.scalar(
                "SELECT COALESCE(MAX(position), -1) + 1 FROM media WHERE property_id = ? AND deleted_at IS NULL",
                (property_id,),
            )
        if size_bytes is not None and size_bytes < 0:
            raise ValidationError("size_bytes must be non-negative")
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO media
                    (property_id, kind, url, caption, storage_path, mime_type, size_bytes, thumbnail_url,
                     metadata_json, position, version, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
                """,
                (
                    property_id,
                    kind,
                    url,
                    caption,
                    storage_path,
                    mime_type,
                    size_bytes,
                    thumbnail_url or build_thumbnail_url(url, caption),
                    metadata_json,
                    position,
                    utcnow(),
                ),
            )
        media_row = self.get_media(int(cursor.lastrowid))
        self.record_event("media_created", {"property_id": property_id, "kind": kind, "media_id": media_row["id"]})
        return media_row

    def get_media(self, media_id: int, *, include_deleted: bool = False) -> dict[str, object]:
        clauses = ["m.id = ?"]
        params: list[object] = [media_id]
        if not include_deleted:
            clauses.append("m.deleted_at IS NULL")
        media_row = self.one(
            f"""
            SELECT m.*, p.title AS property_title
            FROM media m
            JOIN properties p ON p.id = m.property_id
            WHERE {' AND '.join(clauses)}
            """,
            tuple(params),
        )
        if media_row is None:
            raise NotFoundError(f"unknown media id: {media_id}")
        return media_row

    def update_media(
        self,
        media_id: int,
        *,
        kind: str | None = None,
        url: str | None = None,
        caption: str | None = None,
        thumbnail_url: str | None = None,
        metadata: dict[str, object] | str | None = None,
        position: int | None = None,
        version: int | None = None,
    ) -> dict[str, object]:
        current = self.get_media(media_id)
        changes: dict[str, object] = {}
        if kind is not None:
            changes["kind"] = normalize_kind(kind)
        if url is not None:
            changes["url"] = validate_media_url(url)
        if caption is not None:
            changes["caption"] = _require_text(caption, "caption")
        if thumbnail_url is not None:
            changes["thumbnail_url"] = validate_media_url(thumbnail_url)
        if metadata is not None:
            changes["metadata_json"] = normalize_media_metadata(metadata)
        if position is not None:
            if position < 0:
                raise ValidationError("position must be non-negative")
            changes["position"] = position
        if not changes:
            return current
        expected_version = int(version) if version is not None else int(current.get("version") or 1)
        changes["version"] = expected_version + 1
        assignments = ", ".join(f"{column} = ?" for column in changes)
        params = tuple(changes.values()) + (media_id, expected_version)
        with self._transaction() as conn:
            cursor = conn.execute(
                f"UPDATE media SET {assignments} WHERE id = ? AND version = ?",
                params,
            )
            if cursor.rowcount == 0:
                raise ConflictError("media version conflict")
        updated = self.get_media(media_id)
        self.record_event("media_updated", {"id": media_id, "property_id": current["property_id"], "changes": {key: value for key, value in changes.items() if key != "version"}})
        return updated

    def delete_media(self, media_id: int, *, hard: bool = False) -> dict[str, object]:
        media_row = self.get_media(media_id, include_deleted=True)
        if media_row.get("deleted_at") and not hard:
            return {"deleted": True, "media_id": media_id, "soft": True}
        if hard:
            with self._transaction() as conn:
                conn.execute("DELETE FROM media WHERE id = ?", (media_id,))
            self.record_event("media_deleted", {"id": media_id, "property_id": media_row["property_id"]})
            return {"deleted": True, "media_id": media_id, "soft": False}
        with self._transaction() as conn:
            conn.execute(
                "UPDATE media SET deleted_at = ?, version = version + 1 WHERE id = ?",
                (utcnow(), media_id),
            )
        self.record_event("media_soft_deleted", {"id": media_id, "property_id": media_row["property_id"]})
        return {"deleted": True, "media_id": media_id, "soft": True}

    def create_conversation(
        self,
        *,
        user_id: int,
        subject: str,
        status: str = "open",
        property_id: int | None = None,
        initial_message: str | None = None,
        sender_user_id: int | None = None,
    ) -> dict[str, object]:
        subject = _require_text(subject, "subject")
        if initial_message is not None:
            initial_message = _require_text(initial_message, "initial_message")
        self.get_user_by_id(user_id)
        if property_id is not None:
            self.get_property(property_id)
        if sender_user_id is not None:
            self.get_user_by_id(sender_user_id)
        status = _require_text(status, "status").lower()
        if status not in {"open", "closed", "archived"}:
            raise ValidationError(f"unsupported conversation status: {status}")
        added_initial_message = False
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversations (property_id, user_id, subject, status, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (property_id, user_id, subject, status, utcnow()),
            )
            conversation_id = cursor.lastrowid
            if initial_message:
                conn.execute(
                    """
                    INSERT INTO messages (conversation_id, sender_user_id, body, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (conversation_id, sender_user_id or user_id, initial_message, utcnow()),
                )
                added_initial_message = True
        conversation = self.get_conversation(conversation_id)
        self.record_event("conversation_created", {"id": conversation["id"], "property_id": property_id})
        if added_initial_message:
            self.record_event("message_added", {"conversation_id": conversation["id"], "sender_user_id": sender_user_id or user_id})
        return conversation

    def update_conversation(
        self,
        conversation_id: int,
        *,
        subject: str | None = None,
        status: str | None = None,
    ) -> dict[str, object]:
        current = self.get_conversation(conversation_id)
        changes: dict[str, object] = {}
        if subject is not None:
            changes["subject"] = _require_text(subject, "subject")
        if status is not None:
            normalized_status = _require_text(status, "status").lower()
            if normalized_status not in {"open", "closed", "archived"}:
                raise ValidationError(f"unsupported conversation status: {normalized_status}")
            current_status = str(current["status"]).lower()
            allowed_transitions = {
                "open": {"open", "closed", "archived"},
                "closed": {"closed", "archived"},
                "archived": {"archived"},
            }
            if normalized_status not in allowed_transitions.get(current_status, {normalized_status}):
                raise ValidationError(f"invalid conversation status transition: {current_status} -> {normalized_status}")
            changes["status"] = normalized_status
        if not changes:
            return current
        assignments = ", ".join(f"{column} = ?" for column in changes)
        params = tuple(changes.values()) + (conversation_id,)
        with self._transaction() as conn:
            conn.execute(f"UPDATE conversations SET {assignments} WHERE id = ?", params)
        updated = self.get_conversation(conversation_id)
        self.record_event("conversation_updated", {"id": conversation_id, "changes": changes})
        return updated

    def delete_conversation(self, conversation_id: int) -> dict[str, object]:
        conversation = self.get_conversation(conversation_id)
        with self._transaction() as conn:
            conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        self.record_event("conversation_deleted", {"id": conversation_id, "property_id": conversation["property_id"]})
        return {"deleted": True, "conversation_id": conversation_id}

    def add_message(self, conversation_id: int, sender_user_id: int, body: str) -> dict[str, object]:
        body = _require_text(body, "body")
        self.get_conversation(conversation_id)
        self.get_user_by_id(sender_user_id)
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO messages (conversation_id, sender_user_id, body, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (conversation_id, sender_user_id, body, utcnow()),
            )
        message = self.one("SELECT * FROM messages WHERE id = ?", (cursor.lastrowid,))
        assert message is not None
        self.record_event("message_added", {"conversation_id": conversation_id, "sender_user_id": sender_user_id})
        return message

    def list_events(self, limit: int = 50) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        return self.all(
            """
            SELECT *
            FROM events
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            (limit,),
        )

    def get_conversation(self, conversation_id: int) -> dict[str, object]:
        conversation = self.one(
            """
            SELECT c.*, p.title AS property_title, u.full_name AS requester_name, u.email AS requester_email,
                   (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.id) AS message_count,
                   (SELECT body FROM messages m WHERE m.conversation_id = c.id ORDER BY m.created_at DESC LIMIT 1) AS last_message
            FROM conversations c
            LEFT JOIN properties p ON p.id = c.property_id
            JOIN users u ON u.id = c.user_id
            WHERE c.id = ?
            """,
            (conversation_id,),
        )
        if conversation is None:
            raise NotFoundError(f"unknown conversation id: {conversation_id}")
        return conversation

    def list_conversations(self, limit: int = 50) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        return self.all(
            """
            SELECT c.*, p.title AS property_title, u.full_name AS requester_name, u.email AS requester_email,
                   (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.id) AS message_count,
                   (SELECT body FROM messages m WHERE m.conversation_id = c.id ORDER BY m.created_at DESC LIMIT 1) AS last_message
            FROM conversations c
            LEFT JOIN properties p ON p.id = c.property_id
            JOIN users u ON u.id = c.user_id
            ORDER BY c.created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

    def list_messages(self, conversation_id: int) -> list[dict[str, object]]:
        self.get_conversation(conversation_id)
        return self.all(
            """
            SELECT m.*, u.full_name AS sender_name, u.email AS sender_email
            FROM messages m
            JOIN users u ON u.id = m.sender_user_id
            WHERE m.conversation_id = ?
            ORDER BY m.created_at ASC
            """,
            (conversation_id,),
        )

    def summary(self) -> dict[str, object]:
        return {
            "organizations": self.scalar("SELECT COUNT(*) FROM organizations"),
            "users": self.scalar("SELECT COUNT(*) FROM users"),
            "published_properties": self.scalar(
                "SELECT COUNT(*) FROM properties WHERE status = 'published' AND deleted_at IS NULL"
            ),
            "conversations": self.scalar("SELECT COUNT(*) FROM conversations"),
            "messages": self.scalar("SELECT COUNT(*) FROM messages"),
            "media": self.scalar("SELECT COUNT(*) FROM media"),
            "events": self.scalar("SELECT COUNT(*) FROM events"),
            "sessions": self.scalar("SELECT COUNT(*) FROM sessions"),
        }

    def bootstrap_payload(self, *, token: str | None = None) -> dict[str, object]:
        current_user = self.get_user_by_session(token) if token else None
        return {
            "summary": self.summary(),
            "current_user": self._public_user(current_user) if current_user else None,
            "organizations": self.list_organizations(limit=10),
            "users": self.list_users(limit=10),
            "properties": self.list_properties(limit=10)["items"],
            "media": self.list_media(limit=10)["items"],
            "conversations": self.list_conversations(limit=10),
            "matches": self.recommendations(MatchCriteria(limit=5)),
        }

    def recommendations(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        properties = self.list_properties(status="published", limit=100)["items"]
        return rank_properties(properties, criteria)

    def matched_properties(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        return self.recommendations(criteria)

    def _public_user(self, user: dict[str, object] | None) -> dict[str, object] | None:
        if user is None:
            return None
        return {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "role": user["role"],
            "organization_id": user["organization_id"],
            "organization_name": user.get("organization_name"),
            "organization_slug": user.get("organization_slug"),
        }

    def public_user(self, user: dict[str, object] | None) -> dict[str, object] | None:
        return self._public_user(user)
