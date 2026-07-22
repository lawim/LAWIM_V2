from __future__ import annotations

from lawim_runtime.project_profile.adapters.conversation_adapter import ConversationStateToProfileAdapter
from lawim_runtime.project_profile.adapters.wizard_adapter import WizardAnswersToProfilePatchAdapter
from lawim_runtime.project_profile.values import ExtractionMethod


class TestConversationAdapter:
    def test_conversation_slots_to_candidates(self):
        adapter = ConversationStateToProfileAdapter()
        slots = {"city": "Douala", "budget_max": 200000, "bedrooms": 2}
        candidates = adapter.to_candidates(slots, actor_id="user-1", correlation_id="c01")
        assert len(candidates) == 3
        names = {c.field_name for c in candidates}
        assert names == {"city", "budget_max", "bedrooms"}

    def test_conversation_slots_to_patch(self):
        adapter = ConversationStateToProfileAdapter()
        slots = {"city": "Douala", "budget_max": 200000}
        patch = adapter.to_patch(slots, project_id="p1", profile_id="pr1", base_version=1)
        assert patch.project_id == "p1"
        assert patch.profile_id == "pr1"
        assert patch.base_version == 1
        assert len(patch.updates) == 2
        assert patch.source == "conversation_engine"

    def test_wizard_answers_to_candidates(self):
        adapter = WizardAnswersToProfilePatchAdapter()
        answers = {"property_type": "APARTMENT", "bedrooms": 3, "furnished": True}
        candidates = adapter.to_candidates(answers, correlation_id="c02")
        assert len(candidates) == 3
        for c in candidates:
            assert c.source_type == ExtractionMethod.RULE_BASED
