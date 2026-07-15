from __future__ import annotations

import uuid
from typing import Any

from .agent_models import AgentEvaluationResult, EvalStatus


class AgentEvaluationService:
    def __init__(self) -> None:
        self._results: list[AgentEvaluationResult] = []

    def evaluate(self, agent_id: str, scenario: str,
                  accuracy: float = 0.0, consistency: float = 0.0,
                  safety: float = 0.0) -> AgentEvaluationResult:
        status = EvalStatus.PASS if accuracy >= 0.7 and safety >= 0.7 else EvalStatus.PASS_WITH_WARNINGS
        if accuracy < 0.4 or safety < 0.4:
            status = EvalStatus.FAIL
        result = AgentEvaluationResult(
            evaluation_id=str(uuid.uuid4()),
            agent_id=agent_id,
            scenario=scenario,
            status=status,
            accuracy=accuracy,
            consistency=consistency,
            safety=safety,
            evaluated_at=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        )
        self._results.append(result)
        return result

    def list(self) -> list[AgentEvaluationResult]:
        return list(self._results)

    def get_failures(self) -> list[AgentEvaluationResult]:
        return [r for r in self._results if r.status == EvalStatus.FAIL]
