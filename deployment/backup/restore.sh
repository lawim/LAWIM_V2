#!/usr/bin/env bash
set -euo pipefail
RESTORE_ROOT="${RESTORE_ROOT:-${LAWIM_RESTORE_ROOT:-$HOME/.lawim-restores}}"
mkdir -p "$RESTORE_ROOT"
printf 'Restore rehearsal prepared in %s. No data is modified automatically.\n' "$RESTORE_ROOT"