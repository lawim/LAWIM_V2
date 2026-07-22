from __future__ import annotations

import logging
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult

logger = logging.getLogger(__name__)


class V2DocumentAdapter:
    def to_domain_request(self, v2_payload: dict[str, Any]) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id=v2_payload.get("request_id", ""),
            action_code=v2_payload.get("action_code", ""),
            parameters={
                "project_id": v2_payload.get("project_id", ""),
                "document_type": v2_payload.get("document_type", ""),
                "file_reference": v2_payload.get("file_reference", ""),
                "doc_id": v2_payload.get("doc_id", ""),
                "status": v2_payload.get("status", ""),
                **{k: v for k, v in v2_payload.get("metadata", {}).items() if k not in ("project_id", "document_type", "file_reference", "doc_id", "status")},
            },
            correlation_id=v2_payload.get("correlation_id", ""),
            causation_id=v2_payload.get("causation_id", ""),
            idempotency_key=v2_payload.get("idempotency_key", ""),
            metadata=v2_payload.get("metadata", {}),
        )

    def from_domain_result(self, domain_result: DomainRuntimeResult) -> dict[str, Any]:
        return {
            "request_id": domain_result.request_id,
            "action_code": domain_result.action_code,
            "status": domain_result.status.value,
            "output": domain_result.output,
            "error": domain_result.error,
            "events": domain_result.events,
            "metrics": domain_result.metrics,
            "metadata": domain_result.metadata,
        }

    def record_divergence(
        self,
        v2_result: dict[str, Any],
        v3_result: dict[str, Any],
    ) -> None:
        v2_status = v2_result.get("status")
        v3_status = v3_result.get("status", {}).get("status") if isinstance(v3_result.get("status"), dict) else v3_result.get("status")
        if v2_status != v3_status:
            logger.info(
                "document divergence: v2_status=%s v3_status=%s v2_result=%s v3_result=%s",
                v2_status,
                v3_status,
                v2_result,
                v3_result,
            )
