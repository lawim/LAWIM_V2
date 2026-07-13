from __future__ import annotations

import unittest

from lawim_v2.communication.green_api import (
    build_event_key,
    build_message_key,
    canonical_payload,
    extract_message_body,
    normalize_webhook_payload,
    validate_webhook_authorization,
)


class GreenApiWebhookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "typeWebhook": "incomingMessageReceived",
            "timestamp": 1,
            "idMessage": "msg-1",
            "senderData": {
                "chatId": "12345@c.us",
                "sender": "12345@c.us",
            },
            "messageData": {
                "textMessageData": {"textMessage": "Bonjour"},
            },
        }

    def test_validate_webhook_authorization_compares_secret_in_constant_time(self) -> None:
        self.assertTrue(validate_webhook_authorization("Bearer expected", "expected"))
        self.assertFalse(validate_webhook_authorization("Bearer expected", "different"))
        self.assertFalse(validate_webhook_authorization(None, "expected"))

    def test_normalize_payload_extracts_body_and_keys(self) -> None:
        normalized = normalize_webhook_payload(self.payload)
        self.assertEqual(normalized["message_body"], "Bonjour")
        self.assertEqual(normalized["chat_id"], "12345@c.us")
        self.assertEqual(normalized["id_message"], "msg-1")
        self.assertEqual(extract_message_body(normalized["message_data"]), "Bonjour")
        self.assertTrue(build_message_key(normalized))
        self.assertTrue(build_event_key(normalized))

    def test_canonical_payload_is_order_independent(self) -> None:
        first = canonical_payload({"b": 2, "a": 1})
        second = canonical_payload({"a": 1, "b": 2})
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
