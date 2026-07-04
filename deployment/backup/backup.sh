#!/usr/bin/env bash
set -euo pipefail
BACKUP_ROOT="${BACKUP_ROOT:-/var/backups/lawim}"
STAMP="$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_ROOT"
printf 'Backup package dry-run prepared at %s\n' "$BACKUP_ROOT/$STAMP"
