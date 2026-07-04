from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from .aad import AADConfig


class IdentityProviderKind(str, Enum):
    LOCAL = "local"
    AAD = "aad"
    GOOGLE = "google"
    LDAP = "ldap"
    OPENID_CONNECT = "openid_connect"
    SAML = "saml"


@dataclass(frozen=True, slots=True)
class Identity:
    tenant: str | None
    object_id: str | None
    username: str
    display_name: str
    email: str | None
    groups: tuple[str, ...] = ()
    roles: tuple[str, ...] = ()
    scopes: tuple[str, ...] = ()
    claims: dict[str, object] | None = None
    provider: str = IdentityProviderKind.LOCAL.value
    authentication_method: str = "local"


@dataclass(frozen=True, slots=True)
class AuthenticationResult:
    success: bool
    provider: str
    identity: Identity
    message: str = ""


class IdentityProvider:
    def load_identity(self, principal: str) -> Identity:
        raise NotImplementedError


class IdentityValidator:
    def validate_provider(self, provider: str) -> str:
        allowed = {IdentityProviderKind.LOCAL.value, IdentityProviderKind.AAD.value, IdentityProviderKind.GOOGLE.value, IdentityProviderKind.LDAP.value, IdentityProviderKind.OPENID_CONNECT.value, IdentityProviderKind.SAML.value}
        normalized = str(provider).strip().lower()
        if normalized not in allowed:
            raise ValueError(f"Unsupported identity provider: {provider}")
        return normalized

    def validate_claims(self, identity: Identity, required: tuple[str, ...] = ()) -> None:
        claims = identity.claims or {}
        missing = [claim for claim in required if str(claim) not in claims]
        if missing:
            raise ValueError(f"Missing required claims: {', '.join(missing)}")


class LocalIdentityProvider(IdentityProvider):
    def load_identity(self, principal: str) -> Identity:
        return Identity(
            tenant=None,
            object_id=None,
            username=principal,
            display_name=principal,
            email=None,
            groups=(),
            roles=(),
            scopes=(),
            claims={},
            provider=IdentityProviderKind.LOCAL.value,
            authentication_method="local",
        )


class AADIdentityProvider(IdentityProvider):
    def __init__(self, config: AADConfig | None = None) -> None:
        self.config = config or AADConfig(enabled=False)

    def load_identity(self, principal: str) -> Identity:
        return Identity(
            tenant=self.config.tenant_id,
            object_id=None,
            username=principal,
            display_name=principal,
            email=principal if "@" in principal else None,
            groups=(),
            roles=(),
            scopes=self.config.scopes,
            claims={"provider": IdentityProviderKind.AAD.value, "enabled": self.config.enabled},
            provider=IdentityProviderKind.AAD.value,
            authentication_method="scaffold" if self.config.enabled else "disabled",
        )


class AADAuthenticationProvider:
    def __init__(self, config: AADConfig | None = None) -> None:
        self.config = config or AADConfig(enabled=False)
        self.identity_provider = AADIdentityProvider(self.config)

    def authenticate(self, *, principal: str, credentials: Mapping[str, object] | None = None) -> AuthenticationResult:
        if not self.config.enabled:
            return AuthenticationResult(success=False, provider=IdentityProviderKind.AAD.value, identity=self.identity_provider.load_identity(principal), message="AAD disabled")
        identity = self.identity_provider.load_identity(principal)
        return AuthenticationResult(success=True, provider=IdentityProviderKind.AAD.value, identity=identity, message="AAD scaffold")
