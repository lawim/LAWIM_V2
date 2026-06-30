from __future__ import annotations

from http import HTTPStatus
from importlib import resources

from lawim_harness import LawimTestHarness


class PropertySearchStabilizationTest(LawimTestHarness):
    def test_property_search_price_filters_pagination_and_invalid_range(self) -> None:
        filtered = self.invoke("/api/properties?status=published&price_min=100000&price_max=300000&limit=5&sort=price_min&order=asc")
        self.assertEqual(filtered.status, HTTPStatus.OK)
        payload = filtered.body_json()
        self.assertIn("pagination", payload)
        self.assertIn("properties", payload)
        pagination = payload["pagination"]
        self.assertGreaterEqual(int(pagination["page"]), 1)
        self.assertLessEqual(len(payload["properties"]), 5)
        for item in payload["properties"]:
            price = item.get("price") or {}
            price_min = int(price.get("min") or item.get("price_min") or 0)
            price_max = int(price.get("max") or item.get("price_max") or price_min)
            self.assertLessEqual(price_min, 300000)
            if price_max:
                self.assertGreaterEqual(price_max, 100000)

        invalid = self.invoke("/api/properties?price_min=500000&price_max=100000")
        self.assertEqual(invalid.status, HTTPStatus.BAD_REQUEST)
        error = self.assert_error_shape(invalid)
        self.assertEqual(error["code"], "invalid_query")

        bad_sort = self.invoke("/api/properties?sort=unknown")
        self.assertEqual(bad_sort.status, HTTPStatus.BAD_REQUEST)
        self.assertIn(error["code"], {"validation_error", "invalid_state", "invalid_query"})


class MatchingStabilizationTest(LawimTestHarness):
    def test_match_found_notification_is_deduped_and_score_is_explainable(self) -> None:
        token = self.login(email="owner@lawim.local")
        first = self.invoke("/api/matches?city=Douala&limit=3", token=token)
        self.assertEqual(first.status, HTTPStatus.OK)
        body = first.body_json()
        self.assertIn("criteria", body)
        self.assertIn("min_score", body["criteria"])
        if body["matches"]:
            match = body["matches"][0]
            self.assertIn("summary", match)
            self.assertIn("grade", match)
            self.assertIn("eligible", match)
            self.assertIn("breakdown", match)

        notifications_after_first = self.invoke("/api/notifications?kind=match_found", token=token)
        count_first = len(notifications_after_first.body_json()["notifications"])

        second = self.invoke("/api/matches?city=Douala&limit=3", token=token)
        self.assertEqual(second.status, HTTPStatus.OK)
        notifications_after_second = self.invoke("/api/notifications?kind=match_found", token=token)
        count_second = len(notifications_after_second.body_json()["notifications"])
        self.assertEqual(count_first, count_second)

    def test_high_min_score_returns_no_matches(self) -> None:
        response = self.invoke("/api/matches?city=Douala&min_score=99&limit=5")
        self.assertEqual(response.status, HTTPStatus.OK)
        self.assertEqual(response.body_json()["matches"], [])


class NegotiationStabilizationTest(LawimTestHarness):
    def test_negotiation_stage_transitions_and_permissions(self) -> None:
        buyer_token = self.login(email="owner@lawim.local")
        created = self.invoke(
            "/api/conversations",
            method="POST",
            token=buyer_token,
            body={"property_id": 1, "subject": "Offer thread", "initial_message": "Interested"},
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)
        conversation_id = int(created.body_json()["conversation"]["id"])

        offer = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=buyer_token,
            body={"negotiation_stage": "offer"},
        )
        self.assertEqual(offer.status, HTTPStatus.OK)
        negotiation = offer.body_json()["conversation"]["negotiation"]
        self.assertEqual(negotiation["stage"], "offer")
        self.assertIn("offer", negotiation["allowed_stages"])

        invalid = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=buyer_token,
            body={"negotiation_stage": "inquiry"},
        )
        self.assertEqual(invalid.status, HTTPStatus.BAD_REQUEST)
        self.assertIn(self.assert_error_shape(invalid)["code"], {"validation_error", "invalid_state"})

        outsider = self.register(email="outsider.stab@lawim.local", full_name="Outsider", role="owner")
        denied = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=outsider,
            body={"negotiation_stage": "counter"},
        )
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)


class NotificationStabilizationTest(LawimTestHarness):
    def test_notifications_support_kind_filter_and_pagination(self) -> None:
        token = self.login(email="admin@lawim.local")
        all_notifications = self.invoke("/api/notifications?limit=5&page=1", token=token)
        self.assertEqual(all_notifications.status, HTTPStatus.OK)
        payload = all_notifications.body_json()
        self.assertIn("pagination", payload)
        self.assertIn("notifications", payload)
        self.assertLessEqual(len(payload["notifications"]), 5)

        filtered = self.invoke("/api/notifications?kind=conversation_created&limit=10", token=token)
        self.assertEqual(filtered.status, HTTPStatus.OK)
        for item in filtered.body_json()["notifications"]:
            self.assertEqual(item["kind"], "conversation_created")
            self.assertIn("read", item)


class SecurityStabilizationTest(LawimTestHarness):
    def test_cross_access_property_update_is_denied(self) -> None:
        admin_token = self.login(email="admin@lawim.local")
        organization = self.invoke(
            "/api/organizations",
            method="POST",
            token=admin_token,
            body={"name": "Cross Access Org", "slug": "cross-access-org", "kind": "agency", "city": "Douala"},
        )
        organization_id = int(organization.body_json()["organization"]["id"])
        seller_token = self.register(
            email="cross.seller@lawim.local",
            full_name="Cross Seller",
            role="agent",
            organization_id=organization_id,
            token=admin_token,
        )
        created = self.invoke(
            "/api/properties",
            method="POST",
            token=seller_token,
            body={
                "title": "Cross access property",
                "city": "Douala",
                "country": "Cameroon",
                "owner_organization_id": organization_id,
                "status": "draft",
            },
        )
        property_id = int(created.body_json()["property"]["id"])
        version = int(created.body_json()["property"]["version"])
        outsider = self.register(email="cross.outsider@lawim.local", full_name="Outsider", role="owner")
        denied = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=outsider,
            body={"title": "Hijacked", "version": version},
        )
        self.assertEqual(denied.status, HTTPStatus.FORBIDDEN)
        allowed = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=seller_token,
            body={"summary": "Seller update", "version": version},
        )
        self.assertEqual(allowed.status, HTTPStatus.OK)

    def test_oversized_json_payload_is_rejected(self) -> None:
        token = self.login(email="admin@lawim.local")
        oversized = b'{"title":"' + b"x" * self.max_json_body_bytes + b'"}'
        response = self.invoke(
            "/api/properties",
            method="POST",
            token=token,
            raw_body=oversized,
            headers={"Content-Type": "application/json", "Content-Length": str(len(oversized))},
        )
        self.assertEqual(response.status, HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
        self.assertEqual(self.assert_error_shape(response)["code"], "payload_too_large")


class MvpUiDtoRegressionTest(LawimTestHarness):
    def test_static_ui_consumes_stabilized_dto_fields(self) -> None:
        app_js = resources.files("lawim_v2.static").joinpath("app.js").read_text(encoding="utf-8")
        for marker in (
            "match.summary",
            "match.grade",
            "conversation.negotiation",
            "notification.read",
            "property-search-meta",
            "notification-filter-form",
            "negotiation-form",
            "formatApiError",
            "price_min",
            "min_score",
        ):
            self.assertIn(marker, app_js)

    def test_conversation_detail_includes_negotiation_history(self) -> None:
        token = self.login(email="owner@lawim.local")
        created = self.invoke(
            "/api/conversations",
            method="POST",
            token=token,
            body={"property_id": 1, "subject": "History check", "initial_message": "Hello"},
        )
        conversation_id = int(created.body_json()["conversation"]["id"])
        detail = self.invoke(f"/api/conversations/{conversation_id}", token=token)
        self.assertEqual(detail.status, HTTPStatus.OK)
        conversation = detail.body_json()["conversation"]
        self.assertIn("negotiation", conversation)
        self.assertTrue(conversation["negotiation"]["history"])
