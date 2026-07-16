# LAWIM — QA Test Accounts Register

**Document ID:** LAWIM-OPS-QA-ACCOUNTS-V1  
**Status:** OPERATIONAL  
**Date:** 2026-07-15  
**Security:** Passwords stored OUTSIDE Git in `/opt/lawim/secrets/qa-test-accounts.env`

---

## Roles Inventoried

| Code | Label | Level | Permissions |
|------|-------|-------|-------------|
| admin | Administrateur global | System | * (all) |
| manager | Gestionnaire d'agence | Agency | read, write, manage_team |
| operator | Opérateur | Agency | read, write |
| partner | Partenaire | Partner | read |
| user | Utilisateur | Public | read_own |
| tenant_admin | Admin tenant | Tenant | read, write, manage_tenant |
| agent | Agent immobilier | Agency | read, write_conversation, write_property |

## QA Accounts Created

| Login | Role | Agency | Status | Password Location |
|-------|------|--------|--------|-------------------|
| qa.admin.global | admin | — | ACTIVE, must change password | `/opt/lawim/secrets/qa-test-accounts.env` |
| qa.manager.agency01 | manager | QA Agency 01 | ACTIVE, must change password | same |
| qa.manager.agency02 | manager | QA Agency 02 | ACTIVE, must change password | same |
| qa.agent.agency01.01 | agent | QA Agency 01 | ACTIVE, must change password | same |
| qa.agent.agency01.02 | agent | QA Agency 01 | ACTIVE, must change password | same |
| qa.agent.agency02.01 | agent | QA Agency 02 | ACTIVE, must change password | same |
| qa.operator.01 | operator | QA Agency 01 | ACTIVE, must change password | same |
| qa.partner.01 | partner | — | ACTIVE, must change password | same |
| qa.user.01 | user | — | ACTIVE, must change password | same |
| qa.user.02 | user | — | ACTIVE, must change password | same |
| qa.auditor.01 | admin (auditor) | — | ACTIVE, must change password | same |

## Password Policy

- Length: 20+ characters
- Complexity: upper, lower, digits, special
- Unique per account
- Temporary: must change on first login
- Generated via: `python3 -c "import secrets, string; print(''.join(secrets.choice(string.ascii_letters+string.digits+'!@#$%') for _ in range(24)))"`

## Security

- Credentials file: `/opt/lawim/secrets/qa-test-accounts.env`
- Permissions: `600` (owner read/write only)
- Never committed to Git
- Never logged
- Transfer to password manager required
