from __future__ import annotations

from dataclasses import dataclass
from http import HTTPStatus

from .config import AppConfig
from .db import LawimRepository
from .dto import PaginationMeta, geo_location_dto, media_dto, paginated_payload, property_dto
from .media_domain import LocalMediaStorage, decode_upload_content


class ServiceError(Exception):
    def __init__(self, status: HTTPStatus, code: str, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message


class PermissionDenied(ServiceError):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(HTTPStatus.FORBIDDEN, "forbidden", message)


class AuthenticationError(ServiceError):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(HTTPStatus.UNAUTHORIZED, "invalid_credentials", message)


@dataclass(frozen=True, slots=True)
class AccessPolicy:
    def is_admin(self, actor: dict[str, object] | None) -> bool:
        return actor is not None and str(actor.get("role")) == "admin"

    def can_manage_organization(self, actor: dict[str, object] | None) -> bool:
        return self.is_admin(actor)

    def can_manage_user(self, actor: dict[str, object] | None, target_user: dict[str, object] | None = None) -> bool:
        if self.is_admin(actor):
            return True
        if actor is None or target_user is None:
            return False
        return actor.get("id") == target_user.get("id")

    def can_manage_property(self, actor: dict[str, object] | None, property_row: dict[str, object] | None = None) -> bool:
        if self.is_admin(actor):
            return True
        if actor is None:
            return False
        organization_id = actor.get("organization_id")
        if organization_id is None:
            return False
        if property_row is None:
            return True
        return property_row.get("owner_organization_id") == organization_id

    def can_manage_media(self, actor: dict[str, object] | None, property_row: dict[str, object] | None = None) -> bool:
        return self.can_manage_property(actor, property_row)

    def can_manage_conversation(
        self,
        actor: dict[str, object] | None,
        conversation_row: dict[str, object] | None = None,
        property_row: dict[str, object] | None = None,
    ) -> bool:
        if self.is_admin(actor):
            return True
        if actor is None:
            return False
        if conversation_row is not None and conversation_row.get("user_id") == actor.get("id"):
            return True
        organization_id = actor.get("organization_id")
        if organization_id is not None and property_row is not None:
            return property_row.get("owner_organization_id") == organization_id
        return False


class LawimServices:
    def __init__(self, repository: LawimRepository, config: AppConfig, policy: AccessPolicy | None = None) -> None:
        self.repository = repository
        self.config = config
        self.policy = policy or AccessPolicy()
        self.media_storage = LocalMediaStorage(config.media_storage_path, public_base_url=config.public_base_url)

    def health(self) -> dict[str, object]:
        return {
            "status": "ok",
            "environment": {
                "app_env": self.config.app_env,
                "stack_profile": self.config.stack_profile,
                "log_level": self.config.log_level,
                "public_base_url": self.config.public_base_url,
                "secret_provider": self.config.secret_provider,
                "seed_demo_data": self.config.seed_demo_data,
            },
            "database": self.repository.backend_profile(),
            "summary": self.repository.summary(),
        }

    def login(self, *, email: str, password: str) -> dict[str, object]:
        user = self.repository.authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationError("Invalid email or password")
        session = self.repository.create_session(user_id=user["id"], ttl_seconds=self.config.session_ttl_seconds)
        return {
            "token": session["token"],
            "session": session,
            "user": self.repository.public_user(user),
        }

    def register(
        self,
        *,
        actor: dict[str, object] | None,
        email: str,
        password: str,
        full_name: str,
        role: str,
        organization_id: int | None = None,
    ) -> dict[str, object]:
        normalized_role = role.lower()
        if normalized_role not in {"admin", "agent", "owner"}:
            raise ServiceError(HTTPStatus.BAD_REQUEST, "invalid_payload", "Invalid user role")
        if actor is None and normalized_role == "admin":
            raise PermissionDenied("Public registration cannot create administrator accounts")
        if actor is not None and not self.policy.is_admin(actor):
            raise PermissionDenied("Only administrators can create staff accounts")
        user = self.repository.create_user(
            email=email,
            full_name=full_name,
            role=normalized_role,
            password=password,
            organization_id=organization_id,
        )
        session = self.repository.create_session(user_id=user["id"], ttl_seconds=self.config.session_ttl_seconds)
        return {
            "token": session["token"],
            "session": session,
            "user": self.repository.public_user(user),
        }

    def logout(self, *, token: str | None) -> dict[str, object]:
        if token:
            self.repository.delete_session(token)
        return {"status": "logged_out"}

    def create_organization(
        self,
        *,
        actor: dict[str, object],
        name: str,
        slug: str,
        kind: str,
        city: str | None = None,
    ) -> dict[str, object]:
        self._require_admin(actor, "Only administrators can create organizations")
        return self.repository.create_organization(name=name, slug=slug, kind=kind, city=city)

    def update_organization(
        self,
        *,
        actor: dict[str, object],
        organization_id: int,
        name: str | None = None,
        slug: str | None = None,
        kind: str | None = None,
        city: str | None = None,
    ) -> dict[str, object]:
        self._require_admin(actor, "Only administrators can update organizations")
        return self.repository.update_organization(organization_id, name=name, slug=slug, kind=kind, city=city)

    def create_user(
        self,
        *,
        actor: dict[str, object],
        email: str,
        full_name: str,
        role: str,
        password: str,
        organization_id: int | None = None,
    ) -> dict[str, object]:
        self._require_admin(actor, "Only administrators can create users")
        return self.repository.create_user(
            email=email,
            full_name=full_name,
            role=role,
            password=password,
            organization_id=organization_id,
        )

    def update_user(
        self,
        *,
        actor: dict[str, object],
        user_id: int,
        email: str | None = None,
        full_name: str | None = None,
        role: str | None = None,
        password: str | None = None,
        organization_id: int | None = None,
    ) -> dict[str, object]:
        target = self.repository.get_user_by_id(user_id)
        if not self.policy.can_manage_user(actor, target):
            raise PermissionDenied("Only administrators or the account owner can update this user")
        if not self.policy.is_admin(actor):
            if email is not None or role is not None or organization_id is not None:
                raise PermissionDenied("Self-service updates are limited to the profile name and password")
        return self.repository.update_user(
            user_id,
            email=email if self.policy.is_admin(actor) else None,
            full_name=full_name,
            role=role if self.policy.is_admin(actor) else None,
            password=password,
            organization_id=organization_id if self.policy.is_admin(actor) else None,
        )

    def delete_user(self, *, actor: dict[str, object], user_id: int) -> dict[str, object]:
        self._require_admin(actor, "Only administrators can delete users")
        self.repository.delete_user(user_id)
        return {"deleted": True, "user_id": user_id}

    def create_property(
        self,
        *,
        actor: dict[str, object],
        title: str,
        summary: str,
        city: str,
        country: str,
        latitude: float | None = None,
        longitude: float | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        currency: str = "XAF",
        status: str = "draft",
        availability: str = "available",
        property_type: str = "apartment",
        owner_organization_id: int | None = None,
        address_line: str | None = None,
        region: str | None = None,
        postal_code: str | None = None,
        metadata: dict[str, object] | str | None = None,
        bedrooms: int = 0,
        bathrooms: int = 0,
        area_sqm: float = 0,
        listing_code: str | None = None,
    ) -> dict[str, object]:
        if self.policy.is_admin(actor):
            resolved_owner = owner_organization_id
        else:
            organization_id = actor.get("organization_id")
            if organization_id is None:
                raise PermissionDenied("Properties require an owning organization")
            if owner_organization_id is not None and owner_organization_id != organization_id:
                raise PermissionDenied("Cannot assign a property to another organization")
            resolved_owner = organization_id
        row = self.repository.create_property(
            title=title,
            summary=summary,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude,
            price_min=price_min,
            price_max=price_max,
            currency=currency,
            status=status,
            availability=availability,
            property_type=property_type,
            owner_organization_id=resolved_owner,
            address_line=address_line,
            region=region,
            postal_code=postal_code,
            metadata=metadata,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area_sqm=area_sqm,
            listing_code=listing_code,
        )
        return property_dto(row)

    def update_property(
        self,
        *,
        actor: dict[str, object],
        property_id: int,
        title: str | None = None,
        summary: str | None = None,
        city: str | None = None,
        country: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        currency: str | None = None,
        status: str | None = None,
        availability: str | None = None,
        property_type: str | None = None,
        owner_organization_id: int | None = None,
        address_line: str | None = None,
        region: str | None = None,
        postal_code: str | None = None,
        metadata: dict[str, object] | str | None = None,
        bedrooms: int | None = None,
        bathrooms: int | None = None,
        area_sqm: float | None = None,
        version: int | None = None,
    ) -> dict[str, object]:
        current = self.repository.get_property(property_id)
        if not self.policy.can_manage_property(actor, current):
            raise PermissionDenied("Property access is restricted to administrators and the owning organization")
        if not self.policy.is_admin(actor):
            if owner_organization_id is not None and owner_organization_id != actor.get("organization_id"):
                raise PermissionDenied("Cannot reassign a property outside the owning organization")
        row = self.repository.update_property(
            property_id,
            title=title,
            summary=summary,
            city=city,
            country=country,
            latitude=latitude,
            longitude=longitude,
            price_min=price_min,
            price_max=price_max,
            currency=currency,
            status=status,
            availability=availability,
            property_type=property_type,
            owner_organization_id=owner_organization_id if self.policy.is_admin(actor) else None,
            address_line=address_line,
            region=region,
            postal_code=postal_code,
            metadata=metadata,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            area_sqm=area_sqm,
            version=version,
        )
        return property_dto(row)

    def publish_property(self, *, actor: dict[str, object], property_id: int, version: int | None = None) -> dict[str, object]:
        current = self.repository.get_property(property_id)
        if not self.policy.can_manage_property(actor, current):
            raise PermissionDenied("Property access is restricted to administrators and the owning organization")
        row = self.repository.publish_property(property_id, version=version)
        return property_dto(row)

    def get_property(self, property_id: int) -> dict[str, object]:
        row = self.repository.get_property(property_id)
        payload = property_dto(row)
        payload["media"] = [media_dto(item) for item in self.repository.list_media(property_id=property_id, limit=100)["items"]]
        return payload

    def list_properties(
        self,
        *,
        city: str | None = None,
        country: str | None = None,
        region: str | None = None,
        status: str | None = None,
        availability: str | None = None,
        property_type: str | None = None,
        owner_organization_id: int | None = None,
        include_deleted: bool = False,
        search: str | None = None,
        page: int = 1,
        limit: int = 10,
        sort: str = "created_at",
        order: str = "desc",
    ) -> dict[str, object]:
        result = self.repository.list_properties(
            city=city,
            country=country,
            region=region,
            status=status,
            availability=availability,
            property_type=property_type,
            owner_organization_id=owner_organization_id,
            include_deleted=include_deleted,
            search=search,
            page=page,
            limit=limit,
            sort=sort,
            order=order,
        )
        pagination = PaginationMeta(
            page=int(result["pagination"]["page"]),
            limit=int(result["pagination"]["limit"]),
            total=int(result["pagination"]["total"]),
            pages=int(result["pagination"]["pages"]),
            sort=str(result["pagination"]["sort"]),
            order=str(result["pagination"]["order"]),
        )
        return paginated_payload(
            [property_dto(item) for item in result["items"]],
            key="properties",
            pagination=pagination,
        )

    def delete_property(self, *, actor: dict[str, object], property_id: int, hard: bool = False) -> dict[str, object]:
        current = self.repository.get_property(property_id, include_deleted=True)
        if not self.policy.can_manage_property(actor, current):
            raise PermissionDenied("Property access is restricted to administrators and the owning organization")
        return self.repository.delete_property(property_id, hard=hard)

    def create_media(
        self,
        *,
        actor: dict[str, object],
        property_id: int,
        kind: str,
        url: str,
        caption: str,
        metadata: dict[str, object] | str | None = None,
        position: int | None = None,
    ) -> dict[str, object]:
        property_row = self.repository.get_property(property_id)
        if not self.policy.can_manage_media(actor, property_row):
            raise PermissionDenied("Media access is restricted to administrators and the owning organization")
        row = self.repository.create_media(
            property_id=property_id,
            kind=kind,
            url=url,
            caption=caption,
            metadata=metadata,
            position=position,
        )
        return media_dto(row)

    def upload_media(
        self,
        *,
        actor: dict[str, object],
        property_id: int,
        filename: str,
        content_base64: str,
        kind: str = "image",
        caption: str = "LAWIM_V2 media",
        mime_type: str | None = None,
        metadata: dict[str, object] | str | None = None,
    ) -> dict[str, object]:
        property_row = self.repository.get_property(property_id)
        if not self.policy.can_manage_media(actor, property_row):
            raise PermissionDenied("Media access is restricted to administrators and the owning organization")
        content = decode_upload_content(content_base64)
        stored = self.media_storage.store(
            property_id=property_id,
            filename=filename,
            content=content,
            mime_type=mime_type,
        )
        row = self.repository.create_media(
            property_id=property_id,
            kind=kind,
            url=stored.public_url,
            caption=caption,
            storage_path=stored.storage_path,
            mime_type=stored.mime_type,
            size_bytes=stored.size_bytes,
            thumbnail_url=stored.thumbnail_url,
            metadata=metadata,
        )
        return media_dto(row)

    def update_media(
        self,
        *,
        actor: dict[str, object],
        media_id: int,
        kind: str | None = None,
        url: str | None = None,
        caption: str | None = None,
        thumbnail_url: str | None = None,
        metadata: dict[str, object] | str | None = None,
        position: int | None = None,
        version: int | None = None,
    ) -> dict[str, object]:
        current = self.repository.get_media(media_id)
        property_row = self.repository.get_property(int(current["property_id"]))
        if not self.policy.can_manage_media(actor, property_row):
            raise PermissionDenied("Media access is restricted to administrators and the owning organization")
        row = self.repository.update_media(
            media_id,
            kind=kind,
            url=url,
            caption=caption,
            thumbnail_url=thumbnail_url,
            metadata=metadata,
            position=position,
            version=version,
        )
        return media_dto(row)

    def delete_media(self, *, actor: dict[str, object], media_id: int, hard: bool = False) -> dict[str, object]:
        current = self.repository.get_media(media_id, include_deleted=True)
        property_row = self.repository.get_property(int(current["property_id"]), include_deleted=True)
        if not self.policy.can_manage_media(actor, property_row):
            raise PermissionDenied("Media access is restricted to administrators and the owning organization")
        result = self.repository.delete_media(media_id, hard=hard)
        if hard and current.get("storage_path"):
            self.media_storage.delete(str(current["storage_path"]))
        return result

    def get_media(self, media_id: int) -> dict[str, object]:
        return media_dto(self.repository.get_media(media_id))

    def list_media(
        self,
        *,
        property_id: int | None = None,
        kind: str | None = None,
        include_deleted: bool = False,
        page: int = 1,
        limit: int = 10,
        sort: str = "created_at",
        order: str = "desc",
    ) -> dict[str, object]:
        result = self.repository.list_media(
            property_id=property_id,
            kind=kind,
            include_deleted=include_deleted,
            page=page,
            limit=limit,
            sort=sort,
            order=order,
        )
        pagination = PaginationMeta(
            page=int(result["pagination"]["page"]),
            limit=int(result["pagination"]["limit"]),
            total=int(result["pagination"]["total"]),
            pages=int(result["pagination"]["pages"]),
            sort=str(result["pagination"]["sort"]),
            order=str(result["pagination"]["order"]),
        )
        return paginated_payload([media_dto(item) for item in result["items"]], key="media", pagination=pagination)

    def normalize_location(
        self,
        *,
        city: str,
        country: str,
        region: str | None = None,
        address_line: str | None = None,
        postal_code: str | None = None,
    ) -> dict[str, object]:
        return self.repository.normalize_location(
            city=city,
            country=country,
            region=region,
            address_line=address_line,
            postal_code=postal_code,
        )

    def search_locations(self, *, query: str | None = None, limit: int = 20) -> list[dict[str, object]]:
        return [geo_location_dto(item) for item in self.repository.search_locations(query=query, limit=limit)]

    def create_conversation(
        self,
        *,
        actor: dict[str, object],
        user_id: int,
        subject: str,
        status: str = "open",
        property_id: int | None = None,
        initial_message: str | None = None,
        sender_user_id: int | None = None,
    ) -> dict[str, object]:
        if not self.policy.is_admin(actor) and user_id != actor.get("id"):
            raise PermissionDenied("Conversation ownership must match the authenticated user")
        if sender_user_id is not None and not self.policy.is_admin(actor) and sender_user_id != actor.get("id"):
            raise PermissionDenied("Message author must match the authenticated user")
        resolved_sender = sender_user_id if sender_user_id is not None else int(actor["id"])
        return self.repository.create_conversation(
            user_id=user_id,
            subject=subject,
            status=status,
            property_id=property_id,
            initial_message=initial_message,
            sender_user_id=resolved_sender,
        )

    def update_conversation(
        self,
        *,
        actor: dict[str, object],
        conversation_id: int,
        subject: str | None = None,
        status: str | None = None,
    ) -> dict[str, object]:
        current = self.repository.get_conversation(conversation_id)
        property_row = None
        if current.get("property_id") is not None:
            property_row = self.repository.get_property(int(current["property_id"]))
        if not self.policy.can_manage_conversation(actor, current, property_row):
            raise PermissionDenied("Conversation access is restricted to participants and administrators")
        return self.repository.update_conversation(conversation_id, subject=subject, status=status)

    def delete_conversation(self, *, actor: dict[str, object], conversation_id: int) -> dict[str, object]:
        current = self.repository.get_conversation(conversation_id)
        if not self.policy.is_admin(actor) and current.get("user_id") != actor.get("id"):
            raise PermissionDenied("Conversation access is restricted to participants and administrators")
        return self.repository.delete_conversation(conversation_id)

    def add_message(
        self,
        *,
        actor: dict[str, object],
        conversation_id: int,
        sender_user_id: int,
        body: str,
    ) -> dict[str, object]:
        current = self.repository.get_conversation(conversation_id)
        property_row = None
        if current.get("property_id") is not None:
            property_row = self.repository.get_property(int(current["property_id"]))
        if not self.policy.can_manage_conversation(actor, current, property_row):
            raise PermissionDenied("Conversation access is restricted to participants and administrators")
        if not self.policy.is_admin(actor) and sender_user_id != actor.get("id"):
            raise PermissionDenied("Message author must match the authenticated user")
        return self.repository.add_message(conversation_id, sender_user_id, body)

    def events(self, *, actor: dict[str, object], limit: int = 50) -> list[dict[str, object]]:
        if not self.policy.is_admin(actor):
            raise PermissionDenied("Only administrators can inspect the event log")
        return self.repository.list_events(limit=limit)

    def _require_admin(self, actor: dict[str, object], message: str) -> None:
        if not self.policy.is_admin(actor):
            raise PermissionDenied(message)
