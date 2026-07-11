#!/usr/bin/env bash
# Temporary compatibility wrapper.
# Remove after 2026-08-31 once all callers use deployment/backup/ directly.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/../backup/restore.sh" "$@"
