from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import json
import uuid

from ..repository_introspection import table_exists
from .schema_ddl import AI_TABLE_NAMES, POSTGRESQL_AI_STATEMENTS, SQLITE_AI_TABLES_SCRIPT


def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _parse_json(value: str | None) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


class AIRepositoryMixin:
    def ai_tables_present(self) -> bool:
        return table_exists(self, "ai_providers")

    def initialize_ai_catalog(self) -> None:
        driver = str(getattr(self, "driver", "sqlite")).strip().lower()
        with self._transaction() as conn:
            if driver in {"postgresql", "postgres"}:
                for statement in POSTGRESQL_AI_STATEMENTS:
                    conn.execute(statement)
            else:
                conn.executescript(SQLITE_AI_TABLES_SCRIPT)
            for table in ("ai_provider_health", "ai_circuit_breakers"):
                columns = self._table_columns(conn, table)
                if "updated_at" not in columns:
                    if driver in {"postgresql", "postgres"}:
                        conn.execute(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS updated_at TEXT NOT NULL DEFAULT ''")
                    else:
                        conn.execute(f"ALTER TABLE {table} ADD COLUMN updated_at TEXT NOT NULL DEFAULT ''")

    def seed_ai_catalog(self) -> None:
        now = _utcnow()
        providers = (
            {
                "provider_key": "deepseek",
                "provider_name": "DeepSeek",
                "credential_alias": "DEEPSEEK_API_KEY",
                "secret_reference": "DEEPSEEK_API_KEY",
                "enabled": 1,
                "priority": 1,
                "model": "deepseek-v4-flash",
                "base_url": "https://api.deepseek.com",
                "provider_role": "primary",
                "status": "active",
                "notes": "Primary provider for simple requests.",
            },
            {
                "provider_key": "openai",
                "provider_name": "OpenAI",
                "credential_alias": "OPENAI_API_KEY",
                "secret_reference": "OPENAI_API_KEY",
                "enabled": 1,
                "priority": 2,
                "model": "gpt-4o-mini",
                "base_url": "https://api.openai.com/v1",
                "provider_role": "complex",
                "status": "active",
                "notes": "Complexity fallback and reasoning-heavy requests.",
            },
            {
                "provider_key": "gemini_primary",
                "provider_name": "Gemini Primary",
                "credential_alias": "GEMINI_PRIMARY_API_KEY",
                "secret_reference": "GEMINI_PRIMARY_API_KEY",
                "enabled": 1,
                "priority": 3,
                "model": "gemini-3.5-flash",
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "provider_role": "fallback",
                "status": "active",
                "notes": "Primary Gemini fallback.",
            },
            {
                "provider_key": "gemini_secondary",
                "provider_name": "Gemini Secondary",
                "credential_alias": "GEMINI_SECONDARY_API_KEY",
                "secret_reference": "GEMINI_SECONDARY_API_KEY",
                "enabled": 1,
                "priority": 4,
                "model": "gemini-2.5-flash",
                "base_url": "https://generativelanguage.googleapis.com/v1beta",
                "provider_role": "fallback",
                "status": "active",
                "notes": "Secondary Gemini fallback.",
            },
            {
                "provider_key": "internal",
                "provider_name": "LAWIM Internal Fallback",
                "credential_alias": "INTERNAL_FALLBACK",
                "secret_reference": "INTERNAL_FALLBACK",
                "enabled": 1,
                "priority": 5,
                "model": "internal-fallback",
                "base_url": "",
                "provider_role": "internal",
                "status": "active",
                "notes": "Local deterministic fallback provider.",
            },
        )
        fallback_entries = (
            {
                "fallback_key": "greeting-fr",
                "intent": "greeting",
                "question": "bonjour salut hello",
                "variants_json": _json(["bonjour", "salut", "hello", "bonsoir"]),
                "keywords_json": _json(["bonjour", "salut", "accueil"]),
                "category": "presentation",
                "language": "fr",
                "channel": "all",
                "response_text": "Bonjour et bienvenue sur LAWIM. Comment puis-je vous aider ?",
                "confidence": 0.98,
                "validated_at": now,
                "validated_by": "system",
                "version_number": 1,
                "status": "published",
                "expires_at": None,
                "usage_count": 0,
                "satisfaction_rate": 1.0,
                "risk_level": "low",
                "source_type": "manual",
            },
            {
                "fallback_key": "contact-fr",
                "intent": "contact",
                "question": "contact telephone whatsapp telegram",
                "variants_json": _json(["contact", "numero", "whatsapp", "telegram", "telephone"]),
                "keywords_json": _json(["contact", "whatsapp", "telegram", "support"]),
                "category": "contact",
                "language": "fr",
                "channel": "all",
                "response_text": "Vous pouvez contacter LAWIM via WhatsApp ou Telegram. Merci de préciser votre demande pour une prise en charge rapide.",
                "confidence": 0.95,
                "validated_at": now,
                "validated_by": "system",
                "version_number": 1,
                "status": "published",
                "expires_at": None,
                "usage_count": 0,
                "satisfaction_rate": 1.0,
                "risk_level": "low",
                "source_type": "manual",
            },
            {
                "fallback_key": "hours-fr",
                "intent": "hours",
                "question": "horaires ouverture fermeture",
                "variants_json": _json(["horaires", "ouvert", "ouverture", "fermeture"]),
                "keywords_json": _json(["horaires", "ouverture", "fermeture"]),
                "category": "services",
                "language": "fr",
                "channel": "all",
                "response_text": "Les horaires d'assistance peuvent varier selon l'équipe de service. Merci de préciser votre besoin pour être orienté correctement.",
                "confidence": 0.9,
                "validated_at": now,
                "validated_by": "system",
                "version_number": 1,
                "status": "published",
                "expires_at": None,
                "usage_count": 0,
                "satisfaction_rate": 1.0,
                "risk_level": "low",
                "source_type": "manual",
            },
            {
                "fallback_key": "fallback-unavailable-fr",
                "intent": "fallback_unavailable",
                "question": "assistant indisponible",
                "variants_json": _json(["indisponible", "ne repond pas", "fallback"]),
                "keywords_json": _json(["fallback", "indisponible", "assistant"]),
                "category": "support",
                "language": "fr",
                "channel": "all",
                "response_text": "Bonjour et bienvenue sur LAWIM. Votre message a bien été reçu. Merci de préciser brièvement l'objet de votre demande.",
                "confidence": 0.85,
                "validated_at": now,
                "validated_by": "system",
                "version_number": 1,
                "status": "published",
                "expires_at": None,
                "usage_count": 0,
                "satisfaction_rate": 1.0,
                "risk_level": "low",
                "source_type": "manual",
            },
        )
        if self.scalar("SELECT COUNT(*) FROM ai_providers") == 0:
            for provider in providers:
                self.upsert_ai_provider(**provider, last_validated_at=now)
                self.upsert_ai_provider_credentials_metadata(**provider, last_validated_at=now)
                self.upsert_ai_circuit_breaker(
                    provider_key=str(provider["provider_key"]),
                    credential_alias=str(provider["credential_alias"]),
                    state="CLOSED",
                    failure_count=0,
                    success_count=0,
                    half_open_requests=0,
                    opened_at=None,
                    closed_at=None,
                    last_failure_at=None,
                    last_success_at=None,
                    last_checked_at=now,
                    metadata_json={},
                )
        if self.scalar("SELECT COUNT(*) FROM ai_fallback_entries") == 0:
            for entry in fallback_entries:
                self.upsert_ai_fallback_entry(**entry, created_at=now, updated_at=now)
        if self.scalar("SELECT COUNT(*) FROM ai_knowledge_versions") == 0:
            self.create_ai_knowledge_version(
                version_number=1,
                status="published",
                summary="Initial LAWIM AI fallback knowledge base.",
            )

    def _upsert_ai_row(self, table: str, key_column: str, key_value: object, values: dict[str, object]) -> dict[str, object]:
        now = _utcnow()
        fields = dict(values)
        fields.setdefault("updated_at", now)
        with self._transaction() as conn:
            table_columns = self._table_columns(conn, table)
            filtered = {column: value for column, value in fields.items() if column in table_columns}
            if key_column not in filtered:
                filtered[key_column] = key_value
            existing = conn.execute(f"SELECT id FROM {table} WHERE {key_column} = ?", (key_value,)).fetchone()
            columns = list(filtered.keys())
            params = tuple(filtered[column] for column in columns)
            if existing is None:
                conn.execute(
                    f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
                    params,
                )
            else:
                update_columns = [column for column in columns if column != key_column]
                assignments = ", ".join(f"{column} = ?" for column in update_columns)
                update_params = tuple(filtered[column] for column in update_columns)
                if assignments:
                    conn.execute(
                        f"UPDATE {table} SET {assignments} WHERE {key_column} = ?",
                        (*update_params, key_value),
                    )
        row = self.one(f"SELECT * FROM {table} WHERE {key_column} = ?", (key_value,))
        assert row is not None
        return dict(row)

    def upsert_ai_provider(self, **values: object) -> dict[str, object]:
        provider_key = str(values.get("provider_key") or "").strip()
        if not provider_key:
            raise ValueError("provider_key is required")
        payload = {
            "provider_key": provider_key,
            "provider_name": str(values.get("provider_name") or provider_key),
            "credential_alias": str(values.get("credential_alias") or provider_key.upper()),
            "secret_reference": str(values.get("secret_reference") or provider_key.upper()),
            "enabled": int(bool(values.get("enabled", False))),
            "priority": int(values.get("priority") or 0),
            "model": str(values.get("model") or ""),
            "base_url": str(values.get("base_url") or ""),
            "provider_role": str(values.get("provider_role") or "primary"),
            "status": str(values.get("status") or "inactive"),
            "notes": str(values.get("notes") or ""),
            "last_validated_at": values.get("last_validated_at"),
            "last_success_at": values.get("last_success_at"),
            "last_failure_at": values.get("last_failure_at"),
            "consecutive_failures": int(values.get("consecutive_failures") or 0),
            "created_at": values.get("created_at") or _utcnow(),
        }
        return self._upsert_ai_row("ai_providers", "provider_key", provider_key, payload)

    def upsert_ai_provider_credentials_metadata(self, **values: object) -> dict[str, object]:
        provider_key = str(values.get("provider_key") or "").strip()
        if not provider_key:
            raise ValueError("provider_key is required")
        payload = {
            "provider_key": provider_key,
            "credential_alias": str(values.get("credential_alias") or provider_key.upper()),
            "secret_reference": str(values.get("secret_reference") or provider_key.upper()),
            "enabled": int(bool(values.get("enabled", False))),
            "priority": int(values.get("priority") or 0),
            "model": str(values.get("model") or ""),
            "base_url": str(values.get("base_url") or ""),
            "last_validated_at": values.get("last_validated_at"),
            "last_success_at": values.get("last_success_at"),
            "last_failure_at": values.get("last_failure_at"),
            "status": str(values.get("status") or "inactive"),
            "created_at": values.get("created_at") or _utcnow(),
        }
        return self._upsert_ai_row("ai_provider_credentials_metadata", "provider_key", provider_key, payload)

    def list_ai_providers(self, *, enabled: bool | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM ai_providers WHERE 1=1"
        params: list[object] = []
        if enabled is not None:
            query += " AND enabled = ?"
            params.append(1 if enabled else 0)
        query += " ORDER BY priority ASC, id ASC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(query, tuple(params))]

    def get_ai_provider(self, provider_key: str) -> dict[str, object] | None:
        row = self.one("SELECT * FROM ai_providers WHERE provider_key = ?", (provider_key,))
        return dict(row) if row is not None else None

    def upsert_ai_provider_health(self, **values: object) -> dict[str, object]:
        provider_key = str(values.get("provider_key") or "").strip()
        if not provider_key:
            raise ValueError("provider_key is required")
        payload = {
            "provider_key": provider_key,
            "credential_alias": str(values.get("credential_alias") or provider_key.upper()),
            "model": str(values.get("model") or ""),
            "state": str(values.get("state") or "UNKNOWN"),
            "available": int(bool(values.get("available", False))),
            "checked_at": values.get("checked_at") or _utcnow(),
            "latency_ms": int(values.get("latency_ms") or 0),
            "error_type": values.get("error_type"),
            "error_code": values.get("error_code"),
            "credit_remaining": values.get("credit_remaining"),
            "credit_limit": values.get("credit_limit"),
            "quota_status": values.get("quota_status"),
            "last_success_at": values.get("last_success_at"),
            "last_failure_at": values.get("last_failure_at"),
            "consecutive_failures": int(values.get("consecutive_failures") or 0),
            "details_json": _json(values.get("details_json") or values.get("details") or {}),
        }
        return self._upsert_ai_row("ai_provider_health", "provider_key", provider_key, payload)

    def list_ai_provider_health(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_provider_health ORDER BY checked_at DESC, id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def get_ai_circuit_breaker(self, provider_key: str) -> dict[str, object] | None:
        row = self.one("SELECT * FROM ai_circuit_breakers WHERE provider_key = ?", (provider_key,))
        return dict(row) if row is not None else None

    def upsert_ai_circuit_breaker(self, **values: object) -> dict[str, object]:
        provider_key = str(values.get("provider_key") or "").strip()
        if not provider_key:
            raise ValueError("provider_key is required")
        payload = {
            "provider_key": provider_key,
            "credential_alias": str(values.get("credential_alias") or provider_key.upper()),
            "state": str(values.get("state") or "CLOSED"),
            "failure_count": int(values.get("failure_count") or 0),
            "success_count": int(values.get("success_count") or 0),
            "window_started_at": values.get("window_started_at"),
            "opened_at": values.get("opened_at"),
            "closed_at": values.get("closed_at"),
            "half_open_requests": int(values.get("half_open_requests") or 0),
            "last_failure_at": values.get("last_failure_at"),
            "last_success_at": values.get("last_success_at"),
            "last_checked_at": values.get("last_checked_at") or _utcnow(),
            "metadata_json": _json(values.get("metadata_json") or values.get("metadata") or {}),
        }
        return self._upsert_ai_row("ai_circuit_breakers", "provider_key", provider_key, payload)

    def list_ai_circuit_breakers(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_circuit_breakers ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def create_ai_request(self, **values: object) -> dict[str, object]:
        request_key = str(values.get("request_key") or f"req-{uuid.uuid4().hex[:12]}")
        payload = {
            "request_key": request_key,
            "conversation_key": str(values.get("conversation_key") or ""),
            "channel": str(values.get("channel") or "whatsapp"),
            "external_chat_id": str(values.get("external_chat_id") or ""),
            "external_user_id": str(values.get("external_user_id") or ""),
            "message_id": str(values.get("message_id") or ""),
            "language": str(values.get("language") or "fr"),
            "complexity": str(values.get("complexity") or "simple"),
            "prompt_text": str(values.get("prompt_text") or ""),
            "sanitized_text": str(values.get("sanitized_text") or ""),
            "context_json": _json(values.get("context_json") or values.get("context") or []),
            "metadata_json": _json(values.get("metadata_json") or values.get("metadata") or {}),
            "provider_chain_json": _json(values.get("provider_chain_json") or values.get("provider_chain") or []),
            "status": str(values.get("status") or "pending"),
            "created_at": values.get("created_at") or _utcnow(),
            "updated_at": values.get("updated_at") or _utcnow(),
        }
        return self._upsert_ai_row("ai_requests", "request_key", request_key, payload)

    def list_ai_requests(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_requests ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def create_ai_response(self, **values: object) -> dict[str, object]:
        request_key = str(values.get("request_key") or "")
        payload = {
            "request_key": request_key,
            "provider_key": str(values.get("provider_key") or ""),
            "model": str(values.get("model") or ""),
            "success": int(bool(values.get("success", False))),
            "content": str(values.get("content") or ""),
            "latency_ms": int(values.get("latency_ms") or 0),
            "input_tokens": int(values.get("input_tokens") or 0),
            "output_tokens": int(values.get("output_tokens") or 0),
            "estimated_cost": float(values.get("estimated_cost") or 0.0),
            "finish_reason": values.get("finish_reason"),
            "error_type": values.get("error_type"),
            "error_code": values.get("error_code"),
            "retryable": int(bool(values.get("retryable", False))),
            "fallback_required": int(bool(values.get("fallback_required", False))),
            "provider_request_id": values.get("provider_request_id"),
            "valid": int(bool(values.get("valid", False))),
            "complete": int(bool(values.get("complete", False))),
            "relevant": int(bool(values.get("relevant", False))),
            "safe": int(bool(values.get("safe", False))),
            "well_formed": int(bool(values.get("well_formed", False))),
            "confidence_score": float(values.get("confidence_score") or 0.0),
            "metadata_json": _json(values.get("metadata_json") or values.get("metadata") or {}),
            "created_at": values.get("created_at") or _utcnow(),
        }
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_responses (
                    request_key, provider_key, model, success, content, latency_ms, input_tokens, output_tokens,
                    estimated_cost, finish_reason, error_type, error_code, retryable, fallback_required,
                    provider_request_id, valid, complete, relevant, safe, well_formed, confidence_score,
                    metadata_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(payload[column] for column in (
                    "request_key",
                    "provider_key",
                    "model",
                    "success",
                    "content",
                    "latency_ms",
                    "input_tokens",
                    "output_tokens",
                    "estimated_cost",
                    "finish_reason",
                    "error_type",
                    "error_code",
                    "retryable",
                    "fallback_required",
                    "provider_request_id",
                    "valid",
                    "complete",
                    "relevant",
                    "safe",
                    "well_formed",
                    "confidence_score",
                    "metadata_json",
                    "created_at",
                )),
            )
        row = self.one("SELECT * FROM ai_responses WHERE request_key = ? ORDER BY id DESC LIMIT 1", (request_key,))
        assert row is not None
        return dict(row)

    def list_ai_responses(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_responses ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def upsert_ai_usage(self, *, period: str, provider_key: str, values: dict[str, object]) -> dict[str, object]:
        table = "ai_usage_daily" if period == "daily" else "ai_usage_monthly"
        period_column = "period_day" if period == "daily" else "period_month"
        key_value = str(values.get(period_column) or "")
        if not key_value:
            raise ValueError(f"{period_column} is required")
        payload = {
            "provider_key": provider_key,
            period_column: key_value,
            "requests_total": int(values.get("requests_total") or 0),
            "requests_success": int(values.get("requests_success") or 0),
            "requests_failed": int(values.get("requests_failed") or 0),
            "fallbacks_triggered": int(values.get("fallbacks_triggered") or 0),
            "input_tokens": int(values.get("input_tokens") or 0),
            "output_tokens": int(values.get("output_tokens") or 0),
            "estimated_cost": float(values.get("estimated_cost") or 0.0),
            "rate_limit_errors": int(values.get("rate_limit_errors") or 0),
            "authentication_errors": int(values.get("authentication_errors") or 0),
            "timeouts": int(values.get("timeouts") or 0),
            "empty_responses": int(values.get("empty_responses") or 0),
            "invalid_responses": int(values.get("invalid_responses") or 0),
            "circuit_open_count": int(values.get("circuit_open_count") or 0),
            "last_success_at": values.get("last_success_at"),
            "last_failure_at": values.get("last_failure_at"),
            "created_at": values.get("created_at") or _utcnow(),
            "updated_at": values.get("updated_at") or _utcnow(),
        }
        with self._transaction() as conn:
            table_columns = self._table_columns(conn, table)
            filtered = {column: value for column, value in payload.items() if column in table_columns}
            existing = conn.execute(
                f"SELECT id FROM {table} WHERE provider_key = ? AND {period_column} = ?",
                (provider_key, key_value),
            ).fetchone()
            columns = list(filtered.keys())
            params = tuple(filtered[column] for column in columns)
            if existing is None:
                conn.execute(
                    f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join('?' for _ in columns)})",
                    params,
                )
            else:
                update_columns = [column for column in columns if column not in {period_column, "provider_key"}]
                assignments = ", ".join(f"{column} = ?" for column in update_columns)
                update_params = tuple(filtered[column] for column in update_columns)
                if assignments:
                    conn.execute(
                        f"UPDATE {table} SET {assignments} WHERE provider_key = ? AND {period_column} = ?",
                        (*update_params, provider_key, key_value),
                    )
        row = self.one(f"SELECT * FROM {table} WHERE provider_key = ? AND {period_column} = ?", (provider_key, key_value))
        assert row is not None
        return dict(row)

    def list_ai_usage(self, *, period: str = "daily", limit: int = 50) -> list[dict[str, object]]:
        table = "ai_usage_daily" if period == "daily" else "ai_usage_monthly"
        rows = self.all(f"SELECT * FROM {table} ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def record_ai_alert(self, **values: object) -> dict[str, object]:
        alert_key = str(values.get("alert_key") or f"alert-{uuid.uuid4().hex[:12]}")
        payload = {
            "alert_key": alert_key,
            "provider_key": str(values.get("provider_key") or ""),
            "severity": str(values.get("severity") or "info"),
            "alert_type": str(values.get("alert_type") or "general"),
            "message": str(values.get("message") or ""),
            "payload_json": _json(values.get("payload_json") or values.get("payload") or {}),
            "status": str(values.get("status") or "open"),
            "created_at": values.get("created_at") or _utcnow(),
            "acknowledged_at": values.get("acknowledged_at"),
        }
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_alerts (
                    alert_key, provider_key, severity, alert_type, message, payload_json, status,
                    created_at, acknowledged_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(payload[column] for column in (
                    "alert_key",
                    "provider_key",
                    "severity",
                    "alert_type",
                    "message",
                    "payload_json",
                    "status",
                    "created_at",
                    "acknowledged_at",
                )),
            )
        row = self.one("SELECT * FROM ai_alerts WHERE alert_key = ?", (alert_key,))
        assert row is not None
        return dict(row)

    def list_ai_alerts(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM ai_alerts WHERE 1=1"
        params: list[object] = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(query, tuple(params))]

    def record_ai_routing_decision(self, **values: object) -> dict[str, object]:
        routing_key = str(values.get("routing_key") or f"route-{uuid.uuid4().hex[:12]}")
        payload = {
            "routing_key": routing_key,
            "request_key": str(values.get("request_key") or ""),
            "conversation_key": str(values.get("conversation_key") or ""),
            "complexity": str(values.get("complexity") or "simple"),
            "selected_provider": str(values.get("selected_provider") or ""),
            "fallback_used": int(bool(values.get("fallback_used", False))),
            "chain_json": _json(values.get("chain_json") or values.get("chain") or []),
            "rationale_json": _json(values.get("rationale_json") or values.get("rationale") or {}),
            "created_at": values.get("created_at") or _utcnow(),
        }
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_routing_decisions (
                    routing_key, request_key, conversation_key, complexity, selected_provider, fallback_used,
                    chain_json, rationale_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(payload[column] for column in (
                    "routing_key",
                    "request_key",
                    "conversation_key",
                    "complexity",
                    "selected_provider",
                    "fallback_used",
                    "chain_json",
                    "rationale_json",
                    "created_at",
                )),
            )
        row = self.one("SELECT * FROM ai_routing_decisions WHERE routing_key = ?", (routing_key,))
        assert row is not None
        return dict(row)

    def list_ai_routing_decisions(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_routing_decisions ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def list_ai_fallback_entries(
        self,
        *,
        status: str | None = None,
        language: str | None = None,
        channel: str | None = None,
        limit: int = 100,
    ) -> list[dict[str, object]]:
        query = "SELECT * FROM ai_fallback_entries WHERE 1=1"
        params: list[object] = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if language:
            query += " AND language = ?"
            params.append(language)
        if channel:
            query += " AND (channel = ? OR channel = 'all')"
            params.append(channel)
        query += " ORDER BY confidence DESC, usage_count DESC, id ASC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(query, tuple(params))]

    def upsert_ai_fallback_entry(self, **values: object) -> dict[str, object]:
        fallback_key = str(values.get("fallback_key") or "").strip()
        if not fallback_key:
            raise ValueError("fallback_key is required")
        payload = {
            "fallback_key": fallback_key,
            "intent": str(values.get("intent") or fallback_key),
            "question": str(values.get("question") or ""),
            "variants_json": _json(values.get("variants_json") or []),
            "keywords_json": _json(values.get("keywords_json") or []),
            "category": str(values.get("category") or "general"),
            "language": str(values.get("language") or "fr"),
            "channel": str(values.get("channel") or "all"),
            "response_text": str(values.get("response_text") or values.get("answer") or ""),
            "confidence": float(values.get("confidence") or 0.0),
            "validated_at": values.get("validated_at"),
            "validated_by": values.get("validated_by"),
            "version_number": int(values.get("version_number") or 1),
            "status": str(values.get("status") or "published"),
            "expires_at": values.get("expires_at"),
            "usage_count": int(values.get("usage_count") or 0),
            "satisfaction_rate": float(values.get("satisfaction_rate") or 0.0),
            "risk_level": str(values.get("risk_level") or "low"),
            "source_type": str(values.get("source_type") or "manual"),
            "created_at": values.get("created_at") or _utcnow(),
            "updated_at": values.get("updated_at") or _utcnow(),
        }
        return self._upsert_ai_row("ai_fallback_entries", "fallback_key", fallback_key, payload)

    def record_ai_fallback_usage(self, **values: object) -> dict[str, object]:
        usage_key = str(values.get("usage_key") or f"fb-{uuid.uuid4().hex[:12]}")
        payload = {
            "usage_key": usage_key,
            "request_key": str(values.get("request_key") or ""),
            "fallback_key": values.get("fallback_key"),
            "used_generic": int(bool(values.get("used_generic", False))),
            "response_text": str(values.get("response_text") or ""),
            "created_at": values.get("created_at") or _utcnow(),
        }
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_fallback_usage (
                    usage_key, request_key, fallback_key, used_generic, response_text, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                tuple(payload[column] for column in ("usage_key", "request_key", "fallback_key", "used_generic", "response_text", "created_at")),
            )
        row = self.one("SELECT * FROM ai_fallback_usage WHERE usage_key = ?", (usage_key,))
        assert row is not None
        return dict(row)

    def create_ai_learning_candidate(self, **values: object) -> dict[str, object]:
        candidate_key = str(values.get("candidate_key") or f"lc-{uuid.uuid4().hex[:12]}")
        payload = {
            "candidate_key": candidate_key,
            "intent": str(values.get("intent") or candidate_key),
            "question_examples_json": _json(values.get("question_examples_json") or values.get("question_examples") or []),
            "proposed_answer": str(values.get("proposed_answer") or ""),
            "source_count": int(values.get("source_count") or 0),
            "confidence": float(values.get("confidence") or 0.0),
            "risk_level": str(values.get("risk_level") or "low"),
            "language": str(values.get("language") or "fr"),
            "recommended_action": str(values.get("recommended_action") or "review_required"),
            "supporting_conversation_ids_json": _json(
                values.get("supporting_conversation_ids_json") or values.get("supporting_conversation_ids_anonymized") or []
            ),
            "status": str(values.get("status") or "candidate"),
            "created_at": values.get("created_at") or _utcnow(),
            "updated_at": values.get("updated_at") or _utcnow(),
            "published_at": values.get("published_at"),
            "deprecated_at": values.get("deprecated_at"),
        }
        return self._upsert_ai_row("ai_learning_candidates", "candidate_key", candidate_key, payload)

    def list_ai_learning_candidates(self, *, status: str | None = None, limit: int = 50) -> list[dict[str, object]]:
        query = "SELECT * FROM ai_learning_candidates WHERE 1=1"
        params: list[object] = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        return [dict(row) for row in self.all(query, tuple(params))]

    def review_ai_learning_candidate(self, *, candidate_key: str, decision: str, notes: str = "", reviewer_user_id: int | None = None) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_learning_reviews (
                    review_key, candidate_key, reviewer_user_id, decision, notes, reviewed_at, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (f"review-{uuid.uuid4().hex[:12]}", candidate_key, reviewer_user_id, decision, notes, now, now),
            )
            columns = self._table_columns(conn, "ai_learning_candidates")
            if "updated_at" in columns:
                conn.execute(
                    "UPDATE ai_learning_candidates SET status = ?, updated_at = ? WHERE candidate_key = ?",
                    (decision, now, candidate_key),
                )
            else:
                conn.execute(
                    "UPDATE ai_learning_candidates SET status = ? WHERE candidate_key = ?",
                    (decision, candidate_key),
                )
        row = self.one("SELECT * FROM ai_learning_candidates WHERE candidate_key = ?", (candidate_key,))
        assert row is not None
        return dict(row)

    def publish_ai_learning_candidate(self, *, candidate_key: str, reviewer_user_id: int | None = None) -> dict[str, object]:
        candidate = self.review_ai_learning_candidate(candidate_key=candidate_key, decision="published", reviewer_user_id=reviewer_user_id)
        entry = self.upsert_ai_fallback_entry(
            fallback_key=str(candidate["candidate_key"]),
            intent=str(candidate["intent"]),
            question=" ".join(self._json_list(candidate.get("question_examples_json"))),
            variants_json=self._json_list(candidate.get("question_examples_json")),
            keywords_json=self._json_list(candidate.get("question_examples_json")),
            category="learning",
            language=str(candidate.get("language") or "fr"),
            channel="all",
            response_text=str(candidate.get("proposed_answer") or ""),
            confidence=float(candidate.get("confidence") or 0.0),
            validated_at=_utcnow(),
            validated_by=str(reviewer_user_id or "human"),
            version_number=1,
            status="published",
            source_type="learning",
            created_at=str(candidate.get("created_at") or _utcnow()),
            updated_at=_utcnow(),
        )
        with self._transaction() as conn:
            columns = self._table_columns(conn, "ai_learning_candidates")
            if "updated_at" in columns:
                conn.execute(
                    "UPDATE ai_learning_candidates SET published_at = ?, status = 'published', updated_at = ? WHERE candidate_key = ?",
                    (_utcnow(), _utcnow(), candidate_key),
                )
            else:
                conn.execute(
                    "UPDATE ai_learning_candidates SET published_at = ?, status = 'published' WHERE candidate_key = ?",
                    (_utcnow(), candidate_key),
                )
        return {"candidate": candidate, "fallback_entry": entry}

    def deprecate_ai_learning_candidate(self, *, candidate_key: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            columns = self._table_columns(conn, "ai_learning_candidates")
            if "updated_at" in columns:
                conn.execute(
                    "UPDATE ai_learning_candidates SET status = 'deprecated', deprecated_at = ?, updated_at = ? WHERE candidate_key = ?",
                    (now, now, candidate_key),
                )
            else:
                conn.execute(
                    "UPDATE ai_learning_candidates SET status = 'deprecated', deprecated_at = ? WHERE candidate_key = ?",
                    (now, candidate_key),
                )
        row = self.one("SELECT * FROM ai_learning_candidates WHERE candidate_key = ?", (candidate_key,))
        assert row is not None
        return dict(row)

    def create_ai_knowledge_version(self, *, version_number: int, status: str = "draft", summary: str = "", rolled_back_to_version_id: int | None = None) -> dict[str, object]:
        version_key = f"kv-{uuid.uuid4().hex[:12]}"
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_knowledge_versions (
                    version_key, version_number, status, summary, created_at, published_at, rolled_back_at,
                    rolled_back_to_version_id
                ) VALUES (?, ?, ?, ?, ?, NULL, NULL, ?)
                """,
                (version_key, version_number, status, summary, now, rolled_back_to_version_id),
            )
        row = self.one("SELECT * FROM ai_knowledge_versions WHERE version_key = ?", (version_key,))
        assert row is not None
        return dict(row)

    def list_ai_knowledge_versions(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_knowledge_versions ORDER BY version_number DESC, id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    def rollback_ai_knowledge_version(self, *, version_key: str) -> dict[str, object]:
        now = _utcnow()
        with self._transaction() as conn:
            conn.execute(
                "UPDATE ai_knowledge_versions SET status = 'rolled_back', rolled_back_at = ? WHERE version_key = ?",
                (now, version_key),
            )
        row = self.one("SELECT * FROM ai_knowledge_versions WHERE version_key = ?", (version_key,))
        assert row is not None
        return dict(row)

    def record_ai_feedback(self, **values: object) -> dict[str, object]:
        feedback_key = str(values.get("feedback_key") or f"fbk-{uuid.uuid4().hex[:12]}")
        payload = {
            "feedback_key": feedback_key,
            "request_key": str(values.get("request_key") or ""),
            "conversation_key": str(values.get("conversation_key") or ""),
            "rating": int(values.get("rating") or 0),
            "satisfaction": int(values.get("satisfaction") or 0),
            "outcome": str(values.get("outcome") or ""),
            "notes": str(values.get("notes") or ""),
            "created_at": values.get("created_at") or _utcnow(),
        }
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_feedback (
                    feedback_key, request_key, conversation_key, rating, satisfaction, outcome, notes, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(payload[column] for column in ("feedback_key", "request_key", "conversation_key", "rating", "satisfaction", "outcome", "notes", "created_at")),
            )
        row = self.one("SELECT * FROM ai_feedback WHERE feedback_key = ?", (feedback_key,))
        assert row is not None
        return dict(row)

    def record_ai_cost_estimate(self, **values: object) -> dict[str, object]:
        estimate_key = str(values.get("estimate_key") or f"cost-{uuid.uuid4().hex[:12]}")
        payload = {
            "estimate_key": estimate_key,
            "request_key": str(values.get("request_key") or ""),
            "provider_key": str(values.get("provider_key") or ""),
            "model": str(values.get("model") or ""),
            "input_tokens": int(values.get("input_tokens") or 0),
            "output_tokens": int(values.get("output_tokens") or 0),
            "estimated_cost": float(values.get("estimated_cost") or 0.0),
            "created_at": values.get("created_at") or _utcnow(),
        }
        with self._transaction() as conn:
            conn.execute(
                """
                INSERT INTO ai_cost_estimates (
                    estimate_key, request_key, provider_key, model, input_tokens, output_tokens, estimated_cost, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(payload[column] for column in ("estimate_key", "request_key", "provider_key", "model", "input_tokens", "output_tokens", "estimated_cost", "created_at")),
            )
        row = self.one("SELECT * FROM ai_cost_estimates WHERE estimate_key = ?", (estimate_key,))
        assert row is not None
        return dict(row)

    def list_ai_cost_estimates(self, *, limit: int = 50) -> list[dict[str, object]]:
        rows = self.all("SELECT * FROM ai_cost_estimates ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in rows]

    @staticmethod
    def _json_list(value: object | None) -> list[str]:
        parsed = _parse_json(value if isinstance(value, str) else _json(value))
        if isinstance(parsed, list):
            return [str(item) for item in parsed if str(item).strip()]
        return []

    def ai_overview(self) -> dict[str, object]:
        return {
            "providers_total": self.scalar("SELECT COUNT(*) FROM ai_providers"),
            "requests_total": self.scalar("SELECT COUNT(*) FROM ai_requests"),
            "responses_total": self.scalar("SELECT COUNT(*) FROM ai_responses"),
            "alerts_total": self.scalar("SELECT COUNT(*) FROM ai_alerts"),
            "candidates_total": self.scalar("SELECT COUNT(*) FROM ai_learning_candidates"),
            "fallback_entries_total": self.scalar("SELECT COUNT(*) FROM ai_fallback_entries"),
            "knowledge_versions_total": self.scalar("SELECT COUNT(*) FROM ai_knowledge_versions"),
        }
