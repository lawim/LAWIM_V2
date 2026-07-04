#!/usr/bin/env bash
set -euo pipefail
LOG_DIR="${LOG_DIR:-/var/log/lawim}"
mkdir -p "$LOG_DIR"
mkdir -p /opt/lawim/releases /opt/lawim/shared /srv/lawim
printf 'Prepared LAWIM server directories.\n'