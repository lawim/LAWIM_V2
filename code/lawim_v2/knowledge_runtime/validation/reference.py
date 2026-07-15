from __future__ import annotations

import logging
from typing import Any

from ..errors import KnowledgeReferenceError

logger = logging.getLogger(__name__)


class ReferenceValidator:
    def __init__(self) -> None:
        self._errors: list[KnowledgeReferenceError] = []

    def check_field_references(self, field_id: str, known_fields: set[str], source_id: str) -> None:
        if field_id not in known_fields:
            self._errors.append(KnowledgeReferenceError(
                source_id=source_id,
                target_type="field",
                target_id=field_id,
                message=f"Unknown field '{field_id}' referenced by {source_id}",
            ))

    def check_matrix_references(self, matrix_id: str, known_matrices: set[str], source_id: str) -> None:
        if matrix_id not in known_matrices:
            self._errors.append(KnowledgeReferenceError(
                source_id=source_id,
                target_type="matrix",
                target_id=matrix_id,
                message=f"Unknown matrix '{matrix_id}' referenced by {source_id}",
            ))

    def check_property_references(self, property_id: str, known_properties: set[str], source_id: str) -> None:
        if property_id not in known_properties:
            self._errors.append(KnowledgeReferenceError(
                source_id=source_id,
                target_type="property_type",
                target_id=property_id,
                message=f"Unknown property type '{property_id}' referenced by {source_id}",
            ))

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    def get_errors(self) -> list[KnowledgeReferenceError]:
        return list(self._errors)

    def summary(self) -> dict[str, Any]:
        return {"errors": len(self._errors), "details": [str(e) for e in self._errors]}
