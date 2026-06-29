from __future__ import annotations

from dataclasses import dataclass

from .errors import ValidationError


@dataclass(frozen=True, slots=True)
class MultipartPart:
    name: str
    filename: str | None
    content_type: str | None
    data: bytes


def parse_multipart_form_data(content_type: str, body: bytes, *, max_bytes: int) -> dict[str, MultipartPart]:
    if len(body) > max_bytes:
        raise ValidationError(f"upload exceeds maximum size of {max_bytes} bytes")
    if "multipart/form-data" not in content_type.lower():
        raise ValidationError("expected multipart/form-data content type")
    boundary_token = _extract_boundary(content_type)
    if not boundary_token:
        raise ValidationError("multipart boundary is required")
    boundary = boundary_token.encode("utf-8")
    delimiter = b"--" + boundary
    parts: dict[str, MultipartPart] = {}
    for chunk in body.split(delimiter):
        if not chunk or chunk in {b"--", b"--\r\n"}:
            continue
        chunk = chunk.lstrip(b"\r\n")
        if chunk.endswith(b"\r\n"):
            chunk = chunk[:-2]
        header_block, _, content = chunk.partition(b"\r\n\r\n")
        if not header_block:
            continue
        headers = _parse_headers(header_block.decode("utf-8", errors="replace"))
        disposition = headers.get("content-disposition", "")
        name = _extract_param(disposition, "name")
        if not name:
            continue
        filename = _extract_param(disposition, "filename")
        part_content_type = headers.get("content-type")
        if content.endswith(b"\r\n"):
            content = content[:-2]
        parts[name] = MultipartPart(
            name=name,
            filename=filename,
            content_type=part_content_type,
            data=content,
        )
    if not parts:
        raise ValidationError("multipart payload is empty")
    return parts


def _extract_boundary(content_type: str) -> str | None:
    for token in content_type.split(";"):
        token = token.strip()
        if token.lower().startswith("boundary="):
            value = token.split("=", 1)[1].strip().strip('"')
            return value or None
    return None


def _parse_headers(block: str) -> dict[str, str]:
    headers: dict[str, str] = {}
    for line in block.split("\r\n"):
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        headers[key.strip().lower()] = value.strip()
    return headers


def _extract_param(header: str, param: str) -> str | None:
    for token in header.split(";"):
        token = token.strip()
        if token.lower().startswith(f"{param}="):
            return token.split("=", 1)[1].strip().strip('"')
    return None
