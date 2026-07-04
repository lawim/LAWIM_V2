from __future__ import annotations

from typing import Iterable, Mapping


class RoleMapper:
    def __init__(self, mapping: Mapping[str, str] | None = None) -> None:
        self.mapping = {str(group): str(role) for group, role in (mapping or {}).items()}

    def map_groups_to_roles(self, groups: Iterable[str]) -> tuple[str, ...]:
        roles: list[str] = []
        for group in groups:
            role = self.mapping.get(str(group))
            if role is not None and role not in roles:
                roles.append(role)
        return tuple(roles)
