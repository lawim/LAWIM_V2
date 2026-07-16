# LAWIM — QA Accounts Register (Redacted)

**Date:** 2026-07-15  
**Credentials file (outside Git):** `/opt/lawim/secrets/qa-test-accounts.env` (600)

---

| Identifiant | Rôle | Téléphone masqué | Email masqué | Agence/Tenant | Statut |
|------------|------|------------------|-------------|---------------|--------|
| qa.admin.global | admin | +237 6•• •• •• 01 | admin•••@lawim.qa | — | ACTIVE |
| qa.tenant.admin | tenant_admin | +237 6•• •• •• 02 | tenant•••@lawim.qa | Tenant QA | ACTIVE |
| qa.manager.douala | manager | +237 6•• •• •• 03 | mgr-dla•••@lawim.qa | Agence Douala | ACTIVE |
| qa.manager.yaounde | manager | +237 6•• •• •• 04 | mgr-yde•••@lawim.qa | Agence Yaoundé | ACTIVE |
| qa.agent.douala.01 | agent | +237 6•• •• •• 05 | ag-dla1•••@lawim.qa | Agence Douala | ACTIVE |
| qa.agent.douala.02 | agent | +237 6•• •• •• 06 | ag-dla2•••@lawim.qa | Agence Douala | ACTIVE |
| qa.agent.yaounde.01 | agent | +237 6•• •• •• 07 | ag-yde1•••@lawim.qa | Agence Yaoundé | ACTIVE |
| qa.operator.01 | operator | +237 6•• •• •• 08 | op•••@lawim.qa | Agence Douala | ACTIVE |
| qa.partner.01 | partner | +237 6•• •• •• 09 | partner•••@lawim.qa | — | ACTIVE |
| qa.user.01 | user | +237 6•• •• •• 10 | user1•••@lawim.qa | — | ACTIVE |
| qa.user.02 | user | +237 6•• •• •• 11 | user2•••@lawim.qa | — | ACTIVE |
| qa.auditor.01 | auditor | +237 6•• •• •• 12 | auditor•••@lawim.qa | — | ACTIVE |

## Password Policy

- 20+ characters, mixed case, digits, special
- Unique per account, must change on first login
- Generated via `secrets` module
- Stored in `/opt/lawim/secrets/qa-test-accounts.env` (chmod 600)

## Security

- All passwords displayed once to operator during interactive session
- Operator instructed to transfer to password manager
- No passwords committed to Git
- No passwords in logs
- All accounts labeled QA — no real personal data used
