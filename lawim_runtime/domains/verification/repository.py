from __future__ import annotations

from abc import ABC, abstractmethod

from .models import VerificationCheck, VerificationData


class VerificationRepository(ABC):

    @abstractmethod
    def save(self, verification: VerificationData) -> None:
        ...

    @abstractmethod
    def get(self, verification_id: str) -> VerificationData | None:
        ...

    @abstractmethod
    def list_by_project(self, project_id: str) -> list[VerificationData]:
        ...

    @abstractmethod
    def update_check(self, verification_id: str, check: VerificationCheck) -> None:
        ...

    @abstractmethod
    def list_pending(self) -> list[VerificationData]:
        ...


class InMemoryVerificationRepository(VerificationRepository):

    def __init__(self) -> None:
        self._verifications: dict[str, VerificationData] = {}

    def save(self, verification: VerificationData) -> None:
        self._verifications[verification.verification_id] = verification

    def get(self, verification_id: str) -> VerificationData | None:
        return self._verifications.get(verification_id)

    def list_by_project(self, project_id: str) -> list[VerificationData]:
        return [v for v in self._verifications.values() if v.project_id == project_id]

    def update_check(self, verification_id: str, check: VerificationCheck) -> None:
        verification = self._verifications.get(verification_id)
        if verification:
            for i, c in enumerate(verification.checks):
                if c.check_id == check.check_id:
                    verification.checks[i] = check
                    return
            verification.checks.append(check)

    def list_pending(self) -> list[VerificationData]:
        return [
            v for v in self._verifications.values()
            if v.global_status in ("NOT_STARTED", "IN_PROGRESS")
        ]
