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
- `deployment/backup/backup.sh`
- `storage-providers.md`
- `monitoring-alerts.md`
