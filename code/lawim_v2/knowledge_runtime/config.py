from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .constants import (
    DEFAULT_FIELDS_PATH,
    DEFAULT_INTENTS_PATH,
    DEFAULT_MATCHING_SEMANTICS_PATH,
    DEFAULT_PROPERTY_TAXONOMY_PATH,
    DEFAULT_QUALIFICATION_MATRICES_PATH,
    DEFAULT_QUESTION_RULES_PATH,
    DEFAULT_READINESS_PATH,
    DEFAULT_ROLES_PATH,
    DEFAULT_SERVICE_TAXONOMY_PATH,
    DEFAULT_TRANSACTIONS_PATH,
)


@dataclass(frozen=True, slots=True)
class KnowledgeConfig:
    property_taxonomy_path: Path = DEFAULT_PROPERTY_TAXONOMY_PATH
    service_taxonomy_path: Path = DEFAULT_SERVICE_TAXONOMY_PATH
    roles_path: Path = DEFAULT_ROLES_PATH
    intents_path: Path = DEFAULT_INTENTS_PATH
    transactions_path: Path = DEFAULT_TRANSACTIONS_PATH
    matrices_path: Path = DEFAULT_QUALIFICATION_MATRICES_PATH
    fields_path: Path = DEFAULT_FIELDS_PATH
    readiness_path: Path = DEFAULT_READINESS_PATH
    question_rules_path: Path = DEFAULT_QUESTION_RULES_PATH
    matching_semantics_path: Path = DEFAULT_MATCHING_SEMANTICS_PATH
    runtime_enabled: bool = False
    internal_api_enabled: bool = False
    project_root: Path = Path(".")
