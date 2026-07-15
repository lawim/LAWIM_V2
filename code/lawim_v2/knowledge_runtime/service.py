from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

from .config import KnowledgeConfig
from .constants import STATUS_DISABLED, STATUS_FAILED, STATUS_READY
from .errors import KnowledgeNotLoadedError
from .loaders import load_all_knowledge
from .models.common import ValidationReport
from .registry import (
    FieldRegistry,
    IntentRegistry,
    KnowledgeVersionRegistry,
    MatchingSemanticRegistry,
    MatrixRegistry,
    PropertyTaxonomyRegistry,
    QuestionRuleRegistry,
    ReadinessRegistry,
    RoleRegistry,
    ServiceTaxonomyRegistry,
    SourceTraceRegistry,
    TransactionRegistry,
)
from .validation import ReferenceValidator, SchemaValidator, StartupValidator

logger = logging.getLogger(__name__)


class KnowledgeService:
    def __init__(self, config: KnowledgeConfig, build_commit: str = "unknown") -> None:
        self._config = config
        self._build_commit = build_commit
        self._status = STATUS_DISABLED
        self._loaded_at: datetime | None = None
        self._sources: list[dict[str, Any]] = []

        self.property_registry = PropertyTaxonomyRegistry()
        self.service_registry = ServiceTaxonomyRegistry()
        self.role_registry = RoleRegistry()
        self.intent_registry = IntentRegistry()
        self.transaction_registry = TransactionRegistry()
        self.matrix_registry = MatrixRegistry()
        self.field_registry = FieldRegistry()
        self.readiness_registry = ReadinessRegistry()
        self.question_rule_registry = QuestionRuleRegistry()
        self.matching_semantic_registry = MatchingSemanticRegistry()
        self.source_trace_registry = SourceTraceRegistry()
        self.version_registry = KnowledgeVersionRegistry()

        self.schema_validator = SchemaValidator()
        self.reference_validator = ReferenceValidator()
        self.startup_validator = StartupValidator()

    def load_all(self) -> ValidationReport:
        if not self._config.runtime_enabled:
            self._status = STATUS_DISABLED
            return ValidationReport(passed=True)

        try:
            sources = load_all_knowledge(
                property_taxonomy_path=str(self._config.project_root / self._config.property_taxonomy_path),
                service_taxonomy_path=str(self._config.project_root / self._config.service_taxonomy_path),
                roles_path=str(self._config.project_root / self._config.roles_path),
                intents_path=str(self._config.project_root / self._config.intents_path),
                transactions_path=str(self._config.project_root / self._config.transactions_path),
                matrices_path=str(self._config.project_root / self._config.matrices_path),
                fields_path=str(self._config.project_root / self._config.fields_path),
                readiness_path=str(self._config.project_root / self._config.readiness_path),
                question_rules_path=str(self._config.project_root / self._config.question_rules_path),
                matching_semantics_path=str(self._config.project_root / self._config.matching_semantics_path),
                property_registry=self.property_registry,
                service_registry=self.service_registry,
                role_registry=self.role_registry,
                intent_registry=self.intent_registry,
                transaction_registry=self.transaction_registry,
                matrix_registry=self.matrix_registry,
                field_registry=self.field_registry,
                readiness_registry=self.readiness_registry,
                question_rule_registry=self.question_rule_registry,
                matching_semantic_registry=self.matching_semantic_registry,
                source_trace_registry=self.source_trace_registry,
                version_registry=self.version_registry,
                build_commit=self._build_commit,
            )
            self._sources = [
                {
                    "path": s.path,
                    "section": s.section,
                    "domain": s.domain,
                    "version": s.version,
                    "checksum": s.checksum,
                    "record_count": s.record_count,
                    "status": s.status,
                }
                for s in sources
            ]
            self._status = STATUS_READY
            self._loaded_at = datetime.now(timezone.utc)

            validator = self.startup_validator
            validator.check_feature_flag(True, "knowledge_runtime")
            validator.check_loaded("property_registry", self.property_registry.count())
            validator.check_loaded("service_registry", self.service_registry.count())
            validator.check_loaded("role_registry", self.role_registry.count())
            validator.check_loaded("matrix_registry", self.matrix_registry.count())
            validator.check_loaded("field_registry", self.field_registry.count())
            return validator.report()

        except Exception:
            self._status = STATUS_FAILED
            logger.exception("Failed to load knowledge runtime")
            raise

    def health(self) -> dict[str, Any]:
        ver = self.version_registry.get()
        return {
            "status": self._status,
            "loaded_at": self._loaded_at.isoformat() if self._loaded_at else None,
            "version": ver.dict() if ver else None,
            "registries": {
                "properties": self.property_registry.count(),
                "services": self.service_registry.count(),
                "roles": self.role_registry.count(),
                "intents": self.intent_registry.count(),
                "transactions": self.transaction_registry.count(),
                "matrices": self.matrix_registry.count(),
                "fields": self.field_registry.count(),
                "readiness_levels": self.readiness_registry.count(),
                "question_rules": self.question_rule_registry.count(),
                "matching_semantics": self.matching_semantic_registry.count(),
                "source_traces": self.source_trace_registry.count(),
            },
            "sources": self._sources,
            "config": {
                "runtime_enabled": self._config.runtime_enabled,
                "internal_api_enabled": self._config.internal_api_enabled,
            },
        }

    def registry_summaries(self) -> dict[str, Any]:
        return {
            "property_taxonomy": self.property_registry.summary(),
            "service_taxonomy": self.service_registry.summary(),
            "role": self.role_registry.summary(),
            "intent": self.intent_registry.summary(),
            "transaction": self.transaction_registry.summary(),
            "matrix": self.matrix_registry.summary(),
            "field": self.field_registry.summary(),
            "readiness": self.readiness_registry.summary(),
            "question_rule": self.question_rule_registry.summary(),
            "matching_semantic": self.matching_semantic_registry.summary(),
            "source_trace": self.source_trace_registry.summary(),
            "version": self.version_registry.summary(),
        }
