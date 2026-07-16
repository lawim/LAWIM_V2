from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class MemoryEntry:
    key: str
    value: str
    category: str
    priority: int
    ttl_hours: int
    created_at: str
    expires_at: str


@dataclass(frozen=True, slots=True)
class MemoryBundle:
    short_term: tuple[MemoryEntry, ...] = ()
    long_term: tuple[MemoryEntry, ...] = ()
    persistent: tuple[MemoryEntry, ...] = ()
    agent_memory: tuple[MemoryEntry, ...] = ()
    conversation_memory: tuple[MemoryEntry, ...] = ()
    crm_memory: tuple[MemoryEntry, ...] = ()
    property_memory: tuple[MemoryEntry, ...] = ()
    document_memory: tuple[MemoryEntry, ...] = ()
    learning_memory: tuple[MemoryEntry, ...] = ()

    def to_prompt(self) -> str:
        parts: list[str] = []
        if self.short_term:
            items = "\n".join(f"- {e.key}: {e.value}" for e in self.short_term[:10])
            parts.append(f"[Mémoire court terme]\n{items}")
        if self.long_term:
            items = "\n".join(f"- {e.key}: {e.value}" for e in self.long_term[:10])
            parts.append(f"[Mémoire long terme]\n{items}")
        if self.persistent:
            items = "\n".join(f"- {e.key}: {e.value}" for e in self.persistent[:5])
            parts.append(f"[Mémoire persistante]\n{items}")
        if self.crm_memory:
            items = "\n".join(f"- {e.key}: {e.value}" for e in self.crm_memory[:5])
            parts.append(f"[CRM]\n{items}")
        if self.property_memory:
            items = "\n".join(f"- {e.key}: {e.value}" for e in self.property_memory[:5])
            parts.append(f"[Biens]\n{items}")
        return "\n\n".join(parts)


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


class MemoryOptimizer:
    SHORT_TERM_TTL = 24
    LONG_TERM_TTL = 720
    PERSISTENT_TTL = 0

    def __init__(self, repository, config):
        self.repository = repository
        self.config = config

    def load_for_conversation(
        self,
        *,
        conversation_key: str,
        user_id: int | None = None,
        organization_id: int | None = None,
        agent_code: str | None = None,
    ) -> MemoryBundle:
        short_term = self._load_short_term(conversation_key)
        long_term = self._load_long_term(user_id)
        persistent = self._load_persistent(user_id)
        agent_mem = self._load_agent_memory(agent_code)
        conv_mem = self._load_conversation_memory(conversation_key)
        crm_mem = self._load_crm(user_id, organization_id)
        prop_mem = self._load_properties(organization_id)
        doc_mem = self._load_documents(conversation_key)
        learn_mem = self._load_learning(user_id)
        return MemoryBundle(
            short_term=short_term,
            long_term=long_term,
            persistent=persistent,
            agent_memory=agent_mem,
            conversation_memory=conv_mem,
            crm_memory=crm_mem,
            property_memory=prop_mem,
            document_memory=doc_mem,
            learning_memory=learn_mem,
        )

    def store_short_term(self, *, conversation_key: str, key: str, value: str, priority: int = 0) -> None:
        now = _utcnow()
        self.repository.create_ai_memory(
            memory_key=f"st-{conversation_key}-{key}",
            category="short_term",
            value=value,
            priority=priority,
            ttl_hours=self.SHORT_TERM_TTL,
            created_at=now,
            expires_at=self._expiry(self.SHORT_TERM_TTL),
            conversation_key=conversation_key,
        )

    def store_long_term(self, *, user_id: int, key: str, value: str, priority: int = 0) -> None:
        now = _utcnow()
        self.repository.create_ai_memory(
            memory_key=f"lt-u{user_id}-{key}",
            category="long_term",
            value=value,
            priority=priority,
            ttl_hours=self.LONG_TERM_TTL,
            created_at=now,
            expires_at=self._expiry(self.LONG_TERM_TTL),
            user_id=user_id,
        )

    def store_persistent(self, *, user_id: int, key: str, value: str) -> None:
        now = _utcnow()
        self.repository.create_ai_memory(
            memory_key=f"perm-u{user_id}-{key}",
            category="persistent",
            value=value,
            priority=100,
            ttl_hours=0,
            created_at=now,
            expires_at=None,
            user_id=user_id,
        )

    def _load_short_term(self, conversation_key: str) -> tuple[MemoryEntry, ...]:
        try:
            rows = self.repository.list_ai_memory(conversation_key=conversation_key, category="short_term")
            return self._rows_to_entries(rows)
        except Exception:
            return ()

    def _load_long_term(self, user_id: int | None) -> tuple[MemoryEntry, ...]:
        if user_id is None:
            return ()
        try:
            rows = self.repository.list_ai_memory(user_id=user_id, category="long_term")
            return self._rows_to_entries(rows)
        except Exception:
            return ()

    def _load_persistent(self, user_id: int | None) -> tuple[MemoryEntry, ...]:
        if user_id is None:
            return ()
        try:
            rows = self.repository.list_ai_memory(user_id=user_id, category="persistent")
            return self._rows_to_entries(rows)
        except Exception:
            return ()

    def _load_agent_memory(self, agent_code: str | None) -> tuple[MemoryEntry, ...]:
        if not agent_code:
            return ()
        try:
            rows = self.repository.list_ai_memory(category="agent", agent_code=agent_code)
            return self._rows_to_entries(rows)
        except Exception:
            return ()

    def _load_conversation_memory(self, conversation_key: str) -> tuple[MemoryEntry, ...]:
        try:
            messages = self.repository.list_conversation_messages(conversation_key)
            summaries = []
            for msg in messages[-20:]:
                role = msg.get("role", "user")
                body = msg.get("body", "") or msg.get("content", "")
                if len(body) > 200:
                    body = body[:200] + "..."
                summaries.append(MemoryEntry(
                    key=f"msg_{msg.get('id', '')}",
                    value=f"{role}: {body}",
                    category="conversation",
                    priority=1,
                    ttl_hours=self.SHORT_TERM_TTL,
                    created_at=str(msg.get("created_at", "")),
                    expires_at="",
                ))
            return tuple(summaries)
        except Exception:
            return ()

    def _load_crm(self, user_id: int | None, organization_id: int | None) -> tuple[MemoryEntry, ...]:
        entries: list[MemoryEntry] = []
        if user_id:
            try:
                user = self.repository.get_user(user_id=user_id)
                if user:
                    entries.append(MemoryEntry(
                        key="user_role", value=str(user.get("role", "")), category="crm",
                        priority=10, ttl_hours=self.PERSISTENT_TTL if self.PERSISTENT_TTL == 0 else self.LONG_TERM_TTL,
                        created_at=_utcnow(), expires_at="",
                    ))
                    entries.append(MemoryEntry(
                        key="user_org", value=str(user.get("organization_id", "")), category="crm",
                        priority=5, ttl_hours=self.LONG_TERM_TTL,
                        created_at=_utcnow(), expires_at=self._expiry(self.LONG_TERM_TTL),
                    ))
            except Exception:
                pass
        return tuple(entries)

    def _load_properties(self, organization_id: int | None) -> tuple[MemoryEntry, ...]:
        if organization_id is None:
            return ()
        try:
            properties = self.repository.list_properties(organization_id=organization_id)
            return tuple(
                MemoryEntry(
                    key=f"prop_{p.get('id', '')}",
                    value=f"{p.get('title', '')} — {p.get('city', '')} — {p.get('status', '')}",
                    category="property", priority=3, ttl_hours=self.LONG_TERM_TTL,
                    created_at=_utcnow(), expires_at=self._expiry(self.LONG_TERM_TTL),
                )
                for p in properties[:10]
            )
        except Exception:
            return ()

    def _load_documents(self, conversation_key: str) -> tuple[MemoryEntry, ...]:
        return ()

    def _load_learning(self, user_id: int | None) -> tuple[MemoryEntry, ...]:
        return ()

    def _rows_to_entries(self, rows: list[dict[str, Any]]) -> tuple[MemoryEntry, ...]:
        return tuple(
            MemoryEntry(
                key=str(r.get("memory_key", "")),
                value=str(r.get("value", "")),
                category=str(r.get("category", "")),
                priority=int(r.get("priority", 0)),
                ttl_hours=int(r.get("ttl_hours", 0)),
                created_at=str(r.get("created_at", "")),
                expires_at=str(r.get("expires_at", "")),
            )
            for r in rows
        )

    @staticmethod
    def _expiry(ttl_hours: int) -> str | None:
        if ttl_hours <= 0:
            return None
        from datetime import timedelta
        return (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).replace(microsecond=0).isoformat()
