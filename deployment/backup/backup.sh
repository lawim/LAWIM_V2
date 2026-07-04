#!/usr/bin/env bash
set -euo pipefail
BACKUP_ROOT="${BACKUP_ROOT:-${LAWIM_BACKUP_ROOT:-$HOME/.lawim-backups}}"
STAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_DIR="$BACKUP_ROOT/$STAMP"
mkdir -p "$BACKUP_DIR"
cat > "$BACKUP_DIR/manifest.txt" <<EOF
LAWIM backup rehearsal
Timestamp: $STAMP
Mode: dry-run
Target: $BACKUP_DIR
EOF
printf 'Backup package dry-run prepared at %s\n' "$BACKUP_DIR"
