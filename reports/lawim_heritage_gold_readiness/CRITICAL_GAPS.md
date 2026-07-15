# CRITICAL GAPS — Heritage Gold Readiness

**Audité par :** Knowledge Gap Hunter + Risk Assessor (H0.3)
**Date :** 2026-07-15

## Gaps CRITIQUE (2)

| ID | Description | Conversation | Qualification | Search | Matching | CRM | UX | Raison |
|----|-------------|:------------:|:-------------:|:------:|:--------:|:---:|:---:|--------|
| CG-001 | **7 machines à états manquantes** (Dossier, Bien, Visite, Négociation, Transaction, Paiement, Incident) | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | Bloque TOUTE l'orchestration métier. Sans état, pas de transition, pas de workflow, pas d'automatisation. Le système est réduit à un traitement linéaire de messages. |
| CG-002 | **Next Best Action (NBA) Engine non documenté** | 🔴 | 🟡 | 🔴 | 🟡 | 🔴 | 🔴 | Concept architectural central : chaque objet métier a une prochaine action optimale recalculée en continu. Sans NBA, le système est passif — ne propose rien, ne suit rien, ne relance rien. |

## Gaps MAJEUR (6)

| ID | Description | Conversation | Qualification | Search | Matching | CRM | UX |
|----|-------------|:------------:|:-------------:|:------:|:--------:|:---:|:---:|
| MG-001 | **Progressive Search Expansion absente** | 🟡 | 🟡 | 🔴 | 🔴 | 🟡 | 🔴 |
| MG-002 | **Continuous Market Surveillance absente** | 🟡 | 🟡 | 🔴 | 🔴 | 🟡 | 🔴 |
| MG-003 | **SLA par type de bien absents** | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 | 🟡 |
| MG-004 | **Sales scripts (8 scripts) absents** | 🔴 | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 |
| MG-005 | **Objection handling et escalade non implémentés** | 🔴 | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 |
| MG-006 | **Données de proximité/voisinage quasi inexistantes** | 🟡 | 🟡 | 🔴 | 🔴 | 🟡 | 🟡 |

## Gaps MOYEN (8)

| ID | Description | Conversation | Qualification | Search | Matching | CRM | UX |
|----|-------------|:------------:|:-------------:|:------:|:--------:|:---:|:---:|
| MM-001 | Pipeline CRM 8 étapes non implémenté | 🟡 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 |
| MM-002 | Système de rôles sous-documenté (2760 lignes disponibles) | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 |
| MM-003 | Anti-fraude (4 couches) non implémenté | 🟡 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 |
| MM-004 | GPS metadata (source, confiance) absents | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| MM-005 | Entity linking : 50% des paires fabriquées | 🟡 | 🟡 | 🔴 | 🟡 | 🟡 | 🟡 |
| MM-006 | Alias districts : 382/382 districts sans alias | 🟡 | 🟡 | 🔴 | 🟡 | 🟡 | 🟡 |
| MM-007 | Champs profil utilisateur étendus absents | 🟡 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 |
| MM-008 | Dossier Health Score absent | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 | 🟡 |

## Gaps MINEUR (7)

| ID | Description | Conversation | Qualification | Search | Matching | CRM | UX |
|----|-------------|:------------:|:-------------:|:------:|:--------:|:---:|:---:|
| MN-001 | Auto-enrichissement base connaissances | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 |
| MN-002 | Upload fichiers Supabase | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 |
| MN-003 | Landing page / health endpoint | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| MN-004 | WhatsApp deep link generation | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 |
| MN-005 | Synonymes multilingues propriété | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 |
| MN-006 | IDs normalisés inventés (APT, STU) | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 |
| MN-007 | Service Configuration System | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |

## Résumé des risques

| Niveau | Nombre |
|--------|:------:|
| CRITIQUE | 2 |
| MAJEUR | 6 |
| MOYEN | 8 |
| MINEUR | 7 |
| **Total** | **23** |

## Top 5 risques avant intégration

1. **Absence des 7 machines à états** → LAWIM_V2 ne peut pas gérer le cycle de vie des dossiers, biens, visites, négociations, transactions, paiements, ou incidents
2. **NBA Engine non documenté** → Le système n'a pas de capacité proactive : pas de suggestion, pas de relance intelligente, pas d'optimisation continue
3. **Progressive Search Expansion absente** → Quand le matching échoue, le système ne sait pas élargir la recherche progressivement
4. **Sales scripts absents** → Les agents LAWIM n'ont pas de scripts commerciaux pour interagir avec les clients
5. **Objection handling et escalade non implémentés** → Les objections des clients ne sont pas traitées, les escalades ne sont pas routées

## Conclusion risque

Sans les 2 gaps CRITIQUE et les 6 gaps MAJEUR, LAWIM_V2 serait un système fonctionnant à ~40% de ses capacités prévues. Les composants conversationnels et workflow seraient particulièrement affectés.
