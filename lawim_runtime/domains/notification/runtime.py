from __future__ import annotations

from typing import Any
from uuid import uuid4

from lawim_runtime.domains.base.context import DomainRuntimeContext
from lawim_runtime.domains.base.errors import DomainValidationError
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.base.runtime import DomainRuntime

from .models import NotificationData, NotificationStatus


class NotificationRuntime(DomainRuntime):
    runtime_name: str = "notification"
    supported_actions: list[str] = [
        "PREPARE_NOTIFICATION",
        "SCHEDULE_NOTIFICATION",
        "CANCEL_NOTIFICATION",
    ]

    def __init__(self) -> None:
        self._notifications: dict[str, NotificationData] = {}

    def execute_op(self, request: DomainRuntimeRequest, context: DomainRuntimeContext) -> dict[str, Any]:
        action = request.action_code
        params = request.parameters

        if action == "PREPARE_NOTIFICATION":
            return self._execute_prepare(params)
        elif action == "SCHEDULE_NOTIFICATION":
            return self._execute_schedule(params)
        elif action == "CANCEL_NOTIFICATION":
            return self._execute_cancel(params)
        else:
            raise DomainValidationError(f"unsupported action: {action}")

    def _dedup_key(self, params: dict[str, Any]) -> str:
        project_id = params.get("project_id", "")
        template_name = params.get("template_name", "")
        return f"{project_id}:{template_name}"

    def _execute_prepare(self, params: dict[str, Any]) -> dict[str, Any]:
        dedup_key = self._dedup_key(params)
        existing = self._notifications.get(dedup_key)
        if existing and existing.status in (NotificationStatus.PREPARED, NotificationStatus.SCHEDULED):
            return {
                "status": NotificationStatus.PREPARED.value,
                "notification_id": existing.notification_id,
                "deduplicated": True,
            }
        notification_id = params.get("notification_id", "") or uuid4().hex[:16]
        data = NotificationData(
            notification_id=notification_id,
            project_id=params.get("project_id", ""),
            recipient_type=params.get("recipient_type", ""),
            channel=params.get("channel", ""),
            template_name=params.get("template_name", ""),
            parameters=params.get("parameters", {}),
            priority=params.get("priority", 0),
            scheduled_at=params.get("scheduled_at", ""),
            status=NotificationStatus.PREPARED,
        )
        self._notifications[dedup_key] = data
        self._notifications[notification_id] = data
        return {
            "status": NotificationStatus.PREPARED.value,
            "notification_id": notification_id,
            "deduplicated": False,
        }

    def _execute_schedule(self, params: dict[str, Any]) -> dict[str, Any]:
        notification_id = params.get("notification_id", "")
        dedup_key = self._dedup_key(params)
        data = self._notifications.get(dedup_key)
        if not data:
            data = self._notifications.get(notification_id)
        if not data:
            return {
                "status": NotificationStatus.FAILED.value,
                "notification_id": notification_id,
                "error": "notification not found",
            }
        data.status = NotificationStatus.SCHEDULED
        return {
            "status": NotificationStatus.SCHEDULED.value,
            "notification_id": data.notification_id,
        }

    def _execute_cancel(self, params: dict[str, Any]) -> dict[str, Any]:
        notification_id = params.get("notification_id", "")
        dedup_key = self._dedup_key(params)
        data = self._notifications.get(dedup_key)
        if not data:
            data = self._notifications.get(notification_id)
        if not data:
            return {
                "status": NotificationStatus.FAILED.value,
                "notification_id": notification_id,
                "error": "notification not found",
            }
        data.status = NotificationStatus.CANCELLED
        return {
            "status": NotificationStatus.CANCELLED.value,
            "notification_id": data.notification_id,
        }

    def validate(self, request: DomainRuntimeRequest) -> list[str]:
        errors = super().validate(request)
        params = request.parameters
        action = request.action_code
        if action in ("PREPARE_NOTIFICATION", "SCHEDULE_NOTIFICATION"):
            if not params.get("project_id"):
                errors.append("project_id is required for notification")
            if not params.get("template_name"):
                errors.append("template_name is required for notification")
        if action == "PREPARE_NOTIFICATION":
            if not params.get("recipient_type"):
                errors.append("recipient_type is required for PREPARE_NOTIFICATION")
            if not params.get("channel"):
                errors.append("channel is required for PREPARE_NOTIFICATION")
        return errors

    def verify(self, request: DomainRuntimeRequest, output: dict[str, Any]) -> bool:
        if not isinstance(output, dict):
            return False
        if "status" not in output:
            return False
        return True
