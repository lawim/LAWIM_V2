from __future__ import annotations

import json
from typing import Any

from .permissions import evaluate_permissions


def evaluate_rbac(*, role_keys: list[str], required_roles: list[str]) -> bool:
    if not required_roles:
        return True
    normalized = {r.lower() for r in role_keys}
    return any(req.lower() in normalized or req.lower().replace("role-", "") in normalized for req in required_roles)


def evaluate_abac(*, attributes: dict[str, Any], rules: list[dict[str, Any]]) -> bool:
    if not rules:
        return True
    for rule in rules:
        attr = str(rule.get("attribute") or "")
        op = str(rule.get("operator") or "eq")
        expected = rule.get("value")
        actual = attributes.get(attr)
        if op == "eq" and actual != expected:
            return False
        if op == "in" and actual not in (expected or []):
            return False
        if op == "gte":
            try:
                if float(actual or 0) < float(expected or 0):
                    return False
            except (TypeError, ValueError):
                return False
    return True


def evaluate_access_policy(
    *,
    role_keys: list[str],
    permission_grants: list[str],
    attributes: dict[str, Any] | None,
    policy: dict[str, object],
) -> bool:
    policy_type = str(policy.get("policy_type") or "rbac")
    rules = policy.get("rules_json") or "[]"
    try:
        parsed_rules = json.loads(str(rules)) if isinstance(rules, str) else list(rules)
    except json.JSONDecodeError:
        parsed_rules = []

    if policy_type == "abac":
        return evaluate_abac(attributes=attributes or {}, rules=parsed_rules)
    if policy_type == "hybrid":
        rbac_ok = evaluate_rbac(role_keys=role_keys, required_roles=[str(r.get("role")) for r in parsed_rules if r.get("role")])
        perm_ok = evaluate_permissions(
            grants=permission_grants,
            required=[str(r.get("permission")) for r in parsed_rules if r.get("permission")],
        )
        abac_ok = evaluate_abac(attributes=attributes or {}, rules=[r for r in parsed_rules if r.get("attribute")])
        return rbac_ok and perm_ok and abac_ok
    required_roles = [str(r.get("role")) for r in parsed_rules if r.get("role")]
    required_perms = [str(r.get("permission")) for r in parsed_rules if r.get("permission")]
    return evaluate_rbac(role_keys=role_keys, required_roles=required_roles) and evaluate_permissions(
        grants=permission_grants,
        required=required_perms,
    )
