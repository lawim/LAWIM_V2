from __future__ import annotations

import json
import unittest

from lawim_v2 import StorageResourceRegistry
from lawim_v2.storage_platform import LocalStorageProvider, StorageOrchestrator, StorageOrchestratorPolicy


class StorageRoutingAAFTest(unittest.TestCase):
    def test_route_map_covers_official_routes(self) -> None:
        registry = StorageResourceRegistry.default()

        self.assertEqual(registry.route_for("video"), ("drive-1", "drive-2", "drive-8"))
        self.assertEqual(registry.route_for("photo"), ("drive-3", "drive-8"))
        self.assertEqual(registry.route_for("audio"), ("drive-3", "drive-8"))
        self.assertEqual(registry.route_for("document"), ("drive-4", "drive-8"))
        self.assertEqual(registry.route_for("conversation archive"), ("drive-5", "drive-8"))
        self.assertEqual(registry.route_for("export/rapport"), ("drive-6", "drive-8"))
        self.assertEqual(registry.route_for("backup applicatif"), ("drive-7", "drive-10"))
        self.assertEqual(registry.route_for("critical replication"), ("drive-8", "drive-10"))
        self.assertEqual(registry.route_for("reserve"), ("drive-9",))
        self.assertEqual(registry.route_for("maintenance/migration"), ("drive-10",))

    def test_registry_selects_expected_drives_for_content_classes(self) -> None:
        registry = StorageResourceRegistry.default()

        self.assertEqual(registry.select(category="video").drive_id, "drive-1")
        self.assertEqual(registry.select(category="photo").drive_id, "drive-3")
        self.assertEqual(registry.select(category="audio").drive_id, "drive-3")
        self.assertEqual(registry.select(category="document").drive_id, "drive-4")
        self.assertEqual(registry.select(category="conversation archive").drive_id, "drive-5")
        self.assertEqual(registry.select(category="backup applicatif").drive_id, "drive-7")
        self.assertEqual(registry.select(category="export rapport").drive_id, "drive-6")
        self.assertEqual(registry.select(category="maintenance migration").drive_id, "drive-10")
        self.assertEqual(registry.select(category="replication critique").drive_id, "drive-10")

    def test_orchestrator_responses_remain_google_url_free(self) -> None:
        orchestrator = StorageOrchestrator(
            providers=[LocalStorageProvider()],
            policy=StorageOrchestratorPolicy(default_provider="local"),
            resource_registry=StorageResourceRegistry.default(),
        )

        media_access = orchestrator.resolve_media_access(media_id=42, kind="video")
        conversation_access = orchestrator.resolve_conversation_archive_access(conversation_id=7)
        snapshot = orchestrator.resource_snapshot()

        self.assertEqual(media_access["routing"]["route"], ["drive-1", "drive-2", "drive-8"])
        self.assertEqual(media_access["storage_resource"]["drive_id"], "drive-1")
        self.assertEqual(conversation_access["provider"], "drive-5")
        self.assertEqual(conversation_access["routing"]["route"], ["drive-5", "drive-8"])
        self.assertNotIn("drive.google.com", json.dumps(media_access))
        self.assertNotIn("drive.google.com", json.dumps(conversation_access))
        self.assertNotIn("drive.google.com", json.dumps(snapshot))


if __name__ == "__main__":
    unittest.main()
