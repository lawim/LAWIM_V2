from __future__ import annotations

from lawim_runtime.domains.base.policy import DomainRuntimePolicy

VERIFICATION_POLICY = DomainRuntimePolicy(
    idempotent=True,
    max_attempts=2,
    timeout_seconds=120,
    shadow_mode=True,
)
