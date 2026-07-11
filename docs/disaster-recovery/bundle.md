# Recovery Bundle

Each Recovery Bundle is a reproducible reconstruction package.

## Required contents

- `manifest.json`
- `database/postgresql.dump.sql`
- `media/`
- `documents/`
- `config/`
- `inventories/software-inventory.json`
- `inventories/hardware-inventory.json`
- `inventories/docker-inventory.json`
- `inventories/git-state.json`
- `inventories/secret-inventory.json`
- `inventories/backup-config.json`

## Manifest

The manifest records:

- bundle identifier
- creation timestamp
- LAWIM version
- Git SHA, branch, and tag
- environment name
- PostgreSQL, Docker, Docker Compose, Python, Node, npm, Git, and systemd
  versions
- bundle checksum
- file inventory
- size
- generation duration
- encryption method

## Secret handling

- Secret values are never written into the bundle.
- `secret-inventory.json` only records metadata: name, type, location,
  mandatory flag, and present/absent state.
- Environment variables and file templates are redacted or summarized.

## Reproducibility

- File ordering is deterministic.
- The manifest checksum covers the generated bundle files.
- The bundle can be archived and downloaded through the admin DRF API.
