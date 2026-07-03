from __future__ import annotations

import base64
import hashlib
import hmac
import os
import secrets
from dataclasses import dataclass


PBKDF2_ITERATIONS = 210_000
TEST_PBKDF2_ITERATIONS = 1_000
_TRUE_VALUES = {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class PasswordRecord:
    salt: str
    hash: str


def _pbkdf2_iterations() -> int:
    # Production keeps the current cost. Tests must opt in explicitly.
    if os.getenv("LAWIM_TEST_MODE", "").strip().lower() in _TRUE_VALUES:
        return TEST_PBKDF2_ITERATIONS
    if os.getenv("APP_ENV", "").strip().lower() == "test":
        return TEST_PBKDF2_ITERATIONS
    return PBKDF2_ITERATIONS


def hash_password(password: str, salt: bytes | None = None) -> PasswordRecord:
    raw_salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        raw_salt,
        _pbkdf2_iterations(),
    )
    return PasswordRecord(
        salt=base64.b64encode(raw_salt).decode("ascii"),
        hash=digest.hex(),
    )


def verify_password(password: str, salt: str, expected_hash: str) -> bool:
    actual = hash_password(password, base64.b64decode(salt.encode("ascii")))
    return hmac.compare_digest(actual.hash, expected_hash)


def create_session_token() -> str:
    return secrets.token_urlsafe(32)


_EMAIL_PATTERN = __import__("re").compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str) -> str:
    normalized = email.strip().lower()
    if not normalized or not _EMAIL_PATTERN.match(normalized):
        raise ValueError("email format is invalid")
    return normalized


def validate_password(password: str, *, min_length: int = 8) -> None:
    if len(password) < min_length:
        raise ValueError(f"password must be at least {min_length} characters")
