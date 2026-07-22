from __future__ import annotations

from lawim_runtime.domains.base.policy import DomainRuntimePolicy

DOCUMENT_POLICY = DomainRuntimePolicy(
    idempotent=True,
    max_attempts=3,
    timeout_seconds=120,
    shadow_mode=True,
)
