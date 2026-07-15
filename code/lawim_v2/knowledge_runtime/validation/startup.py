from __future__ import annotations

import logging
from typing import Any

from ..constants import (
    KNOWLEDGE_SCHEMA_VERSION,
    LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API,
    LAWIM_FEATURE_KNOWLEDGE_RUNTIME,
)
from ..errors import KnowledgeNotLoadedError
from ..models.common import ValidationIssue, ValidationReport

logger = logging.getLogger(__name__)


class StartupValidator:
    def __init__(self) -> None:
        self._issues: list[ValidationIssue] = []

    def check_feature_flag(self, feature_enabled: bool, flag_name: str) -> None:
        if not feature_enabled:
            self._issues.append(ValidationIssue(
                severity="WARNING",
                code="feature_disabled",
                message=f"Feature flag {flag_name} is disabled",
                source="startup",
            ))

    def check_loaded(self, registry_name: str, count: int, expected_min: int = 1) -> None:
        if count < expected_min:
            self._issues.append(ValidationIssue(
                severity="ERROR",
                code="registry_empty",
                message=f"{registry_name} has {count} items (expected at least {expected_min})",
                source="startup",
            ))

    def check_version(self, version_str: str) -> None:
        if version_str != KNOWLEDGE_SCHEMA_VERSION:
            self._issues.append(ValidationIssue(
                severity="ERROR",
                code="version_mismatch",
                message=f"Schema version {version_str} != expected {KNOWLEDGE_SCHEMA_VERSION}",
                source="startup",
            ))

    def report(self) -> ValidationReport:
        errors = [i for i in self._issues if i.severity == "ERROR"]
        warnings = [i for i in self._issues if i.severity == "WARNING"]
        return ValidationReport(
            total_issues=len(self._issues),
            errors=errors,
            warnings=warnings,
            passed=len(errors) == 0,
        )
