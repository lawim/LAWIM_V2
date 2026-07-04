from __future__ import annotations

import unittest

from lawim_v2.conversation_registry import (
    ConversationArchiveManager,
    ConversationArchiveManifest,
    ConversationLifecycleEngine,
    ConversationRegistry,
    ConversationRestoreEngine,
    ConversationStorageProvider,
    OVHStorageOptimizer,
    StorageOrchestrator,
)


class ConversationRegistryAACCTest(unittest.TestCase):
    def test_conversation_registry_deduplicates_by_conversation_key(self) -> None:
        registry = ConversationRegistry()
        first = registry.create_conversation(
            conversation_key="deal-42",
            subject="Villa Marseille",
            participant_ids=["client-1", "agent-1"],
            media_ids=[101],
        )
        second = registry.create_conversation(
            conversation_key="deal-42",
            subject="Villa Marseille",
            participant_ids=["client-1", "agent-1"],
            media_ids=[101],
        )

        self.assertEqual(first["conversation_id"], second["conversation_id"])
        self.assertEqual(len(registry.list_conversations()), 1)
        self.assertEqual(len(registry.list_participants(first["conversation_id"])), 2)

    def test_archive_manager_builds_structured_manifest_with_media_ids(self) -> None:
        registry = ConversationRegistry()
        conversation = registry.create_conversation(
            conversation_key="deal-99",
            subject="Archive test",
            participant_ids=["client-2"],
            media_ids=[77],
        )
        registry.add_message(conversation_id=conversation["conversation_id"], author_id="client-2", body="hello")

        archive_manager = ConversationArchiveManager()
        manifest = archive_manager.build_manifest(
            conversation_id=conversation["conversation_id"],
            media_ids=[77],
            checksum="abc123",
        )

        self.assertIsInstance(manifest, ConversationArchiveManifest)
        self.assertEqual(manifest.media_ids, [77])
        self.assertIn("participants", manifest.payload)
        self.assertNotIn("drive.google.com", str(manifest.payload))

    def test_conversation_restore_and_storage_provider_use_safe_access(self) -> None:
        provider = ConversationStorageProvider(name="drive-8", kind="conversation-archive")
        restore_engine = ConversationRestoreEngine()
        access = provider.resolve_access(conversation_id=12, kind="conversation_archive")
        restore_plan = restore_engine.build_restore_plan(conversation_id=12, reason="policy")

        self.assertEqual(access["provider"], "drive-8")
        self.assertEqual(restore_plan["conversation_id"], 12)
        self.assertNotIn("drive.google.com", access["temporary_access_url"])
        self.assertNotIn("drive.google.com", str(restore_plan))

    def test_ovh_optimizer_and_lifecycle_engine_are_mock_ready(self) -> None:
        optimizer = OVHStorageOptimizer()
        engine = ConversationLifecycleEngine()
        plan = optimizer.plan(conversation_id=5, kind="conversation_archive")
        lifecycle = engine.transition("active", "archived")

        self.assertEqual(plan["drive_target"], "drive-8")
        self.assertEqual(lifecycle, "archived")
        self.assertEqual(engine.backup_state_for("archived"), "archived")


if __name__ == "__main__":
    unittest.main()
