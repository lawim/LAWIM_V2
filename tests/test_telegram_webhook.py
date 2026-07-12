from __future__ import annotations

from dataclasses import replace
from http import HTTPStatus

from tests.lawim_harness import LawimTestHarness


class TelegramWebhookTests(LawimTestHarness):
    def setUp(self) -> None:
        super().setUp()
        self.telegram_secret = "telegram-webhook-secret"
        self.telegram_webhook_url = "https://api.lawim.app/api/notifications/telegram/webhook"
        self.config = replace(
            self.config,
            telegram_webhook_secret=self.telegram_secret,
            telegram_webhook_url=self.telegram_webhook_url,
        )

    def _message_payload(self) -> dict[str, object]:
        return {
            "update_id": 1000001,
            "message": {
                "message_id": 42,
                "date": 1727698597,
                "chat": {
                    "id": 123456789,
                    "type": "private",
                    "username": "tester",
                },
                "from": {
                    "id": 987654321,
                    "is_bot": False,
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "username": "janedoe",
                },
                "text": "Bonjour LAWIM sur Telegram",
            },
        }

    def _state_payload(self, status: str) -> dict[str, object]:
        return {
            "update_id": 1000002,
            "my_chat_member": {
                "chat": {
                    "id": -1001234567890,
                    "title": "LAWIM Group",
                    "type": "group",
                },
                "from": {
                    "id": 987654321,
                    "is_bot": False,
                    "first_name": "Jane",
                    "username": "janedoe",
                },
                "date": 1727698600,
                "old_chat_member": {
                    "status": "left",
                    "user": {
                        "id": 123,
                        "is_bot": True,
                        "first_name": "LAWIM",
                        "username": "lawim_bot",
                    },
                },
                "new_chat_member": {
                    "status": status,
                    "user": {
                        "id": 123,
                        "is_bot": True,
                        "first_name": "LAWIM",
                        "username": "lawim_bot",
                    },
                },
            },
        }

    def test_incoming_message_webhook_persists_message_and_event(self) -> None:
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")
        before_events = self.repository.scalar("SELECT COUNT(*) FROM communication_events")
        before_updates = self.repository.scalar("SELECT COUNT(*) FROM telegram_updates")

        response = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body=self._message_payload(),
            headers={"X-Telegram-Bot-Api-Secret-Token": self.telegram_secret},
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        body = response.body_json()
        self.assertEqual(body["status"], "ok")
        self.assertFalse(body["duplicate"])
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_events"), before_events + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM telegram_updates"), before_updates + 1)

        message_key = "telegram:message:123456789:42"
        message = self.repository.one("SELECT * FROM communication_messages WHERE message_key = ?", (message_key,))
        self.assertIsNotNone(message)
        assert message is not None
        self.assertEqual(str(message["channel_type"]), "telegram")
        self.assertEqual(str(message["direction"]), "inbound")
        self.assertEqual(str(message["status"]), "delivered")
        self.assertEqual(str(message["body"]), "Bonjour LAWIM sur Telegram")

    def test_webhook_missing_secret_is_rejected(self) -> None:
        response = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body=self._message_payload(),
        )

        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(self.assert_error_shape(response)["code"], "missing_token")

    def test_webhook_incorrect_secret_is_rejected(self) -> None:
        response = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body=self._message_payload(),
            headers={"X-Telegram-Bot-Api-Secret-Token": "wrong-secret"},
        )

        self.assertEqual(response.status, HTTPStatus.UNAUTHORIZED)
        self.assertEqual(self.assert_error_shape(response)["code"], "invalid_token")

    def test_invalid_payload_is_rejected(self) -> None:
        response = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            raw_body=b"not-json",
            headers={
                "Content-Type": "application/json",
                "X-Telegram-Bot-Api-Secret-Token": self.telegram_secret,
            },
        )

        self.assertEqual(response.status, HTTPStatus.BAD_REQUEST)
        self.assertEqual(self.assert_error_shape(response)["code"], "invalid_json")

    def test_unknown_update_type_is_ignored(self) -> None:
        before_updates = self.repository.scalar("SELECT COUNT(*) FROM telegram_updates")
        response = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body={
                "update_id": 1000003,
                "mystery_update": {
                    "value": "ignored",
                },
            },
            headers={"X-Telegram-Bot-Api-Secret-Token": self.telegram_secret},
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        payload = response.body_json()
        self.assertEqual(payload["status"], "ignored")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM telegram_updates"), before_updates)

    def test_duplicate_message_update_is_idempotent(self) -> None:
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")
        before_events = self.repository.scalar("SELECT COUNT(*) FROM communication_events")
        before_updates = self.repository.scalar("SELECT COUNT(*) FROM telegram_updates")

        first = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body=self._message_payload(),
            headers={"X-Telegram-Bot-Api-Secret-Token": self.telegram_secret},
        )
        second = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body=self._message_payload(),
            headers={"X-Telegram-Bot-Api-Secret-Token": self.telegram_secret},
        )

        self.assertEqual(first.status, HTTPStatus.OK)
        self.assertEqual(second.status, HTTPStatus.OK)
        self.assertFalse(first.body_json()["duplicate"])
        self.assertTrue(second.body_json()["duplicate"])
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_events"), before_events + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM telegram_updates"), before_updates + 1)

    def test_state_update_is_processed(self) -> None:
        before_messages = self.repository.scalar("SELECT COUNT(*) FROM communication_messages")
        before_events = self.repository.scalar("SELECT COUNT(*) FROM communication_events")
        before_updates = self.repository.scalar("SELECT COUNT(*) FROM telegram_updates")

        response = self.invoke(
            "/api/notifications/telegram/webhook",
            method="POST",
            body=self._state_payload("member"),
            headers={"X-Telegram-Bot-Api-Secret-Token": self.telegram_secret},
        )

        self.assertEqual(response.status, HTTPStatus.OK, msg=response.body_text())
        body = response.body_json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_messages"), before_messages)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM communication_events"), before_events + 1)
        self.assertEqual(self.repository.scalar("SELECT COUNT(*) FROM telegram_updates"), before_updates + 1)
