from __future__ import annotations

import os

from ..observability import METRICS
from ..project_service import ProjectPermissionDenied, ProjectService
from . import dto as adto
from .providers import resolve_llm_provider


class AssistantService:
    def __init__(self, repository, project_service: ProjectService) -> None:
        self.repository = repository
        self.projects = project_service
        self.llm = resolve_llm_provider(enabled=os.environ.get("LAWIM_LLM_ENABLED", "").lower() in {"1", "true", "yes"})

    def _require_access(self, actor: dict[str, object], project_id: int) -> None:
        self.projects._require_access(actor, project_id)

    def _user_id(self, actor: dict[str, object]) -> int:
        user_id = actor.get("id")
        if user_id is None:
            raise ProjectPermissionDenied("Authentication required")
        return int(user_id)

    def list_sessions(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("assistant_sessions")
        rows = self.repository.list_assistant_sessions(project_id, self._user_id(actor))
        return {"sessions": [adto.session_dto(row) for row in rows]}

    def create_session(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        agent_key: str = "project_advisor",
    ) -> dict[str, object]:
        self._require_access(actor, project_id)
        row = self.repository.create_assistant_session(
            project_id=project_id,
            user_id=self._user_id(actor),
            agent_key=agent_key,
        )
        METRICS.increment("assistant_sessions")
        return {"session": adto.session_dto(row)}

    def get_session(self, *, actor: dict[str, object], project_id: int, session_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        return {"session": adto.session_dto(self.repository.get_assistant_session(project_id, session_id))}

    def list_messages(self, *, actor: dict[str, object], project_id: int, session_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        rows = self.repository.list_assistant_messages(session_id, project_id)
        return {"messages": [adto.message_dto(row) for row in rows]}

    def list_agents(self, *, actor: dict[str, object]) -> dict[str, object]:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")
        METRICS.increment("assistant_agents")
        return {"agents": [adto.agent_dto(row) for row in self.repository.list_assistant_agents()]}

    def list_prompts(self, *, actor: dict[str, object]) -> dict[str, object]:
        if actor is None:
            raise ProjectPermissionDenied("Authentication required")
        METRICS.increment("assistant_prompts")
        return {"prompts": [adto.prompt_dto(row) for row in self.repository.list_assistant_prompts()]}

    def get_context(self, *, actor: dict[str, object], project_id: int, session_id: int | None = None) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("assistant_context")
        return self.repository.get_assistant_context(project_id, session_id)

    def refresh_rag(self, *, actor: dict[str, object], project_id: int) -> dict[str, object]:
        self._require_access(actor, project_id)
        payload = self.repository.refresh_project_rag_index(project_id)
        METRICS.increment("assistant_rag")
        return {"rag_index": payload}

    def retrieve_rag(self, *, actor: dict[str, object], project_id: int, query: str) -> dict[str, object]:
        self._require_access(actor, project_id)
        METRICS.increment("assistant_rag")
        return {"chunks": self.repository.retrieve_assistant_rag(project_id, query)}

    def chat(
        self,
        *,
        actor: dict[str, object],
        project_id: int,
        message: str,
        session_id: int | None = None,
        agent_key: str | None = None,
    ) -> dict[str, object]:
        self._require_access(actor, project_id)
        payload = self.repository.chat_assistant(
            project_id=project_id,
            user_id=self._user_id(actor),
            message=message,
            session_id=session_id,
            agent_key=agent_key,
            llm_provider=self.llm,
        )
        METRICS.increment("assistant_chat")
        return {"chat": adto.chat_response_dto(payload)}
