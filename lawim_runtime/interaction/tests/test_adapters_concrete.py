from lawim_runtime.interaction.adapters.whatsapp import WhatsAppAdapter
from lawim_runtime.interaction.adapters.telegram import TelegramAdapter
from lawim_runtime.interaction.adapters.web_api import WebAPIAdapter
from lawim_runtime.interaction.adapters import ChannelDeliveryRequest


def test_whatsapp_parse_text():
    adapter = WhatsAppAdapter()
    payload = {
        "messageData": {
            "textMessageData": {"textMessage": "Je cherche un appartement"},
            "typeMessage": "textMessage",
        },
        "senderData": {
            "chatId": "237600000000@c.us",
            "sender": "237600000000",
            "senderName": "Jean",
        },
        "idMessage": "msg-wa-001",
    }
    env = adapter.parse_webhook(payload)
    assert env is not None
    assert env.channel == "whatsapp"
    assert env.raw_content == "Je cherche un appartement"
    assert env.external_user_id == "237600000000"
    assert env.external_message_id == "msg-wa-001"


def test_whatsapp_parse_no_id():
    adapter = WhatsAppAdapter()
    payload = {
        "messageData": {
            "textMessageData": {"textMessage": "hello"},
            "typeMessage": "textMessage",
        },
        "senderData": {
            "chatId": "237600000000@c.us",
            "sender": "237600000000",
        },
    }
    env = adapter.parse_webhook(payload)
    assert env is not None
    assert env.external_message_id != ""


def test_whatsapp_extract_identifiers():
    adapter = WhatsAppAdapter()
    payload = {
        "senderData": {
            "sender": "237600000000",
            "chatId": "237600000000@c.us",
            "senderName": "Paul",
        },
    }
    ids = adapter.extract_identifiers(payload)
    assert ids["channel"] == "whatsapp"
    assert ids["external_user_id"] == "237600000000"


def test_whatsapp_send():
    adapter = WhatsAppAdapter()
    req = ChannelDeliveryRequest(
        channel="whatsapp",
        recipient_id="237600000000",
        text="Bonjour",
        correlation_id="corr-001",
    )
    result = adapter.send(req)
    assert result.success
    assert result.provider_message_id != ""


def test_whatsapp_send_missing_recipient():
    adapter = WhatsAppAdapter()
    req = ChannelDeliveryRequest(channel="whatsapp", text="Bonjour")
    result = adapter.send(req)
    assert not result.success
    assert "recipient" in result.error


def test_telegram_parse_text():
    adapter = TelegramAdapter()
    payload = {
        "message": {
            "message_id": 123,
            "from": {"id": 456, "first_name": "Alice", "is_bot": False},
            "chat": {"id": -789},
            "text": "Bonjour Telegram",
        },
    }
    env = adapter.parse_webhook(payload)
    assert env is not None
    assert env.channel == "telegram"
    assert env.raw_content == "Bonjour Telegram"
    assert env.external_user_id == "456"
    assert env.external_thread_id == "-789"


def test_telegram_parse_callback():
    adapter = TelegramAdapter()
    payload = {
        "callback_query": {
            "id": "cq-001",
            "from": {"id": 456, "first_name": "Alice", "is_bot": False},
            "message": {
                "message_id": 124,
                "chat": {"id": -789},
            },
            "data": "select_option_1",
        },
    }
    env = adapter.parse_webhook(payload)
    assert env is not None
    assert env.message_type.value == "BUTTON"
    assert env.raw_content == "select_option_1"
    assert env.external_message_id == "cq-001"


def test_telegram_extract_identifiers():
    adapter = TelegramAdapter()
    payload = {
        "message": {
            "from": {"id": 456, "first_name": "Alice"},
            "chat": {"id": -789},
        },
    }
    ids = adapter.extract_identifiers(payload)
    assert ids["channel"] == "telegram"
    assert ids["external_user_id"] == "456"


def test_telegram_send():
    adapter = TelegramAdapter()
    req = ChannelDeliveryRequest(
        channel="telegram",
        recipient_id="-789",
        text="Hello",
        correlation_id="corr-002",
    )
    result = adapter.send(req)
    assert result.success
    assert result.provider_message_id != ""


def test_telegram_send_missing_recipient():
    adapter = TelegramAdapter()
    req = ChannelDeliveryRequest(channel="telegram", text="Hello")
    result = adapter.send(req)
    assert not result.success


def test_web_api_parse():
    adapter = WebAPIAdapter()
    payload = {
        "message": "Je cherche un terrain",
        "user_id": "user-001",
        "session_id": "session-001",
    }
    headers = {"User-Agent": "Mozilla/5.0", "X-Forwarded-For": "127.0.0.1"}
    env = adapter.parse_webhook(payload, headers)
    assert env is not None
    assert env.channel == "web_api"
    assert env.raw_content == "Je cherche un terrain"
    assert env.external_user_id == "user-001"


def test_web_api_parse_with_correlation():
    adapter = WebAPIAdapter()
    payload = {
        "text": "hello",
        "userId": "user-002",
        "correlationId": "corr-web-001",
    }
    env = adapter.parse_webhook(payload)
    assert env is not None
    assert env.correlation_id == "corr-web-001"


def test_web_api_extract_identifiers():
    adapter = WebAPIAdapter()
    payload = {"user_id": "user-001", "session_id": "session-001"}
    ids = adapter.extract_identifiers(payload)
    assert ids["channel"] == "web_api"


def test_web_api_send():
    adapter = WebAPIAdapter()
    req = ChannelDeliveryRequest(
        channel="web_api",
        text='{"response": "ok"}',
        correlation_id="corr-003",
    )
    result = adapter.send(req)
    assert result.success
    assert result.provider_message_id != ""
