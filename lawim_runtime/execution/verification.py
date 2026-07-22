from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class VerificationStatus(str, Enum):
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"
    INCONCLUSIVE = "INCONCLUSIVE"


@dataclass
class VerificationResult:
    status: VerificationStatus = VerificationStatus.PENDING
    checks: list[dict[str, Any]] = field(default_factory=list)
    verified_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    errors: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == VerificationStatus.PASSED

    @property
    def failed(self) -> bool:
        return self.status == VerificationStatus.FAILED


class ExecutionVerifier:
    def verify(
        self,
        action_code: str,
        output: dict[str, Any],
        expected: dict[str, Any] | None = None,
    ) -> VerificationResult:
        result = VerificationResult()

        if not output:
            result.status = VerificationStatus.INCONCLUSIVE
            result.errors.append("No output to verify")
            return result

        checks: list[dict[str, Any]] = []
        if expected:
            for key, expected_value in expected.items():
                actual = output.get(key)
                check = {
                    "key": key,
                    "expected": expected_value,
                    "actual": actual,
                    "match": actual == expected_value,
                }
                checks.append(check)
                if actual != expected_value:
                    result.errors.append(f"Key '{key}': expected {expected_value}, got {actual}")

        result.checks = checks
        result.status = VerificationStatus.PASSED if not result.errors else VerificationStatus.FAILED
        return result
