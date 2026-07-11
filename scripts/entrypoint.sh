#!/usr/bin/env bash
set -e

# Ensure runtime directories exist with correct permissions
# The lawim user runs the app but Docker volumes are often root-owned
mkdir -p /app/data/runtime/media /app/data/runtime/snapshots
chown -R lawim:lawim /app/data/runtime

exec python -m lawim_v2 "$@"
