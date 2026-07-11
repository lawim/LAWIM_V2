# STATUT : ARCHIVE HISTORIQUE
# NON APPLICABLE A LA VERSION ACTUELLE
#
# Documentation active :
# `backup-disaster-recovery/google-drive.md`

# Google Drive Quota Policy

The storage registry uses a theoretical quota of `13 GB` per logical Google Drive.

## Thresholds

- `0-70%`: normal
- `70-85%`: attention
- `85-92%`: slowdown
- `>92%`: blocked

## Policy response

- Normal resources stay in the primary selection pool
- Attention resources remain selectable and are surfaced in alerts
- Slowdown resources are visible in the dashboard and can still serve fallback routing
- Blocked resources are skipped for large-file selection when a fallback exists

## Quota distribution

- Every Drive receives the same theoretical quota
- Used space and available space are tracked in the registry model
- The admin dashboard surfaces the current usage and alert posture

## Notes

- The quota policy is activation-ready
- No real Google Drive capacity is consumed by this repository
- The secure assistant phase will later bind the real accounts to these placeholders
