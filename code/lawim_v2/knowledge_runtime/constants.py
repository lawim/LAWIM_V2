"""Constants for the Knowledge Runtime package."""

from __future__ import annotations

from pathlib import Path

# ── Knowledge status values ──────────────────────────────────────────────

STATUS_DISABLED: str = "DISABLED"
STATUS_LOADING: str = "LOADING"
STATUS_READY: str = "READY"
STATUS_DEGRADED: str = "DEGRADED"
STATUS_FAILED: str = "FAILED"

KNOWLEDGE_STATUSES: frozenset[str] = frozenset({
    STATUS_DISABLED,
    STATUS_LOADING,
    STATUS_READY,
    STATUS_DEGRADED,
    STATUS_FAILED,
})

# ── Feature flag names ───────────────────────────────────────────────────

LAWIM_FEATURE_KNOWLEDGE_RUNTIME: str = "LAWIM_FEATURE_KNOWLEDGE_RUNTIME"
LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API: str = "LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API"

# ── Default source file paths (relative to project root) ─────────────────

DEFAULT_PROPERTY_TAXONOMY_PATH: Path = Path("docs/domain_extension/property_taxonomy_extensions.json")
DEFAULT_SERVICE_TAXONOMY_PATH: Path = Path("docs/domain_extension/service_taxonomy_extensions.json")
DEFAULT_ROLES_PATH: Path = Path("docs/domain_extension/identity_role_extensions.json")
DEFAULT_INTENTS_PATH: Path = Path("docs/domain_extension/intent_request_extensions.json")
DEFAULT_TRANSACTIONS_PATH: Path = Path("docs/domain_extension/intent_request_extensions.json")
DEFAULT_QUALIFICATION_MATRICES_PATH: Path = Path("docs/lawim_heritage_gold/qualification_matrices/qualification_matrices.json")
DEFAULT_FIELDS_PATH: Path = Path("docs/lawim_heritage_gold/qualification_matrices/field_dictionary.json")
DEFAULT_READINESS_PATH: Path = Path("docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json")
DEFAULT_QUESTION_RULES_PATH: Path = Path("docs/lawim_heritage_gold/qualification_matrices/question_rules.json")
DEFAULT_MATCHING_SEMANTICS_PATH: Path = Path("docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json")

# ── File size & depth limits ─────────────────────────────────────────────

MAX_JSON_FILE_SIZE_BYTES: int = 50 * 1024 * 1024  # 50 MiB
MAX_JSON_DEPTH: int = 32

# ── Validation severity levels ───────────────────────────────────────────

SEVERITY_ERROR: str = "ERROR"
SEVERITY_WARNING: str = "WARNING"

# ── Schema version ──────────────────────────────────────────────────────

KNOWLEDGE_SCHEMA_VERSION: str = "1.0.0"
