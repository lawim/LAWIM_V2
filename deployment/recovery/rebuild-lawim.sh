#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

DRY_RUN="${DRY_RUN:-0}"
LAWIM_ROOT="${LAWIM_ROOT:-/opt/lawim/current}"
LAWIM_RELEASES_ROOT="${LAWIM_RELEASES_ROOT:-/opt/lawim/releases}"
LAWIM_MEDIA_STORAGE_PATH="${LAWIM_MEDIA_STORAGE_PATH:-/opt/lawim/shared/media}"
LAWIM_ENV_FILE="${LAWIM_ENV_FILE:-}"
LAWIM_GIT_REMOTE="${LAWIM_GIT_REMOTE:-}"
LAWIM_RECOVERY_BUNDLE_ROOT="${LAWIM_RECOVERY_BUNDLE_ROOT:-/var/lib/lawim-backup/recovery-bundles}"
LAWIM_RECOVERY_BUNDLE="${LAWIM_RECOVERY_BUNDLE:-}"
LAWIM_HEALTH_URL="${LAWIM_HEALTH_URL:-https://127.0.0.1/health}"
LAWIM_POSTGRES_SERVICE="${LAWIM_POSTGRES_SERVICE:-postgres}"
COMPOSE_FILE="${LAWIM_COMPOSE_FILE:-$LAWIM_ROOT/deployment/compose/docker-compose.prod.yml}"
SECRETS_DIR="${LAWIM_SECRETS_DIR:-}"

log() {
  printf '[rebuild-lawim] %s\n' "$*"
}

die() {
  printf '[rebuild-lawim] ERROR: %s\n' "$*" >&2
  exit 1
}

run_cmd() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: $*"
    return 0
  fi
  "$@"
}

run_shell() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: $*"
    return 0
  fi
  bash -lc "$*"
}

require_root() {
  if [[ "$DRY_RUN" == "1" ]]; then
    return 0
  fi
  if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
    die "run this script as root or use DRY_RUN=1 for a rehearsal"
  fi
}

manifest_value() {
  local manifest_path="$1"
  local key="$2"
  python3 - "$manifest_path" "$key" <<'PY'
import json
import sys

manifest_path = sys.argv[1]
key = sys.argv[2]

with open(manifest_path, "r", encoding="utf-8") as handle:
    payload = json.load(handle)

value = payload.get(key, "")
if value is None:
    print("")
elif isinstance(value, (dict, list)):
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
else:
    print(value)
PY
}

latest_bundle_dir() {
  if [[ -n "$LAWIM_RECOVERY_BUNDLE" ]]; then
    printf '%s\n' "$LAWIM_RECOVERY_BUNDLE"
    return 0
  fi

  if [[ ! -d "$LAWIM_RECOVERY_BUNDLE_ROOT" ]]; then
    return 0
  fi

  find "$LAWIM_RECOVERY_BUNDLE_ROOT" -mindepth 1 -maxdepth 1 -type d -name 'LAWIM-DRF-*' | sort | tail -n 1
}

load_bundle() {
  BUNDLE_DIR="$(latest_bundle_dir)"
  if [[ -z "${BUNDLE_DIR:-}" || ! -d "$BUNDLE_DIR" ]]; then
    die "recovery bundle not found; set LAWIM_RECOVERY_BUNDLE or populate $LAWIM_RECOVERY_BUNDLE_ROOT"
  fi
  [[ -f "$BUNDLE_DIR/manifest.json" ]] || die "missing manifest.json in $BUNDLE_DIR"
  [[ -f "$BUNDLE_DIR/database/postgresql.dump.sql" ]] || die "missing database dump in $BUNDLE_DIR"
  [[ -f "$BUNDLE_DIR/inventories/secret-inventory.json" ]] || die "missing secret inventory in $BUNDLE_DIR"
  log "selected recovery bundle: $BUNDLE_DIR"
}

install_dependencies() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: dependency installation skipped"
    return 0
  fi

  if ! command -v apt-get >/dev/null 2>&1; then
    log "apt-get not available; skipping package installation"
    return 0
  fi

  export DEBIAN_FRONTEND=noninteractive
  apt-get update
  apt-get install -y git curl rsync python3 postgresql-client docker.io docker-compose-plugin
}

restore_repository() {
  local target_sha
  local target_branch
  local release_name
  local release_dir
  target_sha="$(manifest_value "$BUNDLE_DIR/manifest.json" git_sha)"
  target_branch="$(manifest_value "$BUNDLE_DIR/manifest.json" branch)"
  release_name="${target_sha:0:8}"
  if [[ -z "$release_name" || "$release_name" == "unavailable" ]]; then
    release_name="$(basename "$BUNDLE_DIR")"
  fi
  release_dir="$LAWIM_RELEASES_ROOT/$release_name"

  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: repository restore prepared for $release_dir"
    log "dry-run: current symlink will point to $LAWIM_ROOT"
    return 0
  fi

  mkdir -p "$LAWIM_RELEASES_ROOT"

  if [[ -d "$release_dir/.git" ]]; then
    run_cmd git -C "$release_dir" fetch --all --tags
  else
    [[ -n "$LAWIM_GIT_REMOTE" ]] || LAWIM_GIT_REMOTE="$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || true)"
    [[ -n "$LAWIM_GIT_REMOTE" ]] || die "LAWIM_GIT_REMOTE is required to clone the repository"
    if [[ -e "$release_dir" ]]; then
      if [[ -n "$(find "$release_dir" -mindepth 1 -maxdepth 1 -print -quit)" ]]; then
        die "release directory already exists and is not a git repository: $release_dir"
      fi
    fi
    run_cmd git clone "$LAWIM_GIT_REMOTE" "$release_dir"
  fi

  if [[ -n "$target_sha" && "$target_sha" != "unavailable" ]]; then
    run_cmd git -C "$release_dir" checkout "$target_sha"
  elif [[ -n "$target_branch" && "$target_branch" != "unavailable" ]]; then
    run_cmd git -C "$release_dir" checkout "$target_branch"
  fi

  mkdir -p "$(dirname "$LAWIM_ROOT")"
  run_cmd ln -sfnT "$release_dir" "$LAWIM_ROOT"
}

restore_secrets() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: secret restore prepared"
    return 0
  fi

  if [[ -n "$SECRETS_DIR" && -d "$SECRETS_DIR" ]]; then
    mkdir -p /etc/lawim
    run_cmd rsync -a "$SECRETS_DIR"/ /etc/lawim/
  fi

  local candidate
  for candidate in "$LAWIM_ENV_FILE" /etc/lawim/backup.env /etc/lawim/.env.production /etc/lawim/.env; do
    if [[ -n "$candidate" && -f "$candidate" ]]; then
      set -a
      # shellcheck disable=SC1090
      source "$candidate"
      set +a
      log "loaded environment from $candidate"
      break
    fi
  done
}

restore_system_configuration() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: system configuration restore prepared"
    return 0
  fi

  if [[ -d "$BUNDLE_DIR/config/systemd" ]]; then
    mkdir -p /etc/systemd/system
    run_cmd rsync -a "$BUNDLE_DIR/config/systemd"/ /etc/systemd/system/
    run_cmd systemctl daemon-reload
  fi

  if [[ -d "$BUNDLE_DIR/config/nginx" ]]; then
    mkdir -p /etc/nginx
    run_cmd rsync -a "$BUNDLE_DIR/config/nginx"/ /etc/nginx/
  fi

  if [[ -d "$BUNDLE_DIR/config/backup" ]]; then
    mkdir -p /etc/lawim/backup
    run_cmd rsync -a "$BUNDLE_DIR/config/backup"/ /etc/lawim/backup/
  fi
}

restore_database() {
  local dump_path="$BUNDLE_DIR/database/postgresql.dump.sql"
  local database_url="${DATABASE_URL:-${LAWIM_DATABASE_URL:-}}"

  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: database restore prepared from $dump_path"
    return 0
  fi

  if [[ ! -f "$dump_path" ]]; then
    die "database dump missing: $dump_path"
  fi

  if [[ -n "$database_url" ]]; then
    run_cmd psql "$database_url" -f "$dump_path"
    return 0
  fi

  if command -v docker >/dev/null 2>&1 && [[ -f "$COMPOSE_FILE" ]]; then
    run_shell "cd \"$LAWIM_ROOT\" && docker compose -f \"$COMPOSE_FILE\" up -d \"$LAWIM_POSTGRES_SERVICE\" && for attempt in 1 2 3 4 5 6 7 8 9 10 11 12; do if docker compose -f \"$COMPOSE_FILE\" exec -T \"$LAWIM_POSTGRES_SERVICE\" pg_isready -U lawim -d lawim >/dev/null 2>&1; then break; fi; sleep 2; done && docker compose -f \"$COMPOSE_FILE\" exec -T \"$LAWIM_POSTGRES_SERVICE\" pg_isready -U lawim -d lawim >/dev/null 2>&1 && docker compose -f \"$COMPOSE_FILE\" exec -T \"$LAWIM_POSTGRES_SERVICE\" psql -U lawim -d lawim < \"$dump_path\""
    return 0
  fi

  die "DATABASE_URL or LAWIM_DATABASE_URL is required when Docker Compose restore is unavailable"
}

restore_media() {
  local target_media_dir="$LAWIM_MEDIA_STORAGE_PATH"
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: media restore prepared for $target_media_dir"
    return 0
  fi

  mkdir -p "$target_media_dir"
  if [[ -d "$BUNDLE_DIR/media" ]]; then
    run_cmd rsync -a "$BUNDLE_DIR/media"/ "$target_media_dir"/
  fi
}

launch_lawim() {
  local compose_path="$LAWIM_ROOT/deployment/compose/docker-compose.prod.yml"
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: stack launch prepared with $compose_path"
    return 0
  fi

  [[ -f "$compose_path" ]] || die "compose file not found: $compose_path"
  run_shell "cd \"$LAWIM_ROOT\" && docker compose -f \"$COMPOSE_FILE\" up -d --build"
}

verify_recovery() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log "dry-run: recovery verification prepared"
    return 0
  fi

  run_cmd curl -kfsS "$LAWIM_HEALTH_URL" >/dev/null
}

main() {
  local arg_bundle=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --bundle)
        arg_bundle="${2:-}"
        shift 2
        ;;
      --dry-run)
        DRY_RUN=1
        shift
        ;;
      --help|-h)
        cat <<'EOF'
Usage: rebuild-lawim.sh [--bundle PATH] [--dry-run]

Environment variables:
  LAWIM_ROOT
  LAWIM_GIT_REMOTE
  LAWIM_RECOVERY_BUNDLE
  LAWIM_RECOVERY_BUNDLE_ROOT
  LAWIM_SECRETS_DIR
  LAWIM_ENV_FILE
  LAWIM_DATABASE_URL
  LAWIM_HEALTH_URL
EOF
        return 0
        ;;
      *)
        die "unknown argument: $1"
        ;;
    esac
  done

  if [[ -n "$arg_bundle" ]]; then
    LAWIM_RECOVERY_BUNDLE="$arg_bundle"
  fi

  require_root
  install_dependencies
  load_bundle
  restore_repository
  restore_secrets
  restore_system_configuration
  restore_database
  restore_media
  launch_lawim
  verify_recovery

  log "LAWIM recovery completed from bundle $BUNDLE_DIR"
}

main "$@"
