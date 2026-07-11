from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import re
import sqlite3
import time
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
from .bootstrap import build_runtime
from .ecosystem.engines import normalize_partner_type
from .dto import error_dto
from .matching import MatchCriteria, MatchWeights
from .media_domain import THUMBNAIL_CONTRACT
from .multipart import parse_multipart_form_data
from .observability import METRICS
from .rate_limit import AuthRateLimiter
from .services import LawimServices, ServiceError
from .user_roles import USER_ROLE_VALUES
from .project_service import ProjectPermissionDenied


LOGGER = logging.getLogger("lawim_v2")
MAX_JSON_BODY_BYTES = 1_048_576
_STATIC_TEXT_CACHE: dict[str, str] = {}


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
        LOGGER.info(
            json.dumps(
                {
                    "event": "http_request",
                    "client": self.address_string(),
                    "request": format % args,
                    "method": self.command,
                    "path": self.path,
                },
                ensure_ascii=False,
                separators=(",", ":"),
            )
        )

    def _handle_request(self, handler) -> None:
        route = urlparse(self.path).path
        started = time.perf_counter()
        failed = False
        try:
            handler()
        except ApiError as exc:
            failed = True
            self._send_json_error(exc.status, exc.code, exc.message)
        except ServiceError as exc:
            failed = True
            self._send_json_error(exc.status, exc.code, exc.message)
        except ProjectPermissionDenied as exc:
            failed = True
            self._send_json_error(exc.status, exc.code, exc.message)
        except RepositoryError as exc:
            failed = True
            self._send_json_error(getattr(exc, "status", HTTPStatus.INTERNAL_SERVER_ERROR), getattr(exc, "code", "repository_error"), str(exc))
        except Exception as exc:  # pragma: no cover - unexpected runtime failure
            failed = True
            LOGGER.exception("Unhandled %s error: %s", self.command, exc)
            self._send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, "internal_error", "Unexpected server error")
        finally:
            duration_ms = (time.perf_counter() - started) * 1000.0
            METRICS.record_request(route=route, duration_ms=duration_ms, failed=failed)
            if self.config.metrics_enabled:
                LOGGER.debug(
                    json.dumps(
                        {
                            "event": "request_complete",
                            "route": route,
                            "method": self.command,
                            "duration_ms": round(duration_ms, 2),
                            "failed": failed,
                        },
                        separators=(",", ":"),
                    )
                )

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
        if path in {"/logo.svg", "/favicon.svg", "/robots.txt"}:
            content_type = "image/svg+xml" if path.endswith(".svg") else "text/plain; charset=utf-8"
            self._send_static(path.lstrip("/"), content_type)
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
            self._send_json(
                {
                    "events": self.services.events(
                        actor=actor,
                        limit=self._query_limit(query),
                        kind=self._first(query, "kind"),
                    )
                }
            )
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

        if path.startswith("/api/v2/operations"):
            self._send_json({"data": self.services.operations.list(limit=self._query_limit(query))})
            return

        if path.startswith("/api/v2/deployment"):
            self._send_json({"data": self.services.deployment.list(limit=self._query_limit(query))})
            return

        if path.startswith("/api/v2/backup"):
            self._send_json({"data": self.services.backup.list(limit=self._query_limit(query))})
            return

        if path.startswith("/api/v2/installer"):
            self._send_json({"data": self.services.installer.list(limit=self._query_limit(query))})
            return

        if path.startswith("/api/v2/releases"):
            self._send_json({"data": self.services.release_manager.list(limit=self._query_limit(query))})
            return

        if path.startswith("/api/v2/releases"):
            self._send_json({"data": self.services.release_manager.list(limit=self._query_limit(query))})
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

        if path.startswith("/api/v2/assistant"):
            if "/brain/" in path:
                self._handle_v2_brain_get(path, query)
                return
            self._handle_v2_assistant_get(path, query)
            return

        if path.startswith("/api/v2/knowledge/"):
            self._handle_v2_knowledge_subroutes_get(path, query)
            return

        if path == "/api/v2/knowledge":
            actor = self._require_user()
            self._send_json(
                {
                    "knowledge": self.services.intelligent.search_knowledge_global(
                        actor=actor,
                        category=self._first(query, "category"),
                        limit=self._query_limit(query),
                    )
                }
            )
            return

        if (
            path in {
                "/api/v2/decisions",
                "/api/v2/simulations",
                "/api/v2/reasoning",
                "/api/v2/intelligence",
                "/api/v2/next-actions",
                "/api/v2/opportunities",
                "/api/v2/risks",
            }
            or path.startswith("/api/v2/decisions/")
        ):
            self._handle_v2_cognition_get(path, query)
            return

        if path.startswith("/api/v2/analytics"):
            self._handle_v2_analytics_get(path, query)
            return

        if path.startswith("/api/v2/source-intelligence") or path.startswith("/api/v2/sie"):
            self._handle_v2_source_intelligence_get(path, query)
            return

        if path.startswith("/api/v2/communication"):
            self._handle_v2_communication_get(path, query)
            return

        if path.startswith("/api/v2/security"):
            self._handle_v2_security_get(path, query)
            return

        if path.startswith("/api/v2/marketplace"):
            self._handle_v2_marketplace_get(path, query)
            return

        if path.startswith("/api/v2/crm"):
            self._handle_v2_crm_get(path, query)
            return

        if path.startswith("/api/v2/properties"):
            self._handle_v2_rei_get(path, query)
            return

        if path.startswith("/api/v2/workflows/"):
            self._handle_v2_workflow_automation_get(path, query)
            return

        if (
            path.startswith("/api/v2/partners")
            or path.startswith("/api/v2/services")
            or path == "/api/v2/workflows"
            or path.startswith("/api/v2/matching")
            or path.startswith("/api/v2/reputation")
            or path.startswith("/api/v2/notifications/ecosystem")
            or path.startswith("/api/v2/resources")
            or (
                path.startswith("/api/v2/projects/")
                and ("/orchestration" in path or "/matching" in path or "/workflows" in path)
            )
        ):
            self._handle_v2_ecosystem_get(path, query)
            return

        if path.startswith("/api/v2/projects/"):
            self._handle_v2_project_get(path, query)
            return

        if path == "/api/v2/projects":
            actor = self._require_user()
            self._send_json(
                self.services.projects.list_projects(
                    actor=actor,
                    user_id=self._first_int(query, "user_id", minimum=1),
                    organization_id=self._first_int(query, "organization_id", minimum=1),
                    status=self._first(query, "status"),
                    project_type=self._first(query, "project_type"),
                    priority=self._first(query, "priority"),
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                    sort=self._first(query, "sort") or "created_at",
                    order=self._first(query, "order") or "desc",
                )
            )
            return

        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _handle_api_post(self, parsed, body: dict[str, Any]) -> None:
        path = parsed.path

        if path == "/api/auth/login":
            self._enforce_auth_rate_limit(path)
            identifier = self._optional_text(body.get("identifier")) or self._optional_text(body.get("email"))
            if identifier is None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'identifier' is required")
            password = self._require_text(body, "password")
            payload = self.services.login(identifier=identifier, password=password)
            self._send_json(payload, status=HTTPStatus.CREATED)
            return

        if path == "/api/auth/register":
            self._enforce_auth_rate_limit(path)
            email = self._require_text(body, "email")
            password = self._require_text(body, "password")
            password_confirmation = self._require_text(body, "password_confirmation")
            full_name = self._require_text(body, "full_name")
            username = self._require_text(body, "username")
            phone_e164 = (
                self._optional_text(body.get("phone_e164"))
                or self._optional_text(body.get("whatsapp_number"))
                or self._optional_text(body.get("phone"))
                or self._optional_text(body.get("whatsapp"))
            )
            if phone_e164 is None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'phone_e164' is required")
            preferred_language = self._optional_text(body.get("preferred_language")) or "fr"
            accept_terms = self._coerce_bool(body.get("accept_terms"))
            if password != password_confirmation:
                raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Passwords do not match")
            payload = self.services.register(
                actor=None,
                email=email,
                password=password,
                full_name=full_name,
                username=username,
                phone_e164=phone_e164,
                preferred_language=preferred_language,
                accept_terms=accept_terms,
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
                username=self._optional_text(body.get("username")),
                phone_e164=self._optional_text(body.get("phone_e164")) or self._optional_text(body.get("whatsapp_number")),
                preferred_language=self._optional_text(body.get("preferred_language")),
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

        if path.startswith("/api/v2/assistant"):
            if "/brain/" in path:
                self._handle_v2_brain_post(path, body, actor)
                return
            self._handle_v2_assistant_post(path, body, actor)
            return

        if path.startswith("/api/v2/knowledge/"):
            self._handle_v2_knowledge_subroutes_post(path, body, actor)
            return

        if path.startswith("/api/v2/analytics"):
            self._handle_v2_analytics_post(path, body, actor)
            return

        if path.startswith("/api/v2/source-intelligence") or path.startswith("/api/v2/sie"):
            self._handle_v2_source_intelligence_post(path, body, actor)
            return

        if path.startswith("/api/v2/communication"):
            self._handle_v2_communication_post(path, body, actor)
            return

        if path.startswith("/api/v2/security"):
            self._handle_v2_security_post(path, body, actor)
            return

        if path.startswith("/api/v2/marketplace"):
            self._handle_v2_marketplace_post(path, body, actor)
            return

        if path.startswith("/api/v2/crm"):
            self._handle_v2_crm_post(path, body, actor)
            return

        if path.startswith("/api/v2/properties"):
            self._handle_v2_rei_post(path, body, actor)
            return

        if path.startswith("/api/v2/workflows/"):
            self._handle_v2_workflow_automation_post(path, body, actor)
            return

        if path in {"/api/v2/simulations"}:
            self._handle_v2_cognition_post(path, body, actor)
            return

        if path.startswith("/api/v2/partners") or path == "/api/v2/matching" or (path.startswith("/api/v2/projects/") and path.endswith("/matching/run")):
            self._handle_v2_ecosystem_post(path, body, actor)
            return

        if path.startswith("/api/v2/projects/"):
            self._handle_v2_project_post(path, body, actor)
            return

        if path == "/api/v2/projects":
            project = self.services.projects.create_project(
                actor=actor,
                title=self._require_text(body, "title"),
                project_type=self._require_text(body, "project_type"),
                objective=self._require_text(body, "objective"),
                budget_min=self._optional_int(body.get("budget_min"), minimum=0),
                budget_max=self._optional_int(body.get("budget_max"), minimum=0),
                currency=self._optional_text(body.get("currency")) or "XAF",
                location_city=self._optional_text(body.get("location_city")),
                location_region=self._optional_text(body.get("location_region")),
                location_country=self._optional_text(body.get("location_country")) or "Cameroon",
                location_latitude=self._optional_float(body.get("location_latitude")),
                location_longitude=self._optional_float(body.get("location_longitude")),
                timeline_horizon=self._optional_text(body.get("timeline_horizon")),
                status=self._optional_text(body.get("status")) or "draft",
                priority=self._optional_text(body.get("priority")) or "normal",
                organization_id=self._optional_int(body.get("organization_id"), minimum=1),
                metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
            )
            self._send_json({"project": project}, status=HTTPStatus.CREATED)
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

        if path.startswith("/api/v2/projects/"):
            self._handle_v2_project_mutation(path, method, body, actor)
            return

        if path.startswith("/api/v2/source-intelligence") or path.startswith("/api/v2/sie"):
            self._handle_v2_source_intelligence_mutation(path, method, body, actor)
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
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
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
            content = _STATIC_TEXT_CACHE.get(name)
            if content is None:
                content = resources.files("lawim_v2.static").joinpath(name).read_text(encoding="utf-8")
                _STATIC_TEXT_CACHE[name] = content
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

    def _coerce_bool(self, value: object | None) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"true", "1", "yes", "on"}:
                return True
            if normalized in {"false", "0", "no", "off", ""}:
                return False
        if value is None:
            return False
        raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field must be a boolean")

    def _coerce_role(self, value: object | None) -> str:
        if value is None:
            return "operator"
        if not isinstance(value, str):
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Field 'role' must be a string")
        normalized = value.strip().lower()
        if normalized not in USER_ROLE_VALUES:
            raise ApiError(
                HTTPStatus.BAD_REQUEST,
                "invalid_payload",
                "Field 'role' must be one of admin, manager, operator, partner, user or their supported aliases",
            )
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
        budget = self._first_int(query, "budget", minimum=0)
        if budget_max is None and budget is not None:
            budget_max = budget
        if budget_min is None and budget is not None and budget_max is not None:
            budget_min = 0
        if budget_min is not None and budget_max is not None and budget_min > budget_max:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", "Query 'budget_min' cannot exceed 'budget_max'")
        query_min_score = self._first_float(query, "min_score")
        min_score = query_min_score if query_min_score is not None else self.config.match_min_score
        if min_score < 0:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", "Query 'min_score' must be non-negative")
        city = self._first(query, "city")
        region = self._first(query, "region")
        country = self._first(query, "country")
        property_type = self._first(query, "property_type")
        availability = self._first(query, "availability")
        status = self._first(query, "status")
        target_type = self._first(query, "target_type") or self._first(query, "match_type") or self._first(query, "target")
        need = self._first(query, "need")
        need_type = self._first(query, "need_type")
        partner_type = self._first(query, "partner_type")
        project_type = self._first(query, "project_type")
        specialty = self._first(query, "specialty")
        language = self._first(query, "language")
        subject_type = self._first(query, "subject_type")
        rating_min = self._first_float(query, "rating_min")
        deadline_days = self._first_int(query, "deadline_days", minimum=0)
        if target_type is None:
            if any(value for value in (need, need_type, partner_type, project_type, specialty, language, rating_min, deadline_days)):
                target_type = "partner"
            else:
                target_type = "property"
        target_type = str(target_type).strip().lower()
        if target_type not in {"property", "partner"}:
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_query", "Query 'target_type' must be 'property' or 'partner'")
        if target_type == "partner":
            inferred_partner_type = self._infer_partner_type(partner_type, need, need_type, specialty, project_type)
            partner_type = inferred_partner_type or partner_type
            if status is None:
                status = "active"
        elif status is None:
            status = "published"
        default_weights = MatchWeights()
        weights = MatchWeights(
            status=self._first_float(query, "weight_status") or default_weights.status,
            city=self._first_float(query, "weight_city") or default_weights.city,
            region=self._first_float(query, "weight_region") or default_weights.region,
            budget=self._first_float(query, "weight_budget") or default_weights.budget,
            proximity=self._first_float(query, "weight_proximity") or default_weights.proximity,
            attributes=self._first_float(query, "weight_attributes") or default_weights.attributes,
            availability=self._first_float(query, "weight_availability") or default_weights.availability,
        )
        return MatchCriteria(
            target_type=target_type,
            city=city.lower() if city else None,
            region=region.lower() if region else None,
            country=country.lower() if country else None,
            budget_min=budget_min,
            budget_max=budget_max,
            latitude=self._optional_float(self._first(query, "latitude")),
            longitude=self._optional_float(self._first(query, "longitude")),
            property_type=property_type.lower() if property_type else None,
            bedrooms_min=self._first_int(query, "bedrooms_min", minimum=0),
            availability=availability.lower() if availability else None,
            need=need.lower() if need else None,
            need_type=need_type.lower() if need_type else None,
            partner_type=partner_type.lower() if partner_type else None,
            project_type=project_type.lower() if project_type else None,
            specialty=specialty.lower() if specialty else None,
            language=language.lower() if language else None,
            rating_min=rating_min,
            deadline_days=deadline_days,
            subject_type=subject_type.lower() if subject_type else None,
            status=(status.lower() if status else ("active" if target_type == "partner" else "published")),
            limit=self._query_limit(query),
            min_score=min_score,
            weights=weights.normalized(),
        )

    def _infer_partner_type(self, *values: str | None) -> str | None:
        for value in values:
            raw = str(value or "").strip().lower()
            if not raw:
                continue
            try:
                return normalize_partner_type(raw)
            except ValueError:
                pass
            for token in re.split(r"[^a-z0-9_]+", raw):
                if not token:
                    continue
                try:
                    return normalize_partner_type(token)
                except ValueError:
                    continue
        return None

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

    def _extract_project_id(self, path: str, suffix: str = "") -> int:
        return self._extract_path_id(path, marker="/api/v2/projects/", suffix=suffix, resource="Project")

    def _cognition_project_id(self, query: dict[str, list[str]], body: dict[str, Any] | None = None) -> int:
        if body is not None and body.get("project_id") is not None:
            project_id = self._optional_int(body.get("project_id"), minimum=1)
            if project_id is not None:
                return project_id
        return self._first_int(query, "project_id", minimum=1)

    def _handle_v2_knowledge_subroutes_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path in {"/api/v2/knowledge/graph", "/api/v2/knowledge/context"}:
            self._handle_v2_cognition_get(path, query)
            return
        actor = self._require_user()
        kp = self.services.knowledge_platform
        if path == "/api/v2/knowledge/search":
            self._send_json(
                kp.search(
                    actor=actor,
                    query=self._first(query, "q") or self._first(query, "query") or "",
                    domain=self._first(query, "domain"),
                    category=self._first(query, "category"),
                    tag=self._first(query, "tag"),
                    author=self._first(query, "author"),
                    project_id=self._optional_int(self._first(query, "project_id"), minimum=1),
                    partner_id=self._optional_int(self._first(query, "partner_id"), minimum=1),
                    service_id=self._optional_int(self._first(query, "service_id"), minimum=1),
                    limit=self._query_limit(query),
                )
            )
            return
        if path == "/api/v2/knowledge/articles":
            self._send_json(kp.list_articles(actor=actor, status=self._first(query, "status")))
            return
        if path.startswith("/api/v2/knowledge/articles/"):
            article_id = self._extract_path_id(path, marker="/api/v2/knowledge/articles/", resource="Article")
            self._send_json(kp.get_article(actor=actor, article_id=article_id))
            return
        if path == "/api/v2/knowledge/documents":
            self._send_json(kp.list_documents(actor=actor, status=self._first(query, "status")))
            return
        if path.startswith("/api/v2/knowledge/documents/"):
            document_id = self._extract_path_id(path, marker="/api/v2/knowledge/documents/", resource="Document")
            self._send_json(kp.get_document(actor=actor, document_id=document_id))
            return
        if path == "/api/v2/knowledge/categories":
            self._send_json(kp.list_categories(actor=actor, domain=self._first(query, "domain")))
            return
        if path == "/api/v2/knowledge/tags":
            self._send_json(kp.list_tags(actor=actor, domain=self._first(query, "domain")))
            return
        if path == "/api/v2/knowledge/sources":
            self._send_json(kp.list_sources(actor=actor))
            return
        if path == "/api/v2/knowledge/rag":
            self._send_json(
                kp.rag(
                    actor=actor,
                    query=self._first(query, "q") or self._first(query, "query") or "",
                    domain=self._first(query, "domain"),
                    category=self._first(query, "category"),
                    tag=self._first(query, "tag"),
                    limit=self._query_limit(query),
                )
            )
            return
        if path == "/api/v2/knowledge/citations":
            document_id = self._optional_int(self._first(query, "document_id"), minimum=1)
            self._send_json(kp.list_citations(actor=actor, document_id=document_id))
            return
        if path == "/api/v2/knowledge/references":
            document_id = self._optional_int(self._first(query, "document_id"), minimum=1)
            self._send_json(kp.list_references(actor=actor, document_id=document_id))
            return
        if path == "/api/v2/knowledge/stats":
            self._send_json(kp.stats(actor=actor))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown knowledge API route")

    def _extract_crm_id(self, path: str, *, resource: str, suffix: str = "") -> int:
        marker = f"/api/v2/crm/{resource}/"
        return self._extract_path_id(path, marker=marker, suffix=suffix, resource=resource.capitalize())

    def _handle_v2_communication_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path == "/api/v2/communication/integrations":
            self._send_json(self.services.communication.integration_sources(actor=None))
            return
        if path == "/api/v2/communication/health":
            self._send_json(self.services.communication.health(actor=None))
            return
        actor = self._require_user()
        comm = self.services.communication
        if path == "/api/v2/communication/messages":
            self._send_json(
                comm.list_messages(
                    actor=actor,
                    channel_type=self._first(query, "channel_type"),
                    status=self._first(query, "status"),
                    limit=self._query_limit(query),
                )
            )
            return
        if path == "/api/v2/communication/channels":
            self._send_json(comm.list_channels(actor=actor))
            return
        if path == "/api/v2/communication/conversations":
            self._send_json(comm.list_conversations(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/communication/history":
            self._send_json(comm.list_history(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/communication/groups":
            self._send_json(comm.list_groups(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/communication/events":
            self._send_json(comm.list_events(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/communication/templates":
            self._send_json(comm.list_templates(actor=actor, channel_type=self._first(query, "channel_type")))
            return
        if path == "/api/v2/communication/preferences":
            self._send_json(comm.get_preferences(actor=actor, channel_type=self._first(query, "channel_type") or "email"))
            return
        if path == "/api/v2/communication/campaigns":
            self._send_json(comm.list_campaigns(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/communication/notifications":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(comm.list_notifications(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/communication/email":
            self._send_json(comm.list_email_messages(actor=actor))
            return
        if path == "/api/v2/communication/sms":
            self._send_json(comm.list_sms_messages(actor=actor))
            return
        if path == "/api/v2/communication/whatsapp":
            self._send_json(comm.list_whatsapp_messages(actor=actor))
            return
        if path == "/api/v2/communication/telegram":
            self._send_json(comm.list_telegram_messages(actor=actor))
            return
        if path == "/api/v2/communication/push":
            self._send_json(comm.list_push_notifications(actor=actor))
            return
        if path == "/api/v2/communication/inapp":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(comm.list_inapp(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/communication/queue":
            self._send_json(comm.list_queue_jobs(actor=actor, job_status=self._first(query, "status")))
            return
        if path == "/api/v2/communication/statistics":
            self._send_json(comm.stats(actor=actor))
            return
        if path == "/api/v2/communication/dashboard":
            self._send_json(comm.dashboard(actor=actor))
            return
        if path == "/api/v2/communication/analytics":
            self._send_json(comm.analytics(actor=actor))
            return
        if path == "/api/v2/communication/reports":
            self._send_json(comm.reports(actor=actor))
            return
        if path == "/api/v2/communication/search":
            q = self._first(query, "q") or self._first(query, "query") or ""
            self._send_json(comm.search(actor=actor, query=q, limit=self._query_limit(query)))
            return
        if path == "/api/v2/communication/export":
            self._send_json(comm.export_data(actor=actor))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown communication API route")

    def _handle_v2_communication_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        comm = self.services.communication
        if path == "/api/v2/communication/messages":
            self._send_json(comm.create_message(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/messages/send":
            self._send_json(comm.send_message(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/conversations":
            self._send_json(comm.create_conversation(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/templates":
            self._send_json(comm.create_template(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/preferences":
            self._send_json(comm.update_preferences(actor=actor, body=body))
            return
        if path == "/api/v2/communication/campaigns":
            self._send_json(comm.create_campaign(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/notifications":
            self._send_json(comm.create_notification(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/queue":
            self._send_json(comm.enqueue_job(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/events":
            self._send_json(comm.process_event(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/communication/import":
            self._send_json(comm.import_data(actor=actor, body=body))
            return
        if path == "/api/v2/communication/seed":
            self._send_json(comm.seed_catalog(actor=actor))
            return
        if path.startswith("/api/v2/communication/campaigns/") and path.endswith("/execute"):
            campaign_id = self._extract_path_id(path, marker="/api/v2/communication/campaigns/", suffix="/execute", resource="Campaign")
            self._send_json(comm.execute_campaign(actor=actor, campaign_id=campaign_id))
            return
        if path.startswith("/api/v2/communication/queue/") and path.endswith("/retry"):
            job_id = self._extract_path_id(path, marker="/api/v2/communication/queue/", suffix="/retry", resource="Job")
            self._send_json(comm.retry_queue_job(actor=actor, job_id=job_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown communication API route")

    def _handle_v2_analytics_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path in {"/api/v2/analytics/integrations", "/api/v2/analytics/health"}:
            analytics = self.services.analytics
            if path == "/api/v2/analytics/integrations":
                self._send_json(analytics.integration_sources(actor=None))
            else:
                self._send_json(analytics.health(actor=None))
            return
        actor = self._require_user()
        analytics = self.services.analytics
        if path == "/api/v2/analytics/events":
            self._send_json(analytics.list_events(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/metrics":
            self._send_json(analytics.list_metrics(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/kpis":
            self._send_json(analytics.kpi.compute())
            return
        if path == "/api/v2/analytics/dashboards":
            self._send_json(analytics.dashboards.list(limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/reports":
            self._send_json(analytics.reporting.list(limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/bi":
            self._send_json(analytics.bi.summary())
            return
        if path == "/api/v2/analytics/datamarts":
            self._send_json(analytics.datamarts.list(limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/trends":
            self._send_json(analytics.trends.analyze())
            return
        if path == "/api/v2/analytics/scores":
            self._send_json(analytics.scores.compute())
            return
        if path == "/api/v2/analytics/realtime":
            self._send_json(analytics.realtime.summary())
            return
        if path == "/api/v2/analytics/exports":
            self._send_json(analytics.exports.list(limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/ai":
            self._send_json(analytics.ai.list_insights(limit=self._query_limit(query)))
            return
        if path == "/api/v2/analytics/executive":
            self._send_json(analytics.executive.get())
            return
        if path == "/api/v2/analytics/dashboard":
            self._send_json(analytics.dashboard(actor=actor))
            return
        if path == "/api/v2/analytics/statistics":
            self._send_json(analytics.statistics(actor=actor))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown analytics API route")

    def _handle_v2_analytics_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        analytics = self.services.analytics
        if path == "/api/v2/analytics/events":
            self._send_json(analytics.record_event(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/analytics/metrics":
            self._send_json(analytics.create_metric(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/analytics/kpis":
            self._send_json(analytics.kpi.compute())
            return
        if path == "/api/v2/analytics/dashboards":
            self._send_json(analytics.dashboards.list())
            return
        if path == "/api/v2/analytics/reports":
            self._send_json(
                analytics.reporting.create(
                    name=str(body.get("name") or "Analytics Report"),
                    report_type=str(body.get("report_type") or "standard"),
                    config=dict(body.get("config") or {}),
                ),
                status=HTTPStatus.CREATED,
            )
            return
        if path == "/api/v2/analytics/bi":
            self._send_json(analytics.bi.summary())
            return
        if path == "/api/v2/analytics/datamarts":
            mart_id = int(body.get("mart_id") or 1)
            self._send_json(analytics.datamarts.refresh(mart_id))
            return
        if path == "/api/v2/analytics/trends":
            self._send_json(analytics.trends.analyze())
            return
        if path == "/api/v2/analytics/scores":
            self._send_json(analytics.scores.compute())
            return
        if path == "/api/v2/analytics/realtime":
            self._send_json(
                analytics.realtime.record_event(
                    event_type=str(body.get("event_type") or "generic"),
                    payload=dict(body.get("payload") or {}),
                )
            )
            return
        if path == "/api/v2/analytics/exports":
            self._send_json(
                analytics.exports.create(
                    name=str(body.get("name") or "Analytics Export"),
                    export_type=str(body.get("export_type") or "json"),
                    config=dict(body.get("config") or {}),
                    requested_by=int(actor["id"]) if actor.get("id") is not None else None,
                ),
                status=HTTPStatus.CREATED,
            )
            return
        if path == "/api/v2/analytics/ai":
            self._send_json(analytics.ai.generate())
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown analytics API route")

    def _handle_v2_source_intelligence_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        sie = self.services.source_intelligence
        if path in {"/api/v2/source-intelligence", "/api/v2/source-intelligence/dashboard", "/api/v2/sie", "/api/v2/sie/dashboard"}:
            self._send_json(sie.dashboard_view(actor=actor, limit=self._query_limit(query)))
            return
        if path in {"/api/v2/source-intelligence/stats", "/api/v2/sie/stats"}:
            self._send_json(sie.stats(actor=actor))
            return
        if path in {"/api/v2/source-intelligence/sources", "/api/v2/sie/sources"}:
            self._send_json(
                sie.list_sources(
                    actor=actor,
                    status=self._first(query, "status"),
                    query=self._first(query, "q"),
                    limit=self._query_limit(query),
                )
            )
            return
        if path in {"/api/v2/source-intelligence/imports", "/api/v2/sie/imports"}:
            self._send_json(
                {
                    "imports": self.repository.list_source_intelligence_imports(
                        limit=self._query_limit(query),
                        source_id=self._optional_int(self._first(query, "source_id"), minimum=1),
                    )
                }
            )
            return
        if path.startswith("/api/v2/source-intelligence/sources/") or path.startswith("/api/v2/sie/sources/"):
            marker = "/api/v2/sie/sources/" if path.startswith("/api/v2/sie/sources/") else "/api/v2/source-intelligence/sources/"
            if path.endswith("/context"):
                source_id = self._extract_path_id(path, marker=marker, suffix="/context", resource="Source")
                self._send_json(sie.get_context(actor=actor, source_id=source_id))
                return
            if path.endswith("/whatsapp-link"):
                source_id = self._extract_path_id(path, marker=marker, suffix="/whatsapp-link", resource="Source")
                self._send_json(sie.build_whatsapp_link(actor=actor, source_id=source_id))
                return
            source_id = self._extract_path_id(path, marker=marker, resource="Source")
            self._send_json(sie.get_source(actor=actor, source_id=source_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown source intelligence API route")

    def _handle_v2_source_intelligence_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        sie = self.services.source_intelligence
        if path in {"/api/v2/source-intelligence/reference-code", "/api/v2/sie/reference-code"}:
            self._send_json(sie.references.generate(seed=self._optional_text(body.get("seed"))))
            return
        if path in {"/api/v2/source-intelligence/sources", "/api/v2/sie/sources"}:
            self._send_json(sie.create_source(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path in {"/api/v2/source-intelligence/imports", "/api/v2/sie/imports"}:
            self._send_json(sie.import_source(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path in {"/api/v2/source-intelligence/analyze", "/api/v2/sie/analyze"}:
            self._send_json(sie.analyze_source(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path in {"/api/v2/source-intelligence/whatsapp-link", "/api/v2/sie/whatsapp-link"}:
            source_id = self._require_int(body, "source_id", minimum=1)
            self._send_json(sie.build_whatsapp_link(actor=actor, source_id=source_id), status=HTTPStatus.CREATED)
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown source intelligence API route")

    def _handle_v2_source_intelligence_mutation(self, path: str, method: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        sie = self.services.source_intelligence
        if path.startswith("/api/v2/source-intelligence/sources/") or path.startswith("/api/v2/sie/sources/"):
            marker = "/api/v2/sie/sources/" if path.startswith("/api/v2/sie/sources/") else "/api/v2/source-intelligence/sources/"
            if path.endswith("/context"):
                source_id = self._extract_path_id(path, marker=marker, suffix="/context", resource="Source")
                self._send_json(sie.update_context(actor=actor, source_id=source_id, body=body))
                return
            source_id = self._extract_path_id(path, marker=marker, resource="Source")
            if method == "DELETE":
                self._send_json(sie.archive_source(actor=actor, source_id=source_id))
                return
            self._send_json(sie.update_source(actor=actor, source_id=source_id, body=body))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown source intelligence API route")

    def _handle_v2_security_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path == "/api/v2/security/integrations":
            self._send_json(self.services.security.integration_sources(actor=None))
            return
        actor = self._require_user()
        sec = self.services.security
        if path == "/api/v2/security/users":
            self._send_json(sec.list_users(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/security/roles":
            self._send_json(sec.list_roles(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/security/permissions":
            self._send_json(sec.list_permissions(actor=actor))
            return
        if path == "/api/v2/security/policies":
            self._send_json(sec.list_policies(actor=actor))
            return
        if path == "/api/v2/security/sessions":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(sec.list_sessions(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/security/devices":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(sec.list_devices(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/security/api-keys":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(sec.list_api_keys(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/security/audit":
            self._send_json(sec.list_audit_trail(actor=actor, event_type=self._first(query, "event_type")))
            return
        if path == "/api/v2/security/compliance/policies":
            self._send_json(sec.list_compliance_policies(actor=actor))
            return
        if path == "/api/v2/security/compliance/consents":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(sec.list_compliance_consents(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/security/compliance/retention":
            self._send_json(sec.list_retention_rules(actor=actor))
            return
        if path == "/api/v2/security/privacy/exports":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(sec.list_privacy_exports(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/security/privacy/erasure":
            self._send_json(sec.list_privacy_erasure_requests(actor=actor))
            return
        if path == "/api/v2/security/risk/signals":
            user_id = self._optional_int(self._first(query, "user_id"), minimum=1)
            self._send_json(sec.list_risk_signals(actor=actor, user_id=user_id))
            return
        if path == "/api/v2/security/risk/alerts":
            self._send_json(sec.list_risk_alerts(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/security/incidents":
            self._send_json(sec.list_incidents(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/security/analytics":
            self._send_json(sec.analytics(actor=actor))
            return
        if path == "/api/v2/security/stats":
            self._send_json(sec.stats(actor=actor))
            return
        if path == "/api/v2/security/dashboard":
            self._send_json(sec.dashboard(actor=actor))
            return
        if path.startswith("/api/v2/security/users/") and path.count("/") == 5:
            user_id = self._extract_path_id(path, marker="/api/v2/security/users/", resource="User")
            self._send_json(sec.get_user(actor=actor, user_id=user_id))
            return
        if path.startswith("/api/v2/security/risk/scores/") and path.count("/") == 6:
            user_id = self._extract_path_id(path, marker="/api/v2/security/risk/scores/", resource="User")
            self._send_json(sec.compute_risk_score(actor=actor, user_id=user_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown security API route")

    def _handle_v2_security_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        sec = self.services.security
        if path == "/api/v2/security/roles":
            self._send_json(sec.create_role(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/permissions":
            self._send_json(sec.create_permission(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/policies":
            self._send_json(sec.create_policy(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/api-keys":
            self._send_json(sec.create_api_key(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/audit":
            self._send_json(sec.record_audit(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/compliance/deletion":
            self._send_json(sec.create_deletion_request(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/privacy/exports":
            self._send_json(sec.create_privacy_export(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/privacy/erasure":
            self._send_json(sec.create_privacy_erasure_request(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/risk/signals":
            self._send_json(sec.record_risk_signal(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/incidents":
            self._send_json(sec.create_incident(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/security/seed":
            self._send_json(sec.seed_catalog(actor=actor))
            return
        if path.startswith("/api/v2/security/users/") and path.endswith("/roles"):
            user_id = self._extract_path_id(path, marker="/api/v2/security/users/", suffix="/roles", resource="User")
            payload = dict(body)
            payload.setdefault("user_id", user_id)
            self._send_json(sec.assign_user_role(actor=actor, body=payload))
            return
        if path.startswith("/api/v2/security/sessions/") and path.endswith("/revoke"):
            session_record_id = self._extract_path_id(path, marker="/api/v2/security/sessions/", suffix="/revoke", resource="Session")
            self._send_json(sec.revoke_session(actor=actor, session_record_id=session_record_id))
            return
        if path.startswith("/api/v2/security/api-keys/") and path.endswith("/revoke"):
            api_key_id = self._extract_path_id(path, marker="/api/v2/security/api-keys/", suffix="/revoke", resource="ApiKey")
            self._send_json(sec.revoke_api_key(actor=actor, api_key_id=api_key_id))
            return
        if path.startswith("/api/v2/security/compliance/consents/") and path.endswith("/grant"):
            consent_id = self._extract_path_id(path, marker="/api/v2/security/compliance/consents/", suffix="/grant", resource="Consent")
            self._send_json(sec.grant_consent_by_id(actor=actor, consent_id=consent_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown security API route")

    def _handle_v2_marketplace_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path == "/api/v2/marketplace/integrations":
            self._send_json(self.services.marketplace.integration_sources(actor=None))
            return
        actor = self._require_user()
        mp = self.services.marketplace
        if path == "/api/v2/marketplace/partners":
            self._send_json(mp.list_partner_registrations(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/marketplace/providers":
            self._send_json(mp.list_providers(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/marketplace/catalog/categories":
            self._send_json(mp.list_catalog_categories(actor=actor))
            return
        if path == "/api/v2/marketplace/catalog":
            self._send_json(mp.list_catalog_items(actor=actor, category=self._first(query, "category")))
            return
        if path == "/api/v2/marketplace/requests":
            self._send_json(mp.list_requests(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/marketplace/quotes":
            request_id = self._optional_int(self._first(query, "request_id"), minimum=1)
            self._send_json(mp.list_quotes(actor=actor, request_id=request_id))
            return
        if path == "/api/v2/marketplace/contracts":
            self._send_json(mp.list_contracts(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/marketplace/missions":
            self._send_json(mp.list_missions(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/marketplace/reviews":
            provider_id = self._optional_int(self._first(query, "provider_id"), minimum=1)
            self._send_json(mp.list_reviews(actor=actor, provider_id=provider_id))
            return
        if path == "/api/v2/marketplace/commissions":
            contract_id = self._optional_int(self._first(query, "contract_id"), minimum=1)
            self._send_json(mp.list_commissions(actor=actor, contract_id=contract_id))
            return
        if path == "/api/v2/marketplace/subscriptions/plans":
            self._send_json(mp.list_subscription_plans(actor=actor))
            return
        if path == "/api/v2/marketplace/disputes":
            self._send_json(mp.list_disputes(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/marketplace/recommendations":
            request_id = self._optional_int(self._first(query, "request_id"), minimum=1)
            self._send_json(mp.list_recommendations(actor=actor, request_id=request_id))
            return
        if path == "/api/v2/marketplace/analytics":
            self._send_json(mp.analytics(actor=actor))
            return
        if path == "/api/v2/marketplace/stats":
            self._send_json(mp.stats(actor=actor))
            return
        if path == "/api/v2/marketplace/dashboard":
            self._send_json(mp.dashboard(actor=actor))
            return
        if path.startswith("/api/v2/marketplace/providers/") and path.endswith("/availability"):
            provider_id = self._extract_path_id(path, marker="/api/v2/marketplace/providers/", suffix="/availability", resource="Provider")
            self._send_json(mp.provider_availability(actor=actor, provider_id=provider_id))
            return
        if path.startswith("/api/v2/marketplace/providers/") and path.endswith("/portfolio"):
            provider_id = self._extract_path_id(path, marker="/api/v2/marketplace/providers/", suffix="/portfolio", resource="Provider")
            self._send_json(mp.provider_portfolio(actor=actor, provider_id=provider_id))
            return
        if path.startswith("/api/v2/marketplace/providers/") and path.endswith("/reputation"):
            provider_id = self._extract_path_id(path, marker="/api/v2/marketplace/providers/", suffix="/reputation", resource="Provider")
            self._send_json(mp.provider_reputation(actor=actor, provider_id=provider_id))
            return
        if path.startswith("/api/v2/marketplace/matching/"):
            session_id = self._extract_path_id(path, marker="/api/v2/marketplace/matching/", resource="Session")
            self._send_json(mp.get_matching_session(actor=actor, session_id=session_id))
            return
        if path.startswith("/api/v2/marketplace/catalog/") and path.count("/") == 5:
            item_id = self._extract_path_id(path, marker="/api/v2/marketplace/catalog/", resource="CatalogItem")
            self._send_json(mp.get_catalog_item(actor=actor, item_id=item_id))
            return
        if path.startswith("/api/v2/marketplace/requests/") and path.count("/") == 5:
            request_id = self._extract_path_id(path, marker="/api/v2/marketplace/requests/", resource="Request")
            self._send_json(mp.get_request(actor=actor, request_id=request_id))
            return
        if path.startswith("/api/v2/marketplace/missions/") and path.count("/") == 5:
            mission_id = self._extract_path_id(path, marker="/api/v2/marketplace/missions/", resource="Mission")
            self._send_json(mp.get_mission(actor=actor, mission_id=mission_id))
            return
        if path.startswith("/api/v2/marketplace/providers/") and path.count("/") == 5:
            provider_id = self._extract_path_id(path, marker="/api/v2/marketplace/providers/", resource="Provider")
            self._send_json(mp.get_provider(actor=actor, provider_id=provider_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown marketplace API route")

    def _handle_v2_marketplace_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        mp = self.services.marketplace
        if path == "/api/v2/marketplace/partners":
            self._send_json(mp.create_partner_registration(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/providers":
            self._send_json(mp.create_provider(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/catalog":
            self._send_json(mp.create_catalog_item(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/requests":
            self._send_json(mp.create_request(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/quotes":
            self._send_json(mp.create_quote(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/contracts":
            self._send_json(mp.create_contract(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/reviews":
            self._send_json(mp.create_review(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/disputes":
            self._send_json(mp.open_dispute(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/subscriptions":
            self._send_json(mp.subscribe(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/payments/prepare":
            self._send_json(mp.prepare_payment(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/marketplace/seed":
            self._send_json(mp.seed_catalog(actor=actor))
            return
        if path.startswith("/api/v2/marketplace/partners/") and path.endswith("/approve"):
            registration_id = self._extract_path_id(path, marker="/api/v2/marketplace/partners/", suffix="/approve", resource="Registration")
            self._send_json(mp.approve_partner_registration(actor=actor, registration_id=registration_id))
            return
        if path.startswith("/api/v2/marketplace/partners/") and path.endswith("/qualify"):
            registration_id = self._extract_path_id(path, marker="/api/v2/marketplace/partners/", suffix="/qualify", resource="Registration")
            self._send_json(mp.qualify_partner_registration(actor=actor, registration_id=registration_id))
            return
        if path.startswith("/api/v2/marketplace/providers/") and path.endswith("/availability"):
            provider_id = self._extract_path_id(path, marker="/api/v2/marketplace/providers/", suffix="/availability", resource="Provider")
            self._send_json(mp.set_provider_availability(actor=actor, provider_id=provider_id, body=body))
            return
        if path.startswith("/api/v2/marketplace/quotes/") and path.endswith("/send"):
            quote_id = self._extract_path_id(path, marker="/api/v2/marketplace/quotes/", suffix="/send", resource="Quote")
            self._send_json(mp.send_quote(actor=actor, quote_id=quote_id))
            return
        if path.startswith("/api/v2/marketplace/quotes/") and path.endswith("/accept"):
            quote_id = self._extract_path_id(path, marker="/api/v2/marketplace/quotes/", suffix="/accept", resource="Quote")
            self._send_json(mp.accept_quote(actor=actor, quote_id=quote_id))
            return
        if path.startswith("/api/v2/marketplace/contracts/") and path.endswith("/activate"):
            contract_id = self._extract_path_id(path, marker="/api/v2/marketplace/contracts/", suffix="/activate", resource="Contract")
            self._send_json(mp.activate_contract(actor=actor, contract_id=contract_id))
            return
        if path.startswith("/api/v2/marketplace/requests/") and path.endswith("/matching"):
            request_id = self._extract_path_id(path, marker="/api/v2/marketplace/requests/", suffix="/matching", resource="Request")
            self._send_json(mp.run_matching(actor=actor, request_id=request_id))
            return
        if path.startswith("/api/v2/marketplace/requests/") and path.endswith("/recommendations"):
            request_id = self._extract_path_id(path, marker="/api/v2/marketplace/requests/", suffix="/recommendations", resource="Request")
            self._send_json(mp.generate_recommendations(actor=actor, request_id=request_id))
            return
        if path.startswith("/api/v2/marketplace/disputes/") and path.endswith("/resolve"):
            dispute_id = self._extract_path_id(path, marker="/api/v2/marketplace/disputes/", suffix="/resolve", resource="Dispute")
            self._send_json(mp.resolve_dispute(actor=actor, dispute_id=dispute_id, body=body))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown marketplace API route")

    def _handle_v2_crm_get(self, path: str, query: dict[str, list[str]]) -> None:
        if path == "/api/v2/crm/official-contact":
            self._send_json(self.services.crm.official_contact(actor=None))
            return
        actor = self._require_user()
        crm = self.services.crm
        if path == "/api/v2/crm/contacts":
            self._send_json(crm.list_contacts(actor=actor, contact_type=self._first(query, "type"), limit=self._query_limit(query)))
            return
        if path == "/api/v2/crm/leads":
            self._send_json(crm.list_leads(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/crm/leads/sources":
            self._send_json(crm.list_lead_sources(actor=actor))
            return
        if path == "/api/v2/crm/customers":
            self._send_json(crm.list_customers(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/crm/opportunities":
            contact_id = self._optional_int(self._first(query, "contact_id"), minimum=1)
            self._send_json(crm.list_opportunities(actor=actor, contact_id=contact_id, status=self._first(query, "status")))
            return
        if path == "/api/v2/crm/pipelines":
            self._send_json(crm.list_pipelines(actor=actor))
            return
        if path.startswith("/api/v2/crm/pipelines/") and path.endswith("/board"):
            pipeline_id = self._extract_path_id(path, marker="/api/v2/crm/pipelines/", suffix="/board", resource="Pipeline")
            self._send_json(crm.pipeline_board(actor=actor, pipeline_id=pipeline_id))
            return
        if path == "/api/v2/crm/communications":
            contact_id = self._optional_int(self._first(query, "contact_id"), minimum=1)
            self._send_json(crm.list_communications(actor=actor, contact_id=contact_id, channel=self._first(query, "channel")))
            return
        if path == "/api/v2/crm/reminders":
            contact_id = self._optional_int(self._first(query, "contact_id"), minimum=1)
            self._send_json(crm.list_reminders(actor=actor, contact_id=contact_id))
            return
        if path == "/api/v2/crm/followups":
            contact_id = self._optional_int(self._first(query, "contact_id"), minimum=1)
            self._send_json(crm.list_followups(actor=actor, contact_id=contact_id, status=self._first(query, "status")))
            return
        if path == "/api/v2/crm/campaigns":
            self._send_json(crm.list_campaigns(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/crm/segments":
            self._send_json(crm.list_segments(actor=actor))
            return
        if path == "/api/v2/crm/satisfaction/surveys":
            self._send_json(crm.satisfaction_surveys(actor=actor))
            return
        if path.startswith("/api/v2/crm/satisfaction/") and path.endswith("/summary"):
            survey_id = self._extract_path_id(path, marker="/api/v2/crm/satisfaction/", suffix="/summary", resource="Survey")
            self._send_json(crm.satisfaction_summary(actor=actor, survey_id=survey_id))
            return
        if path == "/api/v2/crm/ai/suggestions":
            contact_id = self._optional_int(self._first(query, "contact_id"), minimum=1)
            self._send_json(crm.list_ai_suggestions(actor=actor, contact_id=contact_id))
            return
        if path == "/api/v2/crm/search":
            self._send_json(crm.search(actor=actor, query=self._first(query, "q") or "", limit=self._query_limit(query)))
            return
        if path == "/api/v2/crm/analytics":
            self._send_json(crm.analytics(actor=actor))
            return
        if path == "/api/v2/crm/stats":
            self._send_json(crm.stats(actor=actor))
            return
        if path == "/api/v2/crm/dashboard":
            self._send_json(crm.dashboard(actor=actor))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/360"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/360", resource="Contact")
            self._send_json(crm.customer_360(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/timeline"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/timeline", resource="Contact")
            self._send_json(crm.timeline(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/journey"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/journey", resource="Contact")
            self._send_json(crm.journey(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/notes"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/notes", resource="Contact")
            self._send_json(crm.list_notes(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/scores"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/scores", resource="Contact")
            self._send_json(crm.scores(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/leads/") and path.count("/") == 5:
            lead_id = self._extract_path_id(path, marker="/api/v2/crm/leads/", resource="Lead")
            self._send_json(crm.get_lead(actor=actor, lead_id=lead_id))
            return
        if path.startswith("/api/v2/crm/customers/") and path.count("/") == 5:
            customer_id = self._extract_path_id(path, marker="/api/v2/crm/customers/", resource="Customer")
            self._send_json(crm.get_customer(actor=actor, customer_id=customer_id))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.count("/") == 5:
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", resource="Contact")
            self._send_json(crm.get_contact(actor=actor, contact_id=contact_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown CRM API route")

    def _handle_v2_crm_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        crm = self.services.crm
        if path == "/api/v2/crm/contacts":
            self._send_json(crm.create_contact(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/leads":
            self._send_json(crm.create_lead(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/customers":
            self._send_json(crm.create_customer(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/opportunities":
            self._send_json(crm.create_opportunity(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/pipelines":
            self._send_json(crm.create_pipeline(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/whatsapp":
            self._send_json(crm.send_whatsapp(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/telegram":
            self._send_json(crm.send_telegram(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/email":
            self._send_json(crm.send_email(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/sms":
            self._send_json(crm.send_sms(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/reminders":
            self._send_json(crm.create_reminder(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/followups":
            self._send_json(crm.schedule_followup(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/campaigns":
            self._send_json(crm.create_campaign(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/segments":
            self._send_json(crm.create_segment(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/satisfaction/responses":
            self._send_json(crm.submit_satisfaction(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/notes":
            self._send_json(crm.add_note(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/crm/seed":
            self._send_json(crm.seed_catalog(actor=actor))
            return
        if path.startswith("/api/v2/crm/leads/") and path.endswith("/convert"):
            lead_id = self._extract_path_id(path, marker="/api/v2/crm/leads/", suffix="/convert", resource="Lead")
            self._send_json(crm.convert_lead(actor=actor, lead_id=lead_id, body=body))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/tags"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/tags", resource="Contact")
            self._send_json(crm.add_contact_tag(actor=actor, contact_id=contact_id, body=body), status=HTTPStatus.CREATED)
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/consents"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/consents", resource="Contact")
            self._send_json(crm.grant_consent(actor=actor, contact_id=contact_id, body=body), status=HTTPStatus.CREATED)
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/scores/compute"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/scores/compute", resource="Contact")
            self._send_json(crm.compute_scores(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/contacts/") and path.endswith("/ai/suggestions"):
            contact_id = self._extract_path_id(path, marker="/api/v2/crm/contacts/", suffix="/ai/suggestions", resource="Contact")
            self._send_json(crm.ai_suggestions(actor=actor, contact_id=contact_id))
            return
        if path.startswith("/api/v2/crm/campaigns/") and path.endswith("/launch"):
            campaign_id = self._extract_path_id(path, marker="/api/v2/crm/campaigns/", suffix="/launch", resource="Campaign")
            self._send_json(crm.launch_campaign(actor=actor, campaign_id=campaign_id))
            return
        if path.startswith("/api/v2/crm/followups/") and path.endswith("/complete"):
            followup_id = self._extract_path_id(path, marker="/api/v2/crm/followups/", suffix="/complete", resource="Followup")
            self._send_json(crm.complete_followup(actor=actor, followup_id=followup_id))
            return
        if path.startswith("/api/v2/crm/pipeline-items/") and path.endswith("/move"):
            item_id = self._extract_path_id(path, marker="/api/v2/crm/pipeline-items/", suffix="/move", resource="PipelineItem")
            self._send_json(crm.move_pipeline_item(actor=actor, item_id=item_id, body=body))
            return
        if path.startswith("/api/v2/crm/pipeline-items/") and path.endswith("/advance"):
            item_id = self._extract_path_id(path, marker="/api/v2/crm/pipeline-items/", suffix="/advance", resource="PipelineItem")
            self._send_json(crm.advance_pipeline_item(actor=actor, item_id=item_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown CRM API route")

    def _extract_rei_property_id(self, path: str, suffix: str = "") -> int:
        return self._extract_path_id(path, marker="/api/v2/properties/", suffix=suffix, resource="Property")

    def _handle_v2_rei_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        rei = self.services.real_estate
        if path == "/api/v2/properties":
            self._send_json(rei.list_properties(actor=actor, status=self._first(query, "status"), limit=self._query_limit(query)))
            return
        if path == "/api/v2/properties/listings":
            self._send_json(rei.list_listings(actor=actor, status=self._first(query, "status")))
            return
        if path == "/api/v2/properties/recommendations":
            self._send_json(rei.list_recommendations(actor=actor))
            return
        if path == "/api/v2/properties/visits":
            property_id = self._optional_int(self._first(query, "property_id"), minimum=1)
            self._send_json(rei.visits(actor=actor, property_id=property_id))
            return
        if path == "/api/v2/properties/negotiations":
            property_id = self._optional_int(self._first(query, "property_id"), minimum=1)
            self._send_json(rei.negotiations(actor=actor, property_id=property_id))
            return
        if path == "/api/v2/properties/transactions":
            property_id = self._optional_int(self._first(query, "property_id"), minimum=1)
            self._send_json(rei.transactions(actor=actor, property_id=property_id))
            return
        if path == "/api/v2/properties/search":
            query_text = self._first(query, "q") or self._first(query, "query") or ""
            self._send_json(rei.search(actor=actor, query=query_text, limit=self._query_limit(query)))
            return
        if path == "/api/v2/properties/map":
            self._send_json(rei.map_view(actor=actor, city=self._first(query, "city")))
            return
        if path == "/api/v2/properties/analytics":
            self._send_json(rei.analytics(actor=actor))
            return
        if path == "/api/v2/properties/stats":
            self._send_json(rei.stats(actor=actor))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/owners"):
            property_id = self._extract_rei_property_id(path, suffix="/owners")
            self._send_json(rei.owners(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/documents"):
            property_id = self._extract_rei_property_id(path, suffix="/documents")
            self._send_json(rei.documents(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/verification"):
            property_id = self._extract_rei_property_id(path, suffix="/verification")
            self._send_json(rei.get_verification(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/valuation"):
            property_id = self._extract_rei_property_id(path, suffix="/valuation")
            self._send_json(rei.valuation(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/history"):
            property_id = self._extract_rei_property_id(path, suffix="/history")
            self._send_json(rei.history(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/nearby"):
            property_id = self._extract_rei_property_id(path, suffix="/nearby")
            self._send_json(rei.nearby(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/media"):
            property_id = self._extract_rei_property_id(path, suffix="/media")
            self._send_json(rei.media(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/intelligence"):
            property_id = self._extract_rei_property_id(path, suffix="/intelligence")
            self._send_json(rei.intelligence(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/scores"):
            property_id = self._extract_rei_property_id(path, suffix="/scores")
            self._send_json(rei.scores(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/reports"):
            property_id = self._extract_rei_property_id(path, suffix="/reports")
            report_type = self._first(query, "type") or "summary"
            self._send_json(rei.report(actor=actor, property_id=property_id, report_type=report_type))
            return
        if path.startswith("/api/v2/properties/") and "/offers" in path:
            negotiation_id = self._extract_path_id(path, marker="/api/v2/properties/negotiations/", suffix="/offers", resource="Negotiation")
            self._send_json(rei.offers(actor=actor, negotiation_id=negotiation_id))
            return
        if path.startswith("/api/v2/properties/") and path.count("/") == 4:
            property_id = self._extract_rei_property_id(path)
            self._send_json(rei.get_property(actor=actor, property_id=property_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown real estate intelligence API route")

    def _handle_v2_rei_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        rei = self.services.real_estate
        if path == "/api/v2/properties/listings":
            self._send_json(rei.create_listing(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/properties/matching":
            self._send_json(rei.matching(actor=actor, body=body))
            return
        if path == "/api/v2/properties/recommendations":
            self._send_json(rei.recommendations(actor=actor, body=body))
            return
        if path == "/api/v2/properties/visits":
            self._send_json(rei.schedule_visit(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/properties/negotiations":
            self._send_json(rei.open_negotiation(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/properties/offers":
            self._send_json(rei.submit_offer(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/properties/transactions":
            self._send_json(rei.start_transaction(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/properties/reservations":
            self._send_json(rei.reserve(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/publish"):
            property_id = self._extract_rei_property_id(path, suffix="/publish")
            self._send_json(rei.publish(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/archive"):
            property_id = self._extract_rei_property_id(path, suffix="/archive")
            self._send_json(rei.archive(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/duplicate"):
            property_id = self._extract_rei_property_id(path, suffix="/duplicate")
            self._send_json(rei.duplicate_listing(actor=actor, property_id=property_id), status=HTTPStatus.CREATED)
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/owners"):
            property_id = self._extract_rei_property_id(path, suffix="/owners")
            self._send_json(rei.add_owner(actor=actor, property_id=property_id, body=body), status=HTTPStatus.CREATED)
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/documents"):
            property_id = self._extract_rei_property_id(path, suffix="/documents")
            self._send_json(rei.add_document(actor=actor, property_id=property_id, body=body), status=HTTPStatus.CREATED)
            return
        if path.startswith("/api/v2/properties/") and path.endswith("/verification"):
            property_id = self._extract_rei_property_id(path, suffix="/verification")
            self._send_json(rei.verification(actor=actor, property_id=property_id))
            return
        if path.startswith("/api/v2/properties/visits/") and path.endswith("/confirm"):
            visit_id = self._extract_path_id(path, marker="/api/v2/properties/visits/", suffix="/confirm", resource="Visit")
            self._send_json(rei.confirm_visit(actor=actor, visit_id=visit_id))
            return
        if path.startswith("/api/v2/properties/visits/") and path.endswith("/cancel"):
            visit_id = self._extract_path_id(path, marker="/api/v2/properties/visits/", suffix="/cancel", resource="Visit")
            self._send_json(rei.cancel_visit(actor=actor, visit_id=visit_id))
            return
        if path.startswith("/api/v2/properties/visits/") and path.endswith("/complete"):
            visit_id = self._extract_path_id(path, marker="/api/v2/properties/visits/", suffix="/complete", resource="Visit")
            self._send_json(rei.complete_visit(actor=actor, visit_id=visit_id, body=body))
            return
        if path.startswith("/api/v2/properties/transactions/") and path.endswith("/close"):
            transaction_id = self._extract_path_id(path, marker="/api/v2/properties/transactions/", suffix="/close", resource="Transaction")
            self._send_json(rei.close_transaction(actor=actor, transaction_id=transaction_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown real estate intelligence API route")

    def _handle_v2_workflow_automation_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        wa = self.services.workflow_automation
        if path == "/api/v2/workflows/definitions":
            self._send_json(wa.list_workflows(actor=actor, domain=self._first(query, "domain"), status=self._first(query, "status")))
            return
        if path.startswith("/api/v2/workflows/definitions/"):
            workflow_key = path.removeprefix("/api/v2/workflows/definitions/")
            self._send_json(wa.get_workflow(actor=actor, workflow_key=workflow_key))
            return
        if path == "/api/v2/workflows/templates":
            self._send_json(wa.list_templates(actor=actor, domain=self._first(query, "domain")))
            return
        if path == "/api/v2/workflows/executions":
            instance_id = self._optional_int(self._first(query, "instance_id"), minimum=1)
            self._send_json(wa.list_executions(actor=actor, instance_id=instance_id))
            return
        if path == "/api/v2/workflows/instances":
            project_id = self._optional_int(self._first(query, "project_id"), minimum=1)
            self._send_json(wa.list_instances(actor=actor, project_id=project_id, status=self._first(query, "status")))
            return
        if path == "/api/v2/workflows/tasks":
            instance_id = self._optional_int(self._first(query, "instance_id"), minimum=1)
            self._send_json(wa.list_tasks(actor=actor, instance_id=instance_id, status=self._first(query, "status")))
            return
        if path == "/api/v2/workflows/queues":
            self._send_json(wa.list_queues(actor=actor))
            return
        if path == "/api/v2/workflows/events":
            instance_id = self._optional_int(self._first(query, "instance_id"), minimum=1)
            self._send_json(wa.list_events(actor=actor, instance_id=instance_id))
            return
        if path == "/api/v2/workflows/approvals":
            instance_id = self._optional_int(self._first(query, "instance_id"), minimum=1)
            self._send_json(wa.list_approvals(actor=actor, instance_id=instance_id))
            return
        if path == "/api/v2/workflows/rules":
            self._send_json(wa.list_rules(actor=actor, domain=self._first(query, "domain")))
            return
        if path == "/api/v2/workflows/schedules":
            self._send_json(wa.list_schedules(actor=actor))
            return
        if path == "/api/v2/workflows/timers":
            instance_id = self._optional_int(self._first(query, "instance_id"), minimum=1)
            self._send_json(wa.list_timers(actor=actor, instance_id=instance_id))
            return
        if path == "/api/v2/workflows/notifications":
            instance_id = self._optional_int(self._first(query, "instance_id"), minimum=1)
            self._send_json(wa.list_notifications(actor=actor, instance_id=instance_id))
            return
        if path == "/api/v2/workflows/history":
            instance_id = self._first_int(query, "instance_id", minimum=1)
            self._send_json(wa.history(actor=actor, instance_id=instance_id))
            return
        if path == "/api/v2/workflows/audit":
            self._send_json(wa.audit(actor=actor))
            return
        if path == "/api/v2/workflows/metrics":
            self._send_json(wa.metrics(actor=actor))
            return
        if path == "/api/v2/workflows/monitoring":
            self._send_json(wa.monitoring(actor=actor))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown workflow automation API route")

    def _handle_v2_workflow_automation_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        wa = self.services.workflow_automation
        if path == "/api/v2/workflows/definitions":
            self._send_json(wa.create_workflow(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path.endswith("/duplicate") and path.startswith("/api/v2/workflows/definitions/"):
            workflow_key = path.removeprefix("/api/v2/workflows/definitions/").removesuffix("/duplicate")
            self._send_json(wa.duplicate_workflow(actor=actor, workflow_key=workflow_key), status=HTTPStatus.CREATED)
            return
        if path.endswith("/activate") and path.startswith("/api/v2/workflows/definitions/"):
            workflow_key = path.removeprefix("/api/v2/workflows/definitions/").removesuffix("/activate")
            self._send_json(wa.activate_workflow(actor=actor, workflow_key=workflow_key))
            return
        if path.endswith("/deactivate") and path.startswith("/api/v2/workflows/definitions/"):
            workflow_key = path.removeprefix("/api/v2/workflows/definitions/").removesuffix("/deactivate")
            self._send_json(wa.deactivate_workflow(actor=actor, workflow_key=workflow_key))
            return
        if path == "/api/v2/workflows/templates":
            self._send_json(wa.create_template(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/instances":
            self._send_json(wa.start_instance(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path.endswith("/advance") and path.startswith("/api/v2/workflows/instances/"):
            instance_id = self._extract_path_id(path, marker="/api/v2/workflows/instances/", suffix="/advance", resource="Instance")
            self._send_json(wa.advance_instance(actor=actor, instance_id=instance_id))
            return
        if path.endswith("/complete") and path.startswith("/api/v2/workflows/tasks/"):
            task_id = self._extract_path_id(path, marker="/api/v2/workflows/tasks/", suffix="/complete", resource="Task")
            self._send_json(wa.complete_task(actor=actor, task_id=task_id, body=body))
            return
        if path == "/api/v2/workflows/queues/enqueue":
            self._send_json(wa.enqueue(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/queues/dequeue":
            self._send_json(wa.dequeue(actor=actor, queue_key=self._require_text(body, "queue_key")))
            return
        if path == "/api/v2/workflows/events":
            self._send_json(wa.publish_event(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/approvals":
            self._send_json(wa.create_approval(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path.endswith("/decide") and path.startswith("/api/v2/workflows/approvals/"):
            approval_id = self._extract_path_id(path, marker="/api/v2/workflows/approvals/", suffix="/decide", resource="Approval")
            self._send_json(wa.decide_approval(actor=actor, approval_id=approval_id, body=body))
            return
        if path == "/api/v2/workflows/rules":
            self._send_json(wa.create_rule(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/rules/evaluate":
            self._send_json(wa.evaluate_rules(actor=actor, body=body))
            return
        if path == "/api/v2/workflows/timers":
            self._send_json(wa.create_timer(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/notifications":
            self._send_json(wa.send_notification(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/metrics/snapshot":
            self._send_json(wa.reindex_metrics(actor=actor))
            return
        if path.endswith("/retry") and path.startswith("/api/v2/workflows/executions/"):
            execution_id = self._extract_path_id(path, marker="/api/v2/workflows/executions/", suffix="/retry", resource="Execution")
            self._send_json(wa.retry_execution(actor=actor, execution_id=execution_id))
            return
        if path == "/api/v2/workflows/escalations":
            self._send_json(wa.escalate(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/workflows/ai-hook":
            self._send_json(wa.ai_hook(actor=actor, body=body))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown workflow automation API route")

    def _handle_v2_knowledge_subroutes_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        if path == "/api/v2/knowledge/refresh":
            self._handle_v2_cognition_post(path, body, actor)
            return
        kp = self.services.knowledge_platform
        if path == "/api/v2/knowledge/import":
            if isinstance(body.get("records"), list):
                self._send_json(kp.bulk_import(actor=actor, records=body["records"]), status=HTTPStatus.CREATED)
            else:
                self._send_json(kp.import_document(actor=actor, body=body), status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/knowledge/export":
            self._send_json(kp.export(actor=actor, format_name=self._optional_text(body.get("format")) or "json"))
            return
        if path == "/api/v2/knowledge/reindex":
            document_id = self._optional_int(body.get("document_id"), minimum=1)
            self._send_json(kp.reindex(actor=actor, document_id=document_id))
            return
        if path == "/api/v2/knowledge/rag":
            self._send_json(
                kp.rag(actor=actor, query=self._require_text(body, "query"), domain=self._optional_text(body.get("domain"))),
                status=HTTPStatus.CREATED,
            )
            return
        if path.endswith("/publish") and path.startswith("/api/v2/knowledge/documents/"):
            document_id = self._extract_path_id(path, marker="/api/v2/knowledge/documents/", suffix="/publish", resource="Document")
            self._send_json(kp.publish(actor=actor, document_id=document_id))
            return
        if path.endswith("/approve") and path.startswith("/api/v2/knowledge/documents/"):
            document_id = self._extract_path_id(path, marker="/api/v2/knowledge/documents/", suffix="/approve", resource="Document")
            self._send_json(kp.approve(actor=actor, document_id=document_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown knowledge API route")

    def _handle_v2_cognition_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        cog = self.services.cognition
        project_id = self._cognition_project_id(query)
        if path == "/api/v2/knowledge/graph":
            self._send_json(cog.get_graph(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/knowledge/context":
            self._send_json(cog.get_context(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/decisions":
            self._send_json(cog.list_decisions(actor=actor, project_id=project_id))
            return
        if path.startswith("/api/v2/decisions/"):
            decision_id = self._extract_path_id(path, marker="/api/v2/decisions/", resource="Decision")
            self._send_json(cog.get_decision(actor=actor, project_id=project_id, decision_id=decision_id))
            return
        if path == "/api/v2/reasoning":
            self._send_json(cog.list_reasoning(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/simulations":
            self._send_json(cog.list_simulations(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/intelligence":
            self._send_json(cog.get_intelligence(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/next-actions":
            self._send_json(cog.get_next_action(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/risks":
            self._send_json(cog.list_risks(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/opportunities":
            self._send_json(cog.list_opportunities(actor=actor, project_id=project_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown cognition API route")

    def _handle_v2_cognition_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        cog = self.services.cognition
        project_id = self._cognition_project_id({}, body)
        if path == "/api/v2/knowledge/refresh":
            self._send_json(cog.refresh(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/simulations":
            self._send_json(
                cog.run_simulation(
                    actor=actor,
                    project_id=project_id,
                    scenario_key=self._require_text(body, "scenario_key"),
                    parameters=body.get("parameters") if isinstance(body.get("parameters"), dict) else None,
                ),
                status=HTTPStatus.CREATED,
            )
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown cognition API route")

    def _handle_v2_brain_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        brain = self.services.brain
        if path == "/api/v2/assistant/brain/dossiers":
            self._send_json(
                brain.list_dossiers(
                    actor=actor,
                    status=self._first(query, "status"),
                    limit=self._query_limit(query),
                )
            )
            return
        if path.startswith("/api/v2/assistant/brain/dossiers/") and path.endswith("/resume"):
            project_id = self._extract_path_id(
                path, marker="/api/v2/assistant/brain/dossiers/", suffix="/resume", resource="Project"
            )
            lang = self._first(query, "language") or "fr"
            self._send_json(brain.get_resumption(actor=actor, project_id=project_id, language=lang))
            return
        if path.startswith("/api/v2/assistant/brain/dossiers/") and path.endswith("/memory"):
            project_id = self._extract_path_id(
                path, marker="/api/v2/assistant/brain/dossiers/", suffix="/memory", resource="Project"
            )
            self._send_json(brain.get_memory_summary(actor=actor, project_id=project_id))
            return
        if path.startswith("/api/v2/assistant/brain/dossiers/") and path.endswith("/suggestions"):
            project_id = self._extract_path_id(
                path, marker="/api/v2/assistant/brain/dossiers/", suffix="/suggestions", resource="Project"
            )
            self._send_json(
                brain.get_suggestions(
                    actor=actor,
                    project_id=project_id,
                    status=self._first(query, "status") or "active",
                )
            )
            return
        if path.startswith("/api/v2/assistant/brain/dossiers/") and path.endswith("/matches"):
            project_id = self._extract_path_id(
                path, marker="/api/v2/assistant/brain/dossiers/", suffix="/matches", resource="Project"
            )
            status = self._first(query, "status")
            self._send_json(brain.get_proposals(actor=actor, project_id=project_id, status=status))
            return
        if path.startswith("/api/v2/assistant/brain/dossiers/") and path.endswith("/relations"):
            project_id = self._extract_path_id(
                path, marker="/api/v2/assistant/brain/dossiers/", suffix="/relations", resource="Project"
            )
            self._send_json({"relations": brain.list_established_relations(actor=actor, project_id=project_id)})
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown brain API route")

    def _handle_v2_brain_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        brain = self.services.brain
        if path == "/api/v2/assistant/brain/matching":
            project_id = self._require_int(body, "project_id", minimum=1)
            partner_type = self._optional_text(body.get("partner_type"))
            result = brain.find_matches(
                actor=actor,
                project_id=project_id,
                partner_type=partner_type,
            )
            self._send_json(result, status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/assistant/brain/proposals/accept":
            proposal_id = self._require_int(body, "proposal_id", minimum=1)
            self._send_json(brain.accept_proposal(actor=actor, proposal_id=proposal_id))
            return
        if path == "/api/v2/assistant/brain/proposals/reject":
            proposal_id = self._require_int(body, "proposal_id", minimum=1)
            self._send_json(brain.reject_proposal(actor=actor, proposal_id=proposal_id))
            return
        if path == "/api/v2/assistant/brain/consent/request":
            proposal_id = self._require_int(body, "proposal_id", minimum=1)
            self._send_json(brain.request_consent(actor=actor, proposal_id=proposal_id))
            return
        if path == "/api/v2/assistant/brain/consent/grant":
            proposal_id = self._require_int(body, "proposal_id", minimum=1)
            self._send_json(brain.grant_consent(actor=actor, proposal_id=proposal_id))
            return
        if path == "/api/v2/assistant/brain/chat":
            project_id = self._assistant_project_id({}, body)
            session_id = self._optional_int(body.get("session_id"), minimum=1)
            message = self._require_text(body, "message")
            language = self._optional_text(body.get("language")) or "fr"
            channel = self._optional_text(body.get("channel")) or "web"
            processing = brain.process_chat(
                actor=actor,
                project_id=project_id,
                message=message,
                session_id=session_id,
                language=language,
                channel=channel,
            )
            self._send_json({"brain": processing}, status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/assistant/brain/dossiers":
            # Create a new project/dossier from the conversation
            title = self._require_text(body, "title")
            project_type = self._require_text(body, "project_type")
            objective = self._require_text(body, "objective")
            project = self.services.projects.create_project(
                actor=actor,
                title=title,
                project_type=project_type,
                objective=objective,
                budget_min=self._optional_int(body.get("budget_min"), minimum=0),
                budget_max=self._optional_int(body.get("budget_max"), minimum=0),
                currency=self._optional_text(body.get("currency")) or "XAF",
                location_city=self._optional_text(body.get("location_city")),
                location_region=self._optional_text(body.get("location_region")),
                location_country=self._optional_text(body.get("location_country")) or "Cameroon",
                timeline_horizon=self._optional_text(body.get("timeline_horizon")),
                status=self._optional_text(body.get("status")) or "draft",
                priority=self._optional_text(body.get("priority")) or "normal",
            )
            self._send_json({"project": project}, status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/assistant/brain/confirm":
            project_id = self._assistant_project_id({}, body)
            message = self._require_text(body, "message")
            language = self._optional_text(body.get("language")) or "fr"
            result = brain.handle_confirmation(
                actor=actor,
                project_id=project_id,
                message=message,
                language=language,
            )
            self._send_json({"confirmation": result})
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown brain API route")

    def _assistant_project_id(self, query: dict[str, list[str]], body: dict[str, Any] | None = None) -> int:
        if body is not None and body.get("project_id") is not None:
            project_id = self._optional_int(body.get("project_id"), minimum=1)
            if project_id is not None:
                return project_id
        return self._first_int(query, "project_id", minimum=1)

    def _handle_v2_assistant_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        assistant = self.services.assistant
        if path == "/api/v2/assistant/agents":
            self._send_json(assistant.list_agents(actor=actor))
            return
        if path == "/api/v2/assistant/prompts":
            self._send_json(assistant.list_prompts(actor=actor))
            return
        project_id = self._assistant_project_id(query)
        if path == "/api/v2/assistant/sessions":
            self._send_json(assistant.list_sessions(actor=actor, project_id=project_id))
            return
        if path.startswith("/api/v2/assistant/sessions/"):
            session_id = self._extract_path_id(path, marker="/api/v2/assistant/sessions/", resource="AssistantSession")
            self._send_json(assistant.get_session(actor=actor, project_id=project_id, session_id=session_id))
            return
        if path == "/api/v2/assistant/messages":
            session_id = self._first_int(query, "session_id", minimum=1)
            self._send_json(assistant.list_messages(actor=actor, project_id=project_id, session_id=session_id))
            return
        if path == "/api/v2/assistant/context":
            session_id = self._optional_int(self._first(query, "session_id"), minimum=1)
            self._send_json(assistant.get_context(actor=actor, project_id=project_id, session_id=session_id))
            return
        if path == "/api/v2/assistant/rag":
            query_text = self._first(query, "query") or ""
            self._send_json(assistant.retrieve_rag(actor=actor, project_id=project_id, query=query_text))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown assistant API route")

    def _handle_v2_assistant_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        assistant = self.services.assistant
        project_id = self._assistant_project_id({}, body)
        if path == "/api/v2/assistant/sessions":
            self._send_json(
                assistant.create_session(
                    actor=actor,
                    project_id=project_id,
                    agent_key=self._optional_text(body.get("agent_key")) or "project_advisor",
                ),
                status=HTTPStatus.CREATED,
            )
            return
        if path == "/api/v2/assistant/rag/refresh":
            self._send_json(assistant.refresh_rag(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/assistant/chat" or path == "/api/v2/assistant":
            self._send_json(
                assistant.chat(
                    actor=actor,
                    project_id=project_id,
                    message=self._require_text(body, "message"),
                    session_id=self._optional_int(body.get("session_id"), minimum=1),
                    agent_key=self._optional_text(body.get("agent_key")),
                ),
                status=HTTPStatus.CREATED,
            )
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown assistant API route")

    def _handle_v2_project_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        intel = self.services.intelligent
        if path.endswith("/workspace"):
            project_id = self._extract_project_id(path, suffix="/workspace")
            self._send_json({"workspace": intel.get_workspace(actor=actor, project_id=project_id)})
            return
        if path.endswith("/journey/state"):
            project_id = self._extract_project_id(path, suffix="/journey/state")
            self._send_json({"journey_state": intel.journey_state(actor=actor, project_id=project_id)})
            return
        if path.endswith("/goals"):
            project_id = self._extract_project_id(path, suffix="/goals")
            self._send_json({"goals": intel.list_goals(actor=actor, project_id=project_id)})
            return
        if path.endswith("/knowledge"):
            project_id = self._extract_project_id(path, suffix="/knowledge")
            self._send_json(
                {"knowledge": intel.list_knowledge(actor=actor, project_id=project_id, category=self._first(query, "category"))}
            )
            return
        if path.endswith("/recommendations"):
            project_id = self._extract_project_id(path, suffix="/recommendations")
            self._send_json({"recommendations": intel.list_recommendations(actor=actor, project_id=project_id)})
            return
        if path.endswith("/decisions"):
            project_id = self._extract_project_id(path, suffix="/decisions")
            self._send_json({"decisions": intel.list_decisions(actor=actor, project_id=project_id)})
            return
        if path.endswith("/actions"):
            project_id = self._extract_project_id(path, suffix="/actions")
            self._send_json({"actions": intel.list_actions(actor=actor, project_id=project_id)})
            return
        if path.endswith("/tasks"):
            project_id = self._extract_project_id(path, suffix="/tasks")
            self._send_json({"tasks": intel.list_tasks(actor=actor, project_id=project_id)})
            return
        if path.endswith("/life-events"):
            project_id = self._extract_project_id(path, suffix="/life-events")
            self._send_json({"life_events": intel.list_life_events(actor=actor, project_id=project_id)})
            return
        if path.endswith("/timeline"):
            project_id = self._extract_project_id(path, suffix="/timeline")
            self._send_json({"timeline": intel.get_timeline(actor=actor, project_id=project_id)})
            return
        if path.endswith("/resources"):
            project_id = self._extract_project_id(path, suffix="/resources")
            self._send_json({"resources": intel.list_resources(actor=actor, project_id=project_id)})
            return
        if path.endswith("/steps"):
            project_id = self._extract_project_id(path, suffix="/steps")
            self._send_json({"steps": self.services.projects.list_project_steps(actor=actor, project_id=project_id)})
            return
        if path.endswith("/progress"):
            project_id = self._extract_project_id(path, suffix="/progress")
            self._send_json(
                {"progress": self.services.projects.get_project_progress(actor=actor, project_id=project_id)}
            )
            return
        if path.endswith("/next-actions"):
            project_id = self._extract_project_id(path, suffix="/next-actions")
            self._send_json(
                {"next_actions": self.services.projects.get_project_next_actions(actor=actor, project_id=project_id)}
            )
            return
        project_id = self._extract_project_id(path)
        detail = self.services.projects.get_project_detail(actor=actor, project_id=project_id)
        self._send_json(detail)

    def _handle_v2_project_mutation(
        self,
        path: str,
        method: str,
        body: dict[str, Any],
        actor: dict[str, object],
    ) -> None:
        if method == "DELETE":
            project_id = self._extract_project_id(path)
            project = self.services.projects.archive_project(actor=actor, project_id=project_id)
            self._send_json({"project": project})
            return
        if method not in {"PATCH", "PUT"}:
            raise ApiError(HTTPStatus.METHOD_NOT_ALLOWED, "method_not_allowed", f"{method} not supported for projects")
        if "/steps/" in path:
            parts = path.rstrip("/").split("/")
            step_id = int(parts[-1])
            project_id = self._extract_project_id(path, suffix=f"/steps/{step_id}")
            step = self.services.projects.update_project_step(
                actor=actor,
                project_id=project_id,
                step_id=step_id,
                status=self._optional_text(body.get("status")),
                note=self._optional_text(body.get("note")),
            )
            self._send_json({"step": step})
            return
        project_id = self._extract_project_id(path)
        if self._optional_text(body.get("status")) == "archived" and len(body) == 1:
            project = self.services.projects.archive_project(actor=actor, project_id=project_id)
            self._send_json({"project": project})
            return
        project = self.services.projects.update_project(
            actor=actor,
            project_id=project_id,
            title=self._optional_text(body.get("title")),
            objective=self._optional_text(body.get("objective")),
            project_type=self._optional_text(body.get("project_type")),
            budget_min=self._optional_int(body.get("budget_min"), minimum=0),
            budget_max=self._optional_int(body.get("budget_max"), minimum=0),
            currency=self._optional_text(body.get("currency")),
            location_city=self._optional_text(body.get("location_city")),
            location_region=self._optional_text(body.get("location_region")),
            location_country=self._optional_text(body.get("location_country")),
            location_latitude=self._optional_float(body.get("location_latitude")),
            location_longitude=self._optional_float(body.get("location_longitude")),
            timeline_horizon=self._optional_text(body.get("timeline_horizon")),
            status=self._optional_text(body.get("status")),
            priority=self._optional_text(body.get("priority")),
            organization_id=self._optional_int(body.get("organization_id"), minimum=1),
            metadata=body.get("metadata") if isinstance(body.get("metadata"), dict) else None,
        )
        self._send_json({"project": project})

    def _handle_v2_project_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        intel = self.services.intelligent
        if path.endswith("/intelligence/refresh"):
            project_id = self._extract_project_id(path, suffix="/intelligence/refresh")
            self._send_json({"intelligence": intel.refresh_intelligence(actor=actor, project_id=project_id)})
            return
        if path.endswith("/journey/replan"):
            project_id = self._extract_project_id(path, suffix="/journey/replan")
            self._send_json({"replan": intel.replan_journey(actor=actor, project_id=project_id)})
            return
        if path.endswith("/goals"):
            project_id = self._extract_project_id(path, suffix="/goals")
            goal = intel.create_goal(
                actor=actor,
                project_id=project_id,
                goal_key=self._require_text(body, "goal_key"),
                title=self._require_text(body, "title"),
                priority=self._optional_text(body.get("priority")) or "normal",
            )
            self._send_json({"goal": goal}, status=HTTPStatus.CREATED)
            return
        if path.endswith("/knowledge"):
            project_id = self._extract_project_id(path, suffix="/knowledge")
            fact = intel.create_knowledge(
                actor=actor,
                project_id=project_id,
                category=self._require_text(body, "category"),
                fact_key=self._require_text(body, "fact_key"),
                title=self._require_text(body, "title"),
                content=self._require_text(body, "content"),
            )
            self._send_json({"knowledge": fact}, status=HTTPStatus.CREATED)
            return
        if path.endswith("/actions"):
            project_id = self._extract_project_id(path, suffix="/actions")
            action = intel.create_action(
                actor=actor,
                project_id=project_id,
                action_key=self._require_text(body, "action_key"),
                title=self._require_text(body, "title"),
                priority=self._optional_text(body.get("priority")) or "normal",
                due_at=self._optional_text(body.get("due_at")),
            )
            self._send_json({"action": action}, status=HTTPStatus.CREATED)
            return
        if path.endswith("/tasks"):
            project_id = self._extract_project_id(path, suffix="/tasks")
            task = intel.create_task(
                actor=actor,
                project_id=project_id,
                title=self._require_text(body, "title"),
                action_id=self._optional_int(body.get("action_id"), minimum=1),
                due_at=self._optional_text(body.get("due_at")),
            )
            self._send_json({"task": task}, status=HTTPStatus.CREATED)
            return
        if path.endswith("/life-events"):
            project_id = self._extract_project_id(path, suffix="/life-events")
            event = intel.create_life_event(
                actor=actor,
                project_id=project_id,
                event_type=self._require_text(body, "event_type"),
                title=self._require_text(body, "title"),
                occurred_at=self._optional_text(body.get("occurred_at")),
            )
            self._send_json({"life_event": event}, status=HTTPStatus.CREATED)
            return
        if path.endswith("/resources"):
            project_id = self._extract_project_id(path, suffix="/resources")
            resource = intel.link_property(
                actor=actor,
                project_id=project_id,
                property_id=self._require_int(body, "property_id", minimum=1),
            )
            self._send_json({"resource": resource}, status=HTTPStatus.CREATED)
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown API route")

    def _handle_v2_ecosystem_get(self, path: str, query: dict[str, list[str]]) -> None:
        actor = self._require_user()
        eco = self.services.ecosystem
        if path == "/api/v2/partners":
            self._send_json(
                eco.list_partners(
                    actor=actor,
                    partner_type=self._first(query, "partner_type"),
                    city=self._first(query, "city"),
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                )
            )
            return
        if path.startswith("/api/v2/partners/"):
            partner_id = self._extract_path_id(path, marker="/api/v2/partners/", resource="Partner")
            self._send_json(eco.get_partner(actor=actor, partner_id=partner_id))
            return
        if path == "/api/v2/services":
            self._send_json(
                eco.list_services(
                    actor=actor,
                    category=self._first(query, "category"),
                    page=self._query_page(query),
                    limit=self._query_limit(query),
                )
            )
            return
        if path.startswith("/api/v2/services/"):
            service_id = self._extract_path_id(path, marker="/api/v2/services/", resource="Service")
            self._send_json(eco.get_service(actor=actor, service_id=service_id))
            return
        if path == "/api/v2/workflows":
            self._send_json(eco.list_workflows(actor=actor))
            return
        if path == "/api/v2/matching":
            project_id = self._first_int(query, "project_id", minimum=1)
            if project_id is None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "validation_error", "project_id is required")
            self._send_json(eco.list_project_matching(actor=actor, project_id=project_id))
            return
        if path == "/api/v2/reputation":
            subject_type = self._require_text_query(query, "subject_type")
            subject_id = self._first_int(query, "subject_id", minimum=1)
            if subject_id is None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "validation_error", "subject_id is required")
            self._send_json(eco.get_reputation(actor=actor, subject_type=subject_type, subject_id=subject_id))
            return
        if path == "/api/v2/notifications/ecosystem":
            self._send_json(eco.list_ecosystem_notifications(actor=actor, limit=self._query_limit(query)))
            return
        if path == "/api/v2/resources":
            project_id = self._first_int(query, "project_id", minimum=1)
            if project_id is None:
                raise ApiError(HTTPStatus.BAD_REQUEST, "validation_error", "project_id is required")
            self._send_json(eco.list_project_resources_ecosystem(actor=actor, project_id=project_id))
            return
        if path.endswith("/matching") and path.startswith("/api/v2/projects/"):
            project_id = self._extract_project_id(path, suffix="/matching")
            self._send_json(eco.list_project_matching(actor=actor, project_id=project_id))
            return
        if path.endswith("/orchestration") and path.startswith("/api/v2/projects/"):
            project_id = self._extract_project_id(path, suffix="/orchestration")
            self._send_json(eco.get_orchestration(actor=actor, project_id=project_id))
            return
        if path.endswith("/workflows") and path.startswith("/api/v2/projects/"):
            project_id = self._extract_project_id(path, suffix="/workflows")
            self._send_json(eco.get_project_workflow(actor=actor, project_id=project_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown ecosystem route")

    def _handle_v2_ecosystem_post(self, path: str, body: dict[str, Any], actor: dict[str, object]) -> None:
        eco = self.services.ecosystem
        if path == "/api/v2/partners":
            partner = eco.create_partner(
                actor=actor,
                organization_id=self._require_int(body, "organization_id", minimum=1),
                partner_type=self._require_text(body, "partner_type"),
                display_name=self._require_text(body, "display_name"),
                description=self._optional_text(body.get("description")),
                city=self._optional_text(body.get("city")),
                region=self._optional_text(body.get("region")),
            )
            self._send_json(partner, status=HTTPStatus.CREATED)
            return
        if path == "/api/v2/matching":
            project_id = self._require_int(body, "project_id", minimum=1)
            self._send_json(eco.run_matching(actor=actor, project_id=project_id))
            return
        if path.endswith("/matching/run") and path.startswith("/api/v2/projects/"):
            project_id = self._extract_project_id(path, suffix="/matching/run")
            self._send_json(eco.run_matching(actor=actor, project_id=project_id))
            return
        raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Unknown ecosystem route")

    def _require_text_query(self, query: dict[str, list[str]], key: str) -> str:
        value = self._first(query, key)
        if not value:
            raise ApiError(HTTPStatus.BAD_REQUEST, "validation_error", f"{key} is required")
        return value


def create_server(config: AppConfig) -> LawimThreadingHTTPServer:
    runtime = build_runtime(config)

    class BoundHandler(LawimRequestHandler):
        pass

    BoundHandler.repository = runtime.repository
    BoundHandler.config = runtime.config
    BoundHandler.services = runtime.services
    BoundHandler.auth_limiter = AuthRateLimiter(
        max_attempts=config.auth_rate_limit_max,
        window_seconds=config.auth_rate_limit_window_seconds,
    )

    server = LawimThreadingHTTPServer((config.host, config.port), BoundHandler)
    server.repository = runtime.repository  # type: ignore[attr-defined]
    server.config = runtime.config  # type: ignore[attr-defined]
    server.services = runtime.services  # type: ignore[attr-defined]
    server.runtime = runtime  # type: ignore[attr-defined]
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
        server = create_server(config)
    except (ValueError, OSError, RepositoryError, sqlite3.Error) as exc:
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
        server.runtime.close()  # type: ignore[attr-defined]
    return 0
