# REQUIRED EXTENSIONS — Heritage Gold → LAWIM_V2

**Document ID:** LAWIM-HARM-EXTENSIONS-V1
**Status:** CANONICAL — Definitive list of all Heritage Gold concepts requiring new implementation in LAWIM_V2
**Date:** 2026-07-15

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Trust & Badges (14 concepts)](#2-trust--badges-14-concepts)
3. [Agency Structure (9 concepts)](#3-agency-structure-9-concepts)
4. [Service Model (72+ concepts)](#4-service-model-72-concepts)
5. [Workflows (14 workflows)](#5-workflows-14-workflows)
6. [Property Model (15 concepts)](#6-property-model-15-concepts)
7. [Intent Detection (6 concepts)](#7-intent-detection-6-concepts)
8. [Qualification Engine (107 matrices)](#8-qualification-engine-107-matrices)
9. [CRM (15+ concepts)](#9-crm-15-concepts)
10. [Matching (15+ concepts)](#10-matching-15-concepts)
11. [SLA & NBA (10+ concepts)](#11-sla--nba-10-concepts)
12. [Permission Model (4 concepts)](#12-permission-model-4-concepts)
13. [Appendix: Extension Catalog](#13-appendix-extension-catalog)

---

## 1. Executive Summary

This document catalogs every Heritage Gold concept that has **NO equivalent** in the current LAWIM_V2 codebase. These concepts require new implementation — they cannot be mapped, migrated, or adapted from existing V2 capabilities.

### 1.1 Aggregate Statistics

| Domain | EXTENSION_REQUIRED Concepts | Crosswalk Reference | Priority |
|--------|---------------------------|---------------------|----------|
| Trust & Badges | 14 | ROLE_CROSSWALK.md §2.4, §2.5 | P1 |
| Agency Structure | 9 | ROLE_CROSSWALK.md §2.6 | P2 |
| Service Model | 72+ | SERVICE_CROSSWALK.md | P1 |
| Workflows | 14 workflows | WORKFLOW_STATE_CROSSWALK.md | P1 |
| Property Model | 15+ | PROPERTY_TYPE_CROSSWALK.md | P0 |
| Intent Detection | 6+ | INTENT_TRANSACTION_CROSSWALK.md | P1 |
| Qualification Engine | 107 matrices | INTENT_TRANSACTION_CROSSWALK.md §8 | P2 |
| CRM | 15+ | WORKFLOW_STATE_CROSSWALK.md §2.18 | P1 |
| Matching | 15+ | WORKFLOW_STATE_CROSSWALK.md §2.03 | P1 |
| SLA & NBA | 10+ | WORKFLOW_STATE_CROSSWALK.md §4, §5 | P2 |
| Permission Model | 4 | ROLE_CROSSWALK.md §2.3 | P2 |

### 1.2 Priority Legend

| Priority | Definition | Target Timeline |
|----------|-----------|-----------------|
| P0 | Blocking — core identity model, must ship first | Immediate |
| P1 | Critical — core business logic, must ship with MVP | Sprint 1-2 |
| P2 | High — important functionality, ship in near-term | Sprint 3-4 |
| P3 | Medium — valuable enhancement, ship when ready | Sprint 5+ |
| P4 | Low — nice-to-have, defer to post-launch | Backlog |

---

## 2. Trust & Badges (14 concepts)

**Source:** ROLE_CROSSWALK.md §2.4, §2.5
**Status:** 14/14 EXTENSION_REQUIRED (0% coverage)

### 2.1 Trust Levels (6 concepts)

Trust levels define a graduated verification system for user accounts. Each level gates access to platform features and signals user credibility.

| Extension ID | Concept | Gold Reference | Business Reason | Proposed Target | Impact | Priority | Human Decision Required |
|---|---|---|---|---|---|---|---|
| EXT-RL-TRUST-001 | Niveau 1 — Nouveau compte (New Account) | GOLD-RL-018 | Base trust level for all new users; gates access to basic platform features | Add `trust_level` INT (1-6) field to User model | Security gates for sensitive operations; trust-based matching | P1 | Yes — default trust level assignment policy |
| EXT-RL-TRUST-002 | Niveau 2 — Téléphone vérifié (Phone Verified) | GOLD-RL-019 | OTP phone verification as first identity check; unlocks enhanced platform access | Add `phone_verified` Boolean to User; implement OTP verification flow | Trust score affects match confidence; phone verification unlocks features | P1 | No — standard OTP flow |
| EXT-RL-TRUST-003 | Niveau 3 — Identité vérifiée (Identity Verified) | GOLD-RL-020 | Document-based identity verification (CNI/passport); reduces fraud risk | Add `identity_verified` Boolean; implement document upload + admin validation workflow | Higher match confidence; trust badge; fraud reduction | P1 | Yes — admin validation threshold |
| EXT-RL-TRUST-004 | Niveau 4 — Documents pro validés (Professional Docs Validated) | GOLD-RL-021 | Professional credential validation for agents/partners; unlocks professional features | Add `professional_docs_verified` Boolean; implement pro document workflow | Professional qualification unlocked; trust badge on listings | P2 | Yes — document acceptance criteria |
| EXT-RL-TRUST-005 | Niveau 5 — Professionnel vérifié (Verified Professional) | GOLD-RL-022 | Full professional verification; gates access to pro-tier platform features | Add `professional_verified` Boolean; complete verification workflow | Verified pro badge; prioritized in matches; pro CRM segment | P2 | Yes — professional verification criteria |
| EXT-RL-TRUST-006 | Niveau 6 — Compte de référence (Reference Account) | GOLD-RL-023 | Highest trust level; manually granted by admin for reference/power users | Add `reference_account` Boolean; admin-only grant | Maximum system trust; reference badge; premium qualification | P3 | Yes — admin-only grant policy |

### 2.2 Badges (8 concepts)

Badges are visual trust signals derived from verification status. They display on user profiles, agent profiles, and listings.

| Extension ID | Concept | Gold Reference | Business Reason | Proposed Target | Impact | Priority | Human Decision Required |
|---|---|---|---|---|---|---|---|
| EXT-RL-BADGE-001 | Badge: Téléphone vérifié | GOLD-RL-024 | Visual indicator of phone verification | Implement badge rendering system; derive from `phone_verified` flag | User trust signaling; professional credibility | P2 | No — derive from trust flag |
| EXT-RL-BADGE-002 | Badge: E-mail vérifié | GOLD-RL-025 | Visual indicator of email verification | Add `email_verified` flag; implement badge | User trust signaling | P2 | No — derive from email verification |
| EXT-RL-BADGE-003 | Badge: Identité vérifiée | GOLD-RL-026 | Visual indicator of identity verification | Derive from `identity_verified` trust level; implement badge display | User trust signaling | P2 | No — derive from trust flag |
| EXT-RL-BADGE-004 | Badge: Propriétaire vérifié | GOLD-RL-027 | Visual indicator of property ownership verification | Add `owner_verified` field; implement document verification for owners | Owner verification reduces listing fraud | P2 | Yes — ownership proof criteria |
| EXT-RL-BADGE-005 | Badge: Agence vérifiée | GOLD-RL-028 | Visual indicator of agency registration verification | Add `agency_verified` to Organization model; implement verification workflow | Agency verification prevents fake agencies | P2 | Yes — agency verification criteria |
| EXT-RL-BADGE-006 | Badge: Partenaire LAWIM | GOLD-RL-029 | Visual indicator of partner validation | Derive from `professional_verified`; add partner-specific badge | Partner status reduces fraud | P2 | No — derive from trust flag |
| EXT-RL-BADGE-007 | Badge: Professionnel vérifié | GOLD-RL-030 | Visual indicator of professional status | Derive from `professional_verified` trust level | Professional verification is trust signal | P2 | No — derive from trust flag |
| EXT-RL-BADGE-008 | Badge: Agent actif | GOLD-RL-031 | Visual indicator of fully onboarded and active agent | Add `is_active_agent` field or derive from onboarding completion | Active agent status is operational | P3 | Yes — active agent definition |

---

## 3. Agency Structure (9 concepts)

**Source:** ROLE_CROSSWALK.md §2.6
**Status:** 6/9 EXTENSION_REQUIRED, 3/9 PARTIAL_MATCH

| Extension ID | Concept | Gold Reference | Business Reason | Proposed Target | Impact | Priority | Human Decision Required |
|---|---|---|---|---|---|---|---|
| EXT-RL-AGENCY-001 | Agent onboarding flow | GOLD-RL-035 | Structured step-by-step agent onboarding (invitation → account → phone → CNI → validation → active) | Implement onboarding state machine with `onboarding_status` field on User | Agent activation gates matching; CRM onboarding pipeline | P2 | Yes — onboarding step policy |
| EXT-RL-AGENCY-002 | Minimum 3 active agents for operational agency | GOLD-RL-036 | Business rule: agency requires minimum 3 agents for full operational status | Add agent count validation rule; agency operational status logic | Agency capabilities gated by agent count | P3 | Yes — minimum threshold value |
| EXT-RL-AGENCY-003 | Lead routing by geographic zone | GOLD-RL-037 | Route incoming leads to agents based on geographic zone assignment | Implement `agent_zones` table; build lead routing engine | Lead distribution efficiency; agent lead volume management | P2 | Yes — routing algorithm |
| EXT-RL-AGENCY-004 | Lead cost (500 FCFA default) | GOLD-RL-038 | Charge agents per lead received; core monetization mechanism | Implement lead costing module with configurable price | Financial impact; core revenue model | P1 | Yes — pricing strategy |
| EXT-RL-AGENCY-005 | Agent credits & boosts | GOLD-RL-039 | Agent credit system with boost purchases for visibility | Implement `agent_credits` (credits, total_spent, last_recharge) and `boost_purchases` (boost_type, price, expires_at) | Financial impact; matching priority via boosts | P1 | Yes — credit pricing |
| EXT-RL-AGENCY-006 | Agent rating (1-5) | GOLD-RL-040 | Post-interaction agent rating (1-5 scale) for quality signals | Add `agent_rating` FLOAT field; implement post-interaction rating workflow | Quality signals; matching quality | P2 | Yes — rating calculation method |

### 3.1 Partial Match Items (Requiring Extension)

| Extension ID | Concept | Gold Reference | Current Limitation | Proposed Extension | Priority |
|---|---|---|---|---|---|
| EXT-RL-AGENCY-007 | Agency hierarchy roles | GOLD-RL-010 | V2 has Organization model but no agency-specific role on User | Add `agency_role` enum field (`responsible`, `admin`, `agent`, `assistant`) to User model scoped by organization_id | P2 |
| EXT-RL-AGENCY-008 | Agency components & trust | GOLD-RL-033 | V2 has users+properties on Organization but lacks agency-level validations | Add `trust_level`, `verification` fields to Organization model | P2 |
| EXT-RL-AGENCY-009 | Agency registration fields | GOLD-RL-034 | V2 Organization missing RCCM, CNI, tax ID fields | Add `rccm`, `tax_id`, `cni_document` fields to Organization model | P2 |

---

## 4. Service Model (72+ concepts)

**Source:** SERVICE_CROSSWALK.md
**Status:** 46/72 EXTENSION_REQUIRED (63.9%), 17/72 NORMALIZED_MATCH, 8/72 PARTIAL_MATCH, 1/72 MANY_TO_ONE

### 4.1 Monetized Services (13 concepts)

All 13 Heritage Gold monetized services require full implementation — no equivalent exists in V2.

| Extension ID | Service | Gold Code | Price (FCFA) | Business Reason | Proposed Target | Priority |
|---|---|---|---|---|---|---|
| EXT-SVC-MON-001 | Boost visibilité 7 jours | boost_7j | 2 000 | Paid visibility boost for property listings | Add `boost_level` and `boost_expires_at` to Property model | P1 |
| EXT-SVC-MON-002 | Boost visibilité 30 jours | boost_30j | 5 000 | Extended visibility boost | Same as boost_7j with duration parameter | P1 |
| EXT-SVC-MON-003 | Annonce premium | premium_listing | 10 000 | Premium listing with maximum visibility | Add `is_premium` field to Property; premium ranking boost | P1 |
| EXT-SVC-MON-004 | Abonnement agent professionnel | agent_pro | 10 000/mois | Monthly agent subscription | Implement Subscription model linked to Organization/User | P1 |
| EXT-SVC-MON-005 | Accompagnement de visite | accompagnement_visite | 50 000 | LAWIM agent accompanies property visit | Implement as ServiceOrder with type='visit_accompaniment' | P2 |
| EXT-SVC-MON-006 | Accompagnement de transaction | accompagnement_transaction | 50 000 | Full transaction accompaniment | Implement as ServiceOrder with type='transaction_accompaniment' | P2 |
| EXT-SVC-MON-007 | Contrôle documentaire | controle_documentaire | 5 000 | Document verification service | Defer — requires document workflow | P4 |
| EXT-SVC-MON-008 | Photographie professionnelle | photographie | 15 000 | Professional photography | Extend Media model with service order origin | P4 |
| EXT-SVC-MON-009 | Vidéo professionnelle | video | 25 000 | Professional videography | Extend Media model with service order origin | P4 |
| EXT-SVC-MON-010 | Vérification de bien | verification | 10 000 | Property verification | Add `verification_status` to Property | P2 |
| EXT-SVC-MON-011 | Mise en relation payante | mise_en_relation | 500 | Pay-per-connection — core LAWIM monetization | Implement LeadPurchase model + agent credit system | P1 |
| EXT-SVC-MON-012 | Assistance personnalisée | assistance | 50 000 | Personalized premium assistance | Requires human decision on distinction from accompaniment | P4 |
| EXT-SVC-MON-013 | Visibilité premium | visibilite_premium | 7 500 | Premium visibility package | Requires human decision on distinct semantics vs boost/premium_listing | P3 |

### 4.2 Real Estate Service Matrices (24 concepts)

| Extension ID | Matrix ID | Service | Business Reason | Priority |
|---|---|---|---|---|
| EXT-SVC-RES-001 | SVC-ESTI-001 | estimation_immobiliere | Property valuation — feeds matching pipeline | P1 |
| EXT-SVC-RES-002 | SVC-EXPE-002 | expertise | Professional property inspection | P2 |
| EXT-SVC-RES-003 | SVC-VERI-003 | verification_documentaire | Document verification | P2 |
| EXT-SVC-RES-004 | SVC-VISI-004 | visite_property | Visit scheduling — PARTIAL in Conversation | P1 |
| EXT-SVC-RES-005 | SVC-CONT-005 | contre_visite | Second visit scheduling | P1 |
| EXT-SVC-RES-006 | SVC-GEST-006 | gestion_locative | Rental property management | P3 |
| EXT-SVC-RES-007 | SVC-MISE-007 | mise_en_location | Rental listing service — PARTIAL via Property | P1 |
| EXT-SVC-RES-008 | SVC-MISE-008 | mise_en_vente | Sales listing service — PARTIAL via Property | P1 |
| EXT-SVC-RES-009 | SVC-PUBL-009 | publication_service | Publication service — PARTIAL via publishedAt | P1 |
| EXT-SVC-RES-010 | SVC-PHOT-010 | photographie | Photography service — PARTIAL via Media | P4 |
| EXT-SVC-RES-011 | SVC-VIDE-011 | video_service | Video service — PARTIAL via Media | P4 |
| EXT-SVC-RES-012 | SVC-DRON-012 | drone_service | Drone photography | P4 |
| EXT-SVC-RES-013 | SVC-HOME-013 | home_staging | Property staging | P4 |
| EXT-SVC-RES-014 | SVC-RENO-014 | renovation_service | Renovation — PARTIAL via Project.projectType | P3 |
| EXT-SVC-RES-015 | SVC-CONS-015 | construction_service | Construction — PARTIAL via Project.projectType | P3 |
| EXT-SVC-RES-016 | SVC-ENTR-016 | entretien | Property maintenance | P4 |
| EXT-SVC-RES-017 | SVC-NETT-017 | nettoyage | Cleaning service | P4 |
| EXT-SVC-RES-018 | SVC-SECU-018 | securisation | Security service | P4 |
| EXT-SVC-RES-019 | SVC-DEME-019 | demenagement | Moving service | P4 |
| EXT-SVC-RES-020 | SVC-ASSU-020 | assurance_service | Insurance referral | P4 |
| EXT-SVC-RES-021 | SVC-CONS-021 | conseil_juridique | Legal advice | P4 |
| EXT-SVC-RES-022 | SVC-CONS-022 | conseil_fiscal | Tax advice | P4 |
| EXT-SVC-RES-023 | SVC-GEST-023 | gestion_copropriete | Condominium management | P4 |
| EXT-SVC-RES-024 | SVC-RECO-024 | recouvrement_locatif | Rent recovery | P4 |

### 4.3 Professional Service Matrices (10 of 27 EXTENSION_REQUIRED)

17 of 27 professional services map to business profiles; 10 require extension.

| Extension ID | Matrix ID | Service | V2 Gap | Priority |
|---|---|---|---|---|
| EXT-SVC-PRO-001 | PRO-MACON-008 | macon (Mason) | Not in business_profiles.py | P3 |
| EXT-SVC-PRO-002 | PRO-MENUI-011 | menuisier (Carpenter) | Not in business_profiles.py | P3 |
| EXT-SVC-PRO-003 | PRO-PEINT-012 | peintre (Painter) | Not in business_profiles.py | P3 |
| EXT-SVC-PRO-004 | PRO-CARRE-013 | carreleur (Tiler) | Not in business_profiles.py | P3 |
| EXT-SVC-PRO-005 | PRO-COUVR-014 | couvreur (Roofer) | Not in business_profiles.py | P3 |
| EXT-SVC-PRO-006 | PRO-EXPIM-015 | expert_immobilier (Real estate expert) | Not in business_profiles.py | P3 |
| EXT-SVC-PRO-007 | PRO-EVALU-016 | evaluateur (Appraiser) | Not in business_profiles.py | P4 |
| EXT-SVC-PRO-008 | PRO-SYNDI-018 | syndic (Condo manager) | Not in business_profiles.py | P4 |
| EXT-SVC-PRO-009 | PRO-VIDEO-020 | videaste_drone (Drone videographer) | Not in business_profiles.py | P4 |
| EXT-SVC-PRO-010 | PRO-COURT-026 | courtier (Broker) | Not in business_profiles.py | P4 |
| EXT-SVC-PRO-011 | PRO-GARDI-023 | gardiennage (Security/guard) | Not in business_profiles.py | P4 |
| EXT-SVC-PRO-012 | PRO-PREST-027 | prestataire_administratif (Admin provider) | Not in business_profiles.py | P4 |

### 4.4 CRM Monetized Services (8 concepts)

| Extension ID | Service | Code | Price (FCFA) | Priority |
|---|---|---|---|---|
| EXT-SVC-CRM-001 | Lead Bronze (1 contact) | lead_bronze | 500 | P1 |
| EXT-SVC-CRM-002 | Lead Silver (5 contacts) | lead_silver | 1 500 | P1 |
| EXT-SVC-CRM-003 | Lead Gold (15 contacts) | lead_gold | 3 000 | P1 |
| EXT-SVC-CRM-004 | Déblocage coordonnées propriétaire | deblocage_coordonnees | 500 | P1 |
| EXT-SVC-CRM-005 | Demandeur Premium | demandeur_premium | 1 000 | P4 |
| EXT-SVC-CRM-006 | Diaspora Simple | diaspora_simple | 25 000 | P3 |
| EXT-SVC-CRM-007 | Diaspora Rapport | diaspora_rapport | 50 000 | P3 |
| EXT-SVC-CRM-008 | Diaspora Complet | diaspora_complet | 75 000 | P3 |
| EXT-SVC-CRM-009 | Abonnement Agent Business | agent_business | 25 000/mois | P2 |

### 4.5 Service & Payment Lifecycle (18 states)

| Extension ID | Concept | Gold Reference | Business Reason | Priority |
|---|---|---|---|---|
| EXT-SVC-LIFE-001 | Service lifecycle (8 states) | WORKFLOW_08 | Création → Proposition → Acceptation → Paiement → Activation → Utilisation → Expiration → Archivage | P1 |
| EXT-SVC-LIFE-002 | Payment sub-states (10 states) | WORKFLOW_08 | PAYMENT_CREATED → INITIATED → PENDING → CONFIRMED → FAILED → CANCELLED → EXPIRED → REFUNDED → RECONCILED → DISPUTED | P1 |

---

## 5. Workflows (14 workflows)

**Source:** WORKFLOW_STATE_CROSSWALK.md
**Status:** 14 of 21 workflows require FULL implementation

| Extension ID | Workflow | Gold States | V2 States | Business Reason | Priority |
|---|---|---|---|---|---|
| EXT-WF-001 | Matching Lifecycle | 10 | 0 | Algorithmic property-demandeur matching is the core platform intelligence | P1 |
| EXT-WF-002 | Mise en Relation / Contact | 6 | 0 | Double consent workflow before contact establishment | P1 |
| EXT-WF-003 | Visit Lifecycle | 9 | 0 | Visit scheduling, confirmation, cancellation, no-show tracking | P1 |
| EXT-WF-004 | Transaction Lifecycle | 10 | 0 | End-to-end transaction processing (documents → payment → signature → handover) | P1 |
| EXT-WF-005 | Paid Services & Payment | 8+10 | 0 | Service catalog ordering and payment processing via Campay | P1 |
| EXT-WF-006 | Disputes, Claims & Incidents | 8 | 0 | Fraud detection, incident reporting, claim handling | P2 |
| EXT-WF-007 | Mediation Workflow | 8 | 0 | LAWIM mediator appointment, exchange facilitation, solution proposal | P3 |
| EXT-WF-008 | CRM Pipeline | 8 | 0 | Lead scoring, classification, routing — core CRM intelligence | P1 |
| EXT-WF-009 | Publication (SIE-Enriched) | 11 | 0 | External system publication with reference code generation | P3 |
| EXT-WF-010 | Redirection (SIE-Enriched) | 12 | 0 | Click tracking, bot detection, session creation | P3 |
| EXT-WF-011 | Conversion & Attribution | 12 | 0 | Last-touch conversion attribution pipeline | P3 |
| EXT-WF-012 | Agent Invitation Workflow | 7 | 0 | Structured agent onboarding (invitation → secure link → account → phone → CNI → validation → active) | P2 |
| EXT-WF-013 | Identity Resolution Workflow | 5 | 0 | Duplicate user detection and merging | P3 |
| EXT-WF-014 | Main Cross-cutting Workflow | 9 | 0 | Orchestrator coordinating all sub-workflows | P2 |

### 5.1 Workflow State Machines Detail

#### EXT-WF-001: Matching Lifecycle (10 states)

```
Load Dossier → Check Critical Fields → Select Compatible Properties → Eliminate Incompatible 
→ Calculate Scores → Rank Properties → Propose Best → Wait for Decision → Learn → Recalculate
```

**Score Dimensions:** Real Estate (25/20/15/15/15/10), Availability, Document, Holder Reliability, Transaction Success
**Compatibility Levels:** Excellent, Good, Average, Low
**Rematching:** Automatic on refusal, visit failure, negotiation failure

#### EXT-WF-002: Mise en Relation / Contact (6 states)

```
Matching Complete → Demandeur Interested → Holder Contacted → Holder Decision → Double Consent Obtained → Mise en Relation Established
```

**Key Rule:** Double consent is MANDATORY — both demandeur interested AND holder favorable required
**Holder Silence Escalation:** Reminder 1 → Reminder 2 → Last Reminder → Property "to confirm" → Rematching
**Interlocutor Shift:** After Mise en Relation, AI handoff to human (owner/agency)

#### EXT-WF-003: Visit Lifecycle (9 states)

```
Demandée → En attente de confirmation → Confirmée → Reportée → Annulée 
→ Réalisée → Refusée → Absence demandeur → Absence détenteur
```

**SLA:** Reminder 24h before, Reminder 2h before, configurable reminders
**NBA Post-Visit:** Très satisfait → Open negotiation; Mitigé → Second visit; Insatisfait → Propose another / Rematch

#### EXT-WF-004: Transaction Lifecycle (10 states)

```
Accord → Préparation → Documents → Paiement → Signature → Remise des clés → Confirmation → Transaction terminée → Archivage / Échec
```

**Transaction Types:** Location, Vente, Achat, Bail professionnel, Bail commercial, Location saisonnière
**Document Requirements:** Per transaction type (sale: land title, ID, power of attorney; rental: contract, deposit, inventory)

#### EXT-WF-005: Payment Lifecycle (18 states)

**Service States (8):** Création → Proposition → Acceptation → Paiement → Activation → Utilisation → Expiration → Archivage
**Payment Sub-states (10):** CREATED → INITIATED → PENDING → CONFIRMED → FAILED → CANCELLED → EXPIRED → REFUNDED → RECONCILED → DISPUTED

**Monetized Services:** Boost, Premium, Agent Pro, Agent Business, Leads, Diaspora packages
**Revenue Rule:** LAWIM never deducts % from transactions — revenue from platform services only

#### EXT-WF-006: Disputes & Incidents (8 states)

```
Signalement → Qualification → Analyse → Collecte informations → Décision → Résolution → Clôture → Archivage
```

**Priority Levels:** Critique (Immediate), Élevée (< 24h), Normale (< 72h), Faible (per support)
**Incident Types:** 12 types — property unavailable, inaccurate info, visit cancellation, participant absence, fraud, fake documents, platform abuse
**Fraud Actions:** Temporary suspension (account/property/listing/contact), all motivated, historized, reversible

#### EXT-WF-007: Mediation Workflow (8 states)

```
Incident → Proposition médiation → Acceptation parties → Nomination Médiateur LAWIM → Échanges → Proposition solution → Acceptation / Clôture
```

**Mediator Role:** Listen, facilitate, explain procedures, seek amicable solution, document exchanges
**Cannot:** Impose decision, represent a party, modify dossier history, render legal judgment

#### EXT-WF-008: CRM Pipeline (8 stages)

```
incoming_message → normalize_text → extract_entities → detect_intent → context_enrichment → lead_scoring → lead_classification → crm_routing
```

**Lead Types with Base Scores:** tenant(40), buyer(60), seller(50), investor(80), diaspora_investor(95)
**Score Boosters (13):** budget_detected(+15), city_detected(+10), neighborhood(+10), urgency(+20), diaspora(+25), cash_purchase(+15), etc.
**Score Penalties (8):** missing_budget(-10), unclear_location(-10), spam_like(-50), too_short(-20), external_links(-30), etc.
**Classifications:** HOT, WARM, COLD, LOW, SPAM

#### EXT-WF-009: Publication (SIE-Enriched) (11 states)

```
Création → Validation → Génération Reference Code → Association Campagne → Association Acteur 
→ Association Biens → Association Services → Publication sur canal → Journalisation 
→ Mise à jour statistiques → Disponibilité dashboards
```

**Key Concept:** SIE (Système d'Information Externalisé) reference code is MANDATORY before publication

#### EXT-WF-010: Redirection (SIE-Enriched) (12 states)

```
Utilisateur → Clic lien → Validation Reference Code → Contrôle intégrité → Détection bot 
→ Détection doublon → Journalisation → Création session (éventuelle) → Redirection 
→ Mise à jour statistiques → Événement Reporting → Événement Continuous Learning
```

#### EXT-WF-011: Conversion & Attribution (12 states)

```
Publication → Clic → Redirection → Visite → Création compte (éventuelle) → Conversation 
→ Matching → Visite terrain → Service LAWIM → Paiement Campay → Conversion → Historisation
```

**Attribution Model:** Last-touch attribution

#### EXT-WF-012: Agent Invitation (7 states)

```
Invitation → Secure Link → Account Creation → Phone Verified → CNI Uploaded → LAWIM Validation → Agent actif
```

**Member Departure:** Remove org permissions, keep personal history and audit traces, transfer open dossiers

#### EXT-WF-013: Identity Resolution (5 states)

```
Potential Match Detected → Confidence Evaluation → Human Review (if needed) → Merged / False Positive Discarded
```

**Match Signals:** Phone, email, name, device fingerprint

#### EXT-WF-014: Main Cross-cutting Workflow (9 states)

```
Projet immobilier → Création dossier → Qualification → Matching → Mise en relation 
→ Visite → Négociation → Transaction → Clôture → Archivage
```

This is the **orchestrator** that delegates to all sub-workflows (Dossier, Matching, Contact, Visit, Negotiation, Transaction, Closure).

---

## 6. Property Model (15+ concepts)

**Source:** PROPERTY_TYPE_CROSSWALK.md
**Status:** Multiple critical gaps

| Extension ID | Concept | Gold Reference | Business Reason | Proposed Target | Priority |
|---|---|---|---|---|---|
| EXT-PROP-001 | Property families (7 families) | GOLD-PR-001 to GOLD-PR-007 | Classification backbone for all property logic | Add `property_family` enum: residential, commercial, industrial, land, agricultural, hotel, project | P0 |
| EXT-PROP-002 | Property type hierarchy | GOLD-PR-034 to GOLD-PR-044 | 11 basic types with sub-referentials | Create `PROPERTY_TYPES` enum; store subtype in metadata_json | P0 |
| EXT-PROP-003 | Full matrix types (107) | MATRIX_CATALOG.md | 107 qualification matrices require type granularity | Link property types to qualification matrix catalog | P2 |
| EXT-PROP-004 | 10-step property lifecycle | GOLD-PR (lifecycle) | Réception → Normalisation → Classification → Validation → Publication → Matching → Mise en relation → Suivi → Archivage → Conservation | Extend property state machine from 5 to 10+ states | P1 |
| EXT-PROP-005 | Publication rules (8 rules) | GOLD-PR-062 to GOLD-PR-069 | Family, type, location, price, détenteur, normalization, documents, code checks | Expand `can_publish()` from 3 checks to 8 rules | P1 |
| EXT-PROP-006 | Price concepts (6 levels) | GOLD-PR-070 to GOLD-PR-075 | Prix affiché, négociable, final, estimation, fourchette, historique | Extend price model beyond min/max | P1 |
| EXT-PROP-007 | Additional price types (7) | GOLD-PR-076 to GOLD-PR-082 | Loyer, caution, avance, dépôt garantie, mensualité, frais service, taxes | Add price type fields or metadata_json storage | P2 |
| EXT-PROP-008 | Data quality scoring | GOLD-PR (quality) | completeness*0.6 + reliability*0.4 → grade A+ to D | Implement quality scoring engine | P2 |
| EXT-PROP-009 | Per-type specific fields | GOLD-PR (per-type) | Industrial: access_camion, hauteur_plafond; Land: title_status, is_constructible | Add per-type field schemas in metadata_json | P1 |
| EXT-PROP-010 | Availability state machine | GOLD-PR (availability) | Enforce availability transitions (available→pending→rented/sold→archived) | Implement state machine validation | P2 |
| EXT-PROP-011 | Auto-archive (90 days) | GOLD-PR (auto-archive) | Stale properties auto-archived after 90 days inactivity | Implement auto-archive cron job | P2 |
| EXT-PROP-012 | Investment types (5) | CW-INV-001 to CW-INV-005 | investissement_locatif, terrain, commercial, promotion, syndicat | Add investment-specific property handling | P3 |
| EXT-PROP-013 | Agricultural family | GOLD-PR-005 | Full agricultural sub-referentiel | Add agricultural family and fields | P3 |
| EXT-PROP-014 | Hotelier family | GOLD-PR-006 | Dedicated hotelier family vs commercial type | Add hotel family with specific fields | P3 |
| EXT-PROP-015 | Project family | GOLD-PR-007 | Development project as property family | Link Property to Project for development properties | P3 |

---

## 7. Intent Detection (6 concepts)

**Source:** INTENT_TRANSACTION_CROSSWALK.md
**Status:** 6/6 EXTENSION_REQUIRED

| Extension ID | Concept | Gold Reference | Business Reason | Proposed Target | Priority |
|---|---|---|---|---|---|
| EXT-INT-001 | Keyword-based intent detection | INTENT_MODEL.md | Automatically detect user intent from natural language input | Implement intent classifier KLASS with FR/EN/PID keyword dictionaries | P1 |
| EXT-INT-002 | Confidence threshold (0.70) | INTENT_MODEL.md | Rule-based classification with minimum confidence for intent assignment | Implement configurable confidence threshold with fallback mechanism | P1 |
| EXT-INT-003 | Multi-intent detection | INTENT_MODEL.md | Support multiple parallel intents in single user utterance | Allow parallel project creation from multi-intent input | P2 |
| EXT-INT-004 | Urgency detection | INTENT_MODEL.md | Detect urgency from temporal keywords in user input | Add urgency scoring to intent detection pipeline | P2 |
| EXT-INT-005 | Entity extraction per intent | INTENT_MODEL.md | Extract budget, location, property type, timeline per intent | Implement per-intent entity extraction for qualification auto-population | P2 |
| EXT-INT-006 | Intent-to-role mapping | INTENT_MODEL.md | Map detected intent to platform role (buyer/tenant/seller/investor/visitor) | Implement Intent model with role mapping layer | P2 |

### 7.1 Additional Transaction Types (8 concepts)

| Extension ID | Transaction Type | Gold Reference | Current V2 Type | Priority |
|---|---|---|---|---|
| EXT-TRX-001 | short_stay | MATRIX_CATALOG.md | subsumed by 'rent' | P2 |
| EXT-TRX-002 | lease (bail 3+ ans) | MATRIX_CATALOG.md | subsumed by 'rent' | P2 |
| EXT-TRX-003 | cession_bail | MATRIX_CATALOG.md | 'other' (unmapped) | P3 |
| EXT-TRX-004 | bail_commercial | MATRIX_CATALOG.md | subsumed by 'rent' | P2 |
| EXT-TRX-005 | cession (fonds de commerce) | MATRIX_CATALOG.md | 'other' (unmapped) | P3 |
| EXT-TRX-006 | finance | MATRIX_CATALOG.md | subsumed by 'buy'/'invest' | P2 |
| EXT-TRX-007 | find (professional search) | MATRIX_CATALOG.md | 'other' (unmapped) | P2 |
| EXT-TRX-008 | service (real estate service) | MATRIX_CATALOG.md | 'other' (unmapped) | P2 |

---

## 8. Qualification Engine (107 matrices)

**Source:** INTENT_TRANSACTION_CROSSWALK.md, MATRIX_CATALOG.md
**Status:** 107/107 EXTENSION_REQUIRED

| Extension ID | Concept | Matrices Count | Business Reason | Priority |
|---|---|---|---|---|
| EXT-QUAL-001 | Residential Search matrices | 18 | Core buyer/tenant qualification | P1 |
| EXT-QUAL-002 | Land Search matrices | 7 | Land buyer qualification | P1 |
| EXT-QUAL-003 | Commercial Search matrices | 21 | Commercial property qualification | P2 |
| EXT-QUAL-004 | Investment matrices | 5 | Investor qualification | P2 |
| EXT-QUAL-005 | Financing Request matrices | 10 | Financing qualification | P2 |
| EXT-QUAL-006 | Professional Search matrices | 27 | FIND-type professional service qualification | P2 |
| EXT-QUAL-007 | Real Estate Service matrices | 24 | SERVICE-type real estate service qualification | P2 |
| EXT-QUAL-008 | Field dictionary with matching roles | All matrices | Per-field role mapping for qualification | P2 |
| EXT-QUAL-009 | Question priority system | All matrices | Priority weighting for qualification questions | P2 |
| EXT-QUAL-010 | Progressive qualification order (10 steps) | QUALIFICATION_MODEL.md | Intention → Type → Ville → Quartier → Budget → Délai → Critères → Préférences → Confirmation → Escalade | P1 |
| EXT-QUAL-011 | Per-channel adaptation | QUALIFICATION_MODEL.md | WhatsApp: 1 question, Telegram: 2-3, Dashboard: full form | P2 |

---

## 9. CRM (15+ concepts)

**Source:** WORKFLOW_STATE_CROSSWALK.md §2.18, CRM_MODEL.md
**Status:** Full implementation required

| Extension ID | Concept | Gold Reference | Business Reason | Priority |
|---|---|---|---|---|
| EXT-CRM-001 | Lead scoring engine | CRM_MODEL.md | Base score + boosters - penalties = final score | P1 |
| EXT-CRM-002 | Score boosters (13) | CRM_MODEL.md | budget_detected(+15), city(+10), neighborhood(+10), urgency(+20), diaspora(+25), cash(+15), etc. | P1 |
| EXT-CRM-003 | Score penalties (8) | CRM_MODEL.md | missing_budget(-10), unclear_location(-10), spam(-50), too_short(-20), external_links(-30), etc. | P1 |
| EXT-CRM-004 | Lead classification (5 classes) | CRM_MODEL.md | HOT, WARM, COLD, LOW, SPAM | P1 |
| EXT-CRM-005 | CRM routing engine | CRM_MODEL.md | Route classified leads to appropriate agents/queues | P1 |
| EXT-CRM-006 | 7-factor CRM scoring | CRM_MODEL.md | Multi-dimensional scoring across 7 factors | P2 |
| EXT-CRM-007 | Behavior tracking | CRM_MODEL.md | message_history, response_time, budget_changes, visit_requests | P2 |
| EXT-CRM-008 | Anti-fraud layers | CRM_MODEL.md | broker_spam, duplicate_listing, fake_price, suspicious_urgency | P2 |
| EXT-CRM-009 | Agent rating system | CRM_MODEL.md §13 | Post-interaction agent quality rating | P2 |
| EXT-CRM-010 | Feedback handling | CRM_MODEL.md §13 | Customer satisfaction collection and analysis | P3 |
| EXT-CRM-011 | Lead SLA by priority | CRM_MODEL.md | P0: <30min, P1: <2h, P2: <24h, P3: J+1 to J+7 | P1 |

### 9.1 Lead Types with Base Scores

| Lead Type | Base Score | Description |
|-----------|-----------|-------------|
| tenant | 40 | Rental seeker |
| buyer | 60 | Property buyer |
| seller | 50 | Property seller |
| investor | 80 | Real estate investor |
| diaspora_investor | 95 | Diaspora investor (highest priority) |

---

## 10. Matching (15+ concepts)

**Source:** WORKFLOW_STATE_CROSSWALK.md §2.03
**Status:** Full implementation required

| Extension ID | Concept | Gold Reference | Business Reason | Priority |
|---|---|---|---|---|
| EXT-MAT-001 | Full matching engine | MATCHING_MODEL.md | Algorithmic property-demandeur matching | P1 |
| EXT-MAT-002 | 5 scoring dimensions | MATCHING_MODEL.md | Real Estate (25/20/15/15/15/10), Availability, Document, Holder Reliability, Transaction Success | P1 |
| EXT-MAT-003 | Geographic scoring (5 levels) | MATCHING_MODEL.md | Location-based matching with distance tiers | P1 |
| EXT-MAT-004 | 4 compatibility levels | MATCHING_MODEL.md | Excellent, Good, Average, Low | P1 |
| EXT-MAT-005 | Rematching rules | MATCHING_MODEL.md | Automatic rematching on refusal, visit failure, negotiation failure | P1 |
| EXT-MAT-006 | Exclusion criteria | MATCHING_MODEL.md | Properties excluded based on incompatible criteria | P1 |
| EXT-MAT-007 | Transaction success score | MATCHING_MODEL.md | Predicted transaction success probability | P2 |
| EXT-MAT-008 | Market tension index | MATCHING_MODEL.md | Supply/demand ratio per market segment | P2 |
| EXT-MAT-009 | Dossier health score | MATCHING_MODEL.md | Quality and completeness score for demandeur dossier | P2 |
| EXT-MAT-010 | Property health score | MATCHING_MODEL.md | Quality score for property listing | P2 |
| EXT-MAT-011 | 9 matching roles | MATCHING_MODEL.md | Specific roles for demandeur, holder, agent, etc. | P1 |
| EXT-MAT-012 | Progressive search expansion | MATCHING_MODEL.md | Expand search criteria when matches insufficient | P2 |
| EXT-MAT-013 | Continuous market surveillance | MATCHING_MODEL.md | Monitor new properties against existing dossiers | P2 |

---

## 11. SLA & NBA (10+ concepts)

**Source:** WORKFLOW_STATE_CROSSWALK.md §4, §5
**Status:** Full implementation required

### 11.1 SLA Concepts

| Extension ID | Concept | Example Thresholds | Business Reason | Priority |
|---|---|---|---|---|
| EXT-SLA-001 | SLA per property type | 24h → 1095d rotation | Market timing varies by property category | P2 |
| EXT-SLA-002 | SLA per workflow state | Per entity/state thresholds | Time-in-state enforcement across all workflows | P2 |
| EXT-SLA-003 | Priority-based SLAs | P0=30min, P1=2h, P2=24h, P3=J+7 | Lead response time guarantees | P1 |
| EXT-SLA-004 | Breach detection engine | Configurable check frequency | Monitor and escalate SLA violations | P2 |
| EXT-SLA-005 | 3-tier escalation | NOTIFY → NBA_RECALCULATE → ESCALATE | Progressive escalation on breach | P2 |
| EXT-SLA-006 | Hold silence escalation | Reminder 1→2→3→Property to confirm→Rematch | Holder non-response management | P2 |

### 11.2 NBA (Next Best Action) Concepts

| Extension ID | Concept | Gold Reference | Business Reason | Priority |
|---|---|---|---|---|
| EXT-NBA-001 | NBA per state per workflow | WORKFLOW_CROSSWALK §5 | State-specific recommended next actions | P2 |
| EXT-NBA-002 | 9-level NBA priority system | WORKFLOW_CROSSWALK §5 | CORRECT_INCOHERENCE(1) → HUMAN_ESCALATION(9) | P2 |
| EXT-NBA-003 | Follow-up calendar | J1, J7, J30, J90 | Structured follow-up intervals for negotiations | P2 |
| EXT-NBA-004 | SLA breach → NBA recalculation | WORKFLOW_CROSSWALK §4 | NBA changes when SLA is at risk | P2 |

---

## 12. Permission Model (4 concepts)

**Source:** ROLE_CROSSWALK.md §2.3
**Status:** 1/4 EXTENSION_REQUIRED, 3/4 PARTIAL_MATCH

| Extension ID | Concept | Gold Reference | Business Reason | Proposed Target | Priority |
|---|---|---|---|---|---|
| EXT-PERM-001 | Niveau 4 — Validation (Approve) | GOLD-RL-017 | Formal approval workflow for agency creation, listing validation, professional verification | Implement ApprovalWorkflow model with approver_role, target_type, target_id, status, reviewed_by, reviewed_at | P1 |
| EXT-PERM-002 | Niveau 1 — Lecture (Read) | GOLD-RL-014 | Formalize implicit read access (currently PARTIAL) | Implement explicit permission check system | P2 |
| EXT-PERM-003 | Niveau 2 — Création (Create) | GOLD-RL-015 | Formalize implicit create access (currently PARTIAL) | Formalize Create permission level per role | P2 |
| EXT-PERM-004 | Niveau 3 — Modification (Edit) | GOLD-RL-016 | Formalize edit scope (own vs. managed vs. all) | Formalize Edit permission scope | P2 |

---

## 13. Appendix: Extension Catalog

### 13.1 Complete Extension ID Reference

| Prefix | Domain | Count |
|--------|--------|-------|
| EXT-RL-TRUST | Trust Levels | 6 |
| EXT-RL-BADGE | Badges | 8 |
| EXT-RL-AGENCY | Agency Structure | 9 |
| EXT-SVC-MON | Monetized Services | 13 |
| EXT-SVC-RES | Real Estate Services | 24 |
| EXT-SVC-PRO | Professional Services | 12 |
| EXT-SVC-CRM | CRM Monetized Services | 9 |
| EXT-SVC-LIFE | Service & Payment Lifecycle | 2 |
| EXT-WF | Workflows | 14 |
| EXT-PROP | Property Model | 15 |
| EXT-INT | Intent Detection | 6 |
| EXT-TRX | Transaction Types | 8 |
| EXT-QUAL | Qualification Engine | 11 |
| EXT-CRM | CRM | 11 |
| EXT-MAT | Matching | 13 |
| EXT-SLA | SLA | 6 |
| EXT-NBA | NBA | 4 |
| EXT-PERM | Permission Model | 4 |
| **Total** | | **175** |

### 13.2 Priority Distribution

| Priority | Count | Action |
|----------|-------|--------|
| P0 | 2 | Property families and types — blocking |
| P1 | 45+ | Core business logic — MVP critical |
| P2 | 55+ | Important functionality — near-term |
| P3 | 30+ | Valuable enhancement — medium-term |
| P4 | 25+ | Nice-to-have — backlog |

### 13.3 Implementation Phases

| Phase | Focus | Extensions | Estimated Effort |
|-------|-------|------------|------------------|
| Phase 0: Foundation | Property families, types, basic state machine | EXT-PROP-001, EXT-PROP-002, EXT-PROP-004 | 2-3 weeks |
| Phase 1: Core Business | Trust, matching, CRM, monetization, intent detection | EXT-RL-TRUST, EXT-WF-001/003/004/008, EXT-SVC-MON, EXT-INT | 8-12 weeks |
| Phase 2: Operations | Agency, onboarding, disputes, NBA, SLA | EXT-RL-AGENCY, EXT-WF-006/012, EXT-NBA, EXT-SLA | 6-8 weeks |
| Phase 3: Analytics | SIE pipelines, conversion, quality scoring | EXT-WF-009/010/011, EXT-PROP-008 | 4-6 weeks |
| Phase 4: Enhancement | Mediation, identity resolution, remaining services | EXT-WF-007/013, EXT-SVC-PRO, remaining | 4-6 weeks |

### 13.4 Crosswalk References

| Crosswalk Document | Extensions Referenced |
|--------------------|-----------------------|
| ROLE_CROSSWALK.md | EXT-RL-TRUST-*, EXT-RL-BADGE-*, EXT-RL-AGENCY-*, EXT-PERM-* |
| PROPERTY_TYPE_CROSSWALK.md | EXT-PROP-* |
| SERVICE_CROSSWALK.md | EXT-SVC-* |
| WORKFLOW_STATE_CROSSWALK.md | EXT-WF-*, EXT-MAT-*, EXT-CRM-*, EXT-SLA-*, EXT-NBA-* |
| INTENT_TRANSACTION_CROSSWALK.md | EXT-INT-*, EXT-TRX-*, EXT-QUAL-* |

---

*End of REQUIRED_EXTENSIONS.md — 175 extension concepts cataloged across 18 domains.*
