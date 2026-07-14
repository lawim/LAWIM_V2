from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ..domain.intents import Intent, IntentCandidate


class ProviderType(str, Enum):
    LLM = "llm"
    DETERMINISTIC = "deterministic"
    FALLBACK = "fallback"


class CircuitBreakerState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    failure_count: int = 0
    max_failures: int = 3
    reset_timeout: float = 60.0
    last_failure_time: float = 0.0
    state: CircuitBreakerState = CircuitBreakerState.CLOSED

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = CircuitBreakerState.CLOSED

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.max_failures:
            self.state = CircuitBreakerState.OPEN

    def allow_request(self) -> bool:
        if self.state == CircuitBreakerState.CLOSED:
            return True
        if self.state == CircuitBreakerState.OPEN:
            elapsed = time.time() - self.last_failure_time
            if elapsed >= self.reset_timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False
        return True

    def __bool__(self) -> bool:
        return self.allow_request()


class LLMAdapter:

    def __init__(
        self,
        *,
        provider: str = "mock",
        model: str = "gpt-4o",
        api_key: str | None = None,
        max_retries: int = 2,
        timeout: float = 30.0,
    ) -> None:
        self._provider_name = provider
        self._model = model
        self._api_key = api_key
        self._max_retries = max_retries
        self._timeout = timeout
        self._last_provider_used: ProviderType = ProviderType.DETERMINISTIC
        self._circuit_breaker = CircuitBreaker()

    @property
    def last_provider_used(self) -> ProviderType:
        return self._last_provider_used

    @property
    def is_available(self) -> bool:
        if not self._circuit_breaker.allow_request():
            return False
        if self._provider_name == "mock":
            return False
        return self._api_key is not None and len(self._api_key) > 0

    def classify_intent(self, text: str) -> list[IntentCandidate]:
        if self.is_available:
            try:
                result = self._call_llm_classify(text)
                self._circuit_breaker.record_success()
                self._last_provider_used = ProviderType.LLM
                return result
            except Exception:
                self._circuit_breaker.record_failure()
                return self._fallback_classify(text)
        self._last_provider_used = ProviderType.DETERMINISTIC
        return self._fallback_classify(text)

    def extract_entities(self, text: str) -> dict[str, Any]:
        if self.is_available:
            try:
                result = self._call_llm_extract(text)
                self._circuit_breaker.record_success()
                self._last_provider_used = ProviderType.LLM
                return result
            except Exception:
                self._circuit_breaker.record_failure()
                return self._fallback_extract(text)
        self._last_provider_used = ProviderType.DETERMINISTIC
        return self._fallback_extract(text)

    def rephrase(self, text: str, context: dict[str, Any] | None = None) -> str:
        if self.is_available:
            try:
                result = self._call_llm_rephrase(text, context)
                self._circuit_breaker.record_success()
                self._last_provider_used = ProviderType.LLM
                return result
            except Exception:
                self._circuit_breaker.record_failure()
                self._last_provider_used = ProviderType.FALLBACK
                return text
        self._last_provider_used = ProviderType.DETERMINISTIC
        return text

    def reset_circuit_breaker(self) -> None:
        self._circuit_breaker = CircuitBreaker()

    def _call_llm_classify(self, text: str) -> list[IntentCandidate]:
        raise NotImplementedError(
            "LLM classify_intent requires a concrete provider implementation. "
            "Subclass LLMAdapter and override this method."
        )

    def _call_llm_extract(self, text: str) -> dict[str, Any]:
        raise NotImplementedError(
            "LLM extract_entities requires a concrete provider implementation. "
            "Subclass LLMAdapter and override this method."
        )

    def _call_llm_rephrase(self, text: str, context: dict[str, Any] | None = None) -> str:
        raise NotImplementedError(
            "LLM rephrase requires a concrete provider implementation. "
            "Subclass LLMAdapter and override this method."
        )

    def _fallback_classify(self, text: str) -> list[IntentCandidate]:
        text_lower = text.lower().strip()

        intent_map: list[tuple[list[str], Intent, float]] = [
            (["acheter appartement", "achat appartement", "acheter un appartement"], Intent.BUY_APARTMENT, 0.8),
            (["acheter maison", "achat maison", "acheter une maison"], Intent.BUY_HOUSE, 0.8),
            (["acheter villa", "achat villa", "acheter une villa"], Intent.BUY_VILLA, 0.8),
            (["acheter terrain", "achat terrain", "acheter un terrain", "terrain"], Intent.BUY_LAND, 0.8),
            (["acheter local", "achat commercial", "local commercial"], Intent.BUY_COMMERCIAL, 0.8),
            (["louer appartement", "location appartement", "appartement à louer"], Intent.RENT_APARTMENT, 0.8),
            (["louer maison", "location maison", "maison à louer"], Intent.RENT_HOUSE, 0.8),
            (["louer villa", "location villa", "villa à louer"], Intent.RENT_VILLA, 0.8),
            (["louer studio", "location studio", "studio à louer"], Intent.RENT_STUDIO, 0.8),
            (["louer chambre", "location chambre"], Intent.RENT_ROOM, 0.8),
            (["vendre maison", "vente maison"], Intent.SELL_HOUSE, 0.8),
            (["vendre appartement", "vente appartement"], Intent.SELL_APARTMENT, 0.8),
            (["vendre terrain", "vente terrain"], Intent.SELL_LAND, 0.8),
            (["construire", "construction"], Intent.CONSTRUCT, 0.7),
            (["rénover", "renovation"], Intent.RENOVATE, 0.7),
            (["investir", "investissement"], Intent.INVEST, 0.7),
            (["architecte"], Intent.FIND_ARCHITECT, 0.6),
            (["ingénieur", "ingenieur"], Intent.FIND_ENGINEER, 0.6),
            (["notaire"], Intent.FIND_NOTARY, 0.6),
            (["agent immobilier"], Intent.FIND_AGENT, 0.6),
            (["entrepreneur", "constructeur"], Intent.FIND_CONTRACTOR, 0.6),
            (["avocat"], Intent.FIND_LAWYER, 0.6),
            (["technicien"], Intent.FIND_TECHNICIAN, 0.6),
            (["bonjour", "salut", "bonsoir", "hello"], Intent.GREETING, 0.9),
            (["aide", "information", "documentation"], Intent.INFORMATION, 0.5),
            (["plainte", "réclamation", "reclamation"], Intent.COMPLAINT, 0.6),
        ]

        results: list[IntentCandidate] = []
        matched_triggers: set[str] = set()

        for triggers, intent, confidence in intent_map:
            for trigger in triggers:
                if trigger in text_lower and trigger not in matched_triggers:
                    matched_triggers.add(trigger)
                    results.append(IntentCandidate(
                        intent=intent,
                        confidence=confidence,
                        source="deterministic_fallback",
                        raw_trigger=trigger,
                    ))
                    break

        if not results:
            results.append(IntentCandidate(
                intent=Intent.OTHER,
                confidence=0.3,
                source="deterministic_fallback",
                raw_trigger=None,
            ))

        return results

    def _fallback_extract(self, text: str) -> dict[str, Any]:
        text_lower = text.lower()
        entities: dict[str, Any] = {}

        budget_patterns = [
            (r"(\d+)\s*(?:000\s*)?(?:f|cfa|franc)", "budget"),
            (r"(\d+)\s*(?:millions?\s*)?(?:f|cfa)", "budget"),
            (r"(?:budget|prix|cout|coût)\s*(?:de|:|\s)*\s*(\d+)", "budget"),
        ]
        import re
        for pattern, key in budget_patterns:
            match = re.search(pattern, text_lower)
            if match:
                value = match.group(1)
                if key == "budget":
                    entities["budget"] = value
                    entities["budget_raw"] = match.group(0)
                break

        city_keywords = ["à ", "sur ", "vers ", "dans "]
        for kw in city_keywords:
            idx = text_lower.find(kw)
            if idx >= 0:
                after = text_lower[idx + len(kw):].strip()
                city_end = min(
                    (after.find(ch) for ch in " ?.,!;" if after.find(ch) >= 0),
                    default=len(after),
                )
                candidate = after[:city_end].strip()
                if candidate and len(candidate) > 1 and candidate not in {"paris", "abidjan", "dakar", "yaoundé", "douala"}:
                    entities["city"] = candidate.capitalize()
                break

        for city in ["abidjan", "dakar", "yaoundé", "douala", "paris", "marseille", "lyon"]:
            if city in text_lower:
                entities["city"] = city.capitalize()
                break

        property_keywords = {
            "appartement": "apartment",
            "maison": "house",
            "villa": "villa",
            "terrain": "land",
            "studio": "studio",
            "bureau": "office",
            "local": "commercial",
            "commerce": "commercial",
        }
        for keyword, normalized in property_keywords.items():
            if keyword in text_lower:
                entities["property_type"] = normalized
                break

        room_pattern = r"(\d+)\s*(?:chambres|pièces|pieces|chambre)"
        match = re.search(room_pattern, text_lower)
        if match:
            entities["bedrooms"] = int(match.group(1))

        transaction_keywords = {
            "acheter": "buy",
            "achat": "buy",
            "louer": "rent",
            "location": "rent",
            "vendre": "sell",
            "vente": "sell",
            "construire": "construct",
        }
        for keyword, normalized in transaction_keywords.items():
            if keyword in text_lower:
                entities["transaction_type"] = normalized
                break

        return entities

    def _fallback_rephrase(self, text: str, context: dict[str, Any] | None = None) -> str:
        return text
