# Release Deployment Guide

This directory is the release projection for LAWIM_V2.

It separates three concerns:

- `current/` for a full local release snapshot;
- `ovh/` for the minimized deployment payload;
- `manifests/` for the source-of-truth packaging rules;
- `checksums/` for bundle hashes when a package is materialized;
- `deployment/` for operator-facing release notes.

Rules:

- the master repository remains the reference source;
- no migration is launched from this directory;
- no real secret is stored here;
- no test, report, prompt, benchmark, or cache is copied into the OVH payload;
- runtime payloads are assembled only from the allowlist in `manifests/DEPLOYMENT_MANIFEST.md`.

Rebuild flow:

1. Read `manifests/RELEASE_MANIFEST.md` for the selected snapshot.
2. Materialize `current/` from tracked source inputs.
3. Materialize `ovh/` from the deployment allowlist.
4. Write SHA256 hashes under `checksums/`.
5. Compare the manifest and checksum files between releases.

Canonical references:

- `docs/OVH_DEPLOYMENT_MANIFEST.md`
- `docs/DEPLOYMENT.md`
- `deployment/runbook/`
- `deployment/scripts/`
- `deployment/health/`

