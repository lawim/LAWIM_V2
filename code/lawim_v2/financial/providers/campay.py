from __future__ import annotations

from base64 import b64decode
from dataclasses import dataclass, field
from hashlib import sha256
import hmac
import json
import threading
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from ...errors import ValidationError
from ..exceptions import PaymentProviderUnavailable
from ...observability import METRICS
from .base import ProviderHealth


_DEFAULT_SANDBOX_BASE_URL = "https://demo.campay.net"
_DEFAULT_PRODUCTION_BASE_URL = "https://www.campay.net"
_WEBHOOK_SIGNATURE_HEADERS = (
    "X-LAWIM-WEBHOOK-SIGNATURE",
    "X-Campay-Signature",
    "X-Signature",
)


def _normalize_text(value: object | None, fallback: str = "") -> str:
    text = str(value or "").strip()
    return text or fallback


def _normalize_status(value: object | None, fallback: str = "UNKNOWN") -> str:
    text = _normalize_text(value, fallback).upper()
    return text or fallback


def _minor_amount(value: object | None) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(round(value))
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _response_payload(raw: bytes) -> dict[str, object]:
    if not raw:
        return {}
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"raw_text": raw.decode("utf-8", errors="replace")}
    return payload if isinstance(payload, dict) else {"data": payload}


def _payload_hash(payload: bytes) -> str:
    return sha256(payload).hexdigest()


@dataclass(slots=True)
class CampayProviderAdapter:
    config: Any
    code: str = "CAMPAY"
    name: str = "Campay"
    _cached_token: str | None = field(default=None, init=False, repr=False)
    _cached_token_expires_at: float = field(default=0.0, init=False, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False)

    def _enabled(self) -> bool:
        return bool(getattr(self.config, "campay_enabled", False))

    def _environment(self) -> str:
        return _normalize_text(getattr(self.config, "campay_environment", "sandbox"), "sandbox").lower()

    def _base_url(self) -> str:
        configured = _normalize_text(getattr(self.config, "campay_base_url", ""))
        if configured:
            return configured.rstrip("/")
        return _DEFAULT_PRODUCTION_BASE_URL if self._environment() == "production" else _DEFAULT_SANDBOX_BASE_URL

    def _timeout(self) -> int:
        try:
            return max(1, int(getattr(self.config, "campay_timeout_seconds", 30)))
        except (TypeError, ValueError):
            return 30

    def _headers(self, *, token: str | None = None, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "LAWIM_V2-CampayAdapter/1.0",
        }
        if token:
            headers["Authorization"] = f"Token {token}"
        if extra:
            headers.update(extra)
        return headers

    def _record_duration(self, started_at: float) -> None:
        duration = max(0.0, time.perf_counter() - started_at)
        with METRICS.lock:
            METRICS.campay_request_duration_seconds += duration

    def _request_json(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, object] | None = None,
        token: str | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, object]:
        started_at = time.perf_counter()
        METRICS.increment("campay_request_total")
        url = f"{self._base_url()}{path if path.startswith('/') else f'/{path}'}"
        body = None if payload is None else json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        request = Request(url, data=body, method=method.upper(), headers=self._headers(token=token, extra=extra_headers))
        try:
            with urlopen(request, timeout=self._timeout()) as response:  # noqa: S310 - external API call
                raw = response.read()
                parsed = _response_payload(raw)
                result = {
                    "ok": True,
                    "status_code": int(getattr(response, "status", 200) or 200),
                    "headers": {key: value for key, value in response.headers.items()},
                    "payload": parsed,
                }
                return result
        except HTTPError as exc:
            raw = exc.read() if hasattr(exc, "read") else b""
            return self.normalize_error(
                exc,
                operation=f"{method.upper()} {path}",
                status_code=int(getattr(exc, "code", 0) or 0),
                payload=_response_payload(raw),
            )
        except URLError as exc:
            return self.normalize_error(exc, operation=f"{method.upper()} {path}")
        except TimeoutError as exc:  # pragma: no cover - defensive
            return self.normalize_error(exc, operation=f"{method.upper()} {path}")
        finally:
            self._record_duration(started_at)

    def _cache_token(self, token: str, *, expires_in: int | None = None) -> None:
        with self._lock:
            self._cached_token = token
            ttl_seconds = 55 * 60 if expires_in is None else max(60, int(expires_in))
            self._cached_token_expires_at = time.time() + ttl_seconds

    def _cached_token_valid(self) -> bool:
        with self._lock:
            return bool(self._cached_token) and time.time() < (self._cached_token_expires_at - 30)

    def _initial_token(self) -> str | None:
        initial = _normalize_text(getattr(self.config, "campay_token", ""))
        return initial or None

    def _load_token(self) -> str:
        if self._cached_token_valid():
            with self._lock:
                assert self._cached_token is not None
                return self._cached_token

        initial = self._initial_token()
        if initial:
            self._cache_token(initial)
            return initial

        username = _normalize_text(getattr(self.config, "campay_app_username", ""))
        password = _normalize_text(getattr(self.config, "campay_app_password", ""))
        if not username or not password:
            raise PaymentProviderUnavailable("Campay credentials are incomplete")

        response = self._request_json("POST", "/api/token/", payload={"username": username, "password": password})
        if not response.get("ok"):
            raise PaymentProviderUnavailable(self.normalize_error_message(response))

        payload = response.get("payload") if isinstance(response.get("payload"), dict) else {}
        token = _normalize_text(payload.get("token") or payload.get("access_token"))
        if not token:
            raise PaymentProviderUnavailable("Campay authentication response did not include a token")
        expires_in = payload.get("expires_in")
        self._cache_token(token, expires_in=int(expires_in) if str(expires_in or "").isdigit() else None)
        METRICS.increment("campay_auth_success_total")
        return token

    def normalize_error(self, error: Exception | dict[str, object] | str, *, operation: str = "", status_code: int | None = None, payload: dict[str, object] | None = None) -> dict[str, object]:
        if isinstance(error, dict):
            message = _normalize_text(error.get("error_message") or error.get("message") or error.get("detail"), "Campay request failed")
            code = _normalize_text(error.get("error_code") or error.get("code"), "campay_error")
        else:
            message = _normalize_text(str(error), "Campay request failed")
            code = "campay_error"
        normalized = {
            "ok": False,
            "provider": self.code,
            "provider_name": self.name,
            "operation": operation,
            "status": "FAILED",
            "status_code": status_code,
            "error_code": code,
            "error_message": message,
            "payload": payload or {},
            "environment": self._environment(),
            "available": False,
        }
        return normalized

    def normalize_error_message(self, response: dict[str, object]) -> str:
        payload = response.get("payload") if isinstance(response.get("payload"), dict) else {}
        return _normalize_text(
            payload.get("detail")
            or payload.get("message")
            or payload.get("error")
            or response.get("error_message")
            or response.get("message"),
            "Campay request failed",
        )

    def authenticate(self) -> dict[str, object]:
        if not self._enabled():
            return self.normalize_error(PaymentProviderUnavailable("Campay is disabled"), operation="authenticate")
        try:
            token = self._load_token()
        except PaymentProviderUnavailable as exc:
            METRICS.increment("campay_auth_failure_total")
            return self.normalize_error(exc, operation="authenticate")
        return {
            "ok": True,
            "provider": self.code,
            "provider_name": self.name,
            "status": "authenticated",
            "environment": self._environment(),
            "available": True,
            "token_cached": True,
            "token_source": "cache" if self._cached_token_valid() else "config_or_remote",
            "token_present": bool(token),
        }

    def create_payment(self, *, payload: dict[str, object]) -> dict[str, object]:
        if not self._enabled():
            return self.normalize_error(PaymentProviderUnavailable("Campay is disabled"), operation="create_payment")
        try:
            token = self._load_token()
        except PaymentProviderUnavailable as exc:
            METRICS.increment("campay_payment_failure_total")
            return self.normalize_error(exc, operation="create_payment")

        amount_minor = _minor_amount(payload.get("amount_minor"))
        if amount_minor is None:
            amount_minor = _minor_amount(payload.get("amount")) or 0
        currency = _normalize_text(payload.get("currency"), _normalize_text(getattr(self.config, "campay_default_currency", "XAF"), "XAF")).upper()
        external_reference = _normalize_text(
            payload.get("external_reference")
            or payload.get("reference")
            or payload.get("merchant_reference")
            or payload.get("business_reference"),
        )
        request_payload = {
            "amount": amount_minor,
            "currency": currency,
            "from": _normalize_text(payload.get("phone_number_e164") or payload.get("from") or payload.get("phone_number")),
            "description": _normalize_text(payload.get("description")),
            "external_reference": external_reference,
            "callback_url": _normalize_text(payload.get("callback_url") or getattr(self.config, "campay_webhook_url", "")),
            "redirect_url": _normalize_text(payload.get("redirect_url") or getattr(self.config, "campay_redirect_url", "")),
            "metadata": payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {},
        }
        response = self._request_json("POST", "/api/collect/", payload=request_payload, token=token)
        if not response.get("ok"):
            METRICS.increment("campay_payment_failure_total")
            return {
                **response,
                "provider": self.code,
                "provider_name": self.name,
                "request": request_payload,
            }

        raw_payload = response.get("payload") if isinstance(response.get("payload"), dict) else {}
        provider_reference = _normalize_text(
            raw_payload.get("reference")
            or raw_payload.get("transaction_reference")
            or raw_payload.get("external_reference")
            or external_reference
            or request_payload["external_reference"],
        )
        provider_status = _normalize_status(raw_payload.get("status") or raw_payload.get("state") or "PENDING", "PENDING")
        METRICS.increment("campay_payment_initiated_total")
        if provider_status == "SUCCESSFUL":
            METRICS.increment("campay_payment_success_total")
        elif provider_status in {"FAILED", "CANCELLED", "EXPIRED"}:
            METRICS.increment("campay_payment_failure_total")
        return {
            "ok": True,
            "provider": self.code,
            "provider_name": self.name,
            "status": provider_status if provider_status in {"PENDING", "PROCESSING", "REQUIRES_ACTION", "SUCCESSFUL", "FAILED", "CANCELLED", "EXPIRED"} else "PENDING",
            "provider_reference": provider_reference,
            "request": request_payload,
            "response": raw_payload,
            "available": True,
        }

    def get_payment_status(self, *, provider_reference: str) -> dict[str, object]:
        if not self._enabled():
            return self.normalize_error(PaymentProviderUnavailable("Campay is disabled"), operation="get_payment_status")
        try:
            token = self._load_token()
        except PaymentProviderUnavailable as exc:
            METRICS.increment("campay_status_conflict_total")
            return self.normalize_error(exc, operation="get_payment_status")

        response = self._request_json("GET", f"/api/transaction/{provider_reference}/", token=token)
        METRICS.increment("campay_status_check_total")
        if not response.get("ok"):
            METRICS.increment("campay_status_conflict_total")
            return {
                **response,
                "provider": self.code,
                "provider_name": self.name,
                "provider_reference": provider_reference,
            }
        payload = response.get("payload") if isinstance(response.get("payload"), dict) else {}
        status = _normalize_status(payload.get("status") or payload.get("state") or payload.get("result"), "UNKNOWN")
        amount_minor = _minor_amount(payload.get("amount_minor") or payload.get("amount"))
        currency = _normalize_text(payload.get("currency") or getattr(self.config, "campay_default_currency", "XAF"), "XAF").upper()
        if status == "SUCCESSFUL":
            METRICS.increment("campay_payment_success_total")
        elif status in {"FAILED", "CANCELLED", "EXPIRED"}:
            METRICS.increment("campay_payment_failure_total")
        return {
            "ok": True,
            "provider": self.code,
            "provider_name": self.name,
            "provider_reference": _normalize_text(provider_reference),
            "status": status,
            "amount_minor": amount_minor,
            "currency": currency,
            "raw": payload,
            "available": True,
        }

    def cancel_payment(self, *, provider_reference: str) -> dict[str, object]:
        return {
            "ok": False,
            "provider": self.code,
            "provider_name": self.name,
            "provider_reference": _normalize_text(provider_reference),
            "status": "UNSUPPORTED",
            "supported": False,
            "error_code": "unsupported_operation",
            "error_message": "Campay cancel_payment is not supported by the documented API",
        }

    def refund_payment(self, *, provider_reference: str, amount_minor: int) -> dict[str, object]:
        return {
            "ok": False,
            "provider": self.code,
            "provider_name": self.name,
            "provider_reference": _normalize_text(provider_reference),
            "amount_minor": max(0, int(amount_minor)),
            "status": "UNSUPPORTED",
            "supported": False,
            "error_code": "unsupported_operation",
            "error_message": "Campay refund_payment is handled manually in LAWIM when the provider API does not expose refunds",
        }

    def validate_webhook(self, *, headers: dict[str, str], payload: bytes) -> bool:
        if not self._enabled():
            return False
        secret = _normalize_text(getattr(self.config, "campay_webhook_secret", ""))
        if not secret or not payload:
            return False
        signature = ""
        for header_name in _WEBHOOK_SIGNATURE_HEADERS:
            for key, value in headers.items():
                if key.lower() == header_name.lower():
                    signature = _normalize_text(value)
                    break
            if signature:
                break
        if not signature:
            return False
        expected_hex = hmac.new(secret.encode("utf-8"), payload, sha256).hexdigest()
        normalized = signature.lower().strip()
        if normalized.startswith("sha256="):
            normalized = normalized.split("=", 1)[1].strip()
        if normalized.startswith("hmac-sha256="):
            normalized = normalized.split("=", 1)[1].strip()
        if normalized == expected_hex:
            return True
        try:
            decoded = b64decode(signature, validate=True).hex()
        except Exception:  # pragma: no cover - tolerant fallback
            decoded = ""
        return decoded == expected_hex

    def parse_webhook(self, *, payload: bytes) -> dict[str, object]:
        payload_hash = _payload_hash(payload)
        try:
            parsed = json.loads(payload.decode("utf-8")) if payload else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {
                "ok": False,
                "provider": self.code,
                "provider_name": self.name,
                "error_code": "invalid_webhook_payload",
                "error_message": "Webhook payload must be valid JSON",
                "payload_hash": payload_hash,
                "raw": {},
            }
        if not isinstance(parsed, dict):
            parsed = {"data": parsed}
        event_id = _normalize_text(parsed.get("event_id") or parsed.get("id") or parsed.get("webhook_id") or payload_hash)
        provider_reference = _normalize_text(
            parsed.get("reference")
            or parsed.get("transaction_reference")
            or parsed.get("external_reference")
            or parsed.get("provider_reference")
        )
        amount_minor = _minor_amount(parsed.get("amount_minor"))
        if amount_minor is None:
            amount_minor = _minor_amount(parsed.get("amount"))
        currency = _normalize_text(parsed.get("currency") or getattr(self.config, "campay_default_currency", "XAF"), "XAF").upper()
        status = _normalize_status(parsed.get("status") or parsed.get("state") or parsed.get("result") or parsed.get("event_type"), "UNKNOWN")
        event_type = _normalize_text(parsed.get("event_type") or parsed.get("type") or status.lower(), "webhook")
        return {
            "ok": True,
            "provider": self.code,
            "provider_name": self.name,
            "event_type": event_type,
            "provider_event_id": event_id,
            "provider_reference": provider_reference,
            "status": status,
            "amount_minor": amount_minor,
            "currency": currency,
            "idempotency_key": _normalize_text(parsed.get("idempotency_key") or parsed.get("key") or provider_reference or event_id),
            "correlation_id": _normalize_text(parsed.get("correlation_id") or parsed.get("correlation") or parsed.get("request_id")),
            "raw": parsed,
            "payload_hash": payload_hash,
        }

    def verify_transaction(self, *, provider_reference: str) -> dict[str, object]:
        return self.get_payment_status(provider_reference=provider_reference)

    def health_check(self) -> ProviderHealth:
        details = {
            "has_base_url": bool(_normalize_text(getattr(self.config, "campay_base_url", ""))),
            "has_username": bool(_normalize_text(getattr(self.config, "campay_app_username", ""))),
            "has_password": bool(_normalize_text(getattr(self.config, "campay_app_password", ""))),
            "has_token": bool(_normalize_text(getattr(self.config, "campay_token", ""))),
            "webhook_configured": bool(_normalize_text(getattr(self.config, "campay_webhook_url", ""))),
            "supports_collection": True,
            "supports_status_query": True,
            "supports_webhook": True,
            "supports_refund": False,
            "supports_payout": True,
            "environment": self._environment(),
            "base_url": self._base_url(),
        }
        if not self._enabled():
            with METRICS.lock:
                METRICS.campay_provider_health = 0.0
            return ProviderHealth(
                code=self.code,
                name=self.name,
                status="disabled",
                environment=self._environment(),
                available=False,
                details=details,
            )

        try:
            token = self._load_token()
        except PaymentProviderUnavailable as exc:
            with METRICS.lock:
                METRICS.campay_provider_health = 0.0
            return ProviderHealth(
                code=self.code,
                name=self.name,
                status="degraded",
                environment=self._environment(),
                available=False,
                details={**details, "error": str(exc)},
            )

        response = self._request_json("GET", "/api/balance/", token=token)
        available = bool(response.get("ok"))
        status = "active" if available else "degraded"
        with METRICS.lock:
            METRICS.campay_provider_health = 100.0 if available else 0.0
        if available:
            details["balance_available"] = True
            payload = response.get("payload") if isinstance(response.get("payload"), dict) else {}
            if payload:
                details["balance"] = payload
        else:
            details["balance_available"] = False
            details["error"] = self.normalize_error_message(response)
        return ProviderHealth(
            code=self.code,
            name=self.name,
            status=status,
            environment=self._environment(),
            available=available,
            details=details,
        )
