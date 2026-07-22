from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class DomainRuntimeStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    SIMULATED = "SIMULATED"
    DOMAIN_PROVIDER_REQUIRED = "DOMAIN_PROVIDER_REQUIRED"
    HANDLER_NOT_IMPLEMENTED = "HANDLER_NOT_IMPLEMENTED"

    @property
    def is_terminal(self) -> bool:
        return self in {
            DomainRuntimeStatus.SUCCEEDED,
            DomainRuntimeStatus.FAILED,
            DomainRuntimeStatus.SKIPPED,
            DomainRuntimeStatus.SIMULATED,
            DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED,
            DomainRuntimeStatus.HANDLER_NOT_IMPLEMENTED,
        }

    @property
    def is_success(self) -> bool:
        return self == DomainRuntimeStatus.SUCCEEDED

    @property
    def is_failure(self) -> bool:
        return self in {
            DomainRuntimeStatus.FAILED,
            DomainRuntimeStatus.DOMAIN_PROVIDER_REQUIRED,
            DomainRuntimeStatus.HANDLER_NOT_IMPLEMENTED,
        }


@dataclass
class DomainRuntimeResult:
    request_id: str = ""
    action_code: str = ""
    status: DomainRuntimeStatus = DomainRuntimeStatus.PENDING
    output: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""
    metrics: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
