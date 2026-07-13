from __future__ import annotations

from dataclasses import asdict, dataclass
import http.client
import json
import logging
import os
import re
from hashlib import sha256
import socket
import ssl
import time
from typing import Any
from urllib.parse import urlsplit, urlunsplit

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class DeliveryCall:
    provider: str
    method: str
    url: str
    sanitized_url: str
    ok: bool
    http_status: int | None
    response_text: str
    response_json: dict[str, Any] | None
    response_headers: dict[str, str]
    request_headers: dict[str, str]
    request_payload: dict[str, Any]
    resolved_ipv4: str | None
    latency_ms: int
    error_type: str | None = None
    error_message: str | None = None
    provider_message_id: str = ""
    delivery_status: str = "failed"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def sanitize_delivery_record(call: DeliveryCall, *, recipient: str | None = None) -> dict[str, object]:
    record = call.to_dict()
    record["url"] = record.get("sanitized_url") or record.get("url")
    payload = dict(record.get("request_payload") or {})
    if "chatId" in payload:
        payload["chatId"] = mask_delivery_recipient(str(payload["chatId"]))
    if "chat_id" in payload:
        payload["chat_id"] = mask_delivery_recipient(str(payload["chat_id"]))
    if "to_number" in payload:
        payload["to_number"] = mask_delivery_recipient(str(payload["to_number"]))
    if recipient is not None:
        record["recipient"] = mask_delivery_recipient(recipient)
    record["request_payload"] = payload
    record["request_headers"] = {key: value for key, value in (record.get("request_headers") or {}).items()}
    return record


def mask_delivery_recipient(value: str | None) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    suffix = ""
    for marker in ("@c.us", "@g.us", "@telegram", "@bot"):
        if text.endswith(marker):
            suffix = marker
            text = text[: -len(marker)]
            break
    prefix = ""
    if text.startswith("+"):
        prefix = "+"
        text = text[1:]
    digits = re.sub(r"\D", "", text)
    if not digits:
        return f"{prefix}[redacted]{suffix}"
    if len(digits) <= 6:
        return f"{prefix}{digits[:2]}***{digits[-2:]}{suffix}"
    return f"{prefix}{digits[:3]}***{digits[-3:]}{suffix}"


def sanitize_delivery_url(url: str) -> str:
    parsed = urlsplit(url)
    path = parsed.path
    if "api.telegram.org" in parsed.netloc and path.startswith("/bot"):
        path = re.sub(r"^/bot[^/]+", "/bot[redacted]", path)
    elif "greenapi.com" in parsed.netloc and "/waInstance" in path:
        path = re.sub(r"(/waInstance\d+/(?:[^/]+))/[^/?#]+", r"\1/[redacted]", path)
    return urlunsplit((parsed.scheme, parsed.netloc, path, parsed.query, parsed.fragment))


def _resolve_ipv4(host: str, port: int) -> str:
    infos = socket.getaddrinfo(host, port, family=socket.AF_INET, type=socket.SOCK_STREAM)
    if not infos:
        raise OSError(f"No IPv4 address found for {host}")
    return str(infos[0][4][0])


class _IPv4HTTPConnection(http.client.HTTPConnection):
    def __init__(self, host: str, port: int, *, timeout: float, resolved_ipv4: str | None = None) -> None:
        super().__init__(host, port=port, timeout=timeout)
        self._resolved_ipv4 = resolved_ipv4

    def connect(self) -> None:  # pragma: no cover - exercised via integration tests
        resolved = self._resolved_ipv4 or _resolve_ipv4(self.host, self.port)
        self._resolved_ipv4 = resolved
        self.sock = socket.create_connection((resolved, self.port), self.timeout, self.source_address)


class _IPv4HTTPSConnection(http.client.HTTPSConnection):
    def __init__(self, host: str, port: int, *, timeout: float, resolved_ipv4: str | None = None) -> None:
        super().__init__(host, port=port, timeout=timeout)
        self._resolved_ipv4 = resolved_ipv4

    def connect(self) -> None:  # pragma: no cover - exercised via integration tests
        resolved = self._resolved_ipv4 or _resolve_ipv4(self.host, self.port)
        self._resolved_ipv4 = resolved
        sock = socket.create_connection((resolved, self.port), self.timeout, self.source_address)
        if self._tunnel_host:  # pragma: no cover - not used for LAWIM
            self.sock = sock
            self._tunnel()
            return
        self.sock = self._context.wrap_socket(sock, server_hostname=self.host)


def _decode_json(text: str, content_type: str | None = None) -> dict[str, Any] | None:
    if not text.strip():
        return None
    lowered = (content_type or "").lower()
    if "json" not in lowered and not text.lstrip().startswith(("{", "[")):
        return None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else {"data": parsed}


def _request_json_ipv4_first(
    *,
    provider: str,
    method: str,
    url: str,
    payload: dict[str, Any] | None,
    headers: dict[str, str] | None = None,
    timeout_seconds: int = 30,
) -> DeliveryCall:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"Unsupported URL scheme for {provider}: {parsed.scheme!r}")
    if not parsed.hostname:
        raise ValueError(f"Missing hostname for {provider}")

    request_headers = {
        "Accept": "application/json",
        "User-Agent": "LAWIM_V2/1.0",
    }
    if payload is not None:
        request_headers["Content-Type"] = "application/json"
    if headers:
        request_headers.update(headers)

    body = json.dumps(payload or {}, ensure_ascii=False).encode("utf-8") if payload is not None else None
    path = urlunsplit(("", "", parsed.path or "/", parsed.query, parsed.fragment))
    port = int(parsed.port or (443 if parsed.scheme == "https" else 80))
    resolved_ipv4 = _resolve_ipv4(parsed.hostname, port)
    connection_cls: type[http.client.HTTPConnection]
    if parsed.scheme == "https":
        connection_cls = _IPv4HTTPSConnection
    else:
        connection_cls = _IPv4HTTPConnection

    conn = connection_cls(parsed.hostname, port, timeout=float(timeout_seconds), resolved_ipv4=resolved_ipv4)
    started = time.perf_counter()
    try:
        conn.request(method.upper(), path, body=body, headers=request_headers)
        response = conn.getresponse()
        raw = response.read()
        response_text = raw.decode("utf-8", errors="replace")
        response_headers = {key: value for key, value in response.headers.items()}
        http_status = int(getattr(response, "status", 0) or 0)
        response_json = _decode_json(response_text, response_headers.get("Content-Type"))
        ok = 200 <= http_status < 300
        return DeliveryCall(
            provider=provider,
            method=method.upper(),
            url=url,
            sanitized_url=sanitize_delivery_url(url),
            ok=ok,
            http_status=http_status,
            response_text=response_text,
            response_json=response_json,
            response_headers=response_headers,
            request_headers=dict(request_headers),
            request_payload=dict(payload or {}),
            resolved_ipv4=resolved_ipv4,
            latency_ms=int((time.perf_counter() - started) * 1000),
        )
    except Exception as exc:
        return DeliveryCall(
            provider=provider,
            method=method.upper(),
            url=url,
            sanitized_url=sanitize_delivery_url(url),
            ok=False,
            http_status=None,
            response_text="",
            response_json=None,
            response_headers={},
            request_headers=dict(request_headers),
            request_payload=dict(payload or {}),
            resolved_ipv4=resolved_ipv4,
            latency_ms=int((time.perf_counter() - started) * 1000),
            error_type=exc.__class__.__name__,
            error_message=str(exc),
        )
    finally:
        try:
            conn.close()
        except Exception:  # pragma: no cover - defensive cleanup
            pass


def green_api_chat_id(phone_number: str) -> str:
    text = str(phone_number or "").strip()
    if not text:
        return ""
    if text.endswith("@c.us"):
        return text
    digits = re.sub(r"\D", "", text)
    if not digits:
        return text
    return f"{digits}@c.us"


def send_green_api_message(
    *,
    api_url: str,
    id_instance: str,
    token_instance: str,
    chat_id: str,
    message: str,
    timeout_seconds: int = 30,
) -> DeliveryCall:
    url = f"{api_url.rstrip('/')}/waInstance{id_instance}/sendMessage/{token_instance}"
    payload = {"chatId": chat_id, "message": message}
    call = _request_json_ipv4_first(
        provider="green_api",
        method="POST",
        url=url,
        payload=payload,
        timeout_seconds=timeout_seconds,
    )
    response = call.response_json or {}
    provider_message_id = str(
        response.get("idMessage")
        or response.get("id_message")
        or response.get("messageId")
        or response.get("message_id")
        or ""
    ).strip()
    success = call.ok and bool(provider_message_id)
    error_message = None
    if not success:
        error_message = (
            str(response.get("description") or response.get("message") or call.response_text or "").strip() or None
        )
    error_type = None if success else f"green_api_http_{call.http_status or 'error'}"
    return DeliveryCall(
        **{
            **call.to_dict(),
            "ok": success,
            "error_type": error_type,
            "error_message": error_message,
            "provider_message_id": provider_message_id,
            "delivery_status": "sent" if success else "failed",
        }
    )


def send_telegram_message(
    *,
    bot_token: str,
    chat_id: str,
    message: str,
    timeout_seconds: int = 30,
) -> DeliveryCall:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    call = _request_json_ipv4_first(
        provider="telegram",
        method="POST",
        url=url,
        payload=payload,
        timeout_seconds=timeout_seconds,
    )
    response = call.response_json or {}
    response_result = response.get("result") if isinstance(response.get("result"), dict) else {}
    provider_message_id = str(
        response_result.get("message_id")
        if isinstance(response_result, dict)
        else ""
    ).strip()
    telegram_ok = bool(response.get("ok", False))
    success = call.ok and telegram_ok and bool(provider_message_id)
    error_message = None
    if not success:
        error_message = (
            str(response.get("description") or response.get("message") or call.response_text or "").strip() or None
        )
    error_type = None if success else f"telegram_http_{call.http_status or 'error'}"
    return DeliveryCall(
        **{
            **call.to_dict(),
            "ok": success,
            "error_type": error_type,
            "error_message": error_message,
            "provider_message_id": provider_message_id,
            "delivery_status": "sent" if success else "failed",
        }
    )


def dry_run_delivery(
    *,
    provider: str,
    method: str,
    url: str,
    payload: dict[str, Any],
    recipient: str,
) -> DeliveryCall:
    fingerprint = sha256(
        "|".join(
            [
                provider,
                method.upper(),
                str(recipient or ""),
                str(payload.get("body") or ""),
                str(payload.get("chatId") or payload.get("chat_id") or payload.get("to_number") or ""),
            ]
        ).encode("utf-8")
    ).hexdigest()
    message_id = f"dry-run-{fingerprint[:12]}"
    return DeliveryCall(
        provider=provider,
        method=method.upper(),
        url=url,
        sanitized_url=sanitize_delivery_url(url),
        ok=True,
        http_status=200,
        response_text=json.dumps({"ok": True, "dry_run": True}, ensure_ascii=False),
        response_json={"ok": True, "dry_run": True},
        response_headers={},
        request_headers={"Content-Type": "application/json", "Accept": "application/json"},
        request_payload=dict(payload),
        resolved_ipv4="127.0.0.1",
        latency_ms=0,
        provider_message_id=message_id,
        delivery_status="sent",
    )


def failed_delivery(
    *,
    provider: str,
    method: str,
    url: str,
    payload: dict[str, Any],
    recipient: str,
    error_type: str,
    error_message: str,
    http_status: int | None = None,
    resolved_ipv4: str | None = None,
) -> DeliveryCall:
    return DeliveryCall(
        provider=provider,
        method=method.upper(),
        url=url,
        sanitized_url=sanitize_delivery_url(url),
        ok=False,
        http_status=http_status,
        response_text="",
        response_json=None,
        response_headers={},
        request_headers={"Content-Type": "application/json", "Accept": "application/json"},
        request_payload=dict(payload),
        resolved_ipv4=resolved_ipv4,
        latency_ms=0,
        error_type=error_type,
        error_message=error_message,
        provider_message_id="",
        delivery_status="failed",
    )


def should_use_real_delivery() -> bool:
    return os.getenv("APP_ENV", "development").strip().lower() == "production"
