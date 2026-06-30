from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import sqlite3
from dataclasses import replace
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from importlib import resources
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .config import AppConfig
from .api_query import build_property_query
from .errors import RepositoryError, ValidationError
from .db import LawimRepository
from .dto import error_dto
from .matching import MatchCriteria, MatchWeights
from .media_domain import THUMBNAIL_CONTRACT
from .multipart import parse_multipart_form_data
from .observability import METRICS
from .persistence_adapter import resolve_persistence_adapter
from .rate_limit import AuthRateLimiter
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
    auth_limiter: AuthRateLimiter

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
        self._send_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        LOGGER.info("%s - %s", self.address_string(), format % args)

    def _handle_request(self, handler) -> None:
        try:
            handler()
        except ApiError as exc:
            METRICS.increment("api", failed=True)
            self._send_json_error(exc.status, exc.code, exc.message)
        except ServiceError as exc:
            METRICS.increment("api", failed=True)
            self._send_json_error(exc.status, exc.code, exc.message)
        except RepositoryError as exc:
            METRICS.increment("api", failed=True)
            self._send_json_error(exc.status, exc.code, str(exc))
        except Exception as exc:  # pragma: no cover - unexpected runtime failure
            METRICS.increment("api", failed=True)
            LOGGER.exception("Unhandled %s error: %s", self.command, exc)
            self._send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "Unexpected server error")
        else:
            METRICS.increment("api")

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
        if path.startswith("/media/"):
            self._send_media_asset(path)
            return
        if path == "/healthz":
            self._send_text("ok", content_type="text/plain; charset=utf-8")
            return
        if path == "/readyz":
            payload = self.services.readiness()
            status = HTTPStatus.OK if payload.get("status") == "ready" else HTTPStatus.SERVICE_UNAVAILABLE
            self._send_json(payload, status=status)
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
        if parsed.path == "/api/media/upload" and "multipart/form-data" in self.headers.get("Content-Type", "").lower():
            self._handle_multipart_media_upload(parsed)
            return
        body = self._read_json_body()
        self._handle_api_post(parsed, body)

    def _handle_api_get(self, parsed) -> None:
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/api/health":
            actor = self._require_user(optional=True)
            self._send_json(self.services.health(actor=actor))
            return

        if path == "/api/metrics":
            actor = self._require_user()
            self._send_json(self.services.metrics(actor=actor))
            return

        if path == "/api/bootstrap":
            token = self._bearer_token(optional=True)
            self._send_json(self.services.bootstrap(token=token))
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
            self._send_json({"organizations": self.services.list_organizations(limit=self._query_limit(query))})
            return

        if path == "/api/users":
            actor = self._require_user()
            self._send_json({"users": self.services.list_users(actor=actor, limit=self._query_limit(query))})
            return

        if path == "/api/properties":
            try:
                listing = build_property_query(
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                    sort=self._first(query, "sort"),
                    order=self._first(query, "order"),
                    city=self._first(query, "city"),
                    country=self._first(query, "country"),
                    region=self._first(query, "region"),
                    status=self._first(query, "status"),
                    availability=self._first(query, "availability"),
                    property_type=self._first(query, "property_type"),
                    owner_organization_id=self._first_int(query, "owner_organization_id", minimum=1),
                    include_deleted=self._first_bool(query, "include_deleted"),
                    search=self._first(query, "search"),
                    price_min=self._first_int(query, "price_min", minimum=0),
                    price_max=self._first_int(query, "price_max", minimum=0),
                )
            except ValidationError as exc:
                raise ApiError(HTTPStatus.BAD_REQUEST, "validation_error", str(exc)) from exc
            if listing.include_deleted:
                actor = self._require_user()
                if not self.services.policy.is_admin(actor):
                    raise ApiError(HTTPStatus.FORBIDDEN, "forbidden", "include_deleted requires administrator access")
            self._send_json(
                self.services.list_properties(
                    city=listing.city,
                    country=listing.country,
                    region=listing.region,
                    status=listing.status,
                    availability=listing.availability,
                    property_type=listing.property_type,
                    owner_organization_id=listing.owner_organization_id,
                    include_deleted=listing.include_deleted,
                    search=listing.search,
                    price_min=listing.price_min,
                    price_max=listing.price_max,
                    page=listing.page,
                    limit=listing.limit,
                    sort=listing.sort,
                    order=listing.order,
                )
            )
            return

        if path == "/api/geo/normalize":
            geocode = self._first_bool(query, "geocode")
            self._send_json(
                self.services.normalize_location(
                    city=self._require_query(query, "city"),
                    country=self._require_query(query, "country"),
                    region=self._first(query, "region"),
                    address_line=self._first(query, "address_line"),
                    postal_code=self._first(query, "postal_code"),
                    geocode=geocode,
                )
            )
            return

        if path == "/api/geo/geocode":
            self._send_json(
                self.services.geocode_location(
                    city=self._require_query(query, "city"),
                    country=self._require_query(query, "country"),
                    region=self._first(query, "region"),
                    address_line=self._first(query, "address_line"),
                    postal_code=self._first(query, "postal_code"),
                )
            )
            return

        if path == "/api/geo/search":
            self._send_json(
                {
                    "locations": self.services.search_locations(
                        query=self._first(query, "q"),
                        limit=self._query_limit(query),
                    )
                }
            )
            return

        if path == "/api/geo/contracts":
            self._send_json({"thumbnail": THUMBNAIL_CONTRACT})
            return

        if path.startswith("/api/properties/") and path.endswith("/media"):
            property_id = self._extract_property_id(path, suffix="/media")
            self._send_json(
                self.services.list_media(
                    property_id=property_id,
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                    sort=self._first(query, "sort") or "position",
                    order=self._first(query, "order") or "asc",
                )
            )
            return

        if path.startswith("/api/properties/") and path.endswith("/publish"):
            raise ApiError(HTTPStatus.METHOD_NOT_ALLOWED, "method_not_allowed", "Use POST to publish a property")

        if path.startswith("/api/properties/"):
            property_id = self._extract_property_id(path)
            self._send_json({"property": self.services.get_property(property_id)})
            return

        if path == "/api/conversations":
            actor = self._require_user()
            self._send_json(
                self.services.list_conversations(
                    actor=actor,
                    user_id=self._first_int(query, "user_id", minimum=1),
                    organization_id=self._first_int(query, "organization_id", minimum=1),
                    property_id=self._first_int(query, "property_id", minimum=1),
                    status=self._first(query, "status"),
                    limit=self._query_limit(query),
                )
            )
            return

        if path == "/api/notifications":
            actor = self._require_user()
            self._send_json(
                self.services.list_notifications(
                    actor=actor,
                    unread_only=self._first_bool(query, "unread_only"),
                    kind=self._first(query, "kind"),
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                )
            )
            return

        if path.startswith("/api/conversations/") and path.endswith("/messages"):
            actor = self._require_user()
            conversation_id = self._extract_conversation_id(path, suffix="/messages")
            payload = self.services.get_conversation(actor=actor, conversation_id=conversation_id)
            self._send_json({"messages": payload.get("messages", [])})
            return

        if path.startswith("/api/conversations/"):
            actor = self._require_user()
            conversation_id = self._extract_conversation_id(path)
            self._send_json({"conversation": self.services.get_conversation(actor=actor, conversation_id=conversation_id)})
            return

        if path == "/api/matches":
            criteria = self._build_match_criteria(query)
            actor = self._require_user(optional=True)
            self._send_json(self.services.list_matches(criteria, actor=actor))
            return

        if path == "/api/media":
            property_id = self._first_int(query, "property_id", minimum=1)
            self._send_json(
                self.services.list_media(
                    property_id=property_id,
                    kind=self._first(query, "kind"),
                    include_deleted=self._first_bool(query, "include_deleted"),
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                    sort=self._first(query, "sort") or "created_at",
                    order=self._first(query, "order") or "desc",
                )
            )
            return

        if path.startswith("/api/media/"):
            media_id = self._extract_path_id(path, marker="/api/media/", resource="Media")
            self._send_json({"media": self.services.get_media(media_id)})
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _handle_api_post(self, parsed, body: dict[str, Any]) -> None:
        path = parsed.path

        if path == "/api/auth/login":
            self._enforce_auth_rate_limit(path)
            email = self._require_text(body, "email")
            password = self._require_text(body, "password")
            payload = self.services.login(email=email, password=password)
            self._send_json(payload, status=HTTPStatus.CREATED)
            return

        if path == "/api/auth/register":
            self._enforce_auth_rate_limit(path)
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
                address_line=self._optional_text(body.get("address_line")),
                region=self._optional_text(body.get("region")),
                postal_code=self._optional_text(body.get("postal_code")),
                latitude=self._optional_float(body.get("latitude")),
                longitude=self._optional_float(body.get("longitude")),
                price_min=self._optional_int(body.get("price_min"), minimum=0),
                price_max=self._optional_int(body.get("price_max"), minimum=0),
                currency=self._optional_text(body.get("currency")) or "XAF",
                status=self._coerce_status(body.get("status"), default="draft"),
                availability=self._coerce_availability(body.get("availability")),
                property_type=self._optional_text(body.get("property_type")) or "apartment",
                owner_organization_id=self._optional_int(body.get("owner_organization_id"), minimum=1),
                bedrooms=self._optional_int(body.get("bedrooms"), minimum=0) or 0,
                bathrooms=self._optional_int(body.get("bathrooms"), minimum=0) or 0,
                area_sqm=self._optional_float(body.get("area_sqm")) or 0.0,
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
                listing_code=self._optional_text(body.get("listing_code")),
            )
            self._send_json({"property": property_row}, status=HTTPStatus.CREATED)
            return

        if path == "/api/media/upload":
            media_row = self.services.upload_media(
                actor=actor,
                property_id=self._require_int(body, "property_id", minimum=1),
                filename=self._require_text(body, "filename"),
                content_base64=self._require_text(body, "content_base64"),
                kind=self._optional_text(body.get("kind")) or "image",
                caption=self._optional_text(body.get("caption")) or "LAWIM_V2 media",
                mime_type=self._optional_text(body.get("mime_type")),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
            )
            self._send_json({"media": media_row}, status=HTTPStatus.CREATED)
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
                organization_id=self._optional_int(body.get("organization_id"), minimum=1),
                subject=self._require_text(body, "subject"),
                status=self._coerce_status(body.get("status"), default="open"),
                negotiation_stage=self._optional_text(body.get("negotiation_stage")) or "inquiry",
                initial_message=self._optional_text(body.get("initial_message")),
                sender_user_id=self._optional_int(body.get("sender_user_id"), minimum=1) or int(actor["id"]),
            )
            self._send_json({"conversation": conversation}, status=HTTPStatus.CREATED)
            return

        if path == "/api/notifications/read-all":
            result = self.services.mark_all_notifications_read(actor=actor)
            self._send_json(result)
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

        if path.startswith("/api/properties/") and path.endswith("/publish"):
            property_id = self._extract_property_id(path, suffix="/publish")
            property_row = self.services.publish_property(
                actor=actor,
                property_id=property_id,
                version=self._optional_int(body.get("version"), minimum=1),
            )
            self._send_json({"property": property_row})
            return

        if path == "/api/geo/geocode":
            self._send_json(
                self.services.geocode_location(
                    city=self._require_text(body, "city"),
                    country=self._require_text(body, "country"),
                    region=self._optional_text(body.get("region")),
                    address_line=self._optional_text(body.get("address_line")),
                    postal_code=self._optional_text(body.get("postal_code")),
                )
            )
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
            organization_id = self._extract_path_id(path, marker="/api/organizations/", resource="Organization")
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
            user_id = self._extract_path_id(path, marker="/api/users/", resource="User")
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
                address_line=self._optional_text(body.get("address_line")),
                region=self._optional_text(body.get("region")),
                postal_code=self._optional_text(body.get("postal_code")),
                latitude=self._optional_float(body.get("latitude")),
                longitude=self._optional_float(body.get("longitude")),
                price_min=self._optional_int(body.get("price_min"), minimum=0),
                price_max=self._optional_int(body.get("price_max"), minimum=0),
                currency=self._optional_text(body.get("currency")),
                status=self._optional_text(body.get("status")),
                availability=self._optional_text(body.get("availability")),
                property_type=self._optional_text(body.get("property_type")),
                owner_organization_id=self._optional_int(body.get("owner_organization_id"), minimum=1),
                bedrooms=self._optional_int(body.get("bedrooms"), minimum=0),
                bathrooms=self._optional_int(body.get("bathrooms"), minimum=0),
                area_sqm=self._optional_float(body.get("area_sqm")),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
                version=self._optional_int(body.get("version"), minimum=1),
            )
            self._send_json({"property": property_row})
            return

        if path.startswith("/api/media/") and path.count("/") == 3:
            media_id = self._extract_path_id(path, marker="/api/media/", resource="Media")
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
                thumbnail_url=self._optional_text(body.get("thumbnail_url")),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
                position=self._optional_int(body.get("position"), minimum=0),
                version=self._optional_int(body.get("version"), minimum=1),
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
                negotiation_stage=self._optional_text(body.get("negotiation_stage")),
            )
            self._send_json({"conversation": conversation})
            return

        if path.startswith("/api/notifications/") and path.endswith("/read"):
            notification_id = self._extract_notification_id(path)
            payload = self.services.mark_notification_read(actor=actor, notification_id=notification_id)
            self._send_json(payload)
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _require_user(self, *, optional: bool = False) -> dict[str, object] | None:
        token = self._bearer_token(optional=optional)
        if not token:
            if optional:
                return None
            raise ApiError(HTTPStatus.UNAUTHORIZED, "unauthorized", "Valid session required")
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
        if length > self.config.max_json_body_bytes:
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

    def _read_raw_body(self, *, max_bytes: int) -> bytes:
        content_length = self.headers.get("Content-Length", "0")
        try:
            length = int(content_length)
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_content_length", "Content-Length must be an integer") from exc
        if length < 0:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_content_length", "Content-Length must be non-negative")
        if length <= 0:
            return b""
        if length > max_bytes:
            raise ApiError(HTTPStatus.REQUEST_ENTITY_TOO_LARGE, "payload_too_large", "Request body exceeds the supported size")
        return self.rfile.read(length)

    def _handle_multipart_media_upload(self, parsed) -> None:
        actor = self._require_user()
        raw = self._read_raw_body(max_bytes=self.config.max_upload_bytes)
        parts = parse_multipart_form_data(
            self.headers.get("Content-Type", ""),
            raw,
            max_bytes=self.config.max_upload_bytes,
        )
        file_part = parts.get("file")
        if file_part is None or not file_part.data:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Multipart field 'file' is required")
        property_part = parts.get("property_id")
        if property_part is None or not property_part.data:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Multipart field 'property_id' is required")
        try:
            property_id = int(property_part.data.decode("utf-8").strip())
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "property_id must be an integer") from exc
        filename = file_part.filename or "upload.bin"
        caption_part = parts.get("caption")
        kind_part = parts.get("kind")
        caption = caption_part.data.decode("utf-8").strip() if caption_part and caption_part.data else "LAWIM_V2 media"
        kind = kind_part.data.decode("utf-8").strip() if kind_part and kind_part.data else "image"
        media_row = self.services.upload_media_bytes(
            actor=actor,
            property_id=property_id,
            filename=filename,
            content=file_part.data,
            kind=kind,
            caption=caption,
            mime_type=file_part.content_type,
        )
        self._send_json({"media": media_row}, status=HTTPStatus.CREATED)

    def _request_origin(self) -> str | None:
        raw = self.headers.get("Origin")
        if not raw:
            return None
        stripped = raw.strip()
        return stripped or None

    def _allowed_cors_origin(self) -> str | None:
        origin = self._request_origin()
        allowed = self.config.cors_allowed_origins
        if origin and origin in allowed:
            return origin
        if origin is None and len(allowed) == 1:
            return allowed[0]
        return None

    def _send_cors_headers(self) -> None:
        origin = self._allowed_cors_origin()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")

    def _enforce_auth_rate_limit(self, path: str) -> None:
        client_host = self.client_address[0] if self.client_address else "unknown"
        key = f"{client_host}:{path}"
        if not self.auth_limiter.is_allowed(key):
            raise ApiError(
                HTTPStatus.TOO_MANY_REQUESTS,
                "rate_limited",
                "Too many authentication attempts; try again later",
            )

    def _send_security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")

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
        self._send_cors_headers()
        if status == HTTPStatus.UNAUTHORIZED:
            self.send_header("WWW-Authenticate", 'Bearer realm="LAWIM_V2"')
        if extra_headers:
            for header, value in extra_headers.items():
                self.send_header(header, value)
        self._send_security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_json_error(self, status: HTTPStatus, code: str, message: str) -> None:
        self._send_json(error_dto(code, message), status=status)

    def _send_text(self, text: str, *, content_type: str) -> None:
        body = text.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; base-uri 'self'; form-action 'self'",
        )
        self._send_security_headers()
        self.end_headers()
        self.wfile.write(body)

    def _send_static(self, name: str, content_type: str) -> None:
        try:
            content = resources.files("lawim_v2.static").joinpath(name).read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ApiError(HTTPStatus.NOT_FOUND, "asset_not_found", f"Static asset not found: {name}") from exc
        self._send_text(content, content_type=content_type)

    def _send_media_asset(self, path: str) -> None:
        if not self.config.public_media:
            self._require_user()
        relative = path[len("/media/") :].lstrip("/")
        if not relative or ".." in relative.split("/"):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_media_path", "Invalid media path")
        target = self.config.media_storage_path / relative
        if not target.is_file():
            raise ApiError(HTTPStatus.NOT_FOUND, "asset_not_found", "Media asset not found")
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        body = target.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self._send_cors_headers()
        self._send_security_headers()
        self.end_headers()
        self.wfile.write(body)

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

    def _coerce_availability(self, value: object | None, default: str = "available") -> str:
        if value is None:
            return default
        if not isinstance(value, str):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'availability' must be a string")
        normalized = value.strip().lower()
        if normalized not in {"available", "reserved", "sold", "rented", "unavailable"}:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'availability' is invalid")
        return normalized

    def _first_bool(self, query: dict[str, list[str]], key: str) -> bool:
        value = self._first(query, key)
        if value is None:
            return False
        return value.strip().lower() in {"1", "true", "yes", "on"}

    def _require_query(self, query: dict[str, list[str]], key: str) -> str:
        value = self._first(query, key)
        if not value:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", f"Query '{key}' is required")
        return value

    def _query_page(self, query: dict[str, list[str]]) -> int:
        value = self._first_int(query, "page", minimum=1)
        return value or 1

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
        query_min_score = self._first_float(query, "min_score")
        min_score = query_min_score if query_min_score is not None else self.config.match_min_score
        if min_score < 0:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", "Query 'min_score' must be non-negative")
        weights = MatchWeights(
            status=self._first_float(query, "weight_status") or MatchWeights().status,
            city=self._first_float(query, "weight_city") or MatchWeights().city,
            region=self._first_float(query, "weight_region") or MatchWeights().region,
            budget=self._first_float(query, "weight_budget") or MatchWeights().budget,
            proximity=self._first_float(query, "weight_proximity") or MatchWeights().proximity,
            attributes=self._first_float(query, "weight_attributes") or MatchWeights().attributes,
            availability=self._first_float(query, "weight_availability") or MatchWeights().availability,
        )
        return MatchCriteria(
            city=self._first(query, "city"),
            region=self._first(query, "region"),
            country=self._first(query, "country"),
            budget_min=budget_min,
            budget_max=budget_max,
            latitude=self._optional_float(self._first(query, "latitude")),
            longitude=self._optional_float(self._first(query, "longitude")),
            property_type=self._first(query, "property_type"),
            bedrooms_min=self._first_int(query, "bedrooms_min", minimum=0),
            availability=self._first(query, "availability"),
            status=self._first(query, "status") or "published",
            limit=self._query_limit(query),
            min_score=min_score,
            weights=weights.normalized(),
        )

    def _first_float(self, query: dict[str, list[str]], key: str) -> float | None:
        raw = self._first(query, key)
        if raw is None:
            return None
        return self._optional_float(raw)

    def _extract_path_id(self, path: str, *, marker: str, suffix: str = "", resource: str) -> int:
        if not path.startswith(marker):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", f"{resource} route not found")
        if suffix and not path.endswith(suffix):
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", f"{resource} route not found")
        end = len(path) - len(suffix) if suffix else None
        raw_id = path[len(marker) : end]
        id_key = f"invalid_{resource.lower()}_id"
        try:
            resource_id = int(raw_id.strip("/"))
        except ValueError as exc:
            raise ApiError(HTTPStatus.BAD_REQUEST, id_key, f"{resource} id must be numeric") from exc
        if resource_id < 1:
            raise ApiError(HTTPStatus.BAD_REQUEST, id_key, f"{resource} id must be positive")
        return resource_id

    def _extract_notification_id(self, path: str) -> int:
        return self._extract_path_id(path, marker="/api/notifications/", suffix="/read", resource="Notification")

    def _extract_property_id(self, path: str, suffix: str = "") -> int:
        return self._extract_path_id(path, marker="/api/properties/", suffix=suffix, resource="Property")

    def _extract_conversation_id(self, path: str, suffix: str = "") -> int:
        return self._extract_path_id(path, marker="/api/conversations/", suffix=suffix, resource="Conversation")


def create_server(config: AppConfig) -> LawimThreadingHTTPServer:
    config.validate()
    adapter = resolve_persistence_adapter(
        config.db_path,
        db_driver=config.db_driver,
        database_url=config.database_url,
        allow_sqlite_fallback=config.db_fallback,
    )
    repository = adapter.create_repository()
    repository.initialize(seed_demo_data=config.seed_demo_data)
    services = LawimServices(repository, config)

    class BoundHandler(LawimRequestHandler):
        pass

    BoundHandler.repository = repository
    BoundHandler.config = config
    BoundHandler.services = services
    BoundHandler.auth_limiter = AuthRateLimiter(
        max_attempts=config.auth_rate_limit_max,
        window_seconds=config.auth_rate_limit_window_seconds,
    )

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
        config.validate()
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
