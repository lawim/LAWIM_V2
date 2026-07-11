# Secrets

Secrets are restored separately from the Recovery Bundle.

## Policy

- Never store passwords, OAuth tokens, JWTs, private certificates, or private
  keys inside the bundle.
- Never export raw secret values in inventories or reports.
- Keep only metadata that helps an operator confirm whether the required
  secret is present.

## Secret inventory

`inventories/secret-inventory.json` contains:

- name
- type
- location
- mandatory flag
- present/absent flag

## Restoration

- Restore secrets before restoring PostgreSQL or launching LAWIM.
- Use the documented secret source for the target environment.
- Missing required secrets lower the Recovery Readiness Score.

## Validation

- The bundle validation checks the presence of the secret inventory file.
- The readiness score penalizes missing secret coverage.
- Secret presence is treated as evidence, not as a substitute for the secret
  values themselves.
