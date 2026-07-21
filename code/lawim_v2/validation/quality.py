from __future__ import annotations

import re
from typing import Any


class ResponseQualityEvaluator:
    """Evaluates response quality on a continuous scale (0.0 - 1.0)."""

    CRITERIA: dict[str, float] = {
        "accuracy": 0.25,
        "relevance": 0.15,
        "conciseness": 0.15,
        "clarity": 0.10,
        "naturalness": 0.10,
        "professional_tone": 0.10,
        "language_consistency": 0.10,
        "no_jargon": 0.05,
    }

    def evaluate(
        self,
        content: str,
        request,
        dialogue_plan=None,
    ) -> tuple[float, dict]:
        details: dict[str, float] = {}

        details["accuracy"] = self._score_accuracy(content, request, dialogue_plan)
        details["relevance"] = self._score_relevance(content, request, dialogue_plan)
        details["conciseness"] = self._score_conciseness(content)
        details["clarity"] = self._score_clarity(content)
        details["naturalness"] = self._score_naturalness(content)
        details["professional_tone"] = self._score_professional_tone(content)
        details["language_consistency"] = self._score_language_consistency(content)
        details["no_jargon"] = self._score_no_jargon(content)

        score = sum(
            details[criterion] * weight
            for criterion, weight in self.CRITERIA.items()
        )

        return score, details

    def is_acceptable(
        self,
        content: str,
        request,
        dialogue_plan=None,
        threshold: float = 0.6,
    ) -> bool:
        score, _ = self.evaluate(content, request, dialogue_plan)
        return score >= threshold

    def _score_accuracy(
        self,
        content: str,
        request,
        dialogue_plan=None,
    ) -> float:
        if not content:
            return 0.0
        return 1.0

    def _score_relevance(
        self,
        content: str,
        request,
        dialogue_plan=None,
    ) -> float:
        if not content:
            return 0.0
        return 1.0

    def _score_conciseness(self, content: str) -> float:
        if not content:
            return 0.0
        words = content.split()
        if len(words) <= 30:
            return 1.0
        if len(words) <= 60:
            return 0.7
        if len(words) <= 100:
            return 0.4
        return 0.2

    def _score_clarity(self, content: str) -> float:
        if not content:
            return 0.0
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            return 0.0
        avg_len = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_len <= 15:
            return 1.0
        if avg_len <= 25:
            return 0.7
        if avg_len <= 40:
            return 0.4
        return 0.2

    def _score_naturalness(self, content: str) -> float:
        if not content:
            return 0.0
        return 0.8

    def _score_professional_tone(self, content: str) -> float:
        if not content:
            return 0.0
        unprofessional = ["lol", "omg", "wtf", "stfu", "idk", "btw"]
        lower = content.lower()
        matches = sum(1 for w in unprofessional if w in lower)
        if matches == 0:
            return 1.0
        return max(0.0, 1.0 - matches * 0.3)

    def _score_language_consistency(self, content: str) -> float:
        if not content:
            return 0.0
        return 1.0

    def _score_no_jargon(self, content: str) -> float:
        if not content:
            return 0.0
        return 0.9
