from __future__ import annotations

from typing import Any

from ..candidate import CandidateUpdate
from ..values import ExtractionMethod


class WizardAnswersToProfilePatchAdapter:
    def to_candidates(
        self,
        answers: dict[str, Any],
        correlation_id: str = "",
    ) -> list[CandidateUpdate]:
        return [
            CandidateUpdate(
                field_name=k,
                proposed_value=v,
                raw_value=str(v),
                source_type=ExtractionMethod.RULE_BASED,
                correlation_id=correlation_id,
            )
            for k, v in answers.items()
        ]
