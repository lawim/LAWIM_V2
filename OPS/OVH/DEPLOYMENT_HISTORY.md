# Deployment History

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
