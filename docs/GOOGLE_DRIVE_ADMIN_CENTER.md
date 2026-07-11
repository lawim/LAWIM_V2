# STATUT : ARCHIVE HISTORIQUE
# NON APPLICABLE A LA VERSION ACTUELLE
#
# Documentation active :
# `backup-disaster-recovery/cockpit.md`

# Google Drive Admin Center

The Google Drive Admin Center is the operational dashboard for the 10 Drive model used by LAWIM_V2.

## Route

- `/admin/google-drive-admin-center`

## Displays

- Ten logical Drives
- Capacity and free space
- State and health
- OAuth state
- API version
- Last control
- Last access
- Last upload
- Last download
- Last incident
- Alert posture
- Routing hints
- Automatic folders
- Monitoring metrics

## Data sources

- `Storage Resource Registry`
- `Google Drive Connector`
- `Google Drive Monitoring`
- `Storage Routing Policy`

## Operational summary

- Drive 1 and Drive 2 are reserved for video
- Drive 3 is reserved for photo and audio
- Drive 5 is reserved for conversation archives
- Drive 7 is reserved for application backups
- Drive 8 remains the overflow target
- Drive 9 remains the strategic reserve
- Drive 10 remains the maintenance target
