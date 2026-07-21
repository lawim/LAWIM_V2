from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DialoguePlan:
    speaker: str = "LAWIM AI"
    language: str = "fr"
    dialogue_act: str = ""
    facts_to_confirm: dict[str, Any] = field(default_factory=dict)
    facts_not_to_repeat: list[str] = field(default_factory=list)
    next_question_key: str = ""
    rendered_next_question: str = ""
    maximum_questions: int = 1
    maximum_sentences: int = 4
    maximum_characters: int = 600
    tone: list[str] = field(default_factory=list)
    list_policy: str = "avoid"
    forbidden_phrases: list[str] = field(default_factory=list)
    forbidden_topics: list[str] = field(default_factory=list)
    footer_required: bool = True
    generated_by_ai: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "speaker": self.speaker,
            "language": self.language,
            "dialogue_act": self.dialogue_act,
            "facts_to_confirm": dict(self.facts_to_confirm),
            "facts_not_to_repeat": list(self.facts_not_to_repeat),
            "next_question_key": self.next_question_key,
            "rendered_next_question": self.rendered_next_question,
            "maximum_questions": self.maximum_questions,
            "maximum_sentences": self.maximum_sentences,
            "maximum_characters": self.maximum_characters,
            "tone": list(self.tone),
            "list_policy": self.list_policy,
            "forbidden_phrases": list(self.forbidden_phrases),
            "forbidden_topics": list(self.forbidden_topics),
            "footer_required": self.footer_required,
            "generated_by_ai": self.generated_by_ai,
        }
