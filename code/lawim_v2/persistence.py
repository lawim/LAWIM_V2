from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ForeignKeySpec:
    column: str
    references: str
    on_delete: str = "restrict"

    def to_dict(self) -> dict[str, str]:
        return {
            "column": self.column,
            "references": self.references,
            "on_delete": self.on_delete,
        }


@dataclass(frozen=True, slots=True)
class TableSpec:
    name: str
    purpose: str
    primary_key: str
    columns: tuple[str, ...]
    unique: tuple[tuple[str, ...], ...] = ()
    foreign_keys: tuple[ForeignKeySpec, ...] = ()
    indexes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "purpose": self.purpose,
            "primary_key": self.primary_key,
            "columns": list(self.columns),
            "unique": [list(constraint) for constraint in self.unique],
            "foreign_keys": [foreign_key.to_dict() for foreign_key in self.foreign_keys],
            "indexes": list(self.indexes),
        }


@dataclass(frozen=True, slots=True)
class MigrationSpec:
    target_engine: str
    orm: str
    status: str
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "target_engine": self.target_engine,
            "orm": self.orm,
            "status": self.status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class SeedSpec:
    name: str
    mode: str
    entrypoints: tuple[str, ...]
    summary: dict[str, int]
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "mode": self.mode,
            "entrypoints": list(self.entrypoints),
            "summary": dict(self.summary),
            "notes": list(self.notes),
        }


@dataclass(frozen=True, slots=True)
class SchemaManifest:
    name: str
    version: int
    driver: str
    compatible_backends: tuple[str, ...]
    migration: MigrationSpec
    tables: tuple[TableSpec, ...]
    seed: SeedSpec

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "version": self.version,
            "driver": self.driver,
            "compatible_backends": list(self.compatible_backends),
            "migration": self.migration.to_dict(),
            "tables": [table.to_dict() for table in self.tables],
            "seed": self.seed.to_dict(),
        }


APPLICATION_SCHEMA_VERSION = 4

APPLICATION_MIGRATION = MigrationSpec(
    target_engine="postgresql",
    orm="prisma",
    status="active",
    notes=(
        "SQLite remains the default live runtime engine.",
        "Prisma schema and PostgreSQL repository path are executable when configured.",
        "The manifest fingerprint anchors SQLite ↔ PostgreSQL ↔ Prisma alignment.",
    ),
)

APPLICATION_SEED = SeedSpec(
    name="demo",
    mode="deterministic",
    entrypoints=(
        "LawimRepository.initialize(seed_demo_data=True)",
        "LawimRepository.seed_demo_data()",
    ),
    summary={
        "organizations": 3,
        "users": 3,
        "properties": 3,
        "media": 3,
        "conversations": 1,
        "messages": 3,
    },
    notes=(
        "Idempotent when organizations already exist.",
        "The password remains the repository demo password.",
    ),
)

APPLICATION_SCHEMA = SchemaManifest(
    name="lawim_v2_runtime_schema",
    version=APPLICATION_SCHEMA_VERSION,
    driver="sqlite",
    compatible_backends=("sqlite", "postgresql"),
    migration=APPLICATION_MIGRATION,
    seed=APPLICATION_SEED,
    tables=(
        TableSpec(
            name="organizations",
            purpose="Organizations that own properties and staff accounts.",
            primary_key="id",
            columns=("id", "name", "slug", "kind", "city", "created_at"),
            unique=(("slug",),),
        ),
        TableSpec(
            name="users",
            purpose="Authenticated users and staff accounts.",
            primary_key="id",
            columns=(
                "id",
                "email",
                "full_name",
                "role",
                "organization_id",
                "password_salt",
                "password_hash",
                "created_at",
            ),
            unique=(("email",),),
            foreign_keys=(ForeignKeySpec("organization_id", "organizations.id"),),
        ),
        TableSpec(
            name="sessions",
            purpose="Bearer session tokens for authenticated API access.",
            primary_key="token",
            columns=("token", "user_id", "created_at", "expires_at"),
            foreign_keys=(ForeignKeySpec("user_id", "users.id", on_delete="cascade"),),
            indexes=("idx_sessions_token",),
        ),
        TableSpec(
            name="properties",
            purpose="Property listings exposed through the runtime API.",
            primary_key="id",
            columns=(
                "id",
                "listing_code",
                "title",
                "summary",
                "address_line",
                "city",
                "region",
                "postal_code",
                "country",
                "search_key",
                "latitude",
                "longitude",
                "price_min",
                "price_max",
                "currency",
                "status",
                "availability",
                "property_type",
                "owner_organization_id",
                "bedrooms",
                "bathrooms",
                "area_sqm",
                "metadata_json",
                "version",
                "published_at",
                "deleted_at",
                "created_at",
            ),
            unique=(("listing_code",),),
            foreign_keys=(ForeignKeySpec("owner_organization_id", "organizations.id"),),
            indexes=("idx_properties_status_city", "idx_properties_search_key", "idx_properties_deleted_at"),
        ),
        TableSpec(
            name="media",
            purpose="Media linked to a property listing.",
            primary_key="id",
            columns=(
                "id",
                "property_id",
                "kind",
                "url",
                "caption",
                "storage_path",
                "mime_type",
                "size_bytes",
                "thumbnail_url",
                "metadata_json",
                "position",
                "version",
                "deleted_at",
                "created_at",
            ),
            foreign_keys=(ForeignKeySpec("property_id", "properties.id", on_delete="cascade"),),
            indexes=("idx_media_property_position",),
        ),
        TableSpec(
            name="conversations",
            purpose="Request and negotiation threads associated with a property.",
            primary_key="id",
            columns=("id", "property_id", "user_id", "subject", "status", "created_at"),
            foreign_keys=(
                ForeignKeySpec("property_id", "properties.id"),
                ForeignKeySpec("user_id", "users.id"),
            ),
        ),
        TableSpec(
            name="messages",
            purpose="Conversation messages and audit-visible replies.",
            primary_key="id",
            columns=("id", "conversation_id", "sender_user_id", "body", "created_at"),
            foreign_keys=(
                ForeignKeySpec("conversation_id", "conversations.id", on_delete="cascade"),
                ForeignKeySpec("sender_user_id", "users.id"),
            ),
            indexes=("idx_messages_conversation",),
        ),
        TableSpec(
            name="events",
            purpose="Audit trail for lifecycle and mutation events.",
            primary_key="id",
            columns=("id", "kind", "payload", "created_at"),
        ),
        TableSpec(
            name="schema_meta",
            purpose="Schema metadata and migration markers.",
            primary_key="key",
            columns=("key", "value"),
        ),
    ),
)


def build_application_schema_manifest() -> dict[str, object]:
    return APPLICATION_SCHEMA.to_dict()


def build_schema_fingerprint(manifest: dict[str, object] | None = None) -> str:
    payload = manifest if manifest is not None else build_application_schema_manifest()
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def build_migration_profile() -> dict[str, object]:
    return APPLICATION_MIGRATION.to_dict()


def build_seed_profile() -> dict[str, object]:
    return APPLICATION_SEED.to_dict()


def build_persistence_profile(db_path: Path, schema_version: int) -> dict[str, object]:
    manifest = build_application_schema_manifest()
    return {
        "driver": "sqlite",
        "adapter": "sqlite-repository",
        "path": str(db_path),
        "schema_version": schema_version,
        "schema_fingerprint": build_schema_fingerprint(manifest),
        "schema": manifest,
        "migration": build_migration_profile(),
        "seed": build_seed_profile(),
    }


def build_postgresql_profile(dsn: str, schema_version: int) -> dict[str, object]:
    manifest = build_application_schema_manifest()
    return {
        "driver": "postgresql",
        "adapter": "postgresql-repository",
        "dsn": dsn,
        "schema_version": schema_version,
        "schema_fingerprint": build_schema_fingerprint(manifest),
        "schema": manifest,
        "migration": build_migration_profile(),
        "seed": build_seed_profile(),
        "status": "active",
        "prisma_schema": "prisma/schema.prisma",
    }


def build_demo_seed_blueprint() -> dict[str, object]:
    return {
        "organizations": [
            {"name": "LAWIM Demo Agency", "slug": "lawim-demo-agency", "kind": "agency", "city": "Douala"},
            {"name": "LAWIM Partner Group", "slug": "lawim-partner-group", "kind": "partner", "city": "Yaounde"},
            {"name": "LAWIM Owner Desk", "slug": "lawim-owner-desk", "kind": "owner", "city": "Kribi"},
        ],
        "users": [
            {
                "email": "admin@lawim.local",
                "full_name": "LAWIM Admin",
                "role": "admin",
                "organization_slug": "lawim-demo-agency",
            },
            {
                "email": "agent@lawim.local",
                "full_name": "LAWIM Agent",
                "role": "agent",
                "organization_slug": "lawim-partner-group",
            },
            {
                "email": "owner@lawim.local",
                "full_name": "LAWIM Owner",
                "role": "owner",
                "organization_slug": "lawim-owner-desk",
            },
        ],
        "properties": [
            {
                "title": "Bonanjo City Loft",
                "summary": "Appartement urbain lumineux proche des services et du centre d'affaires.",
                "address_line": "12 Rue de la Joie, Bonanjo",
                "city": "Douala",
                "region": "Littoral",
                "postal_code": "BP-4020",
                "country": "Cameroon",
                "latitude": 4.05,
                "longitude": 9.7,
                "price_min": 250000,
                "price_max": 300000,
                "currency": "XAF",
                "status": "published",
                "availability": "available",
                "property_type": "apartment",
                "owner_organization_slug": "lawim-owner-desk",
                "bedrooms": 2,
                "bathrooms": 1,
                "area_sqm": 78,
                "metadata": {"featured": True, "source": "demo"},
            },
            {
                "title": "Kribi Beach Villa",
                "summary": "Villa familiale avec vue mer, terrasse et accès rapide aux plages.",
                "address_line": "Route de la Plage",
                "city": "Kribi",
                "region": "South",
                "country": "Cameroon",
                "latitude": 2.938,
                "longitude": 9.907,
                "price_min": 450000,
                "price_max": 520000,
                "currency": "XAF",
                "status": "published",
                "availability": "available",
                "property_type": "villa",
                "owner_organization_slug": "lawim-owner-desk",
                "bedrooms": 4,
                "bathrooms": 3,
                "area_sqm": 210,
            },
            {
                "title": "Bastos Studio",
                "summary": "Studio compact prêt à louer pour un usage urbain et flexible.",
                "address_line": "Avenue Kennedy",
                "city": "Yaounde",
                "region": "Centre",
                "country": "Cameroon",
                "latitude": 3.867,
                "longitude": 11.516,
                "price_min": 180000,
                "price_max": 220000,
                "currency": "XAF",
                "status": "published",
                "availability": "reserved",
                "property_type": "studio",
                "owner_organization_slug": "lawim-owner-desk",
                "bedrooms": 1,
                "bathrooms": 1,
                "area_sqm": 35,
            },
        ],
        "media": [
            {
                "property_title": "Bonanjo City Loft",
                "kind": "image",
                "url": "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'><rect width='600' height='400' fill='%231e293b'/><text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>Bonanjo City Loft</text></svg>",
                "caption": "Visuel de démonstration",
            },
            {
                "property_title": "Kribi Beach Villa",
                "kind": "image",
                "url": "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'><rect width='600' height='400' fill='%230f766e'/><text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>Kribi Beach Villa</text></svg>",
                "caption": "Visuel de démonstration",
            },
            {
                "property_title": "Bastos Studio",
                "kind": "image",
                "url": "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'><rect width='600' height='400' fill='%237c3aed'/><text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>Bastos Studio</text></svg>",
                "caption": "Visuel de démonstration",
            },
        ],
        "conversation": {
            "property_title": "Bonanjo City Loft",
            "user_email": "agent@lawim.local",
            "sender_email": "agent@lawim.local",
            "subject": "Demande de visite Bonanjo City Loft",
            "status": "open",
            "initial_message": "Bonjour, je souhaite organiser une visite pour le week-end.",
            "follow_up_messages": [
                {
                    "sender_email": "admin@lawim.local",
                    "body": "Bonjour, la visite est disponible samedi matin.",
                },
                {
                    "sender_email": "owner@lawim.local",
                    "body": "Je confirme la disponibilité du bien.",
                },
            ],
        },
    }
