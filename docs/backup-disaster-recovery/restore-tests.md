# Restore Tests

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Test ladder

- Daily: checksum, readability, manifest presence, remote presence
- Weekly: isolated PostgreSQL restore
- Monthly: full restore in isolated environment
- Quarterly: full disaster recovery exercise

## Test rules

- Use a real backup stored remotely or on the external disk for weekly and monthly tests.
- Do not test only the local cache.
- Record the outcome in the Cockpit or the designated report.

