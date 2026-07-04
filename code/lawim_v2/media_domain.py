from __future__ import annotations

import base64
import binascii
import json
import mimetypes
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse

from .errors import ValidationError


MEDIA_KINDS = frozenset({"image", "video", "document", "floorplan", "thumbnail"})
THUMBNAIL_MAX_EDGE = 256
THUMBNAIL_CONTRACT = {
    "max_edge_px": THUMBNAIL_MAX_EDGE,
    "format": "image/svg+xml",
    "strategy": "deterministic-svg-placeholder",
}


@dataclass(frozen=True, slots=True)
class StoredMedia:
    provider_name: str
    provider_object_id: str | None
    storage_path: str
    public_url: str
    mime_type: str
    size_bytes: int
    thumbnail_url: str


class MediaProvider(Protocol):
    @property
    def name(self) -> str: ...

    def store(
        self,
        *,
        property_id: int,
        filename: str,
        content: bytes,
        mime_type: str | None = None,
    ) -> StoredMedia: ...

    def delete(self, storage_path: str) -> None: ...


MEDIA_LIFECYCLE_STATES = frozenset({"active", "deleted", "archived", "pending"})
MEDIA_BACKUP_STATES = frozenset({"available", "archived", "restored", "missing"})


class MediaRegistry:
    def __init__(self, providers: list[MediaProvider]) -> None:
        self.providers = {provider.name: provider for provider in providers}

    def get(self, provider_name: str) -> MediaProvider:
        provider = self.providers.get(provider_name)
        if provider is None:
            raise ValidationError(f"unknown media provider: {provider_name}")
        return provider

    def register(self, provider: MediaProvider) -> None:
        self.providers[provider.name] = provider


class StorageOrchestrator:
    def __init__(self, registry: MediaRegistry, default_provider: str = "local") -> None:
        self.registry = registry
        self.default_provider = default_provider
        self.registry.get(default_provider)

    def store(
        self,
        *,
        property_id: int,
        filename: str,
        content: bytes,
        mime_type: str | None = None,
        provider_name: str | None = None,
    ) -> StoredMedia:
        resolved_provider = provider_name or self.default_provider
        provider = self.registry.get(resolved_provider)
        return provider.store(property_id=property_id, filename=filename, content=content, mime_type=mime_type)

    def delete(self, provider_name: str, storage_path: str) -> None:
        provider = self.registry.get(provider_name)
        provider.delete(storage_path)


def parse_storage_path(storage_path: str, default_provider: str = "local") -> tuple[str, str]:
    normalized = storage_path.strip()
    if not normalized:
        raise ValidationError("storage_path is required")
    if ":" in normalized:
        provider_name, object_id = normalized.split(":", 1)
        if not provider_name or not object_id:
            raise ValidationError("storage_path must include a provider prefix and object id")
        return provider_name, object_id
    return default_provider, normalized


class MediaLifecycleEngine:
    def transition(self, current_state: str, target_state: str) -> str:
        if target_state not in MEDIA_LIFECYCLE_STATES:
            raise ValidationError(f"unsupported lifecycle state: {target_state}")
        if current_state not in MEDIA_LIFECYCLE_STATES:
            raise ValidationError(f"invalid current lifecycle state: {current_state}")
        if current_state == "deleted" and target_state not in {"deleted", "archived"}:
            raise ValidationError("deleted media cannot be reverted except to archived")
        return target_state


class BackupCenter:
    def __init__(self) -> None:
        pass

    def validate_backup_state(self, backup_state: str) -> str:
        if backup_state not in MEDIA_BACKUP_STATES:
            raise ValidationError(f"unsupported backup state: {backup_state}")
        return backup_state

    def build_metadata(self, metadata: dict[str, Any] | str | None) -> str:
        return normalize_metadata(metadata)


class MediaStorage(ABC):
    @abstractmethod
    def store(
        self,
        *,
        property_id: int,
        filename: str,
        content: bytes,
        mime_type: str | None = None,
    ) -> StoredMedia: ...

    @abstractmethod
    def delete(self, storage_path: str) -> None: ...


class LocalMediaStorage(MediaStorage):
    name = "local"

    def __init__(self, root: Path, *, public_base_url: str, cdn_base_url: str | None = None) -> None:
        self.root = Path(root)
        self.public_base_url = public_base_url.rstrip("/")
        self.cdn_base_url = cdn_base_url.rstrip("/") if cdn_base_url else None

    def _public_url(self, relative: Path) -> str:
        if self.cdn_base_url:
            return f"{self.cdn_base_url}/{relative.as_posix()}"
        return f"{self.public_base_url}/media/{relative.as_posix()}"

    def store(
        self,
        *,
        property_id: int,
        filename: str,
        content: bytes,
        mime_type: str | None = None,
    ) -> StoredMedia:
        if not content:
            raise ValidationError("upload content is required")
        safe_name = _safe_filename(filename)
        resolved_mime = mime_type or mimetypes.guess_type(safe_name)[0] or "application/octet-stream"
        relative = Path("properties") / str(property_id) / f"{uuid.uuid4().hex}-{safe_name}"
        target = self.root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        public_url = self._public_url(relative)
        thumbnail_url = build_thumbnail_url(public_url, safe_name)
        return StoredMedia(
            provider_name=self.name,
            provider_object_id=relative.as_posix(),
            storage_path=relative.as_posix(),
            public_url=public_url,
            mime_type=resolved_mime,
            size_bytes=len(content),
            thumbnail_url=thumbnail_url,
        )

    def delete(self, storage_path: str) -> None:
        target = self.root / storage_path
        if target.is_file():
            target.unlink()


ALLOWED_UPLOAD_MIMES = frozenset({"image/jpeg", "image/png", "image/webp", "image/gif", "application/pdf"})


def sniff_mime_type(content: bytes) -> str | None:
    if content.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if content.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if len(content) >= 12 and content[:4] == b"RIFF" and content[8:12] == b"WEBP":
        return "image/webp"
    if content.startswith((b"GIF87a", b"GIF89a")):
        return "image/gif"
    if content.startswith(b"%PDF"):
        return "application/pdf"
    return None


def validate_upload_bytes(
    content: bytes,
    *,
    mime_type: str | None,
    filename: str,
    max_bytes: int,
) -> str:
    if not content:
        raise ValidationError("upload content is required")
    if len(content) > max_bytes:
        raise ValidationError(f"upload exceeds maximum size of {max_bytes} bytes")
    _safe_filename(filename)
    detected = sniff_mime_type(content)
    if detected is None:
        raise ValidationError("unsupported or unrecognized file content")
    if mime_type and mime_type != detected:
        raise ValidationError(f"mime type mismatch: declared {mime_type}, detected {detected}")
    effective = mime_type or detected
    if effective not in ALLOWED_UPLOAD_MIMES:
        raise ValidationError(f"unsupported mime type: {effective}")
    return effective


def _safe_filename(filename: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", filename.strip()).strip("-")
    if not cleaned:
        raise ValidationError("filename is required")
    return cleaned[:120]


def normalize_kind(kind: str) -> str:
    normalized = kind.strip().lower()
    if normalized not in MEDIA_KINDS:
        raise ValidationError(f"unsupported media kind: {normalized}")
    return normalized


def normalize_metadata(metadata: dict[str, Any] | str | None) -> str:
    if metadata is None:
        return "{}"
    if isinstance(metadata, str):
        try:
            parsed = json.loads(metadata)
        except json.JSONDecodeError as exc:
            raise ValidationError("metadata must be valid JSON") from exc
        if not isinstance(parsed, dict):
            raise ValidationError("metadata must be a JSON object")
        return json.dumps(parsed, ensure_ascii=False, sort_keys=True)
    if not isinstance(metadata, dict):
        raise ValidationError("metadata must be a JSON object")
    return json.dumps(metadata, ensure_ascii=False, sort_keys=True)


def metadata_dict(metadata_json: str | None) -> dict[str, object]:
    if not metadata_json:
        return {}
    try:
        parsed = json.loads(metadata_json)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def decode_upload_content(content_base64: str) -> bytes:
    payload = content_base64.strip()
    if not payload:
        raise ValidationError("content_base64 is required")
    try:
        return base64.b64decode(payload, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValidationError("content_base64 must be valid base64") from exc


def build_thumbnail_url(source_url: str, label: str) -> str:
    safe_label = label.replace("'", "")
    svg = (
        "<svg xmlns='http://www.w3.org/2000/svg' "
        f"width='{THUMBNAIL_MAX_EDGE}' height='{THUMBNAIL_MAX_EDGE}' viewBox='0 0 256 256'>"
        "<rect width='256' height='256' fill='#0f172a'/>"
        f"<text x='16' y='128' fill='white' font-size='18' font-family='sans-serif'>{safe_label[:28]}</text>"
        "</svg>"
    )
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def validate_media_url(url: str) -> str:
    normalized = url.strip()
    if not normalized:
        raise ValidationError("url is required")
    if normalized.startswith(("http://", "https://", "data:", "/media/")):
        parsed = urlparse(normalized)
        host = (parsed.netloc or "").lower()
        if host.endswith("drive.google.com") or host.endswith("docs.google.com") or "drive.google.com" in host or "docs.google.com" in host:
            raise ValidationError("Google Drive URLs are not supported for media storage")
        return normalized
    raise ValidationError("url must be http(s), data or /media/ path")
