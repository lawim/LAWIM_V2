from __future__ import annotations

import unittest

from lawim_v2.communication.telegram_webhook import (
    build_event_key,
    build_message_key,
    canonical_payload,
    extract_message_body,
    normalize_webhook_payload,
    validate_webhook_authorization,
)


class TelegramWebhookTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = {
            "update_id": 1,
            "message": {
                "message_id": 2,
                "date": 1,
                "chat": {"id": 123, "type": "private"},
                "from": {"id": 456, "is_bot": False, "first_name": "A"},
                "text": "Bonjour",
            },
        }

    def test_validate_webhook_authorization_compares_secret_in_constant_time(self) -> None:
        self.assertTrue(validate_webhook_authorization("expected", "expected"))
        self.assertFalse(validate_webhook_authorization("expected", "different"))
        self.assertFalse(validate_webhook_authorization(None, "expected"))

    def test_normalize_payload_extracts_body_and_keys(self) -> None:
        normalized = normalize_webhook_payload(self.payload)
        self.assertEqual(normalized["message_body"], "Bonjour")
        self.assertEqual(normalized["chat_id"], "123")
        self.assertEqual(normalized["user_id"], 456)
        self.assertEqual(extract_message_body(normalized["message_data"]), "Bonjour")
        self.assertTrue(build_message_key(normalized))
        self.assertTrue(build_event_key(normalized))

    def test_canonical_payload_is_order_independent(self) -> None:
        first = canonical_payload({"b": 2, "a": 1})
        second = canonical_payload({"a": 1, "b": 2})
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
