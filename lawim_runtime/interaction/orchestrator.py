from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .context import InteractionContext
from .correlation import CorrelationManager
from .deduplication import DeduplicationStatus, InteractionDeduplicator
from .delivery import DeliveryManager, DeliveryResult, DeliveryStatus
from .envelope import InteractionEnvelope
from .gateway import InteractionGateway
from .identity import IdentityResolver, IdentityStatus
from .normalization import MessageNormalizer
from .project_resolution import ProjectResolver, ProjectResolutionStatus
from .response_plan import InteractionResponsePlan, ResponseType
from .session import SessionManager, SessionStatus

logger = logging.getLogger(__name__)


@dataclass
class OrchestrationResult:
    turn_id: str = field(default_factory=lambda: uuid4().hex[:16])
    envelope: InteractionEnvelope | None = None
    context: InteractionContext | None = None
    response_plan: InteractionResponsePlan | None = None
    delivery_result: DeliveryResult | None = None
    error: str = ""
    warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class InteractionOrchestrator:
    def __init__(
        self,
        gateway: InteractionGateway | None = None,
        normalizer: MessageNormalizer | None = None,
        deduplicator: InteractionDeduplicator | None = None,
        identity_resolver: IdentityResolver | None = None,
        session_manager: SessionManager | None = None,
        project_resolver: ProjectResolver | None = None,
        correlation_manager: CorrelationManager | None = None,
        delivery_manager: DeliveryManager | None = None,
    ) -> None:
        self._gateway = gateway or InteractionGateway()
        self._normalizer = normalizer or MessageNormalizer()
        self._deduplicator = deduplicator or InteractionDeduplicator()
        self._identity_resolver = identity_resolver or IdentityResolver()
        self._session_manager = session_manager or SessionManager()
        self._project_resolver = project_resolver or ProjectResolver()
        self._correlation = correlation_manager or CorrelationManager()
        self._delivery = delivery_manager or DeliveryManager()
        self._extraction_handler = None

    def set_extraction_handler(self, handler: Any) -> None:
        self._extraction_handler = handler

    def process(self, envelope: InteractionEnvelope) -> OrchestrationResult:
        result = OrchestrationResult(envelope=envelope)
        correlation_id = self._correlation.create(envelope.correlation_id or "")
        self._correlation.update(correlation_id, interaction_id=envelope.interaction_id)
        warnings: list[str] = []

        gateway_check = self._gateway.validate_envelope(envelope)
        if not gateway_check.valid:
            result.error = gateway_check.error
            logger.warning("gateway validation failed: %s", gateway_check.error)
            result.response_plan = self._build_safe_fallback(correlation_id)
            return result

        dedup = self._deduplicator.check(envelope.external_message_id, envelope.channel)
        if dedup == DeduplicationStatus.DUPLICATE:
            warnings.append(f"duplicate message {envelope.external_message_id} on {envelope.channel}")
            result.response_plan = InteractionResponsePlan(
                response_type=ResponseType.NO_RESPONSE,
                correlation_id=correlation_id,
            )
            result.warnings = warnings
            return result

        norm = self._normalizer.normalize(envelope.raw_content, envelope.channel)
        if norm.is_empty:
            result.response_plan = InteractionResponsePlan(
                response_type=ResponseType.NO_RESPONSE,
                correlation_id=correlation_id,
            )
            result.warnings = warnings
            return result

        identity = self._identity_resolver.resolve(envelope.channel, envelope.external_user_id, envelope.raw_sender)
        if identity.status == IdentityStatus.BLOCKED:
            result.error = "identity blocked"
            result.response_plan = self._build_safe_fallback(correlation_id)
            return result

        session = self._session_manager.resume_or_create(
            identity.actor_id or identity.identity_id,
            envelope.channel,
        )

        project = self._project_resolver.resolve(identity.actor_id or identity.identity_id)
        if project.status == ProjectResolutionStatus.AMBIGUOUS:
            warnings.append("multiple active projects, clarification needed")

        context = InteractionContext(
            interaction=envelope,
            actor_id=identity.actor_id or identity.identity_id,
            user_id=identity.user_id or identity.identity_id,
            channel_identity=envelope.channel,
            session_id=session.session_id,
            project_id=project.project_id,
            correlation_id=correlation_id,
        )

        if not project.project_id and project.status == ProjectResolutionStatus.NEW_PROJECT:
            new_project_id = uuid4().hex[:16]
            self._project_resolver.register_project(
                identity.actor_id or identity.identity_id,
                new_project_id,
            )
            context.project_id = new_project_id

        response_plan = InteractionResponsePlan(
            project_id=context.project_id,
            correlation_id=correlation_id,
            metadata={"identity_status": identity.status.value, "session_id": session.session_id},
        )

        delivery_result = self._delivery.deliver(response_plan, envelope.channel)

        result.context = context
        result.response_plan = response_plan
        result.delivery_result = delivery_result
        result.warnings = warnings

        self._correlation.update(
            correlation_id,
            session_id=session.session_id,
            project_id=context.project_id,
        )

        return result

    def _build_safe_fallback(self, correlation_id: str = "") -> InteractionResponsePlan:
        return InteractionResponsePlan(
            response_type=ResponseType.SAFE_FALLBACK,
            correlation_id=correlation_id,
        )
