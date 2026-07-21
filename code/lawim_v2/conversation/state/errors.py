from __future__ import annotations


class StateConflictError(Exception):
    """Raised when optimistic locking detects a version conflict."""

    def __init__(self, message: str, expected_version: int, actual_version: int):
        self.expected_version = expected_version
        self.actual_version = actual_version
        super().__init__(message)
