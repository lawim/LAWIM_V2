from __future__ import annotations

from ..user_roles import resolve_official_user_role


FINANCIAL_PERMISSION_CODES: tuple[str, ...] = (
    "financial.catalog.read",
    "financial.catalog.manage",
    "financial.pricing.read",
    "financial.pricing.manage",
    "financial.quote.create",
    "financial.quote.issue",
    "financial.invoice.read_own",
    "financial.invoice.read_all",
    "financial.invoice.issue",
    "financial.payment.initiate",
    "financial.payment.read_own",
    "financial.payment.read_all",
    "financial.refund.request",
    "financial.refund.approve",
    "financial.subscription.manage_own",
    "financial.subscription.manage_all",
    "financial.commission.read_own",
    "financial.commission.validate",
    "financial.payout.manage",
    "financial.ledger.read",
    "financial.reconciliation.manage",
    "financial.audit.read",
    "financial.provider.manage",
)


def financial_permission_key(resource: str, action: str) -> str:
    return f"financial.{resource}.{action}"


def can_access_own(actor: dict[str, object] | None, owner_id: int | None) -> bool:
    if actor is None or owner_id is None:
        return False
    return int(actor.get("id") or 0) == int(owner_id)


def can_access_all(actor: dict[str, object] | None) -> bool:
    return resolve_official_user_role(actor.get("role") if actor else None) == "admin"


def can_access_partner_scope(actor: dict[str, object] | None, *, owner_id: int | None = None, owner_org_id: int | None = None) -> bool:
    if actor is None:
        return False
    role = resolve_official_user_role(actor.get("role"))
    if role == "admin":
        return True
    if role == "partner":
        actor_org_id = actor.get("organization_id")
        if owner_org_id is not None and actor_org_id is not None:
            return int(actor_org_id) == int(owner_org_id)
        return owner_id is not None and int(actor.get("id") or 0) == int(owner_id)
    return can_access_own(actor, owner_id)


def can_read_financial_object(actor: dict[str, object] | None, *, owner_id: int | None = None, owner_org_id: int | None = None) -> bool:
    if can_access_all(actor):
        return True
    return can_access_partner_scope(actor, owner_id=owner_id, owner_org_id=owner_org_id)


def can_manage_financial_object(actor: dict[str, object] | None) -> bool:
    return can_access_all(actor) or resolve_official_user_role(actor.get("role") if actor else None) in {"manager", "operator"}
