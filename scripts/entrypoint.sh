#!/usr/bin/env sh
set -eu

echo "LAWIM_BUILD_SHA=${LAWIM_BUILD_SHA:-unknown}"

# Validate critical imports before starting the full application
python3 - <<'PY'
import sys
sys.path.insert(0, "/app/code")
sys.path.insert(0, "/app/lawim_runtime")

from lawim_v2.credential_vault import CredentialVault
vault_key = __import__("os").environ.get("LAWIM_VAULT_KEY", "")
if vault_key:
    CredentialVault.set_global_key(vault_key)

program_f_enabled = __import__("os").environ.get("PROGRAM_F_ENABLED", "true").strip().lower() in {"1", "true", "yes", "on"}
if program_f_enabled:
    import importlib
    for mod_name in ("lawim_runtime.conversation.journey",):
        try:
            importlib.import_module(mod_name)
            print(f"IMPORT_PASS:{mod_name}")
        except ImportError as exc:
            print(f"IMPORT_FAIL:{mod_name}:{exc}")
            raise SystemExit(1)
    from lawim_v2.conversation.program_f_adapter import ProgramFEngineAdapter
    print("IMPORT_PASS:lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter")
else:
    print("PROGRAM_F_DISABLED:by feature flag")
PY

exec python -m lawim_v2
