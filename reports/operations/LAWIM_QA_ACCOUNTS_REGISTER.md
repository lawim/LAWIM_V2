# LAWIM — QA Test Accounts Register

**Document ID:** LAWIM-OPS-QA-ACCOUNTS-V2
**Status:** OPERATIONAL
**Date:** 2026-07-16
**Decision:** LAWIM QA ACCOUNTS RECREATED AND VERIFIED

---

## Roles Inventoried

| Code | Label | Level | Permissions |
|------|-------|-------|-------------|
| admin | Administrateur global | System | * (all) |
| manager | Gestionnaire d'agence | Agency | read, write, manage_team |
| operator | Opérateur | Agency | read, write |
| partner | Partenaire | Partner | read |
| user | Utilisateur | Public | read_own |

## QA Accounts — Sanitised (Git-safe)

| Identifiant | Rôle | Téléphone masqué | Email masqué | Agence/Tenant | Connexion testée |
|------------|------|-----------------|-------------|---------------|-----------------|
| qa.admin.global | admin | +23769****** | qa.***@lawim.qa | — | ✅ PASS |
| qa.tenant.admin | admin | +23773****** | qa.***@lawim.qa | — | ✅ PASS |
| qa.manager.douala | manager | +23767****** | qa.***@lawim.qa | QA Agency Douala | ✅ PASS |
| qa.manager.yaounde | manager | +23791****** | qa.***@lawim.qa | QA Agency Yaoundé | ✅ PASS |
| qa.agent.douala.01 | agent | +23769****** | qa.***@lawim.qa | QA Agency Douala | ✅ PASS |
| qa.agent.douala.02 | agent | +23769****** | qa.***@lawim.qa | QA Agency Douala | ✅ PASS |
| qa.agent.yaounde.01 | agent | +23761****** | qa.***@lawim.qa | QA Agency Yaoundé | ✅ PASS |
| qa.operator.01 | operator | +23798****** | qa.***@lawim.qa | QA Agency Douala | ✅ PASS |
| qa.partner.01 | partner | +23783****** | qa.***@lawim.qa | — | ✅ PASS |
| qa.user.01 | user | +23783****** | qa.***@lawim.qa | — | ✅ PASS |
| qa.user.02 | user | +23784****** | qa.***@lawim.qa | — | ✅ PASS |
| qa.auditor.01 | admin | +23780****** | qa.***@lawim.qa | — | ✅ PASS |

## Password Policy

- Length: 24 characters
- Complexity: upper, lower, digits, special (`!@#$%&*+-_=.`)
- Unique per account
- Temporary: must change on first login (enforced at DB level)
- Generated via: `secrets.SystemRandom` (cryptographically secure)

## Security

- Credentials file (server): `/opt/lawim/secrets/qa-test-accounts.env` — root:root, chmod 600
- Credentials file (laptop): `/home/abel/.config/lawim/qa-test-accounts.env` — abel:abel, chmod 600
- Never committed to Git (files are outside the repository)
- Never logged
- Passwords not derivable from hashes (PBKDF2-HMAC-SHA256, 210k iterations)
