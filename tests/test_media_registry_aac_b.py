from __future__ import annotations

from http import HTTPStatus
from pathlib import Path

from lawim_v2.db import LawimRepository
from lawim_v2.dto import media_dto
from lawim_v2.errors import ValidationError
from lawim_v2.media_domain import LocalMediaStorage
from lawim_v2.services import LawimServices
from tests.lawim_harness import LawimTestHarness, MINIMAL_JPEG_BYTES


class MediaRegistryAACBTest(LawimTestHarness):
    def _create_property(self) -> int:
        row = self.repository.create_property(
            title="AAC-B Property",
            summary="Compatibility regression property",
            city="Douala",
            country="Cameroon",
            status="draft",
            property_type="apartment",
        )
        return int(row["id"])

    def test_media_rows_default_to_local_provider_metadata(self) -> None:
        property_id = self._create_property()
        media_row = self.repository.create_media(
            property_id=property_id,
            kind="image",
            url="https://example.test/photo.jpg",
            caption="Legacy media",
        )

        self.assertEqual(media_row["provider_name"], "local")
        self.assertIsNone(media_row["provider_object_id"])
        self.assertEqual(media_row["lifecycle_state"], "active")
        self.assertEqual(media_row["backup_state"], "available")

    def test_legacy_media_rows_without_provider_columns_still_load(self) -> None:
        property_id = self._create_property()
        with self.repository._transaction() as conn:
            conn.execute(
                """
                INSERT INTO media (
                    property_id, kind, url, caption, metadata_json, position, version, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    property_id,
                    "image",
                    "https://example.test/legacy.jpg",
                    "Legacy",
                    "{}",
                    0,
                    1,
                    "2024-01-01T00:00:00+00:00",
                ),
            )
        media_row = self.repository.one(
            "SELECT id FROM media WHERE property_id = ? AND url = ? ORDER BY id DESC LIMIT 1",
            (property_id, "https://example.test/legacy.jpg"),
        )
        self.assertIsNotNone(media_row)
        media_id = int(media_row["id"])
        media_row = self.repository.get_media(media_id)

        self.assertEqual(media_row["provider_name"], "local")
        self.assertIsNone(media_row["provider_object_id"])
        self.assertEqual(media_row["lifecycle_state"], "active")
        self.assertEqual(media_row["backup_state"], "available")

    def test_local_media_storage_remains_the_default_provider(self) -> None:
        services = LawimServices(self.repository, self.config)
        self.assertEqual(services.storage_orchestrator.default_provider, "local")
        self.assertEqual(services.storage_orchestrator.registry.get("local").name, "local")
        self.assertIsInstance(services.storage_orchestrator.registry.get("local"), LocalMediaStorage)

    def test_google_drive_urls_are_rejected_for_media_storage(self) -> None:
        property_id = self._create_property()
        with self.assertRaises(ValidationError):
            self.repository.create_media(
                property_id=property_id,
                kind="image",
                url="https://drive.google.com/file/d/abc123/view",
                caption="Google Drive asset",
            )

    def test_media_dto_exposes_provider_metadata(self) -> None:
        property_id = self._create_property()
        media_row = self.repository.create_media(
            property_id=property_id,
            kind="image",
            url="https://example.test/photo.jpg",
            caption="Metadata payload",
            provider_name="local",
            provider_object_id="properties/1/photo.jpg",
            lifecycle_state="active",
            backup_state="available",
        )
        payload = media_dto(media_row)
        self.assertEqual(payload["provider"]["name"], "local")
        self.assertEqual(payload["provider"]["object_id"], "properties/1/photo.jpg")
        self.assertEqual(payload["lifecycle_state"], "active")
        self.assertEqual(payload["backup_state"], "available")
