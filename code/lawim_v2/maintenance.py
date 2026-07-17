from __future__ import annotations

from dataclasses import dataclass

from .observability import METRICS

MAINTENANCE_RESPONSE = (
    "LAWIM est momentanément indisponible.\n\n"
    "Site Web : https://lawim.app\n"
    "Téléphone : +237 686 822 667\n"
    "WhatsApp : +237 686 822 667\n"
    "WhatsApp Business : @lawimofficial\n"
    "Telegram : @lawim_bot\n"
    "Facebook : @lawimofficial\n"
    "Email : contact@lawim.app"
)

MAINTENANCE_FLAGS: dict[str, bool] = {
    "lawim_core_rebuild_maintenance_mode": False,
    "conversation_service_enabled": True,
    "qualification_service_enabled": True,
    "search_orchestration_enabled": True,
    "matching_service_enabled": True,
    "relationship_service_enabled": True,
    "automated_relationship_consent_enabled": True,
    "conversation_driven_visits_enabled": True,
}

MAINTENANCE_EVENTS = {
    "message_received": "lawim.rebuild.maintenance_message_received",
    "handover_requested": "lawim.rebuild.human_handover_requested",
    "blocked_automatic_action": "lawim.rebuild.automated_processing_blocked",
}


@dataclass(frozen=True, slots=True)
class MaintenanceSubmission:
    channel: str
    raw_message: str
    user_id: int | None = None
    channel_identity_id: int | None = None
    delivery_metadata: dict[str, object] | None = None
    handover_requested: bool = False


class MaintenanceService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def status(self) -> dict[str, object]:
        return {
            "maintenance_mode": True,
            "message": MAINTENANCE_RESPONSE,
            "flags": dict(MAINTENANCE_FLAGS),
            "services": {
                "conversation": "DECOMMISSIONED",
                "qualification": "DECOMMISSIONED",
                "search_orchestration": "DECOMMISSIONED",
                "matching": "DECOMMISSIONED",
                "relationship": "DECOMMISSIONED",
            },
        }

    def submit_message(self, submission: MaintenanceSubmission) -> dict[str, object]:
        row = self.repository.create_maintenance_message(
            user_id=submission.user_id,
            channel_identity_id=submission.channel_identity_id,
            channel=submission.channel,
            raw_message=submission.raw_message,
            delivery_metadata=submission.delivery_metadata or {},
            handover_requested=submission.handover_requested,
        )
        self.repository.record_event(
            MAINTENANCE_EVENTS["handover_requested" if submission.handover_requested else "message_received"],
            {
                "maintenance_message_id": row["id"],
                "channel": submission.channel,
                "handover_requested": submission.handover_requested,
            },
        )
        METRICS.increment(
            "lawim_rebuild_handover_requests_total"
            if submission.handover_requested
            else "lawim_rebuild_maintenance_messages_total"
        )
        METRICS.increment("lawim_rebuild_blocked_automatic_actions_total")
        return {
            "message": row,
            "response": MAINTENANCE_RESPONSE,
            "automated_processing": "blocked",
            "handover_requested": submission.handover_requested,
        }

    def request_handover(self, submission: MaintenanceSubmission) -> dict[str, object]:
        return self.submit_message(
            MaintenanceSubmission(
                channel=submission.channel,
                raw_message=submission.raw_message,
                user_id=submission.user_id,
                channel_identity_id=submission.channel_identity_id,
                delivery_metadata=submission.delivery_metadata,
                handover_requested=True,
            )
        )
