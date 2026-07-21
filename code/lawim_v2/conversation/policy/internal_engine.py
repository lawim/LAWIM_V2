from __future__ import annotations

from typing import Any

from .dialogue_plan import DialoguePlan
from .greetings import CANONICAL_GREETINGS


_HANDOVER_MESSAGES: dict[str, str] = {
    "fr": "Je comprends. Je vais vous mettre en relation avec un conseiller LAWIM qui pourra vous assister.",
    "en": "I understand. I will connect you with a LAWIM advisor who can assist you.",
    "pcm": "I sabi. I go connect you with LAWIM advisor wey fit help you.",
}


class LawimInternalResponseEngine:
    def generate(self, plan: DialoguePlan) -> str:
        act = plan.dialogue_act
        lang = plan.language

        if act == "WELCOME":
            return self._generate_welcome(lang, plan)
        if act == "HANDOVER":
            return self._generate_handover(lang, plan)
        if act == "REPHRASE_LAST_QUESTION":
            return self._generate_rephrase(lang, plan)
        if act == "ACKNOWLEDGE_AND_ASK":
            return self._generate_acknowledge_and_ask(plan)
        if act == "CONFIRM_CORRECTION_AND_ASK":
            return self._generate_correction(plan)
        if act == "CLARIFY_CURRENT_SLOT":
            return self._generate_clarify(plan)
        if act in ("SEARCH_READY", "PUBLICATION_READY", "VISIT_READY", "TRANSACTION_READY"):
            return self._generate_readiness(act, lang, plan)
        if act == "SUMMARIZE_AND_CONFIRM":
            return self._generate_summarize(plan)
        if act == "CONTROLLED_ERROR":
            return self._generate_error(lang, plan)

        return plan.rendered_next_question or self._generate_acknowledge_and_ask(plan)

    def _generate_welcome(self, lang: str, plan: DialoguePlan) -> str:
        return CANONICAL_GREETINGS.get(lang, CANONICAL_GREETINGS["fr"])

    def _generate_handover(self, lang: str, plan: DialoguePlan) -> str:
        return _HANDOVER_MESSAGES.get(lang, _HANDOVER_MESSAGES["fr"])

    def _generate_rephrase(self, lang: str, plan: DialoguePlan) -> str:
        question = plan.rendered_next_question or "Pourriez-vous reformuler votre r\u00e9ponse ?"
        if lang == "fr":
            return f"Je reformule ma question : {question}"
        if lang == "en":
            return f"Let me rephrase: {question}"
        return f"Make I talk am well: {question}"

    def _generate_acknowledge_and_ask(self, plan: DialoguePlan) -> str:
        parts: list[str] = []
        for key, value in plan.facts_to_confirm.items():
            formatted = self._format_fact(key, value, plan.language)
            if formatted:
                parts.append(formatted)
        ack = ""
        if parts:
            if plan.language == "fr":
                ack = "Tr\u00e8s bien. Vous recherchez " + ", ".join(parts) + "."
            elif plan.language == "en":
                ack = "Very well. You are looking for " + ", ".join(parts) + "."
            elif plan.language == "pcm":
                ack = "Okay. You dey find " + ", ".join(parts) + "."
        question = plan.rendered_next_question
        if ack and question:
            return f"{ack}\n\n{question}"
        if question:
            return question
        if ack:
            return ack
        return plan.rendered_next_question or ""

    def _generate_correction(self, plan: DialoguePlan) -> str:
        lang = plan.language
        corrected = plan.facts_to_confirm
        parts: list[str] = []
        for key, value in corrected.items():
            formatted = self._format_fact(key, value, lang)
            if formatted:
                parts.append(formatted)
        if lang == "fr":
            base = "J'ai bien not\u00e9 votre correction"
            if parts:
                base += " : " + ", ".join(parts)
        elif lang == "en":
            base = "I have noted your correction"
            if parts:
                base += ": " + ", ".join(parts)
        else:
            base = "I don hammer your correction"
            if parts:
                base += ": " + ", ".join(parts)
        if plan.rendered_next_question:
            return f"{base}.\n\n{plan.rendered_next_question}"
        return f"{base}."

    def _generate_clarify(self, plan: DialoguePlan) -> str:
        return plan.rendered_next_question or "Pourriez-vous reformuler votre r\u00e9ponse ?"

    def _generate_readiness(self, act: str, lang: str, plan: DialoguePlan) -> str:
        if act == "SEARCH_READY":
            if lang == "fr":
                return "Merci ! Vos informations sont compl\u00e8tes. Je lance la recherche..."
            if lang == "en":
                return "Thank you! Your information is complete. Starting search..."
            return "Thank you! Your information don complete. I dey start search..."
        if act == "PUBLICATION_READY":
            return "Merci ! Votre annonce est pr\u00eate \u00e0 \u00eatre publi\u00e9e."
        if act == "VISIT_READY":
            return "Merci ! Je peux organiser une visite pour ce bien."
        return "Votre dossier est pr\u00eat. Que souhaitez-vous faire ?"

    def _generate_summarize(self, plan: DialoguePlan) -> str:
        lang = plan.language
        parts: list[str] = []
        for key, value in plan.facts_to_confirm.items():
            formatted = self._format_fact(key, value, lang)
            if formatted:
                parts.append(formatted)
        if lang == "fr":
            summary = "R\u00e9capitulons vos informations"
        elif lang == "en":
            summary = "Let me summarize your information"
        else:
            summary = "Make I recap your information"
        if parts:
            summary += " :\n- " + "\n- ".join(parts)
        if not plan.rendered_next_question:
            if lang == "fr":
                summary += "\n\nCes informations sont-elles correctes ?"
            elif lang == "en":
                summary += "\n\nIs this information correct?"
            else:
                summary += "\n\nDis information correct?"
        else:
            summary += f"\n\n{plan.rendered_next_question}"
        return summary

    def _generate_error(self, lang: str, plan: DialoguePlan) -> str:
        if lang == "fr":
            return "D\u00e9sol\u00e9, je n'ai pas pu traiter votre demande. Pouvez-vous reformuler ?"
        if lang == "en":
            return "Sorry, I could not process your request. Could you rephrase?"
        return "Sorry, I no fit handle your request. Abeg talk am again."

    @staticmethod
    def _format_fact(key: str, value: Any, language: str) -> str:
        if key in ("budget_max", "budget"):
            return f"avec un budget de {value} FCFA"
        if key == "property_type":
            return f"de type {value}"
        if key == "city":
            return f"\u00e0 {value}"
        if key == "neighborhood":
            return f"dans le quartier {value}"
        if key == "bedroom_count":
            return f"de {value} chambres"
        if key == "district":
            return f"\u00e0 {value}"
        if key == "transaction_type":
            if value == "rent":
                return "en location" if language == "fr" else "for rent"
            if value == "buy":
                return "\u00e0 l'achat" if language == "fr" else "to buy"
            if value == "sell":
                return "\u00e0 vendre" if language == "fr" else "for sale"
        return f"{key}: {value}"
