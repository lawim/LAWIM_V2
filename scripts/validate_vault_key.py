import os
import sys

VAULT_KEY = os.environ.get("LAWIM_VAULT_KEY", "")
PLACEHOLDER = "lawim-credential-vault-placeholder"

if not VAULT_KEY:
    print("MISSING - LAWIM_VAULT_KEY is not set")
    sys.exit(1)

if VAULT_KEY == PLACEHOLDER:
    print("PLACEHOLDER_FORBIDDEN - LAWIM_VAULT_KEY uses the insecure placeholder")
    sys.exit(1)

if len(VAULT_KEY) < 32:
    print("INVALID_LENGTH - LAWIM_VAULT_KEY is too short (minimum 32 characters)")
    sys.exit(1)

print(f"PRESENT - LAWIM_VAULT_KEY is set ({len(VAULT_KEY)} chars)")
sys.exit(0)
