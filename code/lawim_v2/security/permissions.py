from __future__ import annotations

from .constants import PERMISSION_ACTIONS


def permission_key(resource: str, action: str) -> str:
    resource_norm = (resource or "*").strip().lower()
    action_norm = (action or "read").strip().lower()
    if action_norm not in PERMISSION_ACTIONS:
        action_norm = "read"
    return f"{resource_norm}:{action_norm}"


def matches_permission(*, granted: str, required: str) -> bool:
    if granted == required:
        return True
    g_resource, _, g_action = granted.partition(":")
    r_resource, _, r_action = required.partition(":")
    if g_resource in {"*", r_resource} and g_action in {"*", r_action, "admin"}:
        return True
    return False


def evaluate_permissions(*, grants: list[str], required: list[str]) -> bool:
    if not required:
        return True
    return all(any(matches_permission(granted=g, required=r) for g in grants) for r in required)
