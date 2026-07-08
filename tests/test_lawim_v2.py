from __future__ import annotations

import os
import tempfile
from http import HTTPStatus
from pathlib import Path

from lawim_v2.db import ConflictError, LawimRepository

from lawim_harness import LawimTestHarness, MINIMAL_JPEG_BYTES, minimal_jpeg_base64


class LawimV2ExecutableBaselineTest(LawimTestHarness):
    def test_health_bootstrap_and_static_assets_are_exposed(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.status, HTTPStatus.OK)
        health_payload = health.body_json()
        self.assertEqual(health_payload["status"], "ok")
        self.assertEqual(health_payload["database"]["driver"], "sqlite")
        self.assertEqual(health_payload["database"]["schema_version"], 18)
        self.assertNotIn("audit", health_payload)
        self.assertIn("app_env", health_payload["environment"])
        self.assertEqual(health_payload["summary"]["organizations"], 3)
        self.assertEqual(health_payload["summary"]["users"], 10)

        bootstrap = self.invoke("/api/bootstrap")
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        bootstrap_payload = bootstrap.body_json()
        self.assertEqual(bootstrap_payload["summary"]["published_properties"], 50)
        self.assertEqual(len(bootstrap_payload["properties"]), 10)
        self.assertEqual(bootstrap_payload["official_contact"]["brand_slogan"], "L’immobilier autrement")
        self.assertEqual(bootstrap_payload["official_contact"]["brand_subslogan"], "")

        html = self.invoke("/")
        self.assertEqual(html.status, HTTPStatus.OK)
        self.assertIn("L’immobilier autrement", html.body_text())
        self.assertNotIn("En toute confiance", html.body_text())
        self.assertIn("Connexion", html.body_text())
        self.assertIn("Content-Security-Policy", html.response_headers)
        self.assertIn("default-src 'self'", html.response_headers["Content-Security-Policy"])

        logo = self.invoke("/logo.svg")
        self.assertEqual(logo.status, HTTPStatus.OK)
        self.assertEqual(logo.response_headers["Content-Type"], "image/svg+xml")

        favicon = self.invoke("/favicon.svg")
        self.assertEqual(favicon.status, HTTPStatus.OK)
        self.assertEqual(favicon.response_headers["Content-Type"], "image/svg+xml")

        js = self.invoke("/app.js")
        self.assertEqual(js.status, HTTPStatus.OK)
        self.assertIn("renderBootstrap", js.body_text())

    def test_missing_resources_and_invalid_input_are_rejected_cleanly(self) -> None:
        property_lookup = self.invoke("/api/properties/999999")
        self.assertEqual(property_lookup.status, HTTPStatus.NOT_FOUND)
        self.assertEqual(property_lookup.body_json()["error"]["code"], "not_found")

        conversation_messages = self.invoke("/api/conversations/999999/messages")
        self.assertEqual(conversation_messages.status, HTTPStatus.UNAUTHORIZED)

        unauthorized = self.invoke("/api/me")
        self.assertEqual(unauthorized.status, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(unauthorized.response_headers["WWW-Authenticate"], 'Bearer realm="LAWIM_V2"')

        invalid_content_type = self.invoke(
            "/api/auth/login",
            method="POST",
            raw_body=b"{}",
            headers={"Content-Type": "text/plain"},
        )
        self.assertEqual(invalid_content_type.status, HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

        invalid_content_length = self.invoke(
            "/api/auth/login",
            method="POST",
            raw_body=b"{}",
            headers={"Content-Type": "application/json", "Content-Length": "abc"},
        )
        self.assertEqual(invalid_content_length.status, HTTPStatus.BAD_REQUEST)

        invalid_match_range = self.invoke("/api/matches?budget_min=10&budget_max=5")
        self.assertEqual(invalid_match_range.status, HTTPStatus.BAD_REQUEST)

    def test_property_validation_rejects_inverted_price_ranges(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = str(login.body_json()["token"])

        rejected = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Bad Range Property",
                "summary": "This should fail.",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 340000,
                "price_max": 260000,
                "property_type": "apartment",
            },
        )
        self.assertEqual(rejected.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(rejected.body_json()["error"]["code"], "invalid_state")

    def test_persistence_profile_is_formalized_and_seed_helper_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "empty.sqlite3"
            repository = LawimRepository(db_path)
            repository.initialize(seed_demo_data=False)
            try:
                profile = repository.backend_profile()
                self.assertEqual(profile["driver"], "sqlite")
                self.assertEqual(profile["adapter"], "sqlite-repository")
                self.assertEqual(profile["schema_version"], 18)
                self.assertEqual(profile["migration"]["orm"], "prisma")
                self.assertEqual(profile["migration"]["target_engine"], "postgresql")
                self.assertEqual(profile["seed"]["name"], "demo")
                self.assertEqual(profile["schema"]["name"], "lawim_v2_runtime_schema")
                self.assertEqual(profile["schema"]["tables"][0]["name"], "organizations")
                self.assertEqual(len(str(profile["schema_fingerprint"])), 64)

                stored_fingerprint = repository.one(
                    "SELECT value FROM schema_meta WHERE key = 'schema_fingerprint'"
                )
                self.assertIsNotNone(stored_fingerprint)
                self.assertEqual(stored_fingerprint["value"], profile["schema_fingerprint"])
                self.assertEqual(repository.summary()["organizations"], 0)

                first_seed = repository.seed_demo_data()
                self.assertTrue(first_seed["seeded"])
                self.assertEqual(first_seed["schema_version"], 18)
                self.assertEqual(repository.summary()["organizations"], 3)

                second_seed = repository.seed_demo_data()
                self.assertFalse(second_seed["seeded"])
                self.assertEqual(second_seed["summary"]["organizations"], 3)
            finally:
                repository.close()

    def test_sync_demo_credentials_updates_app_accounts(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            db_path = Path(tempdir) / "runtime.sqlite3"
            repository = LawimRepository(db_path)
            repository.initialize(seed_demo_data=False)
            try:
                repository.create_user(
                    email="admin@lawim.app",
                    full_name="Admin LAWIM",
                    role="admin",
                    password="old-secret",
                )
                self.assertIsNotNone(repository.authenticate(email="admin@lawim.app", password="old-secret"))

                updated = repository.sync_demo_credentials("new-secret")
                self.assertIn("admin@lawim.app", updated)
                self.assertIsNone(repository.authenticate(email="admin@lawim.app", password="old-secret"))
                self.assertIsNotNone(repository.authenticate(email="admin@lawim.app", password="new-secret"))
            finally:
                repository.close()

    def test_build_runtime_syncs_credentials_from_environment(self) -> None:
        from lawim_v2.bootstrap import build_runtime
        from lawim_v2.config import AppConfig

        previous = os.environ.get("LAWIM_ADMIN_PASSWORD")
        os.environ["LAWIM_ADMIN_PASSWORD"] = "runtime-secret"
        try:
            with tempfile.TemporaryDirectory() as tempdir:
                db_path = Path(tempdir) / "runtime.sqlite3"
                media_path = Path(tempdir) / "media"
                runtime = build_runtime(AppConfig.for_test(db_path=db_path, media_storage_path=media_path))
                try:
                    self.assertIsNone(
                        runtime.repository.authenticate(email="admin@lawim.local", password="lawim-demo")
                    )
                    self.assertIsNotNone(
                        runtime.repository.authenticate(email="admin@lawim.local", password="runtime-secret")
                    )
                finally:
                    runtime.close()
        finally:
            if previous is None:
                os.environ.pop("LAWIM_ADMIN_PASSWORD", None)
            else:
                os.environ["LAWIM_ADMIN_PASSWORD"] = previous

    def test_referential_integrity_blocks_orphaned_deletes(self) -> None:
        seeded_conversations = self.repository.list_conversations(limit=10)
        self.assertTrue(seeded_conversations)
        property_with_conversation = self.repository.get_property(int(seeded_conversations[0]["property_id"]))
        agent = self.repository.get_user_by_email("agent@lawim.local")

        soft_deleted = self.repository.delete_property(int(property_with_conversation["id"]))
        self.assertTrue(soft_deleted["soft"])

        with self.assertRaises(ConflictError):
            self.repository.delete_user(int(agent["id"]))

    def test_role_based_permissions_block_global_writes_and_impersonation(self) -> None:
        admin_login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        owner_login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "owner@lawim.local", "password": "lawim-demo"},
        )

        admin_payload = admin_login.body_json()
        owner_payload = owner_login.body_json()
        admin_token = str(admin_payload["token"])
        owner_token = str(owner_payload["token"])
        admin_id = int(admin_payload["user"]["id"])
        owner_id = int(owner_payload["user"]["id"])

        created_property = self.invoke(
            "/api/properties",
            method="POST",
            token=admin_token,
            body={
                "title": "Riverfront Tower",
                "summary": "Prime riverside listing.",
                "city": "Douala",
                "country": "Cameroon",
                "status": "draft",
                "property_type": "apartment",
            },
        )
        property_id = int(created_property.body_json()["property"]["id"])

        owner_property_update = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=owner_token,
            body={"title": "Blocked update"},
        )
        self.assertEqual(owner_property_update.status, HTTPStatus.FORBIDDEN)
        self.assertEqual(owner_property_update.body_json()["error"]["code"], "forbidden")

        owner_org_create = self.invoke(
            "/api/organizations",
            method="POST",
            token=owner_token,
            body={"name": "Blocked Org", "slug": "blocked-org", "kind": "owner"},
        )
        self.assertEqual(owner_org_create.status, HTTPStatus.FORBIDDEN)

        owner_user_create = self.invoke(
            "/api/users",
            method="POST",
            token=owner_token,
            body={
                "email": "blocked@lawim.local",
                "full_name": "Blocked User",
                "role": "agent",
                "password": "lawim-demo",
            },
        )
        self.assertEqual(owner_user_create.status, HTTPStatus.FORBIDDEN)

        owner_events = self.invoke("/api/events", token=owner_token)
        self.assertEqual(owner_events.status, HTTPStatus.FORBIDDEN)

        impersonated_conversation = self.invoke(
            "/api/conversations",
            method="POST",
            token=owner_token,
            body={
                "user_id": owner_id,
                "subject": "Impersonation attempt",
                "sender_user_id": admin_id,
            },
        )
        self.assertEqual(impersonated_conversation.status, HTTPStatus.FORBIDDEN)

    def test_backend_mutations_persist_and_event_log_is_available(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        login_payload = login.body_json()
        token = str(login_payload["token"])
        user_id = int(login_payload["user"]["id"])
        organization_id = int(login_payload["user"]["organization_id"])

        user_update = self.invoke(
            f"/api/users/{user_id}",
            method="PATCH",
            token=token,
            body={"full_name": "LAWIM Admin Prime"},
        )
        self.assertEqual(user_update.status, HTTPStatus.OK)
        self.assertEqual(user_update.body_json()["user"]["full_name"], "LAWIM Admin Prime")

        me = self.invoke("/api/me", token=token)
        self.assertEqual(me.status, HTTPStatus.OK)
        self.assertEqual(me.body_json()["user"]["full_name"], "LAWIM Admin Prime")

        organization_update = self.invoke(
            f"/api/organizations/{organization_id}",
            method="PUT",
            token=token,
            body={"name": "LAWIM Demo Agency Plus"},
        )
        self.assertEqual(organization_update.status, HTTPStatus.OK)
        self.assertEqual(organization_update.body_json()["organization"]["name"], "LAWIM Demo Agency Plus")

        property_create = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Riverfront Loft",
                "summary": "Riverside residence ready for upgrade.",
                "city": "Douala",
                "country": "Cameroon",
                "status": "draft",
                "property_type": "apartment",
                "price_min": 250000,
                "price_max": 300000,
            },
        )
        property_payload = property_create.body_json()["property"]
        property_id = int(property_payload["id"])

        property_update = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=token,
            body={"title": "Riverfront Loft Prime", "status": "published", "version": property_payload["version"]},
        )
        self.assertEqual(property_update.status, HTTPStatus.OK)
        self.assertEqual(property_update.body_json()["property"]["title"], "Riverfront Loft Prime")
        self.assertEqual(property_update.body_json()["property"]["status"], "published")

        property_detail = self.invoke(f"/api/properties/{property_id}", token=token)
        self.assertEqual(property_detail.status, HTTPStatus.OK)
        self.assertEqual(property_detail.body_json()["property"]["title"], "Riverfront Loft Prime")

        media_create = self.invoke(
            "/api/media",
            method="POST",
            token=token,
            body={
                "property_id": property_id,
                "kind": "image",
                "url": "https://example.test/riverfront-loft.jpg",
                "caption": "Original caption",
            },
        )
        media_id = int(media_create.body_json()["media"]["id"])

        media_update = self.invoke(
            f"/api/media/{media_id}",
            method="PATCH",
            token=token,
            body={"caption": "Updated caption"},
        )
        self.assertEqual(media_update.status, HTTPStatus.OK)
        self.assertEqual(media_update.body_json()["media"]["caption"], "Updated caption")

        media_delete = self.invoke(f"/api/media/{media_id}", method="DELETE", token=token)
        self.assertEqual(media_delete.status, HTTPStatus.OK)
        self.assertTrue(media_delete.body_json()["deleted"])

        conversation_create = self.invoke(
            "/api/conversations",
            method="POST",
            token=token,
            body={
                "property_id": property_id,
                "subject": "Site visit request",
                "initial_message": "Please share your availability.",
            },
        )
        conversation_id = int(conversation_create.body_json()["conversation"]["id"])

        conversation_update = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=token,
            body={"status": "closed"},
        )
        self.assertEqual(conversation_update.status, HTTPStatus.OK)
        self.assertEqual(conversation_update.body_json()["conversation"]["status"], "closed")

        conversation_delete = self.invoke(f"/api/conversations/{conversation_id}", method="DELETE", token=token)
        self.assertEqual(conversation_delete.status, HTTPStatus.OK)
        self.assertTrue(conversation_delete.body_json()["deleted"])

        property_delete = self.invoke(f"/api/properties/{property_id}", method="DELETE", token=token)
        self.assertEqual(property_delete.status, HTTPStatus.OK)
        self.assertTrue(property_delete.body_json()["deleted"])

        deleted_property_lookup = self.invoke(f"/api/properties/{property_id}", token=token)
        self.assertEqual(deleted_property_lookup.status, HTTPStatus.NOT_FOUND)

        events = self.invoke("/api/events?limit=20", token=token)
        self.assertEqual(events.status, HTTPStatus.OK)
        event_kinds = [event["kind"] for event in events.body_json()["events"]]
        self.assertIn("property_deleted", event_kinds)
        self.assertIn("conversation_deleted", event_kinds)

    def test_authentication_and_matching_flow_work_end_to_end(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        self.assertEqual(login.status, HTTPStatus.CREATED)
        login_payload = login.body_json()
        token = str(login_payload["token"])

        me = self.invoke("/api/me", token=token)
        self.assertEqual(me.status, HTTPStatus.OK)
        me_payload = me.body_json()
        self.assertEqual(me_payload["user"]["email"], "admin@lawim.local")

        matches = self.invoke("/api/matches?city=Douala&budget_max=320000&limit=1", token=token)
        self.assertEqual(matches.status, HTTPStatus.OK)
        matches_payload = matches.body_json()
        self.assertEqual(len(matches_payload["matches"]), 1)
        self.assertEqual(matches_payload["matches"][0]["property"]["geo"]["city"], "Douala")

    def test_authenticated_writes_persist(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        self.assertEqual(login.status, HTTPStatus.CREATED)
        token = str(login.body_json()["token"])

        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Akwa Night Tower",
                "summary": "Prime city-center residence.",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 260000,
                "price_max": 340000,
                "property_type": "apartment",
            },
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)
        property_id = created.body_json()["property"]["id"]

        property_detail = self.invoke(f"/api/properties/{property_id}", token=token)
        self.assertEqual(property_detail.status, HTTPStatus.OK)
        self.assertEqual(property_detail.body_json()["property"]["title"], "Akwa Night Tower")

        conversation = self.invoke(
            "/api/conversations",
            method="POST",
            token=token,
            body={
                "property_id": property_id,
                "subject": "Visit request",
                "initial_message": "I want a visit on Saturday morning.",
            },
        )
        self.assertEqual(conversation.status, HTTPStatus.CREATED)
        conversation_payload = conversation.body_json()["conversation"]
        self.assertEqual(conversation_payload["message_count"], 1)

        conversation_id = conversation_payload["id"]
        messages = self.invoke(f"/api/conversations/{conversation_id}/messages", token=token)
        self.assertEqual(messages.status, HTTPStatus.OK)
        self.assertEqual(len(messages.body_json()["messages"]), 1)

    def test_property_platform_pagination_filtering_and_dto_contract(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = str(login.body_json()["token"])

        listing = self.invoke("/api/properties?city=Douala&status=published&limit=2&page=1&sort=title&order=asc", token=token)
        self.assertEqual(listing.status, HTTPStatus.OK)
        payload = listing.body_json()
        self.assertIn("pagination", payload)
        self.assertEqual(payload["pagination"]["limit"], 2)
        self.assertGreaterEqual(payload["pagination"]["total"], 1)
        self.assertIn("geo", payload["properties"][0])
        self.assertIn("price", payload["properties"][0])
        self.assertIn("listing_code", payload["properties"][0])

    def test_geo_normalization_search_and_contracts(self) -> None:
        normalized = self.invoke("/api/geo/normalize?city=douala&country=cameroun&region=littoral")
        self.assertEqual(normalized.status, HTTPStatus.OK)
        payload = normalized.body_json()
        location = payload["location"]
        self.assertEqual(location["city"], "Douala")
        self.assertEqual(location["country"], "Cameroon")
        self.assertEqual(location["region"], "Littoral")
        self.assertEqual(payload["provider"], "normalize")

        geocoded = self.invoke("/api/geo/geocode?city=Douala&country=Cameroon&address_line=Bonanjo")
        self.assertEqual(geocoded.status, HTTPStatus.OK)
        geo_payload = geocoded.body_json()
        self.assertEqual(geo_payload["provider"], "local")
        self.assertIn("coordinates", geo_payload["location"])

        search = self.invoke("/api/geo/search?q=douala")
        self.assertEqual(search.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(search.body_json()["locations"]), 1)

        contracts = self.invoke("/api/geo/contracts")
        self.assertEqual(contracts.status, HTTPStatus.OK)
        self.assertEqual(contracts.body_json()["thumbnail"]["strategy"], "deterministic-svg-placeholder")

    def test_media_upload_storage_and_soft_delete(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = str(login.body_json()["token"])

        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Media Platform Loft",
                "summary": "Property used to validate media upload.",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 100000,
                "price_max": 150000,
                "status": "draft",
            },
        )
        property_id = int(created.body_json()["property"]["id"])
        content = minimal_jpeg_base64()

        uploaded = self.invoke(
            "/api/media/upload",
            method="POST",
            token=token,
            body={
                "property_id": property_id,
                "filename": "cover.jpg",
                "content_base64": content,
                "caption": "Cover image",
            },
        )
        self.assertEqual(uploaded.status, HTTPStatus.CREATED)
        media_payload = uploaded.body_json()["media"]
        self.assertTrue(str(media_payload["url"]).startswith("http://127.0.0.1:3000/media/"))
        self.assertIn("thumbnail", media_payload)
        self.assertEqual(media_payload["mime_type"], "image/jpeg")

        media_id = int(media_payload["id"])
        deleted = self.invoke(f"/api/media/{media_id}", method="DELETE", token=token)
        self.assertEqual(deleted.status, HTTPStatus.OK)
        self.assertTrue(deleted.body_json()["soft"])

        missing = self.invoke(f"/api/media/{media_id}", token=token)
        self.assertEqual(missing.status, HTTPStatus.NOT_FOUND)

    def test_property_publish_endpoint_and_optimistic_locking(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = str(login.body_json()["token"])

        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Publish Candidate",
                "summary": "Ready for publication.",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 120000,
                "price_max": 180000,
                "status": "draft",
            },
        )
        property_row = created.body_json()["property"]
        property_id = int(property_row["id"])

        published = self.invoke(
            f"/api/properties/{property_id}/publish",
            method="POST",
            token=token,
            body={"version": property_row["version"]},
        )
        self.assertEqual(published.status, HTTPStatus.OK)
        self.assertEqual(published.body_json()["property"]["status"], "published")
        self.assertIsNotNone(published.body_json()["property"]["lifecycle"]["published_at"])

        stale = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=token,
            body={"title": "Stale update", "version": property_row["version"]},
        )
        self.assertEqual(stale.status, HTTPStatus.CONFLICT)

    def test_postgresql_adapter_profile_is_prepared(self) -> None:
        from lawim_v2.persistence_adapter import PostgreSQLPersistenceAdapter

        adapter = PostgreSQLPersistenceAdapter("postgresql://example.test/lawim", allow_sqlite_fallback=True)
        profile = adapter.backend_profile(schema_version=18)
        self.assertEqual(profile["driver"], "postgresql")
        self.assertEqual(profile["adapter"], "postgresql-repository")
        self.assertEqual(profile["status"], "active")
        self.assertEqual(profile["prisma_schema"], "prisma/schema.prisma")

    def test_bootstrap_returns_dto_aligned_properties_and_media(self) -> None:
        bootstrap = self.invoke("/api/bootstrap")
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        payload = bootstrap.body_json()
        self.assertGreaterEqual(len(payload["properties"]), 1)
        property_row = payload["properties"][0]
        self.assertIn("geo", property_row)
        self.assertIn("price", property_row)
        self.assertIn("listing_code", property_row)
        if payload["media"]:
            media_row = payload["media"][0]
            self.assertIn("thumbnail", media_row)

    def test_multipart_media_upload(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = str(login.body_json()["token"])
        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Multipart Property",
                "summary": "Multipart upload target",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 100000,
                "price_max": 120000,
                "status": "draft",
            },
        )
        property_id = int(created.body_json()["property"]["id"])
        boundary = "----LawimBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="property_id"\r\n\r\n'
            f"{property_id}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="cover.jpg"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode("utf-8") + MINIMAL_JPEG_BYTES + f"\r\n--{boundary}--\r\n".encode("utf-8")
        uploaded = self.invoke(
            "/api/media/upload",
            method="POST",
            token=token,
            raw_body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(uploaded.status, HTTPStatus.CREATED)
        self.assertEqual(uploaded.body_json()["media"]["mime_type"], "image/jpeg")

    def test_prisma_manifest_validation_script(self) -> None:
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, "scripts/validate_prisma_manifest.py"],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_local_geocoding_provider_is_deterministic(self) -> None:
        from lawim_v2.geocoding_provider import LocalGeocodingProvider

        provider = LocalGeocodingProvider()
        first = provider.geocode(city="Douala", country="Cameroon", address_line="Bonanjo")
        second = provider.geocode(city="Douala", country="Cameroon", address_line="Bonanjo")
        self.assertEqual(first, second)
        self.assertEqual(first["provider"], "local")

    def test_schema_version_is_five(self) -> None:
        self.assertEqual(self.repository.schema_version(), 18)

    def test_advanced_matching_breakdown_and_weights(self) -> None:
        matches = self.invoke(
            "/api/matches?city=Douala&budget_max=320000&bedrooms_min=2&property_type=apartment&limit=3"
        )
        self.assertEqual(matches.status, HTTPStatus.OK)
        payload = matches.body_json()
        self.assertIn("criteria", payload)
        self.assertIn("weights", payload["criteria"])
        first = payload["matches"][0]
        self.assertIn("breakdown", first)
        self.assertIn("reasons", first)
        self.assertIn("score", first)
        self.assertIn("property", first)

    def test_partner_matching_api_explains_recommendations(self) -> None:
        cases = (
            ("photographe", "photographer", "Douala", None),
            ("architecte", "architect", "Yaounde", "build"),
            ("notaire", "notary", "Douala", "buy"),
            ("banque", "bank", "Douala", "buy"),
        )
        for need, expected_partner_type, city, project_type in cases:
            with self.subTest(need=need, expected_partner_type=expected_partner_type):
                query = f"/api/matches?target_type=partner&need={need}&city={city}&limit=5"
                if project_type:
                    query += f"&project_type={project_type}"
                response = self.invoke(query)
                self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
                payload = response.body_json()
                self.assertEqual(payload["criteria"]["target_type"], "partner")
                self.assertEqual(payload["criteria"]["partner_type"], expected_partner_type)
                self.assertEqual(payload["explanation"]["target_type"], "partner")
                self.assertEqual(payload["explanation"]["need"], need)
                self.assertGreaterEqual(len(payload["matches"]), 1)
                top = payload["matches"][0]
                self.assertEqual(top["target_type"], "partner")
                self.assertEqual(top["partner"]["partner_type"], expected_partner_type)
                self.assertTrue(top["summary"])
                self.assertTrue(top["reasons"])

    def test_notifications_created_on_conversation_and_message(self) -> None:
        owner_login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "owner@lawim.local", "password": "lawim-demo"},
        )
        owner_token = str(owner_login.body_json()["token"])
        created = self.invoke(
            "/api/conversations",
            method="POST",
            token=owner_token,
            body={
                "subject": "Notification probe",
                "initial_message": "Hello from tests",
            },
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)
        conversation_id = int(created.body_json()["conversation"]["id"])

        owner_notifications = self.invoke("/api/notifications?limit=20", token=owner_token)
        self.assertEqual(owner_notifications.status, HTTPStatus.OK)
        owner_kinds = [item["kind"] for item in owner_notifications.body_json()["notifications"]]
        self.assertIn("conversation_created", owner_kinds)

        admin_login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        admin_token = str(admin_login.body_json()["token"])
        reply = self.invoke(
            f"/api/conversations/{conversation_id}/messages",
            method="POST",
            token=admin_token,
            body={"body": "Follow-up ping"},
        )
        self.assertEqual(reply.status, HTTPStatus.CREATED)

        owner_refreshed = self.invoke("/api/notifications?limit=20", token=owner_token)
        refreshed_kinds = [item["kind"] for item in owner_refreshed.body_json()["notifications"]]
        self.assertIn("message_received", refreshed_kinds)

        notification_id = owner_refreshed.body_json()["notifications"][0]["id"]
        marked = self.invoke(f"/api/notifications/{notification_id}/read", method="PATCH", token=owner_token, body={})
        self.assertEqual(marked.status, HTTPStatus.OK)
        self.assertTrue(marked.body_json()["notification"]["read"])

    def test_negotiation_stage_update(self) -> None:
        login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        token = str(login.body_json()["token"])
        created = self.invoke(
            "/api/conversations",
            method="POST",
            token=token,
            body={"subject": "Offer thread", "initial_message": "Interested"},
        )
        conversation_id = int(created.body_json()["conversation"]["id"])
        updated = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=token,
            body={"negotiation_stage": "offer"},
        )
        self.assertEqual(updated.status, HTTPStatus.OK)
        self.assertEqual(updated.body_json()["conversation"]["negotiation_stage"], "offer")

    def test_health_and_metrics_endpoints(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.status, HTTPStatus.OK)
        health_payload = health.body_json()
        self.assertEqual(health_payload["status"], "ok")
        self.assertNotIn("audit", health_payload)
        self.assertIn("notifications", health_payload["summary"])

        admin_login = self.invoke(
            "/api/auth/login",
            method="POST",
            body={"email": "admin@lawim.local", "password": "lawim-demo"},
        )
        admin_token = str(admin_login.body_json()["token"])
        admin_health = self.invoke("/api/health", token=admin_token)
        self.assertIn("audit", admin_health.body_json())

        metrics = self.invoke("/api/metrics", token=admin_token)
        self.assertEqual(metrics.status, HTTPStatus.OK)
        self.assertIn("metrics", metrics.body_json())
