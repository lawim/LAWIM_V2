# ROLE CROSSWALK — Heritage Gold → LAWIM_V2

**Date:** 2026-07-15  
**Status:** Draft for review  
**Scope:** Full semantic mapping between Heritage Gold role model (legacy LAWIM) and current LAWIM_V2 role system.

---

## Executive Summary

Heritage Gold defines a rich role system with **6 role families**, **7 hierarchical levels**, **4 permission levels**, **6 trust levels**, **8 badges**, and **7 partner roles**. Current LAWIM_V2 collapses these into **5 official roles** (`admin`, `manager`, `operator`, `partner`, `user`) with **27 business profiles** providing domain-specific granularity.

**Key findings:**

| Aspect | Heritage Gold | LAWIM_V2 | Mapping |
|--------|---------------|----------|---------|
| Role families | 6 families | 5 official roles | NORMALIZED_MATCH (one-to-one for basic roles) |
| Role hierarchy | 7 levels (L1-L7) | No hierarchy; flat official roles | PARTIAL_MATCH → EXTENSION_REQUIRED |
| Permission levels | 4 levels (Read/Create/Edit/Approve) | Implicit per-role; no explicit permission model | PARTIAL_MATCH → EXTENSION_REQUIRED |
| Trust levels | 6 levels | Not implemented | EXTENSION_REQUIRED |
| Badges | 8 badges | Not implemented | EXTENSION_REQUIRED |
| Partner roles | 7 partners | 1 official role + 14 business profiles | NORMALIZED_MATCH |
| Agency hierarchy | 4 tiers (resp.→admin→agent→assistant) | Organization model exists; no agency roles | EXTENSION_REQUIRED |

**Critical gaps:** Trust levels, badges, agency hierarchy, and explicit permission levels have no equivalent in LAWIM_V2 and require system extensions.

---

## 1. Role Family Comparison Table

| ID | Heritage Gold Family | Heritage Roles | LAWIM_V2 Official Role | LAWIM_V2 Business Profiles | Mapping Status |
|----|----------------------|----------------|------------------------|---------------------------|----------------|
| GOLD-RL-001 | Demandeur | demandeur, buyer, tenant, investor, property_seeker | `user` | buyer, tenant, land_seeker, investor | NORMALIZED_MATCH |
| GOLD-RL-002 | Proprietaire | owner, seller, détenteur | `user` | owner, property_manager | NORMALIZED_MATCH |
| GOLD-RL-003 | Agent | agent_immobilier, broker | `operator` | real_estate_agent | NORMALIZED_MATCH |
| GOLD-RL-004 | Operateur | responsable_agence, administrateur_agence, assistant | `operator` / `manager` | (none specific) | PARTIAL_MATCH |
| GOLD-RL-005 | Superviseur | conseiller, médiateur, responsable_opérationnel | `manager` | (none specific) | PARTIAL_MATCH |
| GOLD-RL-006 | Admin | administrateur, administrateur_principal | `admin` | (none) | EXACT_MATCH |

---

## 2. Detailed Role Mapping Table

### 2.1 Role Families

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-001 | Demandeur family (buyer, tenant, investor, property_seeker) | Role Family | GOLD-RL-001 | official_role="user" + business_profile ∈ {buyer, tenant, land_seeker, investor} | User Roles | OFFICIAL_USER_ROLES, BUSINESS_PROFILES | NORMALIZED_MATCH | Heritage Gold fuses buyer+tenant+investor under one family; LAWIM_V2 uses business profiles for differentiation | Map all demandeur-family users to role="user"; retain original role in metadata for traceability | None — `user` role exists and handles all demandeur functions | Business profile drives qualification; legacy demandeur maps to multiple V2 profiles | Same search scope for all demandeur-type users | Matching logic must consider business_profile not just role | CRM treats all demandeur as "user" — loss of demandeur-specific context | Security level unchanged (lowest privilege) | Implement business_profile on User model; migrate legacy role as fallback | APPROVED |
| XW-RL-002 | Proprietaire family (owner, seller, détenteur) | Role Family | GOLD-RL-002 | official_role="user" + business_profile ∈ {owner, property_manager} | User Roles | OFFICIAL_USER_ROLES, BUSINESS_PROFILES | NORMALIZED_MATCH | Heritage Gold treats seller as contextual role of owner; LAWIM_V2 has dedicated "owner" profile | Map proprietaire users to role="user" + business_profile="owner" | None | Qualification forms must differentiate sell vs. own intent | Listings owned by these users | Owner context preserved via business_profile | CRM must map proprietaire → owner profile | Same security as user role | Use business_profile="owner" for all legacy proprietaire users | APPROVED |
| XW-RL-003 | Agent family (agent_immobilier, broker) | Role Family | GOLD-RL-003 | official_role="operator" + business_profile="real_estate_agent" | User Roles | OFFICIAL_USER_ROLES, BUSINESS_PROFILES | NORMALIZED_MATCH | Heritage Gold agent=broker; V2 has "real_estate_agent" profile and also "agent" profile (LAWIM internal) | Map agent-family users to role="operator" + business_profile="real_estate_agent" | Operator role grants elevated permissions; verify legacy agent permissions match | Agent qualification workflows are preserved via business_profile | Agent sees listings; no change | Agent matching rules unchanged | CRM agent categorization aligned | Operator role has moderate privilege — acceptable for agent functions | Map to operator role with real_estate_agent business profile | APPROVED |
| XW-RL-004 | Operateur family (responsable_agence, administrateur_agence, assistant) | Role Family | GOLD-RL-004 | official_role="operator" or "manager"; agency hierarchy not modeled | User Roles | OFFICIAL_USER_ROLES | PARTIAL_MATCH | Heritage Gold has 3 agency roles with hierarchy; V2 has flat operator/manager with no agency-responsible distinction | Requires new agency role field or Organization-level role assignment | Current User.organizationId exists but no agency-specific role; migration must assign a default | App-level role checks (isAdmin, isOperator) need extension for agency-level authorization | Agency-level listing visibility unaffected | Agency hierarchy affects lead routing — currently broken | CRM lacks agency role field; critical for agency management | Agency roles control access to agency resources; gap is a security concern | Add agency_role field to User or Organization membership model | PENDING_APPROVAL |
| XW-RL-005 | Superviseur family (conseiller, médiateur, responsable_opérationnel) | Role Family | GOLD-RL-005 | official_role="manager" | User Roles | OFFICIAL_USER_ROLES | PARTIAL_MATCH | Heritage Gold Supervisor includes mediation, counseling, operational oversight — V2 "manager" is generic | Map to role="manager"; supervision-specific functions need workflow-layer mapping | Low — small user segment | Manager role needs mediation/supervision permissions added | Supervisors need cross-entity visibility; verify manager role provides this | Supervisor overriding of matches may be needed | CRM supervision workflows not implemented | Manager role has elevated privilege; acceptable | Extend manager role with supervision capabilities | PENDING_APPROVAL |
| XW-RL-006 | Admin family (administrateur, administrateur_principal) | Role Family | GOLD-RL-006 | official_role="admin" | User Roles | OFFICIAL_USER_ROLES | EXACT_MATCH | Direct match; V2 admin covers both administrateur and administrateur_principal | Direct 1:1 mapping | None | Full system access as before | Full visibility | Can override any match | Admin CRM tools equivalent | Highest privilege; same as legacy | No action required; already aligned | APPROVED |

### 2.2 Role Hierarchy

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-007 | demandeur (Level 1) | Role Hierarchy | GOLD-RL-007 | official_role="user" | User Roles | OFFICIAL_USER_ROLES | NORMALIZED_MATCH | Level-1 base role maps directly to lowest user tier | All level-1 users → role="user" | None | Base qualification unchanged | Base search access | Base matching eligibility | Basic CRM classification | Lowest privilege | 1:1 mapping | APPROVED |
| XW-RL-008 | vendeur/propriétaire (Level 2) | Role Hierarchy | GOLD-RL-008 | official_role="user" + business_profile="owner" | User Roles | OFFICIAL_USER_ROLES, BUSINESS_PROFILES | NORMALIZED_MATCH | Level-2 inherits from demandeur and adds ownership capabilities | Map to role="user" with owner profile | None | Owner-specific qualification sections activated | Owner sees own listings | Owner context for property matching | Owner CRM segment | Same as user; ownership is profile, not privilege | Business profile distinction | APPROVED |
| XW-RL-009 | agent (Level 3) | Role Hierarchy | GOLD-RL-009 | official_role="operator" + business_profile="real_estate_agent" | User Roles | OFFICIAL_USER_ROLES, BUSINESS_PROFILES | NORMALIZED_MATCH | Level-3 agent inherits from propriétaire and adds professional capabilities | Map to role="operator" | Operator role has elevated system access — audit required | Professional qualification workflows triggered | Agent listing management | Agent-level matching and proposal | Agent CRM tools | Operator privileges: moderate | Role escalation from user to operator needs approval | APPROVED |
| XW-RL-010 | agence (Level 4) | Role Hierarchy | GOLD-RL-010 | Organization model exists; no agency-level role | User Roles / Organization | schema.prisma (Organization model) | EXTENSION_REQUIRED | Heritage Gold "agence" is a role level; V2 has Organization entity but no "agency" user role | Organization entity can be used but agency-specific role field on User is missing | No runtime representation for agency role on User | Agency-level qualification aggregation not possible | Agency portfolio views depend on organization association | Lead routing to agency not implemented | Agency-level CRM missing | No agency-level access control | Add agency_role: "responsible" | admin | assistant field to User model for agency context | PENDING_APPROVAL |
| XW-RL-011 | assistant (Level 5) | Role Hierarchy | GOLD-RL-011 | official_role="operator" | User Roles | OFFICIAL_USER_ROLES | PARTIAL_MATCH | Heritage Gold assistant is an agency-support role below manager; V2 has no assistant-specific role | Map to role="operator" with business_profile or agency_role distinction | May over-privilege assistants who had fewer permissions in legacy | Assistant-specific qualification views lost | Assistant listing management | Assistant cannot override agent matches | CRM treats as operator | Operator may grant more access than assistant should have | Consider adding "assistant" to agency_role enum OR scope permissions by organization | PENDING_APPROVAL |
| XW-RL-012 | vice_master (Level 6) | Role Hierarchy | GOLD-RL-012 | official_role="manager" | User Roles | OFFICIAL_USER_ROLES | PARTIAL_MATCH | Heritage Gold vice_master is sub-admin supervisor; V2 manager is generic | Map to role="manager" | Some vice_master permissions may exceed manager capabilities | Supervision-level qualification needed | Cross-entity visibility | Match approval workflows | Management CRM tools | Manager privilege is elevated; acceptable for vice_master functions | Extend manager if specific vice_master permissions are needed | PENDING_APPROVAL |
| XW-RL-013 | master (Level 7) | Role Hierarchy | GOLD-RL-013 | official_role="admin" | User Roles | OFFICIAL_USER_ROLES | PARTIAL_MATCH | Heritage Gold master is top internal role (below admin); V2 admin combines both | Map to role="admin" | None — highest internal role | Full system oversight | Full visibility | Override authority | Admin CRM | Highest privilege | 1:1 mapping to admin role | APPROVED |

### 2.3 Permission Levels

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-014 | Niveau 1 — Lecture (Read) | Permission | GOLD-RL-014 | Implicit read access via role; no explicit permission system | Authorization | Implicit in role definitions | PARTIAL_MATCH | Heritage Gold has explicit 4-tier permission model; V2 permissions are implicit per role | No data migration needed — permissions are behavioral, not stored | All users have read access; no explicit permission check required | Read access for qualification data | Read listings | Read match results | Read CRM data | Read access is unrestricted for authenticated users | Implement explicit permission system if role-based access control needs fine-tuning | PENDING_APPROVAL |
| XW-RL-015 | Niveau 2 — Création (Create) | Permission | GOLD-RL-015 | Implicit create access; operator+ can create listings, user can create searches | Authorization | Implicit in role definitions | PARTIAL_MATCH | V2 creation rights are role-dependent but not formally modeled; Heritage Gold ties creation to specific role families | No data migration | Creation permission checks are hardcoded per feature | Create qualification entries | Create listings (operator+), create searches (user+) | Create match proposals | Create CRM records | Creation rights differ by role implicitly | Formalize Create permission level for each role | PENDING_APPROVAL |
| XW-RL-016 | Niveau 3 — Modification (Edit) | Permission | GOLD-RL-016 | Implicit edit access; users edit own, operators edit managed, admin edits all | Authorization | Implicit in role definitions | PARTIAL_MATCH | Heritage Gold ties Edit to items under responsibility; V2 has no formal "items under responsibility" concept | No data migration | Edit access granted by ownership or organization scope | Edit qualification responses | Edit own listings; agents edit managed listings | Edit proposals | Edit CRM records | Edit scoping is implicit and may be inconsistent | Formalize Edit permission scope (own vs. managed vs. all) | PENDING_APPROVAL |
| XW-RL-017 | Niveau 4 — Validation (Approve) | Permission | GOLD-RL-017 | No explicit approval level or workflow in V2 | Authorization | (none) | EXTENSION_REQUIRED | Heritage Gold requires approval for agency creation, listing validation, etc.; V2 has no approval workflow | N/A — new feature required | New approval workflow engine needed for listing validation, agency creation, professional verification | Qualification approval needed | Listing approval workflow | Match approval needed | CRM validation workflows | Approval is a security-critical function | Implement Approval permission level and workflow engine for admin/manager roles | PENDING_APPROVAL |

### 2.4 Trust Levels

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-018 | Niveau 1 — Nouveau compte | Trust Level | GOLD-RL-018 | Not implemented | — | — | EXTENSION_REQUIRED | No equivalent trust or verification level in V2 | New User field(s) required: trust_level, verification_status | Trust checks not performed; all users treated equally | Qualification may need trust-based branching | No trust-based search filtering | No trust-based match weighting | CRM lacks trust scoring | No verification gates for sensitive operations | Add trust_level field to User model with 6 levels matching Gold spec | PENDING_APPROVAL |
| XW-RL-019 | Niveau 2 — Téléphone vérifié | Trust Level | GOLD-RL-019 | Not implemented (phone exists but no verification flag) | — | — | EXTENSION_REQUIRED | Gold marks phone_verified as explicit trust step; V2 has phoneE164 but no verified flag | Add phone_verified Boolean to User | OTP verification flow needed | Phone verification may unlock certain features | No impact | Trust score affects match confidence | CRM trust indicator | Phone verification is low-security gate | Add phone_verified field; implement OTP verification | PENDING_APPROVAL |
| XW-RL-020 | Niveau 3 — Identité vérifiée | Trust Level | GOLD-RL-020 | Not implemented | — | — | EXTENSION_REQUIRED | Identity document validation; no equivalent in V2 | New identity_verified field; document storage | Identity verification workflow needed; admin validation | Identity-sensitive qualification flows | Trusted user badge | Higher match confidence for verified users | Verified identity CRM tag | Identity verification reduces fraud risk | Add identity_verified field; implement document upload + admin validation | PENDING_APPROVAL |
| XW-RL-021 | Niveau 4 — Documents pro validés | Trust Level | GOLD-RL-021 | Not implemented | — | — | EXTENSION_REQUIRED | Professional document validation for agents/partners; no equivalent in V2 | New professional_docs_verified field | Professional document upload + admin review workflow | Professional qualification unlocked | Trust badge on listings | Trusted professional indicator | Professional verification CRM | Validated professionals have elevated system trust | Add professional_docs_verified field; implement pro document workflow | PENDING_APPROVAL |
| XW-RL-022 | Niveau 5 — Professionnel vérifié | Trust Level | GOLD-RL-022 | Not implemented | — | — | EXTENSION_REQUIRED | Full professional verification (agent/partner); no equivalent in V2 | New professional_verified field | Professional status gates access to pro features | Full professional qualification trees | Verified pro badge on listings | Verified professionals prioritized in matches | Verified pro CRM segment | Full trust for professional operations | Add professional_verified field; complete verification workflow | PENDING_APPROVAL |
| XW-RL-023 | Niveau 6 — Compte de référence | Trust Level | GOLD-RL-023 | Not implemented | — | — | EXTENSION_REQUIRED | Highest trust level for reference accounts; no equivalent in V2 | New reference_account field | Reference status gates highest-trust features | Reference status unlocks premium qualification | Reference badge | Reference accounts recommended by system | Reference CRM status | Maximum system trust | Add reference_account field; manual grant by admin only | PENDING_APPROVAL |

### 2.5 Badges

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-024 | Badge: Téléphone vérifié | Badge | GOLD-RL-024 | Not implemented | — | — | EXTENSION_REQUIRED | Explicit badge display for phone verification | Derive from phone_verified trust level | Badge rendering system needed | Badge shown in qualification UI | Badge on user profiles | Trust badge influences match display | CRM displays badges | Badge is informational, not security-critical | Implement badge system tied to trust levels | PENDING_APPROVAL |
| XW-RL-025 | Badge: E-mail vérifié | Badge | GOLD-RL-025 | Not implemented | — | — | EXTENSION_REQUIRED | Email verification badge; no email_verified flag in V2 | Derive from email verification status | Badge rendering | Badge shown in qualification | Badge on user profiles | Trust badge | CRM badge | Informational | Add email_verified flag; implement badge | PENDING_APPROVAL |
| XW-RL-026 | Badge: Identité vérifiée | Badge | GOLD-RL-026 | Not implemented | — | — | EXTENSION_REQUIRED | Identity verification badge | Derive from identity_verified trust level | Badge rendering | Badge shown | Badge on profiles | Trust badge | CRM badge | Informational | Derive from trust level; implement badge display | PENDING_APPROVAL |
| XW-RL-027 | Badge: Propriétaire vérifié | Badge | GOLD-RL-027 | Not implemented | — | — | EXTENSION_REQUIRED | Property ownership verification badge | New owner_verified field or derive from documents | Badge rendering | Badge shown for owners | Badge on listings | Trust badge for owner listings | CRM badge | Owner verification reduces listing fraud | Add owner_verified field; implement document verification for owners | PENDING_APPROVAL |
| XW-RL-028 | Badge: Agence vérifiée | Badge | GOLD-RL-028 | Not implemented | — | — | EXTENSION_REQUIRED | Agency registration verification badge | New agency_verified field on Organization | Agency verification workflow + badge | Badge shown for agency listings | Badge on agency profile | Trust badge for agency listings | CRM badge | Agency verification prevents fake agencies | Add agency_verified to Organization model; implement verification workflow | PENDING_APPROVAL |
| XW-RL-029 | Badge: Partenaire LAWIM | Badge | GOLD-RL-029 | Not implemented | — | — | EXTENSION_REQUIRED | Partner validation badge (notaire, géomètre, banque) | Derive from professional_verified + partner profile | Badge rendering for partners | Badge shown for partner services | Badge on partner profiles | Trust badge for partner services | CRM badge | Partner status reduces fraud | Derive from professional_verified; add partner-specific badge | PENDING_APPROVAL |
| XW-RL-030 | Badge: Professionnel vérifié | Badge | GOLD-RL-030 | Not implemented | — | — | EXTENSION_REQUIRED | Professional status badge (agent, etc.) | Derive from professional_verified trust level | Badge rendering | Badge shown for pros | Badge on pro profiles | Trust badge for pro services | CRM badge | Professional verification is trust signal | Derive from professional_verified trust level | PENDING_APPROVAL |
| XW-RL-031 | Badge: Agent actif | Badge | GOLD-RL-031 | Not implemented | — | — | EXTENSION_REQUIRED | Agent fully onboarded and active badge | Derive from agent status fields | Badge rendering + active status tracking | Badge shown for active agents | Badge on agent profiles | Trust badge for agent matching | CRM badge | Active agent status is operational | Add is_active_agent field or derive from onboarding completion | PENDING_APPROVAL |

### 2.6 Agency Structure

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-032 | Agency definition (organization, not simple user) | Agency | GOLD-RL-032 | Organization model exists | Schema | schema.prisma (Organization) | NORMALIZED_MATCH | V2 Organization matches Gold agency concept | Direct 1:1 mapping of agency → Organization | Organization model handles agency-level grouping | Agency-level qualification | Agency portfolio | Agency-level matching | Agency CRM | Agency context preserved | No action needed | APPROVED |
| XW-RL-033 | Agency components (responsible + agents + admin + properties + files + validations + trust) | Agency | GOLD-RL-033 | Organization has users + properties; no agency-level validations or trust | Schema | schema.prisma | PARTIAL_MATCH | V2 has users+properties on Organization but lacks agency-level trust, validations, and admin role | Organization model needs trust_level, verified fields | Agency trust level not checked | Agency-level qualification aggregation | Agency portfolio views | Agency trust for matching | Agency CRM trust scoring | Agency trust gates certain operations | Add trust_level, verification fields to Organization model | PENDING_APPROVAL |
| XW-RL-034 | Agency creation (name, resp., phone, address, CNI, RCCM, tax ID) | Agency | GOLD-RL-034 | Organization creation exists but no RCCM/CNI/tax ID fields | Schema | schema.prisma (Organization) | PARTIAL_MATCH | V2 Organization missing required registration fields for agency creation | Add RCCM, tax_id, cni fields to Organization | Agency creation workflow needs these fields added | Registration qualification | N/A | N/A | CRM agency registration | Required fields validation | Add registration fields (rccm, tax_id, cni_document) to Organization model | PENDING_APPROVAL |
| XW-RL-035 | Agent onboarding flow | Agency | GOLD-RL-035 | No structured agent onboarding workflow | — | — | EXTENSION_REQUIRED | Gold defines step-by-step agent onboarding (invitation → account → phone → CNI → validation → active) | New onboarding workflow engine needed | Onboarding state machine | Agent qualification during onboarding | N/A | Agent activation gates matching | CRM onboarding pipeline | Onboarding includes identity verification | Implement agent onboarding workflow with state tracking | PENDING_APPROVAL |
| XW-RL-036 | Minimum 3 active agents for operational agency | Agency | GOLD-RL-036 | No minimum agent enforcement | — | — | EXTENSION_REQUIRED | Gold rule: agency needs min 3 active agents; V2 has no such constraint | New validation rule; may need agent count query | Agency operational status depends on agent count | Qualification for agency status | N/A | Agency matching limited if below threshold | CRM agency status | Operational rule affects agency capabilities | Add agency operational status rule; check agent count ≥ 3 | PENDING_APPROVAL |
| XW-RL-037 | Lead routing by geographic zone | Agency | GOLD-RL-037 | No lead routing system | — | — | EXTENSION_REQUIRED | Gold routes leads via agent_zones table; V2 has no routing mechanism | New lead routing engine needed | Lead assignment to agents by zone | Qualification may include zone | Search filtering by agent zone | Lead matching to agents | CRM lead assignment | Lead routing is operational | Implement geographic lead routing with agent_zone assignments | PENDING_APPROVAL |
| XW-RL-038 | Lead cost (500 FCFA default) | Agency | GOLD-RL-038 | No lead costing system | — | — | EXTENSION_REQUIRED | Gold charges agents per lead; V2 has no lead cost model | New billing/costing module needed | Lead cost deducted from agent credits | N/A | N/A | Lead cost affects matching proposals | CRM lead cost tracking | Financial impact | Implement lead costing with configurable price | PENDING_APPROVAL |
| XW-RL-039 | Agent credits & boosts | Agency | GOLD-RL-039 | No agent credit system | — | — | EXTENSION_REQUIRED | Gold has agent_credits and boost_purchases tables; V2 has no equivalent | New credit system fields and tables | Credit deduction per action | N/A | N/A | Boost affects matching priority | CRM credit tracking | Financial | Implement agent_credits (credits, total_spent, last_recharge) and boost_purchases (boost_type, price, expires_at) | PENDING_APPROVAL |
| XW-RL-040 | Agent rating (1-5) | Agency | GOLD-RL-040 | No agent rating system | — | — | EXTENSION_REQUIRED | Gold rates agents 1-5 after each interaction; V2 has no rating mechanism | New rating fields on User or Agent model | Rating calculation after interactions | Agent rating may affect qualification recommendations | Rating displayed on agent profile | Higher-rated agents prioritized in matching | CRM rating tracking | Rating is informational | Implement agent_rating field (1-5 scale) and post-interaction rating workflow | PENDING_APPROVAL |

### 2.7 Partner Roles

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-055 | Notaire | Partner Role | GOLD-RL-055 | official_role="partner" + business_profile="notary" | User Roles | USER_ROLE_ALIASES, BUSINESS_PROFILES | NORMALIZED_MATCH | Direct match: notary/notaire alias exists in V2 | Map to role="partner" + business_profile="notary" | Partner role has limited system access | Notary qualification workflows | Notary service listings | Notary matching for transactions | Partner CRM segment | Partner role: low internal privilege | 1:1 mapping; existing alias | APPROVED |
| XW-RL-056 | Géomètre | Partner Role | GOLD-RL-056 | official_role="partner" + business_profile="surveyor" | User Roles | USER_ROLE_ALIASES, BUSINESS_PROFILES | NORMALIZED_MATCH | Direct match: surveyor (géomètre) exists as business profile | Map to role="partner" | Partner role | Surveyor qualification | Surveyor service listings | Surveyor matching for property measurement | Partner CRM | Partner role | 1:1 mapping; business_profile="surveyor" | APPROVED |
| XW-RL-057 | Banque | Partner Role | GOLD-RL-057 | official_role="partner" + business_profile="bank" or "financing" | User Roles | USER_ROLE_ALIASES, BUSINESS_PROFILES | NORMALIZED_MATCH | Gold "Banque" → V2 "bank" or "financing" business profiles | Map to role="partner" + business_profile in {"bank", "financing"} | Partner role | Financing qualification | Bank service listings | Financing matching for buyers | Partner CRM | Partner role | Dual profile mapping; choose based on function | APPROVED |
| XW-RL-058 | Assurance | Partner Role | GOLD-RL-058 | official_role="partner" + business_profile="insurer" | User Roles | BUSINESS_PROFILES | NORMALIZED_MATCH | Gold "Assurance" → V2 "insurer" business profile | Map to role="partner" + business_profile="insurer" | Partner role | Insurance qualification | Insurance service listings | Insurance matching | Partner CRM | Partner role | 1:1 mapping; business_profile="insurer" | APPROVED |
| XW-RL-059 | Photographe | Partner Role | GOLD-RL-059 | official_role="partner" + business_profile="photographer" | User Roles | USER_ROLE_ALIASES, BUSINESS_PROFILES | NORMALIZED_MATCH | Direct match: photographer/photographe alias exists | Map to role="partner" + business_profile="photographer" | Partner role | Photography qualification | Photography service listings | Photography matching | Partner CRM | Partner role | 1:1 mapping; existing alias | APPROVED |
| XW-RL-060 | Artisan | Partner Role | GOLD-RL-060 | official_role="partner" + business_profile in {architect, engineer, technician, contractor, decorator, electrician, plumber, cleaner, mover} | User Roles | USER_ROLE_ALIASES, BUSINESS_PROFILES | ONE_TO_MANY | Gold "Artisan" is a single partner category; V2 has 9+ artisan business profiles with granular specializations | Map to role="partner" + most specific business_profile; legacy_data may need mapping rules | Partner role with specialized profile | Artisan-specific qualification trees | Artisan service listings | Artisan service matching by specialty | Partner CRM with specialization tag | Partner role | Granular mapping needed per artisan subtype | PENDING_APPROVAL |
| XW-RL-061 | Expert partenaire | Partner Role | GOLD-RL-061 | official_role="partner" + business_profile in {architect, engineer, surveyor, lawyer} | User Roles | BUSINESS_PROFILES | ONE_TO_MANY | Gold "Expert partenaire" is a generic domain expert; V2 has specific expert profiles | Map to role="partner" + business_profile based on expertise domain | Partner role | Expert qualification | Expert service listings | Expert matching | Partner CRM | Partner role | Map to specific business profile based on domain expertise | PENDING_APPROVAL |

### 2.8 Role-to-Journey Coverage

| crosswalk_id | legacy_concept | legacy_domain | legacy_source | current_concept | current_domain | current_source | mapping_status | semantic_differences | data_migration_impact | runtime_impact | qualification_impact | search_impact | matching_impact | CRM_impact | security_impact | recommended_resolution | decision_status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| XW-RL-041 | Property search journey | Journey | GOLD-RL-041 | Supported via user role + buyer/tenant/land_seeker/investor profiles | Journeys | Business flows | NORMALIZED_MATCH | Journey coverage maintained; business profile adds granularity | None | None | Qualification for search intent is profile-driven | Search unchanged | Matching uses profile context | CRM tracking of user intent | None | Already covered; no action | APPROVED |
| XW-RL-042 | Property listing journey | Journey | GOLD-RL-042 | Supported via operator role + real_estate_agent profile or user role + owner profile | Journeys | Business flows | NORMALIZED_MATCH | Journey coverage maintained; role+profile combination works | None | None | Listing qualification for owners/agents | Listing management unchanged | Listing matching | CRM listing tracking | None | Already covered; no action | APPROVED |
| XW-RL-043 | Matching & proposals journey | Journey | GOLD-RL-043 | Partially supported; matching engine exists but proposal workflows may differ | Journeys | Matching engine | PARTIAL_MATCH | Gold specifically ties matching to demandeur+agent; V2 has broader matching | None | Matching engine uses profiles not roles | Qualification drives match quality | Matching search filters | Matching algorithm uses profiles | CRM match tracking | None | Verify matching engine handles demandeur→agent proposal flow | PENDING_APPROVAL |
| XW-RL-044 | Visit scheduling journey | Journey | GOLD-RL-044 | Supported; visit scheduling available for all relevant roles | Journeys | Business flows | NORMALIZED_MATCH | Visit workflows are role-agnostic in V2 | None | None | Visit scheduling in qualification | N/A | Visit scheduling in matching | CRM visit tracking | None | Already covered | APPROVED |
| XW-RL-045 | Negotiation journey | Journey | GOLD-RL-045 | Partially supported; negotiation stage exists on Conversation | Journeys | schema.prisma (Conversation.negotiation_stage) | PARTIAL_MATCH | Gold defines role-specific negotiation; V2 has generic negotiation stage | None | Conversation negotiation_stage field exists but may need enrichment | Negotiation qualification data | N/A | Negotiation matching | CRM negotiation tracking | None | Extend negotiation workflow to be role-aware | PENDING_APPROVAL |
| XW-RL-046 | Transaction journey | Journey | GOLD-RL-046 | Partially supported; no transaction object in V2 | Journeys | (none) | PARTIAL_MATCH | Gold includes notaire in transaction journey; V2 has no transaction entity | New Transaction model may be needed | Transaction workflow missing | Transaction qualification | N/A | Transaction matching | CRM transaction tracking | Legal/financial | Consider Transaction model with role involvement | PENDING_APPROVAL |
| XW-RL-047 | Post-sale follow-up journey | Journey | GOLD-RL-047 | Limited support; no dedicated post-sale workflows | Journeys | (none) | PARTIAL_MATCH | Gold defines post-sale follow-up for agent+owner; V2 has no explicit post-sale flow | New workflows needed | Post-sale notifications/actions missing | Post-sale qualification | N/A | Post-sale matching | CRM post-sale tracking | None | Implement post-sale follow-up workflows | PENDING_APPROVAL |
| XW-RL-048 | Admin supervision journey | Journey | GOLD-RL-048 | Supported via admin role | Journeys | Business flows | NORMALIZED_MATCH | Admin role covers assistant, vice_master, master, admin supervision | None | Admin has full system access | Admin qualification oversight | Admin listing oversight | Admin match oversight | Admin CRM | Highest privilege | Already covered | APPROVED |

---

## 3. Permission Level Mapping

| Gold Level | Gold Name | V2 Equivalent | Mapping Status | Notes |
|------------|-----------|---------------|----------------|-------|
| Niveau 1 | Read | Implicit in all roles | PARTIAL_MATCH | V2 has no explicit permission model; read is implicit |
| Niveau 2 | Create | Implicit per role (operator+ can create listings) | PARTIAL_MATCH | Creation rights are hardcoded per feature, not modeled |
| Niveau 3 | Edit | Implicit scoped (own / managed / all) | PARTIAL_MATCH | Edit scope is not formally defined |
| Niveau 4 | Approve | Not implemented | EXTENSION_REQUIRED | Approval workflows are entirely absent from V2 |

**Resolution:** Implement a formal Permission model with the 4 levels. Map to official roles via a permission matrix.

---

## 4. Trust Level Mapping

| Gold Level | Gold Name | V2 Equivalent | Mapping Status | Notes |
|------------|-----------|---------------|----------------|-------|
| Niveau 1 | Nouveau compte | No equivalent | EXTENSION_REQUIRED | Add trust_level field to User model |
| Niveau 2 | Téléphone vérifié | phoneE164 exists but not verified | EXTENSION_REQUIRED | Add phone_verified flag |
| Niveau 3 | Identité vérifiée | No equivalent | EXTENSION_REQUIRED | Add identity_verified + document workflow |
| Niveau 4 | Documents pro validés | No equivalent | EXTENSION_REQUIRED | Add professional_docs_verified |
| Niveau 5 | Professionnel vérifié | No equivalent | EXTENSION_REQUIRED | Add professional_verified |
| Niveau 6 | Compte de référence | No equivalent | EXTENSION_REQUIRED | Add reference_account (admin-granted) |

**Resolution:** Add `trust_level` (INT 1-6) and individual Boolean verification flags to the User model. Implement verification workflows.

---

## 5. Badge Mapping

| Gold Badge | Requirement | V2 Equivalent | Mapping Status | Notes |
|------------|-------------|---------------|----------------|-------|
| Téléphone vérifié | OTP validated | No equivalent | EXTENSION_REQUIRED | Derive from phone_verified flag |
| E-mail vérifié | Email confirmed | No equivalent | EXTENSION_REQUIRED | Derive from email_verified flag |
| Identité vérifiée | CNI/passport validated | No equivalent | EXTENSION_REQUIRED | Derive from identity_verified |
| Propriétaire vérifié | Property docs verified | No equivalent | EXTENSION_REQUIRED | Derive from owner_verified |
| Agence vérifiée | Agency docs approved | No equivalent | EXTENSION_REQUIRED | Add agency_verified to Organization |
| Partenaire LAWIM | Partner validated | No equivalent | EXTENSION_REQUIRED | Derive from professional_verified |
| Professionnel vérifié | Pro status confirmed | No equivalent | EXTENSION_REQUIRED | Derive from professional_verified |
| Agent actif | Agent fully onboarded | No equivalent | EXTENSION_REQUIRED | Derive from agent onboarding state |

**Resolution:** Implement a badge system that derives from trust level flags and verification fields. Display badges on user profiles, agent profiles, and listings.

---

## 6. Partner Role Mapping

| Gold Partner | V2 Official Role | V2 Business Profile | Mapping Status | Notes |
|--------------|------------------|---------------------|----------------|-------|
| Notaire | partner | notary | EXACT_MATCH | Already aliased in USER_ROLE_ALIASES |
| Géomètre | partner | surveyor | NORMALIZED_MATCH | Direct profile match |
| Banque | partner | bank / financing | NORMALIZED_MATCH | Split by function (bank vs. financing) |
| Assurance | partner | insurer | NORMALIZED_MATCH | Direct profile match |
| Photographe | partner | photographer | EXACT_MATCH | Already aliased in USER_ROLE_ALIASES |
| Artisan | partner | {architect, engineer, technician, contractor, decorator, electrician, plumber, cleaner, mover} | ONE_TO_MANY | Granular artisan profiles in V2 |
| Expert partenaire | partner | {architect, engineer, surveyor, lawyer} | ONE_TO_MANY | Map to specific expertise profile |

**Resolution:** All Gold partner roles have V2 equivalents. V2 adds granularity that Gold did not have (especially for Artisan). No extensions required beyond profile assignment.

---

## 7. Gap Analysis / Extensions Required

### 7.1 Critical Gaps (Security / Operational Impact)

| Gap | Gold Reference | Impact | Effort | Priority |
|-----|----------------|--------|--------|----------|
| No trust level system | GOLD-RL-018 to GOLD-RL-023 | Security gates, fraud prevention, user confidence | High | P1 |
| No badge/verification display | GOLD-RL-024 to GOLD-RL-031 | User trust signaling, professional credibility | Medium | P2 |
| No approval permission level | GOLD-RL-017 | Listing validation, agency creation, professional verification | High | P1 |
| No agency hierarchy roles | GOLD-RL-010, GOLD-RL-032 to GOLD-RL-034 | Agency management, responsible/admin/assistant distinction | Medium | P2 |

### 7.2 Medium Gaps (Functional Impact)

| Gap | Gold Reference | Impact | Effort | Priority |
|-----|----------------|--------|--------|----------|
| No explicit permission model | GOLD-RL-014 to GOLD-RL-016 | Fine-grained access control | Medium | P2 |
| No agent onboarding workflow | GOLD-RL-035 | Agent activation and readiness | Medium | P2 |
| No agent rating system | GOLD-RL-040 | Quality signals, matching quality | Medium | P2 |
| No geographic lead routing | GOLD-RL-037 | Lead distribution efficiency | Medium | P3 |

### 7.3 Low Gaps (Enhancement)

| Gap | Gold Reference | Impact | Effort | Priority |
|-----|----------------|--------|--------|----------|
| No minimum agent enforcement | GOLD-RL-036 | Agency quality control | Low | P3 |
| No lead costing / credits | GOLD-RL-038, GOLD-RL-039 | Monetization, agent engagement | High | P3 |
| No transaction entity | GOLD-RL-046 | End-to-end transaction tracking | Medium | P3 |
| No post-sale workflows | GOLD-RL-047 | Customer retention, follow-up | Low | P3 |

### 7.4 Summary by Domain

| Domain | Total Concepts | Mapped | Gap (EXTENSION_REQUIRED) | Gap (PARTIAL_MATCH) | Completion |
|--------|---------------|--------|--------------------------|---------------------|------------|
| Role Families | 6 | 6 | 0 | 2 | 100% conceptual, 67% match quality |
| Role Hierarchy | 7 | 7 | 1 | 3 | 100% conceptual, 43% match quality |
| Permission Levels | 4 | 4 | 1 | 3 | 100% conceptual, 0% exact |
| Trust Levels | 6 | 6 | 6 | 0 | 100% conceptual, 0% exact |
| Badges | 8 | 8 | 8 | 0 | 100% conceptual, 0% exact |
| Agency Structure | 9 | 9 | 6 | 3 | 100% conceptual, 11% match quality |
| Partner Roles | 7 | 7 | 0 | 0 | 100% conceptual, 100% match quality |
| Role-to-Journey | 8 | 8 | 0 | 4 | 100% conceptual, 50% match quality |
| **Total** | **55** | **55** | **22** | **15** | **100% coverage, 40% exact/normalized** |

---

## 8. Extensions Required — Prioritized Action Plan

| Priority | Extension | Gold IDs | Proposed Implementation |
|----------|-----------|----------|------------------------|
| P1 | Trust Level system on User model | GOLD-RL-018 to GOLD-RL-023 | Add `trust_level` INT field + individual verification Boolean fields (`phone_verified`, `identity_verified`, `professional_docs_verified`, `professional_verified`, `reference_account`) |
| P1 | Approval permission level and workflow | GOLD-RL-017 | Implement `ApprovalWorkflow` model with `approver_role`, `target_type`, `target_id`, `status`, `reviewed_by`, `reviewed_at` |
| P2 | Badge system | GOLD-RL-024 to GOLD-RL-031 | Add `Badge` model or derive badges from verification fields; implement badge display API |
| P2 | Agency hierarchy roles | GOLD-RL-010, GOLD-RL-032 to GOLD-RL-034 | Add `agency_role` field (`responsible`, `admin`, `agent`, `assistant`) to User model scoped by organization_id |
| P2 | Agency registration fields | GOLD-RL-034 | Add `rccm`, `tax_id`, `cni_document` fields to Organization model |
| P2 | Formal permission model | GOLD-RL-014 to GOLD-RL-016 | Create `RolePermission` model or permission matrix; map 4 levels to official roles |
| P2 | Agent onboarding workflow | GOLD-RL-035 | Add `onboarding_status` field to User; implement state machine (invited → phone_verified → identity_verified → validated → active) |
| P2 | Agent rating system | GOLD-RL-040 | Add `agent_rating` FLOAT field; implement post-interaction rating update |
| P3 | Geographic lead routing | GOLD-RL-037 | Add `agent_zones` table (agent_id, zone); implement routing engine |
| P3 | Lead costing and credits | GOLD-RL-038, GOLD-RL-039 | Add `agent_credits` table (agent_id, credits, total_spent, last_recharge) and `boost_purchases` table |
| P3 | Transaction model | GOLD-RL-046 | Create `Transaction` model with roles (demandeur, agent, owner, notaire) and status workflow |
| P3 | Post-sale workflows | GOLD-RL-047 | Add post-sale stages to Project or Conversation models |

---

*Crosswalk generated 2026-07-15 — Certified Gold reference: ROLE_MODEL.md — 55 concepts mapped, 22 extensions identified.*
