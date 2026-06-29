from __future__ import annotations

import io
import json
import tempfile
from http import HTTPStatus
from pathlib import Path
from unittest import TestCase

from lawim_v2.config import AppConfig
from lawim_v2.db import ConflictError, LawimRepository
from lawim_v2.server import LawimRequestHandler
from lawim_v2.services import LawimServices


class DummyHandler(LawimRequestHandler):
    def __init__(
        self,
        repository: LawimRepository,
        config: AppConfig,
        path: str,
        *,
        method: str = "GET",
        headers: dict[str, str] | None = None,
        body: bytes = b"",
    ) -> None:
        self.repository = repository
        self.config = config
        self.services = LawimServices(repository, config)
        self.path = path
        self.command = method
        self.headers = headers or {}
        self.rfile = io.BytesIO(body)
        self.wfile = io.BytesIO()
        self.status: int | None = None
        self.response_headers: dict[str, str] = {}
        self.send_response = lambda status: setattr(self, "status", int(status))
        self.send_header = lambda key, value: self.response_headers.__setitem__(key, value)
        self.end_headers = lambda: None

    def body_text(self) -> str:
        return self.wfile.getvalue().decode("utf-8")

    def body_json(self) -> dict[str, object]:
        return json.loads(self.body_text())


class LawimV2ExecutableBaselineTest(TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tempdir.name) / "lawim.sqlite3"
        self.repository = LawimRepository(self.db_path)
        self.repository.initialize(seed_demo_data=True)
        self.config = AppConfig(
            host="127.0.0.1",
            port=3000,
            db_path=self.db_path,
            app_env="test",
            stack_profile="test",
            log_level="debug",
            public_base_url="http://127.0.0.1:3000",
            secret_provider="external",
            seed_demo_data=True,
            session_ttl_seconds=3600,
        )

    def tearDown(self) -> None:
        self.repository.close()
        self.tempdir.cleanup()

    def invoke(
        self,
        path: str,
        *,
        method: str = "GET",
        body: dict[str, object] | None = None,
        raw_body: bytes | None = None,
        headers: dict[str, str] | None = None,
        token: str | None = None,
    ) -> DummyHandler:
        request_headers: dict[str, str] = dict(headers or {})
        payload = b""
        if raw_body is not None:
            payload = raw_body
            request_headers.setdefault("Content-Length", str(len(payload)))
        if body is not None:
            payload = json.dumps(body).encode("utf-8")
            request_headers.setdefault("Content-Length", str(len(payload)))
            request_headers.setdefault("Content-Type", "application/json")
        if token:
            request_headers["Authorization"] = f"Bearer {token}"

        handler = DummyHandler(self.repository, self.config, path, method=method, headers=request_headers, body=payload)
        if method == "GET":
            handler.do_GET()
        elif method == "POST":
            handler.do_POST()
        elif method == "PUT":
            handler.do_PUT()
        elif method == "PATCH":
            handler.do_PATCH()
        elif method == "DELETE":
            handler.do_DELETE()
        else:  # pragma: no cover - helper is only used for GET/POST/PUT/PATCH/DELETE
            raise AssertionError(f"Unsupported method: {method}")
        return handler

    def test_health_bootstrap_and_static_assets_are_exposed(self) -> None:
        health = self.invoke("/api/health")
        self.assertEqual(health.status, HTTPStatus.OK)
        health_payload = health.body_json()
        self.assertEqual(health_payload["status"], "ok")
        self.assertEqual(health_payload["database"]["driver"], "sqlite")
        self.assertEqual(health_payload["database"]["schema_version"], 3)
        self.assertEqual(health_payload["database"]["migration"]["target_engine"], "postgresql")
        self.assertTrue(health_payload["environment"]["seed_demo_data"])
        self.assertEqual(health_payload["summary"]["organizations"], 3)
        self.assertEqual(health_payload["summary"]["users"], 3)

        bootstrap = self.invoke("/api/bootstrap")
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        bootstrap_payload = bootstrap.body_json()
        self.assertEqual(bootstrap_payload["summary"]["published_properties"], 3)
        self.assertEqual(len(bootstrap_payload["properties"]), 3)

        html = self.invoke("/")
        self.assertEqual(html.status, HTTPStatus.OK)
        self.assertIn("LAWIM_V2 Executable Baseline", html.body_text())
        self.assertIn("Content-Security-Policy", html.response_headers)
        self.assertIn("default-src 'self'", html.response_headers["Content-Security-Policy"])

        js = self.invoke("/app.js")
        self.assertEqual(js.status, HTTPStatus.OK)
        self.assertIn("renderBootstrap", js.body_text())

    def test_missing_resources_and_invalid_input_are_rejected_cleanly(self) -> None:
        property_lookup = self.invoke("/api/properties/999999")
        self.assertEqual(property_lookup.status, HTTPStatus.NOT_FOUND)
        self.assertEqual(property_lookup.body_json()["error"]["code"], "not_found")

        conversation_messages = self.invoke("/api/conversations/999999/messages")
        self.assertEqual(conversation_messages.status, HTTPStatus.NOT_FOUND)

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
                self.assertEqual(profile["schema_version"], 3)
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
                self.assertEqual(first_seed["schema_version"], 3)
                self.assertEqual(repository.summary()["organizations"], 3)

                second_seed = repository.seed_demo_data()
                self.assertFalse(second_seed["seeded"])
                self.assertEqual(second_seed["summary"]["organizations"], 3)
            finally:
                repository.close()

    def test_referential_integrity_blocks_orphaned_deletes(self) -> None:
        seeded_properties = self.repository.list_properties(limit=10)
        property_with_conversation = next(
            property_row for property_row in seeded_properties if property_row["title"] == "Bonanjo City Loft"
        )
        agent = self.repository.get_user_by_email("agent@lawim.local")

        with self.assertRaises(ConflictError):
            self.repository.delete_property(int(property_with_conversation["id"]))

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
            body={"title": "Riverfront Loft Prime", "status": "published"},
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

        events = self.invoke("/api/events?limit=10", token=token)
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
        self.assertEqual(matches_payload["matches"][0]["property"]["title"], "Bonanjo City Loft")

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
