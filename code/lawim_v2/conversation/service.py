from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from ..maintenance import MAINTENANCE_FLAGS, MAINTENANCE_RESPONSE
from ..observability import METRICS
from ..security.audit import AADAuditLogger

from .domain.actions import Action, ActionStatus
from .domain.conversation import Conversation
from .domain.decisions import ConversationDecision
from .domain.errors import ConversationError
from .domain.facts import FactCollection
from .domain.message import NormalizedMessage
from .domain.states import ConversationState
from .generation.composer import GenerativeComposer
from .generation.validator import ContentValidator
from .memory.service import MemoryService
from .planning.planner import Planner
from .qualification.evaluator import QualificationEvaluator


class ConversationService:
    def __init__(
        self,
        repository: Any,
        memory_repo: Any,
        config: Any,
        planner: Planner | None = None,
        memory_service: MemoryService | None = None,
        qualification_evaluator: QualificationEvaluator | None = None,
        composer: GenerativeComposer | None = None,
        content_validator: ContentValidator | None = None,
        audit_logger: AADAuditLogger | None = None,
    ) -> None:
        self._repository = repository
        self._config = config
        self._planner = planner or Planner()
        self._memory_service = memory_service or MemoryService(memory_repo)
        self._qualification_evaluator = qualification_evaluator or QualificationEvaluator()
        self._composer = composer or GenerativeComposer()
        self._content_validator = content_validator or ContentValidator()
        self._audit_logger = audit_logger or AADAuditLogger()

    def process_message(
        self,
        message: NormalizedMessage,
        shadow_mode: bool = False,
    ) -> dict[str, Any]:
        if MAINTENANCE_FLAGS.get("lawim_core_rebuild_maintenance_mode", False):
            return self._maintenance_response(shadow_mode)

        errors: list[str] = []
        actions: list[dict[str, Any]] = []

        try:
            conversation = self._resolve_conversation(message)
            self._ensure_channel_continuity(conversation, message)

            conversation.updated_at = datetime.now(timezone.utc).isoformat()

            active_projects = self._load_active_projects(conversation)
            active_dossiers = self._load_active_dossiers(conversation)
            known_facts = self._load_known_facts(conversation)

            conversation.facts = FactCollection(
                facts=self._memory_service.get_confirmed_facts(
                    project_id=conversation.project_id,
                    conversation_id=conversation.conversation_id,
                ).facts,
            )
            conversation.known_fields = set(known_facts.keys())

            decision = self._planner.plan(
                message=message,
                conversation=conversation,
                active_projects=active_projects,
                active_dossiers=active_dossiers,
                known_facts=known_facts,
            )

            decision.decision_id = str(uuid4())
            decision.created_at = datetime.now(timezone.utc).isoformat()

            if decision.loop_detected and decision.loop_score >= 40:
                conversation.apply_transition("loop_exceeded")
                decision.state_after = conversation.state

            self._persist_message_facts(decision, message, conversation)

            if decision.selected_intent and decision.intent_confidence >= 0.6:
                self._evaluate_readiness(decision, conversation, known_facts)

            response = self._composer.compose(decision)
            violations = self._content_validator.validate(response, decision)

            for v in violations:
                if v.severity == "error":
                    errors.append(v.message)

            if any(v.severity == "error" for v in violations):
                response = self._composer.compose(decision)

            if not shadow_mode:
                self._persist_conversation(conversation)
                self._persist_decision(decision, conversation)
                self._record_metrics(decision)
            else:
                self._log_shadow_decision(decision)

            actions = self._build_actions_from_decision(decision, shadow_mode)

            self._audit(decision, conversation)

            return {
                "decision": decision,
                "response": response,
                "state": conversation.state.value if conversation.state else "unknown",
                "actions": actions,
                "errors": errors,
                "shadow": shadow_mode,
            }

        except ConversationError as exc:
            errors.append(str(exc))
            return self._error_response(str(exc), errors, shadow_mode, exc.code)
        except Exception as exc:
            errors.append(str(exc))
            return self._error_response(str(exc), errors, shadow_mode)

    def process_message_shadow(self, message: NormalizedMessage) -> dict[str, Any]:
        return self.process_message(message, shadow_mode=True)

    def _resolve_conversation(self, message: NormalizedMessage) -> Conversation:
        if message.conversation_id is not None:
            row = self._repository.get_conversation(message.conversation_id)
            if row:
                return self._row_to_conversation(row)

        if message.channel_identity_id is not None:
            rows = self._repository.list_conversations(
                channel_identity_id=message.channel_identity_id,
                limit=1,
            )
            if rows:
                return self._row_to_conversation(rows[0])

        if message.user_id is not None:
            rows = self._repository.list_active_conversations(
                user_id=message.user_id,
                limit=1,
            )
            if rows:
                return self._row_to_conversation(rows[0])

        now = datetime.now(timezone.utc).isoformat()
        conversation = Conversation(
            user_id=message.user_id,
            channel_identity_id=message.channel_identity_id,
            channel=message.channel,
            state=ConversationState.NEW,
            created_at=now,
            updated_at=now,
        )

        if message.project_id:
            conversation.project_id = message.project_id

        return conversation

    def _ensure_channel_continuity(
        self,
        conversation: Conversation,
        message: NormalizedMessage,
    ) -> None:
        user_id = message.user_id or conversation.user_id
        channel_identity_id = message.channel_identity_id or conversation.channel_identity_id

        if user_id is None and channel_identity_id is None:
            return

        if user_id is not None and channel_identity_id is not None:
            linked = self._repository.find_channel_identity(
                user_id=user_id,
                channel_identity_id=channel_identity_id,
            )
            if not linked:
                self._repository.link_channel_identity(
                    user_id=user_id,
                    channel_identity_id=channel_identity_id,
                    channel=message.channel,
                )

        if user_id is not None:
            conversation.user_id = user_id
        if channel_identity_id is not None:
            conversation.channel_identity_id = channel_identity_id

    def _load_active_projects(self, conversation: Conversation) -> list[dict[str, Any]]:
        if conversation.user_id is None:
            return []
        return self._repository.list_projects(
            user_id=conversation.user_id,
            status="ACTIVE",
        )

    def _load_active_dossiers(self, conversation: Conversation) -> list[dict[str, Any]]:
        if conversation.project_id is None:
            return []
        return self._repository.list_dossiers(
            project_id=conversation.project_id,
        )

    def _load_known_facts(self, conversation: Conversation) -> dict[str, Any]:
        if conversation.project_id is None and conversation.conversation_id is None:
            return {}
        return self._memory_service.all_confirmed_as_dict(
            project_id=conversation.project_id,
        )

    def _persist_message_facts(
        self,
        decision: ConversationDecision,
        message: NormalizedMessage,
        conversation: Conversation,
    ) -> None:
        extracted_facts: list[dict[str, Any]] = message.metadata.get("extracted_facts", [])
        for fact_data in extracted_facts:
            field = fact_data.get("field")
            if not field:
                continue
            if conversation.is_field_known(field):
                continue
            fact = self._memory_service.add_fact(
                field=field,
                raw_value=fact_data.get("raw_value", ""),
                normalized_value=fact_data.get("normalized_value"),
                source_message_id=message.channel_message_id,
                source_channel=message.channel,
                source_type=fact_data.get("source_type", "explicit"),
                confidence=fact_data.get("confidence", 0.9),
                project_id=conversation.project_id,
                conversation_id=conversation.conversation_id,
            )
            conversation.facts.add_fact(fact)
            conversation.mark_field_known(field)

        ambiguous_facts: list[dict[str, Any]] = message.metadata.get("ambiguous_facts", [])
        for amb in ambiguous_facts:
            field = amb.get("field")
            if not field:
                continue
            fact = self._memory_service.add_fact(
                field=field,
                raw_value=amb.get("raw_value", ""),
                source_message_id=message.channel_message_id,
                source_channel=message.channel,
                source_type="ambiguous",
                confidence=0.3,
                project_id=conversation.project_id,
                conversation_id=conversation.conversation_id,
            )
            self._memory_service.mark_ambiguous(fact.fact_id)
            conversation.facts.add_fact(fact)

        decision.known_facts = self._load_known_facts(conversation)

    def _evaluate_readiness(
        self,
        decision: ConversationDecision,
        conversation: Conversation,
        known_facts: dict[str, Any],
    ) -> None:
        evaluation = self._qualification_evaluator.evaluate(
            intent=decision.selected_intent or "",
            known_facts=known_facts,
            transaction_type=decision.transaction_type,
            property_type=decision.property_type,
        )

        decision.missing_required_facts = [mf.field for mf in evaluation.missing_required_fields]
        decision.action_parameters["readiness_score"] = evaluation.readiness_score

        if evaluation.is_ready_for_search and conversation.state == ConversationState.QUALIFYING:
            conversation.apply_transition("minimum_readiness")
            decision.state_after = conversation.state

        if evaluation.is_relationship_ready:
            decision.action_parameters["relationship_ready"] = True

    def _persist_conversation(self, conversation: Conversation) -> None:
        if conversation.conversation_id is not None:
            self._repository.update_conversation(
                conversation_id=conversation.conversation_id,
                state=conversation.state.value if conversation.state else "NEW",
                project_id=conversation.project_id,
                dossier_id=conversation.dossier_id,
                updated_at=datetime.now(timezone.utc).isoformat(),
            )
        else:
            row = self._repository.create_conversation(
                user_id=conversation.user_id,
                channel_identity_id=conversation.channel_identity_id,
                channel=conversation.channel,
                state=conversation.state.value if conversation.state else "NEW",
                project_id=conversation.project_id,
            )
            conversation.conversation_id = row.get("id") or row.get("conversation_id")

    def _persist_decision(
        self,
        decision: ConversationDecision,
        conversation: Conversation,
    ) -> None:
        try:
            self._repository.save_decision(decision.to_dict())
        except Exception:
            METRICS.increment("decision_persist_failures")

    def _build_actions_from_decision(
        self,
        decision: ConversationDecision,
        shadow_mode: bool,
    ) -> list[dict[str, Any]]:
        if decision.action is None:
            return []

        status = ActionStatus.PENDING.value if shadow_mode else ActionStatus.EXECUTED.value

        action_entry: dict[str, Any] = {
            "action": decision.action,
            "status": status,
            "parameters": dict(decision.action_parameters),
        }

        if shadow_mode:
            action_entry["would_execute"] = True

        return [action_entry]

    def _record_metrics(self, decision: ConversationDecision) -> None:
        METRICS.increment("conversation_messages_processed")
        if decision.loop_detected:
            METRICS.increment("conversation_loops_detected")
        if decision.requires_human:
            METRICS.increment("conversation_human_handovers")
        if decision.selected_intent:
            METRICS.increment("conversation_intents_identified")

    def _audit(self, decision: ConversationDecision, conversation: Conversation) -> None:
        audit_event = f"conversation.{conversation.state.value.lower()}" if conversation.state else "conversation.unknown"
        if decision.loop_detected:
            audit_event = "conversation.loop_detected"
        if decision.requires_human:
            audit_event = "conversation.handover_requested"

        self._audit_logger.log(
            event=audit_event,
            details={
                "decision_id": decision.decision_id,
                "conversation_id": conversation.conversation_id,
                "user_id": conversation.user_id,
                "channel": conversation.channel,
                "action": decision.action,
                "state_before": decision.state_before.value if decision.state_before else None,
                "state_after": decision.state_after.value if decision.state_after else None,
                "loop_detected": decision.loop_detected,
                "requires_human": decision.requires_human,
                "selected_intent": decision.selected_intent,
            },
        )

    def _log_shadow_decision(self, decision: ConversationDecision) -> None:
        self._audit_logger.log(
            event="conversation.shadow_decision",
            details={
                "decision_id": decision.decision_id,
                "action": decision.action,
                "state_before": decision.state_before.value if decision.state_before else None,
                "state_after": decision.state_after.value if decision.state_after else None,
                "loop_detected": decision.loop_detected,
                "selected_intent": decision.selected_intent,
            },
        )

    def _maintenance_response(self, shadow_mode: bool) -> dict[str, Any]:
        return {
            "decision": ConversationDecision(
                decision_id=str(uuid4()),
                created_at=datetime.now(timezone.utc).isoformat(),
            ),
            "response": MAINTENANCE_RESPONSE,
            "state": "maintenance",
            "actions": [],
            "errors": ["service_in_maintenance_mode"],
            "shadow": shadow_mode,
        }

    def _error_response(
        self,
        message: str,
        errors: list[str],
        shadow_mode: bool,
        code: str = "internal_error",
    ) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        decision = ConversationDecision(
            decision_id=str(uuid4()),
            created_at=now,
        )
        self._audit_logger.log(
            event="conversation.error",
            details={"error": message, "code": code},
        )
        return {
            "decision": decision,
            "response": "Désolé, une erreur technique est survenue. Veuillez réessayer ou contacter un conseiller LAWIM.",
            "state": "error",
            "actions": [],
            "errors": errors,
            "shadow": shadow_mode,
        }

    def _row_to_conversation(self, row: dict[str, Any]) -> Conversation:
        state_value = row.get("state", "NEW")
        try:
            state = ConversationState(state_value)
        except ValueError:
            state = ConversationState.NEW

        return Conversation(
            conversation_id=row.get("id") or row.get("conversation_id"),
            user_id=row.get("user_id"),
            channel_identity_id=row.get("channel_identity_id"),
            channel=row.get("channel", ""),
            state=state,
            project_id=row.get("project_id"),
            dossier_id=row.get("dossier_id"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )
