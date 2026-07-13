from __future__ import annotations

import json
import socket
import tempfile
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from lawim_v2.bootstrap import build_runtime
from lawim_v2.config import AppConfig
from lawim_v2.communication.delivery import (
    DeliveryCall,
    mask_delivery_recipient,
    sanitize_delivery_url,
    send_green_api_message,
    send_telegram_message,
)


class CommunicationDeliveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        db_path = Path(self.tempdir.name) / "lawim.sqlite3"
        media_path = Path(self.tempdir.name) / "media"
        config = AppConfig.for_test(db_path=db_path, media_storage_path=media_path)
        self.runtime = build_runtime(config)

    def tearDown(self) -> None:
        self.runtime.close()
        self.tempdir.cleanup()

    def test_mask_delivery_recipient_masks_phone_and_chat_ids(self) -> None:
        self.assertEqual(mask_delivery_recipient("+237686822667"), "+237***667")
        self.assertEqual(mask_delivery_recipient("237686822667@c.us"), "237***667@c.us")
        self.assertEqual(mask_delivery_recipient("12345"), "12***45")

    def test_sanitize_delivery_url_masks_provider_tokens(self) -> None:
        whatsapp_url = "https://7107.api.greenapi.com/waInstance7107644927/sendMessage/super-secret-token"
        telegram_url = "https://api.telegram.org/bot123456:ABCDEF/sendMessage"
        self.assertIn("[redacted]", sanitize_delivery_url(whatsapp_url))
        self.assertIn("[redacted]", sanitize_delivery_url(telegram_url))

    @patch("lawim_v2.communication.delivery.socket.getaddrinfo")
    def test_resolve_ipv4_prefers_ipv4(self, mock_getaddrinfo: unittest.mock.MagicMock) -> None:
        from lawim_v2.communication.delivery import _resolve_ipv4

        mock_getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("203.0.113.10", 443)),
        ]
        self.assertEqual(_resolve_ipv4("api.telegram.org", 443), "203.0.113.10")

    @patch("lawim_v2.communication.delivery._request_json_ipv4_first")
    def test_send_green_api_message_extracts_message_id(self, mock_request: unittest.mock.MagicMock) -> None:
        mock_request.return_value = DeliveryCall(
            provider="green_api",
            method="POST",
            url="https://7107.api.greenapi.com/waInstance7107644927/sendMessage/super-secret-token",
            sanitized_url="https://7107.api.greenapi.com/waInstance7107644927/sendMessage/[redacted]",
            ok=True,
            http_status=200,
            response_text='{"idMessage":"green-123"}',
            response_json={"idMessage": "green-123"},
            response_headers={"Content-Type": "application/json"},
            request_headers={"Content-Type": "application/json"},
            request_payload={"chatId": "237686822667@c.us", "message": "Bonjour"},
            resolved_ipv4="203.0.113.20",
            latency_ms=15,
        )
        result = send_green_api_message(
            api_url="https://7107.api.greenapi.com",
            id_instance="7107644927",
            token_instance="super-secret-token",
            chat_id="237686822667@c.us",
            message="Bonjour",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.provider_message_id, "green-123")
        self.assertEqual(result.delivery_status, "sent")
        self.assertEqual(result.resolved_ipv4, "203.0.113.20")
        self.assertEqual(mock_request.call_args.kwargs["payload"]["chatId"], "237686822667@c.us")

    @patch("lawim_v2.communication.delivery._request_json_ipv4_first")
    def test_send_telegram_message_extracts_message_id(self, mock_request: unittest.mock.MagicMock) -> None:
        mock_request.return_value = DeliveryCall(
            provider="telegram",
            method="POST",
            url="https://api.telegram.org/bot123456:ABCDEF/sendMessage",
            sanitized_url="https://api.telegram.org/bot[redacted]/sendMessage",
            ok=True,
            http_status=200,
            response_text='{"ok":true,"result":{"message_id":987}}',
            response_json={"ok": True, "result": {"message_id": 987}},
            response_headers={"Content-Type": "application/json"},
            request_headers={"Content-Type": "application/json"},
            request_payload={"chat_id": "12345", "text": "Bonjour"},
            resolved_ipv4="149.154.167.220",
            latency_ms=12,
        )
        result = send_telegram_message(
            bot_token="123456:ABCDEF",
            chat_id="12345",
            message="Bonjour",
        )
        self.assertTrue(result.ok)
        self.assertEqual(result.provider_message_id, "987")
        self.assertEqual(result.delivery_status, "sent")
        self.assertEqual(result.resolved_ipv4, "149.154.167.220")
        self.assertEqual(mock_request.call_args.kwargs["payload"]["chat_id"], "12345")

    @patch("lawim_v2.communication.delivery._request_json_ipv4_first")
    def test_send_telegram_message_extracts_error_description(self, mock_request: unittest.mock.MagicMock) -> None:
        mock_request.return_value = DeliveryCall(
            provider="telegram",
            method="POST",
            url="https://api.telegram.org/bot123456:ABCDEF/sendMessage",
            sanitized_url="https://api.telegram.org/bot[redacted]/sendMessage",
            ok=False,
            http_status=400,
            response_text='{"ok":false,"error_code":400,"description":"Bad Request: chat not found"}',
            response_json={"ok": False, "error_code": 400, "description": "Bad Request: chat not found"},
            response_headers={"Content-Type": "application/json"},
            request_headers={"Content-Type": "application/json"},
            request_payload={"chat_id": "12345", "text": "Bonjour"},
            resolved_ipv4="149.154.166.110",
            latency_ms=12,
        )
        result = send_telegram_message(
            bot_token="123456:ABCDEF",
            chat_id="12345",
            message="Bonjour",
        )
        self.assertFalse(result.ok)
        self.assertEqual(result.error_type, "telegram_http_400")
        self.assertEqual(result.error_message, "Bad Request: chat not found")

    @patch("lawim_v2.communication.repository.should_use_real_delivery", return_value=True)
    @patch("lawim_v2.communication.repository.send_green_api_message")
    def test_repository_send_whatsapp_records_sanitized_delivery(self, mock_send: unittest.mock.MagicMock, _gate: unittest.mock.MagicMock) -> None:
        mock_send.return_value = DeliveryCall(
            provider="green_api",
            method="POST",
            url="https://7107.api.greenapi.com/waInstance7107644927/sendMessage/super-secret-token",
            sanitized_url="https://7107.api.greenapi.com/waInstance7107644927/sendMessage/[redacted]",
            ok=True,
            http_status=200,
            response_text='{"idMessage":"green-456"}',
            response_json={"idMessage": "green-456"},
            response_headers={"Content-Type": "application/json"},
            request_headers={"Content-Type": "application/json"},
            request_payload={"chatId": "237686822667@c.us", "message": "Bonjour"},
            resolved_ipv4="203.0.113.20",
            latency_ms=15,
            provider_message_id="green-456",
            delivery_status="sent",
        )
        with patch.dict(
            os.environ,
            {
                "APP_ENV": "production",
                "GREEN_API_API_URL": "https://7107.api.greenapi.com",
                "GREEN_API_ID_INSTANCE": "7107644927",
                "GREEN_API_TOKEN_INSTANCE": "super-secret-token",
            },
            clear=False,
        ):
            result = self.runtime.repository.send_whatsapp(to_number="+237686822667", body="Bonjour LAWIM")
        self.assertEqual(result["delivery_status"], "sent")
        self.assertEqual(result["delivery"]["provider_message_id"], "green-456")
        self.assertEqual(
            self.runtime.repository.scalar("SELECT COUNT(*) FROM whatsapp_delivery_logs"),
            1,
        )
        row = self.runtime.repository.one("SELECT provider_response FROM whatsapp_delivery_logs ORDER BY id DESC LIMIT 1")
        provider_response = json.loads(str(row["provider_response"]))
        self.assertEqual(provider_response["url"], "https://7107.api.greenapi.com/waInstance7107644927/sendMessage/[redacted]")
        self.assertEqual(provider_response["request_payload"]["chatId"], "237***667@c.us")

    @patch("lawim_v2.communication.repository.should_use_real_delivery", return_value=True)
    @patch("lawim_v2.communication.repository.send_telegram_message")
    def test_repository_send_telegram_records_sanitized_delivery(self, mock_send: unittest.mock.MagicMock, _gate: unittest.mock.MagicMock) -> None:
        mock_send.return_value = DeliveryCall(
            provider="telegram",
            method="POST",
            url="https://api.telegram.org/bot123456:ABCDEF/sendMessage",
            sanitized_url="https://api.telegram.org/bot[redacted]/sendMessage",
            ok=True,
            http_status=200,
            response_text='{"ok":true,"result":{"message_id":654}}',
            response_json={"ok": True, "result": {"message_id": 654}},
            response_headers={"Content-Type": "application/json"},
            request_headers={"Content-Type": "application/json"},
            request_payload={"chat_id": "12345", "text": "Bonjour"},
            resolved_ipv4="149.154.167.220",
            latency_ms=12,
            provider_message_id="654",
            delivery_status="sent",
        )
        with patch.dict(
            os.environ,
            {
                "APP_ENV": "production",
                "TELEGRAM_BOT_TOKEN": "123456:ABCDEF",
            },
            clear=False,
        ):
            result = self.runtime.repository.send_telegram(chat_id="12345", body="Bonjour LAWIM")
        self.assertEqual(result["delivery_status"], "sent")
        self.assertEqual(result["delivery"]["provider_message_id"], "654")
        row = self.runtime.repository.one("SELECT metadata_json FROM telegram_messages ORDER BY id DESC LIMIT 1")
        metadata = json.loads(str(row["metadata_json"]))
        self.assertEqual(metadata["provider_response"]["url"], "https://api.telegram.org/bot[redacted]/sendMessage")
        self.assertEqual(metadata["provider_response"]["request_payload"]["chat_id"], "12***45")


if __name__ == "__main__":
    unittest.main()
