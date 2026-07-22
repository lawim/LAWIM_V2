from __future__ import annotations

from lawim_runtime.domains.base.policy import DomainRuntimePolicy

NOTIFICATION_POLICY = DomainRuntimePolicy(
    idempotent=True,
    max_attempts=3,
    timeout_seconds=30,
    shadow_mode=True,
)
