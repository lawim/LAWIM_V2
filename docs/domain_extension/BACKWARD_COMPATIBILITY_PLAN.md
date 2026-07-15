# BACKWARD COMPATIBILITY PLAN — Extensions Impact on Existing LAWIM_V2 Systems

**Document ID:** LAWIM-BC-EXT-PLAN-V1
**Status:** CANONICAL
**Date:** 2026-07-15
**Scope:** Impact analysis of all domain extensions on currently deployed systems

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Impact by Area](#2-impact-by-area)
   2.1 [API v3](#21-api-v3)
   2.2 [Conversation V2](#22-conversation-v2)
   2.3 [Search Actuel](#23-search-actuel)
   2.4 [Matching Actuel](#24-matching-actuel)
   2.5 [CRM Actuel](#25-crm-actuel)
   2.6 [Relationship Actuel](#26-relationship-actuel)
   2.7 [Frontend](#27-frontend)
   2.8 [SDK](#28-sdk)
   2.9 [Webhooks](#29-webhooks)
   2.10 [Tests](#210-tests)
   2.11 [Données Existantes](#211-donnees-existantes)
3. [State Mapping: V2 States → Unified States](#3-state-mapping-v2-states--unified-states)
4. [Role Mapping: Gold Levels → V2 Roles](#4-role-mapping-gold-levels--v2-roles)
5. [Property Type Migration Strategy](#5-property-type-migration-strategy)
6. [API Compatibility Guarantees](#6-api-compatibility-guarantees)
7. [Feature Flag Strategy](#7-feature-flag-strategy)
8. [Data Migration Sequencing](#8-data-migration-sequencing)
9. [Testing Impacts](#9-testing-impacts)
10. [Rollback Procedures](#10-rollback-procedures)

---

## 1. Executive Summary

The domain extensions introduce 22 new database tables, ~48 new relations, 5 enriched existing tables, and ~60 new API endpoints. This document analyzes the backward compatibility impact on all existing LAWIM_V2 systems.

| Area | Breaking Changes | Mitigation Complexity | Migration Effort |
|------|-----------------|----------------------|------------------|
| API v3 | MEDIUM | HIGH | 4-6 weeks |
| Conversation V2 | LOW | LOW | 1-2 weeks |
| Search Actuel | HIGH | HIGH | 4-8 weeks |
| Matching Actuel | FULL REPLACEMENT | CRITICAL | 8-12 weeks |
| CRM Actuel | FULL REPLACEMENT | CRITICAL | 6-10 weeks |
| Relationship Actuel | MEDIUM | MEDIUM | 2-4 weeks |
| Frontend | HIGH | HIGH | 6-10 weeks |
| SDK | MEDIUM | MEDIUM | 2-4 weeks |
| Webhooks | MEDIUM | MEDIUM | 2-3 weeks |
| Tests | HIGH | HIGH | 4-6 weeks |
| Données Existantes | MEDIUM | HIGH | 3-5 weeks |

**Total estimated migration effort:** 8-14 weeks parallel track with feature-flag gating.

---

## 2. Impact by Area

### 2.1 API v3

| Aspect | Detail |
|--------|--------|
| **Current State** | REST API v3 with endpoints for User, Property, Project, Conversation, Organization, Media, Notification, Event CRUD. JSON over HTTP. Token-based auth. ~25 endpoints. |
| **Impact of Extensions** | ~60 new endpoints added. Existing endpoints get enriched response schemas (new fields on User, Property, Project, Organization). Enum values expand. |
| **Breaking Changes** | - `GET /properties` response includes new fields (`property_family`, `boost_level`, `is_premium`, `verification_status`) — clients ignoring unknown fields are safe; strict-deserialization clients break.<br>- `POST /projects` accepts new `business_role`, `urgency_level`, `journey_stage` fields — optional, no breakage.<br>- `POST /properties` now accepts new optional fields — no breakage.<br>- `GET /users/me` returns new trust/badge fields — no breakage for tolerant clients.<br>- `Property.status` enum adds `pending_validation`, `suspended`, `maintenance` — clients with enum validation break.<br>- `Project.project_type` adds `short_stay`, `lease`, `bail_commercial` — same risk.<br>- `User.role` unchanged (no breaking change). |
| **Mitigation Strategy** | 1. Adopt JSON:API sparse fieldsets: `?fields[properties]=title,price` — clients opt into new fields.<br>2. Version header `Accept: application/vnd.lawim.v3+json` continues to return v3 schema (without new fields).<br>3. New endpoints behind `/v4/` prefix with deprecation of v3 after 6-month overlap.<br>4. Enum additions are additive-only; no values removed.<br>5. Response schema registry with `X-Schema-Version` header. |
| **Migration Steps** | 1. Add feature-flag gating on new response fields (off by default).<br>2. Deploy new endpoints under `/v4/` alongside existing v3.<br>3. Update API gateway to support version negotiation.<br>4. Migrate internal consumers to v4.<br>5. Announce v3 deprecation with 6-month timeline.<br>6. Monitor v3 usage; deprecate when traffic < 5% of total. |
| **Rollback Plan** | Feature flag off → v3 responses revert to original schema. Remove v4 routes if needed. |

---

### 2.2 Conversation V2

| Aspect | Detail |
|--------|--------|
| **Current State** | Conversation model with messages, linked to Property, User, Organization. Status: active/pending/closed/archived. Negotiation stages: inquiry/visit/offer/negotiation/closing/completed. |
| **Impact of Extensions** | - Conversation gets optional `match_id` and `transaction_id` FK fields.<br>- New `conversation_type` field: inquiry, negotiation, support, mediation.<br>- New `negotiation_stage` values: mediation, incident, follow_up.<br>- Conversations can now originate from Match or Transaction rather than just Property. |
| **Breaking Changes** | - None to existing conversation flow (all new fields are optional).<br>- Existing conversations auto-backfilled with `conversation_type = 'inquiry'`.<br>- No existing endpoint changes. |
| **Mitigation Strategy** | Additive only. All new fields are nullable with sensible defaults. |
| **Migration Steps** | 1. Add new columns (nullable).<br>2. Backfill existing conversations.<br>3. Deploy new linking logic in conversation creation.<br>4. Enable match/transaction linking via feature flag. |
| **Rollback Plan** | Remove new columns, revert linking logic. |

---

### 2.3 Search Actuel

| Aspect | Detail |
|--------|--------|
| **Current State** | Basic property search by `searchKey`, city, status, price range. No geographic hierarchy, no full-text search, no faceted search. Limited to `Property` model fields. |
| **Impact of Extensions** | - `GeographicUnit` enables hierarchical location search (country → region → city → neighborhood → zone).<br>- Full-text search on title, summary (gin/tsvector).<br>- Property type reference table enables type-based faceting.<br>- New `data_quality_score`, `property_family` enable quality-filtered search. |
| **Breaking Changes** | - `GET /properties/search` response format changes if we add new filters — additive only if backward-compatible params kept.<br>- Existing `?city=` filter remains but new `?geo_unit_id=` replaces it for geographic search.<br>- `?searchKey=` deprecated in favor of full-text `?q=`. |
| **Mitigation Strategy** | 1. Keep legacy `?city=` and `?searchKey=` params but internally map to new geo/full-text system.<br>2. New `?q=` param for full-text search (coexists with legacy).<br>3. Deprecate legacy params with warning header `Warning: 299 - "searchKey deprecated, use q"`. |
| **Migration Steps** | 1. Build new search index (gin on title, summary).<br>2. Seed GeographicUnit table from existing city/region data.<br>3. Add `?q=` full-text param.<br>4. Map legacy params internally.<br>5. Monitor legacy param usage.<br>6. Remove legacy params after 6-month deprecation. |
| **Rollback Plan** | Remove new search indexes; revert to simple SQL WHERE; keep legacy params. |

---

### 2.4 Matching Actuel

| Aspect | Detail |
|--------|--------|
| **Current State** | No algorithmic matching. Simple property-to-user association via conversation creation. No scoring, no compatibility levels, no match persistence. |
| **Impact of Extensions** | **Full replacement.** New Match entity, scoring engine (6 dimensions, 10+ boost/penalty rules), compatibility levels, rematching engine, continuous surveillance. Current "matching" (conversation linking) becomes deprecated. |
| **Breaking Changes** | - Existing conversation-based "matching" becomes legacy. New matching engine runs in parallel.<br>- No existing API endpoints removed, but new `GET /matches` supersedes manual search for agent workflows.<br>- `Project.matching_status` replaces manual matching tracking. |
| **Mitigation Strategy** | 1. Run old and new matching in parallel for 3 months.<br>2. Old matching remains available as "manual assignment."<br>3. Feature flag: `matching_engine_v2` — off by default during development.<br>4. Gradual rollout: internal agents first, then beta users, then GA. |
| **Migration Steps** | 1. Implement Match entity and scoring engine behind feature flag.<br>2. Port existing conversation-based matching data to new Match records.<br>3. Train agents on new matching interface.<br>4. Enable for beta testers.<br>5. Monitor matching quality metrics.<br>6. GA after 3-month validation.<br>7. Deprecate old manual matching. |
| **Rollback Plan** | Feature flag off → system reverts to conversation-based linking. Match table data preserved (not deleted) for later re-enablement. |

---

### 2.5 CRM Actuel

| Aspect | Detail |
|--------|--------|
| **Current State** | No formal CRM pipeline. Leads tracked implicitly via Conversation creation. No scoring, no classification, no routing. Agent assignment manual. |
| **Impact of Extensions** | **Full replacement.** New Lead entity with 8-stage pipeline, scoring engine (base + 13 boosters - 8 penalties), 5-class classification (hot/warm/cold/low/spam), routing engine, SLA monitoring, anti-fraud. |
| **Breaking Changes** | - Existing conversations are retroactively classified as leads (backfill).<br>- `GET /conversations` still works but `GET /leads` becomes the primary CRM view.<br>- Agent dashboard shifts from conversation-list to lead-pipeline view. |
| **Mitigation Strategy** | 1. Lead engine runs in shadow mode for 1 month (scores generated but not used for routing).<br>2. Backfill leads from existing conversations with audit trail.<br>3. Feature flag: `crm_pipeline_v2` — off by default.<br>4. Gradual rollout: scoring visible → classification visible → auto-routing enabled. |
| **Migration Steps** | 1. Implement Lead model and scoring engine behind feature flag.<br>2. Run shadow scoring for 30 days; validate against manual assessments.<br>3. Backfill historical leads from conversations (estimated 10k-50k records).<br>4. Enable scoring visibility for agents.<br>5. Enable auto-classification.<br>6. Enable auto-routing after 60 days validation.<br>7. Deprecate conversation-as-lead pattern. |
| **Rollback Plan** | Feature flag off → lead table becomes read-only. Conversations remain primary CRM. Routing reverts to manual. |

---

### 2.6 Relationship Actuel

| Aspect | Detail |
|--------|--------|
| **Current State** | No formal Relationship model. Relationships implicit via conversation participants. No double-consent enforcement. No relationship lifecycle. |
| **Impact of Extensions** | New Contact model with 6-state double-consent lifecycle. New Relationship model for tracking active links. Consent tracking model for data-sharing permissions. |
| **Breaking Changes** | - Existing conversations between demandeur and holder implicitly create Contact records via backfill.<br>- New double-consent requirement means new contacts require explicit opt-in.<br>- Old conversations remain accessible but new contact creation requires consent flow. |
| **Mitigation Strategy** | 1. Backfill existing conversation pairs as "auto-consented" legacy contacts.<br>2. Feature flag: `double_consent_enforcement` — off by default; existing flow unchanged.<br>3. New consent flow introduced as optional first, then mandatory after 3 months. |
| **Migration Steps** | 1. Create Contact and Relationship tables.<br>2. Backfill from existing conversations (user A + user B + property = contact).<br>3. Mark legacy contacts as `established` with `consent_*` auto-set.<br>4. Introduce consent UI as optional (feature flag on).<br>5. After 3 months, make consent mandatory for new contacts.<br>6. Audit all existing relationships for GDPR compliance. |
| **Rollback Plan** | Feature flag off → consent flow disabled. Contact table preserved but not enforced. |

---

### 2.7 Frontend

| Aspect | Detail |
|--------|--------|
| **Current State** | Next.js dashboard with property listings, conversation UI, project management, basic user admin. |
| **Impact of Extensions** | 10+ new pages/views: Intent Dashboard, Matching UI (score breakdown), Visit Scheduler, Transaction Tracker, Service Catalog, Lead Pipeline Kanban, Document Manager, Approval Queue, Incident Reporter, Mediation Workspace, Agent Onboarding Wizard, Professional Profile Editor, Geography Manager. |
| **Breaking Changes** | - Property edit form gains 8+ new fields (family, boost, premium, verification, price types).<br>- Project form gains business_role, urgency, journey_stage fields.<br>- User profile gains trust/badge section.<br>- Navigation: new sidebar sections for CRM, Matching, Services, Finance. |
| **Mitigation Strategy** | 1. Feature-flag every new page and field (off by default).<br>2. Progressive enhancement: new fields shown as optional sections.<br>3. Separate routes for new features (`/crm/`, `/matching/`, `/services/`).<br>4. Old navigation unchanged; new items added at bottom. |
| **Migration Steps** | 1. Add new fields to existing forms (behind feature flags).<br>2. Build new pages behind separate routes.<br>3. Update navigation with new section (behind feature flag).<br>4. Internal beta → agent beta → public beta → GA.<br>5. Remove old feature-flag gating after full rollout. |
| **Rollback Plan** | Feature flags off → old UI restored. New routes return 404. New fields hidden. |

---

### 2.8 SDK

| Aspect | Detail |
|--------|--------|
| **Current State** | JavaScript/TypeScript SDK covering v3 API endpoints. Python SDK in progress. |
| **Impact of Extensions** | ~60 new methods across 21 resource groups. TypeScript types need extension for new fields on existing responses. |
| **Breaking Changes** | - TypeScript types auto-generated from OpenAPI spec: new optional fields on User, Property, Project, Organization types (non-breaking for tolerant code).<br>- Strict type checks on enum values may fail with new enum additions (`Property.status`, `Project.projectType`). |
| **Mitigation Strategy** | 1. Generate SDK types from OpenAPI v4 spec.<br>2. Keep v3 SDK published separately for legacy support.<br>3. Enum types use `string` union with `| string` fallback for forward compatibility.<br>4. Versioned SDK packages: `@lawim/sdk-v3` and `@lawim/sdk-v4`. |
| **Migration Steps** | 1. Generate v4 SDK types from new OpenAPI spec.<br>2. Publish v4 SDK as `@lawim/sdk-v4` (alpha → beta → stable).<br>3. Update internal consumers to use v4 SDK.<br>4. Deprecate v3 SDK with 6-month migration window. |
| **Rollback Plan** | Revert to v3 SDK package. Keep v4 SDK available but not default. |

---

### 2.9 Webhooks

| Aspect | Detail |
|--------|--------|
| **Current State** | Outgoing webhooks for: `conversation.created`, `conversation.updated`, `property.created`, `property.updated`, `user.created`. Configurable per organization. |
| **Impact of Extensions** | 15+ new webhook event types (see API_EXTENSION_CONTRACTS.md Appendix A). Payload schemas for new entities. Extended payloads for existing events (new fields on property, user, project). |
| **Breaking Changes** | - Existing webhook payloads gain new optional fields (non-breaking for tolerant consumers).<br>- Enum values in payloads may be unknown to old consumers (`property.status` adds `pending_validation`).<br>- New webhook types are opt-in (no existing subscription breaks). |
| **Mitigation Strategy** | 1. New fields in existing webhooks are additive only; never remove or rename existing fields.<br>2. New webhook types require explicit subscription (no auto-enable).<br>3. Webhook schema version in payload header `X-Lawim-Schema-Version`. |
| **Migration Steps** | 1. Update webhook payload schemas with new fields.<br>2. Register new event types in webhook configuration UI.<br>3. Notify existing webhook subscribers of schema changes.<br>4. Allow subscribers to filter by new event types. |
| **Rollback Plan** | Disable new webhook event types. Keep old webhook payloads unchanged. |

---

### 2.10 Tests

| Aspect | Detail |
|--------|--------|
| **Current State** | ~500 tests: unit tests (pytest), integration tests (API), E2E tests (Playwright). Coverage: ~40% of codebase. |
| **Impact of Extensions** | Estimated 800+ new tests: 22 new entity unit tests, ~60 endpoint integration tests, state machine tests for 14 workflow lifecycles, scoring engine tests for matching + CRM, data migration tests, backward compatibility regression tests. |
| **Breaking Changes** | - Existing tests that assert on `Property.status` enum values may fail with new values.<br>- Existing fixtures need updates for new required fields on enriched models.<br>- Existing mock responses need new optional fields. |
| **Mitigation Strategy** | 1. All existing tests must pass before extension deployment (zero regression).<br>2. New tests use factory patterns that accept new fields as optional.<br>3. Enum assertions use `in` operator instead of `==` for future-proofing.<br>4. Backward compatibility test suite runs v3 contract tests against extended API. |
| **Migration Steps** | 1. Add new optional fields to test factories/fixtures.<br>2. Update enum assertions to be forward-compatible (`status in VALID_STATUSES`).<br>3. Write new unit tests per entity (22 entities × avg 15 tests = ~330).<br>4. Write integration tests per endpoint (~60 × avg 5 tests = ~300).<br>5. Write state machine tests (14 × avg 10 tests = ~140).<br>6. Write scoring engine tests (~100).<br>7. Run full regression suite before each deployment. |
| **Rollback Plan** | Revert test assertions to pre-extension state (git revert). |

---

### 2.11 Données Existantes

| Aspect | Detail |
|--------|--------|
| **Current State** | Production database with ~500 users, ~2000 properties, ~5000 conversations, ~1000 projects, ~10000 events, ~500 organizations. |
| **Impact of Extensions** | 22 new tables created (empty initially). 5 existing tables enriched with new columns (nullable). Data backfill required for: trust levels, property family mapping, lead backfill from conversations, contact backfill from conversation pairs. |
| **Breaking Changes** | - Existing data integrity unchanged (all new columns nullable).<br>- `Property.property_type` values remain as strings until phase 2 FK migration.<br>- `Property.status` values remain valid; new values only appear for new records. |
| **Mitigation Strategy** | 1. All new columns nullable with sensible defaults.<br>2. Backfill scripts are batch-based and reversible.<br>3. Data migration runs in maintenance window with full backup.<br>4. No existing data is deleted or modified beyond adding new columns. |
| **Migration Steps** | See §8 Data Migration Sequencing for detailed timeline. |
| **Rollback Plan** | See §10 Rollback Procedures. |

---

## 3. State Mapping: V2 States → Unified States

### 3.1 Property Status

| V2 Current State | Unified State | Notes |
|-----------------|--------------|-------|
| `draft` | `draft` | Unchanged |
| `published` | `published` | Unchanged |
| `sold` | `sold` | Unchanged |
| `rented` | `rented` | Unchanged |
| `archived` | `archived` | Unchanged |
| *(new)* | `pending_validation` | New state added |
| *(new)* | `suspended` | New state added (fraud/admin hold) |
| *(new)* | `maintenance` | New state added |

### 3.2 Project Status

| V2 Current State | Unified State | Notes |
|-----------------|--------------|-------|
| `draft` | `draft` | Unchanged |
| `active` | `active` (maps to `qualifying`) | Transitional |
| `paused` | `paused` | Unchanged |
| `completed` | `completed` | Unchanged |
| `archived` | `archived` | Unchanged |
| `cancelled` | `cancelled` | Unchanged |
| *(new)* | `qualifying` | Split from `active` |
| *(new)* | `matching` | New journey state |
| *(new)* | `negotiating` | New journey state |

### 3.3 Conversation Status

| V2 Current State | Unified State | Notes |
|-----------------|--------------|-------|
| `active` | `active` | Unchanged |
| `pending` | `pending` | Unchanged |
| `closed` | `closed` | Unchanged |
| `archived` | `archived` | Unchanged |
| *(new)* | `negotiating` | New sub-status |
| *(new)* | `mediated` | New sub-status |
| *(new)* | `escalated` | New sub-status |

### 3.4 Negotiation Stage (Conversation)

| V2 Current Stage | Unified Stage | Notes |
|-----------------|--------------|-------|
| `inquiry` | `inquiry` | Unchanged |
| `visit` | `visit` | Unchanged |
| `offer` | `offer` | Unchanged |
| `negotiation` | `negotiation` | Unchanged |
| `closing` | `closing` | Unchanged |
| `completed` | `completed` | Unchanged |
| *(new)* | `mediation` | New |
| *(new)* | `incident` | New |
| *(new)* | `follow_up` | New |

### 3.5 Property Availability

| V2 Current | Unified | Notes |
|-----------|---------|-------|
| `available` | `available` | Unchanged |
| `pending` | `pending` | Unchanged |
| `sold` | `sold` | Unchanged |
| `rented` | `rented` | Unchanged |
| `archived` | `archived` | Unchanged |
| *(new)* | `reserved` | New |
| *(new)* | `under_negotiation` | New |

---

## 4. Role Mapping: Gold Levels → V2 Roles

### 4.1 Gold Role Hierarchy → V2 official_role + Extensions

| Gold Level | Gold Role | V2 official_role | New agency_role | New trust_level Requirements |
|------------|-----------|-----------------|-----------------|------------------------------|
| Level 1 | demandeur | `user` | — | 1 (New account) |
| Level 2 | vendeur/propriétaire | `user` | — | 2 (Phone verified) |
| Level 3 | agent | `operator` | `agent` | 3 (Identity verified) |
| Level 4 | agence | N/A (Organization) | N/A | Organization-level trust |
| Level 5 | assistant | `operator` | `assistant` | 2+ (Phone verified) |
| Level 6 | vice_master | `manager` | — | 4+ (Pro docs validated) |
| Level 7 | master | `admin` | — | 5+ (Professional verified) |

### 4.2 Gold Business Profiles → V2 business_role

| Gold Profile | V2 business_role | Matching Role | Lead Type (CRM) |
|-------------|-----------------|---------------|-----------------|
| demandeur (buyer) | `buyer` | `demandeur` | `buyer` |
| demandeur (tenant) | `tenant` | `demandeur` | `tenant` |
| propriétaire (seller) | `seller` | `holder` | `seller` |
| investisseur | `investor` | `investor` | `investor` |
| investisseur diaspora | `investor` | `diaspora` | `diaspora_investor` |
| agent immobilier | `client` (when buying) / `agent` (when selling) | `agent` | — |
| professionnel (notaire, etc.) | `client` | `professional` | — |

### 4.3 Gold Permission Levels → V2 Permissions

| Gold Permission | V2 Implementation | Extension |
|----------------|-------------------|-----------|
| Niveau 1 — Lecture (Read) | Implicit via role | EXT-PERM-002 |
| Niveau 2 — Création (Create) | Implicit via role | EXT-PERM-003 |
| Niveau 3 — Modification (Edit) | Implicit via role (own/managed/all) | EXT-PERM-004 |
| Niveau 4 — Validation (Approve) | New ApprovalWorkflow model | EXT-PERM-001 |

---

## 5. Property Type Migration Strategy

### 5.1 Current State

`Property.property_type` is a free-form string field. Current values observed in production:

```
appartment, apartment, appartement, house, maison, villa, duplex, studio,
land, terrain, commercial, office, bureau, shop, boutique, warehouse,
industrial, factory, building, immeuble, guest_house, hotel, farm,
plantation, construction, renovation, project, other
```

### 5.2 Target State

`Property.property_type_id` → FK to `PropertyType` reference table with hierarchical structure:

```
residential
├── apartment (appartement)
├── villa
├── house (maison)
├── studio
├── duplex
└── compound
commercial
├── office (bureau)
├── shop (boutique, magasin)
├── warehouse (entrepôt)
└── retail
industrial
├── factory (usine)
└── warehouse (entrepôt industriel)
land (terrain)
├── residential (constructible)
├── agricultural (agricole)
└── commercial (commercial)
agricultural
├── farm (ferme)
└── plantation
hotel
├── hotel
└── guest_house (chambre d'hôte)
project
├── construction
└── renovation
```

### 5.3 Migration Phases

| Phase | Action | Timeline | Risk |
|-------|--------|----------|------|
| **Phase 1: Normalize** | Clean existing `property_type` values: lowercase, trim, map synonyms (appartment→apartment, maison→house). Audit unmappable values. | Week 1-2 | LOW |
| **Phase 2: Seed** | Create `PropertyType` table with all 19+ types and hierarchy. Seed from canonical list. | Week 2 | LOW |
| **Phase 3: Dual-write** | Add `property_type_id` FK (nullable). On create/update, write BOTH `property_type` (string) and `property_type_id` (FK). | Week 3 | LOW |
| **Phase 4: Backfill** | Batch update all existing properties to set `property_type_id` from mapped string values. | Week 4 | MEDIUM |
| **Phase 5: Enforce** | Make `property_type_id` NOT NULL. Deprecate `property_type` string field. | Week 6 | HIGH |
| **Phase 6: Remove** | Drop `property_type` string column after 6-month deprecation. | Month 9 | HIGH |

### 5.4 Synonym Mapping Table

A configuration-driven synonym map will be used for the backfill:

```json
{
  "appartment": "residential.apartment",
  "apartment": "residential.apartment",
  "appartement": "residential.apartment",
  "house": "residential.house",
  "maison": "residential.house",
  "villa": "residential.villa",
  "duplex": "residential.duplex",
  "studio": "residential.studio",
  "land": "land.residential",
  "terrain": "land.residential",
  "commercial": "commercial.office",
  "office": "commercial.office",
  "bureau": "commercial.office",
  "shop": "commercial.shop",
  "boutique": "commercial.shop",
  "warehouse": "commercial.warehouse",
  "industrial": "industrial.factory",
  "factory": "industrial.factory",
  "usine": "industrial.factory",
  "building": "residential.apartment",
  "immeuble": "residential.apartment",
  "guest_house": "hotel.guest_house",
  "hotel": "hotel.hotel",
  "farm": "agricultural.farm",
  "ferme": "agricultural.farm",
  "plantation": "agricultural.plantation",
  "construction": "project.construction",
  "renovation": "project.renovation",
  "project": "project.construction"
}
```

Properties with unmappable `property_type` values (estimated < 2%) will be flagged for manual review and defaulted to `other.unknown`.

---

## 6. API Compatibility Guarantees

### 6.1 Compatibility Contract

LAWIM_V2 API v3 guarantees the following compatibility for the duration of the extension rollout:

1. **No existing field renamed or removed** — all current response fields remain unchanged
2. **No existing endpoint path changed** — all current URLs continue to work
3. **No existing enum value removed** — new values are additive only
4. **New fields are optional in requests** — adding new fields to requests is always optional
5. **New fields are appended to responses** — new fields appear at end of response objects; clients ignoring unknown fields are safe
6. **New endpoints are under new paths** — `/v4/` prefix for new resources; existing `/v3/` paths unchanged
7. **Error codes unchanged** — existing HTTP status codes and error shapes preserved
8. **Authentication unchanged** — existing token format and validation remain the same

### 6.2 Compatibility Modes

| Mode | Behavior | When Used |
|------|----------|-----------|
| **Strict v3** | No new fields in responses; new endpoints return 404; enum values unchanged | Legacy client compat |
| **Extended v3** | New optional fields in responses; existing params unchanged | Default for v3 Accept header |
| **v4** | Full new schema; new endpoints; extended enums | Accept: application/vnd.lawim.v4+json |

### 6.3 Version Negotiation

```
Client Request:
  GET /properties/7
  Accept: application/vnd.lawim.v3+json  → Extended v3 response (new fields optional)
  Accept: application/vnd.lawim.v3.strict+json  → Strict v3 response (no new fields)
  Accept: application/vnd.lawim.v4+json  → Full v4 response

Server Response:
  Content-Type: application/vnd.lawim.v3+json
  X-API-Version: 3.2.0
  Warning: 299 - "This API version will be deprecated on 2027-01-15"
```

### 6.4 Deprecation Timeline

| Milestone | Date (relative) | Action |
|-----------|-----------------|--------|
| v4 Alpha | Month 0 | Internal only; breaking changes allowed |
| v4 Beta | Month 3 | Beta testers; schema frozen |
| v4 GA | Month 6 | Production ready |
| v3 Soft deprecation | Month 6 | Warning headers added to v3 responses |
| v3 Hard deprecation | Month 12 | v3 returns 406 Not Acceptable |
| v3 Sunset | Month 18 | v3 endpoints removed |

---

## 7. Feature Flag Strategy

### 7.1 Flag Architecture

Feature flags are managed via a centralized feature toggle service with:

- **Scope**: global, organization, user, A/B test
- **Persistence**: database-backed with local cache (TTL 60s)
- **Audit**: all flag changes logged
- **Default**: ALL extension flags default to OFF

### 7.2 Extension Feature Flags

| Flag | Scope | Default | Dependencies | Description |
|------|-------|---------|--------------|-------------|
| `ext_property_family` | Global | OFF | — | Property family field & validation |
| `ext_property_boost` | Global | OFF | `ext_property_family` | Boost/premium listing fields |
| `ext_property_verification` | Org | OFF | — | Property verification workflow |
| `ext_property_pricing` | Global | OFF | — | Extended price fields (negotiable, historical) |
| `ext_property_quality_score` | Global | OFF | — | Data quality scoring engine |
| `ext_user_trust_levels` | Global | OFF | — | Trust level system & badges |
| `ext_user_onboarding` | Org | OFF | `ext_user_trust_levels` | Agent onboarding flow |
| `ext_organization_verification` | Org | OFF | — | Agency verification fields |
| `ext_intent_detection` | Global | OFF | — | NLP intent detection pipeline |
| `ext_matching_engine` | Org | OFF | `ext_intent_detection` | Full matching engine (Match entity) |
| `ext_visit_scheduling` | Org | OFF | `ext_matching_engine` | Visit entity & scheduling |
| `ext_transactions` | Org | OFF | `ext_matching_engine` | Transaction entity & lifecycle |
| `ext_crm_pipeline` | Org | OFF | — | Lead model & scoring pipeline |
| `ext_lead_purchases` | Org | OFF | `ext_crm_pipeline` | Lead purchase system |
| `ext_agent_credits` | Org | OFF | `ext_lead_purchases` | Agent credit balance |
| `ext_service_catalog` | Global | OFF | — | Service catalog & service orders |
| `ext_payments` | Global | OFF | `ext_service_catalog` | Payment processing (Campay) |
| `ext_documents` | Global | OFF | — | Document management & validation |
| `ext_approval_workflows` | Global | OFF | — | Approval workflow engine |
| `ext_incidents` | Org | OFF | — | Incident reporting & management |
| `ext_mediations` | Org | OFF | `ext_incidents` | Mediation workflow |
| `ext_agent_invitations` | Org | OFF | — | Structured agent invitation flow |
| `ext_identity_resolution` | Global | OFF | — | Duplicate user detection |
| `ext_professional_profiles` | Global | OFF | — | Professional service provider profiles |
| `ext_financing_requests` | Global | OFF | — | Financing request management |
| `ext_geography` | Global | OFF | — | Geographic unit reference data |
| `ext_relationships` | Global | OFF | — | Formal relationship management |
| `ext_consent_tracking` | Global | OFF | `ext_relationships` | User consent management |
| `ext_double_consent` | Org | OFF | `ext_relationships` | Mandatory double consent for contacts |
| `ext_sla_monitoring` | Org | OFF | `ext_crm_pipeline` | SLA breach detection & escalation |
| `ext_nba_engine` | Org | OFF | `ext_matching_engine` | Next Best Action recommendations |

### 7.3 Flag Lifecycle

| Stage | Action | Criteria |
|-------|--------|----------|
| **Development** | Flag added, default OFF | Code merged behind flag |
| **Alpha** | Enabled for internal team | Unit + integration tests pass |
| **Beta** | Enabled for org-level opt-in | E2E tests pass, perf benchmark met |
| **GA** | Enabled for all orgs by default | 30-day beta validation, no P1 bugs |
| **Permanent** | Flag removed, behavior permanent | > 90 days GA, no rollback requests |

### 7.4 Flag Dependency Graph

```
ext_consent_tracking
  └── ext_relationships
        └── ext_double_consent

ext_matching_engine
  ├── ext_visit_scheduling
  ├── ext_transactions
  └── ext_nba_engine

ext_crm_pipeline
  └── ext_lead_purchases
        └── ext_agent_credits

ext_service_catalog
  └── ext_payments

ext_incidents
  └── ext_mediations

ext_user_trust_levels
  └── ext_user_onboarding
```

---

## 8. Data Migration Sequencing

### 8.1 Migration Waves

| Wave | Migrations | Tables Affected | Estimated Rows | Downtime | Rollback Risk |
|------|-----------|----------------|---------------|----------|---------------|
| **Wave 0: Schema** | M1-M3 (add columns), M4 (reference tables) | User, Property, Project, Organization, Event, PropertyType, ProfessionalCategory, ServiceCategory, GeoLevel | ~10k updates | Minutes | LOW |
| **Wave 1: Geography** | Seed GeographicUnit | GeographicUnit | ~500 countries/regions/cities | None | LOW |
| **Wave 2: Service Catalog** | Seed Service table | Service | ~60 services | None | LOW |
| **Wave 3: Backfill Enrichments** | Trust levels, property family mapping | User, Property | ~2.5k updates | 5-10 min | LOW |
| **Wave 4: Conversations → Leads** | Backfill Lead from conversations | Lead | ~5k leads | 10-15 min | MEDIUM |
| **Wave 5: Conversations → Contacts** | Backfill Contact from conversation pairs | Contact | ~2k contacts | 5-10 min | MEDIUM |
| **Wave 6: Property Type FK** | String→FK migration | Property | ~2k updates | 15-30 min | HIGH |
| **Wave 7: New Tables (empty)** | Create all new tables (Phase A-F) | 22 tables | 0 new rows | None | LOW |

### 8.2 Wave Dependencies

```
Wave 0 (Schema)
  ├── Wave 1 (Geography) — independent
  ├── Wave 2 (Service Catalog) — independent
  ├── Wave 3 (Backfill Enrichments) — depends on Wave 0
  ├── Wave 4 (Leads) — depends on Wave 0
  ├── Wave 5 (Contacts) — depends on Wave 0
  └── Wave 6 (Property Type FK) — depends on Wave 0 + Wave 3
Wave 7 (New Tables) — depends on Wave 0, can be done in parallel with 1-6
```

### 8.3 Migration Script Requirements

Each migration script MUST include:
1. **Pre-flight check**: validate assumptions (table exists, column nullable, etc.)
2. **Batch processing**: process in chunks of 500 rows with progress logging
3. **Idempotency**: safe to run multiple times (upsert semantics)
4. **Dry-run mode**: `--dry-run` flag that logs what would change without executing
5. **Monitoring**: emit metrics on rows processed, errors, duration
6. **Rollback**: corresponding rollback script (tested)
7. **Audit**: log all changes to migration_audit table

### 8.4 Migration Window Requirements

| Wave | Window Type | Duration | Concurrent App Access? |
|------|-------------|----------|------------------------|
| Wave 0 | Maintenance | 30 min | Read-only mode |
| Wave 1 | Online | 5 min | Full access |
| Wave 2 | Online | 2 min | Full access |
| Wave 3 | Maintenance | 15 min | Read-only mode |
| Wave 4 | Maintenance | 20 min | Read-only mode |
| Wave 5 | Maintenance | 15 min | Read-only mode |
| Wave 6 | Maintenance | 60 min | Read-only mode |
| Wave 7 | Online | 10 min | Full access |

---

## 9. Testing Impacts

### 9.1 New Test Categories

| Category | Count | Est. Effort | Tools |
|----------|-------|-------------|-------|
| Unit tests: 22 new entities | ~330 | 3 weeks | pytest + factory_boy |
| Integration tests: ~60 endpoints | ~300 | 3 weeks | pytest + httpx |
| State machine tests: 14 workflows | ~140 | 2 weeks | pytest + state_machine |
| Scoring engine tests | ~100 | 1 week | pytest + parametrize |
| Data migration tests | ~30 | 1 week | pytest + temp DB |
| Backward compatibility tests | ~50 | 1 week | pytest + v3 contract |
| E2E tests: new pages | ~60 | 2 weeks | Playwright |
| **Total new tests** | **~1010** | **13 weeks** | |

### 9.2 Backward Compatibility Test Suite

A dedicated backward compatibility suite MUST pass before any extension deployment:

| Test | What It Checks |
|------|----------------|
| v3 contract tests | All existing v3 endpoints return expected shapes |
| v3 enum validation | New enum values don't break existing consumers |
| v3 field absence | Strict-mode v3 responses have no new fields |
| v3 error codes | Error codes unchanged |
| v3 auth flow | Authentication unchanged |
| v3 webhook payloads | Webhook payloads backward compatible |
| v3 SDK compatibility | SDK v3 works with extended API |
| Old data integrity | Existing records readable after migration |
| Feature flag off | System behaves exactly as pre-extension |
| Feature flag on | New functionality works without breaking old |

### 9.3 Regression Test Requirements

| Condition | Must Pass | Before |
|-----------|-----------|--------|
| Feature flag OFF + v3 client | Full existing test suite | Every deployment |
| Feature flag OFF + v4 client | Full existing suite + new entity tests | Weekly |
| Feature flag ON + v3 client | Full existing suite + BC tests | Every deployment |
| Feature flag ON + v4 client | Full suite + new tests | Every deployment |
| After data migration | Full existing suite + data integrity checks | Post-migration |

---

## 10. Rollback Procedures

### 10.1 Rollback Decision Criteria

Rollback is triggered if ANY of the following occur within 24 hours of deployment:
- Error rate increase > 5% (baseline vs. post-deploy)
- P1 (critical) bug confirmed
- Data integrity violation detected
- Performance degradation > 20% on p95 latency
- Unable to complete migration within maintenance window

### 10.2 Rollback by Component

| Component | Rollback Action | Data Loss | Time | Trigger |
|-----------|----------------|-----------|------|---------|
| **Feature Flag** | Toggle flag OFF | None (new data becomes invisible) | 1 min | Any issue |
| **New API endpoints** | Remove v4 routes from gateway | None | 5 min | v4 client issues |
| **API v3 enrichment** | Feature flag OFF returns v3-strict | None | 1 min | Client breakage |
| **New columns (M1-M3)** | `ALTER TABLE ... DROP COLUMN` | Column data | 10 min | Schema conflict |
| **Reference tables (M4)** | `DROP TABLE` + revert to string enums | Seed data | 5 min | Application failure |
| **Property type FK (M6)** | Remove FK constraint; keep string column | None | 15 min | Migration failure |
| **New tables (M7)** | `DROP TABLE ... CASCADE` | All new data | 10 min | Catastrophic failure |
| **Full system** | Restore from pre-migration DB snapshot | < 1 hour data | 1-2 hours | Multi-component failure |

### 10.3 Rollback Scripts

Each migration wave has a pre-generated, tested rollback script:

```sql
-- M1_rollback.sql: Remove User enrichment columns
ALTER TABLE users DROP COLUMN IF EXISTS trust_level;
ALTER TABLE users DROP COLUMN IF EXISTS phone_verified;
ALTER TABLE users DROP COLUMN IF EXISTS email_verified;
ALTER TABLE users DROP COLUMN IF EXISTS identity_verified;
ALTER TABLE users DROP COLUMN IF EXISTS professional_docs_verified;
ALTER TABLE users DROP COLUMN IF EXISTS professional_verified;
ALTER TABLE users DROP COLUMN IF EXISTS reference_account;
ALTER TABLE users DROP COLUMN IF EXISTS owner_verified;
ALTER TABLE users DROP COLUMN IF EXISTS is_active_agent;
ALTER TABLE users DROP COLUMN IF EXISTS onboarding_status;
ALTER TABLE users DROP COLUMN IF EXISTS agency_role;
ALTER TABLE users DROP COLUMN IF EXISTS agent_rating;
ALTER TABLE users DROP COLUMN IF EXISTS last_activity_at;
ALTER TABLE users DROP COLUMN IF EXISTS no_show_count;

-- M2_rollback.sql: Remove Property enrichment columns
ALTER TABLE properties DROP COLUMN IF EXISTS property_family;
ALTER TABLE properties DROP COLUMN IF EXISTS boost_level;
ALTER TABLE properties DROP COLUMN IF EXISTS boost_expires_at;
ALTER TABLE properties DROP COLUMN IF EXISTS is_premium;
ALTER TABLE properties DROP COLUMN IF EXISTS verification_status;
ALTER TABLE properties DROP COLUMN IF EXISTS verified_at;
ALTER TABLE properties DROP COLUMN IF EXISTS price_displayed;
ALTER TABLE properties DROP COLUMN IF EXISTS price_negotiable;
ALTER TABLE properties DROP COLUMN IF EXISTS price_negotiable_min;
ALTER TABLE properties DROP COLUMN IF EXISTS price_historical;
ALTER TABLE properties DROP COLUMN IF EXISTS data_quality_score;
ALTER TABLE properties DROP COLUMN IF EXISTS data_quality_grade;
ALTER TABLE properties DROP COLUMN IF EXISTS auto_archive_at;
ALTER TABLE properties DROP COLUMN IF EXISTS publish_status;
ALTER TABLE properties DROP COLUMN IF EXISTS matched_count;
ALTER TABLE properties DROP COLUMN IF EXISTS view_count;

-- M3_rollback.sql: Remove Project enrichment columns
ALTER TABLE projects DROP COLUMN IF EXISTS business_role;
ALTER TABLE projects DROP COLUMN IF EXISTS urgency_score;
ALTER TABLE projects DROP COLUMN IF EXISTS urgency_level;
ALTER TABLE projects DROP COLUMN IF EXISTS journey_stage;
ALTER TABLE projects DROP COLUMN IF EXISTS multi_intent_group_id;
ALTER TABLE projects DROP COLUMN IF EXISTS matching_status;
ALTER TABLE projects DROP COLUMN IF EXISTS rematch_count;
ALTER TABLE projects DROP COLUMN IF EXISTS dossier_health_score;

-- M4_rollback.sql: Remove Organization enrichment columns
ALTER TABLE organizations DROP COLUMN IF EXISTS agency_verified;
ALTER TABLE organizations DROP COLUMN IF EXISTS trust_level;
ALTER TABLE organizations DROP COLUMN IF EXISTS rccm;
ALTER TABLE organizations DROP COLUMN IF EXISTS tax_id;
ALTER TABLE organizations DROP COLUMN IF EXISTS cni_document;
ALTER TABLE organizations DROP COLUMN IF EXISTS operational_status;
ALTER TABLE organizations DROP COLUMN IF EXISTS agent_count_min;

-- M5_rollback.sql: Drop reference tables
DROP TABLE IF EXISTS property_types CASCADE;
DROP TABLE IF EXISTS professional_categories CASCADE;
DROP TABLE IF EXISTS service_categories CASCADE;
DROP TABLE IF EXISTS geo_levels CASCADE;

-- M6_rollback.sql: Revert property type FK
ALTER TABLE properties DROP CONSTRAINT IF EXISTS fk_property_type_id;
ALTER TABLE properties DROP COLUMN IF EXISTS property_type_id;

-- M7_rollback.sql: Drop all new tables (reverse dependency order)
DROP TABLE IF EXISTS identity_resolutions CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS financing_requests CASCADE;
DROP TABLE IF EXISTS professional_profiles CASCADE;
DROP TABLE IF EXISTS agent_invitations CASCADE;
DROP TABLE IF EXISTS mediations CASCADE;
DROP TABLE IF EXISTS incidents CASCADE;
DROP TABLE IF EXISTS approval_workflows CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS agent_credits CASCADE;
DROP TABLE IF EXISTS lead_purchases CASCADE;
DROP TABLE IF EXISTS leads CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS service_orders CASCADE;
DROP TABLE IF EXISTS services CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS visits CASCADE;
DROP TABLE IF EXISTS negotiations CASCADE;
DROP TABLE IF EXISTS contacts CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS intents CASCADE;
DROP TABLE IF EXISTS geographic_units CASCADE;
```

### 10.4 Rollback Drill Requirements

| Drill | Frequency | Participants | Success Criteria |
|-------|-----------|-------------|-----------------|
| Feature flag toggle | Weekly | 1 engineer | < 1 min to toggle |
| Single migration rollback | Monthly | 2 engineers | < 30 min to rollback |
| Full system rollback | Quarterly | Full team | < 2 hours to restore |
| Disaster recovery | Bi-annual | Full team + ops | < 4 hours to full recovery |

### 10.5 Rollback Communication

On rollback trigger:
1. **Immediate**: Toggle feature flag OFF (1 min)
2. **5 min**: Notify stakeholders via incident channel
3. **15 min**: Begin rollback procedure
4. **30 min**: Rollback complete or escalate
5. **60 min**: Post-mortem initiated
6. **24 hours**: Root cause analysis submitted

---

*End of BACKWARD_COMPATIBILITY_PLAN.md — 11 impact areas analyzed, 4 mapping tables, 5 migration strategies, 8 compatibility guarantees, 30 feature flags, 8 migration waves, ~1010 new tests estimated, 10 rollback procedures defined.*
