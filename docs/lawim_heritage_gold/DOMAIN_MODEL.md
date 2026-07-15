# LAWIM Domain Model — Certified Gold Reference

**KNOWLEDGE_ID format:** `GOLD-DM-XXX`

---

## Overview

This document captures the complete LAWIM domain model with validated evidence from primary sources. All knowledge items are cross-referenced and confidence-rated.

---

## 1. LAWIM Mission and Positioning

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-DM-001 | Mission | Démocratiser l'accès à l'information immobilière au Cameroun | Directive/00-CONSTITUTION.md, Article 1 | HIGH |
| GOLD-DM-002 | Platform type | Assistant immobilier intelligent, not a simple classifieds catalog | Directive/00-CONSTITUTION.md, Article 3 | HIGH |
| GOLD-DM-003 | Target market | Cameroon primarily, compatible with international standards | Directive/00-CONSTITUTION.md, Article 1 | HIGH |
| GOLD-DM-004 | Core services | Facilitate, secure, and accelerate: property search, publication, matching, negotiation, transaction, follow-up | Directive/00-CONSTITUTION.md, Article 1 | HIGH |
| GOLD-DM-005 | 8 objectives | Comprendre le besoin réel / Collecter uniquement les infos utiles / Éviter questions inutiles / Réduire messages / Trouver meilleur bien / Mettre en relation / Assurer suivi / Relancer automatiquement | Directive/00-CONSTITUTION.md, Article 2 | HIGH |

---

## 2. Business Model

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-DM-006 | Zero commission | LAWIM ne prélève aucune commission sur les ventes ou locations immobilières | Directive/00-CONSTITUTION.md, Article 1 §230 | HIGH |
| GOLD-DM-007 | Revenue model | Services LAWIM payants + mise en relation payante | Directive/00-CONSTITUTION.md, Article 1 §230 | HIGH |
| GOLD-DM-008 | Paid accompaniment | Accompagnement personnalisé à 50 000 FCFA | Directive/00-CONSTITUTION.md + Directive/48-LAWIM-SALES-PLAYBOOK.md | HIGH |
| GOLD-DM-009 | Lead price | Default 500 FCFA per lead for agents | Directive/08-ROLE-REFERENCE.md + heritage cross-ref | MEDIUM |

---

## 3. Eight Operating Principles

| ID | Principle | Description | Source | Confidence |
|----|-----------|-------------|--------|------------|
| GOLD-DM-010 | P1 — No re-ask | Information already given must never be asked again | Directive/00-CONSTITUTION.md, Article 4, Principe 1 | HIGH |
| GOLD-DM-011 | P2 — Correction replaces | User correction immediately replaces previous information | Directive/00-CONSTITUTION.md, Article 4, Principe 2 | HIGH |
| GOLD-DM-012 | P3 — Deduction | Conversation engine never asks what can be deduced | Directive/00-CONSTITUTION.md, Article 4, Principe 3 | HIGH |
| GOLD-DM-013 | P4 — Continuous extraction | System continuously extracts critical info from all messages | Directive/00-CONSTITUTION.md, Article 4, Principe 4 | HIGH |
| GOLD-DM-014 | P5 — Match early | Matching starts as soon as critical info is available; optional fields improve score, never block | Directive/00-CONSTITUTION.md, Article 4, Principe 5 | HIGH |
| GOLD-DM-015 | P6 — No fixed questionnaire | Conversation follows missing info, not a fixed form | Directive/00-CONSTITUTION.md, Article 4, Principe 6 | HIGH |
| GOLD-DM-016 | P7 — Cameroon adaptation | Platform adapts to Cameroonian usage; local expressions are priority | Directive/00-CONSTITUTION.md, Article 4, Principe 7 | HIGH |
| GOLD-DM-017 | P8 — International compatibility | Platform remains compatible with international standards | Directive/00-CONSTITUTION.md, Article 4, Principe 8 | HIGH |

---

## 4. Seventeen Engines Hierarchy

| ID | Engine | Role | Source | Confidence |
|----|--------|------|--------|------------|
| GOLD-DM-018 | Workflow Engine | Orchestrate states, transitions, and business events | Directive/00-CONSTITUTION.md, Article 12 | HIGH |
| GOLD-DM-019 | Conversation Engine | Understand user needs, ask only useful questions | Directive/00-CONSTITUTION.md, Article 12.1 | HIGH |
| GOLD-DM-020 | Qualification Engine | Transform free conversation into structured real estate data | Directive/00-CONSTITUTION.md, Article 12.2 | HIGH |
| GOLD-DM-021 | Matching Engine | Identify best compatible properties for a need | Directive/00-CONSTITUTION.md, Article 12.3 | HIGH |
| GOLD-DM-022 | Rematching Engine | Automatic re-matching after failed proposal | Directive/00-CONSTITUTION.md, Article 12.4 | HIGH |
| GOLD-DM-023 | Dashboard Engine | Display contextualized indicators, alerts, views | Directive/00-CONSTITUTION.md, Article 12.5 | HIGH |
| GOLD-DM-024 | Notification Engine | Diffuse official alerts and notifications | Directive/00-CONSTITUTION.md, Article 12.6 | HIGH |
| GOLD-DM-025 | Geo Engine | Normalize locations, calculate proximity | Directive/00-CONSTITUTION.md, Article 12.7 | HIGH |
| GOLD-DM-026 | Role Engine | Manage identities, roles, permissions, account orgs | Directive/00-CONSTITUTION.md, Article 12.8 | HIGH |
| GOLD-DM-027 | Reporting Engine | Calculate KPIs and official reports | Directive/00-CONSTITUTION.md, Article 12.9 | HIGH |
| GOLD-DM-028 | Storage Lifecycle Manager | Organize storage, archiving, backup, restoration | Directive/00-CONSTITUTION.md, Article 12.10 | HIGH |
| GOLD-DM-029 | Security Engine | Protect access, secrets, sensitive documents, payments | Directive/00-CONSTITUTION.md, Article 12.11 | HIGH |
| GOLD-DM-030 | API Gateway | Official entry point for all LAWIM APIs | Directive/00-CONSTITUTION.md, Article 12.12 | HIGH |
| GOLD-DM-031 | Administration Engine | Supervision, validation, internal administration | Directive/00-CONSTITUTION.md, Article 12.13 | HIGH |
| GOLD-DM-032 | LAWIM AI | Intelligent assistant for recommendations, summaries, analysis | Directive/00-CONSTITUTION.md, Article 12.14 | HIGH |
| GOLD-DM-033 | Continuous Learning Engine | Prepare monthly human-validated learnings | Directive/00-CONSTITUTION.md, Article 12.15 | HIGH |
| GOLD-DM-034 | Campay Payment Engine | Official Mobile Money payment module via Campay | Directive/00-CONSTITUTION.md, Article 12.16 | HIGH |

---

## 5. Seven Property Families

| ID | Family | Code | Source Document | Confidence |
|----|--------|------|----------------|------------|
| GOLD-DM-035 | Résidentiel | residential | Directive/02A-RESIDENTIAL-REFERENCE.md | HIGH |
| GOLD-DM-036 | Commercial | commercial | Directive/02B-COMMERCIAL-REFERENCE.md | HIGH |
| GOLD-DM-037 | Industriel | industrial | Directive/02C-INDUSTRIAL-REFERENCE.md | HIGH |
| GOLD-DM-038 | Foncier (Terrain) | land | Directive/02D-LAND-REFERENCE.md | HIGH |
| GOLD-DM-039 | Agricole | agricultural | Directive/02E-AGRICULTURAL-REFERENCE.md | HIGH |
| GOLD-DM-040 | Hôtelier | hotel | Directive/02F-HOTEL-REFERENCE.md | HIGH |
| GOLD-DM-041 | Projet immobilier | project | Directive/02G-PROJECT-REFERENCE.md | HIGH |

Source: Directive/02-PROPERTY-REFERENCE.md, Chapitre 4: "LAWIM reconnaît les familles suivantes: résidentiel, commercial, industriel, foncier, agricole, hôtelier, projet immobilier."

---

## 6. Six Transaction Types

| ID | Transaction | Description | Source | Confidence |
|----|-------------|-------------|--------|------------|
| GOLD-DM-042 | rent | Location d'un bien immobilier | knowledge_unified/real_estate/transaction_types.json | HIGH |
| GOLD-DM-043 | buy | Acquisition d'un bien immobilier | knowledge_unified/real_estate/transaction_types.json | HIGH |
| GOLD-DM-044 | sell | Mise en vente d'un bien immobilier | knowledge_unified/real_estate/transaction_types.json | HIGH |
| GOLD-DM-045 | short_stay | Séjour de courte durée | Directive/02F-HOTEL-REFERENCE.md (hébergement meublé de courte durée) | MEDIUM |
| GOLD-DM-046 | invest | Investissement immobilier | knowledge_unified/real_estate/transaction_types.json (id: INVEST) | HIGH |
| GOLD-DM-047 | lease | Location longue durée (bail 3+ ans) | knowledge_unified/real_estate/transaction_types.json (id: LEASE) | HIGH |

---

## 7. Nine User Roles

| ID | Role | Level | Description | Source | Confidence |
|----|------|-------|-------------|--------|------------|
| GOLD-DM-048 | tenant | 1 | Personne cherchant un bien à louer | business_profiles.py, user_roles.py | HIGH |
| GOLD-DM-049 | buyer | 1 | Personne cherchant un bien à acheter | business_profiles.py, user_roles.py | HIGH |
| GOLD-DM-050 | seller | 2 | Personne mettant en vente un bien | user_roles.py | HIGH |
| GOLD-DM-051 | investor | 1 | Personne cherchant à investir | business_profiles.py, user_roles.py | HIGH |
| GOLD-DM-052 | diaspora_investor | 1 | Investisseur de la diaspora | business_profiles.py (diaspora filter), crm/constants.py | HIGH |
| GOLD-DM-053 | property_seeker | 1 | Demandeur recherchant un bien | Directive/08-ROLE-REFERENCE.md (Ch.33 Demandeur) | HIGH |
| GOLD-DM-054 | agent | 3 | Professionnel de l'immobilier | Directive/08-ROLE-REFERENCE.md (Ch.36 Agent immobilier) | HIGH |
| GOLD-DM-055 | owner | 2 | Propriétaire d'un bien | Directive/08-ROLE-REFERENCE.md (Ch.35 Propriétaire) | HIGH |
| GOLD-DM-056 | broker | 3 | Courtier/intermédiaire | user_roles.py | MEDIUM |

---

## 8. Five Lead Types with Base Scores

| ID | Lead Type | Base Score | Description | Source | Confidence |
|----|-----------|------------|-------------|--------|------------|
| GOLD-DM-057 | tenant | 40 | Locataire potentiel | lead_classifier_v1.json (recovered from backup) | HIGH |
| GOLD-DM-058 | buyer | 60 | Acheteur potentiel | lead_classifier_v1.json (recovered from backup) | HIGH |
| GOLD-DM-059 | seller | 50 | Vendeur potentiel | lead_classifier_v1.json (recovered from backup) | HIGH |
| GOLD-DM-060 | investor | 80 | Investisseur potentiel | lead_classifier_v1.json (recovered from backup) | HIGH |
| GOLD-DM-061 | diaspora_investor | 95 | Investisseur diaspora | lead_classifier_v1.json (recovered from backup) | HIGH |

---

## 9. Revenue Model — Service Monetization with 13 Pricing Tiers

| ID | Service Code | Service Name | Price (FCFA) | Source | Confidence |
|----|-------------|--------------|--------------|--------|------------|
| GOLD-DM-062 | boost_7j | Boost visibilité 7 jours | 2 000 | implement_all.sql (recovered) | HIGH |
| GOLD-DM-063 | boost_30j | Boost visibilité 30 jours | 5 000 | implement_all.sql (recovered) | HIGH |
| GOLD-DM-064 | premium_listing | Annonce premium | 10 000 | implement_all.sql (recovered) | HIGH |
| GOLD-DM-065 | agent_pro | Abonnement agent professionnel | 10 000/mois | implement_all.sql (recovered) | HIGH |
| GOLD-DM-066 | accompagnement_visite | Accompagnement de visite | 50 000 | Directive/00-CONSTITUTION.md + implement_all.sql | HIGH |
| GOLD-DM-067 | accompagnement_transaction | Accompagnement de transaction | 50 000 | Directive/00-CONSTITUTION.md | HIGH |
| GOLD-DM-068 | controle_documentaire | Contrôle documentaire | 5 000 | Directive/01-GLOSSAIRE.md (Service LAWIM) | MEDIUM |
| GOLD-DM-069 | photographie | Photographie professionnelle | 15 000 | Directive/01-GLOSSAIRE.md | MEDIUM |
| GOLD-DM-070 | video | Vidéo professionnelle | 25 000 | Directive/01-GLOSSAIRE.md | MEDIUM |
| GOLD-DM-071 | verification | Vérification de bien | 10 000 | Directive/01-GLOSSAIRE.md | MEDIUM |
| GOLD-DM-072 | mise_en_relation | Mise en relation payante | 500 | Directive/00-CONSTITUTION.md (lead price) | MEDIUM |
| GOLD-DM-073 | assistance | Assistance personnalisée | 50 000 | Directive/01-GLOSSAIRE.md | MEDIUM |
| GOLD-DM-074 | visibilite_premium | Visibilité premium | 7 500 | Directive/01-GLOSSAIRE.md | MEDIUM |

---

## 10. Key Principles

### 10.1 Request Centrality

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-DM-075 | Request-driven | Every workflow starts from a user request; the system follows the need until resolved | Directive/00-CONSTITUTION.md, Article 10 | HIGH |
| GOLD-DM-076 | Progressive qualification | Information is collected progressively, never all at once | Directive/00-CONSTITUTION.md, Article 4, Principe 6 | HIGH |
| GOLD-DM-077 | Anonymity | Demandeur remains anonymous until détenteur accepts the relationship | Directive/03-CONVERSATION-REFERENCE.md | HIGH |

### 10.2 Data Retention

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-DM-078 | Account archiving | Accounts are deactivated/archived rather than deleted; data retained for legal obligations | Directive/08-ROLE-REFERENCE.md, Ch.28 | HIGH |
| GOLD-DM-079 | GDPR deletion | Users can request deletion via `SUPPRIMER MES DONNÉES`; processed within 7 days | Directive/00-CONSTITUTION.md, Article 17 | HIGH |
| GOLD-DM-080 | Historical preservation | Business history is never destroyed; archived data remains consultable | Directive/02-PROPERTY-REFERENCE.md, Ch.11 | HIGH |

### 10.3 Matching Rules

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-DM-081 | Multi-criteria matching | Matching never relies on a single criterion; uses family, type, operation, location, price, availability, attributes, data quality | Directive/02-PROPERTY-REFERENCE.md, Ch.10 | HIGH |
| GOLD-DM-082 | Auto-rematching | Automatic re-matching when a proposal fails; continues until all possibilities exhausted | Directive/00-CONSTITUTION.md, Article 2 §2.8 | HIGH |
| GOLD-DM-083 | Score-based ranking | Compatibility score calculated from multiple weighted dimensions | Directive/04-MATCHING-REFERENCE.md | HIGH |

### 10.4 Feature Flags (Recovered)

| ID | Flag | Status | Source | Confidence |
|----|------|--------|--------|------------|
| GOLD-DM-084 | whatsapp_core | ON | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-085 | property_ingestion | ON | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-086 | matching_simple | ON | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-087 | lead_generation | ON | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-088 | payments | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-089 | boost_system | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-090 | agent_subscription | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-091 | lead_scoring_ai | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-092 | dashboard | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-093 | diaspora_services | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-094 | advanced_matching | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-095 | ai_pricing_estimator | OFF | FEATURE_FLAGS.json (recovered) | HIGH |
| GOLD-DM-096 | multi_city_expansion | OFF | FEATURE_FLAGS.json (recovered) | HIGH |

---

*Certified Gold — 2026-07-15 — All entries sourced and confidence-rated.*
