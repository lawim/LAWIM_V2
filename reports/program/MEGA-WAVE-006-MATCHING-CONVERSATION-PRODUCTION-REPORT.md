# MEGA WAVE 006 — Matching, Conversation & Production Hardening

## 1. Résumé exécutif

MEGA WAVE 006 livre les moteurs de valeur utilisateur de LAWIM_V2 : matching multi-critères avec explication, conversations/négociation enrichies, notifications in-app minimales, observabilité applicative et durcissement production partiel. Le schéma runtime passe en **v5** (SQLite par défaut, PostgreSQL/Prisma alignés). **23 tests** passent ; Compose et validation Prisma passent.

## 2. Décisions architecturales

- **Schéma v5** : table `notifications` ; colonnes `organization_id`, `negotiation_stage`, `updated_at` sur `conversations`.
- **Domaines dédiés** : `matching.py` (poids normalisés), `conversation_domain.py` (transitions statut/stage), `notification_domain.py` (kinds), `observability.py` (métriques runtime).
- **DTOs API** : `match_dto`, `conversation_dto`, `message_dto`, `notification_dto` dans `dto.py` — UI et bootstrap alignés.
- **Notifications** : générées côté service (événements domaine → stockage in-app), pas de push externe.
- **SQLite first** : migrations idempotentes via `_apply_migrations` ; PostgreSQL hérite de `LawimRepository` avec DDL v5.

## 3. Matching

- Scoring multi-critères : statut, ville, région, budget, proximité, attributs (type/chambres), disponibilité.
- Pondération configurable via query params (`weight_*`) ; normalisation à 100 points.
- Réponse API : `score`, `breakdown`, `reasons`, `distance_km`, `weights`, `property` (DTO).
- Endpoint : `GET /api/matches` avec filtres étendus (`region`, `country`, `property_type`, `bedrooms_min`, `availability`).

## 4. Conversation

- Modèle enrichi : rattachement `organization_id`, `negotiation_stage` (inquiry → offer → counter → accepted/declined/closed).
- Historique messages inchangé ; `updated_at` mis à jour à chaque message.
- Filtres liste : `user_id`, `organization_id`, `property_id`, `status`.
- Permissions : requester, membres org propriétaire, admin.
- Endpoints : CRUD existants + `negotiation_stage` en PATCH.

## 5. Notifications

- Kinds : `conversation_created`, `message_received`, `conversation_updated`, `match_found`, `system`.
- Stockage SQLite/PostgreSQL ; génération automatique sur création/mise à jour conversation et nouveau message.
- API : `GET /api/notifications`, `PATCH /api/notifications/{id}/read`, `POST /api/notifications/read-all`.

## 6. Observabilité

- Health enrichi : environnement, summary, audit (`recent_events`), métriques si activées.
- `GET /api/metrics` : compteurs requests/matches/conversations/notifications, uptime.
- Compteurs incrémentés dans le handler HTTP ; erreurs comptabilisées (`requests_failed`).
- Erreurs JSON standardisées via `error_dto` / handler existant.

## 7. Production hardening

- Headers sécurité : `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, CSP sur réponses statiques et JSON.
- Limite payload JSON 1 Mo (existant) ; upload multipart via `max_upload_bytes`.
- Config : `LAWIM_CDN_BASE_URL`, `LAWIM_METRICS_ENABLED` ; CDN préparé dans `LocalMediaStorage`.
- **Partiel** : pas de déploiement CDN réel, rate limiting et TLS termination hors scope.

## 8. Prisma/CI

- `prisma/schema.prisma` v5 aligné (Notification, Conversation enrichie).
- `scripts/validate_prisma_manifest.py` vérifie modèle Notification et version manifest.
- Commande utile : `python3 scripts/validate_prisma_manifest.py`

## 9. UI

- Panneau notifications avec marquage lu (clic + « Mark all read »).
- Matches : affichage breakdown et reasons.
- Conversations : stage négociation, DTO requester/property.
- Health strip : compteur requests.

## 10. Tests

- 23 tests unitaires/intégration (`tests/test_lawim_v2.py`).
- Nouveaux : matching breakdown, notifications E2E, negotiation stage, health/metrics, schema v5.
- Validations : compileall, unittest, `--help`, validate_prisma, git diff --check, 4 configs Compose.

## 11. Limites

- Notifications limitées à in-app (pas email/SMS/webhook).
- Matching sans ML ; poids manuels via query string.
- PostgreSQL path testé au niveau profil/DDL, pas en CI live Postgres.
- Production hardening partiel (pas de WAF, pas de déploiement CDN).

## 12. Prochaine vague recommandée

**MEGA WAVE 007** : recherche full-text avancée, webhooks notifications, rate limiting API, tests PostgreSQL CI optionnels, dashboard observabilité externe.

```yaml
wave: MEGA_WAVE_006
status: READY_FOR_DG_REVIEW
matching: IMPLEMENTED
conversation: IMPLEMENTED
notifications: IMPLEMENTED
observability: HARDENED
production_hardening: PARTIAL
tests: PASS
compose: PASS
blocking_risk: false
next_wave: MEGA_WAVE_007
decision_required: true
```
