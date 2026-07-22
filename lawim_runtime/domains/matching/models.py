from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus


@dataclass
class MatchingRequestData:
    property_type: str = ""
    bedrooms: int = 0
    min_budget: float = 0.0
    max_budget: float = 0.0
    city: str = ""
    district: str = ""
    features: list[str] = field(default_factory=list)
    criteria: dict[str, Any] = field(default_factory=dict)


@dataclass
class MatchingRequest:
    request_id: str = ""
    action_code: str = ""
    data: MatchingRequestData = field(default_factory=MatchingRequestData)
    correlation_id: str = ""
    idempotency_key: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_request(self) -> DomainRuntimeRequest:
        return DomainRuntimeRequest(
            request_id=self.request_id,
            action_code=self.action_code,
            parameters={
                "property_type": self.data.property_type,
                "bedrooms": self.data.bedrooms,
                "min_budget": self.data.min_budget,
                "max_budget": self.data.max_budget,
                "city": self.data.city,
                "district": self.data.district,
                "features": self.data.features,
                "criteria": self.data.criteria,
            },
            correlation_id=self.correlation_id,
            idempotency_key=self.idempotency_key,
            metadata=self.metadata,
        )


@dataclass
class MatchingResultItem:
    property_id: str = ""
    score: float = 0.0
    match_reasons: list[str] = field(default_factory=list)
    match_explanations: dict[str, Any] = field(default_factory=dict)
    property_snapshot: dict[str, Any] = field(default_factory=dict)


class MatchingStatus(str, Enum):
    MATCH_FOUND = "MATCH_FOUND"
    NO_MATCH = "NO_MATCH"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    DOMAIN_PROVIDER_REQUIRED = "DOMAIN_PROVIDER_REQUIRED"
    SIMULATED = "SIMULATED"
    FAILED = "FAILED"


@dataclass
class MatchingResult:
    request_id: str = ""
    action_code: str = ""
    status: MatchingStatus = MatchingStatus.NO_MATCH
    matches: list[MatchingResultItem] = field(default_factory=list)
    total_count: int = 0
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_domain_result(self) -> DomainRuntimeResult:
        domain_status_map = {
            MatchingStatus.MATCH_FOUND: DomainRuntimeStatus.SUCCEEDED,
            MatchingStatus.NO_MATCH: DomainRuntimeStatus.SUCCEEDED,
            MatchingStatus.INSUFFICIENT_DATA: DomainRuntimeStatus.FAILED,
            MatchingStatus.DOMAIN_PROVIDER_REQUIRED: DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED,
            MatchingStatus.SIMULATED: DomainRuntimeStatus.SIMULATED,
            MatchingStatus.FAILED: DomainRuntimeStatus.FAILED,
        }
        return DomainRuntimeResult(
            request_id=self.request_id,
            action_code=self.action_code,
            status=domain_status_map.get(self.status, DomainRuntimeStatus.FAILED),
            output={
                "status": self.status.value,
                "matches": [
                    {
                        "property_id": m.property_id,
                        "score": m.score,
                        "match_reasons": m.match_reasons,
                        "match_explanations": m.match_explanations,
                        "property_snapshot": m.property_snapshot,
                    }
                    for m in self.matches
                ],
                "total_count": self.total_count,
            },
            error=self.error,
            metadata=self.metadata,
        )
