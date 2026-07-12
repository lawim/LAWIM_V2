from __future__ import annotations

from dataclasses import replace
from http import HTTPStatus

from tests.lawim_harness import LawimTestHarness


class GreenApiWebhookTests(LawimTestHarness):
    def setUp(self) -> None:
        super().setUp()
        self.green_api_secret = "green-api-webhook-secret"
        self.green_api_webhook_url = "https://api.lawim.app/api/notifications/whatsapp/webhook"
        self.config = replace(
            self.config,
            green_api_webhook_secret=self.green_api_secret,
            green_api_webhook_url=self.green_api_webhook_url,
        )

    def _incoming_payload(self) -> dict[str, object]:
        return {
            "typeWebhook": "incomingMessageReceived",
            "instanceData": {
                "idInstance": 7107644927,
                "wid": "7107644927@c.us",
                "typeInstance": "whatsapp",
            },
            "timestamp": 1727698597,
            "idMessage": "3EB0608D6A2901063D63",
            "senderData": {
                "chatId": "237650000000@c.us",
                "sender": "237650000000@c.us",
                "senderName": "Test Sender",
                "senderContactName": "Test Sender",
            },
            "messageData": {
                "typeMessage": "textMessage",
                "textMessageData": {
                    "textMessage": "Bonjour LAWIM",
                },
            },
        }

    def _outgoing_api_payload(self) -> dict[str, object]:
        return {
            "typeWebhook": "outgoingAPIMessageReceived",
            "instanceData": {
                "idInstance": 7107644927,
                "wid": "7107644927@c.us",
                "typeInstance": "whatsapp",
            },
            "timestamp": 1727698598,
            "idMessage": "OUTGOING-API-1",
            "senderData": {
                "chatId": "237650000000@c.us",
                "sender": "237650000000@c.us",
                "senderName": "LAWIM",
            },
            "messageData": {
                "typeMessage": "textMessage",
                "textMessageData": {
                    "textMessage": "Ping Green API",
                },
            },
        }

    def _status_payload(self, status: str) -> dict[str, object]:
        return {
            "typeWebhook": "outgoingMessageStatus",
            "chatId": "237650000000@c.us",
            "instanceData": {
                "idInstance": 7107644927,
                "wid": "7107644927@c.us",
                "typeInstance": "whatsapp",
            },
            "timestamp": 1727698599,
            "idMessage": "OUTGOING-API-1",
            "status": status,
            "sendByApi": True,
        }

    def test_incoming_message_webhook_persists_message_and_event(self) -> None:
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")
        before_events = self.repository.scalar("SELECT COUNT(*) FROM communication_events")

        response = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._incoming_payload(),
            token=self.green_api_secret,
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        self.assertEqual(response.body_json()["status"], "ok")
        self.assertFalse(response.body_json()["duplicate"])
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_events"), before_events + 1)

        message_key = "green-api:message:3EB0608D6A2901063D63"
        message = self.repository.one("SELECT * FROM communication_messages WHERE message_key = ?", (message_key,))
        self.assertIsNotNone(message)
        assert message is not None
        self.assertEqual(str(message["channel_type"]), "whatsapp")
        self.assertEqual(str(message["direction"]), "inbound")
        self.assertEqual(str(message["status"]), "delivered")
        self.assertEqual(str(message["body"]), "Bonjour LAWIM")

    def test_webhook_missing_secret_is_rejected(self) -> None:
        response = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._incoming_payload(),
        )

        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(self.assert_error_shape(response)["code"], "missing_token")

    def test_webhook_incorrect_secret_is_rejected(self) -> None:
        response = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._incoming_payload(),
            token="wrong-secret",
        )

        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(self.assert_error_shape(response)["code"], "invalid_token")

    def test_invalid_payload_is_rejected(self) -> None:
        response = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            raw_body=b"not-json",
            headers={"Content-Type": "application/json"},
            token=self.green_api_secret,
        )

        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(self.assert_error_shape(response)["code"], "invalid_json")

    def test_unknown_webhook_type_is_ignored(self) -> None:
        before_events = self.repository.scalar("SELECT COUNT(*) FROM communication_events")
        response = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body={
                "typeWebhook": "mysteryWebhook",
                "instanceData": {
                    "idInstance": 7107644927,
                    "wid": "7107644927@c.us",
                    "typeInstance": "whatsapp",
                },
                "timestamp": 1727698600,
            },
            token=self.green_api_secret,
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        payload = response.body_json()
        self.assertEqual(payload["status"], "ignored")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_events"), before_events)

    def test_duplicate_incoming_message_is_idempotent(self) -> None:
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")
        before_events = self.repository.scalar("SELECT COUNT(*) FROM communication_events")

        first = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._incoming_payload(),
            token=self.green_api_secret,
        )
        second = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._incoming_payload(),
            token=self.green_api_secret,
        )

        self.assertEqual(first.status, HTTPStatus.OK)
        self.assertEqual(second.status, HTTPStatus.OK)
        self.assertFalse(first.body_json()["duplicate"])
        self.assertTrue(second.body_json()["duplicate"])
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_events"), before_events + 1)

    def test_outgoing_status_updates_message_state(self) -> None:
        first = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._outgoing_api_payload(),
            token=self.green_api_secret,
        )
        self.assertEqual(first.status, HTTPStatus.OK, msg=first.body_text())

        second = self.invoke(
            "/api/notifications/whatsapp/webhook",
            method="POST",
            body=self._status_payload("delivered"),
            token=self.green_api_secret,
        )
        self.assertEqual(second.status, HTTPStatus.OK, msg=second.body_text())

        message_key = "green-api:message:OUTGOING-API-1"
        message = self.repository.one("SELECT * FROM communication_messages WHERE message_key = ?", (message_key,))
        self.assertIsNotNone(message)
        assert message is not None
        self.assertEqual(str(message["direction"]), "outbound")
        self.assertEqual(str(message["status"]), "delivered")
        self.assertEqual(str(message["body"]), "Ping Green API")
