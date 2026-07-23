from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.result import DomainRuntimeResult, DomainRuntimeStatus
from lawim_runtime.domains.base.runtime import DomainRuntime

from .models import VisitRecord, VisitStatus


class VisitRuntime(DomainRuntime):
    runtime_name: str = "visit"
    supported_actions: list[str] = [
        "REQUEST_VISIT_AVAILABILITY",
        "CREATE_VISIT_REQUEST",
        "SCHEDULE_VISIT",
        "CONFIRM_VISIT",
        "COMPLETE_VISIT",
        "NO_SHOW_VISIT",
        "RESCHEDULE_VISIT",
        "CANCEL_VISIT",
    ]

    def __init__(self) -> None:
        self._visits: dict[str, VisitRecord] = {}
        self._availability_cache: dict[str, list[dict[str, Any]]] = {}

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "REQUEST_VISIT_AVAILABILITY":
            return self._execute_availability(params)
        elif action == "CREATE_VISIT_REQUEST":
            return self._execute_create(params, request.idempotency_key)
        elif action == "SCHEDULE_VISIT":
            return self._execute_schedule(params)
        elif action == "CONFIRM_VISIT":
            return self._execute_confirm(params)
        elif action == "COMPLETE_VISIT":
            return self._execute_complete(params)
        elif action == "NO_SHOW_VISIT":
            return self._execute_no_show(params)
        elif action == "RESCHEDULE_VISIT":
            return self._execute_reschedule(params)
        elif action == "CANCEL_VISIT":
            return self._execute_cancel(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _execute_availability(self, params: dict[str, Any]) -> dict[str, Any]:
        property_id = params.get("property_id", "")
        if not property_id:
            return {
                "status": VisitStatus.FAILED.value,
                "error": "property_id is required",
            }
        cached = self._availability_cache.get(property_id)
        if cached is not None:
            return {
                "status": VisitStatus.AVAILABILITY_CHECKING.value,
                "availability": cached,
            }
        slots = [
            {"date": "2026-07-25", "times": ["09:00", "11:00", "14:00", "16:00"]},
            {"date": "2026-07-26", "times": ["10:00", "12:00", "15:00"]},
            {"date": "2026-07-27", "times": ["09:00", "11:00", "14:00"]},
        ]
        self._availability_cache[property_id] = slots
        return {
            "status": VisitStatus.AVAILABILITY_CHECKING.value,
            "availability": slots,
        }

    def _execute_create(self, params: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
        property_id = params.get("property_id", "")
        requester = params.get("requester_name", "") or params.get("requester_contact", "")
        if not property_id:
            return {
                "status": VisitStatus.FAILED.value,
                "error": "property_id is required",
            }
        if not requester:
            return {
                "status": VisitStatus.FAILED.value,
                "error": "requester name or contact is required",
            }
        existing = self._find_duplicate(property_id, requester)
        if existing is not None:
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"duplicate visit request for property {property_id} by {requester}",
                "visit_id": existing.visit_id,
            }
        record = VisitRecord(
            property_id=property_id,
            requester=requester,
            status=VisitStatus.PENDING,
        )
        if idempotency_key and idempotency_key in self._visits:
            existing_ik = self._visits[idempotency_key]
            return {
                "status": existing_ik.status.value,
                "visit_id": existing_ik.visit_id,
            }
        self._visits[record.visit_id] = record
        return {
            "status": VisitStatus.PENDING.value,
            "visit_id": record.visit_id,
            "property_id": record.property_id,
            "requester": record.requester,
        }

    def _execute_schedule(self, params: dict[str, Any]) -> dict[str, Any]:
        visit_id = params.get("visit_id", "")
        scheduled_date = params.get("scheduled_date", "")
        if not visit_id:
            return {
                "status": VisitStatus.FAILED.value,
                "error": "visit_id is required",
            }
        if not scheduled_date:
            return {
                "status": VisitStatus.FAILED.value,
                "error": "scheduled_date is required",
            }
        record = self._visits.get(visit_id)
        if record is None:
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"visit {visit_id} not found",
            }
        blocked = self._transition(record, VisitStatus.SCHEDULED)
        if blocked:
            return blocked
        record.scheduled_date = scheduled_date
        record.status = VisitStatus.SCHEDULED
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return {
            "status": VisitStatus.SCHEDULED.value,
            "visit_id": record.visit_id,
            "scheduled_date": record.scheduled_date,
        }

    def _execute_cancel(self, params: dict[str, Any]) -> dict[str, Any]:
        visit_id = params.get("visit_id", "")
        if not visit_id:
            return {
                "status": VisitStatus.FAILED.value,
                "error": "visit_id is required",
            }
        record = self._visits.get(visit_id)
        if record is None:
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"visit {visit_id} not found",
            }
        if record.status in (VisitStatus.COMPLETED, VisitStatus.CANCELLED, VisitStatus.NO_SHOW):
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"visit {visit_id} already in terminal state {record.status.value}",
            }
        record.status = VisitStatus.CANCELLED
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return {
            "status": VisitStatus.CANCELLED.value,
            "visit_id": record.visit_id,
        }

    def _transition(self, record: VisitRecord, target: VisitStatus) -> dict[str, Any] | None:
        allowed = {
            "PENDING": ["SCHEDULED", "CANCELLED", "FAILED"],
            "AVAILABILITY_CHECKING": ["PENDING", "SCHEDULED", "CANCELLED", "FAILED"],
            "SCHEDULED": ["CONFIRMED", "CANCELLED", "FAILED", "NO_SHOW"],
            "CONFIRMED": ["COMPLETED", "CANCELLED", "NO_SHOW", "FAILED"],
            "COMPLETED": [],
            "CANCELLED": [],
            "NO_SHOW": [],
            "REJECTED": [],
            "FAILED": [],
        }
        current = record.status.value
        if current not in allowed:
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"visit {record.visit_id} has unknown status {current}",
            }
        if target.value not in allowed[current]:
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"cannot transition visit {record.visit_id} from {current} to {target.value}",
            }
        return None

    def _execute_confirm(self, params: dict[str, Any]) -> dict[str, Any]:
        visit_id = params.get("visit_id", "")
        record = self._visits.get(visit_id)
        if not record:
            return {"status": VisitStatus.FAILED.value, "error": f"visit {visit_id} not found"}
        blocked = self._transition(record, VisitStatus.CONFIRMED)
        if blocked:
            return blocked
        record.status = VisitStatus.CONFIRMED
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return {"status": VisitStatus.CONFIRMED.value, "visit_id": record.visit_id}

    def _execute_complete(self, params: dict[str, Any]) -> dict[str, Any]:
        visit_id = params.get("visit_id", "")
        record = self._visits.get(visit_id)
        if not record:
            return {"status": VisitStatus.FAILED.value, "error": f"visit {visit_id} not found"}
        blocked = self._transition(record, VisitStatus.COMPLETED)
        if blocked:
            return blocked
        record.status = VisitStatus.COMPLETED
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return {"status": VisitStatus.COMPLETED.value, "visit_id": record.visit_id}

    def _execute_no_show(self, params: dict[str, Any]) -> dict[str, Any]:
        visit_id = params.get("visit_id", "")
        record = self._visits.get(visit_id)
        if not record:
            return {"status": VisitStatus.FAILED.value, "error": f"visit {visit_id} not found"}
        blocked = self._transition(record, VisitStatus.NO_SHOW)
        if blocked:
            return blocked
        record.status = VisitStatus.NO_SHOW
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return {"status": VisitStatus.NO_SHOW.value, "visit_id": record.visit_id}

    def _execute_reschedule(self, params: dict[str, Any]) -> dict[str, Any]:
        visit_id = params.get("visit_id", "")
        new_date = params.get("scheduled_date", "")
        record = self._visits.get(visit_id)
        if not record:
            return {"status": VisitStatus.FAILED.value, "error": f"visit {visit_id} not found"}
        if not new_date:
            return {"status": VisitStatus.FAILED.value, "error": "scheduled_date is required for reschedule"}
        if record.status != VisitStatus.SCHEDULED:
            return {
                "status": VisitStatus.FAILED.value,
                "error": f"cannot reschedule visit {visit_id} from {record.status.value}",
            }
        record.scheduled_date = new_date
        record.updated_at = datetime.now(timezone.utc).isoformat()
        return {"status": VisitStatus.SCHEDULED.value, "visit_id": record.visit_id, "scheduled_date": record.scheduled_date}

    def _find_duplicate(self, property_id: str, requester: str) -> VisitRecord | None:
        for record in self._visits.values():
            if record.property_id == property_id and record.requester == requester:
                if record.status in (VisitStatus.PENDING, VisitStatus.AVAILABILITY_CHECKING, VisitStatus.SCHEDULED, VisitStatus.CONFIRMED):
                    return record
        return None

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action in ("REQUEST_VISIT_AVAILABILITY", "CREATE_VISIT_REQUEST", "SCHEDULE_VISIT") and not params.get("property_id"):
            errors.append("property_id is required for visit operations")
        if action in ("SCHEDULE_VISIT", "CONFIRM_VISIT", "COMPLETE_VISIT", "NO_SHOW_VISIT", "RESCHEDULE_VISIT", "CANCEL_VISIT") and not params.get("visit_id"):
            errors.append(f"visit_id is required for {action}")
        visit_type = params.get("visit_type", "")
        if visit_type and visit_type not in ("physical", "virtual"):
            errors.append("visit_type must be 'physical' or 'virtual'")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        if "status" not in output:
            return False
        return True
