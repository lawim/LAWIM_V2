from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from .agent_models import (
    AgentAction,
    AgentHandover,
    AgentInvocation,
    AgentMemory,
    AgentResponse,
    AgentRuntimeContext,
    HandoverStatus,
    InvocationStatus,
    MemoryType,
)

_now = lambda: datetime.now(timezone.utc).isoformat()


class AgentContextBuilder:
    def build(self, actor_id: str = "", conversation_id: str = "",
               channel: str = "", language: str = "fr",
               feature_flags: dict[str, bool] | None = None) -> AgentRuntimeContext:
        return AgentRuntimeContext(
            actor_id=actor_id,
            conversation_id=conversation_id,
            channel=channel,
            language=language,
            feature_flags=feature_flags or {},
        )


class AgentInvocationService:
    def __init__(self) -> None:
        self._invocations: list[AgentInvocation] = []

    def create(self, inv: AgentInvocation) -> AgentInvocation:
        inv.invocation_id = str(uuid.uuid4())
        inv.status = InvocationStatus.CREATED
        inv.started_at = _now()
        self._invocations.append(inv)
        return inv

    def get(self, iid: str) -> AgentInvocation | None:
        for i in self._invocations:
            if i.invocation_id == iid:
                return i
        return None

    def list(self, conversation_id: str | None = None) -> list[AgentInvocation]:
        if conversation_id is None:
            return list(self._invocations)
        return [i for i in self._invocations if i.conversation_id == conversation_id]

    def complete(self, iid: str, result: str = "") -> AgentInvocation | None:
        inv = self.get(iid)
        if inv:
            inv.status = InvocationStatus.COMPLETED
            inv.completed_at = _now()
            inv.result = result
        return inv

    def fail(self, iid: str, error: str = "") -> AgentInvocation | None:
        inv = self.get(iid)
        if inv:
            inv.status = InvocationStatus.FAILED
            inv.completed_at = _now()
            inv.error = error
        return inv


class AgentResponseBuilder:
    def build(self, inv: AgentInvocation, content: str,
               confidence: float = 1.0, sources: list[str] | None = None) -> AgentResponse:
        return AgentResponse(
            response_id=str(uuid.uuid4()),
            invocation_id=inv.invocation_id,
            agent_id=inv.agent_id,
            agent_code=inv.agent_code,
            content=content,
            confidence=confidence,
            sources=sources or [],
            created_at=_now(),
        )


class AgentActionService:
    def __init__(self) -> None:
        self._actions: list[AgentAction] = []

    def create(self, action: AgentAction) -> AgentAction:
        action.action_id = str(uuid.uuid4())
        self._actions.append(action)
        return action

    def list(self, invocation_id: str) -> list[AgentAction]:
        return [a for a in self._actions if a.invocation_id == invocation_id]


class AgentMemoryService:
    def __init__(self) -> None:
        self._memories: list[AgentMemory] = []

    def store(self, memory: AgentMemory) -> AgentMemory:
        memory.memory_id = str(uuid.uuid4())
        memory.created_at = _now()
        self._memories.append(memory)
        return memory

    def get_by_conversation(self, conv_id: str) -> list[AgentMemory]:
        return [m for m in self._memories if m.conversation_id == conv_id]

    def get_by_key(self, key: str) -> AgentMemory | None:
        for m in self._memories:
            if m.key == key:
                return m
        return None


class AgentAuditService:
    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def record(self, entry: dict[str, Any]) -> None:
        entry["audit_id"] = str(uuid.uuid4())
        entry["timestamp"] = _now()
        self._entries.append(entry)

    def query(self, agent_id: str | None = None) -> list[dict[str, Any]]:
        if agent_id is None:
            return list(self._entries)
        return [e for e in self._entries if e.get("agent_id") == agent_id]
