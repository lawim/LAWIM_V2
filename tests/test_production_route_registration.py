from __future__ import annotations

from pathlib import Path


SERVER_PY = Path("code/lawim_v2/server.py")


def _routes(path: str) -> list[str]:
    content = SERVER_PY.read_text(encoding="utf-8")
    lines = content.splitlines()
    routes = []
    for i, line in enumerate(lines, 1):
        if path in line and ('== "' in line or 'in {' in line):
            routes.append(f"{i}: {line.strip()}")
    return routes


def test_health_route_present():
    assert _routes("/health"), "/health route must be defined"


def test_healthz_route_present():
    assert _routes("/healthz"), "/healthz route must be defined"


def test_readyz_route_present():
    assert _routes("/readyz"), "/readyz route must be defined"


def test_web_conversation_list_route_present():
    assert _routes("/api/conversations")


def test_web_conversation_messages_route_present():
    assert _routes("/api/conversations")


def test_telegram_webhook_route_present():
    assert _routes("/api/notifications/telegram/webhook")


def test_whatsapp_webhook_route_present():
    assert _routes("/api/notifications/whatsapp/webhook")


def test_v3_conversation_route_present():
    assert _routes("/api/v3/conversations")


def test_v3_message_post_route_present():
    content = SERVER_PY.read_text(encoding="utf-8")
    assert '"message"' in content or "'message'" in content
