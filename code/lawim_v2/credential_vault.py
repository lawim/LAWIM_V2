from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


ACTIVATION_TIMESTAMP = "2026-07-05T10:00:00Z"
_DEFAULT_VAULT_KEY = "lawim-credential-vault-placeholder"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_timestamp(value: str) -> datetime | None:
    if not value or value == "never":
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc)


def _format_timestamp(value: datetime | None) -> str:
    if value is None:
        return "never"
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _shift_timestamp(value: str, *, days: int = 0) -> str:
    parsed = _parse_timestamp(value)
    if parsed is None:
        return "never"
    return _format_timestamp(parsed + timedelta(days=days))


def _field_value(source: Any, key: str, default: Any = None) -> Any:
    if isinstance(source, Mapping):
        return source.get(key, default)
    return getattr(source, key, default)


def _enum_value(value: Any) -> Any:
    return getattr(value, "value", value)


class CredentialStatus:
    PLACEHOLDER_CONFIGURED = "placeholder-configured"
    READY = "ready"
    ACTIVE = "active"
    ROTATION_DUE = "rotation-due"
    EXPIRED = "expired"
    INVALID = "invalid"
    REVOKED = "revoked"
    DISABLED = "disabled"

    @classmethod
    def active_states(cls) -> tuple[str, ...]:
        return (cls.PLACEHOLDER_CONFIGURED, cls.READY, cls.ACTIVE)


class CredentialScope:
    GOOGLE_DRIVE = "google-drive"
    STORAGE_REGISTRY = "storage-registry"
    STORAGE_SETUP_WIZARD = "storage-setup-wizard"
    GOOGLE_DRIVE_ADMIN = "google-drive-admin"
    GOOGLE_DRIVE_SECURITY = "google-drive-security"
    BACKUP_CENTER = "backup-center"


class CredentialType:
    GOOGLE_DRIVE_OAUTH2 = "google-drive-oauth2"
    SECRET_REFERENCE = "secret-reference"


@dataclass(slots=True)
class AuditTrail:
    entries: list[dict[str, Any]] = field(default_factory=list)

    def append(self, event: str, *, details: Mapping[str, Any] | None = None) -> dict[str, Any]:
        entry = {
            "timestamp": _utc_now(),
            "event": event,
            "details": dict(details or {}),
        }
        self.entries.append(entry)
        return entry

    def latest(self) -> dict[str, Any] | None:
        return self.entries[-1] if self.entries else None

    def snapshot(self) -> dict[str, Any]:
        return {
            "event_count": len(self.entries),
            "latest": self.latest(),
            "entries": list(self.entries[-20:]),
        }


@dataclass(slots=True)
class CredentialReference:
    credential_id: str
    logical_name: str
    drive_id: str
    role: str = ""
    provider: str = "google-drive"
    scope: str = CredentialScope.GOOGLE_DRIVE
    credential_type: str = CredentialType.GOOGLE_DRIVE_OAUTH2
    status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    masked_secret: str = "***"
    last_used_at: str = "never"
    last_test_at: str = "never"
    expires_at: str = "never"
    rotation_due_at: str = "never"

    def as_dict(self) -> dict[str, Any]:
        return {
            "credential_id": self.credential_id,
            "logical_name": self.logical_name,
            "drive_id": self.drive_id,
            "role": self.role,
            "provider": self.provider,
            "scope": self.scope,
            "credential_type": self.credential_type,
            "status": self.status,
            "masked_secret": self.masked_secret,
            "last_used_at": self.last_used_at,
            "last_test_at": self.last_test_at,
            "expires_at": self.expires_at,
            "rotation_due_at": self.rotation_due_at,
        }


@dataclass(slots=True)
class CredentialRecord:
    credential_id: str
    logical_name: str
    drive_id: str
    role: str = ""
    provider: str = "google-drive"
    scope: str = CredentialScope.GOOGLE_DRIVE
    credential_type: str = CredentialType.GOOGLE_DRIVE_OAUTH2
    status: str = CredentialStatus.PLACEHOLDER_CONFIGURED
    encrypted_secret: str = ""
    secret_hash: str = ""
    masked_secret: str = "***"
    created_at: str = field(default_factory=_utc_now)
    updated_at: str = field(default_factory=_utc_now)
    last_used_at: str = "never"
    last_success_at: str = "never"
    last_failure_at: str = "never"
    last_connection_test: str = "never"
    last_upload_test: str = "never"
    last_download_test: str = "never"
    last_healthcheck: str = "never"
    expires_at: str = "never"
    rotation_due_at: str = "never"
    rotation_interval_days: int = 90
    rotation_count: int = 0
    revoked_at: str = "never"
    disabled_at: str = "never"
    notes: str = "placeholder-only"
    history: list[dict[str, Any]] = field(default_factory=list)

    def is_active(self) -> bool:
        return self.status in CredentialStatus.active_states()

    def is_expired(self, *, now: str | None = None) -> bool:
        reference = _parse_timestamp(now or _utc_now())
        expires_at = _parse_timestamp(self.expires_at)
        return bool(reference and expires_at and reference >= expires_at)

    def is_rotation_due(self, *, now: str | None = None) -> bool:
        reference = _parse_timestamp(now or _utc_now())
        rotation_due_at = _parse_timestamp(self.rotation_due_at)
        return bool(reference and rotation_due_at and reference >= rotation_due_at)

    def as_reference(self) -> CredentialReference:
        return CredentialReference(
            credential_id=self.credential_id,
            logical_name=self.logical_name,
            drive_id=self.drive_id,
            role=self.role,
            provider=self.provider,
            scope=self.scope,
            credential_type=self.credential_type,
            status=self.status,
            last_used_at=self.last_used_at,
            last_test_at=self.last_connection_test,
            expires_at=self.expires_at,
            rotation_due_at=self.rotation_due_at,
        )

    def as_dict(self, *, masked: bool = True) -> dict[str, Any]:
        payload = {
            "credential_id": self.credential_id,
            "logical_name": self.logical_name,
            "drive_id": self.drive_id,
            "role": self.role,
            "provider": self.provider,
            "scope": self.scope,
            "credential_type": self.credential_type,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_used_at": self.last_used_at,
            "last_success_at": self.last_success_at,
            "last_failure_at": self.last_failure_at,
            "last_connection_test": self.last_connection_test,
            "last_upload_test": self.last_upload_test,
            "last_download_test": self.last_download_test,
            "last_healthcheck": self.last_healthcheck,
            "expires_at": self.expires_at,
            "rotation_due_at": self.rotation_due_at,
            "rotation_interval_days": self.rotation_interval_days,
            "rotation_count": self.rotation_count,
            "revoked_at": self.revoked_at,
            "disabled_at": self.disabled_at,
            "notes": self.notes,
            "history": list(self.history),
        }
        if masked:
            payload["masked_secret"] = self.masked_secret
        else:
            payload["encrypted_secret"] = self.encrypted_secret
            payload["masked_secret"] = self.masked_secret
        return payload


class CredentialEncryptor:
    def __init__(self, vault_key: str = _DEFAULT_VAULT_KEY) -> None:
        self._key = hashlib.sha256(vault_key.encode("utf-8")).digest()

    def _keystream(self, nonce: bytes, length: int) -> bytes:
        chunks = bytearray()
        counter = 0
        while len(chunks) < length:
            block = hmac.new(self._key, nonce + counter.to_bytes(4, "big"), hashlib.sha256).digest()
            chunks.extend(block)
            counter += 1
        return bytes(chunks[:length])

    def fingerprint(self, secret: str) -> str:
        return hashlib.sha256(secret.encode("utf-8")).hexdigest()

    def encrypt(self, secret: str, *, credential_id: str = "") -> str:
        plaintext = secret.encode("utf-8")
        nonce = secrets.token_bytes(16)
        keystream = self._keystream(nonce, len(plaintext))
        cipher = bytes(left ^ right for left, right in zip(plaintext, keystream))
        mac = hmac.new(self._key, nonce + cipher + credential_id.encode("utf-8"), hashlib.sha256).digest()
        token = base64.urlsafe_b64encode(nonce + cipher + mac).decode("ascii")
        return f"v1:{token}"

    def decrypt(self, encrypted: str, *, credential_id: str = "") -> str:
        if not encrypted.startswith("v1:"):
            raise ValueError("unsupported encrypted secret format")
        payload = base64.urlsafe_b64decode(encrypted[3:].encode("ascii"))
        if len(payload) < 48:
            raise ValueError("encrypted secret is truncated")
        nonce = payload[:16]
        mac = payload[-32:]
        cipher = payload[16:-32]
        expected_mac = hmac.new(self._key, nonce + cipher + credential_id.encode("utf-8"), hashlib.sha256).digest()
        if not hmac.compare_digest(mac, expected_mac):
            raise ValueError("encrypted secret integrity check failed")
        keystream = self._keystream(nonce, len(cipher))
        plaintext = bytes(left ^ right for left, right in zip(cipher, keystream))
        return plaintext.decode("utf-8")


class CredentialMasker:
    _PATTERNS: tuple[re.Pattern[str], ...] = (
        re.compile(r"(?i)\b(client[_-]?secret|refresh[_-]?token|access[_-]?token|oauth[_-]?secret|api[_-]?key)\b\s*[:=]\s*([^\s'\"`]+)"),
        re.compile(r"(?i)https?://(?:www\.)?drive\.google\.com/[^\s'\"`]+"),
        re.compile(r"(?i)\b(secret)\s*=\s*([^\s'\"`]+)"),
    )

    def mask_text(self, text: str) -> str:
        masked = text
        for pattern in self._PATTERNS:
            if pattern.pattern.startswith("(?i)https?://"):
                masked = pattern.sub("[redacted-drive-url]", masked)
            elif "secret" in pattern.pattern.lower():
                masked = pattern.sub(lambda match: f"{match.group(1)}=<redacted>", masked)
            else:
                masked = pattern.sub("<redacted>", masked)
        return masked

    def mask_value(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.mask_text(value)
        if isinstance(value, Mapping):
            return self.mask_mapping(value)
        if isinstance(value, list):
            return [self.mask_value(item) for item in value]
        if isinstance(value, tuple):
            return tuple(self.mask_value(item) for item in value)
        return value

    def mask_mapping(self, mapping: Mapping[str, Any]) -> dict[str, Any]:
        masked: dict[str, Any] = {}
        for key, value in mapping.items():
            key_text = str(key).lower()
            if any(term in key_text for term in ("secret", "token", "api_key", "oauth")):
                masked[key] = "<redacted>"
            else:
                masked[key] = self.mask_value(value)
        return masked

    def mask_record(self, record: CredentialRecord | Mapping[str, Any]) -> dict[str, Any]:
        if isinstance(record, CredentialRecord):
            return self.mask_mapping(record.as_dict(masked=True))
        return self.mask_mapping(record)

    def mask_reference(self, reference: CredentialReference | Mapping[str, Any]) -> dict[str, Any]:
        if isinstance(reference, CredentialReference):
            return self.mask_mapping(reference.as_dict())
        return self.mask_mapping(reference)


@dataclass(slots=True)
class LogMasker:
    masker: CredentialMasker = field(default_factory=CredentialMasker)

    def mask_text(self, text: str) -> str:
        return self.masker.mask_text(text)

    def mask_payload(self, payload: Mapping[str, Any] | Sequence[Any] | str) -> Any:
        if isinstance(payload, str):
            return self.mask_text(payload)
        if isinstance(payload, Mapping):
            return self.masker.mask_mapping(payload)
        if isinstance(payload, Sequence):
            return [self.mask_payload(item) if isinstance(item, (Mapping, Sequence, str)) else item for item in payload]
        return payload


@dataclass(slots=True)
class CredentialProvider:
    records: dict[str, CredentialRecord] = field(default_factory=dict)
    audit_trail: AuditTrail = field(default_factory=AuditTrail)

    def put_record(self, record: CredentialRecord) -> CredentialRecord:
        self.records[record.credential_id] = record
        self.audit_trail.append("credential-record-upserted", details={"credential_id": record.credential_id})
        return record

    def get_record(self, credential_id: str) -> CredentialRecord:
        try:
            return self.records[credential_id]
        except KeyError as exc:
            raise KeyError(f"unknown credential id: {credential_id}") from exc

    def delete_record(self, credential_id: str) -> None:
        self.records.pop(credential_id, None)
        self.audit_trail.append("credential-record-deleted", details={"credential_id": credential_id})

    def list_records(self) -> list[CredentialRecord]:
        return list(self.records.values())

    def snapshot(self) -> dict[str, Any]:
        return {
            "record_count": len(self.records),
            "records": [record.as_dict(masked=True) for record in self.list_records()],
            "audit_trail": self.audit_trail.snapshot(),
        }


@dataclass(slots=True)
class CredentialValidator:
    allowed_statuses: tuple[str, ...] = (
        CredentialStatus.PLACEHOLDER_CONFIGURED,
        CredentialStatus.READY,
        CredentialStatus.ACTIVE,
        CredentialStatus.ROTATION_DUE,
        CredentialStatus.EXPIRED,
        CredentialStatus.INVALID,
        CredentialStatus.REVOKED,
        CredentialStatus.DISABLED,
    )

    def validate_reference(self, reference: CredentialReference) -> list[str]:
        issues: list[str] = []
        if not reference.credential_id.strip():
            issues.append("credential_id is required")
        if not reference.logical_name.strip():
            issues.append("logical_name is required")
        if reference.status not in self.allowed_statuses:
            issues.append(f"unsupported status: {reference.status}")
        return issues

    def validate_record(self, record: CredentialRecord) -> list[str]:
        issues = self.validate_reference(record.as_reference())
        if not record.encrypted_secret.startswith("v1:"):
            issues.append("encrypted_secret must use the v1 envelope")
        if not record.secret_hash:
            issues.append("secret_hash is required")
        if record.is_expired():
            issues.append("credential is expired")
        return issues

    def validate_vault(self, vault: "CredentialVault") -> dict[str, Any]:
        issues = vault.scan()
        return {
            "valid": len(issues) == 0,
            "issue_count": len(issues),
            "issues": issues,
        }


@dataclass(slots=True)
class CredentialAuditLogger:
    trail: AuditTrail = field(default_factory=AuditTrail)
    masker: CredentialMasker = field(default_factory=CredentialMasker)

    def record(self, event: str, *, credential_id: str | None = None, details: Mapping[str, Any] | None = None) -> dict[str, Any]:
        sanitized = self.masker.mask_mapping(dict(details or {}))
        entry = self.trail.append(event, details={**sanitized, **({"credential_id": credential_id} if credential_id else {})})
        return entry

    def snapshot(self) -> dict[str, Any]:
        return self.trail.snapshot()


@dataclass(slots=True)
class CredentialRotationPolicy:
    rotation_interval_days: int = 90
    expiration_days: int = 365
    warning_window_days: int = 14
    auto_rotate: bool = True

    def rotation_due_at(self, created_at: str) -> str:
        return _shift_timestamp(created_at, days=self.rotation_interval_days)

    def expiration_at(self, created_at: str) -> str:
        return _shift_timestamp(created_at, days=self.expiration_days)

    def is_rotation_due(self, record: CredentialRecord, *, now: str | None = None) -> bool:
        if record.status in {CredentialStatus.EXPIRED, CredentialStatus.INVALID, CredentialStatus.REVOKED, CredentialStatus.DISABLED}:
            return True
        reference = _parse_timestamp(now or _utc_now())
        due_at = _parse_timestamp(record.rotation_due_at)
        if reference is None or due_at is None:
            return False
        return reference >= due_at

    def is_expiring_soon(self, record: CredentialRecord, *, now: str | None = None) -> bool:
        reference = _parse_timestamp(now or _utc_now())
        expires_at = _parse_timestamp(record.expires_at)
        if reference is None or expires_at is None:
            return False
        warning = expires_at - timedelta(days=self.warning_window_days)
        return warning <= reference < expires_at


@dataclass(slots=True)
class CredentialRotationManager:
    policy: CredentialRotationPolicy = field(default_factory=CredentialRotationPolicy)
    logger: CredentialAuditLogger = field(default_factory=CredentialAuditLogger)

    def rotation_queue(self, vault: "CredentialVault", *, now: str | None = None) -> list[str]:
        return [record.credential_id for record in vault.list_records() if self.policy.is_rotation_due(record, now=now)]

    def rotate(self, vault: "CredentialVault", credential_id: str, *, secret: str | None = None) -> CredentialRecord:
        record = vault.record_for(credential_id)
        plaintext = secret if secret is not None else vault.decrypt_secret(credential_id)
        record.encrypted_secret = vault.encryptor.encrypt(plaintext, credential_id=record.credential_id)
        record.secret_hash = vault.encryptor.fingerprint(plaintext)
        record.rotation_count += 1
        record.updated_at = _utc_now()
        record.status = CredentialStatus.ACTIVE
        record.rotation_due_at = self.policy.rotation_due_at(record.updated_at)
        record.expires_at = self.policy.expiration_at(record.updated_at)
        record.last_success_at = record.updated_at
        record.last_used_at = record.updated_at
        record.history.append({"timestamp": record.updated_at, "event": "rotated"})
        self.logger.record("credential-rotated", credential_id=credential_id, details={"rotation_count": record.rotation_count})
        vault.provider.put_record(record)
        return record


@dataclass(slots=True)
class SecretScanner:
    patterns: tuple[re.Pattern[str], ...] = (
        re.compile(r"(?i)\b(client[_-]?secret|refresh[_-]?token|access[_-]?token|oauth[_-]?secret|api[_-]?key)\b\s*[:=]\s*([^\s'\"`]+)"),
        re.compile(r"(?i)\bsecret\b\s*[:=]\s*([^\s'\"`]+)"),
        re.compile(r"(?i)https?://(?:www\.)?drive\.google\.com/[^\s'\"`]+"),
    )

    def scan_text(self, text: str) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        for pattern in self.patterns:
            for match in pattern.finditer(text):
                findings.append(
                    {
                        "pattern": pattern.pattern,
                        "match": match.group(0),
                        "redacted": "<redacted>",
                    }
                )
        return findings

    def scan_mapping(self, mapping: Mapping[str, Any]) -> list[dict[str, Any]]:
        findings: list[dict[str, Any]] = []
        safe_keys = {"masked_secret", "secret_hash", "encrypted_secret"}
        for key, value in mapping.items():
            if isinstance(value, Mapping):
                findings.extend(self.scan_mapping(value))
            elif isinstance(value, (list, tuple)):
                for item in value:
                    if isinstance(item, Mapping):
                        findings.extend(self.scan_mapping(item))
                    elif isinstance(item, str):
                        findings.extend(self.scan_text(item))
            elif isinstance(value, str):
                findings.extend(self.scan_text(value))
            key_text = str(key).lower()
            if key_text in safe_keys:
                continue
            if any(term in key_text for term in ("secret", "token", "api_key", "oauth")):
                findings.append({"pattern": str(key), "match": str(value), "redacted": "<redacted>"})
        return findings

    def scan_file(self, path: Path) -> list[dict[str, Any]]:
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="utf-8", errors="ignore")
        return self.scan_text(content)


@dataclass(slots=True)
class CredentialScanner:
    secret_scanner: SecretScanner = field(default_factory=SecretScanner)

    def scan_record(self, record: CredentialRecord | Mapping[str, Any]) -> list[dict[str, Any]]:
        if isinstance(record, CredentialRecord):
            payload = record.as_dict(masked=True)
        else:
            payload = dict(record)
        return self.secret_scanner.scan_mapping(payload)

    def scan_reference(self, reference: CredentialReference | Mapping[str, Any]) -> list[dict[str, Any]]:
        if isinstance(reference, CredentialReference):
            payload = reference.as_dict()
        else:
            payload = dict(reference)
        return self.secret_scanner.scan_mapping(payload)

    def scan_vault(self, vault: "CredentialVault") -> list[dict[str, Any]]:
        return self.secret_scanner.scan_text(json.dumps(vault.snapshot(), sort_keys=True))


@dataclass(slots=True)
class GitSecretGuard:
    scanner: SecretScanner = field(default_factory=SecretScanner)

    def scan_diff(self, diff_text: str) -> list[dict[str, Any]]:
        return self.scanner.scan_text(diff_text)

    def scan_path(self, path: Path) -> list[dict[str, Any]]:
        if path.is_dir():
            findings: list[dict[str, Any]] = []
            for child in path.rglob("*"):
                if child.is_file():
                    findings.extend(self.scanner.scan_file(child))
            return findings
        return self.scanner.scan_file(path)

    def is_clean(self, text: str) -> bool:
        return len(self.scan_diff(text)) == 0

    def assert_clean(self, text: str) -> None:
        findings = self.scan_diff(text)
        if findings:
            raise ValueError("secret material detected in Git payload")


@dataclass(slots=True)
class CredentialVault:
    provider: CredentialProvider = field(default_factory=CredentialProvider)
    encryptor: CredentialEncryptor = field(default_factory=CredentialEncryptor)
    masker: CredentialMasker = field(default_factory=CredentialMasker)
    validator: CredentialValidator = field(default_factory=CredentialValidator)
    audit_logger: CredentialAuditLogger = field(default_factory=CredentialAuditLogger)
    rotation_manager: CredentialRotationManager = field(default_factory=CredentialRotationManager)
    rotation_policy: CredentialRotationPolicy = field(default_factory=CredentialRotationPolicy)
    name: str = "lawim-credential-vault"
    status: str = "activation-ready"

    def register(
        self,
        *,
        credential_id: str,
        logical_name: str,
        drive_id: str,
        role: str = "",
        secret_marker: str,
        provider: str = "google-drive",
        scope: str = CredentialScope.GOOGLE_DRIVE,
        credential_type: str = CredentialType.GOOGLE_DRIVE_OAUTH2,
        status: str = CredentialStatus.PLACEHOLDER_CONFIGURED,
    ) -> CredentialRecord:
        created_at = ACTIVATION_TIMESTAMP
        encrypted_secret = self.encryptor.encrypt(secret_marker, credential_id=credential_id)
        record = CredentialRecord(
            credential_id=credential_id,
            logical_name=logical_name,
            drive_id=drive_id,
            role=role,
            provider=provider,
            scope=scope,
            credential_type=credential_type,
            status=status,
            encrypted_secret=encrypted_secret,
            secret_hash=self.encryptor.fingerprint(secret_marker),
            masked_secret="***",
            created_at=created_at,
            updated_at=created_at,
            last_used_at=created_at,
            last_success_at=created_at,
            last_failure_at="never",
            last_connection_test=created_at,
            last_upload_test=created_at,
            last_download_test=created_at,
            last_healthcheck=created_at,
            expires_at=self.rotation_policy.expiration_at(created_at),
            rotation_due_at=self.rotation_policy.rotation_due_at(created_at),
            rotation_interval_days=self.rotation_policy.rotation_interval_days,
            notes="placeholder-only",
        )
        record.history.append({"timestamp": created_at, "event": "registered", "status": status})
        self.provider.put_record(record)
        self.audit_logger.record("credential-registered", credential_id=credential_id, details=record.as_reference().as_dict())
        return record

    def register_drive(
        self,
        *,
        drive_id: str,
        logical_name: str,
        role: str,
        provider: str = "google-drive",
        scope: str = CredentialScope.GOOGLE_DRIVE,
        credential_type: str = CredentialType.GOOGLE_DRIVE_OAUTH2,
        status: str = CredentialStatus.PLACEHOLDER_CONFIGURED,
    ) -> CredentialRecord:
        credential_id = f"cred-{drive_id}"
        secret_marker = f"vault://{credential_id}/placeholder"
        return self.register(
            credential_id=credential_id,
            logical_name=logical_name,
            drive_id=drive_id,
            role=role,
            secret_marker=secret_marker,
            provider=provider,
            scope=scope,
            credential_type=credential_type,
            status=status,
        )

    def list_records(self) -> list[CredentialRecord]:
        return self.provider.list_records()

    def record_for(self, credential_id: str) -> CredentialRecord:
        return self.provider.get_record(credential_id)

    def reference_for(self, credential_id: str) -> CredentialReference:
        return self.record_for(credential_id).as_reference()

    def decrypt_secret(self, credential_id: str) -> str:
        record = self.record_for(credential_id)
        secret = self.encryptor.decrypt(record.encrypted_secret, credential_id=credential_id)
        record.last_used_at = _utc_now()
        record.last_success_at = record.last_used_at
        record.history.append({"timestamp": record.last_used_at, "event": "decrypted"})
        return secret

    def touch_connection_test(self, credential_id: str, *, success: bool = True) -> CredentialRecord:
        record = self.record_for(credential_id)
        timestamp = _utc_now()
        record.last_connection_test = timestamp
        record.last_healthcheck = timestamp
        record.last_used_at = timestamp
        if success:
            record.last_success_at = timestamp
            record.status = CredentialStatus.PLACEHOLDER_CONFIGURED if record.status == CredentialStatus.PLACEHOLDER_CONFIGURED else CredentialStatus.ACTIVE
        else:
            record.last_failure_at = timestamp
            record.status = CredentialStatus.INVALID
        record.updated_at = timestamp
        record.history.append({"timestamp": timestamp, "event": "connection-test", "success": success})
        self.provider.put_record(record)
        self.audit_logger.record("credential-connection-test", credential_id=credential_id, details={"success": success})
        return record

    def touch_upload_test(self, credential_id: str, *, success: bool = True) -> CredentialRecord:
        record = self.record_for(credential_id)
        timestamp = _utc_now()
        record.last_upload_test = timestamp
        record.last_used_at = timestamp
        if success:
            record.last_success_at = timestamp
        else:
            record.last_failure_at = timestamp
        record.updated_at = timestamp
        record.history.append({"timestamp": timestamp, "event": "upload-test", "success": success})
        self.provider.put_record(record)
        self.audit_logger.record("credential-upload-test", credential_id=credential_id, details={"success": success})
        return record

    def touch_download_test(self, credential_id: str, *, success: bool = True) -> CredentialRecord:
        record = self.record_for(credential_id)
        timestamp = _utc_now()
        record.last_download_test = timestamp
        record.last_used_at = timestamp
        if success:
            record.last_success_at = timestamp
        else:
            record.last_failure_at = timestamp
        record.updated_at = timestamp
        record.history.append({"timestamp": timestamp, "event": "download-test", "success": success})
        self.provider.put_record(record)
        self.audit_logger.record("credential-download-test", credential_id=credential_id, details={"success": success})
        return record

    def touch_healthcheck(self, credential_id: str, *, success: bool = True) -> CredentialRecord:
        record = self.record_for(credential_id)
        timestamp = _utc_now()
        record.last_healthcheck = timestamp
        record.last_used_at = timestamp
        if success:
            record.last_success_at = timestamp
        else:
            record.last_failure_at = timestamp
            record.status = CredentialStatus.INVALID
        record.updated_at = timestamp
        record.history.append({"timestamp": timestamp, "event": "healthcheck", "success": success})
        self.provider.put_record(record)
        self.audit_logger.record("credential-healthcheck", credential_id=credential_id, details={"success": success})
        return record

    def rotate(self, credential_id: str, *, secret: str | None = None) -> CredentialRecord:
        return self.rotation_manager.rotate(self, credential_id, secret=secret)

    def revoke(self, credential_id: str) -> CredentialRecord:
        record = self.record_for(credential_id)
        timestamp = _utc_now()
        record.status = CredentialStatus.REVOKED
        record.revoked_at = timestamp
        record.updated_at = timestamp
        record.history.append({"timestamp": timestamp, "event": "revoked"})
        self.provider.put_record(record)
        self.audit_logger.record("credential-revoked", credential_id=credential_id)
        return record

    def disable(self, credential_id: str) -> CredentialRecord:
        record = self.record_for(credential_id)
        timestamp = _utc_now()
        record.status = CredentialStatus.DISABLED
        record.disabled_at = timestamp
        record.updated_at = timestamp
        record.history.append({"timestamp": timestamp, "event": "disabled"})
        self.provider.put_record(record)
        self.audit_logger.record("credential-disabled", credential_id=credential_id)
        return record

    def scan(self) -> list[str]:
        findings: list[str] = []
        for record in self.list_records():
            findings.extend(self.validator.validate_record(record))
        return findings

    def active_records(self) -> list[CredentialRecord]:
        return [record for record in self.list_records() if record.status in CredentialStatus.active_states()]

    def expired_records(self) -> list[CredentialRecord]:
        return [record for record in self.list_records() if record.is_expired()]

    def invalid_records(self) -> list[CredentialRecord]:
        return [record for record in self.list_records() if record.status == CredentialStatus.INVALID]

    def rotation_due_records(self) -> list[CredentialRecord]:
        return [record for record in self.list_records() if self.rotation_policy.is_rotation_due(record)]

    def monitoring_snapshot(self) -> dict[str, Any]:
        records = self.list_records()
        active = self.active_records()
        expired = self.expired_records()
        invalid = self.invalid_records()
        rotation_due = self.rotation_due_records()
        last_access = max((record.last_used_at for record in records if record.last_used_at != "never"), default="never")
        last_success = max((record.last_success_at for record in records if record.last_success_at != "never"), default="never")
        last_failure = max((record.last_failure_at for record in records if record.last_failure_at != "never"), default="never")
        alerts = []
        alerts.extend(f"{record.credential_id} expired" for record in expired)
        alerts.extend(f"{record.credential_id} invalid" for record in invalid)
        alerts.extend(f"{record.credential_id} rotation due" for record in rotation_due if record not in expired and record not in invalid)
        return {
            "vault": self.name,
            "status": self.status,
            "recordCount": len(records),
            "activeCredentials": len(active),
            "expiredCredentials": len(expired),
            "invalidCredentials": len(invalid),
            "rotationDueCredentials": len(rotation_due),
            "lastAccess": last_access,
            "lastSuccess": last_success,
            "lastFailure": last_failure,
            "alerts": alerts,
            "audit": self.audit_logger.snapshot(),
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "vault": self.name,
            "status": self.status,
            "summary": {
                "record_count": len(self.list_records()),
                "active_count": len(self.active_records()),
                "expired_count": len(self.expired_records()),
                "invalid_count": len(self.invalid_records()),
                "rotation_due_count": len(self.rotation_due_records()),
            },
            "records": [record.as_dict(masked=True) for record in self.list_records()],
            "monitoring": self.monitoring_snapshot(),
            "audit": self.audit_logger.snapshot(),
        }


_DEFAULT_CREDENTIAL_SPECS: tuple[dict[str, str], ...] = (
    {"drive_id": "drive-1", "logical_name": "videos-a", "role": "Videos A"},
    {"drive_id": "drive-2", "logical_name": "videos-b", "role": "Videos B"},
    {"drive_id": "drive-3", "logical_name": "photos-audio", "role": "Photos + Audio"},
    {"drive_id": "drive-4", "logical_name": "documents", "role": "Documents"},
    {"drive_id": "drive-5", "logical_name": "conversation-registry", "role": "Conversation Registry"},
    {"drive_id": "drive-6", "logical_name": "exports-reports-stats", "role": "Exports"},
    {"drive_id": "drive-7", "logical_name": "application-backups", "role": "Backups"},
    {"drive_id": "drive-8", "logical_name": "replication-overflow", "role": "Overflow"},
    {"drive_id": "drive-9", "logical_name": "strategic-reserve", "role": "Reserve"},
    {"drive_id": "drive-10", "logical_name": "maintenance-migration", "role": "Maintenance"},
)


def _build_credential_specs(resource_specs: Sequence[Any] | None = None) -> list[dict[str, str]]:
    specs = list(resource_specs or _DEFAULT_CREDENTIAL_SPECS)
    result: list[dict[str, str]] = []
    for spec in specs:
        result.append(
            {
                "drive_id": str(_field_value(spec, "drive_id")),
                "logical_name": str(_field_value(spec, "logical_name", _field_value(spec, "drive_id"))),
                "role": str(_field_value(spec, "role", _field_value(spec, "logical_name", _field_value(spec, "drive_id")))),
            }
        )
    return result


def build_default_credential_vault(resource_specs: Sequence[Any] | None = None) -> CredentialVault:
    vault = CredentialVault()
    for spec in _build_credential_specs(resource_specs):
        vault.register_drive(
            drive_id=spec["drive_id"],
            logical_name=spec["logical_name"],
            role=spec["role"],
        )
    return vault


def build_default_credential_records(resource_specs: Sequence[Any] | None = None) -> list[CredentialRecord]:
    return build_default_credential_vault(resource_specs).list_records()


__all__ = [
    "ACTIVATION_TIMESTAMP",
    "AuditTrail",
    "CredentialAuditLogger",
    "CredentialEncryptor",
    "CredentialMasker",
    "CredentialProvider",
    "CredentialRecord",
    "CredentialReference",
    "CredentialRotationManager",
    "CredentialRotationPolicy",
    "CredentialScanner",
    "CredentialScope",
    "CredentialStatus",
    "CredentialType",
    "CredentialValidator",
    "CredentialVault",
    "GitSecretGuard",
    "LogMasker",
    "SecretScanner",
    "build_default_credential_records",
    "build_default_credential_vault",
]
