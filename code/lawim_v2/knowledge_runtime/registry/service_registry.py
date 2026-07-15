from __future__ import annotations

import logging
from typing import Any

from ..models.taxonomy import ServiceType
from .base import BaseRegistry
from .errors import (
    AmbiguousAliasError,
    DuplicateEntryError,
    MissingParentError,
    RegistryNotFoundError,
)

logger = logging.getLogger(__name__)


class ServiceTaxonomyRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, ServiceType] = {}
        self._by_alias: dict[str, str] = {}
        self._families: dict[str, list[str]] = {}

    def register(self, item: ServiceType) -> None:
        self._check_readonly()
        if item.canonical_id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate service type: {item.canonical_id}",
                identifier=item.canonical_id,
            )
        for alias in item.aliases:
            if alias in self._by_alias and self._by_alias[alias] != item.canonical_id:
                raise AmbiguousAliasError(
                    f"Alias '{alias}' already maps to {self._by_alias[alias]}",
                    alias=alias,
                    matches=[self._by_alias[alias], item.canonical_id],
                )
        self._by_id[item.canonical_id] = item
        for alias in item.aliases:
            self._by_alias[alias] = item.canonical_id
        family = item.service_family or "uncategorized"
        if family not in self._families:
            self._families[family] = []
        self._families[family].append(item.canonical_id)

    def lock(self) -> None:
        self._lock()

    def get(self, service_id: str) -> ServiceType:
        if service_id in self._by_id:
            return self._by_id[service_id]
        raise RegistryNotFoundError(f"Service type not found: {service_id}", identifier=service_id)

    def resolve(self, name_or_alias: str) -> list[ServiceType]:
        if name_or_alias in self._by_id:
            return [self._by_id[name_or_alias]]
        if name_or_alias in self._by_alias:
            return [self._by_id[self._by_alias[name_or_alias]]]
        results = [st for st in self._by_id.values() if name_or_alias.lower() in st.canonical_name.lower()]
        return results

    def list_by_family(self, family: str) -> list[ServiceType]:
        ids = self._families.get(family, [])
        return [self._by_id[i] for i in ids if i in self._by_id]

    def all(self) -> list[ServiceType]:
        return list(self._by_id.values())

    def families(self) -> dict[str, list[str]]:
        return dict(self._families)

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({
            "registrations": self.count(),
            "families": len(self._families),
            "aliases": len(self._by_alias),
        })
        return base
