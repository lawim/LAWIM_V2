from __future__ import annotations

from .program_m_support import build_sqlite_tables_script, build_postgresql_statements, PROGRAM_M_SCHEMA_VERSION

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


APPLICATION_SCHEMA_VERSION = 19

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
        "users": 15,
        "properties": 50,
        "media": 50,
        "conversations": 5,
        "messages": 15,
        "notifications": 10,
        "projects": 5,
    },
    notes=(
        "Idempotent when organizations already exist.",
        "The password remains the repository demo password.",
        "Includes five role-aligned demo projects, fifty properties and fifteen role-aligned demo users.",
    ),
)


def _crm_table_specs() -> tuple[TableSpec, ...]:
    from .crm.schema_v14_ddl import V14_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x CRM entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("contact_id", "crm_contact_profiles.id", on_delete="cascade"),)
            if "contact_id" in name and name != "crm_contact_profiles"
            else (),
        )
        for name in V14_TABLE_NAMES
    )


def _source_intelligence_table_specs() -> tuple[TableSpec, ...]:
    from .source_intelligence.schema_ddl import SIE_TABLE_NAMES

    table_specs = {
        "source_intelligence_source_contexts": TableSpec(
            name="source_intelligence_source_contexts",
            purpose="LAWIM 2.x source intelligence context entity.",
            primary_key="id",
            columns=(
                "id",
                "source_id",
                "network",
                "publication_url",
                "publication_title",
                "publication_text",
                "publication_author",
                "campaign",
                "city",
                "district",
                "property_type",
                "target_audience",
                "format",
                "language",
                "tags_json",
                "ai_classification",
                "ai_confidence",
                "analysis_json",
                "notes",
                "whatsapp_link",
                "created_at",
                "updated_at",
            ),
            foreign_keys=(ForeignKeySpec("source_id", "crm_lead_sources.id", on_delete="cascade"),),
            indexes=("idx_source_intelligence_contexts_source",),
        ),
        "source_intelligence_imports": TableSpec(
            name="source_intelligence_imports",
            purpose="LAWIM 2.x source intelligence import entity.",
            primary_key="id",
            columns=(
                "id",
                "import_key",
                "source_id",
                "source_url",
                "import_status",
                "source_channel",
                "imported_at",
                "analyzed_at",
                "payload_json",
                "result_json",
                "created_at",
                "updated_at",
            ),
            foreign_keys=(ForeignKeySpec("source_id", "crm_lead_sources.id", on_delete="cascade"),),
            indexes=(
                "idx_source_intelligence_imports_source",
                "idx_source_intelligence_imports_status",
            ),
        ),
    }
    return tuple(table_specs[name] for name in SIE_TABLE_NAMES)


def _marketplace_table_specs() -> tuple[TableSpec, ...]:
    from .marketplace.schema_v15_ddl import V15_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x marketplace entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("partner_profile_id", "partner_profiles.id", on_delete="cascade"),)
            if "partner_profile_id" in name
            else (ForeignKeySpec("service_catalog_id", "service_catalog.id", on_delete="set null"),)
            if "service_catalog_id" in name
            else (),
        )
        for name in V15_TABLE_NAMES
    )


def _security_table_specs() -> tuple[TableSpec, ...]:
    from .security.schema_v16_ddl import V16_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x security IAM entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("user_id", "users.id", on_delete="cascade"),)
            if "user_id" in name and name != "iam_user_roles"
            else (ForeignKeySpec("role_id", "iam_roles.id", on_delete="cascade"),)
            if "role_id" in name
            else (),
        )
        for name in V16_TABLE_NAMES
    )





def _program_m_table_specs() -> tuple[TableSpec, ...]:
    from .program_m_support import COMMON_TABLE_COLUMNS

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x Program M entity ({name}).",
            primary_key="id",
            columns=COMMON_TABLE_COLUMNS,
            indexes=("idx_%s_name" % name,),
        )
        for name in ("operations", "deployment", "backup", "installer", "releases")
    )

def _analytics_table_specs() -> tuple[TableSpec, ...]:
    from .analytics.schema_v18_ddl import V18_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x analytics BI entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("user_id", "users.id", on_delete="set null"),)
            if "user_id" in name
            else (),
        )
        for name in V18_TABLE_NAMES
    )


def _communication_table_specs() -> tuple[TableSpec, ...]:
    from .communication.schema_v17_ddl import V17_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x communication entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("user_id", "users.id", on_delete="set null"),)
            if "user_id" in name
            else (ForeignKeySpec("contact_id", "crm_contact_profiles.id", on_delete="set null"),)
            if "contact_id" in name
            else (),
        )
        for name in V17_TABLE_NAMES
    )


def _real_estate_intelligence_table_specs() -> tuple[TableSpec, ...]:
    from .real_estate_intelligence.schema_v13_ddl import V13_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x real estate intelligence entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("property_id", "properties.id", on_delete="cascade"),)
            if "property_id" in name or name.startswith("rei_property")
            else (),
        )
        for name in V13_TABLE_NAMES
    )


def _workflow_automation_table_specs() -> tuple[TableSpec, ...]:
    from .workflow_automation.schema_v12_ddl import V12_TABLE_NAMES

    global_tables = {
        "automation_workflow_definitions",
        "automation_templates",
        "automation_queues",
        "automation_rules",
        "automation_rule_bindings",
        "automation_schedules",
        "automation_sla_policies",
        "automation_metrics_snapshots",
    }
    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x workflow automation entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(),
        )
        for name in V12_TABLE_NAMES
        if name in global_tables
    ) + tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x workflow automation entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="set null"),)
            if name == "automation_process_instances"
            else (),
        )
        for name in V12_TABLE_NAMES
        if name not in global_tables
    )


def _knowledge_platform_table_specs() -> tuple[TableSpec, ...]:
    from .knowledge_platform.schema_v11_ddl import V11_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x expert knowledge platform entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(),
        )
        for name in V11_TABLE_NAMES
    )


def _brain_table_specs() -> tuple[TableSpec, ...]:
    from .brain.schema_ddl import BRAIN_TABLE_NAMES
    from .brain.relation_ddl import RELATION_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x brain/memory entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),),
        )
        for name in BRAIN_TABLE_NAMES
    ) + tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x brain/relation entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),),
        )
        for name in RELATION_TABLE_NAMES
    )


def _assistant_table_specs() -> tuple[TableSpec, ...]:
    from .assistant.schema_v10_ddl import V10_TABLE_NAMES

    global_tables = {"assistant_agents", "assistant_prompt_versions"}
    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x assistant platform entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(),
        )
        for name in V10_TABLE_NAMES
        if name in global_tables
    ) + tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x assistant platform entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),),
        )
        for name in V10_TABLE_NAMES
        if name not in global_tables
    )


def _cognition_table_specs() -> tuple[TableSpec, ...]:
    from .cognition.schema_v9_ddl import V9_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x cognition platform entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),),
        )
        for name in V9_TABLE_NAMES
    )


def _ecosystem_table_specs() -> tuple[TableSpec, ...]:
    from .ecosystem.schema_v8_ddl import V8_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x ecosystem platform entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),)
            if name
            not in {
                "partner_profiles",
                "partner_zones",
                "partner_skills",
                "partner_certifications",
                "partner_availability",
                "partner_sla",
                "service_catalog",
                "service_catalog_partners",
                "workflows",
                "workflow_steps",
            }
            else (),
        )
        for name in V8_TABLE_NAMES
    )


def _intelligent_table_specs() -> tuple[TableSpec, ...]:
    from .intelligent.schema_v7_ddl import V7_TABLE_NAMES

    return tuple(
        TableSpec(
            name=name,
            purpose=f"LAWIM 2.x intelligent core entity ({name}).",
            primary_key="id",
            columns=("id", "created_at"),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),) if name not in {"user_contexts", "trust_scores"} else (),
        )
        for name in V7_TABLE_NAMES
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
            indexes=("idx_organizations_created_at",),
        ),
        TableSpec(
            name="users",
            purpose="Authenticated users and staff accounts.",
            primary_key="id",
            columns=(
                "id",
                "email",
                "username",
                "full_name",
                "phone_e164",
                "preferred_language",
                "role",
                "organization_id",
                "password_salt",
                "password_hash",
                "created_at",
            ),
            unique=(("email",), ("username",), ("phone_e164",)),
            foreign_keys=(ForeignKeySpec("organization_id", "organizations.id"),),
            indexes=("idx_users_organization", "idx_users_created_at", "idx_users_username", "idx_users_phone_e164"),
        ),
        TableSpec(
            name="sessions",
            purpose="Bearer session tokens for authenticated API access.",
            primary_key="token",
            columns=("token", "user_id", "created_at", "expires_at"),
            foreign_keys=(ForeignKeySpec("user_id", "users.id", on_delete="cascade"),),
            indexes=("idx_sessions_user_expires", "idx_sessions_expires_at"),
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
            indexes=(
                "idx_properties_status_city",
                "idx_properties_search_key",
                "idx_properties_deleted_at",
                "idx_properties_created_at",
                "idx_properties_owner_status",
            ),
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
            indexes=("idx_media_property_position", "idx_media_created_at"),
        ),
        TableSpec(
            name="conversations",
            purpose="Request and negotiation threads associated with a property.",
            primary_key="id",
            columns=(
                "id",
                "property_id",
                "user_id",
                "organization_id",
                "subject",
                "status",
                "negotiation_stage",
                "created_at",
                "updated_at",
            ),
            foreign_keys=(
                ForeignKeySpec("property_id", "properties.id"),
                ForeignKeySpec("user_id", "users.id"),
                ForeignKeySpec("organization_id", "organizations.id"),
            ),
            indexes=(
                "idx_conversations_user_updated",
                "idx_conversations_updated_at",
                "idx_conversations_organization_updated",
                "idx_conversations_property_updated",
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
            indexes=("idx_events_created_at", "idx_events_kind_created"),
        ),
        TableSpec(
            name="notifications",
            purpose="In-app notifications for conversations, matches, and system events.",
            primary_key="id",
            columns=("id", "user_id", "kind", "title", "body", "payload_json", "read_at", "created_at"),
            foreign_keys=(ForeignKeySpec("user_id", "users.id", on_delete="cascade"),),
            indexes=("idx_notifications_user_read",),
        ),
        TableSpec(
            name="schema_meta",
            purpose="Schema metadata and migration markers.",
            primary_key="key",
            columns=("key", "value"),
        ),
        TableSpec(
            name="projects",
            purpose="User real-estate projects — central 2.x domain entity.",
            primary_key="id",
            columns=(
                "id",
                "user_id",
                "organization_id",
                "title",
                "project_type",
                "objective",
                "budget_min",
                "budget_max",
                "currency",
                "location_city",
                "location_region",
                "location_country",
                "location_latitude",
                "location_longitude",
                "timeline_horizon",
                "status",
                "priority",
                "progress_percent",
                "metadata_json",
                "primary_goal_key",
                "intelligence_json",
                "archived_at",
                "created_at",
                "updated_at",
            ),
            foreign_keys=(
                ForeignKeySpec("user_id", "users.id", on_delete="cascade"),
                ForeignKeySpec("organization_id", "organizations.id"),
            ),
            indexes=(
                "idx_projects_user_status",
                "idx_projects_organization_status",
                "idx_projects_created_at",
            ),
        ),
        TableSpec(
            name="project_steps",
            purpose="Guided journey steps for a project.",
            primary_key="id",
            columns=(
                "id",
                "project_id",
                "step_key",
                "title",
                "description",
                "position",
                "status",
                "milestone",
                "next_action",
                "completed_at",
                "created_at",
                "updated_at",
            ),
            unique=(("project_id", "step_key"),),
            foreign_keys=(ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),),
            indexes=("idx_project_steps_project_position",),
        ),
        TableSpec(
            name="project_checklist_items",
            purpose="Checklist items linked to project journey steps.",
            primary_key="id",
            columns=(
                "id",
                "project_id",
                "step_id",
                "label",
                "checked",
                "position",
                "created_at",
                "updated_at",
            ),
            foreign_keys=(
                ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),
                ForeignKeySpec("step_id", "project_steps.id", on_delete="cascade"),
            ),
            indexes=("idx_project_checklist_project",),
        ),
        TableSpec(
            name="project_step_history",
            purpose="Audit history of project step status changes.",
            primary_key="id",
            columns=(
                "id",
                "project_id",
                "step_id",
                "from_status",
                "to_status",
                "note",
                "created_at",
            ),
            foreign_keys=(
                ForeignKeySpec("project_id", "projects.id", on_delete="cascade"),
                ForeignKeySpec("step_id", "project_steps.id", on_delete="cascade"),
            ),
            indexes=("idx_project_step_history_project",),
        ),
    )
    + _intelligent_table_specs()
    + _ecosystem_table_specs()
    + _cognition_table_specs()
    + _assistant_table_specs()
    + _brain_table_specs()
    + _knowledge_platform_table_specs()
    + _workflow_automation_table_specs()
    + _real_estate_intelligence_table_specs()
    + _crm_table_specs()
    + _source_intelligence_table_specs()
    + _marketplace_table_specs()
    + _security_table_specs()
    + _communication_table_specs()
    + _analytics_table_specs()
    + _program_m_table_specs(),
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


def build_standard_demo_accounts() -> tuple[dict[str, object], ...]:
    return (
        {
            "email": "admin@lawim.app",
            "full_name": "LAWIM Admin",
            "username": "admin",
            "phone_e164": "+237686822667",
            "role": "admin",
            "organization_slug": "lawim-demo-agency",
            "password": "LAWIM@Demo2026µ",
            "preferred_language": "fr",
        },
        {
            "email": "manager@lawim.app",
            "full_name": "LAWIM Manager",
            "username": "manager",
            "phone_e164": "+237686822668",
            "role": "manager",
            "organization_slug": "lawim-demo-agency",
            "password": "LAWIM@Demo2026µ",
            "preferred_language": "fr",
        },
        {
            "email": "agent@lawim.app",
            "full_name": "LAWIM Agent",
            "username": "agent",
            "phone_e164": "+237686822669",
            "role": "agent",
            "organization_slug": "lawim-demo-agency",
            "password": "LAWIM@Demo2026µ",
            "preferred_language": "fr",
        },
        {
            "email": "owner@lawim.app",
            "full_name": "LAWIM Owner",
            "username": "owner",
            "phone_e164": "+237686822670",
            "role": "owner",
            "organization_slug": "lawim-owner-desk",
            "password": "LAWIM@Demo2026µ",
            "preferred_language": "fr",
        },
        {
            "email": "investor@lawim.app",
            "full_name": "LAWIM Investor",
            "username": "investor",
            "phone_e164": "+237686822671",
            "role": "investor",
            "organization_slug": "lawim-owner-desk",
            "password": "LAWIM@Demo2026µ",
            "preferred_language": "fr",
        },
    )


def build_demo_seed_blueprint() -> dict[str, object]:
    def svg_data_url(title: str, fill: str) -> str:
        safe_title = (
            title.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("'", "&apos;")
            .replace('"', "&quot;")
        )
        return (
            "data:image/svg+xml;utf8,"
            "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 400'>"
            f"<rect width='600' height='400' fill='{fill}'/>"
            f"<text x='50' y='220' fill='white' font-size='38' font-family='sans-serif'>{safe_title}</text>"
            "</svg>"
        )

    organizations = [
        {"name": "LAWIM Demo Agency", "slug": "lawim-demo-agency", "kind": "agency", "city": "Douala"},
        {"name": "LAWIM Partner Group", "slug": "lawim-partner-group", "kind": "partner", "city": "Yaounde"},
        {"name": "LAWIM Owner Desk", "slug": "lawim-owner-desk", "kind": "owner", "city": "Kribi"},
    ]
    users = [
        {
            "email": "admin@lawim.local",
            "full_name": "LAWIM Admin",
            "username": "admin_local",
            "role": "admin",
            "organization_slug": "lawim-demo-agency",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "director@lawim.local",
            "full_name": "LAWIM Director",
            "username": "director",
            "role": "director",
            "organization_slug": "lawim-demo-agency",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "manager@lawim.local",
            "full_name": "LAWIM Manager",
            "username": "manager_local",
            "role": "manager",
            "organization_slug": "lawim-demo-agency",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "supervisor@lawim.local",
            "full_name": "LAWIM Supervisor",
            "username": "supervisor",
            "role": "supervisor",
            "organization_slug": "lawim-demo-agency",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "operator@lawim.local",
            "full_name": "LAWIM Operator",
            "username": "operator",
            "role": "operator",
            "organization_slug": "lawim-demo-agency",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "agent@lawim.local",
            "full_name": "LAWIM Agent",
            "username": "agent_local",
            "role": "agent",
            "organization_slug": "lawim-demo-agency",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "partner@lawim.local",
            "full_name": "LAWIM Partner",
            "username": "partner",
            "role": "partner",
            "organization_slug": "lawim-partner-group",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "notary@lawim.local",
            "full_name": "LAWIM Notary",
            "username": "notary",
            "role": "notary",
            "organization_slug": "lawim-partner-group",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "user@lawim.local",
            "full_name": "LAWIM User",
            "username": "user_local",
            "role": "user",
            "organization_slug": "lawim-owner-desk",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        {
            "email": "owner@lawim.local",
            "full_name": "LAWIM Owner",
            "username": "owner_local",
            "role": "owner",
            "organization_slug": "lawim-owner-desk",
            "password": "lawim-demo",
            "preferred_language": "fr",
        },
        *build_standard_demo_accounts(),
    ]

    base_properties = [
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
    ]

    city_catalog = (
        ("Douala", "Littoral", 4.05, 9.7),
        ("Yaounde", "Centre", 3.867, 11.516),
        ("Kribi", "South", 2.938, 9.907),
        ("Bafoussam", "West", 5.473, 10.417),
        ("Limbe", "South-West", 4.016, 9.206),
        ("Garoua", "North", 9.3, 13.4),
        ("Bertoua", "East", 4.58, 13.68),
        ("Edea", "Littoral", 3.8, 10.133),
        ("Ngaoundere", "Adamaoua", 7.316, 13.583),
        ("Dschang", "West", 5.448, 10.06),
    )
    property_templates = (
        {"property_type": "apartment", "label": "Appartement", "price_min": 240000, "price_max": 320000, "bedrooms": 2, "bathrooms": 1, "area_sqm": 76},
        {"property_type": "house", "label": "Maison", "price_min": 320000, "price_max": 420000, "bedrooms": 3, "bathrooms": 2, "area_sqm": 132},
        {"property_type": "villa", "label": "Villa", "price_min": 420000, "price_max": 620000, "bedrooms": 4, "bathrooms": 3, "area_sqm": 218},
        {"property_type": "studio", "label": "Studio", "price_min": 150000, "price_max": 210000, "bedrooms": 1, "bathrooms": 1, "area_sqm": 32},
        {"property_type": "terrain", "label": "Terrain", "price_min": 180000, "price_max": 280000, "bedrooms": 0, "bathrooms": 0, "area_sqm": 400},
        {"property_type": "immeuble", "label": "Immeuble", "price_min": 780000, "price_max": 1100000, "bedrooms": 8, "bathrooms": 6, "area_sqm": 540},
        {"property_type": "bureau", "label": "Bureau", "price_min": 260000, "price_max": 360000, "bedrooms": 0, "bathrooms": 2, "area_sqm": 94},
        {"property_type": "commerce", "label": "Commerce", "price_min": 280000, "price_max": 420000, "bedrooms": 0, "bathrooms": 1, "area_sqm": 110},
    )
    owner_cycle = ("lawim-owner-desk", "lawim-demo-agency", "lawim-partner-group")
    generated_properties: list[dict[str, object]] = []
    for index in range(47):
        city, region, latitude, longitude = city_catalog[index % len(city_catalog)]
        template = property_templates[index % len(property_templates)]
        ordinal = index + 4
        owner_slug = owner_cycle[index % len(owner_cycle)]
        availability = ("available", "reserved", "available", "available", "unavailable")[index % 5]
        title = f"{template['label']} {city} {ordinal:02d}"
        generated_properties.append(
            {
                "title": title,
                "summary": f"{template['label']} contemporain à {city}, pensé pour un usage {template['property_type']} premium.",
                "address_line": f"{ordinal} Avenue LAWIM {city}",
                "city": city,
                "region": region,
                "country": "Cameroon",
                "latitude": latitude,
                "longitude": longitude,
                "price_min": template["price_min"] + (index % 4) * 10000,
                "price_max": template["price_max"] + (index % 4) * 12000,
                "currency": "XAF",
                "status": "published",
                "availability": availability,
                "property_type": template["property_type"],
                "owner_organization_slug": owner_slug,
                "bedrooms": template["bedrooms"],
                "bathrooms": template["bathrooms"],
                "area_sqm": template["area_sqm"] + (index % 3) * 4,
                "metadata": {"featured": index % 9 == 0, "source": "demo", "rank": index + 4},
            }
        )

    properties = base_properties + generated_properties
    colors = ("#1e293b", "#0f766e", "#7c3aed", "#c2410c", "#0f172a", "#1d4ed8", "#134e4a", "#4338ca")
    media = [
        {
            "property_title": property_row["title"],
            "kind": "image",
            "url": svg_data_url(str(property_row["title"]), colors[index % len(colors)]),
            "caption": "Visuel de démonstration",
        }
        for index, property_row in enumerate(properties)
    ]

    conversations = [
        {
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
        {
            "property_title": "Kribi Beach Villa",
            "user_email": "owner@lawim.local",
            "sender_email": "owner@lawim.local",
            "subject": "Suivi de la villa de Kribi",
            "status": "open",
            "initial_message": "Je souhaite suivre les demandes reçues pour cette villa.",
            "follow_up_messages": [
                {
                    "sender_email": "partner@lawim.local",
                    "body": "Des photographies supplémentaires pourraient améliorer l'engagement.",
                },
                {
                    "sender_email": "admin@lawim.local",
                    "body": "Les notifications sont prêtes pour la prochaine visite.",
                },
            ],
        },
        {
            "property_title": "Bastos Studio",
            "user_email": "user@lawim.local",
            "sender_email": "user@lawim.local",
            "subject": "Location Bastos Studio",
            "status": "open",
            "initial_message": "Je cherche un logement compact dans ce secteur.",
            "follow_up_messages": [
                {
                    "sender_email": "operator@lawim.local",
                    "body": "Une visite peut être organisée cette semaine.",
                },
                {
                    "sender_email": "manager@lawim.local",
                    "body": "Le dossier est prioritaire.",
                },
            ],
        },
        {
            "property_title": "Appartement Douala 04",
            "user_email": "manager@lawim.local",
            "sender_email": "manager@lawim.local",
            "subject": "Projet Douala 04",
            "status": "open",
            "initial_message": "Merci de suivre la progression de ce projet.",
            "follow_up_messages": [
                {
                    "sender_email": "operator@lawim.local",
                    "body": "Le bien a été vérifié et peut être présenté.",
                },
                {
                    "sender_email": "partner@lawim.local",
                    "body": "Un complément documentaire serait utile.",
                },
            ],
        },
        {
            "property_title": "Maison Yaounde 05",
            "user_email": "partner@lawim.local",
            "sender_email": "partner@lawim.local",
            "subject": "Coordination Maison Yaounde 05",
            "status": "open",
            "initial_message": "Je centralise la mission liée à ce bien.",
            "follow_up_messages": [
                {
                    "sender_email": "admin@lawim.local",
                    "body": "La mission est suivie côté supervision.",
                },
                {
                    "sender_email": "owner@lawim.local",
                    "body": "Merci, je reste disponible pour la suite.",
                },
            ],
        },
    ]

    notifications = [
        {
            "user_email": "admin@lawim.local",
            "kind": "system",
            "title": "Supervision disponible",
            "body": "Les métriques de la plateforme sont prêtes.",
            "payload": {"severity": "info"},
        },
        {
            "user_email": "manager@lawim.local",
            "kind": "conversation_updated",
            "title": "Validation attendue",
            "body": "Un dossier nécessite votre validation.",
            "payload": {"priority": "high"},
        },
        {
            "user_email": "operator@lawim.local",
            "kind": "message_received",
            "title": "Message reçu",
            "body": "Une demande de support vient d'arriver.",
            "payload": {"channel": "dashboard"},
        },
        {
            "user_email": "partner@lawim.local",
            "kind": "match_found",
            "title": "Nouvelle mission",
            "body": "Une opportunité compatible a été identifiée.",
            "payload": {"category": "partner"},
        },
        {
            "user_email": "user@lawim.local",
            "kind": "conversation_created",
            "title": "Conversation ouverte",
            "body": "Votre demande a été transmise.",
            "payload": {"status": "open"},
        },
        {
            "user_email": "owner@lawim.local",
            "kind": "system",
            "title": "Publication confirmée",
            "body": "Le bien a été ajouté au catalogue.",
            "payload": {"status": "published"},
        },
        {
            "user_email": "agent@lawim.local",
            "kind": "message_received",
            "title": "Visite programmée",
            "body": "La visite du week-end est confirmée.",
            "payload": {"property": "Bonanjo City Loft"},
        },
        {
            "user_email": "director@lawim.local",
            "kind": "system",
            "title": "Release prête",
            "body": "La préparation de la release est terminée.",
            "payload": {"release": "LAWIM Experience 1.0"},
        },
        {
            "user_email": "supervisor@lawim.local",
            "kind": "conversation_updated",
            "title": "Point d'étape",
            "body": "Le suivi opérationnel attend votre revue.",
            "payload": {"status": "review"},
        },
        {
            "user_email": "notary@lawim.local",
            "kind": "match_found",
            "title": "Mission notaire",
            "body": "Une demande de mise en relation est disponible.",
            "payload": {"speciality": "notary"},
        },
    ]

    projects = [
        {
            "user_email": "admin@lawim.local",
            "title": "Supervision plateforme LAWIM",
            "project_type": "build",
            "objective": "Surveiller la refonte et les releases de LAWIM.",
            "budget_min": 900000,
            "budget_max": 1200000,
            "currency": "XAF",
            "location_city": "Douala",
            "location_region": "Littoral",
            "location_country": "Cameroon",
            "timeline_horizon": "1_year",
            "status": "active",
            "priority": "high",
            "activate_first_step": True,
        },
        {
            "user_email": "manager@lawim.local",
            "title": "Pilotage agence Yaoundé",
            "project_type": "sell",
            "objective": "Coordonner les validations et la performance commerciale.",
            "budget_min": 600000,
            "budget_max": 800000,
            "currency": "XAF",
            "location_city": "Yaounde",
            "location_region": "Centre",
            "location_country": "Cameroon",
            "timeline_horizon": "6_months",
            "status": "active",
            "priority": "high",
            "activate_first_step": True,
        },
        {
            "user_email": "operator@lawim.local",
            "title": "Qualité annonces Douala",
            "project_type": "other",
            "objective": "Contrôler les publications et les médias des biens.",
            "budget_min": 150000,
            "budget_max": 300000,
            "currency": "XAF",
            "location_city": "Douala",
            "location_region": "Littoral",
            "location_country": "Cameroon",
            "timeline_horizon": "3_months",
            "status": "active",
            "priority": "normal",
            "activate_first_step": True,
        },
        {
            "user_email": "partner@lawim.local",
            "title": "Mission partenaire Kribi",
            "project_type": "rent",
            "objective": "Gérer les rendez-vous et livrables de la mission.",
            "budget_min": 200000,
            "budget_max": 350000,
            "currency": "XAF",
            "location_city": "Kribi",
            "location_region": "South",
            "location_country": "Cameroon",
            "timeline_horizon": "flexible",
            "status": "active",
            "priority": "normal",
            "activate_first_step": True,
        },
        {
            "user_email": "user@lawim.local",
            "title": "Achat appartement Douala",
            "project_type": "buy",
            "objective": "Trouver un appartement 2 chambres à Bonanjo pour résidence principale",
            "budget_min": 200000,
            "budget_max": 320000,
            "currency": "XAF",
            "location_city": "Douala",
            "location_region": "Littoral",
            "location_country": "Cameroon",
            "timeline_horizon": "6_months",
            "status": "active",
            "priority": "normal",
            "activate_first_step": True,
        },
        {
            "user_email": "agent@lawim.local",
            "title": "Suivi commercial Douala",
            "project_type": "buy",
            "objective": "Suivre un dossier actif pour une recherche rapide de bien.",
            "budget_min": 180000,
            "budget_max": 280000,
            "currency": "XAF",
            "location_city": "Douala",
            "location_region": "Littoral",
            "location_country": "Cameroon",
            "timeline_horizon": "3_months",
            "status": "active",
            "priority": "high",
            "activate_first_step": True,
        },
    ]

    return {
        "organizations": organizations,
        "users": users,
        "properties": properties,
        "media": media,
        "conversations": conversations,
        "notifications": notifications,
        "projects": projects,
    }
