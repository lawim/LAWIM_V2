# MEGA WAVE 008 — End-to-End User Journeys

## Résumé exécutif

MEGA WAVE 008 transforme LAWIM_V2 en application orientée parcours : trois flux métier complets (vendeur, acheteur, administrateur) sont implémentés, testés E2E et exposés dans une UI par rôle. **40 tests** passent.

## Parcours vendeur

| Étape | API / UI |
|-------|----------|
| Inscription | `POST /api/auth/register` (agent + org) · formulaire Register |
| Organisation | `POST /api/organizations` (prélude admin) |
| Création bien | `POST /api/properties` · formulaire Create property |
| Géolocalisation | `GET /api/geo/geocode` + `PATCH /api/properties/{id}` |
| Médias | `POST /api/media/upload` |
| Publication | `POST /api/properties/{id}/publish` · bouton Publish |
| Modification | `PATCH /api/properties/{id}` |
| Archivage | `PATCH status=archived` · bouton Archive |

Test : `SellerJourneyTest.test_seller_journey_register_listing_publish_and_archive`

## Parcours acheteur

| Étape | API / UI |
|-------|----------|
| Inscription | `POST /api/auth/register` (owner) |
| Recherche / filtrage | `GET /api/properties?city&status&property_type` · Property search |
| Matching | `GET /api/matches` (auth → notification `match_found`) |
| Consultation | `GET /api/properties/{id}` |
| Conversation | `POST /api/conversations` · Start conversation |
| Négociation | `PATCH negotiation_stage=offer` |
| Notifications | `GET /api/notifications` · panneau Notifications |

Test : `BuyerJourneyTest.test_buyer_journey_search_match_negotiate_and_notify`

## Parcours administrateur

| Étape | API / UI |
|-------|----------|
| Audit | `GET /api/events` |
| Supervision | `GET /api/health`, `GET /api/metrics` · panneau Supervision |
| Gestion contenus | `DELETE /api/properties/{id}` (soft si conversations) |
| Gestion utilisateurs | `POST /api/users`, `GET /api/users` |
| Organisations | `POST /api/organizations` · formulaire Administration |

Test : `AdminJourneyTest.test_admin_journey_supervision_audit_and_user_management`

## Améliorations livrées

- **Notification `match_found`** émise lors d'une recherche matching authentifiée.
- **UI par parcours** : navigation Seller / Buyer / Admin, formulaires dédiés, actions publish/archive, dashboard admin.
- **Harness tests** : `register()` helper dans `lawim_harness.py`.
- **Tests E2E** : `tests/test_user_journeys.py` (3 parcours complets).

## Fichiers modifiés

- `code/lawim_v2/services.py` — `list_matches(actor=...)`, notification match_found
- `code/lawim_v2/server.py` — auth optionnelle sur `/api/matches`
- `code/lawim_v2/static/index.html`, `app.js`, `styles.css` — console par parcours
- `tests/test_user_journeys.py`, `tests/lawim_harness.py`

## Limites

- Création d'organisation réservée à l'admin (inscription vendeur requiert org existante).
- Archivage vendeur via statut `archived` ; suppression soft réservée aux biens avec conversations.
- UI statique (pas de tests navigateur headless).

## Prochaine vague

**MEGA WAVE 009** : onboarding vendeur self-service (org), négociation UI (stages), tests headless, PostgreSQL CI live.

```yaml
wave: MEGA_WAVE_008
status: READY_FOR_DG_REVIEW
seller_journey: IMPLEMENTED
buyer_journey: IMPLEMENTED
admin_journey: IMPLEMENTED
e2e_tests: PASS
ui_journeys: IMPLEMENTED
blocking_risk: false
next_wave: MEGA_WAVE_009
decision_required: true
```
