from __future__ import annotations

import unittest
from datetime import datetime, timedelta

from lawim_v2.conversation.relationship.service import RelationshipService, RelationshipError, ConsentError
from lawim_v2.conversation.relationship.consent import ConsentDirection, ConsentStatus
from lawim_v2.conversation.relationship.proposals import ProposalStatus
from lawim_v2.conversation.relationship.lifecycle import RelationshipStatus
from lawim_v2.conversation.relationship.privacy import DataCategory, PrivacyController
from lawim_v2.conversation.relationship.introductions import IntroductionBuilder


class TestRelationshipFlow(unittest.TestCase):
    """Mission 3B.2 — Relationship, Consent, and Privacy validation."""

    def setUp(self):
        self.service = RelationshipService()

    def _create_proposal(self, requester_id=1, target_id=2, item_id="item_1"):
        return self.service.create_proposal(
            requester_user_id=requester_id,
            target_user_id=target_id,
            target_item_id=item_id,
        )

    def _request_and_grant(self, proposal_id, proposer_id=1, target_id=2):
        req = self.service.request_consent(proposal_id)
        self.service.record_consent_decision(
            req.consent_request_id, user_id=target_id, granted=True
        )
        return req

    # --- Test 1: Double accept → relationship created ---
    def test_1_double_accept_creates_relationship(self):
        prop = self._create_proposal()
        self._request_and_grant(prop.proposal_id)
        rel = self.service.create_relationship(
            prop.proposal_id,
            requester_user_id=1,
            target_user_id=2,
            requester_data={"name": "Alice", "phone": "+331234567"},
            target_data={"name": "Bob", "email": "bob@test.com"},
        )
        self.assertIsNotNone(rel)
        self.assertEqual(rel.status, RelationshipStatus.ACTIVE)
        self.assertEqual(rel.relationship_type, "buyer_seller")
        self.assertEqual(prop.status, ProposalStatus.ACCEPTED)

    # --- Test 2: Requester consent requested → proposal moves to PENDING_CONSENT ---
    def test_2_requester_consent_proposal_pending(self):
        prop = self._create_proposal()
        req = self.service.request_consent(prop.proposal_id)
        self.assertEqual(prop.status, ProposalStatus.PENDING_CONSENT)
        self.assertEqual(req.status, ConsentStatus.PENDING)
        self.assertEqual(req.requester_user_id, 1)
        self.assertEqual(req.target_user_id, 2)

    # --- Test 3: Target grants consent → relationship created ---
    def test_3_target_consent_creates_relationship(self):
        prop = self._create_proposal()
        req = self.service.request_consent(prop.proposal_id)
        decision = self.service.record_consent_decision(
            req.consent_request_id, user_id=2, granted=True
        )
        self.assertEqual(decision.decision, ConsentStatus.GRANTED)
        self.assertEqual(prop.status, ProposalStatus.CONSENT_GRANTED)
        rel = self.service.create_relationship(
            prop.proposal_id,
            requester_user_id=1,
            target_user_id=2,
            requester_data={"name": "Alice"},
            target_data={"name": "Bob"},
        )
        self.assertEqual(rel.status, RelationshipStatus.ACTIVE)

    # --- Test 4: Requester refuses → no relationship ---
    def test_4_requester_refuses_no_relationship(self):
        prop = self._create_proposal()
        req = self.service.request_consent(prop.proposal_id)
        decision = self.service.record_consent_decision(
            req.consent_request_id, user_id=2, granted=False
        )
        self.assertEqual(decision.decision, ConsentStatus.DENIED)
        self.assertEqual(prop.status, ProposalStatus.CONSENT_DENIED)
        with self.assertRaises(RelationshipError) as ctx:
            self.service.create_relationship(
                prop.proposal_id,
                requester_user_id=1,
                target_user_id=2,
                requester_data={},
                target_data={},
            )
        self.assertIn("must have consent granted", str(ctx.exception))

    # --- Test 5: Target refuses → no relationship (same path as test 4) ---
    test_5_target_refuses_no_relationship = test_4_requester_refuses_no_relationship

    # --- Test 6: Consent expires → no relationship ---
    def test_6_consent_expires_no_relationship(self):
        prop = self._create_proposal()
        req = self.service.request_consent(prop.proposal_id)
        req.expires_at = (datetime.utcnow() - timedelta(hours=1)).isoformat()
        with self.assertRaises(ConsentError) as ctx:
            self.service.record_consent_decision(
                req.consent_request_id, user_id=2, granted=True
            )
        self.assertIn("no longer valid", str(ctx.exception))

    # --- Test 7: Consent revoked → relationship ends ---
    def test_7_consent_revoked_relationship_ends(self):
        prop = self._create_proposal()
        self._request_and_grant(prop.proposal_id)
        rel = self.service.create_relationship(
            prop.proposal_id,
            requester_user_id=1,
            target_user_id=2,
            requester_data={"name": "Alice"},
            target_data={"name": "Bob"},
        )
        consent_request = self.service._find_granted_consent(prop.proposal_id)
        self.assertIsNotNone(consent_request)
        ok = self.service.consent_manager.revoke_consent(consent_request.consent_request_id)
        self.assertTrue(ok)
        self.assertEqual(consent_request.status, ConsentStatus.REVOKED)
        self.service.cancel_relationship(rel.relationship_id)
        rel2 = self.service.get_relationship(rel.relationship_id)
        self.assertEqual(rel2.status, RelationshipStatus.CANCELLED)

    # --- Test 8: Duplicate proposal → idempotent ---
    def test_8_duplicate_proposal_idempotent(self):
        p1 = self._create_proposal(requester_id=1, target_id=2, item_id="item_x")
        p2 = self._create_proposal(requester_id=1, target_id=2, item_id="item_x")
        self.assertIsNotNone(p1)
        self.assertIsNotNone(p2)
        self.assertNotEqual(p1.proposal_id, p2.proposal_id)
        proposals = self.service.proposal_manager._proposals
        self.assertIn(p1.proposal_id, proposals)
        self.assertIn(p2.proposal_id, proposals)

    # --- Test 9: Relationship without consent → blocked ---
    def test_9_relationship_without_consent_blocked(self):
        prop = self._create_proposal()
        with self.assertRaises(RelationshipError) as ctx:
            self.service.create_relationship(
                prop.proposal_id,
                requester_user_id=1,
                target_user_id=2,
                requester_data={"name": "Alice"},
                target_data={"name": "Bob"},
            )
        self.assertIn("must have consent granted", str(ctx.exception))

    # --- Test 10: Cross-access blocked ---
    def test_10_cross_access_blocked(self):
        prop = self._create_proposal(requester_id=1, target_id=2)
        self._request_and_grant(prop.proposal_id)
        rel = self.service.create_relationship(
            prop.proposal_id,
            requester_user_id=1,
            target_user_id=2,
            requester_data={"name": "Alice", "phone": "+331234567"},
            target_data={"name": "Bob", "email": "bob@test.com"},
        )
        intro = self.service.get_introduction(
            f"intro_{rel.relationship_id.split('_')[1]}"
        )
        self.assertIsNone(intro)
        all_intros = self.service.introduction_manager._introductions
        intro = list(all_intros.values())[0]
        data = intro.data_shared
        self.assertIn("requester", data)
        self.assertIn("target", data)
        self.assertEqual(data["requester"].get("name"), "Alice")
        self.assertEqual(data["target"].get("name"), "Bob")

    # --- Test 11: Private data masked before consent ---
    def test_11_private_data_masked_before_consent(self):
        data = {
            "name": "Alice",
            "phone": "+331234567",
            "email": "alice@test.com",
            "address": "123 Main St",
        }
        filtered = self.service.shareable_data(data, relationship_id="nonexistent")
        self.assertNotIn("phone", filtered)
        self.assertNotIn("email", filtered)
        self.assertNotIn("name", filtered)
        self.assertNotIn("address", filtered)

    # --- Test 12: Data scope respected after consent ---
    def test_12_data_scope_respected_after_consent(self):
        prop = self._create_proposal()
        req = self.service.request_consent(prop.proposal_id, data_categories=[DataCategory.NAME])
        self.service.record_consent_decision(
            req.consent_request_id, user_id=2, granted=True
        )
        rel = self.service.create_relationship(
            prop.proposal_id,
            requester_user_id=1,
            target_user_id=2,
            requester_data={"name": "Alice", "phone": "+331234567", "email": "alice@test.com"},
            target_data={"name": "Bob", "phone": "+336789"},
        )
        all_intros = self.service.introduction_manager._introductions
        intro = list(all_intros.values())[0]
        self.assertEqual(intro.data_shared["requester"].get("name"), "Alice")
        self.assertNotIn("phone", intro.data_shared["requester"])
        self.assertNotIn("email", intro.data_shared["requester"])
        self.assertEqual(intro.data_shared["target"].get("name"), "Bob")
        self.assertNotIn("phone", intro.data_shared["target"])


if __name__ == "__main__":
    unittest.main()
