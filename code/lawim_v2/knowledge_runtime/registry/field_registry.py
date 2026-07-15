from __future__ import annotations

import logging
from typing import Any

from ..models.field import FieldDefinition
from .base import BaseRegistry
from .errors import DuplicateEntryError, RegistryNotFoundError

logger = logging.getLogger(__name__)


class FieldRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, FieldDefinition] = {}
        self._known_types: frozenset[str] = frozenset({
            "string", "enum", "integer", "boolean", "float", "date", "array", "number",
        })

    def register(self, item: FieldDefinition) -> None:
        self._check_readonly()
        if item.data_type not in self._known_types:
            raise ValueError(
                f"Unknown field data type '{item.data_type}' for field '{item.field_id}'. "
                f"Must be one of {sorted(self._known_types)}"
            )
        if item.field_id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate field: {item.field_id}",
                identifier=item.field_id,
            )
        self._by_id[item.field_id] = item

    def lock(self) -> None:
        self._lock()

    def get(self, field_id: str) -> FieldDefinition:
        if field_id in self._by_id:
            return self._by_id[field_id]
        raise RegistryNotFoundError(f"Field not found: {field_id}", identifier=field_id)

    def all(self) -> list[FieldDefinition]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({"registrations": self.count()})
        return base
