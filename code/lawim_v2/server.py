from __future__ import annotations

import argparse
import json
import logging
import mimetypes
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .config import AppConfig
from .db import LawimRepository
from .matching import MatchCriteria


LOGGER = logging.getLogger("lawim_v2")


class ApiError(Exception):
    def __init__(self, status: HTTPStatus, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


class LawimThreadingHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


class LawimRequestHandler(BaseHTTPRequestHandler):
    server_version = "LAWIM_V2/0.1"
    repository: LawimRepository
    config: AppConfig

    def do_GET(self) -> None:  # noqa: N802
        try:
            self._handle_get()
        except ApiError as exc:
            self._send_json_error(exc.status, exc.code, exc.message)
        except Exception as exc:  # pragma: no cover - unexpected runtime failure
            LOGGER.exception("Unhandled GET error: %s", exc)
            self._send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "Unexpected server error")

    def do_POST(self) -> None:  # noqa: N802
        try:
            self._handle_post()
        except ApiError as exc:
            self._send_json_error(exc.status, exc.code, exc.message)
        except Exception as exc:  # pragma: no cover - unexpected runtime failure
            LOGGER.exception("Unhandled POST error: %s", exc)
            self._send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "Unexpected server error")

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        LOGGER.info("%s - %s", self.address_string(), format % args)

    def _handle_get(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path in {"/", "/index.html"}:
            self._send_static("index.html", "text/html; charset=utf-8")
            return
        if path == "/app.js":
            self._send_static("app.js", "application/javascript; charset=utf-8")
            return
        if path == "/styles.css":
            self._send_static("styles.css", "text/css; charset=utf-8")
            return
        if path == "/healthz":
            self._send_text("ok", content_type="text/plain; charset=utf-8")
            return
        if path.startswith("/api/"):
            self._handle_api_get(parsed)
            return

        if "." not in path.strip("/"):
            self._send_static("index.html", "text/html; charset=utf-8")
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Resource not found")

    def _handle_post(self) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Resource not found")
        body = self._read_json_body()
        self._handle_api_post(parsed, body)

    def _handle_api_get(self, parsed) -> None:
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/health":
            payload = {
                "status": "ok",
                "environment": {
                    "app_env": self.config.app_env,
                    "stack_profile": self.config.stack_profile,
                    "log_level": self.config.log_level,
                    "public_base_url": self.config.public_base_url,
                    "secret_provider": self.config.secret_provider,
                },
                "database": {
                    "driver": "sqlite",
                    "path": str(self.config.db_path),
                },
                "summary": self.repository.summary(),
            }
            self._send_json(payload)
            return

        if path == "/api/bootstrap":
            token = self._bearer_token(optional=True)
            payload = self.repository.bootstrap_payload(token=token)
            self._send_json(payload)
            return

        if path == "/api/me":
            user = self._require_user()
            self._send_json({"user": self.repository.public_user(user)})
            return

        if path == "/api/organizations":
            self._send_json({"organizations": self.repository.list_organizations(limit=self._query_limit(query))})
            return

        if path == "/api/users":
            self._send_json({"users": self.repository.list_users(limit=self._query_limit(query))})
            return

        if path == "/api/properties":
            city = self._first(query, "city")
            status = self._first(query, "status")
            self._send_json({"properties": self.repository.list_properties(city=city, status=status, limit=self._query_limit(query))})
            return

        if path.startswith("/api/properties/") and path.endswith("/media"):
            property_id = self._extract_property_id(path, suffix="/media")
            self._send_json({"media": self.repository.list_media(property_id=property_id)})
            return

        if path.startswith("/api/properties/"):
            property_id = self._extract_property_id(path)
            property_row = self.repository.get_property(property_id)
            property_row["media"] = self.repository.list_media(property_id=property_id)
            self._send_json({"property": property_row})
            return

        if path == "/api/conversations":
            self._send_json({"conversations": self.repository.list_conversations(limit=self._query_limit(query))})
            return

        if path.startswith("/api/conversations/") and path.endswith("/messages"):
            conversation_id = self._extract_conversation_id(path, suffix="/messages")
            self._send_json({"messages": self.repository.list_messages(conversation_id)})
            return

        if path.startswith("/api/conversations/"):
            conversation_id = self._extract_conversation_id(path)
            conversation = self.repository.get_conversation(conversation_id)
            if conversation is None:
                raise ApiError(HTTPStatus.NOT_FOUND, "conversation_not_found", "Conversation not found")
            conversation["messages"] = self.repository.list_messages(conversation_id)
            self._send_json({"conversation": conversation})
            return

        if path == "/api/matches":
            criteria = self._build_match_criteria(query)
            self._send_json({"matches": self.repository.matched_properties(criteria), "criteria": asdict(criteria)})
            return

        if path == "/api/media":
            property_id = self._first_int(query, "property_id")
            self._send_json({"media": self.repository.list_media(property_id=property_id, limit=self._query_limit(query))})
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _handle_api_post(self, parsed, body: dict[str, Any]) -> None:
        path = parsed.path

        if path == "/api/auth/login":
            email = self._require_text(body, "email")
            password = self._require_text(body, "password")
            user = self.repository.authenticate(email=email, password=password)
            if user is None:
                raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_credentials", "Invalid email or password")
            session = self.repository.create_session(user_id=user["id"], ttl_seconds=self.config.session_ttl_seconds)
            self._send_json(
                {
                    "token": session["token"],
                    "session": session,
                    "user": self.repository.public_user(user),
                },
                status=HTTPStatus.CREATED,
            )
            return

        if path == "/api/auth/register":
            email = self._require_text(body, "email")
            password = self._require_text(body, "password")
            full_name = self._require_text(body, "full_name")
            role = self._coerce_role(body.get("role"))
            organization_id = self._optional_int(body.get("organization_id"))
            user = self.repository.create_user(
                email=email,
                full_name=full_name,
                role=role,
                password=password,
                organization_id=organization_id,
            )
            session = self.repository.create_session(user_id=user["id"], ttl_seconds=self.config.session_ttl_seconds)
            self._send_json(
                {
                    "token": session["token"],
                    "session": session,
                    "user": self.repository.public_user(user),
                },
                status=HTTPStatus.CREATED,
            )
            return

        if path == "/api/auth/logout":
            token = self._bearer_token(optional=True)
            if token:
                self.repository.delete_session(token)
            self._send_json({"status": "logged_out"})
            return

        user = self._require_user()

        if path == "/api/organizations":
            organization = self.repository.create_organization(
                name=self._require_text(body, "name"),
                slug=self._require_text(body, "slug"),
                kind=self._coerce_kind(body.get("kind")),
                city=self._optional_text(body.get("city")),
            )
            self._send_json({"organization": organization}, status=HTTPStatus.CREATED)
            return

        if path == "/api/users":
            user_row = self.repository.create_user(
                email=self._require_text(body, "email"),
                full_name=self._require_text(body, "full_name"),
                role=self._coerce_role(body.get("role")),
                password=self._require_text(body, "password"),
                organization_id=self._optional_int(body.get("organization_id")),
            )
            self._send_json({"user": self.repository.public_user(user_row)}, status=HTTPStatus.CREATED)
            return

        if path == "/api/properties":
            property_row = self.repository.create_property(
                title=self._require_text(body, "title"),
                summary=self._optional_text(body.get("summary")) or "Bien LAWIM_V2",
                city=self._require_text(body, "city"),
                country=self._optional_text(body.get("country")) or "Cameroon",
                latitude=self._optional_float(body.get("latitude")),
                longitude=self._optional_float(body.get("longitude")),
                price_min=self._optional_int(body.get("price_min")),
                price_max=self._optional_int(body.get("price_max")),
                currency=self._optional_text(body.get("currency")) or "XAF",
                status=self._coerce_status(body.get("status")),
                property_type=self._optional_text(body.get("property_type")) or "apartment",
                owner_organization_id=self._optional_int(body.get("owner_organization_id")),
                bedrooms=self._optional_int(body.get("bedrooms")) or 0,
                bathrooms=self._optional_int(body.get("bathrooms")) or 0,
                area_sqm=self._optional_float(body.get("area_sqm")) or 0.0,
            )
            self._send_json({"property": property_row}, status=HTTPStatus.CREATED)
            return

        if path == "/api/media":
            media_row = self.repository.create_media(
                property_id=self._require_int(body, "property_id"),
                kind=self._optional_text(body.get("kind")) or "image",
                url=self._require_text(body, "url"),
                caption=self._optional_text(body.get("caption")) or "LAWIM_V2 media",
            )
            self._send_json({"media": media_row}, status=HTTPStatus.CREATED)
            return

        if path == "/api/conversations":
            conversation = self.repository.create_conversation(
                user_id=self._require_int(body, "user_id", default=user["id"]),
                property_id=self._optional_int(body.get("property_id")),
                subject=self._require_text(body, "subject"),
                status=self._coerce_status(body.get("status"), default="open"),
                initial_message=self._optional_text(body.get("initial_message")),
                sender_user_id=self._optional_int(body.get("sender_user_id")) or user["id"],
            )
            self._send_json({"conversation": conversation}, status=HTTPStatus.CREATED)
            return

        if path.startswith("/api/conversations/") and path.endswith("/messages"):
            conversation_id = self._extract_conversation_id(path, suffix="/messages")
            message = self.repository.add_message(
                conversation_id=conversation_id,
                sender_user_id=self._require_int(body, "sender_user_id", default=user["id"]),
                body=self._require_text(body, "body"),
            )
            self._send_json({"message": message}, status=HTTPStatus.CREATED)
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _require_user(self) -> dict[str, object]:
        token = self._bearer_token(optional=False)
        user = self.repository.get_user_by_session(token)
        if user is None:
            raise ApiError(HTTPStatus.UNAUTHORIZED, "unauthorized", "Valid session required")
        return user

    def _bearer_token(self, *, optional: bool) -> str | None:
        authorization = self.headers.get("Authorization", "")
        if authorization.lower().startswith("bearer "):
            token = authorization.split(" ", 1)[1].strip()
            return token or None
        if optional:
            return None
        raise ApiError(HTTPStatus.UNAUTHORIZED, "missing_token", "Bearer token required")

    def _read_json_body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            payload = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_json", "Request body must be valid JSON") from exc
        if not isinstance(payload, dict):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_json", "Request body must be a JSON object")
        return payload

    def _send_json(self, payload: dict[str, Any], *, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.end_headers()
        self.wfile.write(body)

    def _send_json_error(self, status: HTTPStatus, code: str, message: str) -> None:
        self._send_json({"error": {"code": code, "message": message}}, status=status)

    def _send_text(self, text: str, *, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, name: str, content_type: str) -> None:
        try:
            content = resources.files("lawim_v2.static").joinpath(name).read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ApiError(HTTPStatus.NOT_FOUND, "asset_not_found", f"Static asset not found: {name}") from exc
        self._send_text(content, content_type=content_type)

    def _require_text(self, payload: dict[str, Any], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Field '{key}' must be a non-empty string")
        return value.strip()

    def _optional_text(self, value: object) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or None
        return str(value)

    def _optional_int(self, value: object) -> int | None:
        if value is None or value == "":
            return None
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Expected an integer") from exc

    def _require_int(self, payload: dict[str, Any], key: str, default: int | None = None) -> int:
        value = payload.get(key, default)
        if value is None:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Field '{key}' is required")
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Field '{key}' must be an integer") from exc

    def _optional_float(self, value: object) -> float | None:
        if value is None or value == "":
            return None
        try:
            return float(value)
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Expected a number") from exc

    def _coerce_role(self, value: object | None) -> str:
        if not isinstance(value, str):
            return "agent"
        normalized = value.strip().lower()
        return normalized if normalized in {"admin", "agent", "owner"} else "agent"

    def _coerce_kind(self, value: object | None) -> str:
        if not isinstance(value, str):
            return "agency"
        normalized = value.strip().lower()
        return normalized if normalized in {"agency", "partner", "owner"} else "agency"

    def _coerce_status(self, value: object | None, default: str = "published") -> str:
        if not isinstance(value, str):
            return default
        normalized = value.strip().lower()
        return normalized if normalized in {"draft", "open", "closed", "published", "archived"} else default

    def _first(self, query: dict[str, list[str]], key: str) -> str | None:
        value = query.get(key)
        if not value:
            return None
        stripped = value[0].strip()
        return stripped or None

    def _first_int(self, query: dict[str, list[str]], key: str) -> int | None:
        value = self._first(query, key)
        if value is None:
            return None
        try:
            return int(value)
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", f"Query '{key}' must be an integer") from exc

    def _query_limit(self, query: dict[str, list[str]]) -> int:
        value = self._first_int(query, "limit")
        if value is None:
            return 10
        return max(1, min(value, 100))

    def _build_match_criteria(self, query: dict[str, list[str]]) -> MatchCriteria:
        return MatchCriteria(
            city=self._first(query, "city"),
            budget_min=self._first_int(query, "budget_min"),
            budget_max=self._first_int(query, "budget_max"),
            latitude=self._optional_float(self._first(query, "latitude")),
            longitude=self._optional_float(self._first(query, "longitude")),
            limit=self._query_limit(query),
        )

    def _extract_property_id(self, path: str, suffix: str = "") -> int:
        marker = "/api/properties/"
        if suffix and not path.endswith(suffix):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Property route not found")
        raw_id = path[len(marker) : len(path) - len(suffix) if suffix else None]
        try:
            return int(raw_id.strip("/"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_property_id", "Property id must be numeric") from exc

    def _extract_conversation_id(self, path: str, suffix: str = "") -> int:
        marker = "/api/conversations/"
        if suffix and not path.endswith(suffix):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Conversation route not found")
        raw_id = path[len(marker) : len(path) - len(suffix) if suffix else None]
        try:
            return int(raw_id.strip("/"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_conversation_id", "Conversation id must be numeric") from exc


def create_server(config: AppConfig) -> LawimThreadingHTTPServer:
    repository = LawimRepository(config.db_path)
    repository.initialize(seed_demo_data=config.seed_demo_data)

    class BoundHandler(LawimRequestHandler):
        pass

    BoundHandler.repository = repository
    BoundHandler.config = config

    server = LawimThreadingHTTPServer((config.host, config.port), BoundHandler)
    server.repository = repository  # type: ignore[attr-defined]
    server.config = config  # type: ignore[attr-defined]
    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the LAWIM_V2 executable baseline")
    parser.add_argument("--host", default=None, help="Host to bind")
    parser.add_argument("--port", type=int, default=None, help="Port to bind")
    parser.add_argument("--db", default=None, help="SQLite database path")
    parser.add_argument("--no-seed", action="store_true", help="Skip demo data seeding")
    args = parser.parse_args(argv)

    config = AppConfig.from_env()
    if args.host:
        config = config.__class__(
            host=args.host,
            port=config.port,
            db_path=config.db_path,
            app_env=config.app_env,
            stack_profile=config.stack_profile,
            log_level=config.log_level,
            public_base_url=config.public_base_url,
            secret_provider=config.secret_provider,
            seed_demo_data=config.seed_demo_data,
            session_ttl_seconds=config.session_ttl_seconds,
        )
    if args.port:
        config = config.__class__(
            host=config.host,
            port=args.port,
            db_path=config.db_path,
            app_env=config.app_env,
            stack_profile=config.stack_profile,
            log_level=config.log_level,
            public_base_url=config.public_base_url,
            secret_provider=config.secret_provider,
            seed_demo_data=config.seed_demo_data,
            session_ttl_seconds=config.session_ttl_seconds,
        )
    if args.db:
        config = config.__class__(
            host=config.host,
            port=config.port,
            db_path=Path(args.db),
            app_env=config.app_env,
            stack_profile=config.stack_profile,
            log_level=config.log_level,
            public_base_url=config.public_base_url,
            secret_provider=config.secret_provider,
            seed_demo_data=config.seed_demo_data,
            session_ttl_seconds=config.session_ttl_seconds,
        )
    if args.no_seed:
        config = config.__class__(
            host=config.host,
            port=config.port,
            db_path=config.db_path,
            app_env=config.app_env,
            stack_profile=config.stack_profile,
            log_level=config.log_level,
            public_base_url=config.public_base_url,
            secret_provider=config.secret_provider,
            seed_demo_data=False,
            session_ttl_seconds=config.session_ttl_seconds,
        )

    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    config.ensure_runtime_dir()
    server = create_server(config)
    LOGGER.info("LAWIM_V2 listening on http://%s:%s", config.host, config.port)
    LOGGER.info("Database path: %s", config.db_path)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        LOGGER.info("Shutdown requested")
    finally:
        server.shutdown()
        server.server_close()
        server.repository.close()  # type: ignore[attr-defined]
    return 0
