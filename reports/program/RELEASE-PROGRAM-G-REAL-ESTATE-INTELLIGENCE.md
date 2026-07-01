# RELEASE PROGRAM G — Real Estate Intelligence Platform

**Programme :** RELEASE PROGRAM G  
**Date :** 2026-07-01  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-g`  
**Schema :** v13  
**Prérequis :** Programs A–F (gelés, sans régression)

---

## 1. Résumé exécutif

RELEASE PROGRAM G transforme LAWIM_V2 en **plateforme immobilière intelligente de niveau entreprise** : gestion complète du cycle de vie des biens (propriétés, annonces, vérification, matching, visites, négociations, transactions, historique, intelligence et recommandations), intégrée aux moteurs des programmes A–F (IA, Cognition, Knowledge, RAG, Workflow, Rules Engine, Écosystème).

**848 tests** passent (objectif 800+).

---

## 2. Architecture

Package : `code/lawim_v2/real_estate_intelligence/`

```
Real Estate Intelligence Platform
├── Property / Listing / Owner / Document management
├── Verification Engine (trust, anomalies, cohérence)
├── Matching Engine → rank_properties (Program B)
├── Valuation + Intelligence scoring (7 scores)
├── Recommendation Engine → RAG Knowledge (Program E)
├── Visit / Negotiation / Transaction lifecycle
├── Geo / Search / Map / Nearby
└── Workflow hooks → automation (Program F)
```

Préfixe tables : `rei_*` — extension de la table `properties` existante via `property_id` FK (aucun remplacement).

---

## 3. Schema v13

24 tables (`schema_v13_ddl.py`) :

| Domaine | Tables |
|---------|--------|
| Profils & annonces | `rei_property_profiles`, `rei_listings`, `rei_listing_publications`, `rei_listing_scores` |
| Propriétaires & docs | `rei_property_owners`, `rei_property_documents`, `rei_property_valuations` |
| Vérification | `rei_verification_checks`, `rei_verification_scores` |
| Matching | `rei_matching_sessions`, `rei_matching_results` |
| Visites | `rei_visits`, `rei_visit_reports` |
| Négociation & transactions | `rei_negotiations`, `rei_offers`, `rei_transactions`, `rei_reservations` |
| Historique & IA | `rei_property_history`, `rei_recommendations`, `rei_intelligence_scores` |
| Analytics & recherche | `rei_analytics_snapshots`, `rei_search_index`, `rei_nearby_properties`, `rei_property_reports` |

Tables v1–v12 **intactes**. Migration legacy SQLite v12→v13 via `schema_migrations.py`.

---

## 4. API v2 properties

Base : `/api/v2/properties/*` (v1 `/api/properties` inchangé)

| Endpoint | Description |
|----------|-------------|
| `GET /api/v2/properties` | Liste enrichie (profil, listing, scores) |
| `GET /api/v2/properties/{id}` | Détail bundle |
| `GET/POST /api/v2/properties/listings` | Annonces |
| `POST /api/v2/properties/{id}/publish\|archive\|duplicate` | Cycle de vie annonce |
| `GET/POST /api/v2/properties/{id}/owners` | Propriétaires |
| `GET/POST /api/v2/properties/{id}/documents` | Documents |
| `GET/POST /api/v2/properties/{id}/verification` | Vérification & score confiance |
| `GET /api/v2/properties/{id}/valuation` | Estimation |
| `POST /api/v2/properties/matching` | Matching intelligent |
| `GET/POST /api/v2/properties/recommendations` | Recommandations IA |
| `GET/POST /api/v2/properties/visits` + confirm/cancel/complete | Visites |
| `GET/POST /api/v2/properties/negotiations` + offers | Négociations |
| `GET/POST /api/v2/properties/transactions` + close | Transactions |
| `POST /api/v2/properties/reservations` | Réservations |
| `GET /api/v2/properties/{id}/history` | Historique |
| `GET /api/v2/properties/{id}/intelligence\|scores` | Scores intelligence |
| `GET /api/v2/properties/{id}/reports` | Rapports |
| `GET /api/v2/properties/search` | Recherche full-text |
| `GET /api/v2/properties/map` | Cartographie |
| `GET /api/v2/properties/{id}/nearby` | Biens proches |
| `GET /api/v2/properties/analytics\|stats` | Statistiques |

---

## 5. Intégration programmes A–F

| Programme | Usage REI |
|-----------|-----------|
| A — Intelligent Core | Projects, policy, matching foundation |
| B — Ecosystem | `rank_properties`, geo, partners |
| C — Cognition | Décisions contextuelles recommandations |
| D — Assistant | Contexte projet, RAG assistant |
| E — Knowledge | `expert_rag_query` pour recommandations |
| F — Workflow | Instances automation visites/transactions |

---

## 6. Interface administration

Panel **Real Estate Intelligence** dans `static/index.html` / `static/app.js` :

- Dashboard stats (properties, listings, transactions, trust moyen)
- Liste annonces avec score IA
- Recherche propriétés via `/api/v2/properties/search`

---

## 7. Observabilité

Compteurs ajoutés dans `observability.py` :

- `property_*`, `listing_*`, `verification_*`, `matching_*`, `recommendation_*`
- `visit_*`, `transaction_*`, `valuation_*`, `intelligence_*`
- Latence vérification (`verification_latency_ms`)

---

## 8. Sécurité & compatibilité

- Auth requise sur toutes les routes REI ; admin pour publish/archive/close
- Aucune dépendance externe ajoutée
- SQLite + PostgreSQL synchronisés (Prisma migration regénérée)
- Programmes A–F : routes et tables préservées, tests de non-régression passants

---

## 9. Tests

Fichier : `tests/test_release_program_g.py` (223 tests Program G)

Couverture : persistence, constants, engines, repository, API, UI, health, v13 tables, intégration workflow/knowledge, observabilité.

Total suite : **848 tests** (2 skipped).

---

## 10. Validations

| Script | Résultat |
|--------|----------|
| `./scripts/validate-install.sh` | PASS |
| `./scripts/validate-packaging.sh` | PASS |
| `./scripts/run-tests.sh` | PASS (848 tests) |
| `python3 scripts/validate_prisma_manifest.py` | PASS (v13) |
| `python3 scripts/smoke_runtime.py` | PASS |
| `./platform/validate-platform.sh` | PASS |
| `./platform/run-postgres-tests.sh` | PASS |
| `git diff --check` | PASS |
