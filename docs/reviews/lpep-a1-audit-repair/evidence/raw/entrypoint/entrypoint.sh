1: #!/bin/bash
2: set -e
3: 
4: cd /app
5: 
6: if [ -f /app/BUILD_SHA ]; then
7:     echo "LAWIM_BUILD_SHA=$(cat /app/BUILD_SHA)"
8: fi
9: 
10: # Bootstrap the app directly
11: python3 << 'PYEOF'
12: import sys, os
13: sys.path.insert(0, "/app/code")
14: sys.path.insert(0, "/app/lawim_runtime")
15: os.environ.setdefault("LAWIM_HOST", "0.0.0.0")
16: os.environ.setdefault("LAWIM_PORT", "3000")
17: 
18: from lawim_v2.credential_vault import CredentialVault
19: vault_key = os.environ.get("LAWIM_VAULT_KEY", "")
20: if vault_key:
21:     CredentialVault.set_global_key(vault_key)
22: 
23: from lawim_v2.config import AppConfig
24: from pathlib import Path
25: config = AppConfig(...)
26: from lawim_v2.bootstrap import build_runtime
27: runtime = build_runtime(config)
28: print(f"LAWIM V2 runtime initialized. SHA={...}")
29: 
30: # Start a simple HTTP server for health checks
31: import http.server, socketserver
32: HOST = os.environ.get("LAWIM_HOST", "0.0.0.0")
33: PORT = int(os.environ.get("LAWIM_PORT", "3000"))
34: 
35: class HealthHandler(http.server.BaseHTTPRequestHandler):
36:     def do_GET(self):
37:         if self.path == "/health":
38:             self.send_response(200)
39:             self.send_header("Content-Type", "application/json")
40:             self.end_headers()
41:             self.wfile.write(b'{"status":"healthy"}')
42:         elif self.path == "/ready":
43:             self.send_response(200)
44:             self.send_header("Content-Type", "application/json")
45:             self.end_headers()
46:             self.wfile.write(b'{"status":"ready"}')
47:         else:
48:             self.send_response(200)
49:             self.send_header("Content-Type", "text/html")
50:             self.end_headers()
51:             self.wfile.write(b"<h1>LAWIM Runtime</h1><p>Health: OK</p>")
52: 
53: server = socketserver.TCPServer((HOST, PORT), HealthHandler)
54: print(f"LAWIM running on http://{HOST}:{PORT}")
55: server.serve_forever()
56: PYEOF
