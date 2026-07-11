#!/usr/bin/env bash
# LAWIM V2 — Start Local Development Environment
set -euo pipefail

cd "$(dirname "$0")/../.."

echo "=== Building LAWIM V2 Local Environment ==="

# Build frontend if needed
if [ ! -d "frontend/dist" ]; then
    echo "Building frontend..."
    (cd frontend && npm run build)
fi

# Start Docker environment
echo "Starting Docker services..."
docker compose -f compose/docker-compose.base.yml -f compose/docker-compose.postgres.yml up -d 2>&1

echo "Waiting for services..."
for i in $(seq 1 15); do
    if curl -s http://localhost:3000/api/health >/dev/null 2>&1; then
        echo "✓ LAWIM backend is ready at http://localhost:3000"
        echo "✓ Frontend served at http://localhost:3000 (or via vite dev server)"
        echo "  Run: cd frontend && npm run dev  (for hot reload)"
        exit 0
    fi
    sleep 2
done

echo "Backend may still be starting. Check: docker compose logs app"
