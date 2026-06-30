from __future__ import annotations

import json
from http import HTTPStatus
from importlib import resources

from lawim_harness import LawimTestHarness


class ProductDepthE2ETest(LawimTestHarness):
    def test_full_product_journey_from_org_to_audit(self) -> None:
        admin_token = self.login(email="admin@lawim.local")

        organization = self.invoke(
            "/api/organizations",
            method="POST",
            token=admin_token,
            body={"name": "Depth Agency", "slug": "depth-agency", "kind": "agency", "city": "Douala"},
        )
        self.assertEqual(organization.status, HTTPStatus.CREATED)
        organization_id = int(organization.body_json()["organization"]["id"])

        user = self.invoke(
            "/api/users",
            method="POST",
            token=admin_token,
            body={
                "email": "depth.agent@lawim.local",
                "full_name": "Depth Agent",
                "role": "agent",
                "password": "lawim-demo",
                "organization_id": organization_id,
            },
        )
        self.assertEqual(user.status, HTTPStatus.CREATED)
        agent_token = self.login(email="depth.agent@lawim.local")

        property_create = self.invoke(
            "/api/properties",
            method="POST",
            token=agent_token,
            body={
                "title": "Depth Validation Loft",
                "summary": "End-to-end product depth property.",
                "city": "Douala",
                "country": "Cameroon",
                "region": "Littoral",
                "price_min": 200000,
                "price_max": 280000,
                "property_type": "apartment",
                "bedrooms": 3,
                "status": "draft",
            },
        )
        self.assertEqual(property_create.status, HTTPStatus.CREATED)
        property_id = int(property_create.body_json()["property"]["id"])

        geocode = self.invoke("/api/geo/geocode?city=Douala&country=Cameroon&address_line=Bonanjo")
        self.assertEqual(geocode.status, HTTPStatus.OK)
        location = geocode.body_json()["location"]
        coords = location["coordinates"]

        updated = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=agent_token,
            body={
                "latitude": coords["latitude"],
                "longitude": coords["longitude"],
                "version": property_create.body_json()["property"]["version"],
            },
        )
        self.assertEqual(updated.status, HTTPStatus.OK)

        boundary = "----DepthBoundary"
        upload_body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="property_id"\r\n\r\n'
            f"{property_id}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="depth.jpg"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode("utf-8") + b"jpeg-bytes" + f"\r\n--{boundary}--\r\n".encode("utf-8")
        uploaded = self.invoke(
            "/api/media/upload",
            method="POST",
            token=agent_token,
            raw_body=upload_body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(uploaded.status, HTTPStatus.CREATED)
        media_id = int(uploaded.body_json()["media"]["id"])

        published = self.invoke(
            f"/api/properties/{property_id}/publish",
            method="POST",
            token=agent_token,
            body={"version": updated.body_json()["property"]["version"]},
        )
        self.assertEqual(published.status, HTTPStatus.OK)
        self.assertEqual(published.body_json()["property"]["status"], "published")

        matches = self.invoke(
            f"/api/matches?city=Douala&budget_max=300000&limit=10&latitude={coords['latitude']}&longitude={coords['longitude']}"
        )
        self.assertEqual(matches.status, HTTPStatus.OK)
        match_titles = [item["property"]["title"] for item in matches.body_json()["matches"]]
        self.assertIn("Depth Validation Loft", match_titles)

        owner_token = self.login(email="owner@lawim.local")
        conversation = self.invoke(
            "/api/conversations",
            method="POST",
            token=owner_token,
            body={
                "property_id": property_id,
                "subject": "Depth visit request",
                "initial_message": "Can we schedule a visit?",
            },
        )
        self.assertEqual(conversation.status, HTTPStatus.CREATED)
        conversation_id = int(conversation.body_json()["conversation"]["id"])

        reply = self.invoke(
            f"/api/conversations/{conversation_id}/messages",
            method="POST",
            token=agent_token,
            body={"body": "Yes, Saturday works."},
        )
        self.assertEqual(reply.status, HTTPStatus.CREATED)

        owner_notifications = self.invoke("/api/notifications?limit=20", token=owner_token)
        self.assertEqual(owner_notifications.status, HTTPStatus.OK)
        kinds = {item["kind"] for item in owner_notifications.body_json()["notifications"]}
        self.assertIn("conversation_created", kinds)
        self.assertIn("message_received", kinds)

        notification_id = owner_notifications.body_json()["notifications"][0]["id"]
        marked = self.invoke(
            f"/api/notifications/{notification_id}/read",
            method="PATCH",
            token=owner_token,
            body={},
        )
        self.assertEqual(marked.status, HTTPStatus.OK)

        events = self.invoke("/api/events?limit=50", token=admin_token)
        self.assertEqual(events.status, HTTPStatus.OK)
        event_kinds = {event["kind"] for event in events.body_json()["events"]}
        for expected in ("property_created", "media_created", "message_added", "notification_created"):
            self.assertIn(expected, event_kinds)

        metrics_before = self.invoke("/api/metrics")
        self.assertEqual(metrics_before.status, HTTPStatus.OK)

        persisted_property = self.invoke(f"/api/properties/{property_id}")
        self.assertEqual(persisted_property.status, HTTPStatus.OK)
        persisted = persisted_property.body_json()["property"]
        self.assertEqual(persisted["status"], "published")
        self.assertEqual(persisted["geo"]["coordinates"]["latitude"], coords["latitude"])

        persisted_media = self.invoke(f"/api/media/{media_id}")
        self.assertEqual(persisted_media.status, HTTPStatus.OK)
        self.assertEqual(persisted_media.body_json()["media"]["property_id"], property_id)

        storage_path = persisted_media.body_json()["media"].get("storage_path")
        if storage_path:
            asset = self.invoke(f"/media/{storage_path}")
            self.assertEqual(asset.status, HTTPStatus.OK)
            self.assertIn("X-Content-Type-Options", asset.response_headers)

        detail = self.invoke(f"/api/conversations/{conversation_id}", token=owner_token)
        self.assertEqual(detail.status, HTTPStatus.OK)
        self.assertGreaterEqual(len(detail.body_json()["conversation"]["messages"]), 2)


class ProductDepthNegativeTest(LawimTestHarness):
    def test_conversations_require_authentication(self) -> None:
        listing = self.invoke("/api/conversations")
        self.assertEqual(listing.status, HTTPStatus.UNAUTHORIZED)
        error = self.assert_error_shape(listing)
        self.assertEqual(error["code"], "missing_token")

        messages = self.invoke("/api/conversations/1/messages")
        self.assertEqual(messages.status, HTTPStatus.UNAUTHORIZED)

    def test_cross_user_conversation_access_is_forbidden(self) -> None:
        owner_token = self.login(email="owner@lawim.local")
        created = self.invoke(
            "/api/conversations",
            method="POST",
            token=owner_token,
            body={"subject": "Private thread", "initial_message": "Owner only"},
        )
        conversation_id = int(created.body_json()["conversation"]["id"])

        agent_token = self.login(email="agent@lawim.local")
        forbidden = self.invoke(f"/api/conversations/{conversation_id}", token=agent_token)
        self.assertEqual(forbidden.status, HTTPStatus.FORBIDDEN)
        self.assertEqual(self.assert_error_shape(forbidden)["code"], "forbidden")

    def test_invalid_negotiation_stage_transition(self) -> None:
        token = self.login(email="admin@lawim.local")
        created = self.invoke(
            "/api/conversations",
            method="POST",
            token=token,
            body={"subject": "Stage test", "initial_message": "Start"},
        )
        conversation_id = int(created.body_json()["conversation"]["id"])
        invalid = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=token,
            body={"negotiation_stage": "accepted"},
        )
        self.assertEqual(invalid.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(self.assert_error_shape(invalid)["code"], "invalid_state")

    def test_oversized_json_payload_is_rejected(self) -> None:
        token = self.login(email="admin@lawim.local")
        oversized = b"x" * (self.max_json_body_bytes + 1)
        response = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            raw_body=oversized,
            headers={"Content-Type": "application/json", "Content-Length": str(len(oversized))},
        )
        self.assertEqual(response.status, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        self.assertEqual(self.assert_error_shape(response)["code"], "payload_too_large")

    def test_invalid_media_mime_type_is_rejected(self) -> None:
        token = self.login(email="admin@lawim.local")
        created = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            body={
                "title": "Media reject target",
                "summary": "Mime validation",
                "city": "Douala",
                "country": "Cameroon",
            },
        )
        property_id = int(created.body_json()["property"]["id"])
        boundary = "----MimeBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="property_id"\r\n\r\n'
            f"{property_id}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="bad.exe"\r\n'
            f"Content-Type: application/x-msdownload\r\n\r\n"
        ).encode("utf-8") + b"bad" + f"\r\n--{boundary}--\r\n".encode("utf-8")
        rejected = self.invoke(
            "/api/media/upload",
            method="POST",
            token=token,
            raw_body=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(rejected.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(self.assert_error_shape(rejected)["code"], "invalid_state")

    def test_geocode_requires_city_and_country(self) -> None:
        missing_city = self.invoke("/api/geo/geocode?country=Cameroon")
        self.assertEqual(missing_city.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(self.assert_error_shape(missing_city)["code"], "invalid_query")

    def test_events_and_notifications_require_auth(self) -> None:
        events = self.invoke("/api/events")
        self.assertEqual(events.status, HTTPStatus.UNAUTHORIZED)

        notifications = self.invoke("/api/notifications")
        self.assertEqual(notifications.status, HTTPStatus.UNAUTHORIZED)

    def test_non_admin_cannot_read_audit_events(self) -> None:
        owner_token = self.login(email="owner@lawim.local")
        events = self.invoke("/api/events", token=owner_token)
        self.assertEqual(events.status, HTTPStatus.FORBIDDEN)

    def test_api_error_responses_share_consistent_shape(self) -> None:
        cases = [
            self.invoke("/api/properties/999999"),
            self.invoke("/api/me"),
            self.invoke("/api/matches?budget_min=100&budget_max=50"),
        ]
        for response in cases:
            error = self.assert_error_shape(response)
            self.assertIsInstance(error["code"], str)
            self.assertIsInstance(error["message"], str)
            self.assertTrue(error["code"])
            self.assertTrue(error["message"])

    def test_security_headers_on_json_and_static_responses(self) -> None:
        api = self.invoke("/api/health")
        for header in ("X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy"):
            self.assertIn(header, api.response_headers)
        self.assertEqual(api.response_headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(api.response_headers["X-Frame-Options"], "DENY")

        static = self.invoke("/")
        self.assertIn("Content-Security-Policy", static.response_headers)
        self.assertIn("X-Frame-Options", static.response_headers)


class ProductDepthUIValidationTest(LawimTestHarness):
    def test_static_ui_consumes_documented_dto_fields(self) -> None:
        app_js = resources.files("lawim_v2.static").joinpath("app.js").read_text(encoding="utf-8")
        for marker in (
            '"/api/bootstrap"',
            '"/api/matches"',
            "`/api/conversations/${",
            "/api/notifications",
            '"/api/geo/geocode"',
            '"/api/media/upload"',
            "match.breakdown",
            "match.summary",
            "match.grade",
            "conversation.negotiation_stage",
            "conversation.negotiation",
            "notification.read",
            "property.geo",
            "property.price",
        ):
            self.assertIn(marker, app_js)

    def test_bootstrap_guest_hides_private_conversations(self) -> None:
        guest = self.invoke("/api/bootstrap")
        self.assertEqual(guest.status, HTTPStatus.OK)
        self.assertEqual(guest.body_json()["conversations"], [])

    def test_bootstrap_authenticated_includes_notifications_dto(self) -> None:
        token = self.login(email="admin@lawim.local")
        bootstrap = self.invoke("/api/bootstrap", token=token)
        self.assertEqual(bootstrap.status, HTTPStatus.OK)
        payload = bootstrap.body_json()
        self.assertIn("notifications", payload)
        if payload["conversations"]:
            conversation = payload["conversations"][0]
            self.assertIn("requester", conversation)
            self.assertIn("negotiation_stage", conversation)
