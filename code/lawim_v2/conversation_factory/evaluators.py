from __future__ import annotations
from typing import Any
from .models import ConversationScenario, ScenarioOutcome


class Evaluator:
    def evaluate(self, turns: list[dict[str, str]], scenario: ConversationScenario) -> ScenarioOutcome:
        reasons = []
        score = 5.0
        assistant_msgs = [t for t in turns if t["role"] == "assistant"]
        user_msgs = [t for t in turns if t["role"] == "user"]

        if not assistant_msgs:
            return ScenarioOutcome(accepted=False, score=0.0, reasons=["No assistant response"], turns=len(turns)//2)

        for msg in assistant_msgs:
            c = msg.get("content", "")
            if len(c) < 5:
                reasons.append(f"Too short response: {c[:30]}")
                score -= 0.5
            if "erreur" in c.lower() or "error" in c.lower():
                reasons.append("Error in response")
                score -= 1.0
            if "merci" in c.lower() or "thank" in c.lower() or "thank you" in c.lower():
                reasons.append("Conversation ended naturally")
                score = max(score, 4.0)

        if len(user_msgs) >= scenario.max_turns:
            reasons.append("Max turns reached")
            score -= 0.5

        score = max(0.0, min(5.0, score))
        accepted = score >= 3.0
        return ScenarioOutcome(accepted=accepted, score=round(score, 2), reasons=reasons, turns=len(turns)//2)
