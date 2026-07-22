from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timezone

from .models import VisitRecord, VisitStatus


class VisitRepository(ABC):

    @abstractmethod
    def save_visit(self, visit: VisitRecord) -> None:
        ...

    @abstractmethod
    def get_visit(self, visit_id: str) -> VisitRecord | None:
        ...

    @abstractmethod
    def list_by_property(self, property_id: str) -> list[VisitRecord]:
        ...

    @abstractmethod
    def cancel_visit(self, visit_id: str) -> VisitRecord | None:
        ...

    @abstractmethod
    def list_upcoming(self) -> list[VisitRecord]:
        ...


class InMemoryVisitRepository(VisitRepository):

    def __init__(self) -> None:
        self._visits: dict[str, VisitRecord] = {}

    def save_visit(self, visit: VisitRecord) -> None:
        self._visits[visit.visit_id] = visit

    def get_visit(self, visit_id: str) -> VisitRecord | None:
        return self._visits.get(visit_id)

    def list_by_property(self, property_id: str) -> list[VisitRecord]:
        return [v for v in self._visits.values() if v.property_id == property_id]

    def cancel_visit(self, visit_id: str) -> VisitRecord | None:
        record = self._visits.get(visit_id)
        if record is None:
            return None
        record.status = VisitStatus.CANCELLED
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return record

    def list_upcoming(self) -> list[VisitRecord]:
        now = datetime.now(timezone.utc).isoformat()
        return [
            v for v in self._visits.values()
            if v.status in (VisitStatus.SCHEDULED, VisitStatus.CONFIRMED)
            and v.scheduled_date >= now
        ]
