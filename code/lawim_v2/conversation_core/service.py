from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
from typing import Any
import uuid

from ..ai import AIMessage, AIOrchestrator
from ..ai.safety import redact_sensitive_text
from ..brain.intent_engine import IntentEngine
from ..brain.memory import BrainMemory
from ..brain.progression import ProgressionEngine
from ..contact import COMPANY_NAME
from ..observability import METRICS
from ..persona import assistant_brief_warning
from ..project_service import ProjectService
from .models import ConversationTurnPlan, ConversationTurnResult
from .normalizer import normalize_language, normalize_text, normalize_whatsapp_number, resolve_conversation_key, sanitize_metadata
from .response import compose_external_service_refusal, compose_fallback, compose_welcome, is_blocked_external_service_request, validate_final_response


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(slots=True)
class ConversationCoreService:
    repository: Any
    projects: ProjectService
    policy: Any
    config: Any
    ai_orchestrator: AIOrchestrator | None = None
    intent_engine: IntentEngine = field(init=False, repr=False)
    memory: BrainMemory = field(init=False, repr=False)
    progression_engine: ProgressionEngine = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self.intent_engine = IntentEngine()
        self.memory = BrainMemory(self.repository)
        self.progression_engine = ProgressionEngine()
        self.ai_orchestrator = self.ai_orchestrator or AIOrchestrator(self.repository, self.config)

    def process_message(
        self,
        *,
        channel: str,
        message: str,
        normalized: dict[str, Any] | None = None,
        message_row: dict[str, Any] | None = None,
        project_id: int | None = None,
        actor: dict[str, object] | None = None,
        session_id: int | None = None,
        language: str | None = None,
        external_chat_id: str | None = None,
        external_user_id: str | None = None,
        message_id: str | None = None,
        sender_name: str | None = None,
    ) -> ConversationTurnResult:
        normalized_payload = sanitize_metadata(normalized)
        text = normalize_text(message or (message_row or {}).get("body") or normalized_payload.get("message_body"))
        normalized_language = normalize_language(language or normalized_payload.get("language") or self.config.fallback_default_language)
        analysis = self.intent_engine.analyze(text)

        project = self._load_project(project_id, actor)
        contact, thread, conversation_key = self._resolve_identity_and_thread(
            channel=channel,
            text=text,
            normalized=normalized_payload,
            message_row=message_row or {},
            project=project,
            project_id=project_id,
            actor=actor,
            external_chat_id=external_chat_id,
            external_user_id=external_user_id,
            message_id=message_id,
            sender_name=sender_name,
        )
        context_messages = self._load_context_messages(
            thread_id=int(thread["id"]) if thread and thread.get("id") is not None else None,
            exclude_message_id=int(message_row["id"]) if message_row and message_row.get("id") is not None else None,
        )
        memory_summary = self.memory.get_summary(project_id) if project_id else {}
        memory_items = self.memory.get_active(project_id) if project_id else []
        progression = self.progression_engine.compute(
            project_id=project_id or 0,
            intent=analysis["primary_intent"],
            entities=analysis.get("entities", {}),
            memory_items=memory_items,
            project=project,
        )
        direct_reply, reply_kind = self._compose_direct_reply(
            channel=channel,
            text=text,
            language=normalized_language,
            known_user=bool(contact),
            contact=contact,
            project=project,
            analysis=analysis,
            progression=progression,
        )
        route_metadata = {
            "channel": channel,
            "company_name": COMPANY_NAME,
            "project_id": project_id,
            "thread_id": int(thread["id"]) if thread and thread.get("id") is not None else None,
            "contact_id": int(contact["id"]) if contact and contact.get("id") is not None else None,
            "analysis": analysis,
            "progression": progression,
            "memory_summary": memory_summary,
            "direct_reply": bool(direct_reply),
            "reply_kind": reply_kind,
            "commercial_maturity": progression.get("commercial_maturity"),
            "qualification_score": progression.get("qualification_score"),
            "minimum_search_ready": progression.get("minimum_search_ready"),
            "next_action": progression.get("next_action"),
            "transaction_stage": progression.get("transaction_stage"),
            "required_fields": progression.get("required_fields"),
            "optional_fields": progression.get("optional_fields"),
            "warning": assistant_brief_warning(normalized_language),
        }
        request = self.ai_orchestrator.build_request(
            channel=channel,
            text=text,
            conversation_key=conversation_key,
            external_chat_id=str(external_chat_id or normalized_payload.get("chat_id") or normalized_payload.get("chat_id_raw") or ""),
            external_user_id=str(external_user_id or normalized_payload.get("user_id") or ""),
            message_id=str(message_id or (message_row or {}).get("message_key") or (message_row or {}).get("id") or ""),
            thread_id=int(thread["id"]) if thread and thread.get("id") is not None else None,
            contact_id=int(contact["id"]) if contact and contact.get("id") is not None else None,
            organization_id=int(contact["organization_id"]) if contact and contact.get("organization_id") is not None else None,
            language=normalized_language,
            context_messages=context_messages,
            metadata={
                **route_metadata,
                "sender_name": sender_name or normalized_payload.get("sender_name") or normalized_payload.get("full_name") or "",
            },
        )
        outcome = self.ai_orchestrator.generate(request)
        selected_text = direct_reply or normalize_text(outcome.response.content)
        blocked_external_service = is_blocked_external_service_request(selected_text) or is_blocked_external_service_request(text)
        if not selected_text:
            selected_text = compose_fallback(normalized_language)
            reply_kind = "fallback"
        if blocked_external_service:
            selected_text = compose_external_service_refusal(normalized_language)
            reply_kind = "refusal"
        quality = validate_final_response(selected_text)
        if not quality.valid:
            selected_text = compose_fallback(normalized_language)
            quality = validate_final_response(selected_text)
            reply_kind = "fallback"
        if project_id is not None:
            self._persist_project_turn(
                project_id=project_id,
                session_id=session_id,
                analysis=analysis,
                progression=progression,
                message_row=message_row or {},
                response_text=selected_text,
                thread_id=int(thread["id"]) if thread and thread.get("id") is not None else None,
            )
        self._persist_conversation_metadata(
            thread_id=int(thread["id"]) if thread and thread.get("id") is not None else None,
            message_row=message_row or {},
            conversation_key=conversation_key,
            analysis=analysis,
            progression=progression,
            response_text=selected_text,
            request_id=request.request_id,
            response_quality=quality.to_dict(),
            reply_kind=reply_kind,
            outcome=outcome,
        )
        return ConversationTurnResult(
            plan=ConversationTurnPlan(
                channel=channel,
                text=text,
                language=normalized_language,
                normalized=normalized_payload,
                message_row=message_row or {},
                conversation_key=conversation_key,
                external_chat_id=str(external_chat_id or normalized_payload.get("chat_id") or normalized_payload.get("chat_id_raw") or ""),
                external_user_id=str(external_user_id or normalized_payload.get("user_id") or ""),
                message_id=str(message_id or (message_row or {}).get("message_key") or (message_row or {}).get("id") or ""),
                project_id=project_id,
                thread_id=int(thread["id"]) if thread and thread.get("id") is not None else None,
                contact_id=int(contact["id"]) if contact and contact.get("id") is not None else None,
                organization_id=int(contact["organization_id"]) if contact and contact.get("organization_id") is not None else None,
                contact=contact,
                thread=thread,
                project=project,
                analysis=analysis,
                progression=progression,
                memory_summary=memory_summary,
                context_messages=context_messages,
                direct_reply=direct_reply,
                reply_kind=reply_kind,
                route_reason="lawim_first" if direct_reply else "ai",
                route_metadata=route_metadata,
                actor=actor,
            ),
            request=request,
            outcome=outcome,
            final_text=selected_text,
            response_quality=quality.to_dict(),
            response_kind=reply_kind,
            response_source="deterministic" if direct_reply else ("ai" if outcome.response.provider != "internal" or outcome.decision.selected_provider != "internal" else "fallback"),
            fallback_used=bool(outcome.decision.fallback_used or reply_kind == "fallback"),
            should_escalate=bool(
                getattr(self.config, "human_escalation_enabled", False)
                and (
                    reply_kind == "fallback"
                    or blocked_external_service
                    or not quality.valid
                )
            ),
            metadata={
                "conversation_key": conversation_key,
                "thread_id": int(thread["id"]) if thread and thread.get("id") is not None else None,
                "contact_id": int(contact["id"]) if contact and contact.get("id") is not None else None,
                "analysis": analysis,
                "progression": progression,
                "memory_summary": memory_summary,
                "reply_kind": reply_kind,
                "blocked_external_service": blocked_external_service,
                "selected_provider": outcome.decision.selected_provider,
                "provider": outcome.response.provider,
                "commercial_maturity": progression.get("commercial_maturity"),
                "qualification_score": progression.get("qualification_score"),
                "minimum_search_ready": progression.get("minimum_search_ready"),
                "next_action": progression.get("next_action"),
            },
        )

    def _compose_direct_reply(
        self,
        *,
        channel: str,
        text: str,
        language: str,
        known_user: bool,
        contact: dict[str, Any] | None,
        project: dict[str, Any] | None,
        analysis: dict[str, Any],
        progression: dict[str, Any],
    ) -> tuple[str | None, str]:
        lower = text.strip().lower()
        if lower in {"/start", "start", "bonjour", "salut", "hello", "hi"}:
            name = str(contact.get("full_name") or contact.get("name") or "") if contact else ""
            return compose_welcome(language, known_user=known_user, name=name or None), "greeting"
        if is_blocked_external_service_request(text):
            return compose_external_service_refusal(language), "refusal"
        next_question = str(progression.get("next_question") or "").strip()
        search_ready = bool(progression.get("minimum_search_ready") or progression.get("search_ready"))
        if next_question and not progression.get("complete") and not search_ready:
            return next_question, "qualification"
        if channel == "web" and not text.strip():
            return compose_welcome(language, known_user=known_user, name=(str(contact.get("full_name") or "") if contact else None)), "greeting"
        return None, "ai"

    def _resolve_identity_and_thread(
        self,
        *,
        channel: str,
        text: str,
        normalized: dict[str, Any],
        message_row: dict[str, Any],
        project: dict[str, Any] | None,
        project_id: int | None,
        actor: dict[str, object] | None,
        external_chat_id: str | None,
        external_user_id: str | None,
        message_id: str | None,
        sender_name: str | None,
    ) -> tuple[dict[str, Any] | None, dict[str, Any] | None, str]:
        contact = self._resolve_contact(
            channel=channel,
            normalized=normalized,
            text=text,
            sender_name=sender_name,
            external_chat_id=external_chat_id,
            external_user_id=external_user_id,
            actor=actor,
            project_id=project_id,
        )
        conversation_key = resolve_conversation_key(
            channel=channel,
            project_id=project_id,
            contact_id=int(contact["id"]) if contact and contact.get("id") is not None else None,
            external_chat_id=external_chat_id or normalized.get("chat_id") or normalized.get("chat_id_raw"),
            external_user_id=external_user_id or normalized.get("user_id"),
            message_id=message_id or message_row.get("message_key") or message_row.get("id"),
        )
        thread = self._resolve_thread(
            channel=channel,
            conversation_key=conversation_key,
            subject=self._build_subject(channel=channel, normalized=normalized, contact=contact, project=project),
            contact=contact,
            project_id=project_id,
            actor=actor,
        )
        return contact, thread, conversation_key

    def _resolve_contact(
        self,
        *,
        channel: str,
        normalized: dict[str, Any],
        text: str,
        sender_name: str | None,
        external_chat_id: str | None,
        external_user_id: str | None,
        actor: dict[str, object] | None,
        project_id: int | None,
    ) -> dict[str, Any] | None:
        try:
            if channel == "whatsapp":
                raw_chat_id = str(external_chat_id or normalized.get("chat_id") or normalized.get("sender") or "")
                phone = normalize_whatsapp_number(raw_chat_id)
                if not phone:
                    return None
                row = self.repository.one(
                    """
                    SELECT * FROM crm_contact_profiles
                    WHERE whatsapp = ? OR phone = ?
                    ORDER BY id ASC
                    LIMIT 1
                    """,
                    (phone, phone),
                )
                if row is not None:
                    return dict(row)
                full_name = normalize_text(sender_name or normalized.get("sender_name") or normalized.get("full_name") or phone) or phone
                return self.repository.create_crm_contact(
                    full_name=full_name,
                    phone=phone,
                    whatsapp=phone,
                    country="Cameroon",
                    metadata={
                        "channel": channel,
                        "external_chat_id": raw_chat_id,
                        "external_user_id": external_user_id or normalized.get("user_id"),
                    },
                )
            if channel == "telegram":
                username = normalize_text(normalized.get("username"))
                chat_id = normalize_text(external_chat_id or normalized.get("chat_id"))
                telegram_handle = f"@{username}" if username else f"telegram:{chat_id}"
                row = self.repository.one(
                    """
                    SELECT * FROM crm_contact_profiles
                    WHERE telegram = ?
                    ORDER BY id ASC
                    LIMIT 1
                    """,
                    (telegram_handle,),
                )
                if row is not None:
                    return dict(row)
                full_name = normalize_text(sender_name or normalized.get("full_name") or username or chat_id or "Telegram Contact")
                return self.repository.create_crm_contact(
                    full_name=full_name,
                    telegram=telegram_handle,
                    country="Cameroon",
                    metadata={
                        "channel": channel,
                        "external_chat_id": chat_id,
                        "external_user_id": external_user_id or normalized.get("user_id"),
                        "username": username,
                    },
                )
            if project_id is not None and actor is not None:
                user_id = actor.get("id")
                if user_id is not None:
                    row = self.repository.one(
                        """
                        SELECT * FROM crm_contact_profiles
                        WHERE user_id = ?
                        ORDER BY id ASC
                        LIMIT 1
                        """,
                        (int(user_id),),
                    )
                    if row is not None:
                        return dict(row)
            return None
        except Exception as exc:
            self.repository.create_communication_log(
                level="warning",
                message=f"ConversationCore contact resolution failed for {channel}",
                payload={"channel": channel, "error": exc.__class__.__name__},
            )
            return None

    def _resolve_thread(
        self,
        *,
        channel: str,
        conversation_key: str,
        subject: str,
        contact: dict[str, Any] | None,
        project_id: int | None,
        actor: dict[str, object] | None,
    ) -> dict[str, Any] | None:
        try:
            row = self.repository.one("SELECT * FROM communication_threads WHERE thread_key = ?", (conversation_key,))
            if row is not None:
                return dict(row)
            metadata = {
                "channel": channel,
                "contact_id": int(contact["id"]) if contact and contact.get("id") is not None else None,
                "project_id": project_id,
                "actor_user_id": actor.get("id") if actor else None,
            }
            thread = self.repository.create_communication_thread(
                subject=subject,
                thread_key=conversation_key,
                metadata=metadata,
            )
            return thread
        except Exception as exc:
            self.repository.create_communication_log(
                level="warning",
                message=f"ConversationCore thread resolution failed for {channel}",
                payload={"channel": channel, "conversation_key": conversation_key, "error": exc.__class__.__name__},
            )
            return None

    def _build_subject(
        self,
        *,
        channel: str,
        normalized: dict[str, Any],
        contact: dict[str, Any] | None,
        project: dict[str, Any] | None,
    ) -> str:
        if project is not None:
            return normalize_text(project.get("title")) or "LAWIM Project"
        if contact is not None:
            return normalize_text(contact.get("full_name")) or normalize_text(contact.get("whatsapp")) or normalize_text(contact.get("telegram")) or "LAWIM Conversation"
        if channel == "telegram":
            return normalize_text(normalized.get("full_name") or normalized.get("username") or normalized.get("chat_id") or "Telegram Conversation")
        if channel == "whatsapp":
            return normalize_text(normalized.get("sender_name") or normalized.get("chat_id") or normalized.get("sender") or "WhatsApp Conversation")
        return "LAWIM Conversation"

    def _load_context_messages(self, *, thread_id: int | None, exclude_message_id: int | None = None) -> tuple[AIMessage, ...]:
        if thread_id is None:
            return ()
        query = "SELECT direction, body, created_at FROM communication_messages WHERE thread_id = ?"
        params: list[object] = [thread_id]
        if exclude_message_id is not None:
            query += " AND id <> ?"
            params.append(exclude_message_id)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(getattr(self.config, "ai_max_context_messages", 20))
        rows = self.repository.all(query, tuple(params))
        ordered = list(reversed(rows))
        messages: list[AIMessage] = []
        for row in ordered:
            direction = str(row.get("direction") or "inbound")
            role = "assistant" if direction == "outbound" else "user"
            content = normalize_text(row.get("body"))
            if not content:
                continue
            messages.append(AIMessage(role=role, content=content))
        return tuple(messages)

    def _load_project(self, project_id: int | None, actor: dict[str, object] | None) -> dict[str, Any] | None:
        if project_id is None:
            return None
        try:
            if actor is not None:
                return self.projects.get_project(actor=actor, project_id=project_id)
        except Exception:
            pass
        row = self.repository.get_project(project_id)
        return dict(row) if isinstance(row, dict) else row

    def _persist_project_turn(
        self,
        *,
        project_id: int,
        session_id: int | None,
        analysis: dict[str, Any],
        progression: dict[str, Any],
        message_row: dict[str, Any],
        response_text: str,
        thread_id: int | None,
    ) -> None:
        try:
            intent_row = self.repository.create_brain_intent(
                project_id=project_id,
                session_id=session_id,
                source_message_id=int(message_row["id"]) if message_row.get("id") is not None else None,
                intent_type=str(analysis.get("primary_intent") or "other"),
                entities_json=analysis.get("entities", {}),
                language=str(analysis.get("language") or self.config.fallback_default_language or "fr"),
                confidence=int(analysis.get("primary_score") or 0),
                status="hypothesis",
                engine_version="2.0.0",
            )
            if intent_row:
                self.memory.add_item(
                    project_id=project_id,
                    kind="hypothesis",
                    key=f"turn-{uuid.uuid4().hex[:12]}",
                    label="turn",
                    value=response_text,
                    source_table="communication_messages",
                    source_id=int(message_row["id"]) if message_row.get("id") is not None else None,
                    confidence=60,
                    is_global=False,
                    metadata={
                        "intent": analysis.get("primary_intent"),
                        "progression": progression,
                        "thread_id": thread_id,
                    },
                )
            self.repository.upsert_brain_progression(
                project_id=project_id,
                intent_type=str(analysis.get("primary_intent") or "other"),
                current_step=int(progression.get("progress_pct") or 0),
                total_steps=int(progression.get("total_steps") or 0),
                asked_questions=[{"question": progression.get("next_question")}],
                answers=analysis.get("entities", {}),
                missing_fields=list(progression.get("missing_fields") or []),
                next_question=progression.get("next_question"),
                next_question_key=progression.get("next_key"),
                status="complete" if progression.get("complete") else "in_progress",
            )
        except Exception as exc:
            self.repository.create_communication_log(
                level="warning",
                message="ConversationCore project persistence failed",
                payload={
                    "project_id": project_id,
                    "message_id": int(message_row["id"]) if message_row.get("id") is not None else None,
                    "error": exc.__class__.__name__,
                },
            )

    def _persist_conversation_metadata(
        self,
        *,
        thread_id: int | None,
        message_row: dict[str, Any],
        conversation_key: str,
        analysis: dict[str, Any],
        progression: dict[str, Any],
        response_text: str,
        request_id: str,
        response_quality: dict[str, Any],
        reply_kind: str,
        outcome,
    ) -> None:
        message_updates = {
            "status": "processed",
            "metadata": {
                "conversation_key": conversation_key,
                "request_id": request_id,
                "analysis": analysis,
                "progression": progression,
                "response_quality": response_quality,
                "reply_kind": reply_kind,
                "response_text": redact_sensitive_text(response_text),
                "selected_provider": outcome.decision.selected_provider,
                "fallback_used": outcome.decision.fallback_used,
            },
        }
        if message_row.get("id") is not None:
            self.repository.update_communication_message(int(message_row["id"]), **message_updates)
        if thread_id is not None:
            self.repository.execute(
                """
                UPDATE communication_threads
                SET subject = COALESCE(NULLIF(subject, ''), ?),
                    metadata_json = ?,
                    updated_at = ?
                WHERE id = ?
                """,
                (
                    progression.get("next_question")
                    or normalize_text(message_row.get("subject"))
                    or "LAWIM Conversation",
                    json.dumps(
                        {
                            "conversation_key": conversation_key,
                            "analysis": analysis,
                            "progression": progression,
                            "response_quality": response_quality,
                            "reply_kind": reply_kind,
                            "last_response": redact_sensitive_text(response_text),
                            "selected_provider": outcome.decision.selected_provider,
                            "fallback_used": outcome.decision.fallback_used,
                        },
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                    _utcnow(),
                    thread_id,
                ),
            )
