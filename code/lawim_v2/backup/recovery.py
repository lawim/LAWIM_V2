from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
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
        for index, name in os.if_nameindex():
            interfaces.append({"index": index, "name": name})
    except OSError:
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
    duration_seconds: float = 0.0
    validated_at: str = field(default_factory=utc_now)

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
        self.bundle_root.mkdir(parents=True, exist_ok=True)

    def bundle_path(self, bundle_id: str) -> Path:
        return self.bundle_root / bundle_id

    def manifest_path(self, bundle_id: str) -> Path:
        return self.bundle_path(bundle_id) / "manifest.json"

    def checklist_path(self, bundle_id: str) -> Path:
        return self.bundle_path(bundle_id) / "documents" / "RECOVERY_CHECKLIST.md"

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
            ).as_dict()

        started = time.perf_counter()
        manifest = self._read_manifest(target_id)
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
            duration_seconds=round(time.perf_counter() - started, 3),
        ).as_dict()

    def status(self) -> dict[str, object]:
        latest = self.latest_bundle()
        validation = self.validate_bundle((latest or {}).get("bundle_id") if latest else None) if latest else None
        backup_status = self.backup.status()
        git_state = _git_state(self.repo_root)
        versions = _command_versions()
        return {
            "bundle_root": str(self.bundle_root),
            "latest_bundle": latest,
            "validation": validation,
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
