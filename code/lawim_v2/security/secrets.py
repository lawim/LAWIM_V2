from __future__ import annotations


class SecretProvider:
    def __init__(self, provider_name: str = "external") -> None:
        self.provider_name = provider_name

    def resolve_secret(self, name: str) -> str | None:
        raise NotImplementedError

    def store_secret(self, name: str, value: str) -> None:
        raise NotImplementedError


class ExternalSecretProvider(SecretProvider):
    def __init__(self, provider_name: str = "external") -> None:
        super().__init__(provider_name)

    def resolve_secret(self, name: str) -> str | None:
        return None

    def store_secret(self, name: str, value: str) -> None:
        return None
