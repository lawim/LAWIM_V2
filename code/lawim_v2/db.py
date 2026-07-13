from __future__ import annotations

import json
import re
import sqlite3
import threading
from contextlib import contextmanager
from dataclasses import dataclass, replace
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
    build_standard_demo_accounts,
)
from .api_query import ListQuery, build_media_query, build_notification_query, build_property_query, pagination_meta
from .geo_domain import build_geo_dto
from .media_domain import build_thumbnail_url, normalize_kind, normalize_metadata as normalize_media_metadata, validate_media_url
from .property_domain import (
    build_property_input,
    can_publish,
    generate_listing_code,
    normalize_metadata as normalize_property_metadata,
    validate_status_transition,
)
from .conversation_domain import validate_stage_transition, validate_status_transition as validate_conversation_status
from .matching import MatchCriteria, rank_partners, rank_properties
from .notification_domain import build_notification_payload, normalize_kind as normalize_notification_kind
from .security import create_session_token, hash_password, verify_password
from .schema_ddl import SQLITE_INIT_SCRIPT
from .schema_migrations import apply_sqlite_legacy_migrations
from .user_roles import accept_user_role, resolve_official_user_role
from .project_repository import ProjectRepositoryMixin
from .intelligent.repository import IntelligentRepositoryMixin
from .knowledge_platform.repository import KnowledgePlatformRepositoryMixin
from .workflow_automation.repository import WorkflowAutomationRepositoryMixin
from .source_intelligence.repository import SourceIntelligenceRepositoryMixin
from .crm.repository import CrmRepositoryMixin
from .marketplace.repository import MarketplaceRepositoryMixin
from .analytics.repository import AnalyticsRepositoryMixin
from .communication.repository import CommunicationRepositoryMixin
from .security.repository import SecurityRepositoryMixin
from .real_estate_intelligence.repository import RealEstateIntelligenceRepositoryMixin
from .assistant.repository import AssistantRepositoryMixin
from .brain.repository import BrainRepositoryMixin
from .brain.relation_repository import BrainRelationRepositoryMixin
from .cognition.repository import CognitionRepositoryMixin
from .ecosystem.repository import EcosystemRepositoryMixin
from .program_m_support import ProgramMRepositoryMixinBase
from .backup.repository import BackupRepositoryMixin
from .financial.repository import FinancialRepositoryMixin
from .ai.repository import AIRepositoryMixin


SCHEMA = SQLITE_INIT_SCRIPT
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


def _normalize_email(value: str) -> str:
    return _require_text(value, "email").lower()


def _normalize_username(value: str) -> str:
    normalized = _require_text(value, "username").lower()
    if " " in normalized:
        raise ValidationError("username cannot contain spaces")
    return normalized


def _normalize_phone_e164(value: str) -> str:
    raw = _require_text(value, "phone_e164")
    digits = re.sub(r"\D", "", raw)
    if not digits:
        raise ValidationError("phone_e164 is required")
    return f"+{digits}"


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


class LawimRepository(AnalyticsRepositoryMixin, CommunicationRepositoryMixin, AIRepositoryMixin, SecurityRepositoryMixin, SourceIntelligenceRepositoryMixin, MarketplaceRepositoryMixin, FinancialRepositoryMixin, CrmRepositoryMixin, RealEstateIntelligenceRepositoryMixin, WorkflowAutomationRepositoryMixin, KnowledgePlatformRepositoryMixin, AssistantRepositoryMixin, CognitionRepositoryMixin, EcosystemRepositoryMixin, IntelligentRepositoryMixin, ProjectRepositoryMixin, ProgramMRepositoryMixinBase, BackupRepositoryMixin, BrainRepositoryMixin, BrainRelationRepositoryMixin):
    driver = "sqlite"

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

    def _table_columns(self, conn, table: str) -> set[str]:
        if str(getattr(self, "driver", "sqlite")).strip().lower() in {"postgresql", "postgres"}:
            rows = conn.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = ?
                """,
                (table,),
            ).fetchall()
            return {str(row["column_name"]) for row in rows}
        rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
        return {str(row["name"]) for row in rows}

    def initialize(self, seed_demo_data: bool = True) -> None:
        with self._transaction() as conn:
            conn.executescript(SQLITE_INIT_SCRIPT)
            apply_sqlite_legacy_migrations(conn)
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
        if hasattr(self, "seed_ecosystem_catalog"):
            self.seed_ecosystem_catalog()
            self.seed_demo_partners()
            project = self.one("SELECT id FROM projects ORDER BY id ASC LIMIT 1")
            if project and hasattr(self, "bootstrap_project_ecosystem"):
                self.bootstrap_project_ecosystem(int(project["id"]))
            if project and hasattr(self, "bootstrap_project_cognition"):
                self.bootstrap_project_cognition(int(project["id"]))
            if project and hasattr(self, "seed_assistant_catalog"):
                self.seed_assistant_catalog()
            if project and hasattr(self, "bootstrap_project_assistant"):
                self.bootstrap_project_assistant(int(project["id"]))
        if hasattr(self, "seed_expert_knowledge_catalog"):
            self.seed_expert_knowledge_catalog()
        if hasattr(self, "seed_automation_catalog"):
            self.seed_automation_catalog()
        if hasattr(self, "seed_rei_catalog"):
            self.seed_rei_catalog()
        if hasattr(self, "seed_crm_catalog"):
            self.seed_crm_catalog()
        if hasattr(self, "seed_marketplace_catalog"):
            self.seed_marketplace_catalog()
        if hasattr(self, "seed_security_catalog"):
            self.seed_security_catalog()
        if hasattr(self, "seed_financial_catalog"):
            self.seed_financial_catalog()
        if hasattr(self, "seed_communication_catalog"):
            self.seed_communication_catalog()
        if hasattr(self, "initialize_ai_catalog"):
            self.initialize_ai_catalog()
        if hasattr(self, "seed_ai_catalog"):
            self.seed_ai_catalog()
        if hasattr(self, "seed_analytics_catalog"):
            self.seed_analytics_catalog()
        if hasattr(self, "seed_backup_catalog"):
            self.seed_backup_catalog()

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
                username=user.get("username"),
                phone_e164=user.get("phone_e164"),
                preferred_language=str(user.get("preferred_language") or "fr"),
                role=str(user["role"]),
                password=str(user.get("password") or self.seed.admin_password),
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

        conversation_rows = blueprint.get("conversations") or ()
        if "conversation" in blueprint:
            conversation_rows = (*conversation_rows, blueprint["conversation"])
        for conversation_row in conversation_rows:
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

        project_rows = blueprint.get("projects") or ()
        if "project" in blueprint:
            project_rows = (*project_rows, blueprint["project"])
        for project_row in project_rows:
            user_id = user_ids[str(project_row["user_email"])]
            user = self.get_user_by_id(user_id)
            project = self.create_project(
                title=str(project_row["title"]),
                project_type=str(project_row["project_type"]),
                objective=str(project_row["objective"]),
                user_id=user_id,
                organization_id=user.get("organization_id"),
                budget_min=project_row.get("budget_min"),
                budget_max=project_row.get("budget_max"),
                currency=str(project_row.get("currency", "XAF")),
                location_city=project_row.get("location_city"),
                location_region=project_row.get("location_region"),
                location_country=str(project_row.get("location_country", "Cameroon")),
                timeline_horizon=project_row.get("timeline_horizon"),
                status=str(project_row.get("status", "draft")),
                priority=str(project_row.get("priority", "normal")),
            )
            if project_row.get("activate_first_step"):
                steps = self.list_project_steps(int(project["id"]))
                if steps:
                    self.update_project_step(
                        int(project["id"]),
                        int(steps[0]["id"]),
                        status="in_progress",
                        note="Demo seed activation",
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

    def execute(self, sql: str, params: tuple[object, ...] = ()) -> sqlite3.Cursor:
        with self.lock:
            cursor = self.connection.execute(sql, params)
            self.connection.commit()
        self.cursor = cursor
        return cursor

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
        normalized_email = _normalize_email(email)
        user = self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE u.email = ?
            """,
            (normalized_email,),
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
        username: str | None = None,
        phone_e164: str | None = None,
        preferred_language: str | None = None,
        role: str,
        password: str,
        organization_id: int | None = None,
    ) -> dict[str, object]:
        email = _require_text(email, "email").lower()
        full_name = _require_text(full_name, "full_name")
        normalized_username = _normalize_username(username) if username is not None else None
        normalized_phone = _normalize_phone_e164(phone_e164) if phone_e164 is not None else None
        normalized_language = _require_text(preferred_language, "preferred_language").lower() if preferred_language is not None else "fr"
        password = _require_text(password, "password")
        role = accept_user_role(role)
        if not role:
            raise ValidationError(f"unsupported user role: {role}")
        if organization_id is not None:
            self.get_organization_by_id(organization_id)
        password_record = hash_password(password)
        with self._transaction() as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO users
                        (email, username, full_name, phone_e164, preferred_language, role, organization_id, password_salt, password_hash, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        email,
                        normalized_username,
                        full_name,
                        normalized_phone,
                        normalized_language,
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

    def get_user_by_username(self, username: str) -> dict[str, object] | None:
        normalized_username = _normalize_username(username)
        return self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE lower(u.username) = ?
            """,
            (normalized_username,),
        )

    def get_user_by_phone(self, phone_e164: str) -> dict[str, object] | None:
        normalized_phone = _normalize_phone_e164(phone_e164)
        return self.one(
            """
            SELECT u.*, o.name AS organization_name, o.slug AS organization_slug
            FROM users u
            LEFT JOIN organizations o ON o.id = u.organization_id
            WHERE REPLACE(REPLACE(REPLACE(COALESCE(u.phone_e164, ''), ' ', ''), '-', ''), '+', '') = ?
            """,
            (normalized_phone.lstrip("+"),),
        )

    def get_user_by_identifier(self, identifier: str) -> dict[str, object] | None:
        normalized_identifier = _require_text(identifier, "identifier")
        if "@" in normalized_identifier:
            try:
                user = self.get_user_by_email(normalized_identifier)
            except NotFoundError:
                user = None
            if user is not None:
                return user
        user = self.get_user_by_username(normalized_identifier)
        if user is not None:
            return user
        digits = re.sub(r"\D", "", normalized_identifier)
        if digits:
            user = self.get_user_by_phone(normalized_identifier)
            if user is not None:
                return user
        return None

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
            normalized_role = accept_user_role(role)
            if not normalized_role:
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

    def sync_demo_credentials(
        self,
        password: str,
        *,
        emails: tuple[str, ...] = (
            "admin@lawim.app",
            "admin@lawim.local",
        ),
    ) -> list[str]:
        password = _require_text(password, "password")
        password_record = hash_password(password)
        normalized_emails = tuple(_normalize_email(email) for email in emails)
        updated: list[str] = []
        with self._transaction() as conn:
            for email in normalized_emails:
                if conn.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone() is None:
                    continue
                conn.execute(
                    "UPDATE users SET password_salt = ?, password_hash = ? WHERE email = ?",
                    (password_record.salt, password_record.hash, email),
                )
                updated.append(email)
        return updated

    def sync_standard_demo_accounts(self) -> list[str]:
        standard_organizations = (
            {"name": "LAWIM Demo Agency", "slug": "lawim-demo-agency", "kind": "agency", "city": "Douala"},
            {"name": "LAWIM Owner Desk", "slug": "lawim-owner-desk", "kind": "owner", "city": "Kribi"},
        )
        organization_ids: dict[str, int] = {}
        for organization in standard_organizations:
            slug = str(organization["slug"])
            try:
                current = self.get_organization_by_slug(slug)
            except NotFoundError:
                current = self.create_organization(
                    name=str(organization["name"]),
                    slug=slug,
                    kind=str(organization["kind"]),
                    city=str(organization.get("city")) if organization.get("city") is not None else None,
                )
            organization_ids[slug] = int(current["id"])

        synced: list[str] = []
        with self._transaction() as conn:
            for account in build_standard_demo_accounts():
                email = _normalize_email(str(account["email"]))
                full_name = _require_text(account["full_name"], "full_name")
                username = _normalize_username(str(account["username"]))
                phone_e164 = _normalize_phone_e164(str(account["phone_e164"]))
                role = accept_user_role(str(account["role"]))
                if not role:
                    raise ValidationError(f"unsupported user role: {account['role']}")
                preferred_language = _require_text(account.get("preferred_language") or "fr", "preferred_language").lower()
                if preferred_language not in {"fr", "en", "pcm"}:
                    raise ValidationError(f"unsupported preferred language: {preferred_language}")
                organization_slug = str(account["organization_slug"])
                organization_id = organization_ids[organization_slug]
                password_record = hash_password(_require_text(account["password"], "password"))
                existing = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
                if existing is None:
                    conn.execute(
                        """
                        INSERT INTO users
                            (email, username, full_name, phone_e164, preferred_language, role, organization_id, password_salt, password_hash, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            email,
                            username,
                            full_name,
                            phone_e164,
                            preferred_language,
                            role,
                            organization_id,
                            password_record.salt,
                            password_record.hash,
                            utcnow(),
                        ),
                    )
                else:
                    conn.execute(
                        """
                        UPDATE users
                        SET username = ?,
                            full_name = ?,
                            phone_e164 = ?,
                            preferred_language = ?,
                            role = ?,
                            organization_id = ?,
                            password_salt = ?,
                            password_hash = ?
                        WHERE email = ?
                        """,
                        (
                            username,
                            full_name,
                            phone_e164,
                            preferred_language,
                            role,
                            organization_id,
                            password_record.salt,
                            password_record.hash,
                            email,
                        ),
                    )
                synced.append(email)
        return synced

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

    def list_user_ids_by_organization(self, organization_id: int) -> list[int]:
        rows = self.all(
            """
            SELECT u.id
            FROM users u
            WHERE u.organization_id = ?
            ORDER BY u.id ASC
            """,
            (organization_id,),
        )
        return [int(row["id"]) for row in rows]

    def authenticate(
        self,
        *,
        identifier: str | None = None,
        email: str | None = None,
        password: str,
    ) -> dict[str, object] | None:
        lookup_identifier = identifier if identifier is not None else email
        if lookup_identifier is None:
            raise ValidationError("identifier is required")
        user = self.get_user_by_identifier(lookup_identifier)
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
        created_at = now.replace(microsecond=0).isoformat()
        expires_at = expires.replace(microsecond=0).isoformat()
        with self._transaction() as conn:
            conn.execute(
                "INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)",
                (token, user_id, created_at, expires_at),
            )
        return {"token": token, "user_id": user_id, "created_at": created_at, "expires_at": expires_at}

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
        metrics_cte = """
            WITH media_counts AS (
                SELECT property_id, COUNT(*) AS media_count
                FROM media
                WHERE deleted_at IS NULL
                GROUP BY property_id
            ),
            conversation_counts AS (
                SELECT property_id, COUNT(*) AS conversation_count
                FROM conversations
                GROUP BY property_id
            )
        """
        property_row = self.one(
            f"""{metrics_cte}
            SELECT p.*, o.name AS owner_organization_name, o.slug AS owner_organization_slug,
                   COALESCE(mc.media_count, 0) AS media_count,
                   COALESCE(cc.conversation_count, 0) AS conversation_count
            FROM properties p
            LEFT JOIN organizations o ON o.id = p.owner_organization_id
            LEFT JOIN media_counts mc ON mc.property_id = p.id
            LEFT JOIN conversation_counts cc ON cc.property_id = p.id
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
        price_min: int | None = None,
        price_max: int | None = None,
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
            price_min=price_min,
            price_max=price_max,
        )
        return self._list_properties(query)

    def _list_properties(self, query: ListQuery) -> dict[str, object]:
        clauses = ["1 = 1"]
        params: list[object] = []
        if not query.include_deleted:
            clauses.append("p.deleted_at IS NULL")
        if query.city:
            clauses.append("p.city = ?")
            params.append(query.city)
        if query.country:
            clauses.append("p.country = ?")
            params.append(query.country)
        if query.region:
            clauses.append("p.region = ?")
            params.append(query.region)
        if query.status:
            clauses.append("p.status = ?")
            params.append(query.status)
        if query.availability:
            clauses.append("p.availability = ?")
            params.append(query.availability)
        if query.property_type:
            clauses.append("p.property_type = ?")
            params.append(query.property_type)
        if query.owner_organization_id is not None:
            clauses.append("p.owner_organization_id = ?")
            params.append(query.owner_organization_id)
        if query.search:
            clauses.append(
                "(LOWER(p.title) LIKE ? OR LOWER(p.summary) LIKE ? OR p.search_key LIKE ? OR p.listing_code LIKE ?)"
            )
            needle = f"%{query.search.lower()}%"
            params.extend([needle, needle, needle, needle])
        if query.price_min is not None:
            clauses.append("(p.price_max IS NULL OR p.price_max >= ?)")
            params.append(query.price_min)
        if query.price_max is not None:
            clauses.append("(p.price_min IS NULL OR p.price_min <= ?)")
            params.append(query.price_max)
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
        metrics_cte = """
            WITH media_counts AS (
                SELECT property_id, COUNT(*) AS media_count
                FROM media
                WHERE deleted_at IS NULL
                GROUP BY property_id
            ),
            conversation_counts AS (
                SELECT property_id, COUNT(*) AS conversation_count
                FROM conversations
                GROUP BY property_id
            )
        """
        rows = self.all(
            f"""{metrics_cte}
            SELECT p.*, o.name AS owner_organization_name, o.slug AS owner_organization_slug,
                   COALESCE(mc.media_count, 0) AS media_count,
                   COALESCE(cc.conversation_count, 0) AS conversation_count
            FROM properties p
            LEFT JOIN organizations o ON o.id = p.owner_organization_id
            LEFT JOIN media_counts mc ON mc.property_id = p.id
            LEFT JOIN conversation_counts cc ON cc.property_id = p.id
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
        clauses = ["deleted_at IS NULL"]
        params: list[object] = []
        if query:
            escaped = query.casefold().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
            needle = f"%{escaped}%"
            clauses.append(
                "(LOWER(city) LIKE ? ESCAPE '\\' OR LOWER(COALESCE(region, '')) LIKE ? ESCAPE '\\' OR LOWER(country) LIKE ? ESCAPE '\\' OR search_key LIKE ? ESCAPE '\\')"
            )
            params.extend([needle, needle, needle, needle])
        where = " AND ".join(clauses)
        return self.all(
            f"""
            SELECT city, region, country, search_key, COUNT(*) AS property_count
            FROM properties
            WHERE {where}
            GROUP BY city, region, country, search_key
            ORDER BY property_count DESC, city ASC
            LIMIT ?
            """,
            tuple(params + [limit]),
        )

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
            clauses.append("m.kind = ?")
            params.append(query.kind)
        if not query.include_deleted:
            clauses.append("m.deleted_at IS NULL")
        where = " AND ".join(clauses)
        sort_column = {"created_at": "m.created_at", "position": "m.position", "kind": "m.kind"}[query.sort]
        order = "ASC" if query.order == "asc" else "DESC"
        total = self.scalar(f"SELECT COUNT(*) FROM media m WHERE {where}", tuple(params))
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

    def _infer_provider_resource_type(self, kind: str) -> str:
        normalized = (kind or "image").strip().lower()
        if normalized in {"image", "video", "document", "audio", "archive", "other"}:
            return normalized
        return "image"

    def create_media(
        self,
        *,
        property_id: int,
        kind: str,
        url: str,
        caption: str,
        storage_path: str | None = None,
        provider_name: str | None = None,
        provider_object_id: str | None = None,
        provider_media_id: str | None = None,
        provider_public_id: str | None = None,
        provider_resource_type: str | None = None,
        provider_storage_key: str | None = None,
        mime_type: str | None = None,
        size_bytes: int | None = None,
        thumbnail_url: str | None = None,
        metadata: dict[str, object] | str | None = None,
        position: int | None = None,
        lifecycle_state: str = "active",
        backup_state: str = "available",
    ) -> dict[str, object]:
        kind = normalize_kind(kind)
        url = validate_media_url(url)
        caption = _require_text(caption, "caption")
        metadata_json = normalize_media_metadata(metadata)
        effective_provider_name = provider_name or "local"
        effective_provider_object_id = provider_object_id
        effective_provider_public_id = provider_public_id or provider_object_id
        effective_provider_resource_type = provider_resource_type or self._infer_provider_resource_type(kind)
        effective_provider_storage_key = provider_storage_key or storage_path
        effective_lifecycle_state = lifecycle_state or "active"
        effective_backup_state = backup_state or "available"
        self.get_property(property_id)
        if position is None:
            position = self.scalar(
                "SELECT COALESCE(MAX(position), -1) + 1 FROM media WHERE property_id = ? AND deleted_at IS NULL",
                (property_id,),
            )
        if size_bytes is not None and size_bytes < 0:
            raise ValidationError("size_bytes must be non-negative")
        with self._transaction() as conn:
            media_columns = self._table_columns(conn, "media")
            insert_columns: list[str] = []
            insert_values: list[object] = []

            for column_name, value in (
                ("property_id", property_id),
                ("kind", kind),
                ("url", url),
                ("caption", caption),
                ("storage_path", storage_path),
                ("provider_name", effective_provider_name),
                ("provider_media_id", provider_media_id),
                ("provider_public_id", effective_provider_public_id),
                ("provider_resource_type", effective_provider_resource_type),
                ("provider_storage_key", effective_provider_storage_key),
                ("provider_object_id", effective_provider_object_id),
                ("mime_type", mime_type),
                ("size_bytes", size_bytes),
                ("thumbnail_url", thumbnail_url or build_thumbnail_url(url, caption)),
                ("metadata_json", metadata_json),
                ("position", position),
                ("lifecycle_state", effective_lifecycle_state),
                ("backup_state", effective_backup_state),
                ("version", 1),
                ("created_at", utcnow()),
            ):
                if column_name in media_columns:
                    insert_columns.append(column_name)
                    insert_values.append(value)

            insert_sql = (
                "INSERT INTO media "
                f"({', '.join(insert_columns)}) "
                f"VALUES ({', '.join('?' for _ in insert_columns)})"
            )
            cursor = conn.execute(insert_sql, tuple(insert_values))
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
        organization_id: int | None = None,
        negotiation_stage: str = "inquiry",
        initial_message: str | None = None,
        sender_user_id: int | None = None,
    ) -> dict[str, object]:
        subject = _require_text(subject, "subject")
        if initial_message is not None:
            initial_message = _require_text(initial_message, "initial_message")
        user = self.get_user_by_id(user_id)
        property_row = None
        if property_id is not None:
            property_row = self.get_property(property_id)
        if sender_user_id is not None:
            self.get_user_by_id(sender_user_id)
        status = _require_text(status, "status").lower()
        if status not in {"open", "closed", "archived"}:
            raise ValidationError(f"unsupported conversation status: {status}")
        stage = _require_text(negotiation_stage, "negotiation_stage").lower()
        try:
            validate_stage_transition(stage, stage)
        except ValueError as exc:
            raise ValidationError(str(exc)) from exc
        resolved_org = organization_id
        if resolved_org is None and property_row is not None:
            resolved_org = property_row.get("owner_organization_id")
        if resolved_org is None:
            resolved_org = user.get("organization_id")
        if resolved_org is not None:
            self.get_organization_by_id(int(resolved_org))
        now = utcnow()
        added_initial_message = False
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO conversations
                    (property_id, user_id, organization_id, subject, status, negotiation_stage, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (property_id, user_id, resolved_org, subject, status, stage, now, now),
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
        self.record_event("conversation_created", {"id": conversation["id"], "property_id": property_id, "organization_id": resolved_org})
        if added_initial_message:
            self.record_event("message_added", {"conversation_id": conversation["id"], "sender_user_id": sender_user_id or user_id})
        return conversation

    def update_conversation(
        self,
        conversation_id: int,
        *,
        subject: str | None = None,
        status: str | None = None,
        negotiation_stage: str | None = None,
    ) -> dict[str, object]:
        current = self.get_conversation(conversation_id)
        changes: dict[str, object] = {}
        if subject is not None:
            changes["subject"] = _require_text(subject, "subject")
        if status is not None:
            normalized_status = _require_text(status, "status").lower()
            try:
                validate_conversation_status(str(current["status"]).lower(), normalized_status)
            except ValueError as exc:
                raise ValidationError(str(exc)) from exc
            changes["status"] = normalized_status
        if negotiation_stage is not None:
            normalized_stage = _require_text(negotiation_stage, "negotiation_stage").lower()
            try:
                validate_stage_transition(str(current.get("negotiation_stage", "inquiry")).lower(), normalized_stage)
            except ValueError as exc:
                raise ValidationError(str(exc)) from exc
            changes["negotiation_stage"] = normalized_stage
        if not changes:
            return current
        changes["updated_at"] = utcnow()
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
            conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (utcnow(), conversation_id))
        message = self.one("SELECT * FROM messages WHERE id = ?", (cursor.lastrowid,))
        assert message is not None
        self.record_event("message_added", {"conversation_id": conversation_id, "sender_user_id": sender_user_id})
        return message

    def list_events(self, limit: int = 50, *, kind: str | None = None) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        clauses: list[str] = []
        params: list[object] = []
        if kind:
            clauses.append("kind = ?")
            params.append(kind.strip().lower())
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        params.append(limit)
        return self.all(
            f"""
            SELECT *
            FROM events
            {where}
            ORDER BY created_at DESC, id DESC
            LIMIT ?
            """,
            tuple(params),
        )

    def get_conversation(self, conversation_id: int) -> dict[str, object]:
        conversation = self.one(
            """
            SELECT c.*, p.title AS property_title, u.full_name AS requester_name, u.email AS requester_email,
                   o.name AS organization_name, o.slug AS organization_slug,
                   (SELECT COUNT(*) FROM messages m WHERE m.conversation_id = c.id) AS message_count,
                   (
                       SELECT m.body
                       FROM messages m
                       WHERE m.conversation_id = c.id
                       ORDER BY m.created_at DESC, m.id DESC
                       LIMIT 1
                   ) AS last_message
            FROM conversations c
            LEFT JOIN properties p ON p.id = c.property_id
            LEFT JOIN organizations o ON o.id = c.organization_id
            JOIN users u ON u.id = c.user_id
            WHERE c.id = ?
            """,
            (conversation_id,),
        )
        if conversation is None:
            raise NotFoundError(f"unknown conversation id: {conversation_id}")
        return conversation

    def list_conversations(
        self,
        *,
        user_id: int | None = None,
        organization_id: int | None = None,
        property_id: int | None = None,
        status: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, object]]:
        if limit < 1:
            raise ValidationError("limit must be positive")
        clauses = ["1 = 1"]
        params: list[object] = []
        if user_id is not None:
            clauses.append("c.user_id = ?")
            params.append(user_id)
        if organization_id is not None:
            clauses.append("c.organization_id = ?")
            params.append(organization_id)
        if property_id is not None:
            clauses.append("c.property_id = ?")
            params.append(property_id)
        if status:
            clauses.append("c.status = ?")
            params.append(status.lower())
        params.append(limit)
        metrics_cte = """
            WITH message_stats AS (
                SELECT conversation_id, COUNT(*) AS message_count
                FROM messages
                GROUP BY conversation_id
            ),
            last_messages AS (
                SELECT conversation_id, body AS last_message
                FROM (
                    SELECT conversation_id, body,
                           ROW_NUMBER() OVER (
                               PARTITION BY conversation_id
                               ORDER BY created_at DESC, id DESC
                           ) AS rn
                    FROM messages
                ) ranked_messages
                WHERE rn = 1
            )
        """
        return self.all(
            f"""{metrics_cte}
            SELECT c.*, p.title AS property_title, u.full_name AS requester_name, u.email AS requester_email,
                   o.name AS organization_name, o.slug AS organization_slug,
                   COALESCE(ms.message_count, 0) AS message_count,
                   lm.last_message AS last_message
            FROM conversations c
            LEFT JOIN properties p ON p.id = c.property_id
            LEFT JOIN organizations o ON o.id = c.organization_id
            JOIN users u ON u.id = c.user_id
            LEFT JOIN message_stats ms ON ms.conversation_id = c.id
            LEFT JOIN last_messages lm ON lm.conversation_id = c.id
            WHERE {' AND '.join(clauses)}
            ORDER BY c.updated_at DESC, c.id DESC
            LIMIT ?
            """,
            tuple(params),
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

    def create_notification(
        self,
        *,
        user_id: int,
        kind: str,
        title: str,
        body: str,
        payload: dict[str, object] | None = None,
    ) -> dict[str, object]:
        self.get_user_by_id(user_id)
        normalized_kind = normalize_notification_kind(kind)
        title = _require_text(title, "title")
        body = _require_text(body, "body")
        payload_json = build_notification_payload(payload)
        with self._transaction() as conn:
            cursor = conn.execute(
                """
                INSERT INTO notifications (user_id, kind, title, body, payload_json, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (user_id, normalized_kind, title, body, payload_json, utcnow()),
            )
        row = self.one("SELECT * FROM notifications WHERE id = ?", (cursor.lastrowid,))
        assert row is not None
        self.record_event("notification_created", {"id": row["id"], "user_id": user_id, "kind": normalized_kind})
        return row

    def list_notifications(
        self,
        *,
        user_id: int,
        unread_only: bool = False,
        kind: str | None = None,
        page: int = 1,
        limit: int = 50,
    ) -> dict[str, object]:
        query = build_notification_query(page=page, limit=limit, kind=kind, unread_only=unread_only)
        clauses = ["user_id = ?"]
        params: list[object] = [user_id]
        if query.unread_only:
            clauses.append("read_at IS NULL")
        if query.kind:
            clauses.append("kind = ?")
            params.append(query.kind)
        where = " AND ".join(clauses)
        total = self.scalar(f"SELECT COUNT(*) FROM notifications WHERE {where}", tuple(params))
        rows = self.all(
            f"""
            SELECT *
            FROM notifications
            WHERE {where}
            ORDER BY created_at DESC, id DESC
            LIMIT ? OFFSET ?
            """,
            tuple(params + [query.limit, query.offset]),
        )
        return {
            "items": rows,
            "pagination": pagination_meta(page=query.page, limit=query.limit, total=int(total), sort="created_at", order="desc").to_dict(),
        }

    def has_match_notification(self, *, user_id: int, property_id: int) -> bool:
        row = self.one(
            """
            SELECT id
            FROM notifications
            WHERE user_id = ? AND kind = 'match_found'
              AND json_extract(payload_json, '$.property_id') = ?
            LIMIT 1
            """,
            (user_id, property_id),
        )
        return row is not None

    def mark_notification_read(self, notification_id: int, *, user_id: int) -> dict[str, object]:
        row = self.one("SELECT * FROM notifications WHERE id = ? AND user_id = ?", (notification_id, user_id))
        if row is None:
            raise NotFoundError(f"unknown notification id: {notification_id}")
        if row.get("read_at"):
            return row
        read_at = utcnow()
        with self._transaction() as conn:
            conn.execute("UPDATE notifications SET read_at = ? WHERE id = ?", (read_at, notification_id))
        updated = self.one("SELECT * FROM notifications WHERE id = ?", (notification_id,))
        assert updated is not None
        self.record_event("notification_read", {"id": notification_id, "user_id": user_id})
        return updated

    def mark_all_notifications_read(self, *, user_id: int) -> dict[str, object]:
        self.get_user_by_id(user_id)
        read_at = utcnow()
        with self._transaction() as conn:
            cursor = conn.execute(
                "UPDATE notifications SET read_at = ? WHERE user_id = ? AND read_at IS NULL",
                (read_at, user_id),
            )
        return {"updated": cursor.rowcount, "read_at": read_at}

    def summary(self) -> dict[str, object]:
        row = self.one(
            """
            SELECT
                (SELECT COUNT(*) FROM organizations) AS organizations,
                (SELECT COUNT(*) FROM users) AS users,
                (SELECT COUNT(*) FROM properties WHERE status = 'published' AND deleted_at IS NULL) AS published_properties,
                (SELECT COUNT(*) FROM conversations) AS conversations,
                (SELECT COUNT(*) FROM messages) AS messages,
                (SELECT COUNT(*) FROM notifications) AS notifications,
                (SELECT COUNT(*) FROM media) AS media,
                (SELECT COUNT(*) FROM events) AS events,
                (SELECT COUNT(*) FROM sessions) AS sessions,
                (SELECT COUNT(*) FROM projects WHERE status != 'archived') AS projects,
                (SELECT COUNT(*) FROM crm_lead_sources) AS sources,
                (SELECT COUNT(*) FROM source_intelligence_source_contexts) AS source_contexts,
                (SELECT COUNT(*) FROM source_intelligence_imports) AS source_imports,
                (SELECT COUNT(*) FROM financial_invoices) AS financial_invoices,
                (SELECT COUNT(*) FROM financial_payment_intents) AS payment_intents,
                (SELECT COUNT(*) FROM financial_payment_transactions) AS payment_transactions,
                (SELECT COUNT(*) FROM financial_receipts) AS receipts,
                (SELECT COUNT(*) FROM financial_refunds) AS refunds,
                (SELECT COUNT(*) FROM financial_subscriptions) AS subscriptions,
                (SELECT COUNT(*) FROM financial_commissions) AS commissions,
                (SELECT COUNT(*) FROM financial_payouts) AS payouts,
                (SELECT COUNT(*) FROM financial_provider_events) AS provider_events
            """
        )
        assert row is not None
        return {
            "organizations": int(row["organizations"]),
            "users": int(row["users"]),
            "published_properties": int(row["published_properties"]),
            "conversations": int(row["conversations"]),
            "messages": int(row["messages"]),
            "notifications": int(row["notifications"]),
            "media": int(row["media"]),
            "events": int(row["events"]),
            "sessions": int(row["sessions"]),
            "projects": int(row["projects"]),
            "sources": int(row["sources"]),
            "source_contexts": int(row["source_contexts"]),
            "source_imports": int(row["source_imports"]),
            "financial_invoices": int(row["financial_invoices"]),
            "payment_intents": int(row["payment_intents"]),
            "payment_transactions": int(row["payment_transactions"]),
            "receipts": int(row["receipts"]),
            "refunds": int(row["refunds"]),
            "subscriptions": int(row["subscriptions"]),
            "commissions": int(row["commissions"]),
            "payouts": int(row["payouts"]),
            "provider_events": int(row["provider_events"]),
        }

    def bootstrap_payload(self, *, token: str | None = None) -> dict[str, object]:
        current_user = self.get_user_by_session(token) if token else None
        users: list[dict[str, object]] = []
        projects: list[dict[str, object]] = []
        if current_user is not None and resolve_official_user_role(current_user.get("role")) == "admin":
            users = [self._public_user(row) for row in self.list_users(limit=10)]
            projects = self.list_projects(limit=10)["items"]
        conversations: list[dict[str, object]]
        if current_user is not None and resolve_official_user_role(current_user.get("role")) != "admin":
            organization_id = current_user.get("organization_id")
            if organization_id is not None:
                conversations = self.list_conversations(organization_id=int(organization_id), limit=10)
                projects = self.list_projects(organization_id=int(organization_id), limit=10)["items"]
            else:
                conversations = self.list_conversations(user_id=int(current_user["id"]), limit=10)
                projects = self.list_projects(user_id=int(current_user["id"]), limit=10)["items"]
        else:
            conversations = self.list_conversations(limit=10) if current_user is not None else []
        from .contact import to_public_dict

        return {
            "summary": self.summary(),
            "official_contact": to_public_dict(),
            "current_user": self._public_user(current_user) if current_user else None,
            "organizations": self.list_organizations(limit=10),
            "users": users,
            "projects": projects,
            "properties": self.list_properties(limit=10)["items"],
            "media": self.list_media(limit=10)["items"],
            "conversations": conversations,
            "matches": self.recommendations(MatchCriteria(limit=5)),
        }

    def recommendations(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        status = criteria.status or "published"
        properties = self.list_properties(status=status, limit=100)["items"]
        return rank_properties(properties, criteria)

    def matched_properties(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        return self.recommendations(criteria)

    def matched_partners(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        status = criteria.status if criteria.status and criteria.status.lower() != "published" else "active"
        partner_criteria = replace(criteria, status=status)
        partners = self.list_partner_profiles(status=status, limit=100)["partners"]
        return rank_partners(partners, partner_criteria)

    def matched_entities(self, criteria: MatchCriteria) -> list[dict[str, object]]:
        target_type = str(criteria.target_type or "property").strip().lower()
        if target_type == "partner":
            return self.matched_partners(criteria)
        return self.matched_properties(criteria)

    def _public_user(self, user: dict[str, object] | None) -> dict[str, object] | None:
        from .dto import user_dto

        return user_dto(user)

    def public_user(self, user: dict[str, object] | None) -> dict[str, object] | None:
        return self._public_user(user)
