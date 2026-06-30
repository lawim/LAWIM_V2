# WAVE 007 — Product Depth Validation and Hardening

## 1. Endpoints cartographiés

| Méthode | Route | Auth | Description |
|---------|-------|------|-------------|
| GET | `/healthz` | — | Liveness probe |
| GET | `/`, `/index.html`, `/app.js`, `/styles.css` | — | UI statique |
| GET | `/media/*` | — | Fichiers média locaux |
| GET | `/api/health` | — | Health enrichi + audit + metrics |
| GET | `/api/metrics` | — | Compteurs runtime |
| GET | `/api/bootstrap` | optionnel | État agrégé (DTO) |
| POST | `/api/auth/login` | — | Session |
| POST | `/api/auth/register` | — | Inscription publique (roles limités) |
| POST | `/api/auth/logout` | optionnel | Invalidation session |
| GET | `/api/me` | requis | Profil courant |
| GET/POST | `/api/organizations` | POST admin | Organisations |
| PATCH | `/api/organizations/{id}` | admin | Mise à jour org |
| GET/POST | `/api/users` | POST admin | Utilisateurs |
| PATCH/DELETE | `/api/users/{id}` | requis | Profil / suppression |
| GET/POST | `/api/properties` | POST requis | Biens paginés |
| GET/PATCH/DELETE | `/api/properties/{id}` | PATCH/DELETE requis | Détail / mutation |
| POST | `/api/properties/{id}/publish` | requis | Publication |
| GET | `/api/properties/{id}/media` | — | Médias d'un bien |
| GET/POST | `/api/media` | POST requis | Liste / création URL |
| POST | `/api/media/upload` | requis | Upload multipart |
| GET/PATCH/DELETE | `/api/media/{id}` | PATCH/DELETE requis | Média unitaire |
| GET | `/api/geo/normalize` | — | Normalisation adresse |
| GET | `/api/geo/geocode` | — | Géocodage |
| GET | `/api/geo/search` | — | Recherche lieux |
| GET | `/api/geo/contracts` | — | Contrat thumbnail |
| GET | `/api/matches` | — | Matching multi-critères |
| GET/POST | `/api/conversations` | **requis** | Threads négociation |
| GET/PATCH/DELETE | `/api/conversations/{id}` | **requis** | Détail / statut / stage |
| GET/POST | `/api/conversations/{id}/messages` | **requis** | Historique / envoi |
| GET | `/api/notifications` | requis | Liste in-app |
| PATCH | `/api/notifications/{id}/read` | requis | Marquage lu |
| POST | `/api/notifications/read-all` | requis | Tout marquer lu |
| GET | `/api/events` | admin | Audit trail |

## 2. Parcours testés

Parcours E2E complet (`test_full_product_journey_from_org_to_audit`) :

1. Login admin → création organisation → création agent
2. Login agent → création bien (draft)
3. Géocodage → mise à jour coordonnées
4. Upload média multipart → publication
5. Matching retrouve le bien publié
6. Owner ouvre conversation → agent répond
7. Notifications générées et marquées lues
8. Admin consulte audit events
9. Metrics disponibles
10. Relecture persistance (property, media, conversation, asset `/media/`)

## 3. Tests ajoutés

Fichiers : `tests/lawim_harness.py`, `tests/test_product_depth.py`

| Classe | Tests | Focus |
|--------|-------|-------|
| `ProductDepthE2ETest` | 1 | Parcours produit complet |
| `ProductDepthNegativeTest` | 10 | Auth, permissions, payload, média, geo, erreurs, headers |
| `ProductDepthUIValidationTest` | 3 | DTOs UI, bootstrap guest/auth |

Total suite : **37 tests** (23 existants + 14 nouveaux).

## 4. Faiblesses trouvées

1. **Conversations lisibles sans authentification** — fuite de données privées (liste + détail + messages).
2. **Bootstrap guest exposait toutes les conversations** quand `actor=None`.
3. **Headers sécurité absents sur `/media/*`** — pas de `X-Content-Type-Options` / `X-Frame-Options`.
4. **Kind `match_found`** déclaré mais jamais émis (notification simulée).
5. **Géocodage external** configuré mais non testé en CI (provider `local` par défaut).
6. **PostgreSQL** profil validé, pas de tests runtime live Postgres.

## 5. Corrections réalisées

| Correction | Fichiers |
|------------|----------|
| Auth obligatoire sur GET conversations/messages | `server.py` |
| Liste conversations vide pour guest bootstrap | `services.py` |
| Headers sécurité unifiés (`_send_security_headers`) sur JSON + média | `server.py` |
| UI : `selectConversation` exige auth | `app.js` |
| Test baseline : conversations non-auth → 401 | `test_lawim_v2.py` |

## 6. Fonctionnalités réellement utilisables

- Auth session Bearer (login/logout/register)
- CRUD organisations (admin), users (admin), properties (org-scoped)
- Upload média local + validation MIME/taille
- Géocodage déterministe local + normalisation geo
- Publication avec optimistic locking
- Matching multi-critères avec breakdown
- Conversations/négociation avec permissions
- Notifications in-app (created/message/updated)
- Audit events (admin)
- Metrics runtime
- UI statique consommant DTOs bootstrap/matches/conversations/notifications

## 7. Fonctionnalités encore simulées

- **`match_found` notification** — kind défini, jamais généré
- **Géocodage external (Nominatim)** — implémenté, non exercé par défaut
- **CDN (`LAWIM_CDN_BASE_URL`)** — préparation URL, pas de déploiement
- **PostgreSQL runtime** — DDL + adapter, SQLite reste moteur live par défaut
- **Push/email notifications** — hors scope, in-app uniquement

## 8. Limites restantes

- Pas de rate limiting API
- Pas de tests navigateur (UI validée par contenu statique + intégration API)
- Suppression organisation non supportée (by design)
- Conversations sans property restent org-scoped via user org

## 9. Prochaine vague recommandée

**WAVE 008** : émission réelle `match_found`, tests PostgreSQL CI optionnels, rate limiting, durcissement CSP sur JSON, tests UI headless minimaux.

```yaml
wave: WAVE_007
status: READY_FOR_DG_REVIEW
product_depth: VALIDATED
e2e_tests: PASS
negative_tests: PASS
api_hardening: PASS
ui_validation: PASS
persistence_validation: PASS
blocking_risk: false
next_wave: WAVE_008
decision_required: true
```
