from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MockAccessToken:
    value: str
    token_type: str = "access"


@dataclass(frozen=True, slots=True)
class MockIDToken:
    value: str
    token_type: str = "id"


@dataclass(frozen=True, slots=True)
class MockRefreshToken:
    value: str
    token_type: str = "refresh"
