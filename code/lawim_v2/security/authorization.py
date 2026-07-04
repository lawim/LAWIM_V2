from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Mapping


@dataclass(frozen=True, slots=True)
class AuthorizationDecision:
    allowed: bool
    reason: str = ""


class BaseAuthorizer:
    def authorize(self, actor: object, context: Mapping[str, object] | None = None) -> AuthorizationDecision:
        raise NotImplementedError


class RoleBasedAuthorizer(BaseAuthorizer):
    def __init__(self, allowed_roles: tuple[str, ...] = ("admin",)) -> None:
        self.allowed_roles = allowed_roles

    def authorize(self, actor: object, context: Mapping[str, object] | None = None) -> AuthorizationDecision:
        if isinstance(actor, Mapping):
            role = actor.get("role")
            if role is not None and str(role) in self.allowed_roles:
                return AuthorizationDecision(allowed=True, reason="role")
        return AuthorizationDecision(allowed=False, reason="missing_role")


class PolicyBasedAuthorizer(BaseAuthorizer):
    def __init__(self, policy: Callable[[object, Mapping[str, object] | None], bool]) -> None:
        self.policy = policy

    def authorize(self, actor: object, context: Mapping[str, object] | None = None) -> AuthorizationDecision:
        return AuthorizationDecision(allowed=self.policy(actor, context), reason="policy")


class ClaimsBasedAuthorizer(BaseAuthorizer):
    def __init__(self, required_claims: tuple[str, ...] = ()) -> None:
        self.required_claims = required_claims

    def authorize(self, actor: object, context: Mapping[str, object] | None = None) -> AuthorizationDecision:
        claims: Mapping[str, object] = {}
        if isinstance(actor, Mapping):
            claims = actor.get("claims") if isinstance(actor.get("claims"), Mapping) else {}
        allowed = all(str(claim) in claims for claim in self.required_claims)
        return AuthorizationDecision(allowed=allowed, reason="claims")
