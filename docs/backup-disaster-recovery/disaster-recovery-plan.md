# Disaster Recovery Plan

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Purpose

This plan defines the operator response for major loss scenarios and the source of restoration for each case.

| Scenario | Severity | First action | Restore source | Return criteria | Evidence | Communication | Target delay |
|---|---|---|---|---|---|---|---|
| PostgreSQL loss | Critical | Stop write activity and isolate the issue | Latest validated DB backup | Schema and key queries pass | Logs, manifest, checksum | Ops notice | < 2h |
| Media loss | High | Freeze writes to the affected area | Local disk or external disk | File counts and permissions match | File list, checksum | Internal notice | < 30m for files |
| Partial corruption | High | Isolate artifact, keep evidence | Alternate validated copy | Recheck succeeds | Manifest, checksum | Ops notice | < 2h |
| Full server loss | Critical | Declare incident and provision new server | Google Drive or external disk | Full stack validated | Recovery report | Leadership notice | < 8h |
| Google account compromise | Critical | Suspend remote sync and rotate access | Local or external copy | Account and storage secured | Security record | Security notice | ASAP |
| Local disk loss | High | Continue with off-site sources | Google Drive or external disk | Alternate destination verified | Alert log | Ops notice | < 8h |
| External disk loss | Medium | Keep Google Drive as primary off-site source | Google Drive | Remote copy verified | Rotation log | Ops notice | < 24h |
| Key loss | Critical | Stop encrypted restores and escalate | Key escrow or approved backup key source | Key recovered and tested | Secret audit | Security notice | ASAP |
| Ransomware | Critical | Disconnect external media and isolate host | Historical clean backup | Clean rebuild tested | Incident timeline | Leadership notice | < 8h |
| Human error | High | Stop destructive action and preserve state | Latest validated backup | Recovery validated | Change log | Ops notice | < 2h |
| Prolonged network outage | High | Keep local and external copies alive | Local or external disk | Remote sync recovers later | Network evidence | Ops notice | scenario-based |

