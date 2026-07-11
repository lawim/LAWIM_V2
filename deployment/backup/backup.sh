#!/usr/bin/env bash
set -euo pipefail
BACKUP_ROOT="${BACKUP_ROOT:-${LAWIM_BACKUP_ROOT:-/var/backups/lawim}}"
BACKUP_ID="${BACKUP_ID:-LAWIM-$(date +%Y%m%d-%H%M%S)}"
BACKUP_DIR="$BACKUP_ROOT/$BACKUP_ID"
mkdir -p "$BACKUP_DIR"
cat > "$BACKUP_DIR/manifest.txt" <<EOF
LAWIM backup rehearsal
Backup-ID: $BACKUP_ID
Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
Mode: dry-run
Target: $BACKUP_DIR
EOF
printf 'Backup package dry-run prepared at %s\n' "$BACKUP_DIR"
