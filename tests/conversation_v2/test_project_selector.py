from __future__ import annotations

import unittest

from lawim_v2.conversation.planning.project_selector import resolve_project_selection, ProjectSelectionResult


class TestProjectSelectorZeroProjects(unittest.TestCase):
    def test_zero_projects_returns_request_new(self):
        result = resolve_project_selection("bonjour", [])
        self.assertEqual(result.action, "request_new")
        self.assertIsNotNone(result.reply_text)

    def test_zero_projects_no_ambiguity(self):
        result = resolve_project_selection("ok", [])
        self.assertEqual(result.action, "request_new")

    def test_zero_projects_no_clarification_needed(self):
        result = resolve_project_selection("Je cherche un appartement", [])
        self.assertFalse(result.requires_clarification)


class TestProjectSelectorOneProject(unittest.TestCase):
    def setUp(self):
        self.projects = [{"id": 1, "title": "Recherche appartement Douala", "status": "ACTIVE"}]

    def test_one_project_no_context(self):
        result = resolve_project_selection("Je cherche un appartement", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)
        self.assertTrue(result.requires_confirmation)

    def test_one_project_same_id_context(self):
        result = resolve_project_selection("Je cherche un appartement", self.projects, conversation_project_id=1)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)
        self.assertFalse(result.requires_confirmation)

    def test_one_project_ambiguous_ok_auto_selects(self):
        result = resolve_project_selection("ok", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)
        self.assertTrue(result.requires_confirmation)

    def test_one_project_oui_auto_selects(self):
        result = resolve_project_selection("oui", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)

    def test_one_project_exact_name_match(self):
        result = resolve_project_selection("Recherche appartement Douala", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)
        self.assertTrue(result.requires_confirmation)

    def test_one_project_partial_match(self):
        result = resolve_project_selection("appartement", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)

    def test_one_project_unknown_message(self):
        result = resolve_project_selection("xyz", self.projects)
        self.assertEqual(result.action, "select_existing")


class TestProjectSelectorMultipleProjects(unittest.TestCase):
    def setUp(self):
        self.projects = [
            {"id": 1, "title": "Recherche appartement Douala", "status": "ACTIVE"},
            {"id": 2, "title": "Achat maison Yaoundé", "status": "ACTIVE"},
        ]

    def test_multiple_projects_no_context(self):
        result = resolve_project_selection("Bonjour", self.projects)
        self.assertEqual(result.action, "list_projects")
        self.assertTrue(result.requires_clarification)
        self.assertIsNotNone(result.alternatives)
        self.assertEqual(len(result.alternatives), 2)

    def test_multiple_projects_ambiguous(self):
        result = resolve_project_selection("ok", self.projects)
        self.assertEqual(result.action, "ambiguous")
        self.assertTrue(result.requires_clarification)

    def test_multiple_projects_exact_match(self):
        result = resolve_project_selection("Recherche appartement Douala", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)

    def test_multiple_projects_exact_match_second(self):
        result = resolve_project_selection("Achat maison Yaoundé", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 2)

    def test_multiple_projects_partial_match(self):
        result = resolve_project_selection("Douala", self.projects)
        self.assertEqual(result.action, "select_existing")
        self.assertEqual(result.project_id, 1)
        self.assertFalse(result.requires_confirmation)

    def test_multiple_projects_with_existing_context(self):
        result = resolve_project_selection("Bonjour", self.projects, conversation_project_id=1)
        self.assertEqual(result.action, "none")
        self.assertTrue(result.requires_clarification)

    def test_multiple_projects_no_match(self):
        result = resolve_project_selection("xylophone", self.projects)
        self.assertEqual(result.action, "list_projects")
        self.assertTrue(result.requires_clarification)


class TestProjectSelectionResult(unittest.TestCase):
    def test_result_defaults(self):
        r = ProjectSelectionResult(action="none")
        self.assertEqual(r.action, "none")
        self.assertIsNone(r.project_id)
        self.assertFalse(r.requires_confirmation)
        self.assertFalse(r.requires_clarification)
        self.assertFalse(r.requires_human)
        self.assertEqual(r.alternatives, [])
        self.assertIsNone(r.reply_text)

    def test_result_with_alternatives(self):
        r = ProjectSelectionResult(
            action="list_projects",
            requires_clarification=True,
            alternatives=[{"id": 1, "title": "Test"}],
            reply_text="Choisissez un projet",
        )
        self.assertEqual(len(r.alternatives), 1)
        self.assertEqual(r.reply_text, "Choisissez un projet")

    def test_ambiguous_result_has_no_single_project(self):
        r = ProjectSelectionResult(action="ambiguous")
        self.assertIsNone(r.project_id)

    def test_request_new_result(self):
        r = ProjectSelectionResult(action="request_new")
        self.assertFalse(r.requires_clarification)


if __name__ == "__main__":
    unittest.main()
