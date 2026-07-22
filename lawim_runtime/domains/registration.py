from __future__ import annotations

import logging
from typing import Any

from lawim_runtime.domains.base.handler import DomainRuntimeHandler
from lawim_runtime.domains.base.result import DomainRuntimeStatus
from lawim_runtime.domains.crm.handlers import CRMHandler
from lawim_runtime.domains.document.handlers import DocumentHandler
from lawim_runtime.domains.matching.handlers import MatchingHandler
from lawim_runtime.domains.notification.handlers import NotificationHandler
from lawim_runtime.domains.payment.handlers import PaymentHandler
from lawim_runtime.domains.transaction.handlers import TransactionHandler
from lawim_runtime.domains.verification.handlers import VerificationHandler
from lawim_runtime.domains.visit.handlers import VisitHandler
from lawim_runtime.execution.context import ActionExecutionContext
from lawim_runtime.execution.registry import ActionHandlerRegistry

from .config import DEFAULT_DOMAIN_CONFIG, DomainRuntimeConfig

logger = logging.getLogger(__name__)


class _ShadowHandler(DomainRuntimeHandler):
    handler_name: str = ""
    supported_actions: list[str] = []

    def can_handle(self, action_code: str) -> bool:
        return action_code in self.supported_actions

    def validate(self, context: ActionExecutionContext) -> list[str]:
        return []

    def prepare(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {}

    def execute(self, context: ActionExecutionContext) -> dict[str, Any]:
        return {
            "status": DomainRuntimeStatus.SIMULATED.value,
            "message": f"shadow mode: {self.handler_name} returned simulated result",
        }

    def verify(self, context: ActionExecutionContext, raw_result: dict[str, Any]) -> bool:
        return True

    def compensate(self, context: ActionExecutionContext, result: Any) -> dict[str, Any]:
        return {}


_HANDLER_DEFINITIONS: list[tuple[str, str, list[str]]] = [
    ("matching", "matching_handler", [
        "START_PRELIMINARY_MATCHING",
        "START_MATCHING",
        "REFINE_MATCHING",
        "PRESENT_MATCHES",
    ]),
    ("visit", "visit_handler", [
        "REQUEST_VISIT_AVAILABILITY",
        "CREATE_VISIT_REQUEST",
        "SCHEDULE_VISIT",
        "CANCEL_VISIT",
    ]),
    ("crm", "crm_handler", [
        "CREATE_OR_UPDATE_LEAD",
        "CREATE_OR_UPDATE_OPPORTUNITY",
        "ESCALATE_TO_HUMAN",
        "SYNC_PROJECT_TIMELINE",
        "CLOSE_CRM_CASE",
    ]),
    ("notification", "notification_handler", [
        "PREPARE_NOTIFICATION",
        "SCHEDULE_NOTIFICATION",
        "CANCEL_NOTIFICATION",
    ]),
    ("document", "document_handler", [
        "REQUEST_DOCUMENT",
        "REGISTER_DOCUMENT",
        "START_DOCUMENT_ANALYSIS",
        "UPDATE_DOCUMENT_STATUS",
    ]),
    ("verification", "verification_handler", [
        "START_VERIFICATION",
        "RUN_VERIFICATION_CHECK",
        "COMPLETE_VERIFICATION",
        "ESCALATE_VERIFICATION",
    ]),
    ("transaction", "transaction_handler", [
        "PREPARE_TRANSACTION",
        "START_NEGOTIATION",
        "UPDATE_NEGOTIATION",
        "CONFIRM_TRANSACTION",
        "CANCEL_TRANSACTION",
        "CLOSE_PROJECT",
    ]),
    ("payment", "payment_handler", [
        "CREATE_PAYMENT_INTENT",
        "REQUEST_PAYMENT",
        "VERIFY_PAYMENT",
        "RECONCILE_PAYMENT",
        "CANCEL_PAYMENT",
        "REFUND_PAYMENT",
    ]),
]

_REAL_HANDLER_FACTORIES: dict[str, callable] = {
    "matching": lambda: MatchingHandler(),
    "visit": lambda: VisitHandler(),
    "crm": lambda: CRMHandler(),
    "notification": lambda: NotificationHandler(),
    "document": lambda: DocumentHandler(),
    "verification": lambda: VerificationHandler(),
    "transaction": lambda: TransactionHandler(),
    "payment": lambda: PaymentHandler(),
}

_ENABLED_ATTR_MAP: dict[str, str] = {
    "matching": "matching_enabled",
    "visit": "visit_enabled",
    "crm": "crm_enabled",
    "notification": "notification_enabled",
    "document": "document_enabled",
    "verification": "verification_enabled",
    "transaction": "transaction_enabled",
    "payment": "payment_enabled",
}


def _build_shadow_handler(
    domain_name: str,
    handler_name: str,
    actions: list[str],
) -> _ShadowHandler:
    handler = _ShadowHandler()
    handler.handler_name = handler_name
    handler.supported_actions = list(actions)
    return handler


def register_domain_runtimes(
    registry: ActionHandlerRegistry,
    config: DomainRuntimeConfig | None = None,
) -> None:
    cfg = config or DEFAULT_DOMAIN_CONFIG

    for domain_name, handler_name, actions in _HANDLER_DEFINITIONS:
        enabled_attr = _ENABLED_ATTR_MAP[domain_name]
        enabled = getattr(cfg, enabled_attr, False)

        if not enabled and not cfg.shadow_mode:
            logger.info("domain runtime %s: disabled, skipping registration", domain_name)
            continue

        if cfg.shadow_mode:
            handler = _build_shadow_handler(domain_name, handler_name, actions)
            registry.register_handler(handler)
            logger.info(
                "domain runtime %s: registered SHADOW handler (%s) with %d actions",
                domain_name,
                handler_name,
                len(actions),
            )
        else:
            factory = _REAL_HANDLER_FACTORIES[domain_name]
            handler = factory()
            registry.register_handler(handler)
            logger.info(
                "domain runtime %s: registered REAL handler (%s) with %d actions",
                domain_name,
                handler_name,
                len(actions),
            )
