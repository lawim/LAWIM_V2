# Deployment History

## 2026-07-08 - Mission 08.1 validation and PostgreSQL runtime fix

- commit: `29eb91c16e88c23e04cc992a82a9001892bd7dc0`
- tag: `mission-08-dashboard-i18n-matching`
- bundle: `lawim-v2-postgresql-compat.tar.gz`
- checksum: `05aed8ab224f70026bfabf333b68545dad463db1118f2d6569e1eafbf4b4adb9`
- operator: `Codex`
- result: runtime deployed, app/postgres/redis healthy, login validation passed for admin/agent/owner, dashboard and multilingue checks passed
- rollback: available through `/opt/lawim/releases/` and the pre-start backup

## 2026-07-05 - Gate 2B controlled OVH deployment

- commit: `bc46a68664f166d7f079f8dcd48f4e954581fcea`
- tag: `pre-ovh-final`
- bundle: `lawim_v2_ovh_bc46a686.tar`
- checksum: `7644e58bfa80414309b54c38d724cc75b7ced93d8748b6f5b18e95e45cf8b7f2`
- operator: `Codex`
- result: runtime deployed, health endpoints validated, backup captured, login flow rechecked after PostgreSQL adapter fix
- incident: initial session insert path on PostgreSQL used an unsafe `RETURNING id` fallback for `sessions`
- rollback: available through `/opt/lawim/releases/` and the pre-start backup

Future deployments should append one entry per release and keep the checksum chain intact.
