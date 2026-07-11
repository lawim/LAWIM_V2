# Retention

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

Retention must be provider-specific and must never delete the only validated restore point.

## Target policy

- Local disk: recent replications for 48 hours
- Google Drive: multiple daily backups for 7 days, then daily/weekly/monthly retention bands
- External disk: 8 to 12 weekly backups, and monthly copies if capacity allows

## Deletion rules

Deletion is allowed only when:

1. a newer validated copy exists;
2. at least one other destination is available;
3. integrity has been verified;
4. the minimum retention floor is respected;
5. no legal or administrative hold applies.

## Current state

- The repository contains older retention summaries, but no single canonical retention policy yet.
- The canonical policy is documented here and linked from the operational docs.

