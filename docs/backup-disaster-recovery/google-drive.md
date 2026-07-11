# Google Drive

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Role

Google Drive is the off-site destination for complete backups.
It is used only through the provider contract and through rclone-based transfer logic.

## Required checks

- connectivity
- OAuth state
- quota
- upload
- download
- checksum
- manifest verification

## Security rules

- Never store access tokens in Git.
- Never store refresh tokens in Git.
- Never store client secrets in Git.
- Never expose `rclone.conf` contents in the documentation.

## Current state

| Aspect | Target | Implemented | Deployed | Tested | Validated |
|---|---|---|---|---|---|
| rclone remote | Yes | Example config only | Not confirmed | No | No |
| Upload verification | Yes | Partial concept | No | No | No |
| Checksum recheck | Yes | Partial concept | No | No | No |
| Manifest validation | Yes | Partial concept | No | No | No |
| OAuth lifecycle | Yes | Placeholder docs only | No | No | No |

## Repository references

- `deployment/backup/rclone.example.conf`
- `storage-providers.md`
- `monitoring-alerts.md`

## Legacy references

The following historical documents were collapsed into this canonical page:

- `docs/GOOGLE_DRIVE_CONNECTOR.md`
- `docs/GOOGLE_DRIVE_SETUP.md`
- `docs/GOOGLE_DRIVE_OAUTH.md`
- `docs/GOOGLE_DRIVE_ADMIN_CENTER.md`
- `docs/GOOGLE_DRIVE_DISTRIBUTED_STORAGE.md`
- `docs/GOOGLE_DRIVE_MONITORING.md`
- `docs/GOOGLE_DRIVE_QUOTA_POLICY.md`
- `docs/GOOGLE_DRIVE_FUNCTIONAL_CONFIGURATION.md`

