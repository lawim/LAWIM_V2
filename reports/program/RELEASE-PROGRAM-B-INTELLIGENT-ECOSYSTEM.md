# RELEASE PROGRAM B — Intelligent Ecosystem Platform

**Programme :** RELEASE PROGRAM B  
**Date :** 2026-06-30  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-b`  
**Schema :** v8  
**Prérequis :** RELEASE PROGRAM A (`release-program-a`)

---

## 1. Résumé exécutif

RELEASE PROGRAM B transforme LAWIM 2.x en **écosystème immobilier intelligent**. Le projet immobilier (Program A) mobilise désormais automatiquement **partenaires**, **services**, **workflows** et **interventions** — entièrement **déterministe**, sans IA générative.

**224 tests** passent (objectif 220+).

---

## 2. Architecture du domaine Ecosystem

Package : `code/lawim_v2/ecosystem/`

```
Project (aggregate root — Program A)
├── Partner Platform (partner_profiles → organizations)
├── Service Marketplace (service_catalog)
├── Matching Engine 2.0 (project_match_results)
├── Trust & Reputation (reputation_metrics)
├── Workflow Engine (workflows → workflow_instances)
├── Notification & Event Engine (ecosystem_events → ecosystem_notifications)
└── Resource Orchestration (service_orders, project_interventions, project_ecosystem_state)
```

Intégration : `LawimRepository(EcosystemRepositoryMixin, IntelligentRepositoryMixin, ProjectRepositoryMixin)`.

---

## 3. Partner Platform

**19 types** supportés (`ecosystem/constants.py`) : agence, notaire, banque, microfinance, géomètre, architecte, BTP, artisan, déménageur, assureur, expert, syndic, décorateur, gestionnaire locatif, énergie, internet, administration, etc.

Tables : `partner_profiles`, `partner_zones`, `partner_skills`, `partner_certifications`, `partner_availability`, `partner_sla`.

Chaque profil est lié à une **organisation** existante, avec scores qualité/confiance, zones d'intervention, SLA et catalogue de services.

---

## 4. Service Marketplace

Table `service_catalog` — 12 services seedés (recherche, visites, documentaire, financement, estimation, bail, mise en marché, terrain, permis, analyse marché, déménagement, conseil).

Champs : catégorie, tarifs indicatifs, durée, documents, prérequis, livrables, partenaires associés (`service_catalog_partners`).

---

## 5. Matching Engine 2.0

`MatchingEngine2` — centré sur :

- Projet + objectifs + contraintes + contexte géographique + état du parcours

Produit : partenaires recommandés, services recommandés, score, confiance, priorité, justification (règles métier).

Persistance : `project_match_results`. API : `POST /api/v2/matching`, `GET /api/v2/matching?project_id=`, `POST /api/v2/projects/{id}/matching/run`.

---

## 6. Trust & Reputation

`TrustReputationEngine` calcule : Trust Score, Quality Score, Completion Rate, Reliability, Response Time, Satisfaction, Incident History.

Tables : `reputation_metrics` + mise à jour cache `partner_profiles`.

API : `GET /api/v2/reputation?subject_type=partner&subject_id=`.

Architecture extensible par `subject_type` (partner, organization, service, project).

---

## 7. Workflow Engine

8 workflows seedés : buy, sell, rent, build, finance, relocation, succession, invest.

Tables : `workflows`, `workflow_steps`, `workflow_instances`, `workflow_instance_steps`.

Orchestration : tâches, partenaires par étape, dépendances, échéances.

API : `GET /api/v2/workflows`, `GET /api/v2/projects/{id}/workflows`.

Bootstrap automatique à la création de projet.

---

## 8. Notification & Event Engine

`NotificationEventEngine` — événements métier, rappels, changements d'état.

Tables : `ecosystem_events`, `ecosystem_notifications`.

Canaux préparés : `in_app` (livré), `email`, `sms`, `whatsapp`, `push` (pending — sans connecteurs).

API : `GET /api/v2/notifications/ecosystem`.

---

## 9. API v2 Ecosystem

| Route | Description |
|-------|-------------|
| `GET/POST /api/v2/partners` | Annuaire partenaires |
| `GET /api/v2/partners/{id}` | Détail partenaire |
| `GET /api/v2/services` | Catalogue services |
| `GET /api/v2/services/{id}` | Détail service |
| `GET /api/v2/workflows` | Templates workflow |
| `GET/POST /api/v2/matching` | Matching projet |
| `GET /api/v2/reputation` | Scores réputation |
| `GET /api/v2/notifications/ecosystem` | Notifications ecosystem |
| `GET /api/v2/resources?project_id=` | Ressources agrégées |
| `GET /api/v2/projects/{id}/orchestration` | Vue orchestration |
| `GET /api/v2/projects/{id}/workflows` | Instance workflow |
| `POST /api/v2/projects/{id}/matching/run` | Recalcul matching |

Compatibilité v1 et API v2 Program A préservées.

---

## 10. UI

Extension progressive (`static/index.html`, `static/app.js`) :

- Cartes **Ecosystem partners** et **Service marketplace**
- Détail projet : matches partenaires/services, workflow, interventions, orchestration
- Chargement parallèle workspace + orchestration + matching + workflow

---

## 11. Persistance v8

- `APPLICATION_SCHEMA_VERSION = 8`
- **19 nouvelles tables** ecosystem (`schema_v8_ddl.py`)
- Migration legacy v7→v8 via `apply_sqlite_legacy_migrations()`
- Prisma migration SQL régénérée (779 lignes)
- Dual SQLite / PostgreSQL

---

## 12. Tests

| Suite | Focus |
|-------|-------|
| `test_release_program_b.py` | 73 tests — engines, API, repository, migration, UI |
| Suites existantes | 151 |
| **Total** | **224** (2 skipped) |

Validations : install, packaging, prisma manifest, smoke, platform, PostgreSQL.

---

## 13. Observabilité

Compteurs ajoutés : `ecosystem_partners_total`, `ecosystem_services_total`, `ecosystem_matching_total`, `ecosystem_workflows_total`, `ecosystem_reputation_total`, `ecosystem_notifications_total`, `ecosystem_orchestration_total`.

---

## 14. Dette restante

- Modèles Prisma typés pour tables v8 (migration SQL alignée, models à compléter)
- Connecteurs email/SMS/WhatsApp/push
- Commande service_orders UI complète (création API présente)
- Qualification partenaire workflow admin avancé
- Marketplace paiement / facturation

---

## 15. Statut

**RELEASE PROGRAM B — TERMINÉ**

LAWIM organise, coordonne et recommande l'ensemble des acteurs et services nécessaires à la réussite du projet immobilier.
