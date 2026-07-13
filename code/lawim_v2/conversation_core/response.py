from __future__ import annotations

import re

from ..ai.safety import ResponseQuality, validate_response
from ..persona import assistant_fallback_message, assistant_greeting, assistant_start_message


BLOCKED_EXTERNAL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bairbnb\b", re.IGNORECASE),
    re.compile(r"\bbooking(?:\.com)?\b", re.IGNORECASE),
    re.compile(r"\bvrbo\b", re.IGNORECASE),
    re.compile(r"\bjumia\s*house\b", re.IGNORECASE),
    re.compile(r"\bfacebook\s+marketplace\b", re.IGNORECASE),
    re.compile(r"\bconsultez\s+(?:airbnb|booking|vrbo|facebook)\b", re.IGNORECASE),
)


def is_blocked_external_service_request(text: str | None) -> bool:
    candidate = str(text or "")
    if not candidate:
        return False
    return any(pattern.search(candidate) for pattern in BLOCKED_EXTERNAL_PATTERNS)


def compose_external_service_refusal(language: str | None = "fr") -> str:
    lang = str(language or "fr").strip().lower()
    if lang == "en":
        return (
            "🤖 LAWIM AI: I cannot carry out that search or organize your project on an external platform. "
            "I can record your criteria, check the resources available in LAWIM, and propose a LAWIM agent or partner."
        )
    if lang == "pcm":
        return (
            "🤖 LAWIM AI: I no fit do that search or arrange your project for external platform. "
            "I fit record your criteria, check LAWIM resources, and propose LAWIM agent or partner."
        )
    return (
        "🤖 LAWIM AI : Je ne peux pas effectuer cette recherche ni organiser votre projet sur une plateforme extérieure à LAWIM. "
        "Je peux cependant enregistrer vos critères, consulter les ressources disponibles sur LAWIM et vous proposer une mise en relation avec un agent ou un partenaire référencé."
    )


def compose_welcome(language: str | None = "fr", *, known_user: bool = False, name: str | None = None) -> str:
    return assistant_start_message(language, known_user=known_user, name=name)


def compose_fallback(language: str | None = "fr") -> str:
    return assistant_fallback_message(language)


def validate_final_response(text: str | None, *, blocked_external_service: bool = False) -> ResponseQuality:
    quality = validate_response(text)
    if blocked_external_service:
        return ResponseQuality(False, quality.complete, quality.relevant, quality.safe, quality.well_formed, 0.0, "blocked_external_service")
    return quality
