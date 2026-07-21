"""Test LawimCase lifecycle: creation, linking, suspension, closing, archiving."""

from __future__ import annotations

import sqlite3
import unittest

from lawim_v2.conversation.domain.case import CaseStatus, LawimCase
from lawim_v2.conversation.case.repository import LawimCaseRepository
from lawim_v2.conversation.case.service import LawimCaseService
from lawim_v2.conversation.case.resolver import ActiveCaseResolver


class TestLawimCaseContinuity(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        self.repo = LawimCaseRepository(self.conn)
        self.service = LawimCaseService(self.repo)
        self.resolver = ActiveCaseResolver(self.repo, self.service)

    def tearDown(self):
        self.conn.close()

    def _make_active_case(self, **kw) -> LawimCase:
        defaults = dict(
            case_type="RENT",
            primary_actor_id="actor_1",
            active_intent="rental_search",
            journey_code="rent",
        )
        defaults.update(kw)
        case = self.service.create_case(**defaults)
        case.status = CaseStatus.ACTIVE
        return self.service.update_case(case)

    def test_create_case(self):
        case = self.service.create_case(
            case_type="RENT",
            primary_actor_id="actor_1",
            title="Recherche appartement Douala",
            active_intent="rental_search",
            journey_code="rent",
        )
        self.assertTrue(len(case.case_id) > 0)
        self.assertTrue(case.case_code.startswith("CS-"))
        self.assertEqual(case.status, CaseStatus.DRAFT)
        self.assertEqual(case.active_intent, "rental_search")
        self.assertEqual(case.primary_actor_id, "actor_1")

    def test_create_case_idempotent(self):
        c1 = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        c2 = self.service.resolve_or_create(
            actor_id="actor_1", case_type="RENT",
            active_intent="rental_search",
        )
        self.assertEqual(c1.case_id, c2.case_id)

    def test_load_case(self):
        created = self.service.create_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        loaded = self.service.get_case(created.case_id)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded.case_id, created.case_id)

    def test_update_case(self):
        case = self.service.create_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        case.title = "Updated title"
        case.active_intent = "buy_search"
        updated = self.service.update_case(case)
        self.assertEqual(updated.title, "Updated title")
        self.assertEqual(updated.active_intent, "buy_search")

    def test_link_case_conversation(self):
        case = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        link = self.service.link_conversation(
            case_id=case.case_id,
            conversation_id="conv_1",
            channel="whatsapp",
            actor_id="actor_1",
        )
        self.assertEqual(link.case_id, case.case_id)
        self.assertEqual(link.conversation_id, "conv_1")
        self.assertTrue(link.is_active)

        loaded = self.service.get_case(case.case_id)
        self.assertEqual(loaded.active_conversation_id, "conv_1")

    def test_unlink_case_conversation(self):
        case = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        self.service.link_conversation(
            case_id=case.case_id, conversation_id="conv_1",
            channel="whatsapp", actor_id="actor_1",
        )
        self.service.unlink_conversation(case.case_id, "conv_1")
        loaded = self.service.get_case(case.case_id)
        self.assertIsNone(loaded.active_conversation_id)

    def test_multiple_cases_per_actor(self):
        self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        self._make_active_case(
            case_type="BUY", primary_actor_id="actor_1",
            active_intent="buy_search",
        )
        cases = self.service.get_active_cases("actor_1")
        self.assertEqual(len(cases), 2)

    def test_active_case_resolver_by_id(self):
        case = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        resolved = self.resolver.resolve(case_id=case.case_id)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.case_id, case.case_id)

    def test_active_case_resolver_by_conversation(self):
        case = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        self.service.link_conversation(
            case_id=case.case_id, conversation_id="conv_1",
            channel="whatsapp", actor_id="actor_1",
        )
        resolved = self.resolver.resolve(conversation_id="conv_1")
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.case_id, case.case_id)

    def test_active_case_resolver_multiple_active(self):
        self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        self._make_active_case(
            case_type="BUY", primary_actor_id="actor_1",
            active_intent="buy_search",
        )
        resolved = self.resolver.resolve(actor_id="actor_1")
        self.assertIsNone(resolved)
        self.assertTrue(self.resolver.multiple_active)

    def test_active_case_resolver_new_case(self):
        resolved = self.resolver.resolve(
            actor_id="new_actor",
            intent="rental_search",
        )
        self.assertIsNone(resolved)
        self.assertFalse(self.resolver.multiple_active)

    def test_case_suspend_resume(self):
        case = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        case.status = CaseStatus.SUSPENDED
        self.service.update_case(case)
        loaded = self.service.get_case(case.case_id)
        self.assertEqual(loaded.status, CaseStatus.SUSPENDED)
        self.assertFalse(loaded.is_active())

        case.status = CaseStatus.ACTIVE
        self.service.update_case(case)
        loaded = self.service.get_case(case.case_id)
        self.assertTrue(loaded.is_active())

    def test_case_close_archive(self):
        case = self._make_active_case(
            case_type="RENT", primary_actor_id="actor_1",
            active_intent="rental_search",
        )
        closed = self.service.close_case(case.case_id)
        self.assertIsNotNone(closed)
        self.assertEqual(closed.status, CaseStatus.COMPLETED)
        self.assertIsNotNone(closed.closed_at)

        archived = self.service.archive_case(case.case_id)
        self.assertIsNotNone(archived)
        self.assertEqual(archived.status, CaseStatus.ARCHIVED)


class TestCaseStatusTransitions(unittest.TestCase):
    def test_active_statuses(self):
        for status in (
            CaseStatus.DRAFT, CaseStatus.ACTIVE, CaseStatus.WAITING_USER,
            CaseStatus.WAITING_LAWIM, CaseStatus.READY, CaseStatus.IN_PROGRESS,
        ):
            case = LawimCase(status=status)
            if status == CaseStatus.DRAFT:
                self.assertFalse(case.is_active())
            else:
                self.assertTrue(case.is_active())

    def test_terminal_statuses_not_active(self):
        for status in (CaseStatus.COMPLETED, CaseStatus.CANCELLED, CaseStatus.ARCHIVED):
            case = LawimCase(status=status)
            self.assertFalse(case.is_active())


if __name__ == "__main__":
    unittest.main()
