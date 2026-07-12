from __future__ import annotations

from dataclasses import dataclass
import re


COMPLEXITY_KEYWORDS: tuple[str, ...] = (
    "analyse",
    "analyze",
    "juridique",
    "legal",
    "financier",
    "finance",
    "medical",
    "médical",
    "administratif",
    "compare",
    "comparaison",
    "synthese",
    "synthèse",
    "planification",
    "strategie",
    "stratégie",
    "multiple",
    "plusieurs",
    "workflow",
    "contrat",
    "budget",
    "investissement",
    "migration",
    "diagnostic",
    "audit",
)

SIMPLE_KEYWORDS: tuple[str, ...] = (
    "bonjour",
    "salut",
    "merci",
    "contact",
    "horaire",
    "horaires",
    "adresse",
    "prix",
    "services",
)


@dataclass(frozen=True, slots=True)
class ComplexityReport:
    complexity: str
    reason: str
    signals: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {"complexity": self.complexity, "reason": self.reason, "signals": list(self.signals)}


def _normalize(text: str | None) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def classify_text(text: str | None, *, context_messages: int = 0) -> ComplexityReport:
    candidate = _normalize(text)
    signals: list[str] = []
    if not candidate:
        return ComplexityReport("simple", "empty", ())
    length = len(candidate)
    question_marks = candidate.count("?")
    if length > 240:
        signals.append("long_text")
    if question_marks > 1:
        signals.append("multi_question")
    if context_messages > 6:
        signals.append("long_context")
    if any(keyword in candidate for keyword in COMPLEXITY_KEYWORDS):
        signals.append("complex_keyword")
    if any(keyword in candidate for keyword in SIMPLE_KEYWORDS):
        signals.append("simple_keyword")
    if signals and ("complex_keyword" in signals or "long_text" in signals or "long_context" in signals or "multi_question" in signals):
        return ComplexityReport("complex", "heuristic_complexity", tuple(signals))
    if length > 500:
        return ComplexityReport("complex", "very_long_text", tuple(signals))
    return ComplexityReport("simple", "heuristic_simple", tuple(signals))
