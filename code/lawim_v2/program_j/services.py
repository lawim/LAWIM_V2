from __future__ import annotations

from typing import Any

from .actor import Actor, ActorStatus, ActorType
from .channel_endpoint import ChannelEndpoint, ChannelEndpointStatus, EndpointVerification
from .conversation import (
    ChannelSession,
    ConversationParticipant,
    ConversationStatus,
    UnifiedConversation,
)
from .exchange_taxonomy import ContentType, Direction, ExchangeResult, ExchangeType
from .message import MessageDelivery, UnifiedMessage
from .visual_role import visual_role_registry


class ActorResolutionService:
    def resolve_by_user(self, user_id: int, repository: Any) -> Actor | None:
        user = repository.get_user(user_id) if hasattr(repository, "get_user") else None
        if user is None:
            return None
        role = (user.get("role") or "").lower()
        actor_type = ActorType.from_role_label(role)
        return Actor(
            actor_id=f"user_{user_id}",
            actor_type=actor_type,
            display_name=user.get("full_name", user.get("email", f"User#{user_id}")),
            user_id=user_id,
            current_role=role,
            trust_level=user.get("trust_level", 0),
        )

    def resolve_by_endpoint(self, endpoint: ChannelEndpoint, repository: Any) -> Actor | None:
        if endpoint.user_id is not None:
            return self.resolve_by_user(endpoint.user_id, repository)
        if not endpoint.verification.verified:
            return None
        return None

    def resolve_by_provider_user(self, provider: str, channel: str,
                                  provider_user_id: str, repository: Any) -> Actor | None:
        contacts = getattr(repository, "list_crm_contacts", None)
        if contacts is not None:
            all_contacts = contacts(limit=1000)
            phone = provider_user_id.replace("+", "").replace(" ", "").replace("-", "")
            for c in all_contacts:
                cphone = (c.get("phone") or "").replace("+", "").replace(" ", "").replace("-", "")
                if cphone and cphone[-9:] == phone[-9:]:
                    cid = c.get("id")
                    return Actor(
                        actor_id=f"contact_{cid}",
                        actor_type=ActorType.USER,
                        display_name=c.get("full_name", f"Contact#{cid}"),
                        user_id=c.get("user_id"),
                        current_role=c.get("contact_type", "user"),
                        trust_level=1,
                    )
        return None

    def create_minimal(self, actor_type: ActorType = ActorType.USER,
                        display_name: str = "Utilisateur") -> Actor:
        import uuid
        return Actor(
            actor_id=f"actor_{uuid.uuid4().hex[:12]}",
            actor_type=actor_type,
            display_name=display_name,
            status=ActorStatus.ACTIVE,
        )


class ConversationResolutionService:
    def resolve(self, actor_id: str, channel: str, repository: Any) -> UnifiedConversation | None:
        sessions = getattr(repository, "conversation_list_sessions", None)
        if sessions is not None:
            rows = repository.conversation_list_sessions(actor_id=actor_id, channel=channel,
                                                          status="ACTIVE", limit=5)
            for row in rows:
                conv = self._row_to_conversation(row)
                if conv:
                    return conv
        return None

    def create(self, actor_id: str, channel: str, subject: str = "") -> UnifiedConversation:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        conv_id = f"conv_{uuid.uuid4().hex[:16]}"
        conv = UnifiedConversation(
            conversation_id=conv_id,
            subject=subject,
            initial_channel=channel,
            current_channel=channel,
            primary_actor_id=actor_id,
            status=ConversationStatus.ACTIVE,
            created_at=now,
            last_activity_at=now,
        )
        conv.add_participant(actor_id, role="primary", is_primary=True)
        return conv

    def resolve_or_create(self, actor_id: str, channel: str, repository: Any,
                           subject: str = "") -> UnifiedConversation:
        existing = self.resolve(actor_id, channel, repository)
        if existing is not None:
            return existing
        return self.create(actor_id, channel, subject)

    def _row_to_conversation(self, row: dict[str, Any]) -> UnifiedConversation | None:
        cid = row.get("conversation_id") or row.get("id")
        if cid is None:
            return None
        return UnifiedConversation(
            conversation_id=str(cid),
            subject=row.get("subject", row.get("title", "")),
            dossier_id=row.get("dossier_id"),
            project_id=row.get("project_id"),
            initial_channel=row.get("channel", row.get("initial_channel", "")),
            current_channel=row.get("channel", ""),
            primary_actor_id=str(row.get("user_id", "")) if row.get("user_id") else "",
            status=ConversationStatus.ACTIVE if row.get("status", "active") != "closed" else ConversationStatus.CLOSED,
            created_at=row.get("created_at", ""),
            last_activity_at=row.get("updated_at", row.get("last_activity_at", "")),
        )


class MessageIngestionService:
    def ingest(self, msg: UnifiedMessage, repository: Any) -> UnifiedMessage:
        method = getattr(repository, "message_ingest", None)
        if method is not None:
            row = repository.message_ingest(msg.to_dict())
            if row and row.get("message_id"):
                msg.message_id = str(row["message_id"])
        return msg

    def normalize_webhook(self, provider: str, channel: str,
                           payload: dict[str, Any],
                           conversation_id: str = "") -> UnifiedMessage:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return UnifiedMessage(
            message_id=f"msg_{uuid.uuid4().hex[:16]}",
            conversation_id=conversation_id,
            channel=channel,
            provider=provider,
            content=payload.get("content", payload.get("body", payload.get("text", ""))),
            direction=Direction.INBOUND,
            content_type=ContentType.TEXT,
            exchange_type=ExchangeType.INFORMATION_REQUEST,
            exchange_result=ExchangeResult.RECEIVED,
            external_message_id=payload.get("external_message_id", ""),
            sender_actor_id="",
            created_at=payload.get("timestamp", now),
            received_at=now,
            attachments=payload.get("attachments", []),
            metadata=payload.get("raw_metadata", {}),
        )

    def build_outbound(self, conversation_id: str, content: str,
                        sender_actor_id: str, channel: str,
                        exchange_type: ExchangeType = ExchangeType.INFORMATION_REQUEST) -> UnifiedMessage:
        import uuid
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).isoformat()
        return UnifiedMessage(
            message_id=f"msg_{uuid.uuid4().hex[:16]}",
            conversation_id=conversation_id,
            sender_actor_id=sender_actor_id,
            channel=channel,
            direction=Direction.OUTBOUND,
            content=content,
            content_type=ContentType.TEXT,
            exchange_type=exchange_type,
            exchange_result=ExchangeResult.ANSWERED,
            created_at=now,
            sent_at=now,
        )


class ParticipantDisplayService:
    def format(self, actor: Actor) -> str:
        role = visual_role_registry.get(actor.actor_type)
        return role.format_display(actor.display_name)

    def format_safe(self, actor: Actor) -> str:
        role = visual_role_registry.get(actor.actor_type)
        masked_name = self._mask_actor_name(actor, role)
        return role.format_display(masked_name)

    def format_ai(self) -> str:
        return "\U0001f916 LAWIM AI"

    def format_staff(self, name: str) -> str:
        return f"\U0001f9d1\U0000200d\U0001f4bc LAWIM ({name})"

    def _mask_actor_name(self, actor: Actor, role: Any) -> str:
        name = actor.display_name
        if role.mask_phone:
            import re
            name = re.sub(r"\+\d[\d\s\-\(\)]{6,}\d", lambda m: m.group(0)[:4] + "\u2022" * 4 + m.group(0)[-2:], name)
            name = re.sub(r"\b\d{2,}[\s\-]?\d{2,}[\s\-]?\d{2,}[\s\-]?\d{2,}\b",
                          lambda m: m.group(0)[:2] + "\u2022" * 4 + m.group(0)[-2:], name)
        if not name.strip():
            return "Utilisateur"
        if actor.actor_type == ActorType.USER and len(name) > 12:
            name = name[:10] + "\u2026"
        return name
