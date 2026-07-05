# Security Baseline

## Controls in place

- SSH key-based access for the initial operator;
- dedicated `lawim` system user;
- secret files restricted to the server;
- UFW allowing only SSH, HTTP and HTTPS;
- AAD disabled by default;
- default language set to `fr`;
- no internal docs in the OVH payload;
- no real secret in Git.

## Secret handling

- secrets live in `/opt/lawim/secrets/`;
- TLS private material stays on the server;
- password and token values are never written to the repository;
- provisional credentials must be rotated before public exposure.

## Operational rule

- any deviation from this baseline must be recorded before rollout.
