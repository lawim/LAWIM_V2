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
from typing import Any

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
    storage_path: str
    public_url: str
    mime_type: str
    size_bytes: int
    thumbnail_url: str


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
    def __init__(self, root: Path, *, public_base_url: str) -> None:
        self.root = Path(root)
        self.public_base_url = public_base_url.rstrip("/")

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
        public_url = f"{self.public_base_url}/media/{relative.as_posix()}"
        thumbnail_url = build_thumbnail_url(public_url, safe_name)
        return StoredMedia(
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


def validate_upload_bytes(
    content: bytes,
    *,
    mime_type: str | None,
    filename: str,
    max_bytes: int,
) -> None:
    if not content:
        raise ValidationError("upload content is required")
    if len(content) > max_bytes:
        raise ValidationError(f"upload exceeds maximum size of {max_bytes} bytes")
    _safe_filename(filename)
    if mime_type:
        allowed = {"image/jpeg", "image/png", "image/webp", "image/gif", "application/pdf"}
        if mime_type not in allowed:
            raise ValidationError(f"unsupported mime type: {mime_type}")


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
        return normalized
    raise ValidationError("url must be http(s), data or /media/ path")
