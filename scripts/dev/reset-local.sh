#!/usr/bin/env bash
# LAWIM V2 — Reset Local Development Environment
set -euo pipefail

cd "$(dirname "$0")/../.."
echo "=== Resetting LAWIM V2 Local Environment ==="

# Stop containers and remove volumes
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml down -v

# Clean runtime data
rm -rf data/runtime

echo "✓ Reset complete. Run start-local.sh to recreate."
