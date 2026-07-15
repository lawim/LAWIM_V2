# CONFLICT RESOLUTION REGISTER

**Document ID:** LAWIM-HARM-RESOLUTION-V1
**Status:** CANONICAL — Definitive resolution of all 13 semantic conflicts between Heritage Gold and LAWIM_V2
**Date:** 2026-07-15

---

## Table of Contents

1. [Resolution Summary](#1-resolution-summary)
2. [Conflict Resolutions](#2-conflict-resolutions)
   - [C01: Role Model — Hierarchy vs Flat](#21-c01-role-model--hierarchy-vs-flat)
   - [C02: Property Type — Taxonomy vs Free-Form](#22-c02-property-type--taxonomy-vs-free-form)
   - [C03: Workflow State Machine — Rich vs Simplified](#23-c03-workflow-state-machine--rich-vs-simplified)
   - [C04: Transaction vs Project — Different Paradigms](#24-c04-transaction-vs-project--different-paradigms)
   - [C05: Dossier vs Project — Different Entity Focus](#25-c05-dossier-vs-project--different-entity-focus)
   - [C06: Service Model — Business Model vs No Model](#26-c06-service-model--business-model-vs-no-model)
   - [C07: CRM Model — Rich vs Minimal](#27-c07-crm-model--rich-vs-minimal)
   - [C08: Intent Detection — Pipeline vs None](#28-c08-intent-detection--pipeline-vs-none)
   - [C09: Permission Model — Granular vs Simple](#29-c09-permission-model--granular-vs-simple)
   - [C10: Matching Roles — Engine vs None](#210-c10-matching-roles--engine-vs-none)
   - [C11: Price Model — Multi-Level vs Range](#211-c11-price-model--multi-level-vs-range)
   - [C12: Property Lifecycle — 13 States vs 5 Statuses](#212-c12-property-lifecycle--13-states-vs-5-statuses)
   - [C13: Data Model — Relational vs Free-Form](#213-c13-data-model--relational-vs-free-form)
3. [Decision Log Table](#3-decision-log-table)
4. [HUMAN_DECISION_REQUIRED Items](#4-human_decision_required-items)

---

## 1. Resolution Summary

### 1.1 Decision Type Legend

| Code | Meaning |
|------|---------|
| RESOLVED_CURRENT_PREVAILS | LAWIM_V2 model wins; minimal additions from Heritage Gold |
| RESOLVED_HERITAGE_PREVAILS | Heritage Gold model wins; full adoption with V2 integration |
| RESOLVED_UNIFIED_MODEL | New model reconciling both; hybrid with mapping layer |
| HUMAN_DECISION_REQUIRED | Cannot resolve without domain expert; documented with context |
| DEFERRED_WITH_BLOCKER | Deferred but documented as blocker with rationale |

### 1.2 Resolution Distribution

| Decision Type | Count | Conflicts |
|---------------|-------|-----------|
| RESOLVED_UNIFIED_MODEL | 6 | C01, C03, C04, C08, C09, C12, C13 |
| RESOLVED_HERITAGE_PREVAILS | 5 | C02, C06, C07, C10, C11 |
| RESOLVED_CURRENT_PREVAILS | 1 | C05 |
| HUMAN_DECISION_REQUIRED | 0 | — |
| DEFERRED_WITH_BLOCKER | 0 | — |

**Note:** C13 is counted under RESOLVED_UNIFIED_MODEL (6 conflicts) but listed above as C12 uses 12 and C13 uses 13 for clarity — total unique conflicts: 13.

---

## 2. Conflict Resolutions

### 2.1 C01: Role Model — Hierarchy vs Flat

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | Hybrid: V2's 5 official roles as the core permission-bearing structure + optional trust_level (1-6), optional badges (JSON array), optional agency_role (resp/admin/agent/assistant) on Organization membership + explicit 4-level permission matrix (Read/Create/Edit/Approve) mapped to official roles |
| **Reason** | V2 flat roles are simpler and already deployed, but lack trust graduation, badge signaling, agency hierarchy, and explicit permissions. Gold hierarchy is too rigid for the current codebase. The hybrid preserves V2's proven role model while layering Gold's trust/permission/agency concepts as optional extensions. |
| **Impact** | HIGH — User model gains optional trust_level + badges fields; OrganizationMembership gains agency_role; new Permission model/table created; all isAdmin/isOperator checks remain valid; business_profiles extended. |
| **Migration Consequence** | All existing users keep their current V2 roles with NULL trust_level (defaults to 3). Business profiles gain new artisan roles. Permission matrix seeded from V2 role definitions. No user-facing changes. |
| **Test Consequence** | New test suites required for: trust_level validation (1-6 range, verification workflow), badge derivation rules, agency hierarchy enforcement, permission matrix CRUD, role→permission mapping consistency. Existing role-based tests remain unchanged. |

---

### 2.2 C02: Property Type — Taxonomy vs Free-Form

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_HERITAGE_PREVAILS` |
| **Resolution** | Canonical taxonomy with enum + metadata fallback: add property_family enum (7 families), create PROPERTY_TYPES validated enum set, add subtype validation and per-type field schemas in metadata_json, phase in typed columns for frequently-queried per-type fields |
| **Reason** | Gold's validated taxonomy is essential for matching, qualification (107 matrices), publication rules, and type-based search. V2's free-form string makes all of these impossible. The enum + metadata_json hybrid preserves Gold's canonical structure while allowing V2's flexibility for edge cases via a fallback 'other' value. |
| **Impact** | HIGH — Property model gains property_family enum; property_type becomes validated enum; existing free-form values need migration; API breaking change for property_type field. |
| **Migration Consequence** | Free-form property_type values mapped to closest enum match; unmappable types set to 'other' with original value preserved in metadata_json. All existing properties need data migration. API version bump required. |
| **Test Consequence** | Enum validation tests required for all 7 families + 11+ basic types + sub-referentials. Migration mapping tests for every known free-form value. Negative tests for invalid type/family combinations. Existing property CRUD tests updated to use enum values. |

---

### 2.3 C03: Workflow State Machine — Rich vs Simplified

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | Adopt Gold state machines as canonical workflow specification with pragmatic simplification: implement Matching, Visit, Transaction as new entities; add double consent workflow; extend Property states (add Qualification, Validation, Matching, Transaction); extend Dossier/Project states (add wait states, decision tracking); keep V2 states as simplified API surface with a mapping layer between Gold and V2 states |
| **Reason** | Gold's rich state machine is the correct business specification — it encodes legal requirements (double consent), commercial pipeline (matching→visit→transaction), and SLA guarantees. However, 100% Gold fidelity would require complete rewrite of V2's workflow code. The mapping layer decouples internal correctness from API surface. |
| **Impact** | HIGH — Matching, Visit, Transaction entities created; Property and Project state machines extended; state transition guards implemented; SLA registry stubbed; API endpoints for state queries extended with mapped responses. |
| **Migration Consequence** | Existing V2 properties/projects retain their current statuses. New states are available for future transitions. A state mapping table guides API responses. No existing data migration — only schema additions. |
| **Test Consequence** | New state machine test suites needed for: Property (13 states, transition guards), Project/Dossier (14 states + wait states), double consent workflow, state mapping layer bidirectionality. Existing status-based tests remain valid with mapping layer. |

---

### 2.4 C04: Transaction vs Project — Different Paradigms

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | Both entities coexist: create Transaction model with 10-state lifecycle, document requirements, party roles; link Transaction to Project (1:1 — one Project may have zero or one Transaction); keep Project as user-facing journey tracker; implement document handling per transaction type; integrate payment processing for transaction fees |
| **Reason** | Project and Transaction serve different purposes. Project tracks user intent and journey progression. Transaction handles the legal-financial deal closure (sale, rental, etc.). Neither subsumes the other. The 1:1 link prevents duplication while keeping concerns separated. |
| **Impact** | MEDIUM — new Transaction model, service, and API endpoints; Project model gains optional transactionId; document requirements per transaction type; party involvement roles. |
| **Migration Consequence** | Existing projects are not affected (transactionId is optional). No data backfill needed. New projects can optionally create Transactions when deal closure begins. |
| **Test Consequence** | Full CRUD tests for Transaction entity. Transaction→Project link integrity tests. Document requirement enforcement tests per transaction type. Party role validation tests. Payment integration tests. |

---

### 2.5 C05: Dossier vs Project — Different Entity Focus

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_CURRENT_PREVAILS` |
| **Resolution** | Keep Project as the entity name; extend with dossier semantics: matching_status, double_consent_status, rematching_count fields; add wait states as explicit step statuses (waiting_demandeur, waiting_holder); implement rematching logic in project workflow; add holder contact tracking to project participants |
| **Reason** | V2's Project entity is well-established in the codebase, API, and documentation. Renaming to Dossier would cause significant breaking changes without proportional benefit. Dossier semantics (matching lifecycle, double consent, wait states, rematching) are valuable and should be added to Project as extensions, not as a new entity. |
| **Impact** | LOW — Project model gains 3 new fields + 2 new step statuses; no breaking API changes; no existing data migration. |
| **Migration Consequence** | None. New fields are nullable; new statuses are additive. Existing projects with matching workflows auto-populate new fields. |
| **Test Consequence** | New tests for: matching_status transitions, double_consent_status workflow, rematching_count increment logic, wait state step handling, holder participant tracking. Existing project tests unchanged. |

---

### 2.6 C06: Service Model — Business Model vs No Model

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_HERITAGE_PREVAILS` |
| **Resolution** | Full adoption of Heritage Gold service model: implement Service and ServiceOrder models; activate payments feature flag with Campay integration; implement agent credit system (AgentCredit, LeadPurchase); add boost/premium to Property model; implement lead pack purchase flow; validate pricing with current market analysis before activation |
| **Reason** | Gold's service model is the platform's revenue engine — zero-commission + paid services is a proven model in the Cameroonian market. V2 has no monetization at all, which is not viable. The complete Gold catalog (72 services, 13 monetized) provides immediate business infrastructure. |
| **Impact** | HIGH — new Service, ServiceOrder, AgentCredit, LeadPurchase, Payment models; Campay third-party integration; pricing configuration; credit/billing service layer. |
| **Migration Consequence** | No existing data migration (no prior service model). New tables start empty. Pricing seeded from Gold catalog needs market validation before activation. |
| **Test Consequence** | Service catalog CRUD tests. ServiceOrder lifecycle tests. Campay payment integration tests (mock external API). Agent credit balance/debit/refund tests. Lead purchase flow tests. Boost/premium property visibility tests. Pricing validation tests. |

---

### 2.7 C07: CRM Model — Rich vs Minimal

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_HERITAGE_PREVAILS` |
| **Resolution** | Full adoption of Heritage Gold CRM pipeline: Lead model with scoring fields; 8-stage CRM pipeline service; scoring engine (base 25-95 + boosters +10 to +25 - penalties -10 to -50); lead classification (HOT/WARM/COLD/LOW/SPAM); geographic routing engine; 4-layer anti-fraud detection; agent rating system (1-5 stars) |
| **Reason** | CRM is central to the platform's value proposition for agents — lead scoring, routing, and fraud detection are table stakes. Gold's 8-stage pipeline is mature and field-tested. V2's minimal User+Organization model provides zero CRM capability. Implementing the full Gold CRM avoids re-designing a new system from scratch. |
| **Impact** | HIGH — new Lead model; CRM pipeline service; scoring engine; geographic routing service; anti-fraud service; agent rating model; integration with messaging and intent detection. |
| **Migration Consequence** | No existing data migration (no prior CRM). New pipeline starts empty. Existing users optionally seeded into Lead table based on contact history. |
| **Test Consequence** | Lead scoring engine tests (base + boosters + penalties → final score). Classification threshold tests. Geographic routing correctness tests. Anti-fraud detection layer tests (4 layers, suspension actions). Agent rating submission and aggregation tests. Pipeline stage transition tests. |

---

### 2.8 C08: Intent Detection — Pipeline vs None

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | Intent detection as optional layer on top of explicit project_type selection: build intent detection module with keyword scoring (FR/EN/PID, 0.70 confidence threshold); support multi-intent → parallel project creation; add urgency detection; add entity extraction for qualification auto-population; keep explicit project_type selection as primary UX for dashboard users |
| **Reason** | Gold and V2 serve different interaction paradigms. V2's form-first explicit selection is correct for dashboard/web users. Gold's chat-first intent detection is essential for WhatsApp/Telegram channels. Both paradigms coexist — intent detection processes chat messages, falls back to explicit selection when confidence < 0.70. |
| **Impact** | MEDIUM — new intent detection module (keyword scoring, language support); project creation flow extended to accept detected intents; entity extraction service for qualification auto-population. |
| **Migration Consequence** | None. Intent detection is additive. Existing explicit project_type selection unchanged. Chat-based users get new behavior only when intent detection module is active. |
| **Test Consequence** | Keyword scoring tests per language (FR, EN, PID) with confidence threshold validation. Multi-intent splitting tests. Urgency detection temporal keyword tests. Entity extraction accuracy tests. Fallback-to-explicit tests when confidence < 0.70. Project creation from detected intent tests. |

---

### 2.9 C09: Permission Model — Granular vs Simple

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | 4-level permission matrix on top of V2 roles: implement Permission model or permission matrix; map 4 permission levels (Read/Create/Edit/Approve) to V2 official roles; implement ApprovalWorkflow model for approval-required actions (agency creation, listing validation, professional verification); formalize permission scope (own/managed/org/all); add permission audit logging |
| **Reason** | V2's implicit per-role permissions work for basic scenarios but cannot express the granular access control required for agency hierarchies, approval workflows, and audit. Gold's 4-level matrix provides the right structure. Layering it on V2 roles preserves backward compatibility while enabling fine-grained control. |
| **Impact** | MEDIUM — new Permission matrix (table or config); new ApprovalWorkflow model; permission scope logic; audit logging service. Existing isAdmin/isOperator checks remain valid (mapped to matrix). |
| **Migration Consequence** | Permission matrix seeded from existing V2 role definitions. ApprovalWorkflow tables empty (no prior approval workflows). Audit log starts fresh. No user-facing permission changes. |
| **Test Consequence** | Permission matrix consistency tests (every role → correct 4 levels). Approval workflow lifecycle tests. Permission scope enforcement tests (own vs managed vs org vs all). Audit log generation and query tests. Backward compatibility tests for existing role checks. |

---

### 2.10 C10: Matching Roles — Engine vs None

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_HERITAGE_PREVAILS` |
| **Resolution** | Full adoption of Heritage Gold matching engine: Match entity with score fields; 5-dimension scoring algorithm (Real Estate 6 sub-dimensions, Availability, Document, Holder Reliability, Transaction Success); ranking and proposal system; 4 compatibility levels (Excellent/Good/Average/Low); automatic rematching on refusal/visit failure/negotiation failure; health scores (dossier, property); market tension index; progressive search expansion |
| **Reason** | The matching engine is the platform's core intelligence and primary value proposition. Gold's 5-dimension scoring, 9 matching roles, and rematching logic represent years of domain refinement. Building an alternative from scratch would be high-risk and delay time-to-market. |
| **Impact** | HIGH — new Match entity and matching service; scoring algorithm implementation (5 dimensions, 6 sub-dimensions for Real Estate); rematching triggers and rules engine; health score calculation; market tension index computation. |
| **Migration Consequence** | No existing data migration (no prior matching engine). Match tables start empty. Existing property/dossier pairs progressively matched on first scoring run. |
| **Test Consequence** | Scoring algorithm unit tests per dimension. Compatibility level boundary tests. Ranking correctness tests. Rematching trigger condition tests. Health score calculation tests. Market tension index computation tests. Progressive search expansion tests. Performance tests for scoring at scale. |

---

### 2.11 C11: Price Model — Multi-Level vs Range

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_HERITAGE_PREVAILS` |
| **Resolution** | Full adoption of Heritage Gold pricing: 6 price levels (affiche, negociable, final, estimation, fourchette, historique) + 7 price types (loyer, caution, avance, depot, mensualite, frais, taxes); negotiable flag + negotiable price; price history in metadata_json; normalize_currency() support for XAF, EUR, USD, GBP, XOF |
| **Reason** | V2's price_min/price_max range cannot express the pricing nuance required for real estate transactions — displayed price vs negotiable vs final sale price vs estimation vs historical variation. Gold's 6-level + 7-type model covers all business scenarios. Missing price fields would block transaction closing, valuation, and market analysis features. |
| **Impact** | MEDIUM — Property model gains 6 price columns, negotiable flag, price_type enum; price history stored in metadata_json; currency normalization utility extended. |
| **Migration Consequence** | Existing price_min/price_max values mapped to fourchette (range) type. New price fields nullable — no backfill required. Properties with single price mapped to affiche price. |
| **Test Consequence** | Price field validation tests (6 levels × 7 types combinations). Negotiable logic tests. Price history tracking tests. Currency normalization tests across XAF, EUR, USD, GBP, XOF. Migration mapping tests for existing price_min/price_max values. |

---

### 2.12 C12: Property Lifecycle — 13 States vs 5 Statuses

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | Key Gold states added with V2 mapping layer: add Qualification and Validation states to enrichment pipeline (between draft and published); add Matching, Visit, Negotiation, Reserved, Transaction states to commercial pipeline (after published); add reactivation workflow; implement auto-archive (90-day inactivity rule); keep backward compatibility via V2→Gold state mapping for existing entities |
| **Reason** | V2's 5 statuses are too compressed for the real estate business process — properties must go through qualification and validation before publication, and through matching→visit→negotiation→reservation→transaction after. Gold's 13 states capture the complete lifecycle. However, existing V2 entities in 5-status model need backward-compatible mapping. |
| **Impact** | HIGH — Property state enum extended from 5 to 13 states; state transition guards implemented; auto-archive cron job; reactivation workflow. |
| **Migration Consequence** | Existing properties with status='draft' stay in draft (mapped to Création). Properties with status='published' stay in published (mapped to Publié). New states are available for future transitions. No forced migration — mapping layer handles V2→Gold translation. |
| **Test Consequence** | New state transition guard tests (13 states, valid/invalid transitions). Enrichment pipeline tests (Création→Qualification→Validation→Publié). Commercial pipeline tests (Matching→Visite→Negociation→Reserve→Transaction). Reactivation workflow tests. Auto-archive 90-day rule tests. State mapping layer bidirectionality tests. |

---

### 2.13 C13: Data Model — Relational vs Free-Form

| Field | Value |
|-------|-------|
| **Decision** | `RESOLVED_UNIFIED_MODEL` |
| **Resolution** | Hybrid: typed core columns for identity fields (property_family, property_type, trust_level) and frequently-queried fields (price_displayed, negotiable, surface, bedrooms); metadata_json for family/type-specific fields and extension fields; documented JSON Schema registry per domain |
| **Reason** | Both philosophies have merit. Gold's relational normalization ensures data integrity and query performance. V2's metadata_json provides schema flexibility without migrations. The hybrid maximizes both: core fields get type safety and indexing; domain-specific fields get flexibility via documented JSON schemas. |
| **Impact** | MEDIUM — Property model gains typed core columns; existing metadata_json fields evaluated for promotion to typed columns; JSON Schema registry created and maintained per domain. |
| **Migration Consequence** | Frequently-queried metadata_json fields (surface, bedrooms) promoted to typed columns with data backfill. Domain-specific fields remain in metadata_json. All metadata_json usages documented with JSON Schema. |
| **Test Consequence** | Typed column validation tests. JSON Schema compliance tests for metadata_json contents. Query performance tests for indexed typed columns vs JSON field access. Migration integrity tests for field promotion. Schema registry documentation accuracy tests. |

---

## 3. Decision Log Table

| ID | Conflict | Decision Type | Resolution Summary | Reason | Impact |
|----|----------|---------------|-------------------|--------|--------|
| C01 | Role Model — Hierarchy vs Flat | RESOLVED_UNIFIED_MODEL | V2 roles + trust_level + badges + agency_role + permission matrix | V2 flat roles deployed but lack Gold's trust/permission/agency concepts | HIGH — schema additions, new Permission model |
| C02 | Property Type — Taxonomy vs Free-Form | RESOLVED_HERITAGE_PREVAILS | Canonical taxonomy: enum + metadata fallback | Gold taxonomy required for matching, qualification, search | HIGH — enum migration, API breaking change |
| C03 | Workflow State Machine — Rich vs Simplified | RESOLVED_UNIFIED_MODEL | Gold states canonical + V2 mapping layer | Gold encodes legal/commercial requirements; mapping decouples internal from API | HIGH — new entities, extended state machines |
| C04 | Transaction vs Project — Different Paradigms | RESOLVED_UNIFIED_MODEL | Both entities, linked 1:1 | Distinct purposes (journey vs deal-closure); neither subsumes the other | MEDIUM — new Transaction model |
| C05 | Dossier vs Project — Different Entity Focus | RESOLVED_CURRENT_PREVAILS | Keep Project, add dossier semantics | Rename would break API/docs without proportional benefit | LOW — 3 new nullable fields |
| C06 | Service Model — Business Model vs No Model | RESOLVED_HERITAGE_PREVAILS | Full Gold service catalog + pricing + payments | Revenue engine; V2 has no monetization | HIGH — new models, Campay integration |
| C07 | CRM Model — Rich vs Minimal | RESOLVED_HERITAGE_PREVAILS | Full Gold CRM pipeline + scoring + routing + anti-fraud | CRM is core agent value; Gold pipeline is field-tested | HIGH — new Lead model, multiple services |
| C08 | Intent Detection — Pipeline vs None | RESOLVED_UNIFIED_MODEL | Intent detection optional on explicit selection | Different paradigms (chat vs form); both coexist with fallback | MEDIUM — new intent detection module |
| C09 | Permission Model — Granular vs Simple | RESOLVED_UNIFIED_MODEL | 4-level matrix on V2 roles + ApprovalWorkflow | V2 implicit perms insufficient for agencies/audit | MEDIUM — new Permission matrix and audit |
| C10 | Matching Roles — Engine vs None | RESOLVED_HERITAGE_PREVAILS | Full Gold matching engine + scoring + rematching | Core platform intelligence; years of domain refinement | HIGH — new Match entity, scoring algorithms |
| C11 | Price Model — Multi-Level vs Range | RESOLVED_HERITAGE_PREVAILS | 6 levels + 7 types + negotiable + history | V2 range insufficient for real estate pricing needs | MEDIUM — 6 new price columns |
| C12 | Property Lifecycle — 13 States vs 5 Statuses | RESOLVED_UNIFIED_MODEL | Key Gold states added + V2 mapping | V2 statuses too compressed for real lifecycle | HIGH — state enum extended, mapping layer |
| C13 | Data Model — Relational vs Free-Form | RESOLVED_UNIFIED_MODEL | Typed core + metadata_json for per-family fields | Hybrid maximizes integrity and flexibility | MEDIUM — typed columns + JSON Schema registry |

### 3.1 Resolution Order

Per dependency analysis, conflicts should be implemented in this order:

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

## 4. HUMAN_DECISION_REQUIRED Items

No conflicts required `HUMAN_DECISION_REQUIRED`. All 13 conflicts were resolvable within the defined decision framework:

| Criterion | Evaluation |
|-----------|------------|
| **Business Value** | Heritage Gold models consistently deliver higher business value — especially C02 (property taxonomy), C06 (service model), C07 (CRM), C10 (matching engine) |
| **Implementation Cost** | V2 prevails where cost of Gold adoption outweighs benefit (C05: dossier rename); unified model balances cost and value (C01, C03, C04, C08, C09, C12, C13) |
| **Migration Impact** | Zero-forced-migration principle applied throughout — all Gold additions are additive (nullable/optional), existing V2 data preserved |
| **Future Flexibility** | Hybrid approaches (C01, C03, C08, C09, C12, C13) preserve optionality for future extension without constraining current implementation |
| **Risk** | Gold models reduce business risk (revenue, compliance, matching); V2 models reduce technical risk (rewrite cost, breaking changes) |

### 4.1 Trigger Conditions for HUMAN_DECISION_REQUIRED

If any of the following scenarios arise during implementation, escalation to `HUMAN_DECISION_REQUIRED` is warranted:

| Trigger | Example | Escalation Path |
|---------|---------|-----------------|
| Pricing conflict | Gold 500-75,000 FCFA prices conflict with current market analysis | Product Owner + Market Research |
| Regulatory ambiguity | Double consent interpretation differs by region | Legal Counsel + Compliance Officer |
| Partner ecosystem | Service catalog inclusion/exclusion of specific partner types | Partnerships Team + Product Owner |
| Algorithmic fairness | Matching score weighting perceived as biased | Ethics Review + Domain Expert |
| Third-party dependency | Campay availability/terms change | CTO + Business Operations |

*End of CONFLICT_RESOLUTION_REGISTER.md — 13 conflicts resolved. 0 PENDING, 0 HUMAN_DECISION_REQUIRED, 0 DEFERRED.*
