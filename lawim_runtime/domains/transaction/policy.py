from __future__ import annotations

from lawim_runtime.domains.base.policy import DomainRuntimePolicy

TRANSACTION_POLICY = DomainRuntimePolicy(
    idempotent=True,
    max_attempts=5,
    timeout_seconds=600,
    shadow_mode=True,
    requires_verification=True,
)
