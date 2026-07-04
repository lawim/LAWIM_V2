# Conversation Archiving

Conversation archives are structured as a versioned JSON payload with:

- participants
- messages
- events
- media_ids
- audit trail

The archive manager produces mock-safe manifests with checksums and a stable version tag for future OVH cold-storage migration.
