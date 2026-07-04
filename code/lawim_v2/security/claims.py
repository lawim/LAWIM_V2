from __future__ import annotations

from typing import Mapping

from .identity import Identity


class ClaimsManager:
    def read_claims(self, raw_claims: Mapping[str, object] | None) -> dict[str, object]:
        if not raw_claims:
            return {}
        return {str(key): self._normalize(value) for key, value in raw_claims.items()}

    def validate_claims(self, claims: Mapping[str, object], required: tuple[str, ...] = ()) -> bool:
        return all(str(claim) in claims for claim in required)

    def map_identity(self, identity: Identity) -> dict[str, object]:
        return {
            "provider": identity.provider,
            "roles": identity.roles,
            "groups": identity.groups,
            "claims": identity.claims or {},
        }

    def _normalize(self, value: object) -> object:
        if isinstance(value, (list, tuple)):
            return tuple(str(item) for item in value)
        if isinstance(value, set):
            return tuple(str(item) for item in sorted(value))
        return value
