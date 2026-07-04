from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class IdentityGroup:
    name: str
    source: str = "claims"
    display_name: str | None = None


class GroupMapper:
    def from_claims(self, values: Iterable[str]) -> tuple[IdentityGroup, ...]:
        return tuple(IdentityGroup(name=str(value), source="claims", display_name=str(value)) for value in values)
