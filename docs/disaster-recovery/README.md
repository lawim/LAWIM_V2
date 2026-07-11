# Disaster Recovery Framework

This tree is the canonical documentation for the LAWIM_V2 Disaster Recovery
Framework shipped in Mission 13.2.

It describes the implemented recovery path, the generated bundle format, the
rebuild procedure, secret handling, validation checks, and operational
procedures.

## Contents

- [Architecture](architecture.md)
- [Recovery bundle](bundle.md)
- [Reconstruction](reconstruction.md)
- [Secrets](secrets.md)
- [Validation](validation.md)
- [Procedures](procedures.md)

## Implementation anchors

- [Bundle generator](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/backup/recovery.py)
- [Recovery API routes](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/server.py)
- [Rebuild script](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/deployment/recovery/rebuild-lawim.sh)
- [Monthly isolated recovery test](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/deployment/recovery/monthly-recovery-test.sh)
- [Cockpit tab](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/apps/admin/src/DisasterRecoveryPage.tsx)

## Scope

- No business feature is defined here.
- Secrets are never documented in cleartext.
- The DRF extends the existing backup architecture instead of replacing it.
- The Backup Orchestrator remains the operational base for backup activity.
