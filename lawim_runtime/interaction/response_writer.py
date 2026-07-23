from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from .response_plan import InteractionResponsePlan, ResponseType

logger = logging.getLogger(__name__)


@dataclass
class ResponseWriterRequest:
    writer_request_id: str = field(default_factory=lambda: uuid4().hex[:16])
    response_plan: InteractionResponsePlan | None = None
    language: str = "fr"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ResponseWriterResult:
    writer_result_id: str = field(default_factory=lambda: uuid4().hex[:16])
    text: str = ""
    formatted_text: str = ""
    parse_mode: str = "text"
    success: bool = False
    error: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ResponseWriter(ABC):

    @abstractmethod
    def write(self, request: ResponseWriterRequest) -> ResponseWriterResult:
        ...


class DeterministicResponseWriter(ResponseWriter):

    _SAFE_FALLBACK_TEXT = (
        "\U0001f916 LAWIM AI\n\n"
        "Je rencontre momentan\u00e9ment une difficult\u00e9 pour traiter correctement "
        "votre demande. Votre message a bien \u00e9t\u00e9 enregistr\u00e9 et vous "
        "n\u2019aurez pas \u00e0 le reformuler."
    )

    _GREETING_TEXT = (
        "\U0001f916 LAWIM AI\n\n"
        "Bonjour ! Je suis l\u2019assistant intelligent de LAWIM. "
        "Je peux vous aider \u00e0 trouver un bien immobilier, "
        "\u00e0 planifier une visite ou \u00e0 suivre vos projets. "
        "Que puis-je pour vous ?"
    )

    _HANDOVER_TEXT = (
        "\U0001f916 LAWIM AI\n\n"
        "Je vais vous passer \u00e0 un conseiller LAWIM qui pourra "
        "vous assister. Veuillez patienter un instant."
    )

    _ASK_MISSING_FIELD_TEMPLATE = (
        "\U0001f916 LAWIM AI\n\n"
        "Pour avancer, j\u2019ai besoin des informations suivantes :\n"
        "{field_questions}"
    )

    _PRESENT_RESULTS_TEMPLATE = (
        "\U0001f916 LAWIM AI\n\n"
        "Voici les r\u00e9sultats de ma recherche :\n"
        "{results}"
    )

    _SUCCESS_TEMPLATE = (
        "\U0001f916 LAWIM AI\n\n"
        "{message}"
    )

    _WAIT_TEXT = (
        "\U0001f916 LAWIM AI\n\n"
        "Je traite votre demande. Veuillez patienter quelques instants."
    )

    def write(self, request: ResponseWriterRequest) -> ResponseWriterResult:
        plan = request.response_plan
        if not plan:
            return self._fallback()

        rtype = plan.response_type

        if rtype == ResponseType.SAFE_FALLBACK:
            return self._result(self._SAFE_FALLBACK_TEXT, success=True)
        elif rtype == ResponseType.GREETING:
            return self._result(self._GREETING_TEXT, success=True)
        elif rtype == ResponseType.HANDOVER:
            return self._result(self._HANDOVER_TEXT, success=True)
        elif rtype == ResponseType.ASK_MISSING_FIELD:
            field = plan.selected_field or ""
            questions = f"- {field}" if field else "Veuillez pr\u00e9ciser votre demande."
            return self._result(
                self._ASK_MISSING_FIELD_TEMPLATE.format(field_questions=questions),
                success=True,
            )
        elif rtype == ResponseType.PRESENT_RESULTS:
            facts = plan.structured_facts
            results = self._format_facts(facts)
            return self._result(
                self._PRESENT_RESULTS_TEMPLATE.format(results=results),
                success=True,
            )
        elif rtype == ResponseType.SUCCESS:
            msg = plan.structured_facts.get("message", "Op\u00e9ration effectu\u00e9e avec succ\u00e8s.")
            return self._result(
                self._SUCCESS_TEMPLATE.format(message=msg),
                success=True,
            )
        elif rtype == ResponseType.WAIT:
            return self._result(self._WAIT_TEXT, success=True)
        elif rtype in (ResponseType.ASK_CONFIRMATION, ResponseType.ERROR):
            msg = plan.structured_facts.get("message", "")
            if msg:
                return self._result(
                    f"\U0001f916 LAWIM AI\n\n{msg}",
                    success=True,
                )
            return self._result("", success=True)
        elif rtype == ResponseType.NO_RESPONSE:
            return self._result("", success=True)
        else:
            return self._fallback()

    def _result(self, text: str, success: bool = False) -> ResponseWriterResult:
        return ResponseWriterResult(
            text=text,
            formatted_text=text,
            parse_mode="text",
            success=success,
        )

    def _fallback(self) -> ResponseWriterResult:
        return ResponseWriterResult(
            text=self._SAFE_FALLBACK_TEXT,
            formatted_text=self._SAFE_FALLBACK_TEXT,
            parse_mode="text",
            success=True,
        )

    def _format_facts(self, facts: dict[str, Any]) -> str:
        if not facts:
            return "Aucun r\u00e9sultat disponible."
        lines: list[str] = []
        for key, value in facts.items():
            lines.append(f"- {key}: {value}")
        return "\n".join(lines)


class TemplateResponseWriter(DeterministicResponseWriter):
    pass
