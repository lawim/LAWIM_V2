from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
import uuid

from .models import FallbackResolution
from .prompts.fallback import DEFAULT_FALLBACK_MESSAGE
from .safety import redact_sensitive_text


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True, slots=True)
class FallbackMatch:
    entry_key: str
    intent: str
    answer: str
    confidence: float
    used_generic: bool
    metadata: dict[str, object]


class FallbackEngine:
    def __init__(self, repository, config) -> None:
        self.repository = repository
        self.config = config

    def resolve(self, request) -> FallbackResolution:
        query = redact_sensitive_text(request.sanitized_text or request.text)
        best = self._best_match(query, language=request.language, channel=request.channel)
        if best is not None:
            return FallbackResolution(
                provider="internal",
                model="internal-fallback",
                content=best.answer,
                used_generic=False,
                entry_key=best.entry_key,
                intent=best.intent,
                confidence=best.confidence,
                metadata={"match": best.metadata},
            )
        return FallbackResolution(
            provider="internal",
            model="internal-fallback",
            content=self.config.fallback_message or DEFAULT_FALLBACK_MESSAGE,
            used_generic=True,
            entry_key=None,
            intent="fallback_generic",
            confidence=0.45,
            metadata={"reason": "generic_fallback"},
        )

    def _best_match(self, query: str, *, language: str, channel: str) -> FallbackMatch | None:
        rows = self.repository.list_ai_fallback_entries(status="published")
        if not rows:
            rows = self.repository.list_ai_fallback_entries(status="approved")
        query_normalized = self._normalize(query)
        query_words = set(self._tokens(query_normalized))
        best_score = 0.0
        best_match: FallbackMatch | None = None
        for row in rows:
            language_value = str(row.get("language") or "").strip().lower()
            channel_value = str(row.get("channel") or "").strip().lower()
            if language_value and language_value != language.lower():
                continue
            if channel_value and channel_value not in {"all", channel.lower()}:
                continue
            variants = self._json_list(row.get("variants_json"))
            keywords = self._json_list(row.get("keywords_json"))
            question = self._normalize(str(row.get("question") or ""))
            answer = str(row.get("response_text") or row.get("answer") or "").strip()
            if not answer:
                continue
            score = 0.0
            if question and (query_normalized == question or query_normalized in question or question in query_normalized):
                score += 4.0
            score += 1.5 * len(query_words.intersection(self._tokens(question)))
            score += 1.2 * len(query_words.intersection({self._normalize(str(item)) for item in keywords}))
            for variant in variants:
                variant_normalized = self._normalize(str(variant))
                if variant_normalized and variant_normalized in query_normalized:
                    score += 1.0
            if any(token in query_normalized for token in ("bonjour", "salut", "hello", "merci")) and str(row.get("intent") or "").startswith("greeting"):
                score += 1.5
            if any(token in query_normalized for token in ("contact", "telephone", "phone", "whatsapp", "telegram")) and str(row.get("intent") or "").startswith("contact"):
                score += 1.5
            if score > best_score and score >= 1.5:
                best_score = score
                best_match = FallbackMatch(
                    entry_key=str(row.get("fallback_key") or row.get("intent") or uuid.uuid4().hex),
                    intent=str(row.get("intent") or "fallback"),
                    answer=answer,
                    confidence=min(0.99, 0.5 + score / 10.0),
                    used_generic=False,
                    metadata={
                        "category": row.get("category"),
                        "language": row.get("language"),
                        "channel": row.get("channel"),
                        "score": score,
                    },
                )
        return best_match

    @staticmethod
    def _normalize(value: str) -> str:
        return re.sub(r"\s+", " ", value.strip().lower())

    @staticmethod
    def _tokens(value: str) -> tuple[str, ...]:
        return tuple(token for token in re.split(r"[^a-z0-9]+", value) if token)

    @staticmethod
    def _json_list(value: object | None) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value if str(item).strip()]
        if isinstance(value, tuple):
            return [str(item) for item in value if str(item).strip()]
        return []
