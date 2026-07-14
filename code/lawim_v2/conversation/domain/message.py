from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class NormalizedMessage:
    raw_text: str = ""
    normalized_text: str = ""
    channel: str = ""
    channel_message_id: str | None = None
    channel_user_id: str | None = None
    user_id: int | None = None
    channel_identity_id: int | None = None
    conversation_id: int | None = None
    project_id: int | None = None
    reply_to_message_id: str | None = None
    attachments: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    is_duplicate: bool = False
    timestamp: str | None = None

    def is_greeting(self) -> bool:
        greetings = {
            "bonjour", "salut", "hello", "bonsoir", "hi", "cc", "bjr", "slt",
            "coucou", "hey", "yo", "bsr",
        }
        text = self.normalized_text.strip().lower().rstrip("!.,?")
        if not text:
            return False
        words = text.split()
        return text in greetings or (words and words[0] in greetings)

    def is_short_reply(self) -> bool:
        text = self.normalized_text.strip().lower()
        short_affirmatives = {"ok", "oui", "d'accord", "dac", "okay", "d'accord", "yes", "si", "da"}
        short_negatives = {"non", "no", "nan", "pas", "non merci"}
        return text in short_affirmatives or text in short_negatives

    def is_handover_request(self) -> bool:
        text = self.normalized_text.strip().lower()
        indicators = [
            "parler a une personne",
            "parler a un conseiller",
            "agent lawim",
            "conseiller lawim",
            "humain",
            "personne reelle",
            "parler a quelqu'un",
            "operateur",
            "assistance",
        ]
        return any(ind in text for ind in indicators)

    def is_affirmative_short(self) -> bool:
        return self.normalized_text.strip().lower() in {"ok", "oui", "d'accord", "dac", "okay", "yes", "si", "da", "vas-y", "yep"}

    def is_negative_short(self) -> bool:
        return self.normalized_text.strip().lower() in {"non", "no", "nan", "non merci", "pas maintenant"}
