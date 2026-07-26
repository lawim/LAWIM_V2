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

from lawim_v2.bootstrap import build_runtime, ApplicationRuntime
from lawim_v2.config import AppConfig
config = AppConfig()
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
