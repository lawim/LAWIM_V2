#!/usr/bin/env bash
# Live validation for AI providers.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"

if [[ -n "${LAWIM_AI_SECRETS_FILE:-}" && -f "${LAWIM_AI_SECRETS_FILE}" ]]; then
  # shellcheck disable=SC1090
  set -a
  source "${LAWIM_AI_SECRETS_FILE}"
  set +a
fi

python3 - <<'PY'
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

TIMEOUT = float(os.environ.get("AI_REQUEST_TIMEOUT_SECONDS", "30"))
PROMPT = "Réponds uniquement par ok."
MESSAGE_BODY = {
    "messages": [
        {"role": "system", "content": "You are a concise assistant for LAWIM."},
        {"role": "user", "content": PROMPT},
    ],
    "temperature": 0,
}


def _json_request(url: str, headers: dict[str, str], payload: dict[str, object] | None = None) -> tuple[int, dict[str, object], float]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
      status = response.status
      text = response.read().decode("utf-8", "replace")
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    parsed = json.loads(text) if text else {}
    return status, parsed if isinstance(parsed, dict) else {"raw": parsed}, latency_ms


def _classify_error(status: int, body: str) -> str:
    body_lower = body.lower()
    if status in {401, 403}:
        return "authentication_error"
    if status == 404 or "model" in body_lower and ("not found" in body_lower or "unknown" in body_lower or "unsupported" in body_lower):
        return "model_unavailable"
    if status == 429:
        return "rate_limited"
    if status >= 500:
        return "upstream_error"
    if "timeout" in body_lower:
        return "timeout"
    return "request_failed"


def _result(provider: str, credential_alias: str, model: str, status: str, latency_ms: float, http_status: int, error_type: str | None) -> dict[str, object]:
    return {
        "provider": provider,
        "credential_alias": credential_alias,
        "model": model,
        "status": status,
        "latency_ms": int(round(latency_ms)),
        "http_status": http_status,
        "error_type": error_type,
    }


def run_deepseek() -> dict[str, object]:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/")
    if not api_key:
        return _result("deepseek", "DEEPSEEK_API_KEY", model, "missing_secret", 0, 0, "missing_secret")
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = dict(MESSAGE_BODY)
    payload.update({"model": model, "max_tokens": 64})
    try:
        http_status, response, latency_ms = _json_request(url, headers, payload)
        content = ""
        choices = response.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message") or {}
                if isinstance(message, dict):
                    content = str(message.get("content") or "").strip()
        if http_status == 200 and content:
            return _result("deepseek", "DEEPSEEK_API_KEY", model, "ok", latency_ms, http_status, None)
        return _result("deepseek", "DEEPSEEK_API_KEY", model, "invalid_response" if http_status == 200 else "failed", latency_ms, http_status, _classify_error(http_status, json.dumps(response, ensure_ascii=False)))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return _result("deepseek", "DEEPSEEK_API_KEY", model, _classify_error(exc.code, body), 0, exc.code, _classify_error(exc.code, body))
    except Exception as exc:  # noqa: BLE001
        return _result("deepseek", "DEEPSEEK_API_KEY", model, "network_error", 0, 0, type(exc).__name__)


def run_openai() -> dict[str, object]:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    if not api_key:
        return _result("openai", "OPENAI_API_KEY", model, "missing_secret", 0, 0, "missing_secret")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = dict(MESSAGE_BODY)
    payload.update({"model": model, "max_tokens": 8})
    try:
        http_status, response, latency_ms = _json_request(url, headers, payload)
        content = ""
        choices = response.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                message = first.get("message") or {}
                if isinstance(message, dict):
                    content = str(message.get("content") or "").strip()
        if http_status == 200 and content:
            return _result("openai", "OPENAI_API_KEY", model, "ok", latency_ms, http_status, None)
        return _result("openai", "OPENAI_API_KEY", model, "invalid_response" if http_status == 200 else "failed", latency_ms, http_status, _classify_error(http_status, json.dumps(response, ensure_ascii=False)))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return _result("openai", "OPENAI_API_KEY", model, _classify_error(exc.code, body), 0, exc.code, _classify_error(exc.code, body))
    except Exception as exc:  # noqa: BLE001
        return _result("openai", "OPENAI_API_KEY", model, "network_error", 0, 0, type(exc).__name__)


def run_gemini(provider_name: str, alias: str, api_key_env: str, model_env: str) -> dict[str, object]:
    api_key = os.getenv(api_key_env)
    model = os.getenv(model_env, "gemini-3.5-flash" if alias == "GEMINI_PRIMARY_API_KEY" else "gemini-2.5-flash")
    if not api_key:
        return _result(provider_name, alias, model, "missing_secret", 0, 0, "missing_secret")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": PROMPT}],
            }
        ],
        "generationConfig": {
            "temperature": 0,
            "maxOutputTokens": 32,
        },
    }
    try:
        http_status, response, latency_ms = _json_request(url, headers, payload)
        content = ""
        candidates = response.get("candidates")
        if isinstance(candidates, list) and candidates:
            first = candidates[0]
            if isinstance(first, dict):
                content_data = first.get("content") or {}
                if isinstance(content_data, dict):
                    parts = content_data.get("parts") or []
                    if isinstance(parts, list) and parts:
                        part = parts[0]
                        if isinstance(part, dict):
                            content = str(part.get("text") or "").strip()
        if http_status == 200 and content:
            return _result(provider_name, alias, model, "ok", latency_ms, http_status, None)
        return _result(provider_name, alias, model, "invalid_response" if http_status == 200 else "failed", latency_ms, http_status, _classify_error(http_status, json.dumps(response, ensure_ascii=False)))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return _result(provider_name, alias, model, _classify_error(exc.code, body), 0, exc.code, _classify_error(exc.code, body))
    except Exception as exc:  # noqa: BLE001
        return _result(provider_name, alias, model, "network_error", 0, 0, type(exc).__name__)


results = [
    run_deepseek(),
    run_openai(),
    run_gemini("gemini_primary", "GEMINI_PRIMARY_API_KEY", "GEMINI_PRIMARY_API_KEY", "GEMINI_PRIMARY_MODEL"),
    run_gemini("gemini_secondary", "GEMINI_SECONDARY_API_KEY", "GEMINI_SECONDARY_API_KEY", "GEMINI_SECONDARY_MODEL"),
]
print(json.dumps(results, ensure_ascii=False, indent=2))
PY
