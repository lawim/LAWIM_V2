from __future__ import annotations

from typing import Any

from ..persona import assistant_start_message

RESUMPTION_TEMPLATES: dict[str, str] = {
    "fr": (
        "Nous avions avancé sur votre projet **{objective}** à **{city}**.\n\n"
        "{confirmed_section}"
        "{pending_section}"
        "{next_step}"
    ),
    "en": (
        "We had been working on your project **{objective}** in **{city}**.\n\n"
        "{confirmed_section}"
        "{pending_section}"
        "{next_step}"
    ),
    "pcm": (
        "We don stop for your project **{objective}** for **{city}**.\n\n"
        "{confirmed_section}"
        "{pending_section}"
        "{next_step}"
    ),
}


def _items_text(items: list[dict[str, Any]], lang: str) -> str:
    lines: list[str] = []
    for item in items:
        label = str(item.get("label", ""))
        value = str(item.get("value", ""))
        lines.append(f"- {label} : {value}")
    return "\n".join(lines)


def _confirm_label(lang: str) -> str:
    labels = {"fr": "✅ Ce qui est confirmé", "en": "✅ Confirmed", "pcm": "✅ We don confirm"}
    return labels.get(lang, labels["fr"])


def _pending_label(lang: str) -> str:
    labels = {"fr": "⏳ En attente", "en": "⏳ Pending", "pcm": "⏳ Dey wait"}
    return labels.get(lang, labels["fr"])


def _next_label(lang: str) -> str:
    labels = {"fr": "▶️ Prochaine étape", "en": "▶️ Next step", "pcm": "▶️ Next tin"}
    return labels.get(lang, labels["fr"])


def build_resumption(
    *,
    project: dict[str, Any] | None,
    confirmed_facts: list[dict[str, Any]],
    pending_hypotheses: list[dict[str, Any]],
    last_action: str | None,
    next_step: str | None,
    next_question: str | None,
    language: str = "fr",
) -> dict[str, Any]:
    lang = language if language in RESUMPTION_TEMPLATES else "fr"
    objective = str(project.get("objective", "immobilier")) if project else "immobilier"
    city = str(project.get("location_city", "")) if project else ""
    if not confirmed_facts and not pending_hypotheses and not project:
        short = {
            "fr": assistant_start_message("fr"),
            "en": assistant_start_message("en"),
            "pcm": assistant_start_message("pcm"),
        }
        return {
            "has_history": False,
            "short_summary": short.get(lang, short["fr"]),
            "summary": short.get(lang, short["fr"]),
            "next_question": None,
            "language": lang,
        }

    confirmed_section = ""
    if confirmed_facts:
        lines = _items_text(confirmed_facts, lang)
        confirmed_section = f"{_confirm_label(lang)} :\n{lines}\n\n"
    else:
        confirmed_section = ""

    pending_section = ""
    if pending_hypotheses:
        lines = _items_text(pending_hypotheses, lang)
        pending_section = f"{_pending_label(lang)} :\n{lines}\n\n"

    next_step_text = ""
    if next_question:
        next_step_text = f"{_next_label(lang)} : {next_question}"
    elif next_step:
        next_step_text = f"{_next_label(lang)} : {next_step}"

    summary = RESUMPTION_TEMPLATES[lang].format(
        objective=objective,
        city=city,
        confirmed_section=confirmed_section,
        pending_section=pending_section,
        next_step=next_step_text,
    )

    short = confirmed_section.split("\n")[0] if confirmed_section else ""
    if not short and next_question:
        short = f"{_next_label(lang)} : {next_question}"

    return {
        "has_history": True,
        "short_summary": short.strip() or summary[:120],
        "summary": summary.strip(),
        "objective": objective,
        "city": city,
        "confirmed_count": len(confirmed_facts),
        "pending_count": len(pending_hypotheses),
        "last_action": last_action,
        "next_step": next_step,
        "next_question": next_question,
        "language": lang,
    }


class ResumeEngine:
    def build(
        self,
        *,
        project: dict[str, Any] | None,
        confirmed_facts: list[dict[str, Any]],
        pending_hypotheses: list[dict[str, Any]],
        last_action: str | None = None,
        next_step: str | None = None,
        next_question: str | None = None,
        language: str = "fr",
    ) -> dict[str, Any]:
        return build_resumption(
            project=project,
            confirmed_facts=confirmed_facts,
            pending_hypotheses=pending_hypotheses,
            last_action=last_action,
            next_step=next_step,
            next_question=next_question,
            language=language,
        )
