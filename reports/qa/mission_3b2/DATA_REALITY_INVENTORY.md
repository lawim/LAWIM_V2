# DATA REALITY INVENTORY — Mission 3B.2 Vague 1

**Date:** 2026-07-15
**Source:** OVH — ubuntu@164.132.44.192 (lawim_v2 database)
**Méthode:** SQL inventory queries via docker exec

---

## 1. PROPERTIES

| id | title | city | property_type | price_min | price_max | status | availability | bedrooms | deleted_at |
|----|-------|------|---------------|-----------|-----------|--------|--------------|----------|------------|
| — | — | — | — | — | — | — | — | — | — |

**Count:** 0 rows
**Observation:** La table `properties` est vide. Aucun bien immobilier en base de production.
**Impact:** Search et Matching ne peuvent pas produire de résultats. Les tests de zéro résultat sont seuls testables.

---

## 2. USERS

| id | email | role | preferred_language |
|----|-------|------|--------------------|
| 5 | admin@lawim.app | admin | fr |
| 6 | agent@lawim.app | agent | fr |
| 7 | owner@lawim.app | owner | fr |
| 8 | manager@lawim.app | manager | fr |
| 9 | investor@lawim.app | investor | fr |

**Count:** 5 rows
**Roles:** admin, agent, owner, manager, investor
**Langue:** 100% français
**Observation:** Utilisateurs purement fonctionnels. Pas d'utilisateurs réels.

---

## 3. PARTNER PROFILES

| id | partner_type | display_name | status |
|----|--------------|--------------|--------|
| 1 | real_estate_agency | LAWIM Partner Agency | active |
| 2 | photographer | LAWIM Studio Photo | active |
| 3 | architect | LAWIM Architecture | active |
| 4 | notary | LAWIM Notaire Associé | active |
| 5 | bank | LAWIM Finance Desk | active |
| 6 | artisan | LAWIM Artisan Hub | active |
| 7 | diagnostician | LAWIM Diagnostics | active |
| 8 | mover | LAWIM Move Partner | active |

**Count:** 8 rows
**Types:** agency, photographer, architect, notary, bank, artisan, diagnostician, mover
**Observation:** Pas de colonne `city` — organisation par zone via `partner_zones`. Profils partenaires génériques LAWIM.

---

## 4. ORGANIZATIONS

| id | name | kind | city |
|----|------|------|------|
| 1 | LAWIM Demo Agency | agency | Douala |
| 2 | LAWIM Owner Desk | owner | Kribi |

**Count:** 2 rows
**Types:** agency, owner
**Observation:** Organisations minimales de démonstration.

---

## 5. PROJECTS

| id | user_id | title | project_type | status | location_city |
|----|---------|-------|--------------|--------|---------------|
| 1 | 7 | Studio Yaounde | rent | draft | Yaounde |

**Count:** 1 row
**Status:** draft
**Observation:** Projet unique en brouillon. Pas de projet actif.

---

## 6. SERVICE CATALOG

| id | service_key | category | title | status |
|----|-------------|----------|-------|--------|
| 1 | property_search | acquisition | Recherche de biens | active |
| 2 | visit_support | acquisition | Accompagnement visites | active |
| 3 | document_check | legal | Vérification documentaire | active |
| 4 | financing_prequalification | financing | Préqualification financement | active |
| 5 | valuation | valuation | Estimation immobilière | active |
| 6 | lease_review | rental | Relecture bail | active |
| 7 | listing_support | sale | Mise en marché | active |
| 8 | land_search | construction | Recherche terrain | active |
| 9 | permit_guidance | construction | Permis de construire | active |
| 10 | market_analysis | advisory | Analyse de marché | active |
| 11 | moving_service | moving | Déménagement | active |
| 12 | project_guidance | advisory | Conseil projet | active |

**Count:** 12 rows
**Status:** 100% active
**Couverture:** 12 services couvrant acquisition, legal, financing, valuation, rental, sale, construction, advisory, moving

---

## 7. DATABASE INVENTORY SUMMARY

| Table | Enregistrements | Statut |
|-------|-----------------|--------|
| users | 5 | Données fonctionnelles |
| properties | 0 | **VIDE** |
| partner_profiles | 8 | Profils génériques |
| organizations | 2 | Démonstration |
| projects | 1 | Draft uniquement |
| service_catalog | 12 | Complet |

**Schéma total:** 465 tables (identifiées via information_schema)

**Tables clés supplémentaires pour Mission 3B.2:**
- `conversations`, `conversation_messages`, `conversation_facts`, `conversation_decisions`
- `match_results`, `rei_matching_results`, `marketplace_matching_results`
- `relationships`, `relationship_proposals`, `relationship_participants`
- `consent_requests`, `compliance_consents`
- `search_requests`
- `ai_providers`, `ai_requests`, `ai_responses`, `ai_circuit_breakers`, `ai_fallback_entries`
- `crm_leads`, `crm_contacts`, `crm_opportunities`
- `projects` (détaillé ci-dessus), `project_steps`, `project_milestones`

---

## 8. CONSTATS ET RISQUES

1. **Properties table vide** — Search et Matching ne peuvent pas être validés en conditions réelles. Le système ne peut retourner que des résultats vides.
2. **Pas de données de production réelles** — Toutes les données sont des artefacts de démonstration ou de test.
3. **Système de matching multiple** — 3 tables de matching (`match_results`, `rei_matching_results`, `marketplace_matching_results`) suggèrent une fragmentation non-canonique.
4. **Consentement** — Table `consent_requests` et `compliance_consents` existent, à vérifier pour alignement avec le modèle canonique.
5. **465 tables** — Indique une dérive architecturale importante par rapport à la cible canonique qui définit ~30 objets.
