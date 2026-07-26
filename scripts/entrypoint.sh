#!/bin/bash
set -e

cd /app

if [ -f /app/BUILD_SHA ]; then
    echo "LAWIM_BUILD_SHA=$(cat /app/BUILD_SHA)"
fi

# Bootstrap the app directly
python3 << 'PYEOF'
import sys, os
sys.path.insert(0, "/app/code")
sys.path.insert(0, "/app/lawim_runtime")
os.environ.setdefault("LAWIM_HOST", "0.0.0.0")
os.environ.setdefault("LAWIM_PORT", "3000")

from lawim_v2.credential_vault import CredentialVault
vault_key = os.environ.get("LAWIM_VAULT_KEY", "")
if vault_key:
    CredentialVault.set_global_key(vault_key)

from lawim_v2.config import AppConfig
from pathlib import Path
config = AppConfig(
    host=os.environ.get("LAWIM_HOST", "0.0.0.0"),
    port=int(os.environ.get("LAWIM_PORT", "3000")),
    db_path=Path(os.environ.get("LAWIM_DB_PATH", "/app/data/runtime/lawim.sqlite3")),
    db_driver=os.environ.get("LAWIM_DB_DRIVER", "sqlite"),
    database_url=os.environ.get("DATABASE_URL", ""),
    db_fallback=True,
    app_env=os.environ.get("APP_ENV", "production"),
    stack_profile=os.environ.get("LAWIM_STACK_PROFILE", "standard"),
    log_level=os.environ.get("LOG_LEVEL", "info"),
    public_base_url=os.environ.get("PUBLIC_BASE_URL", "https://api.lawim.app"),
    secret_provider=os.environ.get("LAWIM_SECRET_PROVIDER", "env"),
    seed_demo_data=os.environ.get("LAWIM_SEED_DEMO_DATA", "true").lower() == "true",
    session_ttl_seconds=int(os.environ.get("SESSION_TTL_SECONDS", "86400")),
    media_storage_path=Path(os.environ.get("LAWIM_MEDIA_PATH", "/app/data/runtime/media")),
)
from lawim_v2.bootstrap import build_runtime
runtime = build_runtime(config)
runtime.start()

# Start a simple HTTP server for health checks
import http.server, socketserver
HOST = os.environ.get("LAWIM_HOST", "0.0.0.0")
PORT = int(os.environ.get("LAWIM_PORT", "3000"))

class HealthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"healthy"}')
        elif self.path == "/ready":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"ready"}')
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>LAWIM Runtime</h1><p>Health: OK</p>")

server = socketserver.TCPServer((HOST, PORT), HealthHandler)
print(f"LAWIM running on http://{HOST}:{PORT}")
server.serve_forever()
PYEOF
