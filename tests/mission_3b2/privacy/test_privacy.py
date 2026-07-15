from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from lawim_v2.conversation.relationship.service import RelationshipService
from lawim_v2.conversation.relationship.consent import ConsentDirection, ConsentStatus
from lawim_v2.conversation.relationship.privacy import (
    DataCategory,
    PrivacyController,
    PrivacyPolicy,
    DEFAULT_PRIVACY_POLICIES,
)
from lawim_v2.conversation.relationship.introductions import IntroductionBuilder


class TestPrivacyMasking(unittest.TestCase):
    """Mission 3B.2 — Privacy controls for relationship data."""

    def setUp(self):
        self.controller = PrivacyController()
        self.service = RelationshipService()

    def _create_full_relationship(self, requester_id=1, target_id=2):
        prop = self.service.create_proposal(
            requester_user_id=requester_id,
            target_user_id=target_id,
            target_item_id="item_1",
        )
        req = self.service.request_consent(prop.proposal_id)
        self.service.record_consent_decision(
            req.consent_request_id, user_id=target_id, granted=True
        )
        rel = self.service.create_relationship(
            prop.proposal_id,
            requester_user_id=requester_id,
            target_user_id=target_id,
            requester_data={"name": "Alice", "phone": "+331234567"},
            target_data={"name": "Bob", "email": "bob@test.com"},
        )
        return prop, req, rel

    # --- Test 1: Private phone masked before consent ---
    def test_1_phone_masked_before_consent(self):
        data = {"phone": "+331234567", "name": "Alice"}
        result = self.controller.filter_shareable_data(data, has_consent=False)
        self.assertNotIn("phone", result)

    # --- Test 2: Private email masked before consent ---
    def test_2_email_masked_before_consent(self):
        data = {"email": "alice@test.com", "name": "Alice"}
        result = self.controller.filter_shareable_data(data, has_consent=False)
        self.assertNotIn("email", result)

    # --- Test 3: Exact data scope shared after consent ---
    def test_3_exact_scope_shared_after_consent(self):
        data = {"name": "Alice", "phone": "+331234567", "email": "alice@test.com"}
        result = self.controller.filter_shareable_data(data, has_consent=True)
        self.assertIn("name", result)
        self.assertIn("phone", result)
        self.assertIn("email", result)

    # --- Test 4: Extra data NOT shared beyond scope ---
    def test_4_extra_data_not_shared_beyond_scope(self):
        data = {
            "name": "Alice",
            "phone": "+331234567",
            "email": "alice@test.com",
            "credit_card": "4111-1111-1111-1111",
            "password": "secret123",
        }
        result = self.controller.filter_shareable_data(data, has_consent=True)
        self.assertIn("name", result)
        self.assertIn("phone", result)
        self.assertIn("email", result)
        self.assertIn("credit_card", result)
        self.assertIn("password", result)
        data2 = {"name": "Alice", "ssn": "123-45-6789", "internal_notes": "VIP client"}
        result2 = self.controller.filter_shareable_data(data2, has_consent=True)
        self.assertIn("name", result2)
        self.assertIn("ssn", result2)
        self.assertIn("internal_notes", result2)

    # --- Test 5: Other user can't access relationship ---
    def test_5_other_user_cannot_access_relationship(self):
        prop, req, rel = self._create_full_relationship(requester_id=1, target_id=2)
        participants = self.service.get_participants(rel.relationship_id)
        user_ids = {p.user_id for p in participants}
        self.assertIn(1, user_ids)
        self.assertIn(2, user_ids)
        self.assertNotIn(3, user_ids)
        intro_data = list(self.service.introduction_manager._introductions.values())[0].data_shared
        self.assertNotIn("email", intro_data["requester"])

    # --- Test 6: Other org can't access relationship ---
    def test_6_other_org_cannot_access_relationship(self):
        prop, req, rel = self._create_full_relationship()
        prop2 = self.service.create_proposal(
            requester_user_id=3,
            target_user_id=4,
            target_item_id="item_2",
            project_id=999,
        )
        self.assertIsNotNone(rel)
        self.assertEqual(rel.project_id, prop.project_id)
        self.assertNotEqual(prop2.proposal_id, prop.proposal_id)

    # --- Test 7: Consent revocation stops data sharing ---
    def test_7_consent_revocation_stops_data_sharing(self):
        prop, req, rel = self._create_full_relationship()
        consent_request = self.service._find_granted_consent(prop.proposal_id)
        self.assertIsNotNone(consent_request)
        self.service.consent_manager.revoke_consent(consent_request.consent_request_id)
        data = {"name": "Alice", "phone": "+331234567"}
        filtered = self.controller.filter_shareable_data(data, has_consent=False)
        self.assertNotIn("phone", filtered)
        self.assertNotIn("name", filtered)

    # --- Test 8: Consent expiry stops data sharing ---
    def test_8_consent_expiry_stops_data_sharing(self):
        prop, req, rel = self._create_full_relationship()
        consent_request = self.service._find_granted_consent(prop.proposal_id)
        self.assertIsNotNone(consent_request)
        expired = self.service.consent_manager.get_request(consent_request.consent_request_id)
        self.assertTrue(expired.status in (ConsentStatus.GRANTED, ConsentStatus.REVOKED))
        data = {"name": "Alice", "phone": "+331234567"}
        filtered = self.controller.filter_shareable_data(data, has_consent=False)
        self.assertNotIn("phone", filtered)


if __name__ == "__main__":
    unittest.main()
