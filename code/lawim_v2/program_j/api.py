from __future__ import annotations

from typing import Any

from .config import ProgramJConfig
from .services import ActorResolutionService, ConversationResolutionService, ParticipantDisplayService
from .visual_role import visual_role_registry

config = ProgramJConfig()
actor_resolver = ActorResolutionService()
conv_resolver = ConversationResolutionService()
display_service = ParticipantDisplayService()


def handle_j1_actor_get(path: str, query: dict[str, list[str]],
                         actor: dict[str, object]) -> dict[str, Any] | None:
    if not config.actor_registry_enabled:
        return {"status": "disabled", "message": "actor_registry_enabled=false"}
    if path == "actors/roles":
        return {"roles": visual_role_registry.to_dict_list(), "count": visual_role_registry.count()}
    if path.startswith("actors/roles/"):
        code = path.split("/")[-1].upper()
        for role in visual_role_registry.list_all():
            if role.code == code:
                return {"role": role.to_dict()}
        return {"error": "role_not_found"}, 404
    return None


def handle_j1_actor_post(path: str, body: dict[str, Any],
                          actor: dict[str, object]) -> dict[str, Any] | None:
    if not config.actor_registry_enabled:
        return {"status": "disabled", "message": "actor_registry_enabled=false"}
    return None


def handle_j2_conversation_get(path: str, query: dict[str, list[str]],
                                actor: dict[str, object]) -> dict[str, Any] | None:
    if not config.unified_conversation_enabled:
        return {"status": "disabled", "message": "unified_conversation_enabled=false"}
    return None


def handle_j5_exchange_get(path: str, query: dict[str, list[str]],
                            actor: dict[str, object]) -> dict[str, Any] | None:
    if not config.exchange_taxonomy_enabled:
        return {"status": "disabled", "message": "exchange_taxonomy_enabled=false"}
    if path == "exchange/directions":
        from .exchange_taxonomy import Direction
        return {"directions": [d.value for d in Direction]}
    if path == "exchange/content-types":
        from .exchange_taxonomy import ContentType
        return {"content_types": [c.value for c in ContentType]}
    if path == "exchange/types":
        from .exchange_taxonomy import ExchangeType
        return {"exchange_types": [e.value for e in ExchangeType]}
    if path == "exchange/results":
        from .exchange_taxonomy import ExchangeResult
        return {"exchange_results": [r.value for r in ExchangeResult]}
    return None
