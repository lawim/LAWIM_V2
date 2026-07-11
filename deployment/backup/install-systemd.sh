#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<'EOF'
Usage:
  install-systemd.sh install
  install-systemd.sh rollback <backup-dir>

The install mode backs up the current LAWIM backup units, installs the
versioned units from deployment/systemd, verifies them, reloads systemd, and
enables the validated timers.
EOF
}

require_root() {
    if [[ "${EUID:-$(id -u)}" -ne 0 ]]; then
        printf 'This script must be run as root.\n' >&2
        exit 1
    fi
}

script_dir() {
    cd "$(dirname "${BASH_SOURCE[0]}")" && pwd
}

repo_root() {
    cd "$(script_dir)/../.." && pwd
}

backup_existing_units() {
    local backup_dir="$1"
    local unit_dir="$2"
    local unit
    mkdir -p "$backup_dir"
    for unit in "$unit_dir"/lawim-*.service "$unit_dir"/lawim-*.timer; do
        [[ -e "$unit" ]] || continue
        cp -a "$unit" "$backup_dir/"
    done
}

install_unit() {
    local source_dir="$1"
    local unit_dir="$2"
    local unit="$3"
    if [[ -f "$source_dir/$unit" ]]; then
        install -Dm0644 "$source_dir/$unit" "$unit_dir/$unit"
        INSTALLED_UNITS+=("$unit_dir/$unit")
    fi
}

verify_units() {
    if ((${#INSTALLED_UNITS[@]})); then
        systemd-analyze verify "${INSTALLED_UNITS[@]}"
    fi
}

enable_base_timer() {
    systemctl daemon-reload
    systemctl enable --now lawim-backup.timer
}

enable_optional_timer() {
    local unit_dir="$1"
    local service_name="$2"
    local timer_name="$3"
    local flag_name="$4"
    local flag_value="${!flag_name:-0}"
    if [[ "$flag_value" == "1" && -f "$unit_dir/$service_name" && -f "$unit_dir/$timer_name" ]]; then
        systemctl enable --now "$timer_name"
        OPTIONAL_TIMERS+=("$timer_name")
    fi
}

show_status() {
    systemctl list-timers --all | grep -i 'lawim' || true
}

rollback_units() {
    local backup_dir="$1"
    local unit_dir="$2"
    if [[ ! -d "$backup_dir" ]]; then
        printf 'Rollback directory not found: %s\n' "$backup_dir" >&2
        exit 1
    fi
    systemctl disable --now lawim-backup.timer || true
    systemctl disable --now lawim-local-replication.timer || true
    systemctl disable --now lawim-external-backup.timer || true
    systemctl disable --now lawim-restore-test.timer || true
    rm -f "$unit_dir"/lawim-*.service "$unit_dir"/lawim-*.timer
    cp -a "$backup_dir"/lawim-*.service "$unit_dir/" 2>/dev/null || true
    cp -a "$backup_dir"/lawim-*.timer "$unit_dir/" 2>/dev/null || true
    systemctl daemon-reload
}

main() {
    local mode="${1:-install}"
    require_root

    local repo
    repo="$(repo_root)"
    local source_dir="$repo/deployment/systemd"
    local unit_dir="${UNIT_TARGET_DIR:-/etc/systemd/system}"
    local backup_root="${BACKUP_ROOT:-/var/backups/lawim/systemd}"
    local stamp
    stamp="$(date +%Y%m%d%H%M%S)"
    local backup_dir="${2:-$backup_root/$stamp}"

    INSTALLED_UNITS=()
    OPTIONAL_TIMERS=()

    case "$mode" in
        install)
            backup_existing_units "$backup_dir" "$unit_dir"
            install_unit "$source_dir" "$unit_dir" "lawim-backup.service"
            install_unit "$source_dir" "$unit_dir" "lawim-backup.timer"
            install_unit "$source_dir" "$unit_dir" "lawim-local-replication.service"
            install_unit "$source_dir" "$unit_dir" "lawim-local-replication.timer"
            install_unit "$source_dir" "$unit_dir" "lawim-external-backup.service"
            install_unit "$source_dir" "$unit_dir" "lawim-external-backup.timer"
            install_unit "$source_dir" "$unit_dir" "lawim-restore-test.service"
            install_unit "$source_dir" "$unit_dir" "lawim-restore-test.timer"
            verify_units
            enable_base_timer
            enable_optional_timer "$unit_dir" "lawim-local-replication.service" "lawim-local-replication.timer" "ENABLE_LOCAL_REPLICATION"
            enable_optional_timer "$unit_dir" "lawim-external-backup.service" "lawim-external-backup.timer" "ENABLE_EXTERNAL_BACKUP"
            enable_optional_timer "$unit_dir" "lawim-restore-test.service" "lawim-restore-test.timer" "ENABLE_RESTORE_TEST"
            printf 'Backup units installed. Previous units saved in %s\n' "$backup_dir"
            show_status
            ;;
        rollback)
            if [[ $# -lt 2 ]]; then
                usage
                exit 1
            fi
            rollback_units "$2" "$unit_dir"
            printf 'Rollback completed from %s\n' "$2"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"
