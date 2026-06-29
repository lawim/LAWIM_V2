from __future__ import annotations

import json
import sqlite3
import threading
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from pathlib import Path

from .matching import MatchCriteria, rank_properties
from .security import create_session_token, hash_password, verify_password


SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    kind TEXT NOT NULL DEFAULT 'agency',
    city TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL,
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
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    price_min INTEGER,
    price_max INTEGER,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    property_type TEXT NOT NULL,
    owner_organization_id INTEGER,
    bedrooms INTEGER NOT NULL DEFAULT 0,
    bathrooms INTEGER NOT NULL DEFAULT 0,
    area_sqm REAL NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (owner_organization_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    kind TEXT NOT NULL,
    url TEXT NOT NULL,
    caption TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (property_id) REFERENCES properties(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER,
    user_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    status TEXT NOT NULL,
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

CREATE INDEX IF NOT EXISTS idx_properties_status_city ON properties(status, city);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token);
CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id, created_at);
"""


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str):
        raise ValidationError(f"{field} must be a string")
    stripped = value.strip()
    if not stripped:
        raise ValidationError(f"{field} is required")
    return stripped


class RepositoryError(ValueError):
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    code = "repository_error"


class NotFoundError(RepositoryError):
    status = HTTPStatus.NOT_FOUND
    code = "not_found"


class ConflictError(RepositoryError):
    status = HTTPStatus.CONFLICT
    code = "conflict"


class ValidationError(RepositoryError):
    status = HTTPStatus.BAD_REQUEST
    code = "invalid_state"


@dataclass(frozen=True, slots=True)
class DemoSeed:
    admin_password: str = "lawim-demo"


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
        if seed_demo_data:
            self._seed_demo_data()

    def _seed_demo_data(self) -> None:
        if self.scalar("SELECT COUNT(*) FROM organizations") > 0:
            return

        organizations = [
            {"name": "LAWIM Demo Agency", "slug": "lawim-demo-agency", "kind": "agency", "city": "Douala"},
            {"name": "LAWIM Partner Group", "slug": "lawim-partner-group", "kind": "partner", "city": "Yaounde"},
            {"name": "LAWIM Owner Desk", "slug": "lawim-owner-desk", "kind": "owner", "city": "Kribi"},
        ]
        for organization in organizations:
            self.create_organization(**organization)

        admin_org = self.get_organization_by_slug("lawim-demo-agency")
        partner_org = self.get_organization_by_slug("lawim-partner-group")
        owner_org = self.get_organization_by_slug("lawim-owner-desk")

        demo_users = [
            ("admin@lawim.local", "LAWIM Admin", "admin", admin_org["id"]),
            ("agent@lawim.local", "LAWIM Agent", "agent", partner_org["id"]),
            ("owner@lawim.local", "LAWIM Owner", "owner", owner_org["id"]),
        ]
        for email, full_name, role, organization_id in demo_users:
            self.create_user(
                email=email,
                full_name=full_name,
                role=role,
                password=self.seed.admin_password,
                organization_id=organization_id,
            )

        owner_id = self.get_user_by_email("owner@lawim.local")["id"]
        agent_id = self.get_user_by_email("agent@lawim.local")["id"]
        admin_id = self.get_user_by_email("admin@lawim.local")["id"]

        properties = [
            {
                "title": "Bonanjo City Loft",
                "summary": "Appartement urbain lumineux proche des services et du centre d'affaires.",
                "city": "Douala",
                "country": "Cameroon",
                "latitude": 4.050,
                "longitude": 9.700,
                "price_min": 250000,
                "price_max": 300000,
                "currency": "XAF",
                "status": "published",
                "property_type": "apartment",
                "owner_organization_id": owner_id,
                "bedrooms": 2,
                "bathrooms": 1,
                "area_sqm": 78,
            },
            {
                "title": "Kribi Beach Villa",
                "summary": "Villa familiale avec vue mer, terrasse et accès rapide aux plages.",
                "city": "Kribi",
                "country": "Cameroon",
                "latitude": 2.938,
                "longitude": 9.907,
                "price_min": 450000,
                "price_max": 520000,
                "currency": "XAF",
                "status": "published",
                "property_type": "villa",
                "owner_organization_id": owner_id,
                "bedrooms": 4,
                "bathrooms": 3,
                "area_sqm": 210,
            },
            {
                "title": "Bastos Studio",
                "summary": "Studio compact prêt à louer pour un usage urbain et flexible.",
                "city": "Yaounde",
                "country": "Cameroon",
                "latitude": 3.867,
                "longitude": 11.516,
                "price_min": 180000,
                "price_max": 220000,
                "currency": "XAF",
                "status": "published",
                "property_type": "studio",
                "owner_organization_id": owner_id,
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqm": 35,
            },
        ]
        seeded_properties = [self.create_property(**property_row) for property_row in properties]

        media = [
            (
                seeded_properties[0]["id"],
                "image",
                "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'><rect width='600' height='400' fill='%231e293b'/><text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>Bonanjo City Loft</text></svg>",
                "Visuel de démonstration",
            ),
            (
                seeded_properties[1]["id"],
                "image",
                "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'><rect width='600' height='400' fill='%230f766e'/><text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>Kribi Beach Villa</text></svg>",
                "Visuel de démonstration",
            ),
            (
                seeded_properties[2]["id"],
                "image",
                "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'><rect width='600' height='400' fill='%237c3aed'/><text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>Bastos Studio</text></svg>",
                "Visuel de démonstration",
            ),
        ]
        for property_id, kind, url, caption in media:
            self.create_media(property_id=property_id, kind=kind, url=url, caption=caption)

        conversation = self.create_conversation(
            user_id=agent_id,
            property_id=seeded_properties[0]["id"],
            subject="Demande de visite Bonanjo City Loft",
            status="open",
            initial_message="Bonjour, je souhaite organiser une visite pour le week-end.",
            sender_user_id=agent_id,
        )
        self.add_message(conversation["id"], admin_id, "Bonjour, la visite est disponible samedi matin.")
        self.add_message(conversation["id"], owner_id, "Je confirme la disponibilité du bien.")

        self.record_event(
            "bootstrap_seeded",
            {
                "organizations": 3,
                "users": 3,
                "properties": 3,
                "conversations": 1,
            },
        )

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
        slug = _require_text(slug, "organization slug")
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
        email = _require_text(email, "email")
        full_name = _require_text(full_name, "full_name")
        password = _require_text(password, "password")
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
        status: str = "published",
        property_type: str = "apartment",
        owner_organization_id: int | None = None,
        bedrooms: int = 0,
        bathrooms: int = 0,
        area_sqm: float = 0,
    ) -> dict[str, object]:
        title = _require_text(title, "title")
        summary = _require_text(summary, "summary")
        city = _require_text(city, "city")
        country = _require_text(country, "country")
        currency = _require_text(currency, "currency")
        property_type = _require_text(property_type, "property_type")
        if status not in {"draft", "open", "closed", "published", "archived"}:
            raise ValidationError(f"unsupported property status: {status}")
        if owner_organization_id is not None:
            self.get_organization_by_id(owner_organization_id)
        if price_min is not None and price_min < 0:
            raise ValidationError("price_min must be non-negative")
        if price_max is not None and price_max < 0:
            raise ValidationError("price_max must be non-negative")
        if price_min is not None and price_max is not None and price_min > price_max:
            raise ValidationError("price_min cannot exceed price_max")
        if latitude is not None and not -90.0 <= latitude <= 90.0:
            raise ValidationError("latitude must be between -90 and 90")
        if longitude is not None and not -180.0 <= longitude <= 180.0:
            raise ValidationError("longitude must be between -180 and 180")
        if bedrooms < 0:
            raise ValidationError("bedrooms must be non-negative")
        if bathrooms < 0:
            raise ValidationError("bathrooms must be non-negative")
        if area_sqm < 0:
            raise ValidationError("area_sqm must be non-negative")
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO properties
                    (title, summary, city, country, latitude, longitude, price_min, price_max, currency,
                     status, property_type, owner_organization_id, bedrooms, bathrooms, area_sqm, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    title,
                    summary,
                    city,
                    country,
                    latitude,
                    longitude,
                    price_min,
                    price_max,
                    currency,
                    status,
                    property_type,
                    owner_organization_id,
                    bedrooms,
                    bathrooms,
                    area_sqm,
                    utcnow(),
                ),
            )
        property_row = self.get_property(cursor.lastrowid)
        self.record_event("property_created", {"id": property_row["id"], "title": title, "city": city})
        return property_row

    def get_property(self, property_id: int) -> dict[str, object]:
        property_row = self.one(
            """
            SELECT p.*, o.name AS owner_organization_name, o.slug AS owner_organization_slug,
                   (SELECT COUNT(*) FROM media m WHERE m.property_id = p.id) AS media_count,
                   (SELECT COUNT(*) FROM conversations c WHERE c.property_id = p.id) AS conversation_count
            FROM properties p
            LEFT JOIN organizations o ON o.id = p.owner_organization_id
            WHERE p.id = ?
            """,
            (property_id,),
        )
        if property_row is None:
            raise NotFoundError(f"unknown property id: {property_id}")
        return property_row

    def list_properties(self, *, city: str | None = None, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        clauses = ["1 = 1"]
        params: list[object] = []
        if city:
            clauses.append("LOWER(p.city) = LOWER(?)")
            params.append(city)
        if status:
            clauses.append("LOWER(p.status) = LOWER(?)")
            params.append(status)
        params.append(limit)
        return self.all(
            f"""
            SELECT p.*, o.name AS owner_organization_name, o.slug AS owner_organization_slug,
                   (SELECT COUNT(*) FROM media m WHERE m.property_id = p.id) AS media_count,
                   (SELECT COUNT(*) FROM conversations c WHERE c.property_id = p.id) AS conversation_count
            FROM properties p
            LEFT JOIN organizations o ON o.id = p.owner_organization_id
            WHERE {' AND '.join(clauses)}
            ORDER BY p.created_at DESC
            LIMIT ?
            """,
            tuple(params),
        )

    def list_media(self, property_id: int | None = None, limit: int = 50) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        clauses = ["1 = 1"]
        params: list[object] = []
        if property_id is not None:
            self.get_property(property_id)
            clauses.append("m.property_id = ?")
            params.append(property_id)
        params.append(limit)
        return self.all(
            f"""
            SELECT m.*, p.title AS property_title
            FROM media m
            JOIN properties p ON p.id = m.property_id
            WHERE {' AND '.join(clauses)}
            ORDER BY m.created_at DESC
            LIMIT ?
            """,
            tuple(params),
        )

    def create_media(self, *, property_id: int, kind: str, url: str, caption: str) -> dict[str, object]:
        kind = _require_text(kind, "kind")
        url = _require_text(url, "url")
        caption = _require_text(caption, "caption")
        self.get_property(property_id)
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO media (property_id, kind, url, caption, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (property_id, kind, url, caption, utcnow()),
            )
        media_row = self.one("SELECT * FROM media WHERE id = ?", (cursor.lastrowid,))
        assert media_row is not None
        self.record_event("media_created", {"property_id": property_id, "kind": kind})
        return media_row

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
            "published_properties": self.scalar("SELECT COUNT(*) FROM properties WHERE status = 'published'"),
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
            "properties": self.list_properties(limit=10),
            "media": self.list_media(limit=10),
            "conversations": self.list_conversations(limit=10),
            "matches": self.recommendations(MatchCriteria(limit=5)),
        }

    def recommendations(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        properties = self.list_properties(status="published", limit=100)
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
