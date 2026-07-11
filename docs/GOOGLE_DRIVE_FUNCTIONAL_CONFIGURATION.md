# STATUT : ARCHIVE HISTORIQUE
# NON APPLICABLE A LA VERSION ACTUELLE
#
# Documentation active :
# `backup-disaster-recovery/google-drive.md`

# Google Drive Functional Configuration

This document defines the placeholder configuration model used by the Storage Resource Registry.

## Model

Each Drive entry includes:

- `drive_id`
- `logical_name`
- `email_placeholder`
- `provider`
- `category`
- `quota`
- `used`
- `available`
- `credential_status`
- `test_status`

## Placeholder policy

- The email is a logical placeholder only, for example `drive-1@placeholder.lawim.invalid`
- No URL is stored in the registry
- No real Google secret is stored in the repository
- No refresh token is stored in the repository
- No client secret is stored in the repository

## Drive assignment

- Drive 1: Videos A
- Drive 2: Videos B
- Drive 3: Photos + Audio
- Drive 4: Documents
- Drive 5: Conversation Registry
- Drive 6: Exports / reports / statistics
- Drive 7: Application backups
- Drive 8: Replication / overflow
- Drive 9: Strategic reserve
- Drive 10: Maintenance / migration

## Configuration status

- `credential_status`: placeholder until the secure assistant phase
- `test_status`: activation validation result
- `provider`: `google-drive`
- `quota`: `13 GB` theoretical per Drive

## Notes

- Business data continues to reference `MediaID` and `ConversationID`
- Google Drive is resolved through the storage registry and not embedded in records
- This configuration is ready for the secure onboarding of the real ten Google Drive accounts
