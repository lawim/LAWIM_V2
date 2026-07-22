from __future__ import annotations
from typing import Any
from ..qualification.engine import QualificationEngine
from ..qualification.registry import RequirementRegistry
from ..qualification.result import QualificationResult
from ..decision.engine import DecisionEngine
from ..decision.result import DecisionResult
from ..decision.handover import HumanHandoverEvaluator, HandoverEvaluation
from ..project_profile.base import AbstractProjectProfile
from ..project_profile.registry import FieldRegistry
from .state import ProjectBrainState


class ProjectBrain:
    def __init__(
        self,
        qual_engine: QualificationEngine,
        decision_engine: DecisionEngine,
        handover_evaluator: HumanHandoverEvaluator,
    ) -> None:
        self._qual = qual_engine
        self._decision = decision_engine
        self._handover = handover_evaluator

    def evaluate(
        self,
        profile: AbstractProjectProfile,
        user_message: str = "",
    ) -> tuple[QualificationResult, DecisionResult, ProjectBrainState]:
        qual_result = self._qual.evaluate(profile)
        handover_eval = self._handover.evaluate(profile, user_message)
        decision = self._decision.decide(profile, qual_result)
        state = ProjectBrainState(
            project_id=profile.project_id,
            profile_id=profile.profile_id,
            project_type=profile.profile_type,
            qualification_score=qual_result.score.final_score,
            qualification_level=qual_result.level.value,
            selected_action=decision.selected_action,
            selected_field=decision.selected_field,
            blocking_reasons=qual_result.blockers,
            human_required=handover_eval.handover_required or decision.human_required,
        )
        return qual_result, decision, state
