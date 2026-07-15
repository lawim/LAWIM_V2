from __future__ import annotations

import logging
from typing import Any

from ..models.role import Role
from .base import BaseRegistry
from .errors import (
    AmbiguousAliasError,
    DuplicateEntryError,
    RegistryNotFoundError,
)

logger = logging.getLogger(__name__)

VALID_ROLE_DIMENSIONS: frozenset[str] = frozenset({
    "system_role",
    "business_role",
    "user_typology",
    "professional_category",
    "transaction_participant_role",
    "organization_role",
    "CRM_status",
    "permission_scope",
    "trust_level",
    "badge",
    "agency_structure",
})


class RoleRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, Role] = {}
        self._by_alias: dict[str, str] = {}
        self._by_dimension: dict[str, list[str]] = {}

    def register(self, item: Role) -> None:
        self._check_readonly()
        if item.id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate role: {item.id}",
                identifier=item.id,
            )
        if item.dimension not in VALID_ROLE_DIMENSIONS:
            raise ValueError(f"Invalid role dimension: {item.dimension}")
        for alias in item.aliases:
            if alias in self._by_alias and self._by_alias[alias] != item.id:
                raise AmbiguousAliasError(
                    f"Alias '{alias}' already maps to {self._by_alias[alias]}",
                    alias=alias,
                    matches=[self._by_alias[alias], item.id],
                )
        self._by_id[item.id] = item
        for alias in item.aliases:
            self._by_alias[alias] = item.id
        if item.dimension not in self._by_dimension:
            self._by_dimension[item.dimension] = []
        self._by_dimension[item.dimension].append(item.id)

    def lock(self) -> None:
        self._lock()

    def get(self, role_id: str) -> Role:
        if role_id in self._by_id:
            return self._by_id[role_id]
        raise RegistryNotFoundError(f"Role not found: {role_id}", identifier=role_id)

    def resolve(self, name_or_alias: str) -> list[Role]:
        if name_or_alias in self._by_id:
            return [self._by_id[name_or_alias]]
        if name_or_alias in self._by_alias:
            return [self._by_id[self._by_alias[name_or_alias]]]
        results = [r for r in self._by_id.values() if name_or_alias.lower() in r.name.lower()]
        return results

    def list_by_dimension(self, dimension: str) -> list[Role]:
        ids = self._by_dimension.get(dimension, [])
        return [self._by_id[i] for i in ids if i in self._by_id]

    def all(self) -> list[Role]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({
            "registrations": self.count(),
            "dimensions": len(self._by_dimension),
            "aliases": len(self._by_alias),
        })
        return base
