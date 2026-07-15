# PROPERTY TYPE CROSSWALK — Heritage Gold → LAWIM V2

**Document ID:** LAWIM-HARM-CROSSWALK-PROPERTY-V1
**Status:** CANONICAL — Semantic harmonization reference
**Date:** 2026-07-15

---

## Table of Contents

1. [Family Comparison](#1-family-comparison)
2. [Detailed Type Mapping](#2-detailed-type-mapping)
3. [Lifecycle State Machine Comparison](#3-lifecycle-state-machine-comparison)
4. [Publication Rules Comparison](#4-publication-rules-comparison)
5. [Price Concepts Mapping](#5-price-concepts-mapping)
6. [Data Quality Scoring Comparison](#6-data-quality-scoring-comparison)
7. [Gaps Analysis](#7-gaps-analysis)

---

## 1. Family Comparison

### Heritage Gold — 7 Well-Defined Property Families

| ID | Family | Code | Sub-referentiel | Confidence |
|----|--------|------|-----------------|------------|
| GOLD-PR-001 | Résidentiel | residential | Directive/02A-RESIDENTIAL-REFERENCE.md | HIGH |
| GOLD-PR-002 | Commercial | commercial | Directive/02B-COMMERCIAL-REFERENCE.md | HIGH |
| GOLD-PR-003 | Industriel | industrial | Directive/02C-INDUSTRIAL-REFERENCE.md | HIGH |
| GOLD-PR-004 | Foncier (Terrain) | land | Directive/02D-LAND-REFERENCE.md | HIGH |
| GOLD-PR-005 | Agricole | agricultural | Directive/02E-AGRICULTURAL-REFERENCE.md | HIGH |
| GOLD-PR-006 | Hôtelier | hotel | Directive/02F-HOTEL-REFERENCE.md | HIGH |
| GOLD-PR-007 | Projet immobilier | project | Directive/02G-PROJECT-REFERENCE.md | HIGH |

### Current LAWIM V2 — No Family Concept

| Aspect | Current V2 | Gap |
|--------|-----------|-----|
| propertyType | Free-form String (no enum) | No type constraint |
| Family field | Not present | Full gap — no family/sub-referentiel |
| Inheritance | No master model | Full gap |
| Sub-referentiel | No sub-type system | Full gap |

### Family-Level Crosswalk

| Gold Family | V2 Equivalent | Mapping Status | Notes |
|-------------|---------------|----------------|-------|
| Résidentiel | implied by type values | ONE_TO_MANY | Can be inferred from property_type in metadata_json |
| Commercial | implied by type values | ONE_TO_MANY | Can be inferred from property_type in metadata_json |
| Industriel | not represented | EXTENSION_REQUIRED | No distinct family in V2 |
| Foncier (Terrain) | loosely implied by "land" type | PARTIAL_MATCH | No land-specific family handling |
| Agricole | not represented | EXTENSION_REQUIRED | Entire family missing |
| Hôtelier | not represented | PARTIAL_MATCH | Hotel is a commercial type but lacks dedicated family |
| Projet immobilier | not represented | EXTENSION_REQUIRED | Entire family missing |

**Recommended Resolution:** Add a `property_family` enum field to the Property model with the 7 Gold families. Use `metadata_json` as interim storage until schema migration.

---

## 2. Detailed Type Mapping

### 2.1 Eleven Basic Types (from property-qualification-reference.md)

| Crosswalk ID | Gold Type | Gold Family | V2 Current | Mapping Status | Semantic Differences | Recommended Resolution |
|-------------|-----------|-------------|------------|----------------|---------------------|----------------------|
| CW-TYPE-001 | appartement | Résidentiel | Free string | NORMALIZED_MATCH | V2 accepts any string; Gold has sub-types (non_meuble, meuble, courte_duree) | Normalize to `apartment`; store sub-type in metadata_json |
| CW-TYPE-002 | maison | Résidentiel | Free string | NORMALIZED_MATCH | Gold distinguishes maison_individuelle and maison_de_ville | Normalize to `house`; store specificity in metadata_json |
| CW-TYPE-003 | villa | Résidentiel | Free string | NORMALIZED_MATCH | Gold distinguishes villa (large) and villa_basse (single-story) | Normalize to `villa`; store subtype in metadata_json |
| CW-TYPE-004 | studio | Résidentiel | Free string | NORMALIZED_MATCH | Gold has studio, studio_moderne, studio_meuble subtypes | Normalize to `studio`; store subtype in metadata_json |
| CW-TYPE-005 | duplex | Résidentiel | Free string | NORMALIZED_MATCH | Two-level apartment | Normalize to `duplex` |
| CW-TYPE-006 | chambre | Résidentiel | Free string | NORMALIZED_MATCH | Gold has chambre_simple, chambre_moderne, chambre_hotel | Normalize to `room`; store subtype in metadata_json |
| CW-TYPE-007 | immeuble | Résidentiel | Free string | NORMALIZED_MATCH | Gold: residential building; V2 has no building-specific fields | Normalize to `building` |
| CW-TYPE-008 | terrain | Foncier | Free string | NORMALIZED_MATCH | Gold has 7 land subtypes (titre/loti/morcellement) | Normalize to `land`; store subtype in metadata_json |
| CW-TYPE-009 | boutique | Commercial | Free string | NORMALIZED_MATCH | Gold: shop/retail space | Normalize to `shop` |
| CW-TYPE-010 | entrepôt | Industriel | Free string | NORMALIZED_MATCH | Gold: warehouse; can also be commercial | Normalize to `warehouse` |
| CW-TYPE-011 | bureau | Commercial | Free string | NORMALIZED_MATCH | Gold: office space | Normalize to `office` |

### 2.2 Residential Matrix Types (18)

| Crosswalk ID | Gold Matrix Type | Parent Type | V2 Current | Mapping Status | Notes |
|-------------|-----------------|-------------|------------|----------------|-------|
| CW-RES-001 | chambre_simple | chambre | Free string | NORMALIZED_MATCH | Basic room for rent |
| CW-RES-002 | chambre_moderne | chambre | Free string | NORMALIZED_MATCH | Room with private shower |
| CW-RES-003 | studio | studio | Free string | EXACT_MATCH | Basic studio apartment |
| CW-RES-004 | studio_moderne | studio | Free string | NORMALIZED_MATCH | Studio with internal shower |
| CW-RES-005 | studio_meuble | studio | Free string | NORMALIZED_MATCH | Furnished studio |
| CW-RES-006 | appartement_non_meuble | appartement | Free string | NORMALIZED_MATCH | Unfurnished apartment |
| CW-RES-007 | appartement_meuble | appartement | Free string | NORMALIZED_MATCH | Furnished apartment |
| CW-RES-008 | villa | villa | Free string | EXACT_MATCH | Standalone villa |
| CW-RES-009 | villa_basse | villa | Free string | NORMALIZED_MATCH | Single-story villa |
| CW-RES-010 | duplex | duplex | Free string | EXACT_MATCH | Two-level unit |
| CW-RES-011 | triplex | (extension) | Free string | NORMALIZED_MATCH | Three-level unit — not in basic types |
| CW-RES-012 | maison_individuelle | maison | Free string | NORMALIZED_MATCH | Single-family home |
| CW-RES-013 | maison_de_ville | maison | Free string | NORMALIZED_MATCH | Townhouse |
| CW-RES-014 | chambre_hotel | chambre | Free string | NORMALIZED_MATCH | Hotel room (short-term) |
| CW-RES-015 | appartement_courte_duree | appartement | Free string | NORMALIZED_MATCH | Short-term rental apartment |
| CW-RES-016 | residence_meublee | (extension) | Free string | NORMALIZED_MATCH | Furnished residence |
| CW-RES-017 | colocation | (extension) | Free string | NORMALIZED_MATCH | Shared housing |
| CW-RES-018 | cite_universitaire | (extension) | Free string | NORMALIZED_MATCH | University residence |

### 2.3 Land Matrix Types (7)

| Crosswalk ID | Gold Matrix Type | Parent Type | V2 Current | Mapping Status | Notes |
|-------------|-----------------|-------------|------------|----------------|-------|
| CW-LAND-001 | terrain_titre | terrain | Free string | NORMALIZED_MATCH | Land with title deed |
| CW-LAND-002 | terrain_non_titre | terrain | Free string | NORMALIZED_MATCH | Land without title deed |
| CW-LAND-003 | terrain_loti | terrain | Free string | NORMALIZED_MATCH | Serviced land |
| CW-LAND-004 | terrain_non_loti | terrain | Free string | NORMALIZED_MATCH | Unserviced land |
| CW-LAND-005 | terrain_titre_collectif | terrain | Free string | NORMALIZED_MATCH | Collective title land |
| CW-LAND-006 | terrain_titre_individuel | terrain | Free string | NORMALIZED_MATCH | Individual title land |
| CW-LAND-007 | terrain_sous_morcellement | terrain | Free string | NORMALIZED_MATCH | Land undergoing subdivision |

### 2.4 Commercial Matrix Types (16)

| Crosswalk ID | Gold Matrix Type | Parent Type | V2 Current | Mapping Status | Notes |
|-------------|-----------------|-------------|------------|----------------|-------|
| CW-COM-001 | boutique | boutique | Free string | EXACT_MATCH | Shop/retail |
| CW-COM-002 | bureau | bureau | Free string | EXACT_MATCH | Office space |
| CW-COM-003 | local_commercial | (extension) | Free string | NORMALIZED_MATCH | General commercial space |
| CW-COM-004 | magasin | (extension) | Free string | NORMALIZED_MATCH | Store |
| CW-COM-005 | entrepot | entrepôt | Free string | NORMALIZED_MATCH | Warehouse |
| CW-COM-006 | hangar | (extension) | Free string | NORMALIZED_MATCH | Hangar/shed |
| CW-COM-007 | atelier | (extension) | Free string | NORMALIZED_MATCH | Workshop |
| CW-COM-008 | restaurant | (extension) | Free string | NORMALIZED_MATCH | Restaurant space |
| CW-COM-009 | bar | (extension) | Free string | NORMALIZED_MATCH | Bar/nightlife |
| CW-COM-010 | hotel | (extension) | Free string | NORMALIZED_MATCH | Hotel (commercial family vs hotelier family in Gold) |
| CW-COM-011 | auberge | (extension) | Free string | NORMALIZED_MATCH | Inn/lodge |
| CW-COM-012 | immeuble_de_rapport | (extension) | Free string | NORMALIZED_MATCH | Income-generating building |
| CW-COM-013 | immeuble_commercial | (extension) | Free string | NORMALIZED_MATCH | Commercial building |
| CW-COM-014 | station_service | (extension) | Free string | NORMALIZED_MATCH | Gas station |
| CW-COM-015 | site_industriel | (extension) | Free string | NORMALIZED_MATCH | Industrial site |
| CW-COM-016 | espace_evenementiel | (extension) | Free string | NORMALIZED_MATCH | Event space |

### 2.5 Investment Types (5)

| Crosswalk ID | Gold Matrix Type | V2 Current | Mapping Status | Notes |
|-------------|-----------------|------------|----------------|-------|
| CW-INV-001 | investissement_locatif | Not represented | EXTENSION_REQUIRED | Rental investment |
| CW-INV-002 | investissement_terrain | Not represented | EXTENSION_REQUIRED | Land investment |
| CW-INV-003 | investissement_immobilier_commercial | Not represented | EXTENSION_REQUIRED | Commercial real estate investment |
| CW-INV-004 | investissement_promotion | Not represented | EXTENSION_REQUIRED | Development investment |
| CW-INV-005 | syndicat_copropriete | Not represented | EXTENSION_REQUIRED | Condominium syndicate |

### 2.6 Financing Types (10) — Not in Property Model

| Crosswalk ID | Gold Matrix Type | V2 Current | Mapping Status | Notes |
|-------------|-----------------|------------|----------------|-------|
| CW-FIN-001 through CW-FIN-010 | credit_immobilier through financement_professionnel | Not represented | EXTENSION_REQUIRED | Financing is outside property scope; maps to Project model |

### 2.7 Service Types (51) — Out of Property Scope

| Type | Count | V2 Current | Mapping Status | Notes |
|------|-------|------------|----------------|-------|
| Professional Services | 27 | Not represented | EXTENSION_REQUIRED | Outside property model scope |
| Real Estate Services | 24 | Not represented | EXTENSION_REQUIRED | Outside property model scope |

---

## 3. Lifecycle State Machine Comparison

### Heritage Gold — 10-Step Workflow

| Step | Name | Description |
|------|------|-------------|
| 1 | Réception | Reception of property data |
| 2 | Normalisation | Data normalization |
| 3 | Classification | Family and type classification |
| 4 | Validation | Consistency checks |
| 5 | Publication | Publication or hold |
| 6 | Matching | Compatibility scoring |
| 7 | Mise en relation | Connection between demandeur and détenteur |
| 8 | Suivi | Transaction follow-up |
| 9 | Archivage | Archiving |
| 10 | Conservation historique | Historical preservation |

### Current LAWIM V2 — 5 Statuses

| Status | Allowed Transitions | Description |
|--------|---------------------|-------------|
| draft | draft, open, closed, published, archived | Initial creation |
| open | open, published, closed, archived | Active listing |
| published | published, closed, archived | Publicly visible |
| closed | closed, archived | Ended without transaction |
| archived | archived | Final state |

### Heritage Gold Availability States (5)

```
available ──► pending ──► rented ──► archived
  │            │  │         │
  │            │  └──► sold ────► archived
  │            │
  └──► archived  └──► available
```

### Current V2 Availability States (5)

| State | Description |
|-------|-------------|
| available | Property available |
| reserved | Reserved for a client |
| sold | Property sold |
| rented | Property rented |
| unavailable | Temporarily unavailable |

### Lifecycle Crosswalk

| Gold Concept | V2 Status | V2 Availability | Mapping Status | Notes |
|-------------|-----------|-----------------|----------------|-------|
| Réception (step 1) | draft | available | PARTIAL_MATCH | V2 has draft but no explicit reception phase |
| Normalisation (step 2) | draft | — | PARTIAL_MATCH | No explicit normalization step |
| Classification (step 3) | — | — | UNMAPPED | No family/type classification step in V2 |
| Validation (step 4) | open | — | PARTIAL_MATCH | V2 validates on create but has no dedicated validation step |
| Publication (step 5) | published | available | NORMALIZED_MATCH | Gold can_publish() ≈ V2 can_publish() |
| Matching (step 6) | published | — | NORMALIZED_MATCH | Matching runs on published properties |
| Mise en relation (step 7) | — | — | UNMAPPED | No explicit connection tracking |
| Suivi (step 8) | — | — | UNMAPPED | No transaction follow-up state |
| Archivage (step 9) | archived | — | NORMALIZED_MATCH | Both have archived as final state |
| Conservation historique (step 10) | — | — | UNMAPPED | No historical preservation in V2 |
| available→pending | — | reserved | NORMALIZED_MATCH | Gold pending ≈ V2 reserved |
| available→archived | archived | — | NORMALIZED_MATCH | Direct archiving path |
| pending→rented | — | rented | EXACT_MATCH | Same semantics |
| pending→sold | — | sold | EXACT_MATCH | Same semantics |
| pending→available | — | available | NORMALIZED_MATCH | Transaction cancelled, re-available |
| pending→archived | archived | — | NORMALIZED_MATCH | Transaction failed → archive |
| rented→archived | archived | — | NORMALIZED_MATCH | Rental ended → archive |
| sold→archived | archived | — | NORMALIZED_MATCH | Sale finalized → archive |
| archived→available | — | available | NORMALIZED_MATCH | Re-listing |
| Auto-archive 90 days | — | — | PARTIAL_MATCH | V2 has no auto-archive rule |

**Gap:** V2 has no `pending` status equivalent in the status field; the `reserved` availability serves as a proxy. V2 has no workflow steps 1-4, 7-8, 10. The 10-step workflow is compressed into 5 statuses.

---

## 4. Publication Rules Comparison

### Heritage Gold Publication Rules

| ID | Rule | Description |
|----|------|-------------|
| GOLD-PR-062 | Family identified | Property must have a family |
| GOLD-PR-063 | Type coherent | Type must be consistent with family |
| GOLD-PR-064 | Location known | Minimum location must be known |
| GOLD-PR-065 | Price provided | Price must be provided |
| GOLD-PR-066 | Détenteur identifiable | Holder must be identifiable |
| GOLD-PR-067 | Critical info normalized | All critical info must be normalized |
| GOLD-PR-068 | Documents present | Required documents must be present |
| GOLD-PR-069 | Code check | `can_publish()` checks: title, city, price exist; deleted_at is null |

### Current V2 Publication Check

```python
def can_publish(property_row: dict[str, object]) -> bool:
    if property_row.get("deleted_at"):
        return False
    if not property_row.get("title") or not property_row.get("city"):
        return False
    if property_row.get("price_min") is None and property_row.get("price_max") is None:
        return False
    return True
```

### Publication Rules Crosswalk

| Gold Rule | V2 Equivalent | Mapping Status | Notes |
|-----------|---------------|----------------|-------|
| Family identified | Not checked | UNMAPPED | No family concept in V2 |
| Type coherent | Not checked | UNMAPPED | No type validation against family |
| Location known | city must be present | NORMALIZED_MATCH | V2 checks city presence |
| Price provided | price_min or price_max | NORMALIZED_MATCH | V2 checks price range |
| Détenteur identifiable | ownerOrganizationId (optional) | PARTIAL_MATCH | V2 has organization but it's nullable |
| Critical info normalized | Not checked | UNMAPPED | No normalization check |
| Documents present | Not checked | UNMAPPED | No document requirement check |
| Code check: title | title must be present | EXACT_MATCH | Both require title |
| Code check: deleted_at | deleted_at must be null | EXACT_MATCH | Both require non-deleted |

**Gap:** V2 has only 3 of 8 Gold publication rules implemented. Family validation, type coherence, détenteur identification, normalization, and document presence are missing.

---

## 5. Price Concepts Mapping

### Heritage Gold — 6 Price Levels

| ID | Concept | Description |
|----|---------|-------------|
| GOLD-PR-070 | Prix affiché | Displayed/listed price |
| GOLD-PR-071 | Prix négociable | Negotiable price |
| GOLD-PR-072 | Prix final | Final agreed price |
| GOLD-PR-073 | Estimation | Estimated value |
| GOLD-PR-074 | Fourchette de marché | Market price range |
| GOLD-PR-075 | Historique de variation | Historical price variation |

### Heritage Gold — Additional Price Types

| ID | Price Type | Context |
|----|-----------|---------|
| GOLD-PR-076 | Loyer | Monthly rent |
| GOLD-PR-077 | Caution | Security deposit |
| GOLD-PR-078 | Avance | Rent advance |
| GOLD-PR-079 | Dépôt de garantie | Guarantee deposit |
| GOLD-PR-080 | Mensualité | Monthly payment |
| GOLD-PR-081 | Frais de service | Service fees |
| GOLD-PR-082 | Taxes | Applicable taxes |

### Current V2 — Price Model

```prisma
priceMin    Int?    @map("price_min")
priceMax    Int?    @map("price_max")
currency    String
```

### Price Concepts Crosswalk

| Gold Concept | V2 Equivalent | Mapping Status | Notes |
|-------------|---------------|----------------|-------|
| Prix affiché | price_min / price_max | PARTIAL_MATCH | V2 has range but no single displayed price |
| Prix négociable | metadata_json | PARTIAL_MATCH | Could be stored as `negotiable: true` in metadata |
| Prix final | Not stored | EXTENSION_REQUIRED | No final price tracking |
| Estimation | Not stored | EXTENSION_REQUIRED | No estimation concept |
| Fourchette de marché | price_min / price_max | NORMALIZED_MATCH | Range maps to min/max |
| Historique de variation | Not stored | EXTENSION_REQUIRED | No price history |
| Loyer | Not distinguished | PARTIAL_MATCH | Rent vs sale not distinguished in price fields |
| Caution | Not stored | EXTENSION_REQUIRED | No deposit field |
| Avance | Not stored | EXTENSION_REQUIRED | No advance field |
| Dépôt de garantie | Not stored | EXTENSION_REQUIRED | No guarantee deposit |
| Mensualité | Not stored | EXTENSION_REQUIRED | No monthly payment |
| Frais de service | Not stored | EXTENSION_REQUIRED | No service fee concept |
| Taxes | Not stored | EXTENSION_REQUIRED | No tax concept |
| Currency normalization | normalize_currency() | EXACT_MATCH | Both support XAF, EUR, USD, GBP, XOF |

**Gap:** V2 supports only 2 of 13 Gold price concepts (range + currency). The remaining 11 concepts require schema extension or metadata_json storage.

---

## 6. Data Quality Scoring Comparison

### Heritage Gold Scoring

| Component | Weight | Details |
|-----------|--------|---------|
| Quality Score | 100% | `int(completeness * 0.6 + reliability * 0.4)` |
| Completeness | 60% | Title(10%), Description(15%), Price(15%), Location(15%), Type(15%), Images(15%) |
| Source Reliability | 40% | agent(90), google_form(85), import(70), whatsapp(50), unknown(30) |
| Grading | — | A+(≥80), A(≥60), B(≥40), C(≥20), D(<20) |

### Current V2 — No Scoring

| Aspect | V2 Status | Gap |
|--------|-----------|-----|
| Quality scoring | Not implemented | Full gap |
| Completeness | Not calculated | Full gap |
| Source reliability | Not tracked | Full gap |
| Grading scale | Not exists | Full gap |

**Gap:** Entire data quality scoring system is absent from V2. All 5 grading levels, both scoring dimensions, and the reliability matrix require implementation.

---

## 7. Gaps Analysis

### 7.1 Summary of All Gaps

| # | Gap Area | Gold Coverage | V2 Coverage | Gap Severity | Impact |
|---|----------|--------------|-------------|-------------|--------|
| GAP-001 | Property Families | 7 families with sub-referentials | 0 (free-form only) | CRITICAL | Classification, matching, validation broken |
| GAP-002 | Property Types | 11 basic + 41 matrix types | 0 (free-form only) | CRITICAL | Cannot validate type; no type-based logic |
| GAP-003 | Full Matrix Types | 107 matrices | 0 | HIGH | Qualification matrices unusable |
| GAP-004 | Workflow Steps | 10-step workflow | 5 statuses | HIGH | Missing normalization, classification, validation, matching stages |
| GAP-005 | Availability States | 5 states with transitions | 5 strings (no transitions) | MEDIUM | No availability state machine enforcement |
| GAP-006 | Auto-Archive | 90-day rule | Not implemented | MEDIUM | Stale properties never auto-archived |
| GAP-007 | Publication Rules | 8 rules | 3 of 8 | HIGH | Missing family, type, détenteur, docs validation |
| GAP-008 | Price Concepts | 6 levels + 7 types | 2 fields (min/max) | HIGH | Cannot support pricing workflows |
| GAP-009 | Data Quality Scoring | Full scoring engine | Not implemented | MEDIUM | No quality-based ranking |
| GAP-010 | Per-Type Specific Fields | 4 categories with specific fields | 3 generic fields | HIGH | Missing surface, floor, elevator, title status, etc. |
| GAP-011 | Investment Types | 5 types | Not represented | MEDIUM | Investment workflow not supported |
| GAP-012 | Agricultural Family | Full family spec | Not represented | MEDIUM | Agricultural properties unsupported |
| GAP-013 | Hotelier Family | Full family spec | Not represented | LOW | Hotel as commercial type in V2 |
| GAP-014 | Project Family | Full family spec | Not represented | LOW | Project not a property type in V2 |
| GAP-015 | Transaction Types | rent/buy/sell/invest/finance/find | Not on Property model | MEDIUM | Transaction not on property schema |

### 7.2 Severity Breakdown

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 2 | Families, Types — core identity model |
| HIGH | 4 | Matrix types, Workflow, Publication, Pricing, Per-type fields |
| MEDIUM | 6 | Availability, Auto-archive, Quality Scoring, Investment, Agricultural, Transaction types |
| LOW | 2 | Hotelier, Project families |

### 7.3 Migration Priority

| Priority | Gaps | Effort | Recommendation |
|----------|------|--------|----------------|
| P0 | GAP-001, GAP-002 | Medium | Add `property_family` enum and `property_type` enum to Prisma schema |
| P1 | GAP-004, GAP-007, GAP-010 | High | Implement sub-type specific fields via metadata_json; expand publication checks |
| P2 | GAP-005, GAP-006, GAP-009 | Medium | Add availability state machine; implement auto-archive cron; add quality scoring |
| P3 | GAP-003, GAP-008 | High | Link to qualification matrix system; extend price model |
| P4 | GAP-011, GAP-012, GAP-013, GAP-014, GAP-015 | Low | Add remaining families and transaction types |

### 7.4 Quick Wins (Can Be Done Now)

| # | Action | Impact | Effort |
|---|--------|--------|--------|
| 1 | Add `property_family` validation to `property_domain.py` | Validates one of 7 families | 15 min |
| 2 | Create `PROPERTY_TYPES` enum set in Python | Enables type validation | 15 min |
| 3 | Store complete Gold type in `metadata_json` | Preserves granularity | 5 min |
| 4 | Add `negotiable`, `deposit`, `service_fees` to `metadata_json` | Extends price model | 5 min |
| 5 | Implement state machine validation for availability transitions | Enforces lifecycle | 30 min |

---

*End of PROPERTY_TYPE_CROSSWALK.md*
