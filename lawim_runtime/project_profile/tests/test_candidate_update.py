from __future__ import annotations

import pytest

from lawim_runtime.project_profile.candidate import CandidateUpdate
from lawim_runtime.project_profile.values import ExtractionMethod


class TestCandidateUpdate:
    def test_create_candidate(self):
        c = CandidateUpdate(
            field_name="city",
            raw_value="Douala",
            proposed_value="Douala",
            confidence=0.9,
            source_type=ExtractionMethod.LLM,
            actor_id="user-1",
            correlation_id="c01",
        )
        assert c.field_name == "city"
        assert c.proposed_value == "Douala"
        assert c.confidence == 0.9
        assert c.source_type == ExtractionMethod.LLM

    def test_candidate_frozen(self):
        c = CandidateUpdate(field_name="city", raw_value="Douala")
        with pytest.raises(AttributeError):
            c.field_name = "other"

    def test_extraction_methods(self):
        c1 = CandidateUpdate(field_name="a", proposed_value=1, source_type=ExtractionMethod.DETERMINISTIC)
        c2 = CandidateUpdate(field_name="b", proposed_value=2, source_type=ExtractionMethod.RULE_BASED)
        c3 = CandidateUpdate(field_name="c", proposed_value=3, source_type=ExtractionMethod.USER_CONFIRMED)
        assert c1.source_type == ExtractionMethod.DETERMINISTIC
        assert c2.source_type == ExtractionMethod.RULE_BASED
        assert c3.source_type == ExtractionMethod.USER_CONFIRMED

    def test_candidate_defaults(self):
        c = CandidateUpdate(field_name="price", proposed_value=100000)
        assert c.confidence == 1.0
        assert c.source_type == ExtractionMethod.DETERMINISTIC
        assert c.candidate_id is not None
        assert len(c.candidate_id) == 16
