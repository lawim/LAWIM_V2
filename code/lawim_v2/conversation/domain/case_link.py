from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class CaseConversationLink:
    link_id: str = ""
    case_id: str = ""
    conversation_id: str = ""
    channel: str = ""
    actor_id: str = ""
    linked_at: str = ""
    is_active: bool = True
    unlinked_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "link_id": self.link_id,
            "case_id": self.case_id,
            "conversation_id": self.conversation_id,
            "channel": self.channel,
            "actor_id": self.actor_id,
            "linked_at": self.linked_at,
            "is_active": self.is_active,
            "unlinked_at": self.unlinked_at,
        }
