# SEMANTIC CONFLICTS — Heritage Gold vs LAWIM_V2

**Document ID:** LAWIM-HARM-CONFLICTS-V1
**Status:** CANONICAL — Definitive catalog of semantic contradictions between Heritage Gold and current LAWIM_V2
**Date:** 2026-07-15

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Conflict 1: Role Model — Hierarchy vs Flat](#2-conflict-1-role-model--hierarchy-vs-flat)
3. [Conflict 2: Property Type — Taxonomy vs Free-Form](#3-conflict-2-property-type--taxonomy-vs-free-form)
4. [Conflict 3: Workflow State Machine — Rich vs Simplified](#4-conflict-3-workflow-state-machine--rich-vs-simplified)
5. [Conflict 4: Transaction vs Project — Different Paradigms](#5-conflict-4-transaction-vs-project--different-paradigms)
6. [Conflict 5: Dossier vs Project — Different Entity Focus](#6-conflict-5-dossier-vs-project--different-entity-focus)
7. [Conflict 6: Service Model — Business Model vs No Model](#7-conflict-6-service-model--business-model-vs-no-model)
8. [Conflict 7: CRM Model — Rich vs Minimal](#8-conflict-7-crm-model--rich-vs-minimal)
9. [Conflict 8: Intent Detection — Pipeline vs None](#9-conflict-8-intent-detection--pipeline-vs-none)
10. [Conflict 9: Permission Model — Granular vs Simple](#10-conflict-9-permission-model--granular-vs-simple)
11. [Conflict 10: Matching Roles — Engine vs None](#11-conflict-10-matching-roles--engine-vs-none)
12. [Conflict 11: Price Model — Multi-Level vs Range](#12-conflict-11-price-model--multi-level-vs-range)
13. [Conflict 12: Property Lifecycle — 13 States vs 5 Statuses](#13-conflict-12-property-lifecycle--13-states-vs-5-statuses)
14. [Conflict 13: Data Model — Relational vs Free-Form](#14-conflict-13-data-model--relational-vs-free-form)
15. [Appendix: Resolution Decision Log](#15-appendix-resolution-decision-log)

---

## 1. Executive Summary

This document identifies and analyzes **semantic conflicts** — situations where Heritage Gold and current LAWIM_V2 define contradictory models for the same or overlapping domain concepts. Unlike gaps (where a concept simply doesn't exist in V2), conflicts require deliberate resolution: choosing one model, reconciling both, or defining a new model that supersedes both.

### 1.1 Conflict Severity Legend

| Severity | Definition | Action Required |
|----------|-----------|-----------------|
| CRITICAL | Fundamental architectural contradiction | Architectural decision required before any implementation |
| HIGH | Major structural conflict affecting multiple sub-domains | Design decision required; impacts multiple teams |
| MEDIUM | Significant but localized contradiction | Technical decision required; impacts single domain |
| LOW | Minor semantic difference | Can be resolved during implementation |

### 1.2 Summary of Conflicts

| # | Conflict | Severity | Heritage Gold Position | LAWIM_V2 Position | Decision Status |
|---|----------|----------|----------------------|-------------------|-----------------|
| 1 | Role Model | CRITICAL | 6 families + 7 levels + hierarchy | 5 official roles + 27 business profiles (flat) | PENDING |
| 2 | Property Type | CRITICAL | 7 families with sub-referentials | Free-form string | PENDING |
| 3 | Workflow State Machine | HIGH | Property: 13 states, Dossier: 14 states | Property: 5 statuses, Project: 5 statuses | PENDING |
| 4 | Transaction vs Project | HIGH | "Transaction" is core entity with lifecycle | "Project" is core organizing concept | PENDING |
| 5 | Dossier vs Project | HIGH | "Dossier" with matching lifecycle | "Project" with journey steps | PENDING |
| 6 | Service Model | HIGH | 13 paid services + payment lifecycle | No service model at all | PENDING |
| 7 | CRM Model | HIGH | 8-stage pipeline + scoring + routing + anti-fraud | Basic User + Organization model | PENDING |
| 8 | Intent Detection | HIGH | Full intent detection pipeline | No intent detection | PENDING |
| 9 | Permission Model | MEDIUM | 4-level explicit permission matrix | Flat role aliases, implicit permissions | PENDING |
| 10 | Matching Roles | HIGH | 9 matching roles + full scoring engine | No matching engine | PENDING |
| 11 | Price Model | MEDIUM | 6 price levels + 7 price types | price_min / price_max range only | PENDING |
| 12 | Property Lifecycle | HIGH | 10-step enrichment pipeline | 5 generic statuses | PENDING |
| 13 | Data Model | MEDIUM | Strongly-typed, relational, normalized | Free-form strings, metadata_json, flexible | PENDING |

---

## 2. Conflict 1: Role Model — Hierarchy vs Flat

### 2.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Structure | 6 families, 7 hierarchical levels (L1-L7) | 5 flat official roles |
| Role Hierarchy | L1: demandeur → L7: master (inheritance chain) | No hierarchy; admin > manager > operator > partner > user (implicit) |
| Permission Model | 4 explicit levels (Read/Create/Edit/Approve) | Implicit per-role permissions |
| Trust Levels | 6 graduated trust levels with validation workflow | Not implemented |
| Badges | 8 visual trust badges | Not implemented |
| Agency Roles | resp. → admin → agent → assistant (4-tier) | No agency-level role distinction |
| Partner Roles | 7 partner types (notaire, géomètre, banque, etc.) | 1 partner role + business profiles |

### 2.2 Nature of Conflict

**CONFLICT:** Heritage Gold defines a **rich hierarchical role taxonomy** with inheritance (Level N inherits from Level N-1), explicit permission levels per role, trust levels, and badges. LAWIM_V2 uses a **flat role model** with 5 official roles and 27 business profiles as role aliases/labels.

The fundamental contradiction is:
- **Hierarchy vs Flat:** Gold models roles as a tree (inheritance, escalation); V2 models roles as a set (flat, assignment-based)
- **Permission Levels vs Role Aliases:** Gold ties permissions to role hierarchy levels; V2 treats business profiles as descriptive labels with no permission implications
- **Trust Graduation vs Binary Status:** Gold has 6 trust levels; V2 has no trust concept

### 2.3 Risk if Heritage Gold Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| V2 business_profile system must be refactored or deprecated | HIGH — 27 profiles used across codebase | HIGH |
| Role/permission checks throughout V2 codebase need rewriting | HIGH — hundreds of isAdmin/isOperator checks | HIGH |
| Current User model lacks trust_level, verification fields | MEDIUM — schema migration needed | CERTAIN |
| Agent/agency relationship model needs extension | MEDIUM — organization membership rework | HIGH |
| Migration complexity for existing users with flat roles | HIGH — every user needs hierarchy level assignment | HIGH |

### 3.4 Proposed Solution (Reconciliation)

**Adopt LAWIM_V2 as the base role system** with the following enhancements:

1. **Keep V2's 5 official roles** as the core permission-bearing structure
2. **Add optional `trust_level` (INT 1-6)** to User model for trust graduation
3. **Add optional `badges` (JSON array)** derived from verification flags
4. **Add optional `agency_role`** to Organization membership for agency hierarchy
5. **Map Gold hierarchy levels to V2 roles** via a lookup table (not inheritance)
6. **Extend business_profiles** with missing artisan roles (macon, menuisier, etc.)
7. **Implement explicit Permission model** with 4 levels (Read/Create/Edit/Approve) mapped to official roles

### 2.4 Risk if LAWIM_V2 Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Trust graduation cannot be expressed | MEDIUM — missing fraud prevention signal | CERTAIN |
| Permission granularity limited to 5 levels | MEDIUM — no fine-grained access control | HIGH |
| Agency hierarchy (resp./admin/agent/assistant) cannot be modeled | MEDIUM — agency management incomplete | HIGH |
| Badge system cannot be implemented | LOW — cosmetic/trust signaling only | HIGH |
| Role inheritance business rules lost | LOW — can be simulated with role mapping | MEDIUM |

### 2.5 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Role hierarchy or flat roles? | (a) Implement Gold hierarchy, (b) Keep V2 flat, (c) Hybrid with mapping layer | Architectural — affects all role-based logic |
| Trust level system scope? | (a) Full 6-level implementation, (b) Simplified verification flags only, (c) Defer | Security — affects fraud prevention |
| Permission model format? | (a) Explicit 4-level permission matrix, (b) Keep implicit, (c) Hybrid with role-permission mapping | Security — affects access control |

---

## 3. Conflict 2: Property Type — Taxonomy vs Free-Form

### 3.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Families | 7 well-defined families with sub-referentials (residential, commercial, industrial, land, agricultural, hotel, project) | No family concept |
| Type Validation | 11 basic types + 41 matrix types with full validation | Free-form string (propertyType) — any value accepted |
| Sub-types | Sub-referentials per family (residential: 18 types; land: 7 types; commercial: 16 types) | No subtype system |
| Per-type Fields | Specific fields per type (industrial: access_camion, hauteur_plafond; land: title_status, is_constructible) | 3 generic fields (surface, bedrooms, bathrooms) |
| Inheritance | Master property model with type-specific extensions | Single flat Property model |

### 3.2 Nature of Conflict

**CONFLICT:** Heritage Gold defines a **rigid, validated taxonomy** with 7 families, 11+ basic types, sub-referentials per family, and type-specific fields. LAWIM_V2 uses a **flexible free-form string** for property type.

The fundamental contradiction is:
- **Rigid Taxonomy vs Flexible String:** Gold enforces type validity; V2 accepts any string
- **Structured vs Unstructured:** Gold has family-specific fields and validation; V2 has a single flat model
- **Enforcement vs Freedom:** Gold prevents invalid type combinations; V2 allows any combination

### 3.3 Risk if Heritage Gold Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| All existing properties with free-form types need migration | HIGH — type mapping and cleanup needed | CERTAIN |
| Current Property model schema must add property_family field | MEDIUM — Prisma migration | CERTAIN |
| metadata_json storage pattern must be standardized | MEDIUM — schema governance needed | HIGH |
| API consumers must adapt to enum-based type values | MEDIUM — breaking change for integrators | HIGH |

### 3.4 Risk if LAWIM_V2 Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Cannot run family-specific business logic | HIGH — matching, qualification, publication all affected | CERTAIN |
| Cannot validate property type coherence | HIGH — invalid type combinations possible | CERTAIN |
| Cannot apply 107 qualification matrices without type granularity | HIGH — qualification engine unusable | CERTAIN |
| Cannot enforce type-specific publication rules | MEDIUM — family, type, document rules unenforceable | HIGH |
| Type-based search filtering impossible | MEDIUM — must use text matching | HIGH |

### 3.5 Proposed Solution (Reconciliation)

**Adopt Heritage Gold taxonomy as the canonical type system** but implement incrementally:

1. **Phase 1 (Immediate):** Add `property_family` enum to Property model with 7 families
2. **Phase 1 (Immediate):** Create `PROPERTY_TYPES` enum set for validation
3. **Phase 2 (Short-term):** Add subtype validation and per-type field schemas in metadata_json
4. **Phase 2 (Short-term):** Implement type-to-family coherence rules
5. **Phase 3 (Medium-term):** Add per-type specific fields as optional typed columns
6. **Migration:** Free-form types → validated enum; unknown types → `other` family with metadata preservation

### 3.6 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Property type validation approach? | (a) Strict enum (Gold), (b) Free string + metadata (V2), (c) Enum + metadata fallback | Architectural — affects all property logic |
| Family field granularity? | (a) 7 families exact, (b) Simplified (residential/commercial/land only), (c) Defer | Functional — affects classification |
| Per-type field implementation? | (a) Typed schema columns, (b) metadata_json only, (c) Hybrid (core fields typed, rest JSON) | Technical — affects query performance |

---

## 4. Conflict 3: Workflow State Machine — Rich vs Simplified

### 4.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Property States | 13 states (Création → Qualification → Validation → Publié → Disponible → Matching → Visites → Négociation → Réservé → Transaction → Indisponible → Réactivation → Archivé) | 5 statuses (draft, open, closed, published, archived) + 5 availability states |
| Dossier States | 14 states with wait states, double consent, decision tracking | 5 project statuses (draft, active, paused, completed, archived) |
| Transition Guards | Multiple guards per transition (health scores, coherence, consent) | Single guard: can_publish() |
| Audit Events | 12+ typed audit events per workflow | Generic Event model (kind, payload) |
| SLA Rules | Per-state, per-entity SLA thresholds with breach detection | None |
| NBA | State-specific Next Best Actions with 9-level priority | derive_next_actions() for pending steps |

### 4.2 Nature of Conflict

**CONFLICT:** Heritage Gold defines **rich, highly-structured state machines** with 10-14 states per workflow, typed events, SLA enforcement, NBA, and multi-condition guards. LAWIM_V2 uses **simplified 5-state status machines** with free-form transitions and no SLA/NBA layer.

The fundamental contradiction:
- **Rich Lifecycle vs Simplified States:** Gold models every business stage explicitly; V2 compresses into generic statuses
- **Enforced Transitions vs Free Transitions:** Gold has guarded state transitions; V2 allows nearly any state-to-state transition
- **Event-Driven vs Status-Based:** Gold uses typed events to drive transitions; V2 uses status assignment

### 4.3 Risk if Heritage Gold Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Current V2 state machines must be completely rewritten | HIGH — property_domain.py, project_domain.py, conversation_domain.py all affected | CERTAIN |
| All existing entities in V2 states must be migrated to Gold states | HIGH — data migration for all properties, projects, conversations | CERTAIN |
| Complexity increases significantly — more states, guards, events, SLAs | HIGH — development and maintenance cost | CERTAIN |
| API surface changes for all state-related endpoints | MEDIUM — breaking API changes | HIGH |

### 4.4 Risk if LAWIM_V2 Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Missing matching, visit, transaction states block core business flows | HIGH — cannot implement key platform features | CERTAIN |
| No double consent workflow — legal/compliance risk for contact establishment | HIGH — regulatory non-compliance | HIGH |
| No SLA enforcement — cannot guarantee service levels | MEDIUM — quality of service degradation | HIGH |
| Loss of business rules encoded in state guards | MEDIUM — rules must be re-implemented elsewhere | HIGH |
| No NBA engine — manual action recommendation only | LOW — operational efficiency loss | MEDIUM |

### 4.5 Proposed Solution (Reconciliation)

**Adopt Heritage Gold state machines as the canonical workflow specification** with pragmatic simplification:

1. **Phase 1 (Immediate):** Implement Matching, Visit, and Transaction state machines as new entities
2. **Phase 1 (Immediate):** Add double consent workflow to Contact/Mise en Relation
3. **Phase 2 (Short-term):** Extend Property states (add Qualification, Validation, Matching, Transaction states)
4. **Phase 2 (Short-term):** Extend Dossier/Project states (add wait states, decision tracking)
5. **Phase 3 (Medium-term):** Implement SLA registry and breach detection engine
6. **Phase 3 (Medium-term):** Implement NBA engine with 9-level priority
7. **Keep V2 states** as simplified surface for API consumers where appropriate; map between Gold and V2 states

### 4.6 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| State machine implementation strategy? | (a) Full Gold state machines, (b) Simplified V2 + key extensions, (c) Hybrid with mapping layer | Architectural — affects all workflow logic |
| Double consent enforcement? | (a) Mandatory for all contact, (b) Optional/configurable, (c) Defer | Legal/Compliance — affects regulatory requirements |
| SLA engine priority? | (a) Build with Phase 1, (b) Phase 2 enhancement, (c) Defer to Phase 3 | Operational — affects service quality guarantees |

---

## 5. Conflict 4: Transaction vs Project — Different Paradigms

### 5.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Core Entity | **Transaction** — end-to-end deal lifecycle | **Project** — organizing concept for user journeys |
| State Machine | 10 states (Accord → Préparation → Documents → Paiement → Signature → Remise des clés → Confirmation → Terminée / Échec) | 5 statuses (draft, active, paused, completed, archived) |
| Transaction Types | 6 types (Location, Vente, Achat, Bail professionnel, Bail commercial, Location saisonnière) | No transaction types |
| Document Handling | Per-type document requirements (sale: land title, ID; rental: contract, deposit) | No document workflow |
| Party Involvement | demandeur, agent, owner, notaire | Project creator (implicit) |
| Payment Integration | Campay Mobile Money integration | Feature flag payments=OFF |

### 5.2 Nature of Conflict

**CONFLICT:** Heritage Gold treats **"transaction" as the core deal-closing entity** with a dedicated lifecycle, document requirements, and party involvement. LAWIM_V2 uses **"project" as the organizing concept** that groups user journeys, with no dedicated transaction entity.

The fundamental contradiction:
- **Transaction-Centric vs Project-Centric:** Gold models the deal as a first-class entity; V2 models the user journey as first-class
- **Legal/Financial vs Journey/Tracking:** Gold focuses on the legal-financial closure process; V2 focuses on user intent and progress tracking
- **Structured vs Flexible:** Gold has structured transaction types with specific requirements; V2 has flexible project types with generic steps

### 5.3 Risk if Heritage Gold Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Project model must coexist with Transaction model — potential duplication | MEDIUM — both entities track similar concepts | HIGH |
| Current journey templates and step tracking may need restructuring | MEDIUM — project semantics change | HIGH |
| Existing projects in transaction-like states need mapping | MEDIUM — data migration | HIGH |

### 5.4 Risk if LAWIM_V2 Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| No legal/financial deal-closing entity — cannot track sale/rental execution | HIGH — core business requirement unmet | CERTAIN |
| Cannot enforce document requirements per transaction type | HIGH — legal risk for unverified documents | HIGH |
| No notary/party involvement tracking | MEDIUM — missing collaboration features | HIGH |
| No payment integration for transaction fees | MEDIUM — revenue leakage | HIGH |

### 5.5 Proposed Solution (Reconciliation)

**Add Transaction as a new entity** while preserving Project for user journey tracking:

1. **Create Transaction model** with 10-state lifecycle, document requirements, party roles
2. **Link Transaction to Project** (one Project may have zero or one Transaction)
3. **Keep Project** as the user-facing journey tracker with current step templates
4. **Implement document handling** per transaction type
5. **Integrate payment** processing for transaction-related fees
6. **Add party involvement** (demandeur, agent, owner, notaire) to Transaction

### 5.6 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Transaction entity creation? | (a) New Transaction model, (b) Extend Project with transaction semantics, (c) Defer | Architectural — affects data model |
| Project-Transaction relationship? | (a) 1:1 (one project → one transaction), (b) 1:N, (c) Unlinked | Functional — affects workflow integration |
| Document handling scope? | (a) Full per-type document requirements, (b) Generic document upload, (c) Defer | Legal — affects compliance |

---

## 6. Conflict 5: Dossier vs Project — Different Entity Focus

### 6.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Entity Name | **Dossier** — structured case file for a demandeur's property search | **Project** — user journey with configurable steps |
| State Count | 14 states (Création → Qualification → Matching → Présentation → Wait decisions → Mise en relation → Visite → Négociation → Accord → Transaction → Clôture → Archivage) | 5 states (draft, active, paused, completed, archived) |
| Lifecycle Focus | Matching lifecycle + double consent + holder decision chain | Journey step progression |
| Wait States | Dedicated wait states (Attente décision demandeur, Attente décision détenteur) | No wait states (paused is generic) |
| Rematching | Automatic rematching on refusal | No rematching concept |

### 6.2 Nature of Conflict

**CONFLICT:** Heritage Gold defines **"dossier" as a case file with a matching-centric lifecycle** involving double consent, holder decision tracking, and automatic rematching. LAWIM_V2 uses **"project" as a flexible journey tracker** with generic steps and no matching/consent logic.

### 6.3 Proposed Solution (Reconciliation)

**Extend Project model with dossier semantics** rather than creating a separate Dossier entity:

1. Keep `Project` as the entity name (avoid breaking API surface)
2. Add dossier-specific fields: `matching_status`, `double_consent_status`, `rematching_count`
3. Add wait states as explicit step statuses (waiting_demandeur, waiting_holder)
4. Implement rematching logic in project workflow
5. Add holder contact tracking to project participants

### 6.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Entity name? | (a) Keep "Project" with extended semantics, (b) Rename to "Dossier", (c) Create Dossier model + alias to Project | Communication — affects all documentation and API |
| Wait state implementation? | (a) New step statuses, (b) Paused with reason, (c) Sub-states | Functional — affects workflow UX |

---

## 7. Conflict 6: Service Model — Business Model vs No Model

### 7.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Service Catalog | 72 total: 13 monetized, 24 real estate, 27 professional, 8 CRM | No service catalog |
| Pricing | Fixed prices for all services (500-75,000 FCFA) | No pricing model |
| Payment Processing | Campay Mobile Money integration | Feature flag payments=OFF |
| Agent Credits | Agent credit system with boost purchases | No credit system |
| Revenue Model | Zero commission on transactions; revenue from platform services | No revenue model implemented |

### 7.2 Nature of Conflict

**CONFLICT:** Heritage Gold has a **complete commercial service model** with 72 services, fixed pricing, payment processing, agent credits, and a clear revenue model. LAWIM_V2 has **no service model** — no catalog, no pricing, no payment processing, no monetization.

This is not a mapping gap (extension required); it is a **business model conflict** because:
- Gold's revenue model (zero commission + paid services) contradicts any implicit assumption of commission-based revenue
- Gold's agent credit system implies lead purchasing; V2 has no costing concept
- Gold's pricing tiers (500-75,000 FCFA) reflect a specific market positioning that must be confirmed

### 7.3 Risk if Heritage Gold Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Full service infrastructure must be built from scratch | HIGH — Service, ServiceOrder, Payment, Credit models all new | CERTAIN |
| Current V2 monetization assumptions (if any) must be discarded | MEDIUM — business model alignment | CERTAIN |
| Campay integration required (Cameroonian payment processor) | MEDIUM — third-party integration dependency | HIGH |
| Pricing strategy must be validated for current market | MEDIUM — prices set in Gold may be outdated | HIGH |

### 7.4 Risk if LAWIM_V2 Prevails (No Service Model)

| Risk | Impact | Likelihood |
|------|--------|------------|
| No platform revenue — LAWIM cannot monetize | CRITICAL — business viability | CERTAIN |
| No lead purchase system — agents cannot acquire leads | HIGH — core value proposition broken | CERTAIN |
| No boost/premium — properties lack paid visibility | MEDIUM — reduced agent engagement | HIGH |
| No subscription — no recurring revenue | MEDIUM — reduced revenue predictability | HIGH |

### 7.5 Proposed Solution (Reconciliation)

**Adopt Heritage Gold service model as the business model specification:**

1. **Phase 1 (Immediate):** Implement `Service` and `ServiceOrder` Prisma models
2. **Phase 1 (Immediate):** Activate payments feature flag + Campay integration
3. **Phase 1 (Immediate):** Implement agent credit system (AgentCredit, LeadPurchase)
4. **Phase 2 (Short-term):** Add boost/premium to Property model
5. **Phase 2 (Short-term):** Implement lead pack purchase flow
6. **Phase 3 (Medium-term):** Add subscription management, diaspora packages
7. **Validate pricing** with current market analysis before activation

### 7.6 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Revenue model confirmation? | (a) Zero commission + paid services (Gold), (b) Commission model, (c) Hybrid | Business — affects entire monetization strategy |
| Payment processor? | (a) Campay (Gold — Cameroonian market), (b) Multi-processor, (c) Defer | Technical — affects payment integration |
| Pricing validation? | (a) Use Gold prices as-is, (b) Market analysis before setting prices, (c) Configurable pricing | Business — affects revenue and competitiveness |

---

## 8. Conflict 7: CRM Model — Rich vs Minimal

### 8.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Pipeline | 8-stage CRM pipeline (incoming → normalize → extract → detect intent → enrich → score → classify → route) | No CRM pipeline |
| Lead Scoring | Base score (25-95) + boosters (+10 to +25) + penalties (-10 to -50) = final score | No lead scoring |
| Lead Classification | HOT, WARM, COLD, LOW, SPAM | No classification |
| Routing | Geographic zone + agent availability + score-based routing | No routing |
| Anti-Fraud | 4 fraud detection layers + temporary suspension actions | No fraud detection |
| Behavior Tracking | message_history, response_time, budget_changes, visit_requests | No behavior tracking |
| Agent Rating | 1-5 star post-interaction rating | No agent rating |

### 8.2 Nature of Conflict

**CONFLICT:** Heritage Gold defines a **full CRM system** with scoring, classification, routing, fraud detection, and behavior tracking. LAWIM_V2 has a **basic User + Organization model** with no CRM capabilities.

This is a structural conflict because implementing CRM requires:
- New Lead entity (currently no lead concept)
- New scoring/routing infrastructure
- Integration with messaging/intent detection
- Anti-fraud service layer

### 8.3 Proposed Solution (Reconciliation)

**Adopt Heritage Gold CRM model** as the specification:

1. Implement Lead model with scoring fields
2. Build CRM pipeline as a service (8 stages)
3. Implement scoring engine (base + boosters - penalties)
4. Add lead classification logic
5. Build geographic routing engine
6. Implement anti-fraud detection layers
7. Add agent rating system

### 8.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| CRM implementation scope? | (a) Full 8-stage pipeline, (b) Basic scoring + classification only, (c) Minimal (leads only) | Functional — affects all CRM features |
| Anti-fraud implementation? | (a) Built-in (4 layers), (b) External service, (c) Defer | Security — affects platform trust |

---

## 9. Conflict 8: Intent Detection — Pipeline vs None

### 9.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Detection Method | Keyword-based scoring with 0.70 confidence threshold | None — explicit project_type selection |
| Language Support | FR, EN, PID (Pidgin) | N/A |
| Multi-Intent | Supported | Not supported |
| Urgency Detection | Temporal keyword analysis | Not detected |
| Entity Extraction | Per-intent (budget, location, type, timeline) | Not implemented |
| Fallback | SEARCH_PROPERTY when confidence < 0.70 | 'other' project type (no fallback logic) |
| Score Weights | BUY=50, RENT=30, SELL=60, INVEST=100, SEARCH=25 | No scoring |

### 9.2 Nature of Conflict

**CONFLICT:** Heritage Gold has a **complete intent detection pipeline** that automatically classifies user intent from natural language. LAWIM_V2 has **no intent detection** — users must explicitly select a project type from a form.

This conflict extends beyond "not implemented" because:
- Gold assumes chat-based interaction (WhatsApp/Telegram) where intent must be inferred
- V2 assumes form/dashboard interaction where user selects intent explicitly
- These are different user interaction paradigms, not just missing features

### 9.3 Proposed Solution (Reconciliation)

**Implement Heritage Gold intent detection as an optional layer** on top of explicit project_type selection:

1. **Build intent detection module** with keyword scoring (FR/EN/PID)
2. **Use 0.70 confidence threshold** with fallback to explicit selection
3. **Support multi-intent** → parallel project creation
4. **Add urgency detection** → priority scoring
5. **Add entity extraction** → qualification auto-population
6. **Map intent to role** for user journey personalization
7. Keep explicit project_type selection as the primary UX for dashboard users

### 9.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Interaction paradigm? | (a) Chat-first with intent detection (Gold), (b) Form-first with explicit selection (V2), (c) Hybrid (both) | UX — affects all user interfaces |
| Intent detection mandatory or optional? | (a) Required for all channels, (b) Chat only, (c) Configurable per channel | Technical — affects implementation scope |

---

## 10. Conflict 9: Permission Model — Granular vs Simple

### 10.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Permission Levels | 4 explicit levels: Read, Create, Edit, Approve | Implicit per-role; no permission model |
| Role → Permission Mapping | Explicit matrix per role family | Implicit in role definitions (isAdmin, isOperator checks) |
| Approval Workflow | Required for: agency creation, listing validation, professional verification | No approval workflow |
| Permission Scope | By item-under-responsibility (own, managed, org, all) | By ownership (own) or role (admin) |
| Audit | Permission checks logged | No permission audit |

### 10.2 Nature of Conflict

**CONFLICT:** Heritage Gold defines an **explicit 4-level permission model** with formal approval workflows. LAWIM_V2 has **implicit permissions** embedded in role definitions as hardcoded checks.

### 10.3 Proposed Solution (Reconciliation)

**Add explicit permission model** while preserving current role structure:

1. Implement Permission model or permission matrix
2. Map 4 permission levels to official roles
3. Implement ApprovalWorkflow model for approval-required actions
4. Formalize permission scope (own vs. managed vs. all)
5. Add permission audit logging

### 10.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Permission model format? | (a) Role-based permission matrix, (b) Attribute-based (ABAC), (c) Hybrid | Security — affects access control architecture |

---

## 11. Conflict 10: Matching Roles — Engine vs None

### 11.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Matching Engine | Full algorithmic engine with 5 scoring dimensions, ranking, proposals | No matching engine |
| Matching Roles | 9 roles (demandeur, holder, agent, etc.) with role-specific scoring | No matching roles |
| Score Dimensions | Real Estate (6 sub-dimensions), Availability, Document, Holder Reliability, Transaction Success | No scoring |
| Compatibility Levels | 4 levels: Excellent, Good, Average, Low | No compatibility model |
| Rematching | Automatic on refusal, visit failure, negotiation failure | No rematching |
| Market Intelligence | Market tension index, health scores | No market intelligence |

### 11.2 Nature of Conflict

**CONFLICT:** Heritage Gold has a **complete algorithmic matching engine** as the platform's core intelligence. LAWIM_V2 has **no matching engine** — properties are listed, and users search/contact manually.

This is the most critical business model conflict: matching is the core value proposition of LAWIM.

### 11.3 Proposed Solution (Reconciliation)

**Full implementation of Heritage Gold matching engine:**

1. Implement Match entity with score fields
2. Build 5-dimension scoring algorithm
3. Implement ranking and proposal system
4. Add rematching rules and triggers
5. Implement health scores (dossier, property)
6. Add market tension index
7. Implement progressive search expansion

### 11.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Matching engine strategy? | (a) Full Gold algorithm, (b) Simplified scoring, (c) External ML service | Architectural — core platform intelligence |
| Rematching automation? | (a) Fully automatic, (b) Semi-automatic (approval needed), (c) Manual only | UX — affects user control |

---

## 12. Conflict 11: Price Model — Multi-Level vs Range

### 12.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Price Fields | 6 levels: affiché, négociable, final, estimation, fourchette, historique | price_min, price_max |
| Additional Types | 7 types: loyer, caution, avance, dépôt, mensualité, frais, taxes | Not distinguished |
| Negotiability | Explicit negotiable flag + negotiable price | Not modeled |
| Price History | Historical price variation tracking | Not implemented |
| Currency | normalize_currency() supports XAF, EUR, USD, GBP, XOF | Currency field exists |

### 12.2 Nature of Conflict

**CONFLICT:** Heritage Gold requires **6 price levels + 7 price types** for comprehensive property pricing. LAWIM_V2 stores only a **price range (min/max)**.

### 12.3 Proposed Solution (Reconciliation)

**Extend price model** with Gold concepts:

1. Add `price_displayed` (single displayed price)
2. Add `negotiable` Boolean + `price_negotiable`
3. Add `price_final` for closed deals
4. Add `price_estimation` for valuation
5. Store price history in metadata_json
6. Add price type classification (rent/sale/deposit/etc.)

### 12.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Price model extension? | (a) All Gold price fields, (b) Selected fields (affiché + négociable only), (c) metadata_json storage | Financial — affects pricing capabilities |

---

## 13. Conflict 12: Property Lifecycle — 13 States vs 5 Statuses

### 13.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Total States | 13 states across workflow and availability | 5 statuses + 5 availability states (overlapping) |
| Enrichment Pipeline | Création → Qualification → Validation (3-step before publication) | draft → published (compressed) |
| Commercial Pipeline | Matching → Visites → Négociation → Réservé → Transaction (5-step) | Not modeled |
| Reactivation | Explicit Réactivation éventuelle state | No reactivation concept |
| Auto-Archive | 90-day inactivity auto-archive | Not implemented |

### 13.2 Nature of Conflict

**CONFLICT:** Heritage Gold property lifecycle has **3x more states** than V2, with specific enrichment and commercial pipeline stages that V2 compresses into generic statuses.

### 13.3 Proposed Solution (Reconciliation)

**Extend Property state machine** to include key Gold states:

1. Add Qualification, Validation states to enrichment pipeline
2. Add Matching, Visit, Transaction states to commercial pipeline
3. Add reactivation workflow
4. Implement auto-archive (90-day rule)
5. Keep backward compatibility with existing status values via mapping

### 13.4 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| State machine expansion? | (a) Full 13 states, (b) Key states only (Qualification, Validation, Transaction), (c) Keep 5 + metadata | Functional — affects property workflow |

---

## 14. Conflict 13: Data Model — Relational vs Free-Form

### 14.1 Overview

| Aspect | Heritage Gold | LAWIM_V2 |
|--------|---------------|----------|
| Philosophy | Strongly-typed, relational, normalized | Flexible, metadata_json for extensibility |
| Property Type | Enum with validation | Free-form string |
| Price Model | 6 typed price fields | metadata_json (price_min, price_max) |
| Per-type Fields | Specific typed fields per family | metadata_json |
| State Machine | Formal state machine with guarded transitions | Status string + free transitions |
| Key-Value Storage | Minimal — normalized where possible | Extensive use of metadata_json |

### 14.2 Nature of Conflict

**CONFLICT:** Heritage Gold favors **relational normalization and type safety** — every concept gets a dedicated column or model. LAWIM_V2 favors **flexibility via metadata_json** — many domain-specific fields are stored as JSON to avoid schema migrations.

This is a philosophical conflict:
- **Safety vs Flexibility:** Gold prevents invalid data at schema level; V2 allows any data structure
- **Explicit vs Implicit:** Gold makes every concept explicit; V2 uses convention-based key access in JSON
- **Migration Cost vs Runtime Cost:** Gold incurs migration cost for changes; V2 incurs runtime parsing/validation cost

### 14.3 Risk if Heritage Gold Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| More Prisma migrations for every new field | MEDIUM — slower schema evolution | HIGH |
| Existing metadata_json data must be migrated to typed columns | HIGH — data migration effort | HIGH |
| Current code accessing metadata_json via key strings must be updated | HIGH — refactoring needed | HIGH |

### 14.4 Risk if LAWIM_V2 Prevails

| Risk | Impact | Likelihood |
|------|--------|------------|
| Cannot enforce data integrity at database level | MEDIUM — invalid data possible | HIGH |
| Type-specific business logic must parse JSON | MEDIUM — runtime overhead and error-prone | HIGH |
| Querying by metadata fields is inefficient | MEDIUM — no indexing on JSON fields | HIGH |
| No schema documentation for metadata_json contents | MEDIUM — tribal knowledge, hard to maintain | HIGH |

### 14.5 Proposed Solution (Reconciliation)

**Pragmatic hybrid approach:**

1. **Core identity fields** → typed columns (property_family, property_type, trust_level)
2. **Frequently-queried fields** → typed columns (price_displayed, negotiable, surface, bedrooms)
3. **Family/type-specific fields** → metadata_json with documented schema per type
4. **Extension fields** → metadata_json (future-proofing)
5. **Document metadata_json schema** per domain in a JSON Schema registry

### 14.6 Decision Required

| Decision | Options | Impact |
|----------|---------|--------|
| Data modeling philosophy? | (a) Typed columns first (Gold), (b) metadata_json first (V2), (c) Hybrid with documented boundaries | Architectural — affects all schema decisions |

---

## 15. Appendix: Resolution Decision Log

| Conflict ID | Decision | Date | Decided By | Rationale |
|-------------|----------|------|------------|-----------|
| C01: Role Model | PENDING | — | — | Requires architectural review |
| C02: Property Type | PENDING | — | — | Requires product owner input |
| C03: Workflow State Machine | PENDING | — | — | Requires implementation effort estimate |
| C04: Transaction vs Project | PENDING | — | — | Requires domain expert input |
| C05: Dossier vs Project | PENDING | — | — | Tied to C04 resolution |
| C06: Service Model | PENDING | — | — | Requires business model confirmation |
| C07: CRM Model | PENDING | — | — | Requires product roadmap alignment |
| C08: Intent Detection | PENDING | — | — | Requires UX/design input |
| C09: Permission Model | PENDING | — | — | Requires security review |
| C10: Matching Roles | PENDING | — | — | Requires algorithm/ML input |
| C11: Price Model | PENDING | — | — | Requires financial/product input |
| C12: Property Lifecycle | PENDING | — | — | Tied to C03 resolution |
| C13: Data Model | PENDING | — | — | Requires technical architecture decision |

### 15.1 Decision-Making Framework

Each conflict should be resolved using the following criteria:

1. **Business Value:** Which model delivers more value to users and the platform?
2. **Implementation Cost:** What is the relative effort to implement each model?
3. **Migration Impact:** How many existing entities/APIs are affected?
4. **Future Flexibility:** Which model better accommodates future requirements?
5. **Risk:** Which model carries more technical/business risk?

### 15.2 Recommended Decision Order

Due to dependencies, conflicts should be resolved in this order:

1. **C02: Property Type** — Foundation for all property logic (P0)
2. **C04/C05: Transaction/Dossier vs Project** — Core entity model (P1)
3. **C01: Role Model** — Affects all authorization (P1)
4. **C03/C12: State Machine** — Affects all workflows (P1)
5. **C06: Service Model** — Revenue model (P1)
6. **C07: CRM Model** — Lead management (P1)
7. **C10: Matching Roles** — Core intelligence (P1)
8. **C08: Intent Detection** — UX paradigm (P2)
9. **C09: Permission Model** — Access control (P2)
10. **C11: Price Model** — Property pricing (P2)
11. **C13: Data Model** — Technical philosophy (P2)

---

*End of SEMANTIC_CONFLICTS.md — 13 semantic conflicts cataloged, all pending resolution.*
