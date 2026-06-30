# MEGA WAVE 009 — MVP Stabilization

## Résumé exécutif

MEGA WAVE 009 consolide LAWIM_V2 comme MVP démontrable : recherche, matching, négociation, notifications, UI statique et sécurité sont renforcés sans nouveau domaine métier. **49 tests** passent.

## 1. Recherche de biens (HARDENED)

| Capacité | Détail |
|----------|--------|
| Filtres | `city`, `region`, `country`, `status`, `type`, `price_min`, `price_max`, `search` |
| Pagination | `page`, `limit` + métadonnées `pagination` |
| Tri | `sort` (`created_at`, `title`, `price_min`, `city`, `status`) + `order` |
| Erreurs | `invalid_query` (fourchette prix), `validation_error` / `invalid_query` (tri invalide) |

Fichiers : `api_query.py`, `db.py`, `services.py`, `server.py`, UI Property search.

## 2. Matching (HARDENED)

| Capacité | Détail |
|----------|--------|
| Déduplication | `has_match_notification` — une seule alerte `match_found` par bien/utilisateur |
| Score explicable | `summary`, `grade`, `score_percent`, `breakdown`, `eligible` |
| Seuil configurable | `LAWIM_MATCH_MIN_SCORE` (défaut 10) + query `min_score` |
| Tests négatifs | `min_score=99` → liste vide ; déduplication vérifiée |

Fichiers : `matching.py`, `dto.py`, `db.py`, `services.py`, `config.py`.

## 3. Négociation (HARDENED)

| Capacité | Détail |
|----------|--------|
| Statuts | Stages `inquiry` → `offer` → `counter` → `accepted` / `declined` / `closed` |
| Historique | `conversation.negotiation.history` (timeline messages) |
| Transitions | Validation `STAGE_TRANSITIONS` (erreur cohérente) |
| Permissions | Participants + org + admin ; refus cross-user |

Fichiers : `conversation_domain.py`, `dto.py`, UI formulaire negotiation stage.

## 4. Notifications (HARDENED)

| Capacité | Détail |
|----------|--------|
| Lu / non lu | champ `read`, `read_at` |
| Filtrage | `kind`, `unread_only` |
| Pagination | `page`, `limit` + `pagination` |
| Cohérence | `match_found` déduplié ; filtres alignés sur événements existants |

Fichiers : `api_query.py`, `db.py`, `services.py`, `server.py`, UI filtre notifications.

## 5. UI statique (IMPROVED)

- Parcours Seller / Buyer / Admin : recherche enrichie, pagination visible, badges statut publication.
- Erreurs : `formatApiError` affiche `[code] message`.
- États : chips statut bien, compteur unread notifications, détail négociation avec stages autorisés.
- Matching : affichage `grade` + `summary`.

Fichiers : `index.html`, `app.js`, `styles.css`.

## 6. Sécurité

- Accès croisés : PATCH property refusé hors org (test dédié).
- Payload limits : `LAWIM_MAX_JSON_BODY_BYTES` (config) appliqué au JSON body.
- Headers : inchangés (CSP, X-Frame-Options) — validés par tests existants.

## 7. Tests

Nouveau fichier : `tests/test_mvp_stabilization.py` (9 cas) :
- Recherche prix / pagination / erreurs
- Matching déduplication + min_score + DTO enrichi
- Négociation transitions + permissions
- Notifications kind + pagination
- Cross-access property + payload oversized
- Régression UI DTO

## Fichiers modifiés

- `code/lawim_v2/api_query.py`, `config.py`, `matching.py`, `conversation_domain.py`, `dto.py`
- `code/lawim_v2/db.py`, `services.py`, `server.py`
- `code/lawim_v2/static/index.html`, `app.js`, `styles.css`
- `tests/test_mvp_stabilization.py`, `tests/test_product_depth.py`, `tests/lawim_harness.py`, `tests/test_lawim_v2.py`

## Contrôles obligatoires

- `python3 -m compileall` — OK
- `python3 -m unittest discover -s tests -v` — **49 tests OK**
- `python3 -m lawim_v2 --help` — OK
- `python3 scripts/validate_prisma_manifest.py` — OK
- `git diff --check` — OK
- Docker compose configs (4 variantes) — OK

## Limites

- Historique négociation basé sur messages (pas de journal d'événements stage séparé).
- UI statique sans tests headless navigateur.
- PostgreSQL live non exercé en CI.

## Prochaine vague

**MEGA WAVE 010** : onboarding vendeur self-service, tests headless UI, PostgreSQL CI live.

```yaml
wave: MEGA_WAVE_009
status: READY_FOR_DG_REVIEW
mvp: STABILIZED
search: HARDENED
matching: HARDENED
negotiation: HARDENED
notifications: HARDENED
ui: IMPROVED
tests: PASS
blocking_risk: false
next_wave: MEGA_WAVE_010
decision_required: true
```
