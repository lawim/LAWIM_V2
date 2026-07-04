# Checksums

This directory stores hashes for a materialized release bundle.

Recommended format:

- `SHA256SUMS` for the full local snapshot
- `SHA256SUMS.ovh` for the minimized OVH payload

Verification:

- `sha256sum -c SHA256SUMS`
- compare manifest files and checksum files between releases before promotion

