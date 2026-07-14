from __future__ import annotations

from http import HTTPStatus
from pathlib import Path

from lawim_v2.maintenance import MAINTENANCE_RESPONSE

from .lawim_harness import LawimTestHarness


class Mission2MaintenanceDecommissioningTests(LawimTestHarness):
    def test_legacy_domain_modules_are_absent(self) -> None:
        root = Path(__file__).resolve().parents[1] / "code" / "lawim_v2"
        removed_paths = (
            root / "conversation_core",
            root / "assistant",
            root / "brain",
            root / "matching.py",
            root / "persona.py",
            root / "ai" / "fallback.py",
            root / "ai" / "providers" / "internal_fallback.py",
        )
        for path in removed_paths:
            with self.subTest(path=str(path)):
                self.assertFalse(path.exists())

    def test_legacy_routes_are_not_available(self) -> None:
        token = self.login(email="agent@lawim.local")
        legacy_routes = (
            "/api/matches?city=Douala",
            "/api/v2/assistant/agents",
            "/api/v2/assistant/chat",
            "/api/v2/assistant/brain/matching",
            "/api/v2/matching?project_id=1",
            "/api/v2/properties/matching",
        )
        for route in legacy_routes:
            with self.subTest(route=route):
                method = "POST" if route in {"/api/v2/assistant/chat", "/api/v2/assistant/brain/matching", "/api/v2/properties/matching"} else "GET"
                response = self.invoke(route, method=method, token=token, body={"message": "Bonjour", "project_id": 1})
                self.assertEqual(response.status, HTTPStatus.NOT_FOUND)

    def test_maintenance_message_is_persisted_without_automation(self) -> None:
        token = self.login(email="agent@lawim.local")
        projects_before = self.repository.scalar("SELECT COUNT(*) FROM projects")
        response = self.invoke(
            "/api/v2/maintenance/messages",
            method="POST",
            token=token,
            body={"channel": "web", "message": "Je cherche un studio", "handover_requested": True},
        )
        self.assertEqual(response.status, HTTPStatus.CREATED)
        payload = response.body_json()
        self.assertEqual(payload["response"], MAINTENANCE_RESPONSE)
        self.assertEqual(payload["automated_processing"], "blocked")
        self.assertTrue(payload["handover_requested"])
        rows = self.repository.list_maintenance_messages(channel="web", handover_requested=True)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["raw_message"], "Je cherche un studio")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM projects"), projects_before)

    def test_maintenance_status_flags_are_locked(self) -> None:
        response = self.invoke("/api/v2/maintenance/status")
        self.assertEqual(response.status, HTTPStatus.OK)
        payload = response.body_json()
        self.assertTrue(payload["maintenance_mode"])
        self.assertTrue(payload["flags"]["lawim_core_rebuild_maintenance_mode"])
        self.assertFalse(payload["flags"]["conversation_service_enabled"])
        self.assertFalse(payload["flags"]["matching_service_enabled"])
        self.assertFalse(payload["flags"]["relationship_service_enabled"])
