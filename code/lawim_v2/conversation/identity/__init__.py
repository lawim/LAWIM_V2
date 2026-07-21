from __future__ import annotations

from .models import (
    IdentityBinding,
    IdentityConfidence,
    IdentitySource,
    ResolvedIdentity,
    CrossChannelConsent,
)
from .resolver import (
    IdentityBindingRepository,
    CrossChannelConsentRepository,
    CrossChannelIdentityResolver,
)
from .events import (
    IDENTITY_RESOLVED,
    IDENTITY_CONSENT_REQUIRED,
    IDENTITY_RESUMED,
    IDENTITY_CONFLICT,
)

__all__ = [
    "IdentityConfidence",
    "IdentitySource",
    "ResolvedIdentity",
    "IdentityBinding",
    "CrossChannelConsent",
    "IdentityBindingRepository",
    "CrossChannelConsentRepository",
    "CrossChannelIdentityResolver",
    "IDENTITY_RESOLVED",
    "IDENTITY_CONSENT_REQUIRED",
    "IDENTITY_RESUMED",
    "IDENTITY_CONFLICT",
]
