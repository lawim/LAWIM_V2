from __future__ import annotations

from lawim_runtime.domains.base.policy import DomainRuntimePolicy

CRM_POLICY = DomainRuntimePolicy(
    idempotent=True,
    max_attempts=3,
    timeout_seconds=60,
    shadow_mode=True,
)
