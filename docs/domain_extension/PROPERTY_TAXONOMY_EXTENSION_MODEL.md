# PROPERTY TAXONOMY EXTENSION MODEL

**Document ID:** LAWIM-H13-PROPERTY-TAXONOMY-V1  
**Status:** CANONICAL — Extension target for H2 implementation  
**Date:** 2026-07-15  
**Source Documents:** `PROPERTY_TYPE_CROSSWALK.md`, `required_extensions.json` (§property_model), `LAWIM_UNIFIED_DOMAIN_MODEL.md` (§3), `MATRIX_CATALOG.md`

---

## Table of Contents

1. [Target Taxonomy Overview](#1-target-taxonomy-overview)
2. [Property Families](#2-property-families)
3. [Sub-Referentials Per Family](#3-sub-referentials-per-family)
4. [Extensible Taxonomy Structure](#4-extensible-taxonomy-structure)
5. [Why Monolithic Enums Are Avoided](#5-why-monolithic-enums-are-avoided)
6. [Per-Type Specific Fields](#6-per-type-specific-fields)
7. [Price Model](#7-price-model)
8. [Property Lifecycle](#8-property-lifecycle)
9. [Publication Rules](#9-publication-rules)
10. [Data Quality Scoring](#10-data-quality-scoring)
11. [Availability State Machine](#11-availability-state-machine)
12. [Auto-Archive (90-Day Rule)](#12-auto-archive-90-day-rule)
13. [Complete Extension Table](#13-complete-extension-table)

---

## 1. Target Taxonomy Overview

The property taxonomy is organized as a hierarchical classification system with clear separation of concerns across these dimensions:

| Dimension | Purpose | Example Values |
|-----------|---------|----------------|
| **property_family** | Top-level classification backbone | `residential`, `commercial`, `industrial`, `land`, `agricultural`, `hotel`, `project` |
| **property_type** | Canonical type within family | `apartment`, `villa`, `land`, `warehouse` |
| **property_subtype** | Matrix-level granularity per type | `appartement_meuble`, `terrain_titre`, `studio_moderne` |
| **usage_type** | How the property is used | `owner_occupied`, `tenant_occupied`, `vacant`, `seasonal`, `mixed`, `investment_only` |
| **occupancy_type** | Current occupancy state | `vacant`, `occupied_by_owner`, `occupied_by_tenant`, `seasonal_occupancy` |
| **furnishing_status** | Level of furnishing | `furnished`, `semi_furnished`, `unfurnished`, `equipped_kitchen` |
| **construction_style** | Architectural style | `moderne`, `traditionnelle`, `ancienne`, `contemporaine`, `industrielle` |
| **legal_status** | Legal/documentation status | `title_deed`, `land_title`, `building_permit`, `co_ownership`, `customary`, `leasehold`, `undivided` |
| **commercial_category** | Commercial use sub-category | `retail`, `office`, `food_service`, `warehouse_logistics`, `hospitality`, `industrial`, `mixed_use`, `event_space`, `vehicle_related` |
| **investment_category** | Investment type classification | `investissement_locatif`, `investissement_terrain`, `investissement_commercial`, `investissement_promotion`, `syndicat_copropriete` |

### 1.1 Taxonomy Dimensions Relationship

```
property_family (7)
  ├── property_type (11 canonical)
  │     └── property_subtype (41 matrix-level)
  ├── usage_type (6)
  ├── occupancy_type (4)
  ├── furnishing_status (4)
  ├── construction_style (5)
  ├── legal_status (7)
  ├── commercial_category (9)  [commercial family only]
  └── investment_category (5)   [investment context]
```

---

## 2. Property Families

Seven canonical property families form the classification backbone for all property logic:

| # | Family | Code | Description | Gold Source |
|---|--------|------|-------------|-------------|
| 1 | Résidentiel | `residential` | Properties designed for human habitation | GOLD-PR-001 |
| 2 | Commercial | `commercial` | Properties for business and commercial activities | GOLD-PR-002 |
| 3 | Industriel | `industrial` | Properties for manufacturing, storage, industrial use | GOLD-PR-003 |
| 4 | Foncier (Terrain) | `land` | Land parcels and undeveloped plots | GOLD-PR-004 |
| 5 | Agricole | `agricultural` | Properties for agricultural and farming activities | GOLD-PR-005 |
| 6 | Hôtelier | `hotel` | Properties for hospitality and accommodation services | GOLD-PR-006 |
| 7 | Projet immobilier | `project` | Real estate development projects and construction programs | GOLD-PR-007 |

### 2.1 Family-Level Business Rules

- Each property MUST have exactly one `property_family`
- `property_type` MUST be valid for the assigned family
- Family determines available qualification matrices
- Family determines applicable publication rules
- Family gates per-type specific fields in `metadata_json`

---

## 3. Sub-Referentials Per Family

### 3.1 Residential (18 matrix types)

| Type | Parent | Qualification Matrix | Description |
|------|--------|---------------------|-------------|
| `chambre_simple` | room | MAT-RES-001 | Basic room for rent |
| `chambre_moderne` | room | MAT-RES-002 | Room with private shower |
| `studio` | studio | MAT-RES-003 | Basic studio apartment |
| `studio_moderne` | studio | MAT-RES-004 | Studio with internal shower |
| `studio_meuble` | studio | MAT-RES-005 | Furnished studio |
| `appartement_non_meuble` | apartment | MAT-RES-006 | Unfurnished apartment |
| `appartement_meuble` | apartment | MAT-RES-007 | Furnished apartment |
| `villa` | villa | MAT-RES-008 | Standalone villa |
| `villa_basse` | villa | MAT-RES-009 | Single-story villa |
| `duplex` | duplex | MAT-RES-010 | Two-level unit |
| `triplex` | apartment | MAT-RES-011 | Three-level unit |
| `maison_individuelle` | house | MAT-RES-012 | Single-family home |
| `maison_de_ville` | house | MAT-RES-013 | Townhouse |
| `chambre_hotel` | room | MAT-RES-014 | Hotel room (short-term) |
| `appartement_courte_duree` | apartment | MAT-RES-015 | Short-term rental apartment |
| `residence_meublee` | apartment | MAT-RES-016 | Furnished residence |
| `colocation` | apartment | MAT-RES-017 | Shared housing |
| `cite_universitaire` | apartment | MAT-RES-018 | University residence |

### 3.2 Land (7 matrix types)

| Type | Parent | Qualification Matrix | Description |
|------|--------|---------------------|-------------|
| `terrain_titre` | land | MAT-LAND-001 | Land with title deed |
| `terrain_non_titre` | land | MAT-LAND-002 | Land without title deed |
| `terrain_loti` | land | MAT-LAND-003 | Serviced land |
| `terrain_non_loti` | land | MAT-LAND-004 | Unserviced land |
| `terrain_titre_collectif` | land | MAT-LAND-005 | Collective title land |
| `terrain_titre_individuel` | land | MAT-LAND-006 | Individual title land |
| `terrain_sous_morcellement` | land | MAT-LAND-007 | Land undergoing subdivision |

### 3.3 Commercial (16 matrix types)

| Type | Parent | Matrix | Description |
|------|--------|--------|-------------|
| `boutique` | shop | MAT-COM-001 | Retail shop |
| `bureau` | office | MAT-COM-002 | Office space |
| `local_commercial` | shop | MAT-COM-003 | General commercial space |
| `magasin` | shop | MAT-COM-004 | Store |
| `entrepot` | warehouse | MAT-COM-005 | Warehouse |
| `hangar` | — | MAT-COM-006 | Hangar/shed |
| `atelier` | — | MAT-COM-007 | Workshop |
| `restaurant` | — | MAT-COM-008 | Restaurant space |
| `bar` | — | MAT-COM-009 | Bar/nightlife |
| `hotel` | — | MAT-COM-010 | Hotel (commercial context) |
| `auberge` | — | MAT-COM-011 | Inn/lodge |
| `immeuble_de_rapport` | building | MAT-COM-012 | Income-generating building |
| `immeuble_commercial` | building | MAT-COM-013 | Commercial building |
| `station_service` | — | MAT-COM-014 | Gas station |
| `site_industriel` | — | MAT-COM-015 | Industrial site |
| `espace_evenementiel` | — | MAT-COM-016 | Event space |

### 3.4 Industrial (5 matrix types)

| Type | Parent | Matrix | Description |
|------|--------|--------|-------------|
| `usine` | — | MAT-IND-001 | Factory |
| `atelier_industriel` | — | MAT-IND-002 | Industrial workshop |
| `entrepot_industriel` | warehouse | MAT-IND-003 | Industrial warehouse |
| `plateforme_logistique` | — | MAT-IND-004 | Logistics platform |
| `zone_industrielle` | — | MAT-IND-005 | Industrial zone |

### 3.5 Agricultural (5 matrix types)

| Type | Parent | Matrix | Description |
|------|--------|--------|-------------|
| `plantation` | — | MAT-AGR-001 | Plantation |
| `ferme` | — | MAT-AGR-002 | Farm |
| `terre_agricole` | — | MAT-AGR-003 | Agricultural land |
| `elevage` | — | MAT-AGR-004 | Livestock farm |
| `exploitation_agricole` | — | MAT-AGR-005 | Agricultural operation |

### 3.6 Hotel (5 matrix types)

| Type | Parent | Matrix | Description |
|------|--------|--------|-------------|
| `hotel` | — | MAT-HOT-001 | Hotel establishment |
| `auberge` | — | MAT-HOT-002 | Inn |
| `residence_touristique` | — | MAT-HOT-003 | Tourist residence |
| `chambre_hotel` | — | MAT-HOT-004 | Hotel room |
| `campement` | — | MAT-HOT-005 | Lodging camp |

### 3.7 Project (4 matrix types)

| Type | Parent | Matrix | Description |
|------|--------|--------|-------------|
| `lotissement` | — | MAT-PRO-001 | Land subdivision |
| `promotion_immobiliere` | — | MAT-PRO-002 | Real estate development |
| `construction_neuve` | — | MAT-PRO-003 | New construction |
| `renovation` | — | MAT-PRO-004 | Renovation project |

---

## 4. Extensible Taxonomy Structure

Each taxonomy node follows this canonical schema:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `canonical_id` | String | Yes | Unique hierarchical identifier (e.g., `residential.apartment.studio_meuble`) |
| `canonical_name` | String | Yes | Primary canonical name |
| `aliases` | String[] | No | Alternative names and legacy mappings |
| `parent_id` | String | No | Parent canonical ID for hierarchical relationships |
| `family` | String | Yes | Property family this type belongs to |
| `applicable_transactions` | String[] | Yes | Transaction types applicable to this property type |
| `applicable_fields` | String[] | No | Specific fields relevant for this type |
| `qualification_matrix_ids` | String[] | No | References to qualification matrices applicable to this type |
| `matching_dimensions` | String[] | No | Matching scoring dimensions relevant for this type |
| `verification_requirements` | String[] | No | Required verification documents or checks |
| `status` | Enum | Yes | `active`, `deprecated`, `draft` |
| `version` | Integer | Yes | Version number for change tracking |

### 4.1 Canonical ID Convention

```
{family}.{type}.{subtype}
```

Examples:
- `residential.apartment.appartement_meuble`
- `land.land.terrain_titre`
- `commercial.shop.boutique`
- `industrial.warehouse.entrepot_industriel`

### 4.2 Registry Pattern

Types are registered in family-scoped registries rather than a global enum:

```typescript
interface PropertyTypeRegistry {
  [family: string]: {
    [typeId: string]: PropertyTypeNode;
  };
}
```

---

## 5. Why Monolithic Enums Are Avoided

The taxonomy explicitly rejects a single monolithic `property_type` enum in favor of a hierarchical, registry-based approach. Rationale:

| # | Reason | Detail |
|---|--------|--------|
| 1 | **Unmanageable cardinality** | 76+ types across 7 families would create an unwieldy single enum |
| 2 | **Family-specific validation** | Per-family validation rules require polymorphic handling a flat enum cannot express |
| 3 | **Independent evolution** | Sub-referentials evolve independently — coupling unrelated types in one enum creates fragility |
| 4 | **Metadata binding** | Qualification matrix, field, and verification requirement binding is per-type, not per-enum |
| 5 | **Legacy aliasing** | Multiple legacy names map to the same canonical type — structured taxonomy supports aliasing naturally |
| 6 | **Extensibility** | New types can be added per family without affecting other families or breaking the enum contract |
| 7 | **Versioning** | Individual types can be deprecated or versioned without affecting the entire classification system |
| 8 | **Query performance** | Family-scoped lookups are faster and more cacheable than monolithic enum filtering |

### 5.1 Alternative: Family-Scoped Type Registries

```
property_family (enum of 7)
  └── property_type (string reference to canonical_id)
  └── property_subtype (string reference to matrix type)
```

Storage in `Property` model:
- `property_family` — database enum field
- `property_type` — lookup key into PROPERTY_TYPES registry
- `property_subtype` — stored in `metadata_json`

---

## 6. Per-Type Specific Fields

Rather than a single generic field set, each property family defines its own specific fields stored in `metadata_json`.

### 6.1 Land-Specific Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `title_status` | Enum | `titre_foncier`, `titre_terrain`, `sans_titre`, `coutumier`, `indivision`, `en_cours` | Legal title status |
| `is_constructible` | Boolean | — | Whether land can be built on |
| `lot_size` | Decimal | — | Lot size in m² |
| `zoning` | String | — | Zoning classification |
| `servitude` | String | — | Easements |
| `acces_route` | Boolean | — | Road access |
| `raccordement_eau` | Boolean | — | Water connection |
| `raccordement_electricite` | Boolean | — | Electricity connection |
| `loti` | Boolean | — | Whether serviced |
| `coefficient_occupation_sol` | Decimal | — | Floor area ratio |

### 6.2 Industrial-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `access_camion` | Boolean | Truck access |
| `hauteur_plafond` | Decimal | Ceiling height (m) |
| `charge_sol` | Decimal | Floor load capacity (kg/m²) |
| `puissance_electrique` | String | Electrical capacity |
| `quai_chargement` | Boolean | Loading dock |
| `parking_poids_lourds` | Boolean | Heavy vehicle parking |
| `pont_roulant` | Boolean | Overhead crane |
| `alarme_incendie` | Boolean | Fire alarm |
| `extracteur_air` | Boolean | Air extraction |

### 6.3 Commercial-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `front_window` | Decimal | Storefront width (m) |
| `vitrine` | Boolean | Display window |
| `parking_clients` | Integer | Customer parking spaces |
| `superficie_commerciale` | Decimal | Commercial floor area (m²) |
| `hauteur_sous_plafond` | Decimal | Ceiling height |
| `sanitaires_clients` | Boolean | Customer restrooms |
| `acces_handicapes` | Boolean | Disabled access |
| `terrasse` | Boolean | Outdoor terrace |
| `enseigne` | Boolean | Signage allowed |
| `climatisation_commerciale` | Boolean | Commercial HVAC |

### 6.4 Residential-Specific Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `etage` | Integer | — | Floor number |
| `ascenseur` | Boolean | — | Elevator |
| `parking` | String | `none`, `street`, `garage`, `covered`, `multiple` | Parking type |
| `gardien` | Boolean | — | Security guard |
| `cuisine_equipee` | Boolean | — | Equipped kitchen |
| `climatisation` | String | `none`, `central`, `split`, `window` | AC type |
| `balcon` | Boolean | — | Balcony |
| `jardin` | Boolean | — | Garden |
| `piscine` | Boolean | — | Swimming pool |
| `groupe_electrogene` | Boolean | — | Generator |
| `citerme_eau` | Boolean | — | Water tank |
| `internet` | Boolean | — | Internet |
| `meuble` | Boolean | — | Furnished |
| `nombre_pieces` | Integer | — | Room count |
| `surface_habitable` | Decimal | — | Living area (m²) |

### 6.5 Agricultural-Specific Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `type_culture` | String | — | Crop type |
| `surface_exploitable` | Decimal | — | Farmable area (m²) |
| `source_eau` | String | `puit`, `forage`, `cours_eau`, `reseau`, `pluvial` | Water source |
| `acces_engins` | Boolean | — | Machinery access |
| `type_elevage` | String | — | Livestock type |
| `infrastructure_existante` | String | — | Existing infrastructure |

### 6.6 Hotel-Specific Fields

| Field | Type | Description |
|-------|------|-------------|
| `nombre_chambres` | Integer | Room count |
| `etoiles` | Integer | Star rating |
| `restaurant_interne` | Boolean | On-site restaurant |
| `piscine_hotel` | Boolean | Hotel pool |
| `salle_conference` | Boolean | Conference room |
| `parking_hotel` | Integer | Parking capacity |

### 6.7 Project-Specific Fields

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `nombre_logements` | Integer | — | Housing units planned |
| `date_livraison` | DateTime | — | Expected delivery |
| `phase_projet` | String | `conception`, `chantier`, `finition`, `livre` | Project phase |
| `promoteur` | String | — | Developer name |
| `permis_construire` | Boolean | — | Building permit |

### 6.8 Verification Requirements Per Family

| Family | Required Documents | Checks |
|--------|-------------------|--------|
| **land** | title_deed_or_proof, owner_id, tax_receipt | title_status_verification, cadastral_reference_match, ownership_chain |
| **residential** | owner_id, property_title, tax_receipt | ownership_verification, property_visit_confirmation |
| **commercial** | owner_id, commercial_license, property_title, tax_receipt | ownership_verification, commercial_zoning_check |
| **industrial** | owner_id, industrial_permit, property_title, environmental_clearance | ownership_verification, industrial_zoning_check, environmental_compliance |
| **agricultural** | owner_id, land_title, agricultural_permit | ownership_verification, agricultural_zoning_check |
| **hotel** | owner_id, hotel_license, property_title, health_certificate | ownership_verification, hospitality_license_verification |
| **project** | developer_id, building_permit, land_title, project_approval | developer_verification, permit_validation, project_feasibility |

---

## 7. Price Model

The price model consists of 6 price levels and 7 price types, replacing the current V2 `price_min`/`price_max` range-only model.

### 7.1 Six Price Levels

| Level | Field | Gold Source | Required | Type | Description |
|-------|-------|-------------|----------|------|-------------|
| 1 | `price_displayed` | Prix affiché (GOLD-PR-070) | Yes | Decimal | Single displayed/listed price |
| 2 | `price_negotiable` | Prix négociable (GOLD-PR-071) | No | Decimal | Negotiable price if different |
| 3 | `price_final` | Prix final (GOLD-PR-072) | No | Decimal | Final agreed transaction price |
| 4 | `price_estimation` | Estimation (GOLD-PR-073) | No | Decimal | Estimated market value |
| 5 | `price_min`/`price_max` | Fourchette (GOLD-PR-074) | No | Decimal | Market price range (retained from V2) |
| 6 | `price_history` | Historique (GOLD-PR-075) | No | JSON[] | Historical price variation data |

### 7.2 Seven Price Types

| Type | Field | Gold Source | Applicable Transactions |
|------|-------|-------------|------------------------|
| 1 | `rent` | Loyer (GOLD-PR-076) | rent, lease, commercial_lease, short_stay |
| 2 | `sale` | Vente | sale, investment |
| 3 | `deposit` | Dépôt de garantie (GOLD-PR-079) | rent, lease, short_stay |
| 4 | `guarantee` | Caution (GOLD-PR-077) | rent, lease |
| 5 | `monthly` | Mensualité (GOLD-PR-080) | sale, investment |
| 6 | `fees` | Frais de service (GOLD-PR-081) | rent, sale, lease |
| 7 | `taxes` | Taxes (GOLD-PR-082) | rent, sale, lease, commercial_lease |

### 7.3 Price Model Implementation

```typescript
interface PriceModel {
  price_displayed: Decimal;      // Required — primary displayed price
  price_negotiable?: Decimal;    // Optional — negotiable price
  price_final?: Decimal;         // Optional — set after transaction
  price_estimation?: Decimal;    // Optional — estimated value
  price_min?: Decimal;           // Retained from V2
  price_max?: Decimal;           // Retained from V2
  negotiable: Boolean;           // Whether price is negotiable
  price_type: PriceTypeEnum;     // rent | sale | deposit | guarantee | monthly | fees | taxes
  price_history?: PriceRecord[]; // Historical price records
}

interface PriceRecord {
  amount: Decimal;
  type: PriceTypeEnum;
  recorded_at: DateTime;
  source: string;  // user | system | estimation
  notes?: string;
}
```

---

## 8. Property Lifecycle

The 10-step property lifecycle replaces the current V2 5-status model, covering the full enrichment and commercial pipeline.

### 8.1 Lifecycle States

| Step | State | Gold Name | Description | Allowable Previous | Allowable Next |
|------|-------|-----------|-------------|-------------------|----------------|
| 1 | `creation` | Réception | Initial reception of property data | — | normalization |
| 2 | `normalization` | Normalisation | Data normalization and cleansing | creation | classification, creation |
| 3 | `classification` | Classification | Family and type assignment | normalization | validation, normalization |
| 4 | `validation` | Validation | Consistency and completeness checks | classification | published, classification |
| 5 | `published` | Publication | Published and publicly visible | validation | matching, archived, validation |
| 6 | `matching` | Matching | Active in matching engine | published | mise_en_relation, published, archived |
| 7 | `mise_en_relation` | Mise en relation | Contact established | matching | suivi, matching, archived |
| 8 | `suivi` | Suivi | Transaction follow-up | mise_en_relation | archived, conserve, mise_en_relation |
| 9 | `archived` | Archivage | Archived after completion or inactivity | published, matching, mise_en_relation, suivi | conserve, published |
| 10 | `conserve` | Conservation | Historical preservation (terminal) | suivi, archived | — |

### 8.2 State Transition Diagram

```
creation → normalization → classification → validation → published → matching → mise_en_relation → suivi → archived → conserve
  │            │                │               │              │           │              │           │
  │            └→ creation      │               │              │           │              │           │
  │                             └→ normalization │              │           │              │           │
  │                                               └→ classification │           │              │           │
  │                                                                 └→ validation │              │           │
  │                                                                               └→ published    │           │
  │                                                                                             └→ matching   │
  │                                                                                                           └→ archived
```

---

## 9. Publication Rules

Eight publication validation rules gate the transition from `validation` to `published` state.

| # | Rule | Gold ID | Severity | V2 Status | Description |
|---|------|---------|----------|-----------|-------------|
| 1 | **Family check** | GOLD-PR-062 | Critical | UNMAPPED | `property_family` must be set to a valid family |
| 2 | **Type check** | GOLD-PR-063 | Critical | UNMAPPED | `property_type` must be valid and consistent with family |
| 3 | **Location check** | GOLD-PR-064 | Critical | MAPPED | City + neighborhood required |
| 4 | **Price check** | GOLD-PR-065 | Critical | PARTIAL | At least `price_displayed` > 0 |
| 5 | **Holder check** | GOLD-PR-066 | High | UNMAPPED | `owner_id` must be a verified user |
| 6 | **Normalization check** | GOLD-PR-067 | High | UNMAPPED | Critical info fields must pass normalization |
| 7 | **Documents check** | GOLD-PR-068 | High | UNMAPPED | Required documents per type must be uploaded |
| 8 | **Reference code check** | GOLD-PR-069 | Medium | UNMAPPED | SIE reference code must be generated |

### 9.1 Publication Check Implementation

```typescript
function canPublish(property: Property): PublicationResult {
  const rules: PublicationRule[] = [
    { check: () => property.family !== null,                    rule: 1, severity: 'critical' },
    { check: () => isValidType(property.family, property.type), rule: 2, severity: 'critical' },
    { check: () => property.city && property.neighborhood,      rule: 3, severity: 'critical' },
    { check: () => property.price_displayed > 0,                rule: 4, severity: 'critical' },
    { check: () => property.owner_verified,                     rule: 5, severity: 'high' },
    { check: () => isNormalized(property),                      rule: 6, severity: 'high' },
    { check: () => hasRequiredDocuments(property),              rule: 7, severity: 'high' },
    { check: () => property.sie_code !== null,                  rule: 8, severity: 'medium' },
  ];

  return evaluatePublicationRules(rules);
}
```

---

## 10. Data Quality Scoring

A quality scoring engine evaluates each property on completeness and source reliability.

### 10.1 Scoring Formula

```
quality_score = int(completeness × 0.6 + reliability × 0.4)
```

### 10.2 Completeness Dimensions (60%)

| Field | Weight | Description |
|-------|--------|-------------|
| Title | 10% | Property title present |
| Description | 15% | Description present with sufficient length |
| Price | 15% | Price information provided |
| Location | 15% | City and neighborhood provided |
| Type | 15% | Family and type specified |
| Images | 15% | At least one image uploaded |
| Contact | 15% | Contact information provided |

### 10.3 Source Reliability (40%)

| Source | Score |
|--------|-------|
| Agent | 90 |
| Google Form | 85 |
| Dashboard | 85 |
| API | 75 |
| Import | 70 |
| WhatsApp | 50 |
| Telegram | 50 |
| Unknown | 30 |

### 10.4 Grading Scale

| Grade | Min Score | Description |
|-------|-----------|-------------|
| A+ | ≥ 80 | Excellent quality |
| A | ≥ 60 | Good quality |
| B | ≥ 40 | Average quality |
| C | ≥ 20 | Below average quality |
| D | < 20 | Poor quality — needs improvement |

### 10.5 Storage

```typescript
interface DataQuality {
  quality_score: Float;    // 0-100
  quality_grade: String;   // A+ | A | B | C | D
  completeness: Float;     // 0-100
  reliability: Float;      // 0-100
  source: String;          // Data source identifier
}
```

---

## 11. Availability State Machine

A finite state machine enforces valid availability transitions with guarded rules.

### 11.1 States

| State | Description |
|-------|-------------|
| `available` | Property is available for transaction |
| `pending` | Reserved or under negotiation |
| `rented` | Property has been rented |
| `sold` | Property has been sold |
| `archived` | No longer active on the market |

### 11.2 Transition Matrix

```
available ──► pending ──► rented ──► archived
  │            │  │         │
  │            │  └──► sold ────► archived
  │            │
  └──► archived  └──► available
```

### 11.3 Guarded Transitions

| From | To | Guard |
|------|----|-------|
| `available` | `pending` | Reservation or negotiation initiated |
| `available` | `archived` | Owner request or 90-day inactivity |
| `pending` | `available` | Reservation cancelled |
| `pending` | `rented` | Rental agreement signed |
| `pending` | `sold` | Sale completed |
| `pending` | `archived` | Deal failed or withdrawn |
| `rented` | `archived` | Lease ended |
| `rented` | `available` | Lease terminated early |
| `sold` | `archived` | Sale finalized |
| `archived` | `available` | Relisted by owner |

---

## 12. Auto-Archive (90-Day Rule)

Properties with no activity for 90 consecutive days are automatically archived.

### 12.1 Rule Definition

| Aspect | Detail |
|--------|--------|
| **Trigger** | `last_activity_at` + 90 days without new activity |
| **Action** | Move property lifecycle to `archived` state |
| **Notification** | Notify owner 7 days before auto-archive |
| **Exclusions** | Properties in `suivi` or `conserve` state |
| **Check frequency** | Daily (cron job) |
| **Gold Source** | PROPERTY_TYPE_CROSSWALK.md §7 (GAP-006) |

### 12.2 Required Fields

```
Property {
  last_activity_at: DateTime   // Timestamp of last property activity
  expires_at: DateTime         // Auto-archive date = last_activity_at + 90 days
}
```

### 12.3 Re-activation

Property can be re-activated from `archived` state by owner action (transition to `available`), which resets `last_activity_at` and `expires_at`.

---

## 13. Complete Extension Table

All property model extensions from `required_extensions.json` with enriched fields:

| ID | Concept | Priority | Source | Proposed Target | Human Decision |
|----|---------|----------|--------|-----------------|----------------|
| EXT-PROP-001 | 7 property families + sub-referentials | **P0** | GOLD-PR-001-007 | Add `property_family` enum with 7 values | No |
| EXT-PROP-002 | Property type hierarchy (11 basic + 41 matrix) | **P0** | GOLD-PR-034-044 | Create PROPERTY_TYPES registry; subtype in `metadata_json` | No |
| EXT-PROP-003 | 107 qualification matrices | P2 | MATRIX_CATALOG.md | Link types to qualification matrix catalog | No |
| EXT-PROP-004 | 10-step property lifecycle | P1 | PROPERTY_TYPE_CROSSWALK §3 | Extend state machine from 5 to 10+ states | Yes |
| EXT-PROP-005 | 8 publication rules | P1 | GOLD-PR-062-069 | Expand `can_publish()` from 3 to 8 rules | No |
| EXT-PROP-006 | 6 price levels | P1 | GOLD-PR-070-075 | Add `price_displayed`, negotiable, final, estimation fields | Yes |
| EXT-PROP-007 | 7 price types | P2 | GOLD-PR-076-082 | Add price type classification; typed prices in `metadata_json` | Yes |
| EXT-PROP-008 | Data quality scoring | P2 | PROPERTY_TYPE_CROSSWALK §6 | Implement scoring engine with completeness + reliability | Yes |
| EXT-PROP-009 | Per-type specific fields | P1 | GAP-010 | Add per-family field schemas in `metadata_json` | Yes |
| EXT-PROP-010 | Availability state machine | P2 | PROPERTY_TYPE_CROSSWALK §3 | Implement guarded transition FSM | No |
| EXT-PROP-011 | Auto-archive 90-day rule | P2 | GAP-006 | Implement cron job for inactivity archiving | Yes |
| EXT-PROP-012 | Investment types (5) | P3 | CW-INV-001-005 | Add investment-specific fields and workflows | No |
| EXT-PROP-013 | Agricultural family | P3 | GOLD-PR-005 | Add agricultural to family enum + sub-referentiel | No |
| EXT-PROP-014 | Hotelier family | P3 | GOLD-PR-006 | Add hotel to family enum; map commercial.hotel | No |
| EXT-PROP-015 | Real estate project family | P3 | GOLD-PR-007 | Add project family; link Property to Project | Yes |

### 13.1 Implementation Phases

| Phase | Focus | Extensions | Effort |
|-------|-------|-----------|--------|
| **Phase 0: Foundation** | Families, types, basic state machine | EXT-PROP-001, EXT-PROP-002, EXT-PROP-004 | 2-3 weeks |
| **Phase 1: Core Business** | Publication, pricing, per-type fields | EXT-PROP-005, EXT-PROP-006, EXT-PROP-009 | 8-12 weeks |
| **Phase 2: Operations** | — | — | 6-8 weeks |
| **Phase 3: Analytics** | Quality scoring, availability, auto-archive | EXT-PROP-008, EXT-PROP-010, EXT-PROP-011 | 4-6 weeks |
| **Phase 4: Enhancement** | Investment, agricultural, hotel, project | EXT-PROP-012, EXT-PROP-013, EXT-PROP-014, EXT-PROP-015 | 4-6 weeks |

### 13.2 Cross-References

| Domain | Reference | Description |
|--------|-----------|-------------|
| Qualification Matrices | EXT-QUAL-* | 107 matrices across all property types |
| Matching Engine | EXT-MAT-* | 5 scoring dimensions, 9 matching roles |
| Publication Workflow | EXT-WF-009 | SIE-enriched publication pipeline |
| Transaction Types | EXT-TRX-* | Transaction type alignment with property families |
| Data Quality | EXT-PROP-008 | Quality scoring engine |

---

*End of PROPERTY_TAXONOMY_EXTENSION_MODEL.md*
