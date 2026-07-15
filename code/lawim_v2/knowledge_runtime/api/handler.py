from __future__ import annotations

import json
import logging
from http import HTTPStatus
from typing import Any

from ..constants import LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API, LAWIM_FEATURE_KNOWLEDGE_RUNTIME
from ..errors import KnowledgeNotLoadedError
from ..registry.errors import RegistryNotFoundError
from ..service import KnowledgeService

logger = logging.getLogger(__name__)


class KnowledgeApiHandler:
    def __init__(self, service: KnowledgeService, internal_api_enabled: bool) -> None:
        self._service = service
        self._enabled = internal_api_enabled

    def _check_enabled(self) -> None:
        if not self._enabled:
            raise ApiDisabledError("Knowledge internal API is disabled")

    def handle_health(self) -> dict[str, Any]:
        self._check_enabled()
        return self._service.health()

    def handle_version(self) -> dict[str, Any]:
        self._check_enabled()
        ver = self._service.version_registry.get()
        if ver is None:
            return {"version": None}
        return ver.dict()

    def handle_registries(self) -> dict[str, Any]:
        self._check_enabled()
        return self._service.registry_summaries()

    def handle_property_types(self, type_id: str | None = None, query: str | None = None) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.property_registry
        if type_id:
            try:
                pt = reg.get(type_id)
                return {
                    "canonical_id": pt.canonical_id,
                    "canonical_name": pt.canonical_name,
                    "aliases": list(pt.aliases),
                    "parent_id": pt.parent_id,
                    "family": pt.family,
                    "subtype": pt.subtype,
                    "applicable_transactions": list(pt.applicable_transactions),
                    "qualification_matrix_ids": list(pt.qualification_matrix_ids),
                    "sources": list(pt.sources),
                }
            except RegistryNotFoundError:
                return {"error": "not_found"}
        if query:
            results = reg.resolve(query)
            return {"results": [{"id": r.canonical_id, "name": r.canonical_name} for r in results]}
        return {"property_types": [{"id": pt.canonical_id, "name": pt.canonical_name} for pt in reg.all()]}

    def handle_services(self, service_id: str | None = None, query: str | None = None) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.service_registry
        if service_id:
            try:
                st = reg.get(service_id)
                return {
                    "canonical_id": st.canonical_id,
                    "canonical_name": st.canonical_name,
                    "service_family": st.service_family,
                    "aliases": list(st.aliases),
                    "sources": list(st.sources),
                }
            except RegistryNotFoundError:
                return {"error": "not_found"}
        if query:
            results = reg.resolve(query)
            return {"results": [{"id": r.canonical_id, "name": r.canonical_name} for r in results]}
        return {"services": [{"id": st.canonical_id, "name": st.canonical_name} for st in reg.all()]}

    def handle_roles(self) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.role_registry
        return {"roles": [{"id": r.id, "name": r.name, "dimension": r.dimension} for r in reg.all()]}

    def handle_intents(self) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.intent_registry
        return {"intents": [{"id": i.id, "name": i.name} for i in reg.all()]}

    def handle_transactions(self) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.transaction_registry
        return {"transactions": [{"id": t.id, "name": t.name} for t in reg.all()]}

    def handle_matrices(self, matrix_id: str | None = None) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.matrix_registry
        if matrix_id:
            try:
                m = reg.get(matrix_id)
                return {
                    "matrix_id": m.matrix_id,
                    "canonical_name": m.canonical_name,
                    "request_family": m.request_family,
                    "property_type": m.property_type,
                    "sources": list(m.sources),
                }
            except RegistryNotFoundError:
                return {"error": "not_found"}
        return {"matrices": [{"id": m.matrix_id, "name": m.canonical_name} for m in reg.all()]}

    def handle_field(self, field_id: str) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.field_registry
        try:
            f = reg.get(field_id)
            return {
                "field_id": f.field_id,
                "label": f.label,
                "data_type": f.data_type,
                "matching_role": f.matching_role,
                "privacy_level": f.privacy_level,
            }
        except RegistryNotFoundError:
            return {"error": "not_found"}

    def handle_source_trace(self, concept_id: str) -> dict[str, Any]:
        self._check_enabled()
        reg = self._service.source_trace_registry
        try:
            t = reg.get(concept_id)
            return {
                "concept_id": t.concept_id,
                "concept_type": t.concept_type,
                "source_path": t.source_path,
                "source_section": t.source_section,
            }
        except RegistryNotFoundError:
            return {"error": "not_found"}


class ApiDisabledError(Exception):
    def __init__(self, message: str = "API disabled") -> None:
        super().__init__(message)
