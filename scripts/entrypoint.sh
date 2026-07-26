#!/bin/bash
set -e

cd /app

if [ -f /app/BUILD_SHA ]; then
    echo "LAWIM_BUILD_SHA=$(cat /app/BUILD_SHA)"
fi

exec python3 -m uvicorn lawim_v2.main:app --host 0.0.0.0 --port 3000
