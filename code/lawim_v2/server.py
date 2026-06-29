from __future__ import annotations

import argparse
import json
import logging
import sqlite3
from dataclasses import asdict, replace
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .config import AppConfig
from .db import LawimRepository, RepositoryError
from .matching import MatchCriteria
from .services import LawimServices, ServiceError


LOGGER = logging.getLogger("lawim_v2")
MAX_JSON_BODY_BYTES = 1_048_576


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
    services: LawimServices

    def do_GET(self) -> None:  # noqa: N802
        self._handle_request(self._handle_get)

    def do_POST(self) -> None:  # noqa: N802
        self._handle_request(self._handle_post)

    def do_PUT(self) -> None:  # noqa: N802
        self._handle_request(self._handle_put)

    def do_PATCH(self) -> None:  # noqa: N802
        self._handle_request(self._handle_patch)

    def do_DELETE(self) -> None:  # noqa: N802
        self._handle_request(self._handle_delete)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        LOGGER.info("%s - %s", self.address_string(), format % args)

    def _handle_request(self, handler) -> None:
        try:
            handler()
        except ApiError as exc:
            self._send_json_error(exc.status, exc.code, exc.message)
        except ServiceError as exc:
            self._send_json_error(exc.status, exc.code, exc.message)
        except RepositoryError as exc:
            self._send_json_error(exc.status, exc.code, str(exc))
        except Exception as exc:  # pragma: no cover - unexpected runtime failure
            LOGGER.exception("Unhandled %s error: %s", self.command, exc)
            self._send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "Unexpected server error")

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
            self._send_json(self.services.health())
            return

        if path == "/api/bootstrap":
            token = self._bearer_token(optional=True)
            payload = self.repository.bootstrap_payload(token=token)
            self._send_json(payload)
            return

        if path == "/api/events":
            actor = self._require_user()
            self._send_json({"events": self.services.events(actor=actor, limit=self._query_limit(query))})
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
            conversation["messages"] = self.repository.list_messages(conversation_id)
            self._send_json({"conversation": conversation})
            return

        if path == "/api/matches":
            criteria = self._build_match_criteria(query)
            self._send_json({"matches": self.repository.matched_properties(criteria), "criteria": asdict(criteria)})
            return

        if path == "/api/media":
            property_id = self._first_int(query, "property_id", minimum=1)
            self._send_json({"media": self.repository.list_media(property_id=property_id, limit=self._query_limit(query))})
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _handle_api_post(self, parsed, body: dict[str, Any]) -> None:
        path = parsed.path

        if path == "/api/auth/login":
            email = self._require_text(body, "email")
            password = self._require_text(body, "password")
            payload = self.services.login(email=email, password=password)
            self._send_json(payload, status=HTTPStatus.CREATED)
            return

        if path == "/api/auth/register":
            email = self._require_text(body, "email")
            password = self._require_text(body, "password")
            full_name = self._require_text(body, "full_name")
            role = self._coerce_role(body.get("role"))
            organization_id = self._optional_int(body.get("organization_id"), minimum=1)
            payload = self.services.register(
                actor=None,
                email=email,
                password=password,
                full_name=full_name,
                role=role,
                organization_id=organization_id,
            )
            self._send_json(payload, status=HTTPStatus.CREATED)
            return

        if path == "/api/auth/logout":
            token = self._bearer_token(optional=True)
            self._send_json(self.services.logout(token=token))
            return

        actor = self._require_user()

        if path == "/api/organizations":
            organization = self.services.create_organization(
                actor=actor,
                name=self._require_text(body, "name"),
                slug=self._require_text(body, "slug"),
                kind=self._coerce_kind(body.get("kind")),
                city=self._optional_text(body.get("city")),
            )
            self._send_json({"organization": organization}, status=HTTPStatus.CREATED)
            return

        if path == "/api/users":
            user_row = self.services.create_user(
                actor=actor,
                email=self._require_text(body, "email"),
                full_name=self._require_text(body, "full_name"),
                role=self._coerce_role(body.get("role")),
                password=self._require_text(body, "password"),
                organization_id=self._optional_int(body.get("organization_id"), minimum=1),
            )
            self._send_json({"user": self.repository.public_user(user_row)}, status=HTTPStatus.CREATED)
            return

        if path == "/api/properties":
            property_row = self.services.create_property(
                actor=actor,
                title=self._require_text(body, "title"),
                summary=self._optional_text(body.get("summary")) or "Bien LAWIM_V2",
                city=self._require_text(body, "city"),
                country=self._optional_text(body.get("country")) or "Cameroon",
                latitude=self._optional_float(body.get("latitude")),
                longitude=self._optional_float(body.get("longitude")),
                price_min=self._optional_int(body.get("price_min"), minimum=0),
                price_max=self._optional_int(body.get("price_max"), minimum=0),
                currency=self._optional_text(body.get("currency")) or "XAF",
                status=self._coerce_status(body.get("status")),
                property_type=self._optional_text(body.get("property_type")) or "apartment",
                owner_organization_id=self._optional_int(body.get("owner_organization_id"), minimum=1),
                bedrooms=self._optional_int(body.get("bedrooms"), minimum=0) or 0,
                bathrooms=self._optional_int(body.get("bathrooms"), minimum=0) or 0,
                area_sqm=self._optional_float(body.get("area_sqm")) or 0.0,
            )
            self._send_json({"property": property_row}, status=HTTPStatus.CREATED)
            return

        if path == "/api/media":
            media_row = self.services.create_media(
                actor=actor,
                property_id=self._require_int(body, "property_id", minimum=1),
                kind=self._optional_text(body.get("kind")) or "image",
                url=self._require_text(body, "url"),
                caption=self._optional_text(body.get("caption")) or "LAWIM_V2 media",
            )
            self._send_json({"media": media_row}, status=HTTPStatus.CREATED)
            return

        if path == "/api/conversations":
            conversation = self.services.create_conversation(
                actor=actor,
                user_id=self._require_int(body, "user_id", default=int(actor["id"]), minimum=1),
                property_id=self._optional_int(body.get("property_id"), minimum=1),
                subject=self._require_text(body, "subject"),
                status=self._coerce_status(body.get("status"), default="open"),
                initial_message=self._optional_text(body.get("initial_message")),
                sender_user_id=self._optional_int(body.get("sender_user_id"), minimum=1) or int(actor["id"]),
            )
            self._send_json({"conversation": conversation}, status=HTTPStatus.CREATED)
            return

        if path.startswith("/api/conversations/") and path.endswith("/messages"):
            conversation_id = self._extract_conversation_id(path, suffix="/messages")
            message = self.services.add_message(
                actor=actor,
                conversation_id=conversation_id,
                sender_user_id=self._require_int(body, "sender_user_id", default=int(actor["id"]), minimum=1),
                body=self._require_text(body, "body"),
            )
            self._send_json({"message": message}, status=HTTPStatus.CREATED)
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _handle_put(self) -> None:
        self._handle_mutation("PUT")

    def _handle_patch(self) -> None:
        self._handle_mutation("PATCH")

    def _handle_delete(self) -> None:
        self._handle_mutation("DELETE")

    def _handle_mutation(self, method: str) -> None:
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/"):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Resource not found")
        body = self._read_json_body()
        path = parsed.path
        actor = self._require_user()

        if path.startswith("/api/organizations/") and path.count("/") == 3:
            organization_id = self._extract_resource_id(path, "/api/organizations/", resource="Organization")
            if method == "DELETE":
                raise ApiError(HTTPStatus.METHOD_NOT_ALLOWED, "method_not_allowed", "Organizations cannot be deleted in this baseline")
            organization = self.services.update_organization(
                actor=actor,
                organization_id=organization_id,
                name=self._optional_text(body.get("name")),
                slug=self._optional_text(body.get("slug")),
                kind=self._optional_text(body.get("kind")),
                city=self._optional_text(body.get("city")),
            )
            self._send_json({"organization": organization})
            return

        if path.startswith("/api/users/") and path.count("/") == 3:
            user_id = self._extract_resource_id(path, "/api/users/", resource="User")
            if method == "DELETE":
                payload = self.services.delete_user(actor=actor, user_id=user_id)
                self._send_json(payload)
                return
            user_row = self.services.update_user(
                actor=actor,
                user_id=user_id,
                email=self._optional_text(body.get("email")),
                full_name=self._optional_text(body.get("full_name")),
                role=self._optional_text(body.get("role")),
                password=self._optional_text(body.get("password")),
                organization_id=self._optional_int(body.get("organization_id"), minimum=1),
            )
            self._send_json({"user": self.repository.public_user(user_row)})
            return

        if path.startswith("/api/properties/") and path.count("/") == 3:
            property_id = self._extract_property_id(path)
            if method == "DELETE":
                payload = self.services.delete_property(actor=actor, property_id=property_id)
                self._send_json(payload)
                return
            property_row = self.services.update_property(
                actor=actor,
                property_id=property_id,
                title=self._optional_text(body.get("title")),
                summary=self._optional_text(body.get("summary")),
                city=self._optional_text(body.get("city")),
                country=self._optional_text(body.get("country")),
                latitude=self._optional_float(body.get("latitude")),
                longitude=self._optional_float(body.get("longitude")),
                price_min=self._optional_int(body.get("price_min"), minimum=0),
                price_max=self._optional_int(body.get("price_max"), minimum=0),
                currency=self._optional_text(body.get("currency")),
                status=self._optional_text(body.get("status")),
                property_type=self._optional_text(body.get("property_type")),
                owner_organization_id=self._optional_int(body.get("owner_organization_id"), minimum=1),
                bedrooms=self._optional_int(body.get("bedrooms"), minimum=0),
                bathrooms=self._optional_int(body.get("bathrooms"), minimum=0),
                area_sqm=self._optional_float(body.get("area_sqm")),
            )
            self._send_json({"property": property_row})
            return

        if path.startswith("/api/media/") and path.count("/") == 3:
            media_id = self._extract_resource_id(path, "/api/media/", resource="Media")
            if method == "DELETE":
                payload = self.services.delete_media(actor=actor, media_id=media_id)
                self._send_json(payload)
                return
            media_row = self.services.update_media(
                actor=actor,
                media_id=media_id,
                kind=self._optional_text(body.get("kind")),
                url=self._optional_text(body.get("url")),
                caption=self._optional_text(body.get("caption")),
            )
            self._send_json({"media": media_row})
            return

        if path.startswith("/api/conversations/") and path.count("/") == 3:
            conversation_id = self._extract_conversation_id(path)
            if method == "DELETE":
                payload = self.services.delete_conversation(actor=actor, conversation_id=conversation_id)
                self._send_json(payload)
                return
            conversation = self.services.update_conversation(
                actor=actor,
                conversation_id=conversation_id,
                subject=self._optional_text(body.get("subject")),
                status=self._optional_text(body.get("status")),
            )
            self._send_json({"conversation": conversation})
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
        content_length = self.headers.get("Content-Length", "0")
        try:
            length = int(content_length)
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_content_length", "Content-Length must be an integer") from exc
        if length < 0:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_content_length", "Content-Length must be non-negative")
        if length <= 0:
            return {}
        if length > MAX_JSON_BODY_BYTES:
            raise ApiError(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "payload_too_large", "Request body exceeds the supported size")
        content_type = self.headers.get("Content-Type", "")
        if "application/json" not in content_type.lower():
            raise ApiError(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "unsupported_media_type", "Mutating requests must use application/json")
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

    def _send_json(
        self,
        payload: dict[str, Any],
        *,
        status: HTTPStatus = HTTPStatus.OK,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        if status == HTTPStatus.UNAUTHORIZED:
            self.send_header("WWW-Authenticate", 'Bearer realm="LAWIM_V2"')
        if extra_headers:
            for header, value in extra_headers.items():
                self.send_header(header, value)
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
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'self'; form-action 'self'",
        )
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
        if not isinstance(value, str):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Optional text fields must be strings")
        stripped = value.strip()
        return stripped or None

    def _optional_int(self, value: object, *, minimum: int | None = None) -> int | None:
        if value is None or value == "":
            return None
        try:
            parsed = int(value)
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Expected an integer") from exc
        if minimum is not None and parsed < minimum:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Expected an integer greater than or equal to {minimum}")
        return parsed

    def _require_int(self, payload: dict[str, Any], key: str, default: int | None = None, *, minimum: int | None = None) -> int:
        value = payload.get(key, default)
        if value is None:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Field '{key}' is required")
        try:
            parsed = int(value)
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Field '{key}' must be an integer") from exc
        if minimum is not None and parsed < minimum:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", f"Field '{key}' must be greater than or equal to {minimum}")
        return parsed

    def _optional_float(self, value: object) -> float | None:
        if value is None or value == "":
            return None
        try:
            parsed = float(value)
        except (TypeError, ValueError) as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Expected a number") from exc
        if not float("-inf") < parsed < float("inf"):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Expected a finite number")
        return parsed

    def _coerce_role(self, value: object | None) -> str:
        if value is None:
            return "agent"
        if not isinstance(value, str):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'role' must be a string")
        normalized = value.strip().lower()
        if normalized not in {"admin", "agent", "owner"}:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'role' must be one of admin, agent or owner")
        return normalized

    def _coerce_kind(self, value: object | None) -> str:
        if value is None:
            return "agency"
        if not isinstance(value, str):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'kind' must be a string")
        normalized = value.strip().lower()
        if normalized not in {"agency", "partner", "owner"}:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'kind' must be one of agency, partner or owner")
        return normalized

    def _coerce_status(self, value: object | None, default: str = "published") -> str:
        if value is None:
            return default
        if not isinstance(value, str):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'status' must be a string")
        normalized = value.strip().lower()
        if normalized not in {"draft", "open", "closed", "published", "archived"}:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'status' must be one of draft, open, closed, published or archived")
        return normalized

    def _first(self, query: dict[str, list[str]], key: str) -> str | None:
        value = query.get(key)
        if not value:
            return None
        stripped = value[0].strip()
        return stripped or None

    def _first_int(self, query: dict[str, list[str]], key: str, *, minimum: int | None = None) -> int | None:
        value = self._first(query, key)
        if value is None:
            return None
        try:
            parsed = int(value)
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", f"Query '{key}' must be an integer") from exc
        if minimum is not None and parsed < minimum:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", f"Query '{key}' must be greater than or equal to {minimum}")
        return parsed

    def _query_limit(self, query: dict[str, list[str]]) -> int:
        value = self._first_int(query, "limit", minimum=1)
        if value is None:
            return 10
        if value > 100:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", "Query 'limit' must not exceed 100")
        return value

    def _build_match_criteria(self, query: dict[str, list[str]]) -> MatchCriteria:
        budget_min = self._first_int(query, "budget_min", minimum=0)
        budget_max = self._first_int(query, "budget_max", minimum=0)
        if budget_min is not None and budget_max is not None and budget_min > budget_max:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", "Query 'budget_min' cannot exceed 'budget_max'")
        return MatchCriteria(
            city=self._first(query, "city"),
            budget_min=budget_min,
            budget_max=budget_max,
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
            property_id = int(raw_id.strip("/"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_property_id", "Property id must be numeric") from exc
        if property_id < 1:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_property_id", "Property id must be positive")
        return property_id

    def _extract_conversation_id(self, path: str, suffix: str = "") -> int:
        marker = "/api/conversations/"
        if suffix and not path.endswith(suffix):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Conversation route not found")
        raw_id = path[len(marker) : len(path) - len(suffix) if suffix else None]
        try:
            conversation_id = int(raw_id.strip("/"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_conversation_id", "Conversation id must be numeric") from exc
        if conversation_id < 1:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_conversation_id", "Conversation id must be positive")
        return conversation_id

    def _extract_resource_id(self, path: str, prefix: str, *, resource: str) -> int:
        if not path.startswith(prefix):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", f"{resource} route not found")
        raw_id = path[len(prefix) :]
        try:
            resource_id = int(raw_id.strip("/"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, f"invalid_{resource.lower()}_id", f"{resource} id must be numeric") from exc
        if resource_id < 1:
            raise ApiError(HTTPStatus.BAD_REQUEST, f"invalid_{resource.lower()}_id", f"{resource} id must be positive")
        return resource_id


def create_server(config: AppConfig) -> LawimThreadingHTTPServer:
    repository = LawimRepository(config.db_path)
    repository.initialize(seed_demo_data=config.seed_demo_data)
    services = LawimServices(repository, config)

    class BoundHandler(LawimRequestHandler):
        pass

    BoundHandler.repository = repository
    BoundHandler.config = config
    BoundHandler.services = services

    server = LawimThreadingHTTPServer((config.host, config.port), BoundHandler)
    server.repository = repository  # type: ignore[attr-defined]
    server.config = config  # type: ignore[attr-defined]
    server.services = services  # type: ignore[attr-defined]
    return server


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the LAWIM_V2 executable baseline")
    parser.add_argument("--host", default=None, help="Host to bind")
    parser.add_argument("--port", type=int, default=None, help="Port to bind")
    parser.add_argument("--db", default=None, help="SQLite database path")
    parser.add_argument("--no-seed", action="store_true", help="Skip demo data seeding")
    args = parser.parse_args(argv)

    try:
        config = AppConfig.from_env()
    except ValueError as exc:
        parser.error(str(exc))

    overrides: dict[str, object] = {}
    if args.host is not None:
        overrides["host"] = args.host
    if args.port is not None:
        overrides["port"] = args.port
    if args.db is not None:
        overrides["db_path"] = Path(args.db).expanduser()
    if args.no_seed:
        overrides["seed_demo_data"] = False
    if overrides:
        config = replace(config, **overrides)

    logging.basicConfig(
        level=getattr(logging, config.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    try:
        config.ensure_runtime_dir()
        server = create_server(config)
    except (OSError, sqlite3.Error) as exc:
        parser.error(str(exc))
    bound_host, bound_port = server.server_address[:2]
    LOGGER.info("LAWIM_V2 listening on http://%s:%s", bound_host, bound_port)
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
