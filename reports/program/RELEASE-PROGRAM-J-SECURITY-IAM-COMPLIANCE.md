# RELEASE PROGRAM J — Security • IAM • Audit • Compliance Platform

## Phase 0 — Cartographie

### Composants existants réutilisés

| Composant | Emplacement | Rôle Program J |
|-----------|-----------|--------------|
| Auth crypto | `security/credentials.py` (ex-`security.py`) | Hachage mot de passe, tokens session |
| Sessions core | `users`, `sessions` | Source auth inchangée ; extension via `access_session_records` |
| AccessPolicy | `services.py` | Délégation RBAC ; routes A–I préservées |
| Events | `events` + `record_event()` | Pont audit grossier ; trail immuable v16 |
| HTTP hardening | `server.py` | Bearer, CSP, rate limit auth |
| Automation audit | `automation_audit_log` (Program F) | Domaine workflow, non dupliqué |

### Interdictions respectées

- Pas de seconde table `users` ni store session parallèle
- Pas de duplication `risk_intelligence_scores` (Program C) ni `marketplace_review_moderation`
- Routes `/api/auth/*`, `/api/me`, `/api/events` inchangées
- Programs A–I figés, extension uniquement

## Schema v16 — 32 tables

**IAM:** `iam_roles`, `iam_permissions`, `iam_role_permissions`, `iam_user_roles`, `iam_groups`, `iam_group_members`, `iam_teams`, `iam_team_members`, `iam_access_policies`, `iam_policy_bindings`

**Access:** `access_devices`, `access_api_keys`, `access_session_records`, `access_route_policies`, `access_mfa_enrollments`, `access_token_rotations`

**Audit:** `audit_trail_entries`, `audit_system_events`, `audit_user_events`, `audit_admin_events`, `audit_ai_events`

**Compliance:** `compliance_policies`, `compliance_consents`, `compliance_retention_rules`, `compliance_deletion_requests`

**Privacy:** `privacy_data_exports`, `privacy_erasure_requests`

**Risk:** `risk_signals`, `risk_scores`, `risk_alerts`

**Security:** `security_incidents`, `security_analytics_snapshots`

## Package `code/lawim_v2/security/`

| Fichier | Rôle |
|---------|------|
| `constants.py` | Statuts, rôles/permissions par défaut |
| `schema_v16_ddl.py` | DDL SQLite + PostgreSQL |
| `engines.py` | Permission, Audit, Compliance, Risk, Privacy |
| `policies.py` / `permissions.py` | RBAC/ABAC |
| `repository.py` | `SecurityRepositoryMixin` |
| `service.py` | `SecurityService` facade |
| `dto.py` | DTOs API |
| `credentials.py` | Auth helpers (évite conflit package/module) |

## API `/api/v2/security/*`

| Route | Description |
|-------|-------------|
| `GET/POST /users`, `/roles`, `/permissions`, `/policies` | IAM |
| `GET /sessions`, `POST .../revoke` | Sessions étendues |
| `GET/POST /devices`, `/api-keys` | Appareils et clés API |
| `GET/POST /audit` | Audit trail immuable |
| `GET /compliance/*`, `POST /compliance/deletion` | Conformité |
| `GET/POST /privacy/exports`, `/privacy/erasure` | Privacy Center |
| `GET/POST /risk/*` | Risk engine |
| `GET/POST /incidents` | Incidents sécurité |
| `GET /dashboard`, `/stats`, `/analytics` | Tableau de bord |
| `GET /integrations` | Sources Programs A–I |

## Observabilité

Préfixes métriques : `security_`, `iam_`, `access_`, `role_`, `permission_`, `session_`, `audit_`, `compliance_`, `privacy_`, `risk_`

Exposé : `security_requests_total` + détail dans `crm_metrics` via `/api/metrics`.

## Tests

`tests/test_release_program_j.py` — 306 tests, 11 classes (persistence, constants, engines, permissions, repository, API, UI, health, v16 tables, integration A–I, observability).

## Compatibilité A–I

Extension transverse sans modification des routes existantes. FK vers `users`, `organizations`, `sessions`, `crm_contact_profiles`, `assistant_sessions`.
