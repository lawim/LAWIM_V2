from __future__ import annotations

from collections.abc import Iterable

OFFICIAL_USER_ROLES: tuple[str, ...] = ("admin", "manager", "operator", "partner", "user",
    "commercial", "auditor", "super_admin", "service_provider")

USER_ROLE_ALIASES: dict[str, str] = {
    "admin": "admin",
    "administrator": "admin",
    "superadmin": "super_admin",
    "director": "admin",
    "root": "admin",
    "manager": "manager",
    "supervisor": "manager",
    "lead": "manager",
    "coordinator": "manager",
    "operator": "operator",
    "agent": "operator",
    "operateur": "operator",
    "opérateur": "operator",
    "staff": "operator",
    "support": "operator",
    "moderator": "operator",
    "partner": "partner",
    "photographer": "partner",
    "photographe": "partner",
    "notary": "partner",
    "notaire": "partner",
    "bank": "partner",
    "banque": "partner",
    "artisan": "partner",
    "architect": "partner",
    "architecte": "partner",
    "diagnostician": "partner",
    "diagnostiqueur": "partner",
    "decorator": "partner",
    "decorateur": "partner",
    "demenageur": "partner",
    "mover": "partner",
    "broker": "partner",
    "user": "user",
    "owner": "user",
    "buyer": "user",
    "seller": "user",
    "vendeur": "user",
    "acheteur": "user",
    "tenant": "user",
    "locataire": "user",
    "landlord": "user",
    "proprietaire": "user",
    "investor": "user",
    "investisseur": "user",
    "promoter": "user",
    "promoteur": "user",
    "customer": "user",
    "viewer": "user",
    "company": "user",
    "enterprise": "user",
    "entreprise": "user",
    "business": "user",
    "particulier": "user",
    "private": "user",
    "requester": "user",
    # V3 roles mapped to themselves
    "commercial": "commercial",
    "auditor": "auditor",
    "super_admin": "super_admin",
    "service_provider": "service_provider",
    "property_manager": "user",
    "doc_manager": "user",
    "finance_manager": "user",
    "visit_manager": "user",
}

USER_ROLE_VALUES: tuple[str, ...] = tuple(dict.fromkeys((*OFFICIAL_USER_ROLES, *USER_ROLE_ALIASES.keys())))

ROLE_LABELS_FR: dict[str, str] = {
    "admin": "Administrateur LAWIM",
    "manager": "Manager",
    "operator": "Opérateur LAWIM",
    "partner": "Partenaire",
    "user": "Utilisateur",
    "commercial": "Commercial LAWIM",
    "auditor": "Auditeur",
    "super_admin": "Super Administrateur",
    "service_provider": "Prestataire de services",
}


def normalize_user_role(value: object, *, default: str = "") -> str:
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if not normalized:
        return default
    if normalized in USER_ROLE_VALUES:
        return normalized
    resolved = USER_ROLE_ALIASES.get(normalized)
    return resolved or default


def accept_user_role(value: object, *, default: str = "") -> str:
    if value is None:
        return default
    normalized = str(value).strip().lower()
    if normalized in USER_ROLE_VALUES:
        return normalized
    return default


def resolve_official_user_role(value: object, *, default: str = "") -> str:
    role = normalize_user_role(value, default=default)
    if not role:
        return default
    return USER_ROLE_ALIASES.get(role, role)


def resolve_highest_role(values: Iterable[object], *, default: str = "user") -> str:
    candidates = [resolve_official_user_role(value) for value in values]
    for role in OFFICIAL_USER_ROLES:
        if role in candidates:
            return role
    return default
