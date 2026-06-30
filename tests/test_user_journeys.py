from __future__ import annotations

from http import HTTPStatus

from lawim_harness import LawimTestHarness, MINIMAL_JPEG_BYTES


class SellerJourneyTest(LawimTestHarness):
    def test_seller_journey_register_listing_publish_and_archive(self) -> None:
        admin_token = self.login(email="admin@lawim.local")

        organization = self.invoke(
            "/api/organizations",
            method="POST",
            token=admin_token,
            body={"name": "Seller Journey Agency", "slug": "seller-journey-agency", "kind": "agency", "city": "Douala"},
        )
        self.assertEqual(organization.status, HTTPStatus.CREATED)
        organization_id = int(organization.body_json()["organization"]["id"])

        seller_token = self.register(
            email="seller.journey@lawim.local",
            full_name="Seller Journey",
            role="agent",
            organization_id=organization_id,
        )

        created = self.invoke(
            "/api/properties",
            method="POST",
            token=seller_token,
            body={
                "title": "Seller Journey Villa",
                "summary": "Full seller lifecycle property.",
                "city": "Douala",
                "country": "Cameroon",
                "region": "Littoral",
                "price_min": 180000,
                "price_max": 240000,
                "property_type": "house",
                "bedrooms": 4,
                "status": "draft",
            },
        )
        self.assertEqual(created.status, HTTPStatus.CREATED)
        property_id = int(created.body_json()["property"]["id"])
        version = int(created.body_json()["property"]["version"])

        geocode = self.invoke("/api/geo/geocode?city=Douala&country=Cameroon&address_line=Akwa")
        coords = geocode.body_json()["location"]["coordinates"]
        updated = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=seller_token,
            body={"latitude": coords["latitude"], "longitude": coords["longitude"], "version": version},
        )
        self.assertEqual(updated.status, HTTPStatus.OK)
        version = int(updated.body_json()["property"]["version"])

        boundary = "----SellerJourney"
        upload_body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="property_id"\r\n\r\n'
            f"{property_id}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="villa.jpg"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode("utf-8") + MINIMAL_JPEG_BYTES + f"\r\n--{boundary}--\r\n".encode("utf-8")
        uploaded = self.invoke(
            "/api/media/upload",
            method="POST",
            token=seller_token,
            raw_body=upload_body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(uploaded.status, HTTPStatus.CREATED)

        published = self.invoke(
            f"/api/properties/{property_id}/publish",
            method="POST",
            token=seller_token,
            body={"version": version},
        )
        self.assertEqual(published.status, HTTPStatus.OK)
        self.assertEqual(published.body_json()["property"]["status"], "published")
        version = int(published.body_json()["property"]["version"])

        modified = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=seller_token,
            body={"summary": "Updated seller summary.", "version": version},
        )
        self.assertEqual(modified.status, HTTPStatus.OK)
        version = int(modified.body_json()["property"]["version"])

        matches = self.invoke("/api/matches?city=Douala&limit=20")
        titles = [item["property"]["title"] for item in matches.body_json()["matches"]]
        self.assertIn("Seller Journey Villa", titles)

        archived = self.invoke(
            f"/api/properties/{property_id}",
            method="PATCH",
            token=seller_token,
            body={"status": "archived", "version": version},
        )
        self.assertEqual(archived.status, HTTPStatus.OK)
        self.assertEqual(archived.body_json()["property"]["status"], "archived")

        matches_after = self.invoke("/api/matches?city=Douala&limit=20")
        titles_after = [item["property"]["title"] for item in matches_after.body_json()["matches"]]
        self.assertNotIn("Seller Journey Villa", titles_after)

        persisted = self.invoke(f"/api/properties/{property_id}", token=seller_token)
        self.assertEqual(persisted.status, HTTPStatus.OK)
        self.assertEqual(persisted.body_json()["property"]["status"], "archived")


class BuyerJourneyTest(LawimTestHarness):
    def test_buyer_journey_search_match_negotiate_and_notify(self) -> None:
        admin_token = self.login(email="admin@lawim.local")
        org = self.invoke(
            "/api/organizations",
            method="POST",
            token=admin_token,
            body={"name": "Buyer Target Agency", "slug": "buyer-target-agency", "kind": "agency", "city": "Douala"},
        )
        org_id = int(org.body_json()["organization"]["id"])
        agent_token = self.register(
            email="listing.agent@lawim.local",
            full_name="Listing Agent",
            role="agent",
            organization_id=org_id,
        )
        listing = self.invoke(
            "/api/properties",
            method="POST",
            token=agent_token,
            body={
                "title": "Buyer Journey Target",
                "summary": "Published listing for buyer flow.",
                "city": "Douala",
                "country": "Cameroon",
                "price_min": 150000,
                "price_max": 200000,
                "property_type": "apartment",
                "bedrooms": 2,
                "status": "draft",
            },
        )
        property_id = int(listing.body_json()["property"]["id"])
        version = int(listing.body_json()["property"]["version"])
        self.invoke(
            f"/api/properties/{property_id}/publish",
            method="POST",
            token=agent_token,
            body={"version": version},
        )

        buyer_token = self.register(
            email="buyer.journey@lawim.local",
            full_name="Buyer Journey",
            role="owner",
        )

        search = self.invoke("/api/properties?city=Douala&status=published&property_type=apartment&limit=20")
        self.assertEqual(search.status, HTTPStatus.OK)
        search_titles = [row["title"] for row in search.body_json()["properties"]]
        self.assertIn("Buyer Journey Target", search_titles)

        matches = self.invoke(
            "/api/matches?city=Douala&budget_max=220000&bedrooms_min=2&limit=5",
            token=buyer_token,
        )
        self.assertEqual(matches.status, HTTPStatus.OK)
        match_titles = [item["property"]["title"] for item in matches.body_json()["matches"]]
        self.assertIn("Buyer Journey Target", match_titles)

        detail = self.invoke(f"/api/properties/{property_id}")
        self.assertEqual(detail.status, HTTPStatus.OK)
        self.assertIn("media", detail.body_json()["property"])

        conversation = self.invoke(
            "/api/conversations",
            method="POST",
            token=buyer_token,
            body={
                "property_id": property_id,
                "subject": "Purchase inquiry",
                "initial_message": "Is the price negotiable?",
            },
        )
        self.assertEqual(conversation.status, HTTPStatus.CREATED)
        conversation_id = int(conversation.body_json()["conversation"]["id"])

        negotiation = self.invoke(
            f"/api/conversations/{conversation_id}",
            method="PATCH",
            token=buyer_token,
            body={"negotiation_stage": "offer"},
        )
        self.assertEqual(negotiation.status, HTTPStatus.OK)
        self.assertEqual(negotiation.body_json()["conversation"]["negotiation_stage"], "offer")

        agent_reply = self.invoke(
            f"/api/conversations/{conversation_id}/messages",
            method="POST",
            token=agent_token,
            body={"body": "We can discuss a counter-offer."},
        )
        self.assertEqual(agent_reply.status, HTTPStatus.CREATED)

        notifications = self.invoke("/api/notifications?limit=20", token=buyer_token)
        kinds = {item["kind"] for item in notifications.body_json()["notifications"]}
        self.assertIn("match_found", kinds)
        self.assertIn("conversation_created", kinds)
        self.assertIn("message_received", kinds)


class AdminJourneyTest(LawimTestHarness):
    def test_admin_journey_supervision_audit_and_user_management(self) -> None:
        admin_token = self.login(email="admin@lawim.local")

        health = self.invoke("/api/health", token=admin_token)
        self.assertEqual(health.status, HTTPStatus.OK)
        self.assertIn("audit", health.body_json())

        metrics = self.invoke("/api/metrics", token=admin_token)
        self.assertEqual(metrics.status, HTTPStatus.OK)

        organization = self.invoke(
            "/api/organizations",
            method="POST",
            token=admin_token,
            body={"name": "Admin Supervised Org", "slug": "admin-supervised-org", "kind": "partner", "city": "Yaounde"},
        )
        organization_id = int(organization.body_json()["organization"]["id"])

        user = self.invoke(
            "/api/users",
            method="POST",
            token=admin_token,
            body={
                "email": "supervised.agent@lawim.local",
                "full_name": "Supervised Agent",
                "role": "agent",
                "password": "lawim-demo",
                "organization_id": organization_id,
            },
        )
        self.assertEqual(user.status, HTTPStatus.CREATED)

        users = self.invoke("/api/users?limit=50", token=admin_token)
        emails = [row["email"] for row in users.body_json()["users"]]
        self.assertIn("supervised.agent@lawim.local", emails)

        agent_token = self.login(email="supervised.agent@lawim.local")
        property_row = self.invoke(
            "/api/properties",
            method="POST",
            token=agent_token,
            body={
                "title": "Admin Supervised Listing",
                "summary": "Needs moderation.",
                "city": "Yaounde",
                "country": "Cameroon",
                "status": "published",
            },
        )
        property_id = int(property_row.body_json()["property"]["id"])

        owner_token = self.login(email="owner@lawim.local")
        self.invoke(
            "/api/conversations",
            method="POST",
            token=owner_token,
            body={
                "property_id": property_id,
                "subject": "Admin moderation probe",
                "initial_message": "Reporting listing",
            },
        )

        events_before = self.invoke("/api/events?limit=100", token=admin_token)
        self.assertEqual(events_before.status, HTTPStatus.OK)

        moderated = self.invoke(f"/api/properties/{property_id}", method="DELETE", token=admin_token)
        self.assertEqual(moderated.status, HTTPStatus.OK)
        self.assertTrue(moderated.body_json()["soft"])

        events_after = self.invoke("/api/events?limit=100", token=admin_token)
        event_kinds = {event["kind"] for event in events_after.body_json()["events"]}
        self.assertIn("property_soft_deleted", event_kinds)

        supervised = self.invoke("/api/properties?include_deleted=true&limit=50", token=admin_token)
        archived = next(item for item in supervised.body_json()["properties"] if item["id"] == property_id)
        self.assertEqual(archived["status"], "archived")
