from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
import os


@dataclass(frozen=True, slots=True)
class AADConfig:
    enabled: bool
    tenant_id: str | None = None
    client_id: str | None = None
    scopes: tuple[str, ...] = ()
    redirect_uri: str | None = None
    secret_provider: str = "external"
    provider: str = "aad"
    authentication_method: str = "scaffold"

    def validate(self) -> None:
        if not self.enabled:
            return
        missing = []
        if not self.tenant_id:
            missing.append("tenant_id")
        if not self.client_id:
            missing.append("client_id")
        if self.provider not in {"aad", "entra"}:
            raise ValueError(f"Unsupported AAD provider: {self.provider}")
        if not self.authentication_method:
            raise ValueError("AAD authentication_method must not be empty")
        if missing:
            raise ValueError(f"AAD configuration is incomplete: {', '.join(missing)}")


@dataclass(frozen=True, slots=True)
class AADAuthResult:
    enabled: bool
    mode: str
    message: str
    provider: str | None = None


class AADAuthenticator:
    def __init__(self, config: AADConfig | None = None) -> None:
        self.config = config or AADConfig(enabled=False)

    def is_enabled(self) -> bool:
        return self.config.enabled

    def authenticate(self, *, email: str | None = None, password: str | None = None) -> AADAuthResult:
        if not self.is_enabled():
            return AADAuthResult(enabled=False, mode="disabled", message="AAD authentication is disabled")
        return AADAuthResult(
            enabled=True,
            mode="scaffold",
            message="AAD scaffold is active; no Microsoft network call is performed",
            provider="entra",
        )


def _bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def resolve_aad_config(env: Mapping[str, str] | None = None) -> AADConfig:
    source = os.environ if env is None else env
    enabled = _bool_env("LAWIM_AAD_ENABLED", False) or str(source.get("LAWIM_AAD_ENABLED", "")).strip().lower() in {"1", "true", "yes", "on"}
    tenant_id = str(source.get("LAWIM_AAD_TENANT_ID", "")).strip() or None
    client_id = str(source.get("LAWIM_AAD_CLIENT_ID", "")).strip() or None
    scopes = tuple(value.strip() for value in str(source.get("LAWIM_AAD_SCOPES", "")).split(",") if value.strip())
    redirect_uri = str(source.get("LAWIM_AAD_REDIRECT_URI", "")).strip() or None
    secret_provider = str(source.get("SECRET_PROVIDER", "external")).strip() or "external"
    provider = str(source.get("LAWIM_AAD_PROVIDER", "aad")).strip().lower() or "aad"
    authentication_method = str(source.get("LAWIM_AAD_AUTH_METHOD", "scaffold")).strip() or "scaffold"
    config = AADConfig(
        enabled=enabled,
        tenant_id=tenant_id,
        client_id=client_id,
        scopes=scopes,
        redirect_uri=redirect_uri,
        secret_provider=secret_provider,
        provider=provider,
        authentication_method=authentication_method,
    )
    config.validate()
    return config
