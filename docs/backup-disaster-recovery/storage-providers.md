# Storage Providers

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

All backup destinations implement the same provider contract so that the backup core does not know whether it talks to Google Drive, a local disk, an external disk, or a future cloud provider.

## Common contract

- initialize()
- isAvailable()
- store()
- retrieve()
- verify()
- delete()
- list()
- getFreeSpace()
- health()

## Provider rules

- The core service must never know Google Drive internals.
- The provider layer must never know PostgreSQL semantics.
- Each provider must expose its own availability and integrity checks.
- A failed provider must not block the other providers.

## Current state

| Provider | Target | Implemented | Deployed | Tested | Validated |
|---|---|---|---|---|---|
| Google Drive | Yes | Partial concept only | No confirmed live deployment | No | No |
| Local disk | Yes | Not yet | No | No | No |
| External disk | Yes | Not yet | No | No | No |
| Future S3/Azure/NAS | Yes | Not yet | No | No | No |

## Related references

- `google-drive.md`
- `local-disk.md`
- `external-disk.md`
- `architecture.md`

