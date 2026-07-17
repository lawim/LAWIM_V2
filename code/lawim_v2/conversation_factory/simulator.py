from __future__ import annotations
import json, logging, time, uuid
from typing import Any
from .models import ConversationScenario, ConversationSimulationState, ScenarioOutcome, PERSONAS, EMOTIONS
from .scenarios import SCENARIOS
from .evaluators import Evaluator

LOGGER = logging.getLogger(__name__)


class Simulator:
    def __init__(self, lawim_pipeline=None, evaluator: Evaluator | None = None):
        self.pipeline = lawim_pipeline
        self.evaluator = evaluator or Evaluator()
        self.results: list[dict[str, Any]] = []

    def _build_user_message(self, scenario: ConversationScenario, state: ConversationSimulationState) -> str:
        persona = PERSONAS.get(scenario.user_persona, {})
        goal = scenario.user_goal
        if state.current_turn == 0:
            return goal
        if len(state.events) < 2:
            return f"Je cherche un bien à {persona.get('location', 'ville')}."
        return "Oui, je confirme. Continuez."

    def simulate_one(self, scenario: ConversationScenario) -> ScenarioOutcome:
        state = ConversationSimulationState(
            simulation_id=str(uuid.uuid4())[:12],
            scenario_id=scenario.scenario_id,
        )
        turns = []
        start = time.perf_counter()

        for turn in range(scenario.max_turns):
            state.current_turn = turn
            user_msg = self._build_user_message(scenario, state)
            if not user_msg.strip():
                break
            turns.append({"role": "user", "content": user_msg})

            if self.pipeline:
                try:
                    lawim_response = self.pipeline(user_msg, scenario.language)
                    response_text = lawim_response.get("response", "") if isinstance(lawim_response, dict) else str(lawim_response)
                except Exception as exc:
                    response_text = f"Erreur: {exc}"
            else:
                response_text = f"[mock] Question de qualification pour: {user_msg}"
            turns.append({"role": "assistant", "content": response_text})
            state.events.append(f"turn_{turn}_completed")

            if any(t in response_text.lower() for t in ["merci", "au revoir", "visite confirmée", "transaction complétée"]):
                state.completed = True
                break

        duration = time.perf_counter() - start
        outcome = self.evaluator.evaluate(turns, scenario)
        result = {
            "scenario_id": scenario.scenario_id,
            "turns": turns,
            "turn_count": len(turns) // 2,
            "duration_s": round(duration, 3),
            "accepted": outcome.accepted,
            "score": outcome.score,
            "reasons": outcome.reasons,
            "synthetic": True,
        }
        self.results.append(result)
        return outcome

    def simulate_all(self, scenarios: list[ConversationScenario] | None = None) -> list[dict[str, Any]]:
        scenarios = scenarios or SCENARIOS
        for sc in scenarios:
            self.simulate_one(sc)
        return self.results
