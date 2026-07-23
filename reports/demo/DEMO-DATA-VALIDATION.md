# LAWIM Demo World V1 — Data Validation Report

**Date:** 2026-07-23

## 1. Fichier maître

| Check | Status |
|-------|--------|
| Existence | ✅ `demo/reference/LAWIM-DEMO-WORLD-REFERENCE.yaml` (33KB) |
| Schéma de validation | ✅ `demo/reference/LAWIM-DEMO-WORLD-REFERENCE.schema.json` |
| Conformité au schéma | ✅ PASSED |
| Source de vérité unique | ✅ Toutes les données dans le YAML |

## 2. Intégrité des identifiants

| Check | Status |
|-------|--------|
| IDs uniques | ✅ Vérifié par analyse |
| Format DEMO-* | ✅ Tous les IDs suivent la convention |
| Références valides | ✅ owner_id pointe vers utilisateur existant |

## 3. Couverture fonctionnelle

| Domaine | Statut | Notes |
|---------|--------|-------|
| Clients | ✅ 5 profils | 3 consentements, 2 niveaux vérification |
| Propriétaires | ✅ 4 profils | 3 consentements, 1 inactif |
| Agents | ✅ 3 profils | 2 actifs, 1 suspendu |
| Architectes | ✅ 1 profil | Associé à organisation |
| Notaires | ✅ 1 profil | Associé à organisation |
| Géomètres | ✅ 1 profil | Associé à organisation |
| Avocats | ❌ 0 | Défini dans coverage mais pas de données |
| Artisans | ❌ 0 | Défini dans coverage mais pas de données |
| Commerciaux | ✅ 1 profil | |

## 4. Catalogue immobilier

| Check | Statut | Détail |
|-------|--------|--------|
| Nombre de biens | ✅ | 95 (cible ~100) |
| Villes couvertes | ✅ | 5 villes |
| Types APARTMENT | ✅ | 44 |
| Types HOUSE | ✅ | 35 |
| Types STUDIO | ✅ | 16 |
| Types LAND | ❌ | 0 |
| Biens actifs | ✅ | Majorité |
| Biens suspendus | ✅ | ~5 |
| Propriétaires assignés | ✅ | Tous |
| Médias associés | ❌ | Aucun |

## 5. Services professionnels

| Check | Statut |
|-------|--------|
| Architecture | ✅ 3 services |
| Notaire | ✅ 2 services |
| Géomètre | ✅ 2 services |
| Juridique | ✅ 1 service |
| Construction | ✅ 2 services |
| Maintenance | ✅ 1 service |

## 6. Tests

| Suite | Résultat |
|-------|----------|
| LROS total | 733 PASS |
| V2 journey | 47 PASS |
| Matching E2E | 12 PASS |
| Nouvelles régressions | 0 |

## 7. Sécurité

| Check | Statut |
|-------|--------|
| Vrais numéros de téléphone | ✅ Aucun dans le YAML |
| Emails personnels | ✅ Adresses @demo.lawim.app |
| Tokens / clés | ✅ Aucun |
| Secrets versionnés | ✅ Aucun |
| Coordonnées réelles | ✅ Aucune |

## 8. Gaps identifiés

1. **LAND property type non représenté** dans les biens (pourtant nécessaire pour SCENARIO-LAND-NKOABANG-001)
2. **Avocats, artisans, électriciens, plombiers** dans coverage mais pas de profils dédiés
3. **Médias, documents, rendez-vous** sections absentes
4. **Seed, verify, reset scripts** non implémentés
5. **Persistance OVH** non vérifiée
