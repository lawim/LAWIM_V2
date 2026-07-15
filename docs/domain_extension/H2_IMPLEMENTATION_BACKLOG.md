# H2 Implementation Backlog — 204 Tasks Across 12 Waves

**Document ID:** LAWIM-H2-BACKLOG-V1  
**Status:** CANONICAL  
**Date:** 2026-07-15  
**Total Tasks:** 204  
**Total Extensions Covered:** 282+  
**Source:** EXTENSION_CATALOG.md, GEOGRAPHY_EXTENSION_MODEL.md, RELATIONSHIP_CONSENT_EXTENSION_MODEL.md, EVENT_AUDIT_EXTENSION_MODEL.md, PROJECT_DOSSIER_EXTENSION_MODEL.md

---

## Wave Summary

| Wave | Theme | Count | Priority Range |
|------|-------|-------|----------------|
| 1 | Taxonomies and Registries | 6 | P0-P4 |
| 2 | Qualification Definitions | 11 | P1-P2 |
| 3 | Identity, Roles and Profiles | 11 | P1-P3 |
| 4 | Projects and Dossiers | 22 | P1-P3 |
| 5 | Geography | 12 | P1-P3 |
| 6 | Search and Matching | 27 | P1-P3 |
| 7 | Professional and Service Domains | 47 | P1-P4 |
| 8 | CRM | 11 | P1-P3 |
| 9 | Relationship and Consent | 13 | P1-P2 |
| 10 | Workflows and NBA | 24 | P1-P3 |
| 11 | Events, Audit and Permissions | 14 | P1-P3 |
| 12 | APIs, Compatibility and Migration | 6 | P1 |
| **Total** | | **204** | |

---

## Detailed Task Listings

\n## Wave 1 — Taxonomies and Registries\n\n### H2-W1-001: Add property_family enum (7 families: residential, commercial, land, agricultural, hotelier, investm

| Field | Value |
|-------|-------|
| **task_id** | H2-W1-001 |
| **wave** | 1 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-001 |
| **description** | Add property_family enum (7 families: residential, commercial, land, agricultural, hotelier, investment, project) to Property model with validation. |
| **dependencies** | None |
| **files_expected** | models/property.py, enums/property_family.py, validators/property_validator.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P0 |
| **acceptance_criteria** | Property model has property_family enum with 7 values; Family required on creation; Validation rejects unknown families; Migration sets defaults |

### H2-W1-002: Create PROPERTY_TYPES enum set (11 basic + 41 matrix subtypes). Store subtype in metadata_json. Fami

| Field | Value |
|-------|-------|
| **task_id** | H2-W1-002 |
| **wave** | 1 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-002 |
| **description** | Create PROPERTY_TYPES enum set (11 basic + 41 matrix subtypes). Store subtype in metadata_json. Family-to-type mapping. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/property_type.py, catalog/type_hierarchy.json, models/property.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P0 |
| **acceptance_criteria** | 11 basic types; 41 matrix subtypes; Each type maps to family; Migration maps existing |

### H2-W1-003: Create service catalog registry with all 13 monetized service types and FCFA prices.

| Field | Value |
|-------|-------|
| **task_id** | H2-W1-003 |
| **wave** | 1 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-001, EXT-SVC-MON-002, EXT-SVC-MON-003, EXT-SVC-MON-004, EXT-SVC-MON-005, EXT-SVC-MON-006, EXT-SVC-MON-007, EXT-SVC-MON-008, EXT-SVC-MON-009, EXT-SVC-MON-010, EXT-SVC-MON-011, EXT-SVC-MON-012, EXT-SVC-MON-013 |
| **description** | Create service catalog registry with all 13 monetized service types and FCFA prices. |
| **dependencies** | None |
| **files_expected** | catalog/services.json, enums/service_type.py, models/service_catalog.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 13 monetized services in catalog; Prices with FCFA; Types categorized; Catalog API |

### H2-W1-004: Register 9 core real estate services (estimation, expertise, verification, visit, contre-visite, ren

| Field | Value |
|-------|-------|
| **task_id** | H2-W1-004 |
| **wave** | 1 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-001, EXT-SVC-RES-002, EXT-SVC-RES-003, EXT-SVC-RES-004, EXT-SVC-RES-005, EXT-SVC-RES-006, EXT-SVC-RES-007, EXT-SVC-RES-008, EXT-SVC-RES-009 |
| **description** | Register 9 core real estate services (estimation, expertise, verification, visit, contre-visite, rental mgmt, rental listing, sales listing, publication). |
| **dependencies** | H2-W1-003 |
| **files_expected** | catalog/services_real_estate.json, models/service_catalog.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 9 services registered; Descriptions; Extended catalog API |

### H2-W1-005: Register 15 extended services (photography, video, drone, staging, renovation, construction, mainten

| Field | Value |
|-------|-------|
| **task_id** | H2-W1-005 |
| **wave** | 1 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-010, EXT-SVC-RES-011, EXT-SVC-RES-012, EXT-SVC-RES-013, EXT-SVC-RES-014, EXT-SVC-RES-015, EXT-SVC-RES-016, EXT-SVC-RES-017, EXT-SVC-RES-018, EXT-SVC-RES-019, EXT-SVC-RES-020, EXT-SVC-RES-021, EXT-SVC-RES-022, EXT-SVC-RES-023, EXT-SVC-RES-024 |
| **description** | Register 15 extended services (photography, video, drone, staging, renovation, construction, maintenance, cleaning, security, moving, insurance, legal, tax, condo mgmt, rent recovery). |
| **dependencies** | H2-W1-003 |
| **files_expected** | catalog/services_extended.json, models/service_catalog.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | 15 services registered; Partner flagged; P4 deferred flag |

### H2-W1-006: Register 9 CRM services (lead bronze/silver/gold, coordinate unlock, premium seeker, diaspora tiers,

| Field | Value |
|-------|-------|
| **task_id** | H2-W1-006 |
| **wave** | 1 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-CRM-001, EXT-SVC-CRM-002, EXT-SVC-CRM-003, EXT-SVC-CRM-004, EXT-SVC-CRM-005, EXT-SVC-CRM-006, EXT-SVC-CRM-007, EXT-SVC-CRM-008, EXT-SVC-CRM-009 |
| **description** | Register 9 CRM services (lead bronze/silver/gold, coordinate unlock, premium seeker, diaspora tiers, agent business subscription). |
| **dependencies** | H2-W1-003 |
| **files_expected** | catalog/services_crm.json, models/service_catalog.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 9 CRM services; Lead packs with counts; Diaspora tiers; Subscription tiers |

\n## Wave 2 — Qualification Definitions\n\n### H2-W2-001: Implement 18 residential qualification matrices with fields, question types, validation, role assign

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-001 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-001 |
| **description** | Implement 18 residential qualification matrices with fields, question types, validation, role assignments. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/residential.py, models/qualification_matrix.py, data/residential_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 18 matrices; Linked to property type; Fields with validation; Role assignments |

### H2-W2-002: Implement 7 land qualification matrices with title status, land type, zoning, surface area validatio

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-002 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-002 |
| **description** | Implement 7 land qualification matrices with title status, land type, zoning, surface area validation. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/land.py, data/land_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 7 land matrices; Title status fields; Surface validators |

### H2-W2-003: Implement 21 commercial qualification matrices: office, retail, warehouse, industrial, hotel, mixed-

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-003 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-003 |
| **description** | Implement 21 commercial qualification matrices: office, retail, warehouse, industrial, hotel, mixed-use. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/commercial.py, data/commercial_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 21 matrices; Business fields; Zoning fields |

### H2-W2-004: Implement 5 investment qualification matrices for ROI-focused property search.

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-004 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-004 |
| **description** | Implement 5 investment qualification matrices for ROI-focused property search. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/investment.py, data/investment_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 5 matrices; ROI fields; Horizon questions |

### H2-W2-005: Implement 10 financing request matrices for loan/mortgage qualification.

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-005 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-005 |
| **description** | Implement 10 financing request matrices for loan/mortgage qualification. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/financing.py, data/financing_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P2 |
| **acceptance_criteria** | 10 matrices; Financial fields; Document requirement fields |

### H2-W2-006: Implement 27 professional search matrices covering all professional service categories.

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-006 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-006 |
| **description** | Implement 27 professional search matrices covering all professional service categories. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/professional_search.py, data/professional_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 27 matrices; Linked to profiles; Certification fields |

### H2-W2-007: Implement 24 real estate service matrices for service procurement qualification.

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-007 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-007 |
| **description** | Implement 24 real estate service matrices for service procurement qualification. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | matrices/service.py, data/service_matrices.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 24 matrices; Scope fields; Budget/timeline |

### H2-W2-008: Implement field dictionary with role assignments per matrix field.

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-008 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-008 |
| **description** | Implement field dictionary with role assignments per matrix field. |
| **dependencies** | H2-W2-001, H2-W2-002 |
| **files_expected** | models/field_dictionary.py, data/field_roles.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Covers all fields; Role per field; Field metadata |

### H2-W2-009: Implement question priority: mandatory, important, optional. Priority drives ordering.

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-009 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-009 |
| **description** | Implement question priority: mandatory, important, optional. Priority drives ordering. |
| **dependencies** | H2-W2-008 |
| **files_expected** | enums/question_priority.py, engine/priority_engine.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 3 priority levels; Priority drives order; UI shows required vs optional |

### H2-W2-010: 10-step progressive qualification wizard: intent, location, type, budget, timeline, features, docume

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-010 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-010 |
| **description** | 10-step progressive qualification wizard: intent, location, type, budget, timeline, features, documents, preferences, contact, review. |
| **dependencies** | H2-W2-001, H2-W2-002, H2-W2-003, H2-W2-004, H2-W2-005, H2-W2-006, H2-W2-007, H2-W2-009 |
| **files_expected** | engine/progressive_qualification.py, workflows/qualification_wizard.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 10-step wizard; Adapts to type; Save/resume |

### H2-W2-011: Channel-adaptive qualification with configurable question limits per channel (chat/web/mobile).

| Field | Value |
|-------|-------|
| **task_id** | H2-W2-011 |
| **wave** | 2 |
| **domain** | qualification_engine |
| **extension_ids** | EXT-QUAL-011 |
| **description** | Channel-adaptive qualification with configurable question limits per channel (chat/web/mobile). |
| **dependencies** | H2-W2-010 |
| **files_expected** | engine/channel_adapter.py, config/channel_limits.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Channel limits; Adaptive selection; Fallback |

\n## Wave 3 — Identity, Roles and Profiles\n\n### H2-W3-001: Trust level 1-6 on User. OTP phone, identity docs, pro docs, professional verification, reference ac

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-001 |
| **wave** | 3 |
| **domain** | trust_and_badges |
| **extension_ids** | EXT-RL-TRUST-001, EXT-RL-TRUST-002, EXT-RL-TRUST-003, EXT-RL-TRUST-004, EXT-RL-TRUST-005, EXT-RL-TRUST-006 |
| **description** | Trust level 1-6 on User. OTP phone, identity docs, pro docs, professional verification, reference account. |
| **dependencies** | None |
| **files_expected** | models/user.py, enums/trust_level.py, services/verification_service.py, workflows/identity_verification.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | trust_level 1-6; OTP flow; Identity doc validation; Pro docs; Reference account grant |

### H2-W3-002: 8 badges derived from verification flags. Badge rendering system on profile.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-002 |
| **wave** | 3 |
| **domain** | trust_and_badges |
| **extension_ids** | EXT-RL-BADGE-001, EXT-RL-BADGE-002, EXT-RL-BADGE-003, EXT-RL-BADGE-004, EXT-RL-BADGE-005, EXT-RL-BADGE-006, EXT-RL-BADGE-007, EXT-RL-BADGE-008 |
| **description** | 8 badges derived from verification flags. Badge rendering system on profile. |
| **dependencies** | H2-W3-001 |
| **files_expected** | models/badge.py, enums/badge_type.py, services/badge_service.py, views/profile_badges.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 8 badge types; Derived eligibility; Profile display; Badge events |

### H2-W3-003: Agent onboarding state machine: profile, training, documents, approval, activation.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-003 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-001 |
| **description** | Agent onboarding state machine: profile, training, documents, approval, activation. |
| **dependencies** | H2-W3-001 |
| **files_expected** | workflows/agent_onboarding.py, models/user_onboarding.py, enums/onboarding_status.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 5+ states; Status field; Admin approval |

### H2-W3-004: Minimum 3 active agents rule. Agency operational status logic.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-004 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-002 |
| **description** | Minimum 3 active agents rule. Agency operational status logic. |
| **dependencies** | H2-W3-003 |
| **files_expected** | rules/minimum_agents.py, services/agency_status_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Min 3 enforced; Non-operational below threshold |

### H2-W3-005: Agent_zones table. Lead routing by geographic zone, availability, capacity.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-005 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-003 |
| **description** | Agent_zones table. Lead routing by geographic zone, availability, capacity. |
| **dependencies** | H2-W5-001, H2-W5-004 |
| **files_expected** | models/agent_zone.py, engine/lead_routing_engine.py, services/routing_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Zone assignment; Zone routing; Round-robin; Capacity-aware |

### H2-W3-006: Lead costing module. 500 FCFA default, configurable.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-006 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-004 |
| **description** | Lead costing module. 500 FCFA default, configurable. |
| **dependencies** | None |
| **files_expected** | models/lead_cost.py, services/pricing_service.py, config/lead_pricing.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Configurable; 500 FCFA default; Cost tracked |

### H2-W3-007: Agent credits (credits, total_spent, last_recharge). Boost purchases. Campay integration.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-007 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-005 |
| **description** | Agent credits (credits, total_spent, last_recharge). Boost purchases. Campay integration. |
| **dependencies** | None |
| **files_expected** | models/agent_credit.py, models/boost_purchase.py, services/credit_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | Credit balance; Deduction on purchase; Boost flow; Campay |

### H2-W3-008: Agent rating 1-5 FLOAT. Post-interaction collection. Weighted average.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-008 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-006 |
| **description** | Agent rating 1-5 FLOAT. Post-interaction collection. Weighted average. |
| **dependencies** | H2-W3-003 |
| **files_expected** | models/agent_rating.py, services/rating_service.py, workflows/post_interaction_rating.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Post-interaction; 1-5 scale; Weighted avg; Profile display |

### H2-W3-009: Agency role enum: responsible, admin, agent, assistant. Role-based access.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-009 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-007 |
| **description** | Agency role enum: responsible, admin, agent, assistant. Role-based access. |
| **dependencies** | None |
| **files_expected** | enums/agency_role.py, models/organization_member.py, services/agency_role_service.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 4 roles; Role on membership; Permissions |

### H2-W3-010: Trust level and verification fields on Organization. Agency trust calc.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-010 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-008 |
| **description** | Trust level and verification fields on Organization. Agency trust calc. |
| **dependencies** | H2-W3-001 |
| **files_expected** | models/organization.py, services/agency_verification_service.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Org trust level; Verification status; Score from members |

### H2-W3-011: RCCM, tax_id, CNI documents on Organization. Registration form with upload.

| Field | Value |
|-------|-------|
| **task_id** | H2-W3-011 |
| **wave** | 3 |
| **domain** | agency_structure |
| **extension_ids** | EXT-RL-AGENCY-009 |
| **description** | RCCM, tax_id, CNI documents on Organization. Registration form with upload. |
| **dependencies** | None |
| **files_expected** | models/organization.py, forms/agency_registration.py, validators/agency_documents.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | RCCM field; Tax ID; CNI upload; Validation |

\n## Wave 4 — Projects and Dossiers\n\n### H2-W4-001: Link 107 property types to qualification matrices. Type-family mapping with versioning.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-001 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-003 |
| **description** | Link 107 property types to qualification matrices. Type-family mapping with versioning. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | catalog/type_matrix_mapping.json, models/type_matrix_link.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 107 types mapped; Selection by type; Versioned |

### H2-W4-002: Extend property state machine: draft, pending_review, published, reserved, under_negotiation, sold/r

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-002 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-004 |
| **description** | Extend property state machine: draft, pending_review, published, reserved, under_negotiation, sold/rented, archived, deleted. |
| **dependencies** | H2-W1-001 |
| **files_expected** | state_machines/property_lifecycle.py, enums/property_status.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 10 states; Valid transitions; State events |

### H2-W4-003: 8 publication rules: required fields, photos, price, location, owner verified, agent, fee, no duplic

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-003 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-005 |
| **description** | 8 publication rules: required fields, photos, price, location, owner verified, agent, fee, no duplicate. |
| **dependencies** | H2-W4-002 |
| **files_expected** | rules/publication_rules.py, validators/property_validator.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 8 rules; Pre-publish eval; Error per rule |

### H2-W4-004: 6 price concepts: price_displayed, negotiable, price_negotiable, price_suggestion, hidden_price, pri

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-004 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-006 |
| **description** | 6 price concepts: price_displayed, negotiable, price_negotiable, price_suggestion, hidden_price, pricing_note. |
| **dependencies** | H2-W1-001 |
| **files_expected** | models/property_price.py, enums/price_visibility.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 6 levels; Visibility controls; Negotiable flag |

### H2-W4-005: 7 price types: asking, selling, rental, monthly_charges, agency_fees, notary_fees, tax.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-005 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-007 |
| **description** | 7 price types: asking, selling, rental, monthly_charges, agency_fees, notary_fees, tax. |
| **dependencies** | H2-W4-004 |
| **files_expected** | models/typed_price.py, enums/price_type.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 7 types; Type per value; Breakdown API |

### H2-W4-006: Data quality scoring: completeness + reliability dimensions. Score 0-100.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-006 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-008 |
| **description** | Data quality scoring: completeness + reliability dimensions. Score 0-100. |
| **dependencies** | H2-W4-003, H2-W4-004 |
| **files_expected** | engine/quality_scoring_engine.py, models/property_quality_score.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Score computed; Completeness; Reliability; Dashboard |

### H2-W4-007: Per-type field schemas in metadata_json. Validation per family. Dynamic forms.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-007 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-009 |
| **description** | Per-type field schemas in metadata_json. Validation per family. Dynamic forms. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | schemas/type_field_schemas.py, validators/type_field_validator.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Per-type schemas; Family validation; Dynamic forms |

### H2-W4-008: Availability state machine: available, under_option, reserved, sold, rented, unavailable, seasonal.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-008 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-010 |
| **description** | Availability state machine: available, under_option, reserved, sold, rented, unavailable, seasonal. |
| **dependencies** | H2-W4-002 |
| **files_expected** | state_machines/availability_machine.py, enums/availability_status.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 7 states; Valid transitions; Change events |

### H2-W4-009: Cron job for 90-day inactivity auto-archive. Warning 7 days before.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-009 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-011 |
| **description** | Cron job for 90-day inactivity auto-archive. Warning 7 days before. |
| **dependencies** | H2-W4-002 |
| **files_expected** | cron/auto_archive_job.py, services/archive_service.py, notifications/archive_warning.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Daily cron; Configurable 90d; Warning 7d; Reversible |

### H2-W4-010: 5 investment types: buy_to_let, fix_and_flip, development, commercial_investment, land_banking.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-010 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-012 |
| **description** | 5 investment types: buy_to_let, fix_and_flip, development, commercial_investment, land_banking. |
| **dependencies** | H2-W1-001, H2-W1-002 |
| **files_expected** | enums/investment_type.py, models/property_investment.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 5 types; ROI fields |

### H2-W4-011: Agricultural family. Crop types, land use, soil quality fields.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-011 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-013 |
| **description** | Agricultural family. Crop types, land use, soil quality fields. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/property_family.py, models/agricultural_property.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Family added; Sub-referentiel; Agri fields |

### H2-W4-012: Hotelier family. Hotel-specific fields: star_rating, room_count, amenities.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-012 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-014 |
| **description** | Hotelier family. Hotel-specific fields: star_rating, room_count, amenities. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/property_family.py, models/hotel_property.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Family added; Hotel fields; Migration |

### H2-W4-013: Project family. Link Property to Project. Phase tracking for developments.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-013 |
| **wave** | 4 |
| **domain** | property_model |
| **extension_ids** | EXT-PROP-015 |
| **description** | Project family. Link Property to Project. Phase tracking for developments. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/property_family.py, models/project_linked_property.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P3 |
| **acceptance_criteria** | Family added; Property-Project link; Phase tracking |

### H2-W4-014: Multi-dossier project model: parent_project_id, is_multi_dossier, dossier_count.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-014 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-001 |
| **description** | Multi-dossier project model: parent_project_id, is_multi_dossier, dossier_count. |
| **dependencies** | H2-W4-002 |
| **files_expected** | models/project_dossier.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Parent field; Multi flag; Child support |

### H2-W4-015: Dossier state machine: draft, qualifying, matching, proposed, negotiating, transacting, closed, arch

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-015 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-002 |
| **description** | Dossier state machine: draft, qualifying, matching, proposed, negotiating, transacting, closed, archived. |
| **dependencies** | H2-W4-014 |
| **files_expected** | state_machines/dossier_machine.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 8 states; Valid transitions; Events |

### H2-W4-016: Double consent on dossier: C1 demandeur + C2 holder required before match.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-016 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-003 |
| **description** | Double consent on dossier: C1 demandeur + C2 holder required before match. |
| **dependencies** | H2-W4-015 |
| **files_expected** | workflows/double_consent_dossier.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | C1 collection; C2 collection; Blocked without both |

### H2-W4-017: Holder decision tracking: pending, favorable, refused. Deadline enforcement.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-017 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-004, EXT-DOS-005 |
| **description** | Holder decision tracking: pending, favorable, refused. Deadline enforcement. |
| **dependencies** | H2-W4-015 |
| **files_expected** | models/holder_decision.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Decision fields; Deadline |

### H2-W4-018: Rematching on dossier. Count, reason, max 3.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-018 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-006, EXT-DOS-007 |
| **description** | Rematching on dossier. Count, reason, max 3. |
| **dependencies** | H2-W4-015, H2-W6-005 |
| **files_expected** | models/dossier_rematch.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Count tracked; Max 3; Reason logged |

### H2-W4-019: Participant tracking: holder_id, agent_ids, roles. Qualification completion.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-019 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-008, EXT-DOS-009, EXT-DOS-010 |
| **description** | Participant tracking: holder_id, agent_ids, roles. Qualification completion. |
| **dependencies** | H2-W4-015 |
| **files_expected** | models/dossier_participant.py, models/dossier_qualification.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Roles; Progress tracking |

### H2-W4-020: Dossier health score and linked entities. Auto-link properties, conversations, visits.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-020 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-011, EXT-DOS-012 |
| **description** | Dossier health score and linked entities. Auto-link properties, conversations, visits. |
| **dependencies** | H2-W4-015 |
| **files_expected** | scoring/dossier_health.py, models/dossier_linked_entities.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Health 0-100; Auto-linking |

### H2-W4-021: Channel adaptation, SLA priority, NBA, progressive expansion for dossier.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-021 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-013, EXT-DOS-014, EXT-DOS-015, EXT-DOS-016 |
| **description** | Channel adaptation, SLA priority, NBA, progressive expansion for dossier. |
| **dependencies** | H2-W4-015 |
| **files_expected** | services/dossier_channel_service.py, config/dossier_sla.json, services/dossier_nba.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Channel-adaptive; SLA per priority; NBA per state; Expansion |

### H2-W4-022: Dossier data scope, privacy controls, doc requirements, completion criteria.

| Field | Value |
|-------|-------|
| **task_id** | H2-W4-022 |
| **wave** | 4 |
| **domain** | project_dossier |
| **extension_ids** | EXT-DOS-017, EXT-DOS-018, EXT-DOS-019, EXT-DOS-020 |
| **description** | Dossier data scope, privacy controls, doc requirements, completion criteria. |
| **dependencies** | H2-W4-015 |
| **files_expected** | models/dossier_data_scope.py, models/dossier_document.py, rules/dossier_completion.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Scope; Privacy; Docs; Completion |

\n## Wave 5 — Geography\n\n### H2-W5-001: GeographicUnit model 14-level hierarchy. Canonical IDs. Parent-child. GeoJSON.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-001 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-001 |
| **description** | GeographicUnit model 14-level hierarchy. Canonical IDs. Parent-child. GeoJSON. |
| **dependencies** | None |
| **files_expected** | models/geographic_unit.py, enums/geo_level.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 14 levels; Canonical IDs; Hierarchy; GeoJSON |

### H2-W5-002: Full hierarchy: admin (1-5) + operational (6-14). Seed Cameroon: regions, depts, municipalities, cit

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-002 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-002 |
| **description** | Full hierarchy: admin (1-5) + operational (6-14). Seed Cameroon: regions, depts, municipalities, cities. |
| **dependencies** | H2-W5-001 |
| **files_expected** | data/cameroon_geo_seed.py, seeds/regions.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 14 levels; 10 regions; 58 depts; 28 cities |

### H2-W5-003: Alias resolution for geo names. Misspellings, historical names, alternative names.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-003 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-003 |
| **description** | Alias resolution for geo names. Misspellings, historical names, alternative names. |
| **dependencies** | H2-W5-001 |
| **files_expected** | services/alias_resolution_service.py, models/geo_alias.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Case-insensitive; Misspellings; Priority |

### H2-W5-004: LAWIM-defined zone groupings for agent routing. Zones across admin boundaries.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-004 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-004 |
| **description** | LAWIM-defined zone groupings for agent routing. Zones across admin boundaries. |
| **dependencies** | H2-W5-001, H2-W5-002 |
| **files_expected** | models/geo_zone.py, services/zone_routing_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Zone groups; Agent assignment |

### H2-W5-005: Geographic scoring 5 distance tiers: same_neighborhood, same_city, same_region, same_country, intern

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-005 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-005 |
| **description** | Geographic scoring 5 distance tiers: same_neighborhood, same_city, same_region, same_country, international. |
| **dependencies** | H2-W5-001 |
| **files_expected** | scoring/geographic_scoring.py, services/proximity_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 5 tiers; GPS calc; Hierarchy |

### H2-W5-006: Mobility modes: walking, car, public_transit, any. Affects proximity radius.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-006 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-006 |
| **description** | Mobility modes: walking, car, public_transit, any. Affects proximity radius. |
| **dependencies** | H2-W5-005 |
| **files_expected** | enums/mobility_mode.py, scoring/mobility_adjusted_scoring.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 4 modes; Adjusted radius |

### H2-W5-007: GeographicRelation join table: contains, adjacent, nearby, equivalent, historically_known_as.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-007 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-007 |
| **description** | GeographicRelation join table: contains, adjacent, nearby, equivalent, historically_known_as. |
| **dependencies** | H2-W5-001 |
| **files_expected** | models/geographic_relation.py, enums/geo_relation_type.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 5 types; CRUD; Query |

### H2-W5-008: Market equivalents for cross-market area comparison.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-008 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-008 |
| **description** | Market equivalents for cross-market area comparison. |
| **dependencies** | H2-W5-001, H2-W5-007 |
| **files_expected** | models/market_equivalent.py, services/market_comparison_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Mapping; Comparison; Confidence |

### H2-W5-009: Complete Cameroon seed: 10 regions, 58 depts, 360 municipalities, 28 cities, 500+ neighborhoods, GPS

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-009 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-009 |
| **description** | Complete Cameroon seed: 10 regions, 58 depts, 360 municipalities, 28 cities, 500+ neighborhoods, GPS. |
| **dependencies** | H2-W5-002 |
| **files_expected** | seeds/cameroon_full_seed.py, data/gps_coordinates.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Full seed; GPS for priority; Idempotent |

### H2-W5-010: Geo auto-completion and search API. Partial matching, hierarchy drill, multi-language.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-010 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-010 |
| **description** | Geo auto-completion and search API. Partial matching, hierarchy drill, multi-language. |
| **dependencies** | H2-W5-003, H2-W5-009 |
| **files_expected** | api/geo_search.py, services/geo_autocomplete.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Auto-complete; Partial match; Multi-lang |

### H2-W5-011: Geo-level constraints for search: valid property/transaction types per geographic level.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-011 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-011 |
| **description** | Geo-level constraints for search: valid property/transaction types per geographic level. |
| **dependencies** | H2-W5-001, H2-W1-001 |
| **files_expected** | rules/geo_level_constraints.py, config/geo_type_mapping.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Per-level constraints; Validation |

### H2-W5-012: Geo reference data API: list countries, regions, depts, cities, neighborhoods. Hierarchy browsing.

| Field | Value |
|-------|-------|
| **task_id** | H2-W5-012 |
| **wave** | 5 |
| **domain** | geography |
| **extension_ids** | EXT-GEO-012 |
| **description** | Geo reference data API: list countries, regions, depts, cities, neighborhoods. Hierarchy browsing. |
| **dependencies** | H2-W5-009, H2-W5-010 |
| **files_expected** | api/geo_reference.py, serializers/geo_serializer.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | REST API; Hierarchy; <200ms |

\n## Wave 6 — Search and Matching\n\n### H2-W6-001: Match entity + matching algorithm with trigger events. Min 60/100, max 10 results.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-001 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-001 |
| **description** | Match entity + matching algorithm with trigger events. Min 60/100, max 10 results. |
| **dependencies** | H2-W4-002, H2-W5-005 |
| **files_expected** | models/match.py, engine/matching_engine.py, triggers/matching_triggers.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | Match entity; Algorithm; Events; Min 60 |

### H2-W6-002: 5 scoring dimensions: location_match, budget_match, type_match, feature_match, agent_quality. Config

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-002 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-002 |
| **description** | 5 scoring dimensions: location_match, budget_match, type_match, feature_match, agent_quality. Configurable weights. |
| **dependencies** | H2-W6-001 |
| **files_expected** | scoring/scoring_dimensions.py, config/dimension_weights.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 5 dimensions; Weights; Composite |

### H2-W6-003: Geographic scoring tiers: same_neighborhood=100, same_city=80, same_region=50, same_country=20, inte

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-003 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-003 |
| **description** | Geographic scoring tiers: same_neighborhood=100, same_city=80, same_region=50, same_country=20, international=0. |
| **dependencies** | H2-W6-002, H2-W5-005 |
| **files_expected** | scoring/geo_scoring_integration.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Integrated; 5 tiers |

### H2-W6-004: 4 compatibility levels: excellent >=85, good 70-84, average 50-69, low <50. Color coded.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-004 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-004 |
| **description** | 4 compatibility levels: excellent >=85, good 70-84, average 50-69, low <50. Color coded. |
| **dependencies** | H2-W6-002 |
| **files_expected** | scoring/compatibility_levels.py, enums/compatibility_level.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 4 levels; On Match; Configurable |

### H2-W6-005: Rematching: triggers (new property, dossier update, expired, declined). Max 3.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-005 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-005 |
| **description** | Rematching: triggers (new property, dossier update, expired, declined). Max 3. |
| **dependencies** | H2-W6-001 |
| **files_expected** | engine/rematching_engine.py, triggers/rematch_triggers.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Triggers; Max 3; Reason logged |

### H2-W6-006: Exclusion rules: already_contacted, same_owner, budget_mismatch>50%, location, type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-006 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-006 |
| **description** | Exclusion rules: already_contacted, same_owner, budget_mismatch>50%, location, type. |
| **dependencies** | H2-W6-001 |
| **files_expected** | rules/exclusion_rules.py, engine/exclusion_engine.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Rules; Pre-match eval; Configurable |

### H2-W6-007: Transaction success score from historical patterns. 0-100.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-007 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-007 |
| **description** | Transaction success score from historical patterns. 0-100. |
| **dependencies** | H2-W6-001 |
| **files_expected** | scoring/transaction_success_scoring.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Score 0-100; Historical analysis; Configurable |

### H2-W6-008: Market tension index = demand/supply ratio by type, location, price.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-008 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-008 |
| **description** | Market tension index = demand/supply ratio by type, location, price. |
| **dependencies** | H2-W6-001, H2-W5-001 |
| **files_expected** | analytics/market_tension_index.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Calculated; Filterable; API |

### H2-W6-009: Dossier health score from qualification completeness and data quality.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-009 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-009 |
| **description** | Dossier health score from qualification completeness and data quality. |
| **dependencies** | H2-W6-001, H2-W2-010 |
| **files_expected** | scoring/dossier_health_scoring.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 0-100; Completeness; Freshness |

### H2-W6-010: Property health score from data quality, completeness, freshness. Verification boosts.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-010 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-010 |
| **description** | Property health score from data quality, completeness, freshness. Verification boosts. |
| **dependencies** | H2-W6-001, H2-W4-006 |
| **files_expected** | scoring/property_health_scoring.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 0-100; Quality; Freshness; Boost |

### H2-W6-011: 9 matching roles: demandeur, holder, agent_demandeur, agent_holder, agency_admin, supervisor, mediat

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-011 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-011 |
| **description** | 9 matching roles: demandeur, holder, agent_demandeur, agent_holder, agency_admin, supervisor, mediator, expert, system. |
| **dependencies** | H2-W6-001 |
| **files_expected** | enums/matching_role.py, config/role_scoring_weights.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 9 roles; Weights; Permissions |

### H2-W6-012: Progressive search expansion: location, budget+20%, type relax, feature relax.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-012 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-012 |
| **description** | Progressive search expansion: location, budget+20%, type relax, feature relax. |
| **dependencies** | H2-W6-001 |
| **files_expected** | engine/search_expansion_engine.py, config/expansion_rules.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 4 levels; Auto expansion; Logged |

### H2-W6-013: Continuous market surveillance on new property and availability changes.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-013 |
| **wave** | 6 |
| **domain** | matching |
| **extension_ids** | EXT-MAT-013 |
| **description** | Continuous market surveillance on new property and availability changes. |
| **dependencies** | H2-W6-001, H2-W11-001 |
| **files_expected** | engine/market_surveillance.py, triggers/new_property_trigger.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | New property trigger; Avail trigger; Notification |

### H2-W6-014: Keyword intent classifier for FR, EN, PID. 7+ intents: buy, rent, sell, invest, finance, find, servi

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-014 |
| **wave** | 6 |
| **domain** | intent_detection |
| **extension_ids** | EXT-INT-001 |
| **description** | Keyword intent classifier for FR, EN, PID. 7+ intents: buy, rent, sell, invest, finance, find, service. |
| **dependencies** | None |
| **files_expected** | engine/intent_classifier.py, data/intent_keywords.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | FR/EN/PID; 7+ intents; Configurable dicts |

### H2-W6-015: Confidence threshold 0.70 default. Fallback to manual below threshold.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-015 |
| **wave** | 6 |
| **domain** | intent_detection |
| **extension_ids** | EXT-INT-002 |
| **description** | Confidence threshold 0.70 default. Fallback to manual below threshold. |
| **dependencies** | H2-W6-014 |
| **files_expected** | engine/confidence_threshold.py, config/intent_threshold.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Configurable; Fallback |

### H2-W6-016: Multi-intent detection: parallel project creation from multiple intents.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-016 |
| **wave** | 6 |
| **domain** | intent_detection |
| **extension_ids** | EXT-INT-003 |
| **description** | Multi-intent detection: parallel project creation from multiple intents. |
| **dependencies** | H2-W6-014 |
| **files_expected** | engine/multi_intent_handler.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Multi detect; Parallel creation |

### H2-W6-017: Urgency scoring from keywords. Urgency level on Project.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-017 |
| **wave** | 6 |
| **domain** | intent_detection |
| **extension_ids** | EXT-INT-004 |
| **description** | Urgency scoring from keywords. Urgency level on Project. |
| **dependencies** | H2-W6-014 |
| **files_expected** | engine/urgency_detector.py, data/urgency_keywords.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Scoring; Keywords; Stored |

### H2-W6-018: Entity extraction per intent: location, budget, type, size. Auto-populate qualification.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-018 |
| **wave** | 6 |
| **domain** | intent_detection |
| **extension_ids** | EXT-INT-005 |
| **description** | Entity extraction per intent: location, budget, type, size. Auto-populate qualification. |
| **dependencies** | H2-W6-014 |
| **files_expected** | engine/entity_extractor.py, schemas/extracted_entities.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Per intent; Fields extracted; Auto-populate |

### H2-W6-019: Intent-to-role mapping: buy->demandeur, sell->holder, service->service_seeker.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-019 |
| **wave** | 6 |
| **domain** | intent_detection |
| **extension_ids** | EXT-INT-006 |
| **description** | Intent-to-role mapping: buy->demandeur, sell->holder, service->service_seeker. |
| **dependencies** | H2-W6-014 |
| **files_expected** | models/intent.py, services/role_mapping_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Model; Role mapping |

### H2-W6-020: short_stay PROJECT_TYPE. Sub-type: min_nights, max_nights, seasonal_pricing.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-020 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-001 |
| **description** | short_stay PROJECT_TYPE. Sub-type: min_nights, max_nights, seasonal_pricing. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/project_type.py, models/short_stay_property.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Type added; Sub-type metadata |

### H2-W6-021: lease (bail 3+ ans) PROJECT_TYPE. timeline_horizon extended to 10 years.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-021 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-002 |
| **description** | lease (bail 3+ ans) PROJECT_TYPE. timeline_horizon extended to 10 years. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/project_type.py, models/project.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Type added; Horizon extended |

### H2-W6-022: commercial_lease_transfer (cession_bail) project type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-022 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-003 |
| **description** | commercial_lease_transfer (cession_bail) project type. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/project_type.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Type added; Transfer fields |

### H2-W6-023: Commercial lease (bail 3-9 ans) as lease sub-type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-023 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-004 |
| **description** | Commercial lease (bail 3-9 ans) as lease sub-type. |
| **dependencies** | H2-W6-021 |
| **files_expected** | enums/project_type.py, models/commercial_lease.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Sub-type defined; 3-9 year duration |

### H2-W6-024: business_transfer (cession) project type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-024 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-005 |
| **description** | business_transfer (cession) project type. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/project_type.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Type added; Valuation fields |

### H2-W6-025: finance PROJECT_TYPE. 10 financing matrices.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-025 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-006 |
| **description** | finance PROJECT_TYPE. 10 financing matrices. |
| **dependencies** | H2-W1-001, H2-W2-005 |
| **files_expected** | enums/project_type.py, workflows/financing_workflow.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | high |
| **priority** | P2 |
| **acceptance_criteria** | Type added; 10 matrices linked |

### H2-W6-026: find PROJECT_TYPE. Professional search workflow.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-026 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-007 |
| **description** | find PROJECT_TYPE. Professional search workflow. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/project_type.py, workflows/professional_search_workflow.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Type added; Search flow |

### H2-W6-027: service PROJECT_TYPE. Service procurement workflow.

| Field | Value |
|-------|-------|
| **task_id** | H2-W6-027 |
| **wave** | 6 |
| **domain** | transaction_types |
| **extension_ids** | EXT-TRX-008 |
| **description** | service PROJECT_TYPE. Service procurement workflow. |
| **dependencies** | H2-W1-001 |
| **files_expected** | enums/project_type.py, workflows/service_procurement_workflow.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Type added; Procurement flow |

\n## Wave 7 — Professional and Service Domains\n\n### H2-W7-001: ServiceOrder 8-state lifecycle: created, confirmed, in_progress, completed, cancelled, refunded, dis

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-001 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-LIFE-001 |
| **description** | ServiceOrder 8-state lifecycle: created, confirmed, in_progress, completed, cancelled, refunded, disputed, archived. |
| **dependencies** | H2-W1-003 |
| **files_expected** | models/service_order.py, state_machines/service_order_machine.py, enums/service_order_status.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 8 states; Valid transitions; Events |

### H2-W7-002: Payment 10-state machine. Campay integration for MTN/Orange mobile money.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-002 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-LIFE-002 |
| **description** | Payment 10-state machine. Campay integration for MTN/Orange mobile money. |
| **dependencies** | H2-W7-001 |
| **files_expected** | models/payment.py, state_machines/payment_machine.py, integrations/campay_client.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 10 states; Campay; Refunds |

### H2-W7-003: Boost system: 7-day (2K) and 30-day (5K). boost_level and boost_expires_at. Ranking boost.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-003 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-001, EXT-SVC-MON-002 |
| **description** | Boost system: 7-day (2K) and 30-day (5K). boost_level and boost_expires_at. Ranking boost. |
| **dependencies** | H2-W7-001, H2-W7-002 |
| **files_expected** | models/property.py, services/boost_service.py, workflows/boost_purchase_flow.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Boost fields; 7/30 options; Purchase flow; Ranking |

### H2-W7-004: Premium listing (10K). is_premium field. Premium badge and ranking boost.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-004 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-003 |
| **description** | Premium listing (10K). is_premium field. Premium badge and ranking boost. |
| **dependencies** | H2-W7-001, H2-W7-002 |
| **files_expected** | models/property.py, services/premium_service.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | is_premium; Ranking boost; Badge |

### H2-W7-005: Agent Pro subscription (10K/month). Recurring Campay billing. Trial period.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-005 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-004 |
| **description** | Agent Pro subscription (10K/month). Recurring Campay billing. Trial period. |
| **dependencies** | H2-W7-001, H2-W7-002 |
| **files_expected** | models/subscription.py, services/subscription_service.py, enums/subscription_tier.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | Model; Billing; Trial; Cancel |

### H2-W7-006: Visit accompaniment ServiceOrder (50K). Linked to Conversation.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-006 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-005 |
| **description** | Visit accompaniment ServiceOrder (50K). Linked to Conversation. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/visit_accompaniment_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Type=visit_accompaniment; Conv link |

### H2-W7-007: Transaction accompaniment ServiceOrder (50K). Document checklist.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-007 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-006 |
| **description** | Transaction accompaniment ServiceOrder (50K). Document checklist. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/transaction_accompaniment_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Type; Checklist |

### H2-W7-008: Document verification ServiceOrder (5K). Deferred P4.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-008 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-007 |
| **description** | Document verification ServiceOrder (5K). Deferred P4. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/document_control_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Type; Deferred flag |

### H2-W7-009: Professional photography (15K). Media service order origin.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-009 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-008 |
| **description** | Professional photography (15K). Media service order origin. |
| **dependencies** | H2-W7-001 |
| **files_expected** | models/media.py, services/photography_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Origin tracking; Photo order |

### H2-W7-010: Professional videography (25K). Media service order origin.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-010 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-009 |
| **description** | Professional videography (25K). Media service order origin. |
| **dependencies** | H2-W7-001 |
| **files_expected** | models/media.py, services/videography_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Video order; Origin |

### H2-W7-011: Property verification (10K). verification_status and verified_at on Property.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-011 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-010 |
| **description** | Property verification (10K). verification_status and verified_at on Property. |
| **dependencies** | H2-W7-001 |
| **files_expected** | models/property.py, services/property_verification_service.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Fields; ServiceOrder flow; Badge |

### H2-W7-012: Pay-per-connection (500). LeadPurchase + agent credit. Core monetization.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-012 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-011 |
| **description** | Pay-per-connection (500). LeadPurchase + agent credit. Core monetization. |
| **dependencies** | H2-W7-001, H2-W7-002, H2-W3-007 |
| **files_expected** | models/lead_purchase.py, services/lead_purchase_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | LeadPurchase; Credit deduction; 500 CFA; Receipt |

### H2-W7-013: Personalized assistance (50K). Needs human decision on scope.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-013 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-012 |
| **description** | Personalized assistance (50K). Needs human decision on scope. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/personalized_assistance_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | ServiceOrder; Scope def |

### H2-W7-014: Premium visibility (7.5K). Distinct from boost/premium listing.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-014 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-MON-013 |
| **description** | Premium visibility (7.5K). Distinct from boost/premium listing. |
| **dependencies** | H2-W7-003, H2-W7-004 |
| **files_expected** | services/premium_visibility_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Distinct tier; Purchase |

### H2-W7-015: Property estimation/valuation service with valuation matrix.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-015 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-001 |
| **description** | Property estimation/valuation service with valuation matrix. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/estimation_service.py, matrices/estimation_matrix.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Estimation; Matrix; Report |

### H2-W7-016: Professional expertise/inspection service with checklist.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-016 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-002 |
| **description** | Professional expertise/inspection service with checklist. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/expertise_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Expertise; Checklist |

### H2-W7-017: Document verification workflow.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-017 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-003 |
| **description** | Document verification workflow. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/document_verification_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Workflow; Upload portal |

### H2-W7-018: Visit scheduling service: requested, scheduled, confirmed, completed, cancelled, no_show.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-018 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-004 |
| **description** | Visit scheduling service: requested, scheduled, confirmed, completed, cancelled, no_show. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/visit_scheduling_service.py, workflows/visit_workflow.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Scheduling; State machine; No-show |

### H2-W7-019: Contre-visite (second visit) type. Linked to initial visit.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-019 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-005 |
| **description** | Contre-visite (second visit) type. Linked to initial visit. |
| **dependencies** | H2-W7-018 |
| **files_expected** | models/visit.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Type; Original visit link |

### H2-W7-020: Rental management. Recurring model. Full vs referral scope.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-020 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-006 |
| **description** | Rental management. Recurring model. Full vs referral scope. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/rental_management_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Service; Recurring; Tenant mgmt |

### H2-W7-021: Rental listing service with channel distribution.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-021 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-007 |
| **description** | Rental listing service with channel distribution. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/rental_listing_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Order; Channel |

### H2-W7-022: Sales listing service (for-sale).

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-022 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-008 |
| **description** | Sales listing service (for-sale). |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/sales_listing_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Order; For-sale fields |

### H2-W7-023: Publication service with multi-channel (web, mobile, partner).

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-023 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-009 |
| **description** | Publication service with multi-channel (web, mobile, partner). |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/publication_service.py, enums/publication_channel.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | Multi-channel; Status tracking |

### H2-W7-024: Photography service order flow. Media model extension.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-024 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-010 |
| **description** | Photography service order flow. Media model extension. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/photography_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Delivery |

### H2-W7-025: Video service order flow. Media model extension.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-025 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-011 |
| **description** | Video service order flow. Media model extension. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/video_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Delivery |

### H2-W7-026: Drone photography sub-service of photography.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-026 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-012 |
| **description** | Drone photography sub-service of photography. |
| **dependencies** | H2-W7-024 |
| **files_expected** | services/drone_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Sub-service; Aerial delivery |

### H2-W7-027: Home staging professional service with staging workflow.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-027 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-013 |
| **description** | Home staging professional service with staging workflow. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/home_staging_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Staging; Consultation |

### H2-W7-028: Renovation service. Scope management, milestones.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-028 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-014 |
| **description** | Renovation service. Scope management, milestones. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/renovation_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Order; Scope; Milestones |

### H2-W7-029: Construction service. Project management integration.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-029 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-015 |
| **description** | Construction service. Project management integration. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/construction_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Order; Phase tracking |

### H2-W7-030: Maintenance recurring service with scheduling.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-030 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-016 |
| **description** | Maintenance recurring service with scheduling. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/maintenance_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Recurring |

### H2-W7-031: Cleaning professional service with scheduling.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-031 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-017 |
| **description** | Cleaning professional service with scheduling. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/cleaning_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Schedule |

### H2-W7-032: Security professional service with guard assignment.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-032 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-018 |
| **description** | Security professional service with guard assignment. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/security_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Guard assign |

### H2-W7-033: Moving professional service with inventory tracking.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-033 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-019 |
| **description** | Moving professional service with inventory tracking. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/moving_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Inventory |

### H2-W7-034: Insurance referral with partner integration.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-034 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-020 |
| **description** | Insurance referral with partner integration. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/insurance_referral_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Referral; Partner |

### H2-W7-035: Legal advice with lawyer network matching.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-035 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-021 |
| **description** | Legal advice with lawyer network matching. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/legal_advice_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Lawyer match |

### H2-W7-036: Tax advice as partner professional service.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-036 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-022 |
| **description** | Tax advice as partner professional service. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/tax_advice_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Expert match |

### H2-W7-037: Condo management professional service.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-037 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-023 |
| **description** | Condo management professional service. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/condo_management_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Fee tracking |

### H2-W7-038: Rent recovery dispute resolution service.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-038 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-RES-024 |
| **description** | Rent recovery dispute resolution service. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/rent_recovery_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Order; Dispute |

### H2-W7-039: Add mason, carpenter, painter to business_profiles.py.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-039 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-PRO-001, EXT-SVC-PRO-002, EXT-SVC-PRO-003 |
| **description** | Add mason, carpenter, painter to business_profiles.py. |
| **dependencies** | None |
| **files_expected** | enums/business_profiles.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 3 profiles; Labels FR/EN |

### H2-W7-040: Add tiler, roofer, real estate expert. Expert distinct from agent.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-040 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-PRO-004, EXT-SVC-PRO-005, EXT-SVC-PRO-006 |
| **description** | Add tiler, roofer, real estate expert. Expert distinct from agent. |
| **dependencies** | None |
| **files_expected** | enums/business_profiles.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 3 profiles; Expert distinction |

### H2-W7-041: Add appraiser, condo manager, drone videographer.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-041 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-PRO-007, EXT-SVC-PRO-008, EXT-SVC-PRO-009 |
| **description** | Add appraiser, condo manager, drone videographer. |
| **dependencies** | None |
| **files_expected** | enums/business_profiles.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | 3 profiles; Metadata |

### H2-W7-042: Add broker, security guard, admin service provider.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-042 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-PRO-010, EXT-SVC-PRO-011, EXT-SVC-PRO-012 |
| **description** | Add broker, security guard, admin service provider. |
| **dependencies** | None |
| **files_expected** | enums/business_profiles.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | 3 profiles; Broker distinction |

### H2-W7-043: Lead packs: Bronze 500/1, Silver 1500/5, Gold 3000/15.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-043 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-CRM-001, EXT-SVC-CRM-002, EXT-SVC-CRM-003 |
| **description** | Lead packs: Bronze 500/1, Silver 1500/5, Gold 3000/15. |
| **dependencies** | H2-W7-001, H2-W7-002 |
| **files_expected** | models/lead_purchase.py, services/lead_pack_service.py, enums/lead_pack_tier.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 3 tiers; Counts/price; Campay |

### H2-W7-044: Coordinate unlock (500). Owner contact unlock per property.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-044 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-CRM-004 |
| **description** | Coordinate unlock (500). Owner contact unlock per property. |
| **dependencies** | H2-W7-001, H2-W7-002 |
| **files_expected** | services/coordinate_unlock_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Purchase type; Toggle visibility |

### H2-W7-045: Premium seeker profile (1K). Priority features.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-045 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-CRM-005 |
| **description** | Premium seeker profile (1K). Priority features. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/premium_seeker_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P4 |
| **acceptance_criteria** | Premium tier; Features |

### H2-W7-046: Diaspora: Simple 25K, Rapport 50K, Complet 75K.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-046 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-CRM-006, EXT-SVC-CRM-007, EXT-SVC-CRM-008 |
| **description** | Diaspora: Simple 25K, Rapport 50K, Complet 75K. |
| **dependencies** | H2-W7-001 |
| **files_expected** | services/diaspora_service.py, enums/diaspora_tier.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P3 |
| **acceptance_criteria** | 3 tiers; Access; Report; Accompaniment |

### H2-W7-047: Agent Business subscription (25K/month). Feature differentiation.

| Field | Value |
|-------|-------|
| **task_id** | H2-W7-047 |
| **wave** | 7 |
| **domain** | service_model |
| **extension_ids** | EXT-SVC-CRM-009 |
| **description** | Agent Business subscription (25K/month). Feature differentiation. |
| **dependencies** | H2-W7-005 |
| **files_expected** | models/subscription.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Tier added; Diff from Pro |

\n## Wave 8 — CRM\n\n### H2-W8-001: Lead scoring engine: base + boosters - penalties. 0-100 range. Real-time on update.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-001 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-001 |
| **description** | Lead scoring engine: base + boosters - penalties. 0-100 range. Real-time on update. |
| **dependencies** | H2-W2-010 |
| **files_expected** | engine/lead_scoring_engine.py, models/lead_score.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | Scoring engine; 0-100; Real-time |

### H2-W8-002: 13 configurable score boosters with weights and caps.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-002 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-002 |
| **description** | 13 configurable score boosters with weights and caps. |
| **dependencies** | H2-W8-001 |
| **files_expected** | scoring/boosters.py, config/booster_weights.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 13 boosters; Config weights; Caps |

### H2-W8-003: 8 configurable score penalties with weights. Floor at 0.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-003 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-003 |
| **description** | 8 configurable score penalties with weights. Floor at 0. |
| **dependencies** | H2-W8-001 |
| **files_expected** | scoring/penalties.py, config/penalty_weights.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 8 penalties; Weights; Floor 0 |

### H2-W8-004: 5 lead classes: Hot>=80, Warm 60-79, Warmish 40-59, Cold 20-39, Dead<20.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-004 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-004 |
| **description** | 5 lead classes: Hot>=80, Warm 60-79, Warmish 40-59, Cold 20-39, Dead<20. |
| **dependencies** | H2-W8-001 |
| **files_expected** | engine/lead_classifier.py, enums/lead_class.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 5 classes; Thresholds; Auto-classify |

### H2-W8-005: CRM routing: score-based, zone-based, round-robin. Configurable rules.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-005 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-005 |
| **description** | CRM routing: score-based, zone-based, round-robin. Configurable rules. |
| **dependencies** | H2-W8-004, H2-W5-004 |
| **files_expected** | engine/crm_routing_engine.py, config/routing_rules.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 3 strategies; Rules; Round-robin |

### H2-W8-006: 7-factor scoring: engagement, recency, frequency, monetary, depth, response, channel.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-006 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-006 |
| **description** | 7-factor scoring: engagement, recency, frequency, monetary, depth, response, channel. |
| **dependencies** | H2-W8-001 |
| **files_expected** | scoring/seven_factor_scoring.py, config/factor_weights.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P2 |
| **acceptance_criteria** | 7 factors; Weights; Tracked |

### H2-W8-007: Behavior tracking: last_activity, login_count, search_count, view_count, contact_count, response_rat

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-007 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-007 |
| **description** | Behavior tracking: last_activity, login_count, search_count, view_count, contact_count, response_rate. |
| **dependencies** | None |
| **files_expected** | models/user_behavior.py, services/behavior_tracking_service.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Fields; Data collection; Analytics |

### H2-W8-008: 4-layer anti-fraud: identity, behavior, velocity, blacklist. Auto-suspension.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-008 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-008 |
| **description** | 4-layer anti-fraud: identity, behavior, velocity, blacklist. Auto-suspension. |
| **dependencies** | None |
| **files_expected** | engine/anti_fraud_engine.py, config/fraud_rules.json, services/fraud_monitoring_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P2 |
| **acceptance_criteria** | 4 layers; Rules; Suspension |

### H2-W8-009: Post-interaction agent rating 1-5. Recency-weighted average.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-009 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-009 |
| **description** | Post-interaction agent rating 1-5. Recency-weighted average. |
| **dependencies** | None |
| **files_expected** | models/agent_rating.py, services/rating_service.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Prompt; 1-5; Recency bias |

### H2-W8-010: Feedback handling: collection, aggregation, reporting. Categories.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-010 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-010 |
| **description** | Feedback handling: collection, aggregation, reporting. Categories. |
| **dependencies** | None |
| **files_expected** | models/feedback.py, services/feedback_service.py, analytics/feedback_analytics.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | API; Categories; Trends |

### H2-W8-011: Lead SLA by class: Hot=15m, Warm=1h, Warmish=4h, Cold=24h, Dead=48h.

| Field | Value |
|-------|-------|
| **task_id** | H2-W8-011 |
| **wave** | 8 |
| **domain** | crm |
| **extension_ids** | EXT-CRM-011 |
| **description** | Lead SLA by class: Hot=15m, Warm=1h, Warmish=4h, Cold=24h, Dead=48h. |
| **dependencies** | H2-W8-004 |
| **files_expected** | models/lead_sla.py, services/lead_sla_service.py, config/sla_thresholds.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Thresholds; Breach; Escalation |

\n## Wave 9 — Relationship and Consent\n\n### H2-W9-001: Match consent tracking: demandeur_decision, holder_decision, consent_ids, double_consent_at, deadlin

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-001 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-001 |
| **description** | Match consent tracking: demandeur_decision, holder_decision, consent_ids, double_consent_at, deadline. |
| **dependencies** | H2-W6-001 |
| **files_expected** | models/match_consent.py, state_machines/match_consent_machine.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Fields on Match; Consent states; Deadline |

### H2-W9-002: Proposal workflow: score>=60 and rank<=10 triggers proposal.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-002 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-002 |
| **description** | Proposal workflow: score>=60 and rank<=10 triggers proposal. |
| **dependencies** | H2-W9-001 |
| **files_expected** | models/proposal.py, workflows/proposal_workflow.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Proposal create; Notify; Deadline |

### H2-W9-003: Double consent: C1 demandeur, C2 holder. Both required for relationship.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-003 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-003 |
| **description** | Double consent: C1 demandeur, C2 holder. Both required for relationship. |
| **dependencies** | H2-W9-001 |
| **files_expected** | models/consent.py, workflows/double_consent_workflow.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | C1; C2; Both required |

### H2-W9-004: Relationship entity after double consent. Links demandeur, holder, property, agent.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-004 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-004 |
| **description** | Relationship entity after double consent. Links demandeur, holder, property, agent. |
| **dependencies** | H2-W9-003 |
| **files_expected** | models/relationship.py, enums/relationship_status.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | Entity; Created on consent; Status |

### H2-W9-005: Participant roles: demandeur, holder, agent_demandeur, agent_holder, mediator.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-005 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-005 |
| **description** | Participant roles: demandeur, holder, agent_demandeur, agent_holder, mediator. |
| **dependencies** | H2-W9-004 |
| **files_expected** | enums/relationship_role.py, models/relationship_participant.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 5 roles; Assignment; Visibility |

### H2-W9-006: Introduction tracking: method, outcome, assigned agent.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-006 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-006 |
| **description** | Introduction tracking: method, outcome, assigned agent. |
| **dependencies** | H2-W9-004 |
| **files_expected** | models/introduction.py, services/introduction_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Record; Method; Outcome |

### H2-W9-007: Shared data scope per relationship. Field-level visibility.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-007 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-007 |
| **description** | Shared data scope per relationship. Field-level visibility. |
| **dependencies** | H2-W9-004 |
| **files_expected** | models/data_scope.py, config/scope_templates.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Defined; Per-field control |

### H2-W9-008: Consent lifecycle: requested, granted, active, expired, revoked. Valid transitions.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-008 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-008 |
| **description** | Consent lifecycle: requested, granted, active, expired, revoked. Valid transitions. |
| **dependencies** | H2-W9-003 |
| **files_expected** | state_machines/consent_machine.py, enums/consent_status.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P1 |
| **acceptance_criteria** | 5 states; Transitions; Events |

### H2-W9-009: Revocation by either party. Relationship pause. Notification. Data restriction.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-009 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-009 |
| **description** | Revocation by either party. Relationship pause. Notification. Data restriction. |
| **dependencies** | H2-W9-008 |
| **files_expected** | workflows/revocation_workflow.py, services/revocation_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Revoke; Pause; Notify |

### H2-W9-010: Consent expiration 30 days. Cron check. Re-consent flow.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-010 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-010 |
| **description** | Consent expiration 30 days. Cron check. Re-consent flow. |
| **dependencies** | H2-W9-008 |
| **files_expected** | services/expiration_service.py, cron/consent_expiration_job.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Period; Cron; Re-consent |

### H2-W9-011: Idempotency for consent operations. Keys prevent duplicates.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-011 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-011 |
| **description** | Idempotency for consent operations. Keys prevent duplicates. |
| **dependencies** | H2-W9-008 |
| **files_expected** | services/idempotency_service.py, middleware/idempotency_middleware.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Key validation; Prevention |

### H2-W9-012: Audit trail for consent changes. Actor, action, timestamp, state.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-012 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-012 |
| **description** | Audit trail for consent changes. Actor, action, timestamp, state. |
| **dependencies** | H2-W9-008, H2-W11-002 |
| **files_expected** | models/consent_audit.py, services/consent_audit_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Log; Actor tracking; Immutable |

### H2-W9-013: Human handover: automated -> human agent -> relationship manager.

| Field | Value |
|-------|-------|
| **task_id** | H2-W9-013 |
| **wave** | 9 |
| **domain** | relationship_consent |
| **extension_ids** | EXT-RC-013 |
| **description** | Human handover: automated -> human agent -> relationship manager. |
| **dependencies** | H2-W9-004 |
| **files_expected** | workflows/human_handover_workflow.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Handover; Agent assign; Tracking |

\n## Wave 10 — Workflows and NBA\n\n### H2-W10-001: Matching lifecycle 10 states: created, scored, proposed, demandeur_consented, holder_consented, rela

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-001 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-001 |
| **description** | Matching lifecycle 10 states: created, scored, proposed, demandeur_consented, holder_consented, relationship, active, expired, closed, archived. |
| **dependencies** | H2-W6-001 |
| **files_expected** | state_machines/matching_lifecycle.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 10 states; Transitions; Consent |

### H2-W10-002: Contact lifecycle 6 states: initiated, demandeur_consented, holder_consented, active, closed, archiv

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-002 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-002 |
| **description** | Contact lifecycle 6 states: initiated, demandeur_consented, holder_consented, active, closed, archived. Double consent. |
| **dependencies** | None |
| **files_expected** | state_machines/contact_lifecycle.py, models/contact.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 6 states; Double consent |

### H2-W10-003: Visit lifecycle 9 states: requested, scheduled, confirmed, reminder, in_progress, completed, cancell

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-003 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-003 |
| **description** | Visit lifecycle 9 states: requested, scheduled, confirmed, reminder, in_progress, completed, cancelled, no_show, rescheduled. |
| **dependencies** | None |
| **files_expected** | state_machines/visit_lifecycle.py, models/visit.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 9 states; Schedule; No-show; NBA |

### H2-W10-004: Transaction lifecycle 10 states: initiated, offer, negotiation, accepted, docs, signed, payment, com

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-004 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-004 |
| **description** | Transaction lifecycle 10 states: initiated, offer, negotiation, accepted, docs, signed, payment, completed, cancelled, disputed. |
| **dependencies** | None |
| **files_expected** | state_machines/transaction_lifecycle.py, models/transaction.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 10 states; Doc requirements; Payment |

### H2-W10-005: Paid Services & Payment combined lifecycle 18 states. ServiceOrder+Payment integration.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-005 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-005 |
| **description** | Paid Services & Payment combined lifecycle 18 states. ServiceOrder+Payment integration. |
| **dependencies** | H2-W7-001, H2-W7-002 |
| **files_expected** | state_machines/service_payment_lifecycle.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 18 states; Integration; Campay |

### H2-W10-006: Incident lifecycle 8 states. 12 types, 4 priorities. SLA integration.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-006 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-006 |
| **description** | Incident lifecycle 8 states. 12 types, 4 priorities. SLA integration. |
| **dependencies** | None |
| **files_expected** | state_machines/incident_lifecycle.py, models/incident.py, enums/incident_type.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 8 states; 12 types; 4 priorities |

### H2-W10-007: Mediation lifecycle 8 states for dispute resolution.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-007 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-007 |
| **description** | Mediation lifecycle 8 states for dispute resolution. |
| **dependencies** | H2-W10-006 |
| **files_expected** | state_machines/mediation_lifecycle.py, models/mediation.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 8 states; Mediator assign; Resolution |

### H2-W10-008: CRM Pipeline 8 stages: lead_in, qualification, proposition, negotiation, closing, won, lost, recycle

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-008 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-008 |
| **description** | CRM Pipeline 8 stages: lead_in, qualification, proposition, negotiation, closing, won, lost, recycled. |
| **dependencies** | H2-W8-001, H2-W8-004, H2-W8-005 |
| **files_expected** | state_machines/crm_pipeline.py, models/lead_pipeline.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | 8 stages; Scoring; Routing |

### H2-W10-009: Publication lifecycle 11 states. SIE integration. Multi-channel.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-009 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-009 |
| **description** | Publication lifecycle 11 states. SIE integration. Multi-channel. |
| **dependencies** | None |
| **files_expected** | state_machines/publication_lifecycle.py, models/publication.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 11 states; SIE; Channel mgmt |

### H2-W10-010: Redirection lifecycle 12 states. Bot/dedup detection.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-010 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-010 |
| **description** | Redirection lifecycle 12 states. Bot/dedup detection. |
| **dependencies** | None |
| **files_expected** | state_machines/redirection_lifecycle.py, models/redirection.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 12 states; Bot detect |

### H2-W10-011: Conversion & Attribution 12 states. Last-touch attribution.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-011 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-011 |
| **description** | Conversion & Attribution 12 states. Last-touch attribution. |
| **dependencies** | None |
| **files_expected** | state_machines/conversion_lifecycle.py, models/conversion.py, analytics/attribution_model.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | 12 states; Attribution |

### H2-W10-012: Agent Invitation 7 states. Secure link. Onboarding steps.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-012 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-012 |
| **description** | Agent Invitation 7 states. Secure link. Onboarding steps. |
| **dependencies** | None |
| **files_expected** | state_machines/agent_invitation_lifecycle.py, models/agent_invitation.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 7 states; Secure link; Steps |

### H2-W10-013: Identity Resolution 5 states. Signal matching for duplicates.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-013 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-013 |
| **description** | Identity Resolution 5 states. Signal matching for duplicates. |
| **dependencies** | None |
| **files_expected** | state_machines/identity_resolution_lifecycle.py, models/identity_resolution.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P3 |
| **acceptance_criteria** | 5 states; Signal matching; Dedup |

### H2-W10-014: Orchestrator workflow engine. Delegates to sub-workflows: matching, contact, visit, transaction, ser

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-014 |
| **wave** | 10 |
| **domain** | workflows |
| **extension_ids** | EXT-WF-014 |
| **description** | Orchestrator workflow engine. Delegates to sub-workflows: matching, contact, visit, transaction, service. |
| **dependencies** | H2-W10-001, H2-W10-002, H2-W10-003, H2-W10-004, H2-W10-005 |
| **files_expected** | engine/orchestrator_engine.py, state_machines/orchestrator_machine.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P2 |
| **acceptance_criteria** | Delegation; Events; Coordination |

### H2-W10-015: SLA registry per property type per state. Configurable thresholds.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-015 |
| **wave** | 10 |
| **domain** | sla |
| **extension_ids** | EXT-SLA-001 |
| **description** | SLA registry per property type per state. Configurable thresholds. |
| **dependencies** | H2-W10-014 |
| **files_expected** | models/sla_registry.py, config/sla_property_thresholds.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Per type/state; Duration |

### H2-W10-016: SLA per workflow state. Duration per entity type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-016 |
| **wave** | 10 |
| **domain** | sla |
| **extension_ids** | EXT-SLA-002 |
| **description** | SLA per workflow state. Duration per entity type. |
| **dependencies** | H2-W10-014 |
| **files_expected** | config/sla_state_thresholds.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | State-level; Entity-specific |

### H2-W10-017: Priority-based SLA P0-P3. Breach detection and escalation.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-017 |
| **wave** | 10 |
| **domain** | sla |
| **extension_ids** | EXT-SLA-003 |
| **description** | Priority-based SLA P0-P3. Breach detection and escalation. |
| **dependencies** | H2-W10-015 |
| **files_expected** | models/sla_priority.py, services/sla_service.py, config/sla_priority_thresholds.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | P0-P3; Breach; Escalation |

### H2-W10-018: Breach detection engine. Configurable check intervals.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-018 |
| **wave** | 10 |
| **domain** | sla |
| **extension_ids** | EXT-SLA-004 |
| **description** | Breach detection engine. Configurable check intervals. |
| **dependencies** | H2-W10-017 |
| **files_expected** | engine/breach_detection_engine.py, cron/sla_breach_check_job.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Service; Intervals |

### H2-W10-019: 3-tier SLA escalation. Configurable actions per tier.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-019 |
| **wave** | 10 |
| **domain** | sla |
| **extension_ids** | EXT-SLA-005 |
| **description** | 3-tier SLA escalation. Configurable actions per tier. |
| **dependencies** | H2-W10-018 |
| **files_expected** | workflows/sla_escalation_workflow.py, config/escalation_actions.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 3 tiers; Actions |

### H2-W10-020: Holder silence escalation. Reminder intervals. Escalate on silence.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-020 |
| **wave** | 10 |
| **domain** | sla |
| **extension_ids** | EXT-SLA-006 |
| **description** | Holder silence escalation. Reminder intervals. Escalate on silence. |
| **dependencies** | H2-W10-018 |
| **files_expected** | services/holder_silence_service.py, config/silence_thresholds.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Tracking; Reminders; Escalation |

### H2-W10-021: NBA per state per workflow. State-specific action registry.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-021 |
| **wave** | 10 |
| **domain** | nba |
| **extension_ids** | EXT-NBA-001 |
| **description** | NBA per state per workflow. State-specific action registry. |
| **dependencies** | H2-W10-014 |
| **files_expected** | engine/nba_engine.py, config/nba_registry.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Per state; Actions; Recs |

### H2-W10-022: 9-level NBA priority. Action-specific assignment.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-022 |
| **wave** | 10 |
| **domain** | nba |
| **extension_ids** | EXT-NBA-002 |
| **description** | 9-level NBA priority. Action-specific assignment. |
| **dependencies** | H2-W10-021 |
| **files_expected** | enums/nba_priority.py, config/nba_priority_assignments.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 9 levels; Per action |

### H2-W10-023: Follow-up calendar: J1, J7, J30, J90. Auto-reminders.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-023 |
| **wave** | 10 |
| **domain** | nba |
| **extension_ids** | EXT-NBA-003 |
| **description** | Follow-up calendar: J1, J7, J30, J90. Auto-reminders. |
| **dependencies** | H2-W10-021 |
| **files_expected** | services/follow_up_calendar_service.py, cron/follow_up_reminder_job.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 4 intervals; Reminders; Config |

### H2-W10-024: NBA recalculation on SLA breach events.

| Field | Value |
|-------|-------|
| **task_id** | H2-W10-024 |
| **wave** | 10 |
| **domain** | nba |
| **extension_ids** | EXT-NBA-004 |
| **description** | NBA recalculation on SLA breach events. |
| **dependencies** | H2-W10-021, H2-W10-018 |
| **files_expected** | engine/nba_recalculation_engine.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Recalc on breach; Adjust |

\n## Wave 11 — Events, Audit and Permissions\n\n### H2-W11-001: Enriched Event: entity_type, entity_id, actor_id, previous/new_state, transition, source, correlatio

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-001 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-001 |
| **description** | Enriched Event: entity_type, entity_id, actor_id, previous/new_state, transition, source, correlation_id, severity, privacy_level, retention_days, metadata, schema_version. |
| **dependencies** | None |
| **files_expected** | models/event.py, enums/event_enums.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | 13 attributes; Entity ref; Actor; State tracking |

### H2-W11-002: Typed Event Catalog: user.*, property.*, match.*, consent.*, payment.* etc. Schema per type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-002 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-002 |
| **description** | Typed Event Catalog: user.*, property.*, match.*, consent.*, payment.* etc. Schema per type. |
| **dependencies** | H2-W11-001 |
| **files_expected** | catalog/event_catalog.json, schemas/event_schemas.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Types defined; Schema per type; Versioned |

### H2-W11-003: Audit trail: actor, action, timestamp, previous/current values, IP, user_agent.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-003 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-003 |
| **description** | Audit trail: actor, action, timestamp, previous/current values, IP, user_agent. |
| **dependencies** | H2-W11-001 |
| **files_expected** | models/audit_trail.py, services/audit_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Sensitive ops; Immutable; Queryable |

### H2-W11-004: Retention policy per event type. Configurable days. Auto-archive/purge.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-004 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-004 |
| **description** | Retention policy per event type. Configurable days. Auto-archive/purge. |
| **dependencies** | H2-W11-002 |
| **files_expected** | config/retention_policies.json, cron/event_retention_job.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Per-type; Auto-archive; Purge |

### H2-W11-005: Privacy levels: public, internal, restricted, confidential. Access control.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-005 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-005 |
| **description** | Privacy levels: public, internal, restricted, confidential. Access control. |
| **dependencies** | H2-W11-002 |
| **files_expected** | enums/event_privacy.py, services/event_access_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | 4 levels; Access control |

### H2-W11-006: Event consumers registry. Webhooks, queues, consumer groups per type.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-006 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-006 |
| **description** | Event consumers registry. Webhooks, queues, consumer groups per type. |
| **dependencies** | H2-W11-002 |
| **files_expected** | models/event_consumer.py, services/event_bus_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Registry; Webhooks; Bindings |

### H2-W11-007: Correlation ID for event chains. Links related events.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-007 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-007 |
| **description** | Correlation ID for event chains. Links related events. |
| **dependencies** | H2-W11-001 |
| **files_expected** | middleware/correlation_middleware.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | ID on events; Chain tracking |

### H2-W11-008: Event sourcing: append-only log, replay, snapshots.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-008 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-008 |
| **description** | Event sourcing: append-only log, replay, snapshots. |
| **dependencies** | H2-W11-001 |
| **files_expected** | engine/event_sourcing_engine.py, services/replay_service.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P3 |
| **acceptance_criteria** | Append-only; Replay; Snapshots |

### H2-W11-009: Event delivery: at-least-once, retry backoff, dead letter queue.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-009 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-009 |
| **description** | Event delivery: at-least-once, retry backoff, dead letter queue. |
| **dependencies** | H2-W11-006 |
| **files_expected** | services/event_delivery_service.py, config/delivery_config.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Delivery guarantee; Retry; DLQ |

### H2-W11-010: Event monitoring: throughput, error rates, latency, consumer health.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-010 |
| **wave** | 11 |
| **domain** | event_audit |
| **extension_ids** | EXT-EVT-010 |
| **description** | Event monitoring: throughput, error rates, latency, consumer health. |
| **dependencies** | H2-W11-006 |
| **files_expected** | monitoring/event_dashboard.py, analytics/event_metrics.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P3 |
| **acceptance_criteria** | Throughput; Errors; Health |

### H2-W11-011: Approval workflow (Niveau 4): approver_role, target_type, status, reviewed_by.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-011 |
| **wave** | 11 |
| **domain** | permission_model |
| **extension_ids** | EXT-PERM-001 |
| **description** | Approval workflow (Niveau 4): approver_role, target_type, status, reviewed_by. |
| **dependencies** | None |
| **files_expected** | models/approval_workflow.py, workflows/approval_workflow.py, enums/approval_status.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Model; Role-based; Status |

### H2-W11-012: Read permission (Niveau 1). Explicit RBAC read check.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-012 |
| **wave** | 11 |
| **domain** | permission_model |
| **extension_ids** | EXT-PERM-002 |
| **description** | Read permission (Niveau 1). Explicit RBAC read check. |
| **dependencies** | H2-W11-011 |
| **files_expected** | services/permission_service.py, enums/permission_level.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P2 |
| **acceptance_criteria** | Read perms; RBAC |

### H2-W11-013: Create permission (Niveau 2). Per-role create matrix.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-013 |
| **wave** | 11 |
| **domain** | permission_model |
| **extension_ids** | EXT-PERM-003 |
| **description** | Create permission (Niveau 2). Per-role create matrix. |
| **dependencies** | H2-W11-012 |
| **files_expected** | permissions/create_permission.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | Per role; Matrix |

### H2-W11-014: Edit permission (Niveau 3). Three tiers: own, managed, all.

| Field | Value |
|-------|-------|
| **task_id** | H2-W11-014 |
| **wave** | 11 |
| **domain** | permission_model |
| **extension_ids** | EXT-PERM-004 |
| **description** | Edit permission (Niveau 3). Three tiers: own, managed, all. |
| **dependencies** | H2-W11-012 |
| **files_expected** | permissions/edit_permission.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | low |
| **priority** | P2 |
| **acceptance_criteria** | 3 tiers; Enforcement |

\n## Wave 12 — APIs, Compatibility and Migration\n\n### H2-W12-001: New REST endpoints for Match, ServiceOrder, Payment, Lead, Visit, Transaction, Relationship, Geograp

| Field | Value |
|-------|-------|
| **task_id** | H2-W12-001 |
| **wave** | 12 |
| **domain** | api |
| **extension_ids** | EXT-API-001 |
| **description** | New REST endpoints for Match, ServiceOrder, Payment, Lead, Visit, Transaction, Relationship, GeographicUnit, Intent, Contact. |
| **dependencies** | H2-W6-001, H2-W7-001, H2-W7-002, H2-W8-001, H2-W10-003, H2-W10-004, H2-W9-004, H2-W5-001, H2-W6-014, H2-W10-002 |
| **files_expected** | api/matches.py, api/services.py, api/payments.py, api/leads.py, api/visits.py, api/transactions.py, api/relationships.py, api/geography.py, api/intents.py, api/contacts.py |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | REST for all; Paginated; CRUD |

### H2-W12-002: API versioning: URL-based /v1/ /v2/. Deprecation headers. Migration guide.

| Field | Value |
|-------|-------|
| **task_id** | H2-W12-002 |
| **wave** | 12 |
| **domain** | api |
| **extension_ids** | EXT-API-002 |
| **description** | API versioning: URL-based /v1/ /v2/. Deprecation headers. Migration guide. |
| **dependencies** | H2-W12-001 |
| **files_expected** | middleware/api_versioning.py, docs/api_migration_guide.md |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Versioned; Deprecation; Guide |

### H2-W12-003: Backward compat layer. V1 endpoints unchanged. Feature flags for V2.

| Field | Value |
|-------|-------|
| **task_id** | H2-W12-003 |
| **wave** | 12 |
| **domain** | api |
| **extension_ids** | EXT-API-003 |
| **description** | Backward compat layer. V1 endpoints unchanged. Feature flags for V2. |
| **dependencies** | H2-W12-002 |
| **files_expected** | middleware/backward_compat.py, config/feature_flags.json |
| **migration_required** | False |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | V1 unchanged; Feature flags; Compat tests |

### H2-W12-004: Data migrations: trust level defaults, property family mapping, location data.

| Field | Value |
|-------|-------|
| **task_id** | H2-W12-004 |
| **wave** | 12 |
| **domain** | migration |
| **extension_ids** | EXT-MIG-001 |
| **description** | Data migrations: trust level defaults, property family mapping, location data. |
| **dependencies** | H2-W1-001, H2-W1-002, H2-W3-001 |
| **files_expected** | migrations/xxx_add_trust_level.py, migrations/xxx_add_property_family.py, scripts/migrate_locations.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | Trust defaults; Family mapping; Location; Rollback |

### H2-W12-005: Seed migrations: service catalog, qualification matrices, geography data.

| Field | Value |
|-------|-------|
| **task_id** | H2-W12-005 |
| **wave** | 12 |
| **domain** | migration |
| **extension_ids** | EXT-MIG-002 |
| **description** | Seed migrations: service catalog, qualification matrices, geography data. |
| **dependencies** | H2-W1-003, H2-W2-001, H2-W5-009 |
| **files_expected** | migrations/xxx_seed_service_catalog.py, migrations/xxx_seed_qualification_matrices.py, migrations/xxx_seed_geography.py |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | medium |
| **priority** | P1 |
| **acceptance_criteria** | Seeded catalog; Matrices loaded; Geo populated |

### H2-W12-006: State machine migration: map existing project states to new dossier states.

| Field | Value |
|-------|-------|
| **task_id** | H2-W12-006 |
| **wave** | 12 |
| **domain** | migration |
| **extension_ids** | EXT-MIG-003 |
| **description** | State machine migration: map existing project states to new dossier states. |
| **dependencies** | H2-W4-002, H2-W4-015 |
| **files_expected** | migrations/xxx_migrate_project_states.py, scripts/state_mapping.json |
| **migration_required** | True |
| **tests_required** | True |
| **risk** | high |
| **priority** | P1 |
| **acceptance_criteria** | States mapped; No data loss |

## Summary Statistics

- **Total Tasks:** 204
- **Total Extensions Covered:** 282
- **By Priority:** P0=2, P1=70, P2=88, P3=23, P4=21
- **By Risk:** high=25, low=112, medium=67

