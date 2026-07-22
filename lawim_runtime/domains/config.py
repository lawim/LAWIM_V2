from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DomainRuntimeConfig:
    matching_enabled: bool = False
    visit_enabled: bool = False
    crm_enabled: bool = False
    notification_enabled: bool = False
    document_enabled: bool = False
    verification_enabled: bool = False
    transaction_enabled: bool = False
    payment_enabled: bool = False

    shadow_mode: bool = True
    log_divergences: bool = True

    @property
    def any_enabled(self) -> bool:
        return any([
            self.matching_enabled,
            self.visit_enabled,
            self.crm_enabled,
            self.notification_enabled,
            self.document_enabled,
            self.verification_enabled,
            self.transaction_enabled,
            self.payment_enabled,
        ])


DEFAULT_DOMAIN_CONFIG = DomainRuntimeConfig()
