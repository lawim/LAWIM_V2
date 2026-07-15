from __future__ import annotations

from typing import Any

from .agent_config import AgentConfig
from .agent_registry import agent_registry, capability_registry

_config = AgentConfig()


def handle_agent_get(path: str, query: dict[str, list[str]],
                     actor: dict[str, object]) -> dict[str, Any] | None:
    if not _config.agent_platform_enabled:
        return {"status": "disabled", "message": "agent_platform_enabled=false"}

    if path == "agents":
        return {"agents": [a.to_dict() for a in agent_registry.list()],
                "count": agent_registry.count()}

    if path == "agents/capabilities":
        return {"capabilities": [c.to_dict() for c in capability_registry.list()],
                "count": capability_registry.count()}

    if path.startswith("agents/"):
        code = path.split("/")[-1]
        agent = agent_registry.get(code)
        if agent is None:
            return {"error": "agent_not_found"}
        return {"agent": agent.to_dict()}

    return None
