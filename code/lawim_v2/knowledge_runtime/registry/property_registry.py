from __future__ import annotations

import logging
from typing import Any

from ..models.taxonomy import PropertyType
from .base import BaseRegistry
from .errors import (
    AmbiguousAliasError,
    DuplicateEntryError,
    MissingParentError,
    CycleDetectionError,
    RegistryNotFoundError,
)

logger = logging.getLogger(__name__)


class PropertyTaxonomyRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, PropertyType] = {}
        self._by_alias: dict[str, str] = {}
        self._families: dict[str, list[str]] = {}

    def register(self, item: PropertyType) -> None:
        self._check_readonly()
        if item.canonical_id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate property type: {item.canonical_id}",
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
        family = item.family or "uncategorized"
        if family not in self._families:
            self._families[family] = []
        self._families[family].append(item.canonical_id)

    def lock(self) -> None:
        self._validate_references()
        self._lock()

    def _validate_references(self) -> None:
        for pid, pt in self._by_id.items():
            if pt.parent_id and pt.parent_id not in self._by_id:
                raise MissingParentError(
                    f"Property type {pid} references missing parent {pt.parent_id}",
                    child_id=pid,
                    missing_parent_id=pt.parent_id,
                )
        self._detect_cycles()

    def _detect_cycles(self) -> None:
        visited: set[str] = set()
        rec_stack: set[str] = set()
        parent_map: dict[str, str | None] = {}
        for pid, pt in self._by_id.items():
            parent_map[pid] = pt.parent_id

        def dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            parent = parent_map.get(node)
            if parent and parent in self._by_id:
                if parent not in visited:
                    path.append(parent)
                    dfs(parent, path)
                elif parent in rec_stack:
                    raise CycleDetectionError(
                        f"Cycle detected in property taxonomy: {' -> '.join(path + [parent])}",
                        cycle_path=path + [parent],
                    )
            rec_stack.discard(node)

        for pid in self._by_id:
            if pid not in visited:
                dfs(pid, [pid])

    def get(self, type_id: str) -> PropertyType:
        if type_id in self._by_id:
            return self._by_id[type_id]
        raise RegistryNotFoundError(f"Property type not found: {type_id}", identifier=type_id)

    def resolve(self, name_or_alias: str) -> list[PropertyType]:
        if name_or_alias in self._by_id:
            return [self._by_id[name_or_alias]]
        if name_or_alias in self._by_alias:
            return [self._by_id[self._by_alias[name_or_alias]]]
        results = [pt for pt in self._by_id.values() if name_or_alias.lower() in pt.canonical_name.lower()]
        return results

    def list_by_family(self, family: str) -> list[PropertyType]:
        ids = self._families.get(family, [])
        return [self._by_id[i] for i in ids if i in self._by_id]

    def all(self) -> list[PropertyType]:
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
