from __future__ import annotations

import logging
import re
from typing import Any

from ..models.qualification import QualificationMatrix
from .base import BaseRegistry
from .errors import DuplicateEntryError, RegistryNotFoundError, AmbiguousSelectionError

logger = logging.getLogger(__name__)

_NORMALIZE_RE = re.compile(r"[^a-z0-9_]")


def _normalize(text: str) -> str:
    return _NORMALIZE_RE.sub("", text.lower().replace("-", "_").replace(" ", "_"))


_MATCH_EXACT = "exact_match"
_MATCH_NORMALIZED = "normalized_match"
_MATCH_PARTIAL = "authorized_partial_match"
_MATCH_GENERIC = "generic_family_match"
_MATCH_AMBIGUITY = "ambiguity"
_MATCH_NOT_FOUND = "not_found"


class MatrixRegistry(BaseRegistry):
    def __init__(self) -> None:
        super().__init__()
        self._by_id: dict[str, QualificationMatrix] = {}
        self._by_normalized_id: dict[str, str] = {}
        self._by_family: dict[str, list[str]] = {}
        self._by_property_type: dict[str, list[str]] = {}

    def register(self, item: QualificationMatrix) -> None:
        self._check_readonly()
        if item.matrix_id in self._by_id:
            raise DuplicateEntryError(
                f"Duplicate matrix: {item.matrix_id}",
                identifier=item.matrix_id,
            )
        self._by_id[item.matrix_id] = item
        nid = _normalize(item.matrix_id)
        if nid != item.matrix_id:
            self._by_normalized_id[nid] = item.matrix_id
        family = item.request_family
        if family not in self._by_family:
            self._by_family[family] = []
        self._by_family[family].append(item.matrix_id)
        ptype = item.property_type
        if ptype not in self._by_property_type:
            self._by_property_type[ptype] = []
        self._by_property_type[ptype].append(item.matrix_id)

    def lock(self) -> None:
        self._lock()

    def get(self, matrix_id: str) -> QualificationMatrix:
        if matrix_id in self._by_id:
            return self._by_id[matrix_id]
        nid = _normalize(matrix_id)
        if nid in self._by_normalized_id:
            return self._by_id[self._by_normalized_id[nid]]
        raise RegistryNotFoundError(f"Matrix not found: {matrix_id}", identifier=matrix_id)

    def resolve(
        self, query: str, *, property_type: str | None = None, family: str | None = None
    ) -> dict[str, Any]:
        query_norm = _normalize(query)

        if query in self._by_id:
            return {"match_type": _MATCH_EXACT, "matrices": [self._by_id[query]]}

        if query_norm in self._by_normalized_id:
            return {"match_type": _MATCH_NORMALIZED, "matrices": [self._by_id[self._by_normalized_id[query_norm]]]}

        candidates: list[QualificationMatrix] = []

        if property_type and property_type in self._by_property_type:
            for mid in self._by_property_type[property_type]:
                m = self._by_id[mid]
                if (query_norm in _normalize(m.canonical_name)
                        or query_norm in _normalize(m.matrix_id)
                        or query_norm in _normalize(m.property_type)):
                    candidates.append(m)

        if not candidates and family and family in self._by_family:
            for mid in self._by_family[family]:
                m = self._by_id[mid]
                if query_norm in _normalize(m.canonical_name) or query_norm in _normalize(m.property_type):
                    candidates.append(m)

        if not candidates:
            for m in self._by_id.values():
                if query_norm in _normalize(m.canonical_name):
                    candidates.append(m)

        if not candidates:
            return {"match_type": _MATCH_NOT_FOUND, "matrices": []}

        if len(candidates) > 1:
            return {"match_type": _MATCH_AMBIGUITY, "matrices": candidates}

        return {"match_type": _MATCH_PARTIAL, "matrices": [candidates[0]]}

    def list_by_family(self, family: str) -> list[QualificationMatrix]:
        ids = self._by_family.get(family, [])
        return [self._by_id[i] for i in ids if i in self._by_id]

    def list_by_property_type(self, ptype: str) -> list[QualificationMatrix]:
        ids = self._by_property_type.get(ptype, [])
        return [self._by_id[i] for i in ids if i in self._by_id]

    def all(self) -> list[QualificationMatrix]:
        return list(self._by_id.values())

    def count(self) -> int:
        return len(self._by_id)

    def summary(self) -> dict[str, Any]:
        base = super().summary()
        base.update({
            "registrations": self.count(),
            "families": len(self._by_family),
            "property_types": len(self._by_property_type),
        })
        return base
