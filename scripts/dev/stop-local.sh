#!/usr/bin/env bash
# LAWIM V2 — Stop Local Development Environment
set -euo pipefail

cd "$(dirname "$0")/../.."
echo "Stopping LAWIM V2..."
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml down
echo "✓ Stopped"
