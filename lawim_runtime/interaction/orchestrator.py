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
        ai_policy: Any = None,
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
        self._ai_policy = ai_policy

    def set_extraction_handler(self, handler: Any) -> None:
        self._extraction_handler = handler

    def set_ai_policy(self, policy: Any) -> None:
        self._ai_policy = policy

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

        response_plan = self._build_response_plan(
            context=context,
            correlation_id=correlation_id,
            envelope=envelope,
            identity_status=identity.status,
            session=session,
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

    def _build_response_plan(
        self,
        context: InteractionContext,
        correlation_id: str,
        envelope: InteractionEnvelope,
        identity_status: Any,
        session: Any,
    ) -> InteractionResponsePlan:
        plan = InteractionResponsePlan(
            project_id=context.project_id,
            correlation_id=correlation_id,
            metadata={
                "identity_status": identity_status.value if hasattr(identity_status, 'value') else str(identity_status),
                "session_id": session.session_id if hasattr(session, 'session_id') else "",
            },
        )

        if self._ai_policy and self._ai_policy.is_extraction_enabled():
            try:
                ai_request = self._build_ai_request(envelope, context, correlation_id)
                ai_result = self._ai_policy.gateway.process(ai_request) if self._ai_policy.gateway else None
                if ai_result and ai_result.structured_output:
                    plan.metadata["ai_extraction"] = ai_result.structured_output
            except Exception as e:
                logger.warning("ai extraction failed (falling back): %s", e)

        if self._ai_policy and self._ai_policy.is_writer_enabled():
            writer_req = self._build_writer_request(plan, context)
            if self._ai_policy.ai_writer:
                writer_result = self._ai_policy.ai_writer.write(writer_req)
                if writer_result.success and not writer_result.fallback_used:
                    val_result = self._ai_policy.response_validator.validate(writer_result.text, plan)
                    if val_result.valid:
                        plan.metadata["ai_written"] = True
                        plan.metadata["ai_writer_text"] = writer_result.text
                    else:
                        logger.warning("ai writer output invalid, using deterministic fallback")
                        fallback_req = ResponseWriterRequest(response_plan=plan)
                        fb = self._ai_policy.det_writer.write(fallback_req)
                        plan.metadata["ai_writer_fallback"] = True
                        if fb.text:
                            plan.metadata["ai_writer_text"] = fb.text

        return plan

    def _build_ai_request(self, envelope: InteractionEnvelope, context: InteractionContext, correlation_id: str) -> Any:
        from ..intelligence.request import AIRequest, AITaskType
        return AIRequest(
            task_type=AITaskType.FIELD_EXTRACTION,
            interaction_id=envelope.interaction_id,
            project_id=context.project_id,
            session_id=context.session_id,
            input_text=envelope.raw_content,
            correlation_id=correlation_id,
        )

    def _build_writer_request(self, plan: InteractionResponsePlan, context: InteractionContext) -> Any:
        from ..intelligence.writing.writer import AIResponseWriterRequest
        return AIResponseWriterRequest(
            response_plan=plan,
            context={"project_id": context.project_id, "session_id": context.session_id},
            correlation_id=plan.correlation_id,
        )

    def _build_safe_fallback(self, correlation_id: str = "") -> InteractionResponsePlan:
        return InteractionResponsePlan(
            response_type=ResponseType.SAFE_FALLBACK,
            correlation_id=correlation_id,
        )
