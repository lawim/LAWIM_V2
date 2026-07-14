from __future__ import annotations

import io
import hashlib
import json
import os
import platform
import re
import socket
import shutil
import subprocess
import sys
import time
import zipfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol, TYPE_CHECKING

from .. import __version__ as LAWIM_VERSION
from ..config import AppConfig

if TYPE_CHECKING:
    from ..db import LawimRepository


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_recovery_bundle_id(prefix: str = "LAWIM-DRF") -> str:
    return f"{prefix}-{datetime.now(timezone.utc):%Y%m%d-%H%M%S}"


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [_jsonable(item) for item in value]
    if isinstance(value, set):
        return sorted(_jsonable(item) for item in value)
    return value


def _as_str(value: object, default: str = "") -> str:
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _safe_run(command: list[str], *, cwd: Path | None = None, timeout: int = 10) -> str:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except (FileNotFoundError, subprocess.SubprocessError, OSError):
        return "unavailable"
    output = (result.stdout or result.stderr or "").strip()
    if result.returncode != 0 and not output:
        return "unavailable"
    return output or "unavailable"


def _git(cwd: Path, *args: str) -> str:
    return _safe_run(["git", *args], cwd=cwd, timeout=10)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_checksum(files: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for item in sorted(files, key=lambda entry: str(entry.get("relative_path", ""))):
        digest.update(str(item.get("relative_path", "")).encode("utf-8"))
        digest.update(str(item.get("sha256", "")).encode("utf-8"))
        digest.update(str(item.get("size_bytes", 0)).encode("utf-8"))
    return digest.hexdigest()


def _is_text_file(path: Path) -> bool:
    text_extensions = {
        ".md",
        ".txt",
        ".sh",
        ".conf",
        ".yml",
        ".yaml",
        ".json",
        ".py",
        ".ts",
        ".js",
        ".mjs",
        ".cjs",
        ".ini",
        ".service",
        ".timer",
        ".example",
        ".template",
    }
    return path.suffix.lower() in text_extensions or path.name.startswith(".env")


def _copy_file(source: Path, target: Path, *, bundle_dir: Path) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return {
        "relative_path": str(target.relative_to(bundle_dir)),
        "source_path": str(source),
        "size_bytes": target.stat().st_size,
        "sha256": _sha256(target),
        "kind": "file",
    }


def _copy_text_file(source: Path, target: Path, *, bundle_dir: Path, redact_env: bool = False) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    text = source.read_text(encoding="utf-8")
    if redact_env and source.name.startswith(".env"):
        lines: list[str] = []
        for raw_line in text.splitlines():
            if "=" not in raw_line or raw_line.strip().startswith("#"):
                lines.append(raw_line)
                continue
            key, _ = raw_line.split("=", 1)
            lines.append(f"{key}=***REDACTED***")
        text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    target.write_text(text, encoding="utf-8")
    return {
        "relative_path": str(target.relative_to(bundle_dir)),
        "source_path": str(source),
        "size_bytes": target.stat().st_size,
        "sha256": _sha256(target),
        "kind": "file",
    }


def _copy_tree(source_root: Path, target_root: Path, *, bundle_dir: Path, glob_pattern: str | None = None) -> list[dict[str, Any]]:
    if not source_root.exists():
        return []
    entries: list[dict[str, Any]] = []
    if source_root.is_file():
        if _is_text_file(source_root):
            entries.append(_copy_text_file(source_root, target_root / source_root.name, bundle_dir=bundle_dir))
        else:
            entries.append(_copy_file(source_root, target_root / source_root.name, bundle_dir=bundle_dir))
        return entries
    files = sorted(source_root.rglob(glob_pattern or "*")) if glob_pattern else sorted(source_root.rglob("*"))
    for source in files:
        if not source.is_file():
            continue
        relative = source.relative_to(source_root)
        destination = target_root / relative
        if _is_text_file(source):
            entries.append(_copy_text_file(source, destination, bundle_dir=bundle_dir))
        else:
            entries.append(_copy_file(source, destination, bundle_dir=bundle_dir))
    return entries


def _read_optional_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _database_dump_from_sqlite(repository: LawimRepository) -> str:
    connection = getattr(repository, "connection", None)
    if connection is None:
        return "-- database dump unavailable\n"
    try:
        lines = list(connection.iterdump())
    except Exception:
        return "-- database dump unavailable\n"
    if not lines:
        return "-- database dump empty\n"
    header = [
        "-- LAWIM recovery bundle database dump",
        "-- Source engine: sqlite compatibility dump",
        f"-- Generated at: {utc_now()}",
        "",
    ]
    return "\n".join(header + lines) + "\n"


def _command_versions() -> dict[str, str]:
    return {
        "python": sys.version.split()[0],
        "docker": _safe_run(["docker", "--version"]),
        "docker_compose": _safe_run(["docker", "compose", "version", "--short"]),
        "postgresql": _safe_run(["psql", "--version"]),
        "node": _safe_run(["node", "--version"]),
        "npm": _safe_run(["npm", "--version"]),
        "git": _safe_run(["git", "--version"]),
        "systemd": _safe_run(["systemctl", "--version"]),
        "kernel": platform.release(),
    }


def _hardware_inventory() -> dict[str, Any]:
    cpu_count = os.cpu_count() or 0
    memory_total = 0
    meminfo = Path("/proc/meminfo")
    if meminfo.is_file():
        for line in meminfo.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("MemTotal:"):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        memory_total = int(parts[1]) * 1024
                    except ValueError:
                        memory_total = 0
                break
    filesystems: list[dict[str, Any]] = []
    try:
        mounts = Path("/proc/mounts").read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        mounts = []
    for line in mounts:
        parts = line.split()
        if len(parts) < 3:
            continue
        device, mount_point, fs_type = parts[:3]
        try:
            usage = shutil.disk_usage(mount_point)
            free_bytes = usage.free
            total_bytes = usage.total
        except OSError:
            free_bytes = 0
            total_bytes = 0
        filesystems.append(
            {
                "device": device,
                "mount_point": mount_point,
                "type": fs_type,
                "free_bytes": free_bytes,
                "total_bytes": total_bytes,
            }
        )
    interfaces = []
    try:
        for index, name in socket.if_nameindex():
            interfaces.append({"index": index, "name": name})
    except (AttributeError, OSError):
        interfaces = []
    disks = []
    lsblk = _safe_run(["lsblk", "-J", "-o", "NAME,SIZE,TYPE,UUID,MOUNTPOINT"], timeout=10)
    if lsblk not in {"", "unavailable"}:
        try:
            payload = json.loads(lsblk)
            for device in payload.get("blockdevices", []) if isinstance(payload, dict) else []:
                if isinstance(device, dict):
                    disks.append(device)
        except json.JSONDecodeError:
            disks = []
    return {
        "cpu": {
            "count": cpu_count,
            "architecture": platform.machine(),
            "model": platform.processor() or "unknown",
        },
        "ram": {
            "total_bytes": memory_total,
        },
        "disks": disks,
        "filesystems": filesystems,
        "free_space_bytes": sum(item["free_bytes"] for item in filesystems),
        "uuid": _safe_run(["cat", "/etc/machine-id"], timeout=5) or "unavailable",
        "network_interfaces": interfaces,
    }


def _software_inventory() -> dict[str, Any]:
    return {
        "docker": _safe_run(["docker", "--version"]),
        "postgresql": _safe_run(["psql", "--version"]),
        "python": sys.version.split()[0],
        "node": _safe_run(["node", "--version"]),
        "npm": _safe_run(["npm", "--version"]),
        "git": _safe_run(["git", "--version"]),
        "systemd": _safe_run(["systemctl", "--version"]),
        "kernel": platform.release(),
    }


def _docker_lines(command: list[str]) -> list[dict[str, Any]]:
    output = _safe_run(command, timeout=20)
    if output in {"", "unavailable"}:
        return []
    rows: list[dict[str, Any]] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            rows.append({"value": line})
            continue
        if isinstance(payload, dict):
            rows.append(payload)
        else:
            rows.append({"value": payload})
    return rows


def _docker_inventory() -> dict[str, Any]:
    return {
        "version": _safe_run(["docker", "--version"]),
        "compose_version": _safe_run(["docker", "compose", "version", "--short"]),
        "images": _docker_lines(["docker", "image", "ls", "--format", "{{json .}}"]),
        "volumes": _docker_lines(["docker", "volume", "ls", "--format", "{{json .}}"]),
        "networks": _docker_lines(["docker", "network", "ls", "--format", "{{json .}}"]),
        "containers": _docker_lines(["docker", "ps", "-a", "--format", "{{json .}}"]),
    }


def _git_state(repo_root: Path) -> dict[str, Any]:
    sha = _git(repo_root, "rev-parse", "HEAD")
    branch = _git(repo_root, "branch", "--show-current")
    remote = _git(repo_root, "remote", "get-url", "origin")
    tags_output = _git(repo_root, "tag", "--points-at", "HEAD")
    tags = [line.strip() for line in tags_output.splitlines() if line.strip() and line.strip() != "unavailable"]
    describe = _git(repo_root, "describe", "--tags", "--always", "--dirty")
    status = _git(repo_root, "status", "--short")
    return {
        "remote": remote,
        "branch": branch,
        "sha": sha,
        "tags": tags,
        "tag": tags[0] if tags else "",
        "status": status,
        "version": describe,
        "is_clean": status == "",
    }


def _secret_inventory(config: AppConfig, repo_root: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    env_sources = [
        ("LAWIM_ADMIN_PASSWORD", "environment", True),
        ("LAWIM_DATABASE_URL", "environment", True),
        ("LAWIM_GEOCODING_API_KEY", "environment", False),
        ("LAWIM_CDN_BASE_URL", "environment", False),
        ("DATABASE_PASSWORD", "environment", True),
        ("REDIS_PASSWORD", "environment", True),
        ("JWT_SECRET", "environment", True),
        ("CAMPAY_API_KEY", "environment", False),
        ("SMTP_PASSWORD", "environment", False),
    ]
    for name, location, required in env_sources:
        entries.append(
            {
                "name": name,
                "type": "environment-variable",
                "location": location,
                "required": required,
                "present": bool(os.getenv(name, "").strip()),
            }
        )

    file_sources = [
        (repo_root / "deployment/environments/production/secrets.example", "production secrets example", True),
        (repo_root / "deployment/.env.example", "deployment env example", True),
        (repo_root / "deployment/.env.production.example", "production env example", True),
        (repo_root / "deployment/.env.production.template", "production env template", True),
    ]
    for path, label, required in file_sources:
        entries.append(
            {
                "name": path.name,
                "type": "secret-template",
                "location": label,
                "required": required,
                "present": path.is_file(),
            }
        )
    return entries


def _write_json_artifact(bundle_dir: Path, relative_path: str, payload: Any, *, kind: str) -> dict[str, Any]:
    target = bundle_dir / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
    return {
        "relative_path": str(target.relative_to(bundle_dir)),
        "source_path": "generated",
        "size_bytes": target.stat().st_size,
        "sha256": _sha256(target),
        "kind": kind,
    }


def _validation_check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "status": "pass" if passed else "fail",
        "detail": detail,
    }


def _score_signal(name: str, passed: bool, weight: int, detail: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": passed,
        "weight": max(0, int(weight)),
        "detail": detail,
    }


def _checklist_markdown(bundle_id: str, bundle_dir: Path) -> str:
    return (
        "# Recovery Checklist\n\n"
        f"Bundle: `{bundle_id}`\n"
        f"Location: `{bundle_dir}`\n\n"
        "1. Create the server.\n"
        "2. Install Docker and the required system packages.\n"
        "3. Retrieve LAWIM from Git.\n"
        "4. Restore the approved secrets.\n"
        "5. Restore PostgreSQL.\n"
        "6. Restore the media tree.\n"
        "7. Restore the operational configuration.\n"
        "8. Launch LAWIM.\n"
        "9. Run the validation checks.\n"
        "10. Confirm the system is ready for traffic.\n"
    )


class BackupSnapshotProvider(Protocol):
    def status(self) -> dict[str, object]: ...

    def configuration(self) -> dict[str, object]: ...

    def metrics(self) -> dict[str, object]: ...


@dataclass(slots=True)
class RecoveryBundleManifest:
    bundle_id: str
    created_at: str
    lawim_version: str
    git_sha: str
    branch: str
    tag: str
    environment: str
    postgresql_version: str
    docker_version: str
    docker_compose_version: str
    python_version: str
    checksum: str
    files: list[dict[str, Any]] = field(default_factory=list)
    size_bytes: int = 0
    duration_seconds: float = 0.0
    encryption_method: str = "none"
    database_engine: str = ""
    software_versions: dict[str, str] = field(default_factory=dict)
    bundle_root: str = ""
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        payload = _jsonable(asdict(self))
        payload["file_count"] = len(self.files)
        return payload


@dataclass(slots=True)
class RecoveryBundleSummary:
    bundle_id: str
    created_at: str
    size_bytes: int
    checksum: str
    file_count: int
    environment: str
    validation_state: str = "unknown"
    path: str = ""

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))


@dataclass(slots=True)
class RecoveryValidationResult:
    bundle_id: str
    manifest_present: bool
    checksum_valid: bool
    compatible: bool
    git_ok: bool
    docker_ok: bool
    postgresql_ok: bool
    restore_ready: bool
    missing_files: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: list[dict[str, Any]] = field(default_factory=list)
    duration_seconds: float = 0.0
    validated_at: str = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))


@dataclass(slots=True)
class RecoveryReadinessScore:
    score: int
    maximum_score: int = 100
    state: str = "UNKNOWN"
    bundle_id: str = ""
    bundle_age_days: float | None = None
    rpo_seconds: float = 0.0
    rto_seconds: float = 0.0
    signals: list[dict[str, Any]] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    calculated_at: str = field(default_factory=utc_now)

    def as_dict(self) -> dict[str, object]:
        return _jsonable(asdict(self))


class DisasterRecoveryService:
    def __init__(self, repository: Any, config: AppConfig, backup: BackupSnapshotProvider) -> None:
        self.repository = repository
        self.config = config
        self.backup = backup
        self.repo_root = Path(__file__).resolve().parents[3]
        backup_configuration = self.backup.configuration()
        state_root = Path(str(backup_configuration.get("state_root") or self.config.media_storage_path.parent))
        self.bundle_root = state_root / "recovery-bundles"

    def _safe_bundle_identifier(self, bundle_id: str) -> str:
        identifier = bundle_id.strip()
        if not identifier or not re.fullmatch(r"[A-Za-z0-9._-]+", identifier):
            raise ValueError(f"Invalid recovery bundle identifier: {bundle_id!r}")
        return identifier

    def bundle_path(self, bundle_id: str) -> Path:
        return self.bundle_root / self._safe_bundle_identifier(bundle_id)

    def manifest_path(self, bundle_id: str) -> Path:
        return self.bundle_path(bundle_id) / "manifest.json"

    def checklist_path(self, bundle_id: str) -> Path:
        return self.bundle_path(bundle_id) / "documents" / "RECOVERY_CHECKLIST.md"

    def archive_bundle(self, bundle_id: str) -> tuple[str, bytes]:
        bundle_dir = self.bundle_path(bundle_id)
        if not bundle_dir.is_dir():
            raise FileNotFoundError(f"Recovery bundle not found: {bundle_id}")
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
            for source in sorted(bundle_dir.rglob("*")):
                if source.is_file():
                    archive.write(source, arcname=str(source.relative_to(bundle_dir)))
        return f"{self._safe_bundle_identifier(bundle_id)}.zip", buffer.getvalue()

    def _copy_config_sources(self, bundle_dir: Path) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        config_dir = bundle_dir / "config"
        sources: list[tuple[Path, Path]] = [
            (self.repo_root / "Dockerfile", config_dir / "Dockerfile"),
            (self.repo_root / "deployment/compose/docker-compose.prod.yml", config_dir / "docker-compose.yml"),
            (self.repo_root / "deployment/compose/docker-compose.staging.yml", config_dir / "compose" / "docker-compose.staging.yml"),
            (self.repo_root / "deployment/compose/docker-compose.dev.yml", config_dir / "compose" / "docker-compose.dev.yml"),
            (self.repo_root / "deployment/backup/backup.sh", config_dir / "backup" / "backup.sh"),
            (self.repo_root / "deployment/backup/restore.sh", config_dir / "backup" / "restore.sh"),
            (self.repo_root / "deployment/backup/install-systemd.sh", config_dir / "backup" / "install-systemd.sh"),
            (self.repo_root / "deployment/backup/backup-policy.md", config_dir / "backup" / "backup-policy.md"),
            (self.repo_root / "deployment/backup/postgres-init.sql", config_dir / "backup" / "postgres-init.sql"),
            (self.repo_root / "deployment/backup/postgresql.conf", config_dir / "backup" / "postgresql.conf"),
            (self.repo_root / "deployment/backup/rclone.example.conf", config_dir / "backup" / "rclone.example.conf"),
            (self.repo_root / "deployment/scripts/backup.sh", config_dir / "scripts" / "backup.sh"),
            (self.repo_root / "deployment/scripts/restore.sh", config_dir / "scripts" / "restore.sh"),
            (self.repo_root / "deployment/scripts/deploy.sh", config_dir / "scripts" / "deploy.sh"),
            (self.repo_root / "deployment/nginx/nginx.conf", config_dir / "nginx" / "nginx.conf"),
            (self.repo_root / "deployment/systemd/lawim-backup.service", config_dir / "systemd" / "lawim-backup.service"),
            (self.repo_root / "deployment/systemd/lawim-backup.timer", config_dir / "systemd" / "lawim-backup.timer"),
            (self.repo_root / "deployment/server/scripts", config_dir / "server" / "scripts"),
            (self.repo_root / "deployment/checklists", config_dir / "checklists"),
            (self.repo_root / "deployment/runbook", config_dir / "runbook"),
            (self.repo_root / "deployment/validator", config_dir / "validator"),
            (self.repo_root / "deployment/orchestrator", config_dir / "orchestrator"),
            (self.repo_root / "deployment/health", config_dir / "health"),
            (self.repo_root / "deployment/environments/production", config_dir / "environments" / "production"),
            (self.repo_root / "OPS", config_dir / "OPS"),
        ]
        for source, target in sources:
            if source.is_file():
                if _is_text_file(source):
                    records.append(_copy_text_file(source, target, bundle_dir=bundle_dir))
                else:
                    records.append(_copy_file(source, target, bundle_dir=bundle_dir))
                continue
            if source.is_dir():
                records.extend(_copy_tree(source, target, bundle_dir=bundle_dir))
        extra_nginx = sorted((self.repo_root / "deployment/nginx/conf.d").glob("*.conf"))
        for source in extra_nginx:
            records.append(_copy_text_file(source, config_dir / "nginx" / "conf.d" / source.name, bundle_dir=bundle_dir))
        extra_dockerfiles = sorted((self.repo_root / "deployment/docker").glob("Dockerfile.*"))
        for source in extra_dockerfiles:
            records.append(_copy_text_file(source, config_dir / "docker" / source.name, bundle_dir=bundle_dir))
        extra_env = [
            self.repo_root / "deployment/.env.example",
            self.repo_root / "deployment/.env.production.example",
            self.repo_root / "deployment/.env.production.template",
        ]
        for source in extra_env:
            if source.is_file():
                records.append(_copy_text_file(source, config_dir / "env" / source.name, bundle_dir=bundle_dir))
        return records

    def _copy_media(self, bundle_dir: Path) -> list[dict[str, Any]]:
        media_root = self.config.media_storage_path
        target_root = bundle_dir / "media"
        if not media_root.exists():
            return []
        return _copy_tree(media_root, target_root, bundle_dir=bundle_dir)

    def _write_inventories(self, bundle_dir: Path) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        backup_status = self.backup.status()
        backup_configuration = self.backup.configuration()
        policy = backup_configuration.get("policy") if isinstance(backup_configuration, dict) else {}
        retention = policy.get("retention") if isinstance(policy, dict) else {}
        records.append(_write_json_artifact(bundle_dir, "inventories/software-inventory.json", _software_inventory(), kind="inventory"))
        records.append(_write_json_artifact(bundle_dir, "inventories/hardware-inventory.json", _hardware_inventory(), kind="inventory"))
        records.append(_write_json_artifact(bundle_dir, "inventories/docker-inventory.json", _docker_inventory(), kind="inventory"))
        records.append(_write_json_artifact(bundle_dir, "inventories/git-state.json", _git_state(self.repo_root), kind="inventory"))
        records.append(_write_json_artifact(bundle_dir, "inventories/secret-inventory.json", _secret_inventory(self.config, self.repo_root), kind="inventory"))

        backup_config_payload = {
            "identifier": _as_str(backup_configuration.get("identifier"), "current"),
            "enabled": bool(backup_configuration.get("enabled", True)),
            "timezone": _as_str(backup_configuration.get("timezone"), "Africa/Douala"),
            "backup_root": _as_str(backup_configuration.get("backup_root")),
            "state_root": _as_str(backup_configuration.get("state_root")),
            "logs_root": _as_str(backup_configuration.get("logs_root")),
            "temp_root": _as_str(backup_configuration.get("temp_root")),
            "retention": _jsonable(retention),
            "schedules": backup_configuration.get("schedules", []),
            "destinations": backup_status.get("destinations", []),
            "providers": backup_status.get("providers", []),
            "alerts_enabled": bool(backup_configuration.get("alerts_enabled", True)),
            "verify_after_upload": bool(backup_configuration.get("verify_after_upload", True)),
            "automated_restore_tests": bool(backup_configuration.get("automated_restore_tests", True)),
            "restore_isolation_required": bool(backup_configuration.get("restore_isolation_required", True)),
            "systemd": backup_configuration.get("systemd", {}),
            "version": backup_configuration.get("version", {}),
        }
        records.append(_write_json_artifact(bundle_dir, "inventories/backup-config.json", backup_config_payload, kind="inventory"))
        return records

    def _write_database_dump(self, bundle_dir: Path) -> dict[str, Any]:
        target = bundle_dir / "database" / "postgresql.dump.sql"
        target.parent.mkdir(parents=True, exist_ok=True)
        dump = _database_dump_from_sqlite(self.repository)
        target.write_text(dump, encoding="utf-8")
        return {
            "relative_path": str(target.relative_to(bundle_dir)),
            "source_path": str(self.repository.db_path),
            "size_bytes": target.stat().st_size,
            "sha256": _sha256(target),
            "kind": "database",
        }

    def _write_documents(self, bundle_dir: Path, bundle_id: str) -> list[dict[str, Any]]:
        documents_dir = bundle_dir / "documents"
        documents_dir.mkdir(parents=True, exist_ok=True)
        checklist = documents_dir / "RECOVERY_CHECKLIST.md"
        checklist.write_text(_checklist_markdown(bundle_id, bundle_dir), encoding="utf-8")
        summary = documents_dir / "RECOVERY_BUNDLE_SUMMARY.json"
        summary_payload = {
            "bundle_id": bundle_id,
            "created_at": utc_now(),
            "bundle_root": str(bundle_dir),
            "notes": "Generated by the DRF bundle generator.",
        }
        summary.write_text(json.dumps(summary_payload, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
        return [
            {
                "relative_path": str(checklist.relative_to(bundle_dir)),
                "source_path": "generated",
                "size_bytes": checklist.stat().st_size,
                "sha256": _sha256(checklist),
                "kind": "document",
            },
            {
                "relative_path": str(summary.relative_to(bundle_dir)),
                "source_path": "generated",
                "size_bytes": summary.stat().st_size,
                "sha256": _sha256(summary),
                "kind": "document",
            },
        ]

    def _build_bundle_manifest(
        self,
        *,
        bundle_id: str,
        bundle_dir: Path,
        file_records: list[dict[str, Any]],
        created_at: str,
        duration_seconds: float,
        warnings: list[str],
    ) -> RecoveryBundleManifest:
        versions = _command_versions()
        git_state = _git_state(self.repo_root)
        checksum = _tree_checksum(file_records)
        size_bytes = sum(int(item.get("size_bytes", 0)) for item in file_records)
        return RecoveryBundleManifest(
            bundle_id=bundle_id,
            created_at=created_at,
            lawim_version=LAWIM_VERSION,
            git_sha=git_state["sha"],
            branch=git_state["branch"],
            tag=git_state["tag"],
            environment=self.config.app_env,
            postgresql_version=versions["postgresql"],
            docker_version=versions["docker"],
            docker_compose_version=versions["docker_compose"],
            python_version=versions["python"],
            checksum=checksum,
            files=sorted(file_records, key=lambda item: str(item.get("relative_path", ""))),
            size_bytes=size_bytes,
            duration_seconds=duration_seconds,
            encryption_method="none",
            database_engine="sqlite-compatibility" if self.repository.driver == "sqlite" else self.repository.driver,
            software_versions=versions,
            bundle_root=str(bundle_dir),
            warnings=warnings,
        )

    def generate_bundle(self, *, bundle_id: str | None = None) -> dict[str, object]:
        resolved_id = bundle_id or build_recovery_bundle_id()
        bundle_dir = self.bundle_path(resolved_id)
        if bundle_dir.exists():
            shutil.rmtree(bundle_dir)
        bundle_dir.mkdir(parents=True, exist_ok=True)
        started = time.perf_counter()
        warnings: list[str] = []
        file_records: list[dict[str, Any]] = []

        status = self.backup.status()
        status_path = bundle_dir / "documents" / "BACKUP_STATUS.json"
        status_path.parent.mkdir(parents=True, exist_ok=True)
        status_path.write_text(json.dumps(status, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
        file_records.append(
            {
                "relative_path": str(status_path.relative_to(bundle_dir)),
                "source_path": "backup-status",
                "size_bytes": status_path.stat().st_size,
                "sha256": _sha256(status_path),
                "kind": "document",
            }
        )

        file_records.append(self._write_database_dump(bundle_dir))
        file_records.extend(self._copy_media(bundle_dir))
        file_records.extend(self._copy_config_sources(bundle_dir))
        file_records.extend(self._write_inventories(bundle_dir))
        file_records.extend(self._write_documents(bundle_dir, resolved_id))

        if not file_records:
            warnings.append("bundle generated without source files")

        created_at = utc_now()
        duration_seconds = round(time.perf_counter() - started, 3)
        manifest = self._build_bundle_manifest(
            bundle_id=resolved_id,
            bundle_dir=bundle_dir,
            file_records=file_records,
            created_at=created_at,
            duration_seconds=duration_seconds,
            warnings=warnings,
        )
        manifest_path = bundle_dir / "manifest.json"
        manifest_path.write_text(json.dumps(manifest.as_dict(), ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")

        file_records.append(
            {
                "relative_path": str(manifest_path.relative_to(bundle_dir)),
                "source_path": "generated",
                "size_bytes": manifest_path.stat().st_size,
                "sha256": _sha256(manifest_path),
                "kind": "manifest",
            }
        )
        manifest = self._build_bundle_manifest(
            bundle_id=resolved_id,
            bundle_dir=bundle_dir,
            file_records=[record for record in file_records if record["kind"] != "manifest"],
            created_at=created_at,
            duration_seconds=duration_seconds,
            warnings=warnings,
        )
        manifest_path.write_text(json.dumps(manifest.as_dict(), ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")

        return {
            "bundle": manifest.as_dict(),
            "bundle_path": str(bundle_dir),
            "manifest_path": str(manifest_path),
        }

    def _read_manifest(self, bundle_id: str) -> RecoveryBundleManifest | None:
        manifest_path = self.manifest_path(bundle_id)
        if not manifest_path.is_file():
            return None
        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(payload, dict):
            return None
        files = payload.get("files")
        if not isinstance(files, list):
            files = []
        return RecoveryBundleManifest(
            bundle_id=_as_str(payload.get("bundle_id"), bundle_id),
            created_at=_as_str(payload.get("created_at"), utc_now()),
            lawim_version=_as_str(payload.get("lawim_version"), LAWIM_VERSION),
            git_sha=_as_str(payload.get("git_sha")),
            branch=_as_str(payload.get("branch")),
            tag=_as_str(payload.get("tag")),
            environment=_as_str(payload.get("environment"), self.config.app_env),
            postgresql_version=_as_str(payload.get("postgresql_version")),
            docker_version=_as_str(payload.get("docker_version")),
            docker_compose_version=_as_str(payload.get("docker_compose_version")),
            python_version=_as_str(payload.get("python_version")),
            checksum=_as_str(payload.get("checksum")),
            files=[dict(item) for item in files if isinstance(item, dict)],
            size_bytes=int(payload.get("size_bytes") or 0),
            duration_seconds=float(payload.get("duration_seconds") or 0.0),
            encryption_method=_as_str(payload.get("encryption_method"), "none"),
            database_engine=_as_str(payload.get("database_engine")),
            software_versions=dict(payload.get("software_versions") or {}),
            bundle_root=_as_str(payload.get("bundle_root"), str(self.bundle_path(bundle_id))),
            warnings=[str(item) for item in payload.get("warnings") or [] if item is not None],
        )

    def _read_json_file(self, path: Path) -> Any | None:
        if not path.is_file():
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return payload

    def _recovery_test_report_path(self) -> Path:
        return self.bundle_root.parent / "recovery-tests" / "reports" / "latest-report.json"

    def _read_recovery_test_report(self) -> dict[str, Any] | None:
        payload = self._read_json_file(self._recovery_test_report_path())
        return payload if isinstance(payload, dict) else None

    def readiness_score(
        self,
        *,
        latest_bundle: dict[str, object] | None = None,
        validation: dict[str, object] | None = None,
        backup_status: dict[str, object] | None = None,
    ) -> dict[str, object]:
        latest = latest_bundle if latest_bundle is not None else self.latest_bundle()
        backup_snapshot = backup_status if backup_status is not None else self.backup.status()
        validation_snapshot = validation
        if validation_snapshot is None and latest is not None:
            validation_snapshot = self.validate_bundle(_as_str(latest.get("bundle_id")))

        score = 100
        signals: list[dict[str, Any]] = []
        reasons: list[str] = []

        def apply_signal(name: str, passed: bool, penalty: int, detail: str) -> None:
            nonlocal score
            signal = _score_signal(name, passed, penalty, detail)
            signals.append(signal)
            if not passed:
                score = max(0, score - max(0, int(penalty)))
                reasons.append(detail)

        bundle_id = _as_str((latest or {}).get("bundle_id"))
        bundle_path = self.bundle_path(bundle_id) if bundle_id else None
        bundle_age_days: float | None = None
        if latest is None:
            apply_signal("latest-bundle-present", False, 35, "No recovery bundle is available")
        else:
            apply_signal("latest-bundle-present", True, 0, f"Latest bundle {bundle_id} is available")
            created_at = _parse_datetime(_as_str(latest.get("created_at")))
            if created_at is None:
                apply_signal("bundle-freshness", False, 10, "Latest bundle timestamp is unreadable")
            else:
                bundle_age_days = max(0.0, (datetime.now(timezone.utc) - created_at).total_seconds() / 86_400)
                if bundle_age_days <= 7:
                    apply_signal("bundle-freshness", True, 0, f"Latest bundle age is {bundle_age_days:.1f} days")
                else:
                    penalty = min(20, max(1, round(bundle_age_days)))
                    apply_signal(
                        "bundle-freshness",
                        False,
                        penalty,
                        f"Latest bundle age is {bundle_age_days:.1f} days",
                    )

        if validation_snapshot is None:
            apply_signal("validation-available", False, 20, "No recovery validation snapshot is available")
        else:
            apply_signal("validation-available", True, 0, "Recovery validation snapshot is available")
            validation_checks = {
                "manifest_present": ("validation-manifest", 20, "manifest.json is missing"),
                "checksum_valid": ("validation-checksum", 15, "At least one bundle file checksum drifted"),
                "compatible": ("validation-compatibility", 10, "Bundle runtime compatibility failed"),
                "git_ok": ("validation-git", 10, "Git is not synchronized with the bundle"),
                "docker_ok": ("validation-docker", 5, "Docker is unavailable for recovery"),
                "postgresql_ok": ("validation-postgresql", 5, "PostgreSQL is unavailable for recovery"),
                "restore_ready": ("validation-restore-ready", 15, "Bundle is not ready to restore"),
            }
            for key, (signal_name, penalty, detail) in validation_checks.items():
                passed = bool(validation_snapshot.get(key))
                apply_signal(signal_name, passed, penalty, detail if not passed else f"{key.replace('_', ' ').title()} passed")

        secret_inventory: list[dict[str, Any]] = []
        if bundle_path is None:
            apply_signal("secret-inventory", False, 15, "Recovery bundle is unavailable")
        else:
            secret_inventory_payload = self._read_json_file(bundle_path / "inventories" / "secret-inventory.json")
            if not isinstance(secret_inventory_payload, list):
                apply_signal("secret-inventory", False, 15, "Secret inventory is missing or unreadable")
            else:
                secret_inventory = [entry for entry in secret_inventory_payload if isinstance(entry, dict)]
                required = [entry for entry in secret_inventory if bool(entry.get("required"))]
                missing_required = [str(entry.get("name") or "unknown") for entry in required if not bool(entry.get("present"))]
                if missing_required:
                    penalty = min(15, max(5, len(missing_required) * 5))
                    apply_signal(
                        "secret-coverage",
                        False,
                        penalty,
                        f"Missing required secrets: {', '.join(sorted(missing_required))}",
                    )
                else:
                    apply_signal("secret-coverage", True, 0, "All required secrets were inventoried")

        report_payload = self._read_recovery_test_report()
        if report_payload is None:
            apply_signal("isolated-recovery-test", False, 15, "No isolated recovery test report is available")
        else:
            report_status = _as_str(report_payload.get("status")).upper()
            report_exit_code = int(report_payload.get("exit_code") or 0)
            report_passed = report_status == "PASS" and report_exit_code == 0
            report_completed_at = _parse_datetime(_as_str(report_payload.get("completed_at")))
            report_age_days: float | None = None
            if report_completed_at is not None:
                report_age_days = max(0.0, (datetime.now(timezone.utc) - report_completed_at).total_seconds() / 86_400)
            if report_passed:
                penalty = 0
                if report_age_days is not None and report_age_days > 30:
                    penalty = 10
                apply_signal(
                    "isolated-recovery-test",
                    True,
                    penalty,
                    f"Latest isolated recovery test passed{'' if report_age_days is None else f' ({report_age_days:.1f} days old)'}",
                )
            else:
                penalty = 15
                if report_age_days is not None and report_age_days > 30:
                    penalty += 5
                apply_signal(
                    "isolated-recovery-test",
                    False,
                    penalty,
                    "Latest isolated recovery test did not pass",
                )

        destinations = backup_snapshot.get("destinations")
        if not isinstance(destinations, list):
            apply_signal("destination-health", False, 10, "Backup destinations are unavailable")
        else:
            destination_rows = [entry for entry in destinations if isinstance(entry, dict)]
            google_drive = next((entry for entry in destination_rows if str(entry.get("identifier")) == "google-drive"), None)
            external_disk = next((entry for entry in destination_rows if str(entry.get("identifier")) == "external-disk"), None)
            google_drive_ready = google_drive is not None and str(google_drive.get("state")) == "AVAILABLE"
            external_ready = external_disk is not None and str(external_disk.get("state")) == "AVAILABLE"
            apply_signal(
                "offsite-destination",
                google_drive_ready,
                10,
                "Google Drive destination is unavailable" if not google_drive_ready else "Google Drive destination is available",
            )
            apply_signal(
                "offline-destination",
                external_ready,
                5,
                "External disk destination is unavailable" if not external_ready else "External disk destination is available",
            )

        metrics = backup_snapshot.get("metrics") if isinstance(backup_snapshot, dict) else {}
        rpo_seconds = float(metrics.get("rpo_seconds") or 0) if isinstance(metrics, dict) else 0.0
        rto_seconds = float(metrics.get("rto_seconds") or 0) if isinstance(metrics, dict) else 0.0
        if rpo_seconds > 24 * 3600:
            apply_signal("rpo-target", False, 10, f"RPO is {rpo_seconds:.0f} seconds")
        else:
            apply_signal("rpo-target", True, 0, f"RPO is {rpo_seconds:.0f} seconds")
        if rto_seconds > 2 * 3600:
            apply_signal("rto-target", False, 10, f"RTO is {rto_seconds:.0f} seconds")
        else:
            apply_signal("rto-target", True, 0, f"RTO is {rto_seconds:.0f} seconds")

        state = "READY" if score >= 90 else "WATCH" if score >= 75 else "DEGRADED" if score >= 50 else "BLOCKED"
        return RecoveryReadinessScore(
            score=score,
            state=state,
            bundle_id=bundle_id,
            bundle_age_days=bundle_age_days,
            rpo_seconds=rpo_seconds,
            rto_seconds=rto_seconds,
            signals=signals,
            reasons=reasons,
        ).as_dict()

    def list_bundles(self, *, limit: int = 20) -> list[dict[str, object]]:
        if not self.bundle_root.is_dir():
            return []
        bundles: list[RecoveryBundleSummary] = []
        for manifest_path in sorted(self.bundle_root.glob("*/manifest.json"), reverse=True):
            bundle_id = manifest_path.parent.name
            manifest = self._read_manifest(bundle_id)
            if manifest is None:
                continue
            bundles.append(
                RecoveryBundleSummary(
                    bundle_id=manifest.bundle_id,
                    created_at=manifest.created_at,
                    size_bytes=manifest.size_bytes,
                    checksum=manifest.checksum,
                    file_count=len(manifest.files),
                    environment=manifest.environment,
                    validation_state="generated",
                    path=str(manifest_path.parent),
                )
            )
        return [bundle.as_dict() for bundle in bundles[:limit]]

    def latest_bundle(self) -> dict[str, object] | None:
        bundles = self.list_bundles(limit=1)
        return bundles[0] if bundles else None

    def validate_bundle(self, bundle_id: str | None = None) -> dict[str, object]:
        target_id = bundle_id or _as_str((self.latest_bundle() or {}).get("bundle_id"))
        if not target_id:
            return RecoveryValidationResult(
                bundle_id="",
                manifest_present=False,
                checksum_valid=False,
                compatible=False,
                git_ok=False,
                docker_ok=False,
                postgresql_ok=False,
                restore_ready=False,
                warnings=["no recovery bundle available"],
                checks=[_validation_check("manifest-present", False, "No recovery bundle is available")],
            ).as_dict()

        started = time.perf_counter()
        try:
            manifest = self._read_manifest(target_id)
        except ValueError as exc:
            return RecoveryValidationResult(
                bundle_id=target_id,
                manifest_present=False,
                checksum_valid=False,
                compatible=False,
                git_ok=False,
                docker_ok=False,
                postgresql_ok=False,
                restore_ready=False,
                missing_files=[target_id],
                warnings=[str(exc)],
                checks=[
                    _validation_check("manifest-present", False, str(exc)),
                    _validation_check("restore-ready", False, "Bundle identifier is invalid"),
                ],
                duration_seconds=round(time.perf_counter() - started, 3),
            ).as_dict()
        if manifest is None:
            return RecoveryValidationResult(
                bundle_id=target_id,
                manifest_present=False,
                checksum_valid=False,
                compatible=False,
                git_ok=False,
                docker_ok=False,
                postgresql_ok=False,
                restore_ready=False,
                missing_files=["manifest.json"],
                warnings=["manifest is missing or unreadable"],
                checks=[
                    _validation_check("manifest-present", False, "manifest.json is missing or unreadable"),
                    _validation_check("checksum-valid", False, "Bundle manifest could not be loaded"),
                    _validation_check("restore-ready", False, "Bundle cannot be restored without a manifest"),
                ],
                duration_seconds=round(time.perf_counter() - started, 3),
            ).as_dict()

        missing_files: list[str] = []
        checksum_valid = True
        for file_record in manifest.files:
            relative_path = str(file_record.get("relative_path") or "").strip()
            expected_sha = str(file_record.get("sha256") or "").strip()
            file_path = self.bundle_path(target_id) / relative_path
            if not file_path.is_file():
                missing_files.append(relative_path)
                checksum_valid = False
                continue
            if expected_sha and _sha256(file_path) != expected_sha:
                checksum_valid = False
        git_state = _git_state(self.repo_root)
        current_sha = str(git_state.get("sha") or "")
        compatibility = manifest.lawim_version == LAWIM_VERSION and manifest.git_sha not in {"", "unavailable"}
        docker_ok = "unavailable" not in {manifest.docker_version, manifest.docker_compose_version}
        postgresql_ok = manifest.postgresql_version != "unavailable"
        restore_ready = checksum_valid and not missing_files and compatibility
        checks = [
            _validation_check("manifest-present", True, "manifest.json was loaded successfully"),
            _validation_check(
                "bundle-integrity",
                not missing_files,
                "All bundle files are present" if not missing_files else f"Missing files: {', '.join(sorted(missing_files))}",
            ),
            _validation_check(
                "checksum-valid",
                checksum_valid,
                "All file checksums match the manifest" if checksum_valid else "At least one bundle file checksum drifted",
            ),
            _validation_check(
                "lawim-version-compatible",
                compatibility,
                f"Bundle LAWIM version {manifest.lawim_version or 'unknown'} vs runtime {LAWIM_VERSION}",
            ),
            _validation_check(
                "git-synced",
                manifest.git_sha not in {"", "unavailable"} and manifest.git_sha == current_sha,
                f"Bundle SHA {manifest.git_sha or 'unknown'} vs current SHA {current_sha or 'unknown'}",
            ),
            _validation_check(
                "docker-available",
                docker_ok,
                f"Docker {manifest.docker_version or 'unavailable'} / Compose {manifest.docker_compose_version or 'unavailable'}",
            ),
            _validation_check(
                "postgresql-available",
                postgresql_ok,
                f"PostgreSQL {manifest.postgresql_version or 'unavailable'}",
            ),
            _validation_check(
                "restore-ready",
                restore_ready,
                "Recovery bundle is ready to restore" if restore_ready else "Bundle validation failed",
            ),
        ]
        return RecoveryValidationResult(
            bundle_id=target_id,
            manifest_present=True,
            checksum_valid=checksum_valid,
            compatible=compatibility,
            git_ok=manifest.git_sha not in {"", "unavailable"} and manifest.git_sha == current_sha,
            docker_ok=docker_ok,
            postgresql_ok=postgresql_ok,
            restore_ready=restore_ready,
            missing_files=missing_files,
            warnings=manifest.warnings,
            checks=checks,
            duration_seconds=round(time.perf_counter() - started, 3),
        ).as_dict()

    def status(self) -> dict[str, object]:
        latest = self.latest_bundle()
        backup_status = self.backup.status()
        validation = self.validate_bundle((latest or {}).get("bundle_id") if latest else None) if latest else None
        readiness = self.readiness_score(latest_bundle=latest, validation=validation, backup_status=backup_status)
        git_state = _git_state(self.repo_root)
        versions = _command_versions()
        return {
            "bundle_root": str(self.bundle_root),
            "latest_bundle": latest,
            "validation": validation,
            "readiness": readiness,
            "git": git_state,
            "versions": versions,
            "backup": {
                "global_status": backup_status.get("global_status"),
                "last_backup": backup_status.get("last_backup"),
                "last_restore": backup_status.get("last_restore"),
                "metrics": backup_status.get("metrics"),
            },
            "checklist": _read_optional_text(self.checklist_path(str((latest or {}).get("bundle_id", "")))) if latest else None,
        }
