from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from .facts import Fact, FactStatus


class SlotChangeType(str, Enum):
    INITIAL = "INITIAL"
    UPDATE = "UPDATE"
    CORRECTION = "CORRECTION"
    CLEAR = "CLEAR"
    SYSTEM_DERIVED = "SYSTEM_DERIVED"
    HUMAN_OVERRIDE = "HUMAN_OVERRIDE"


@dataclass
class SlotValueHistory:
    slot_name: str = ""
    previous_value: Any = None
    new_value: Any = None
    change_type: SlotChangeType = SlotChangeType.INITIAL
    source_message_id: str | None = None
    source_channel: str | None = None
    changed_at: str = ""
    fact: Fact | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "slot_name": self.slot_name,
            "previous_value": self.previous_value,
            "new_value": self.new_value,
            "change_type": self.change_type.value,
            "source_message_id": self.source_message_id,
            "source_channel": self.source_channel,
            "changed_at": self.changed_at,
            "fact_id": self.fact.fact_id if self.fact else None,
            "fact_field": self.fact.field if self.fact else None,
            "metadata": dict(self.metadata),
        }
