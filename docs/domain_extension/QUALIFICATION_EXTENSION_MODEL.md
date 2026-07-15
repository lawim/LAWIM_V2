# QUALIFICATION EXTENSION MODEL

**Document ID:** LAWIM-H13-QUAL-V1
**Status:** CANONICAL DOMAIN EXTENSION
**Date:** 2026-07-15
**Extends:** LAWIM_UNIFIED_DOMAIN_MODEL.md §6 (Dossier/Project Model), §7 (Matching Engine)
**Source Crosswalks:** required_extensions.json (qualification_engine), MATRIX_CATALOG.md (Gold), QUALIFICATION_MODEL.md (Gold)

---

## Table of Contents

1. [Conceptual Architecture](#1-conceptual-architecture)
2. [Entity: QualificationMatrixDefinition](#2-entity-qualificationmatrixdefinition)
3. [Entity: QualificationFieldDefinition](#3-entity-qualificationfielddefinition)
4. [Entity: QualificationRuleDefinition](#4-entity-qualificationruledefinition)
5. [Entity: ReadinessDefinition](#5-entity-readinessdefinition)
6. [Entity: QuestionRuleDefinition](#6-entity-questionruledefinition)
7. [Entity: MatchingSemanticDefinition](#7-entity-matchingsemanticdefinition)
8. [Entity: MatrixVersion](#8-entity-matrixversion)
9. [Entity: MatrixApplicability](#9-entity-matrixapplicability)
10. [107 Matrix Catalog by Domain](#10-107-matrix-catalog-by-domain)
11. [Field Dictionary with Matching Roles](#11-field-dictionary-with-matching-roles)
12. [Question Priority System](#12-question-priority-system)
13. [10-Step Progressive Qualification Order](#13-10-step-progressive-qualification-order)
14. [Per-Channel Adaptation](#14-per-channel-adaptation)
15. [Matrix Versioning Strategy](#15-matrix-versioning-strategy)
16. [Matrix Applicability Rules](#16-matrix-applicability-rules)
17. [Complete Extension Mapping Table](#17-complete-extension-mapping-table)

---

## 1. Conceptual Architecture

The qualification extension model treats the 107 Heritage Gold qualification matrices as **versioned, configurable metadata** — not rigid database columns. Each matrix is a collection of field definitions, question rules, matching semantics, and applicability constraints that drive the progressive qualification of a user's dossier.

### 1.1 Design Principles

| Principle | Description |
|-----------|-------------|
| **Metadata-driven** | Matrices are defined as data, not schema. Adding a new matrix requires zero migrations. |
| **Versioned** | Every matrix tracks its version history. Active dossiers continue using the version they were qualified under. |
| **Channel-adaptive** | The same matrix renders differently per channel (WhatsApp, Telegram, Dashboard). |
| **Progressive** | Questions are asked in a strict 10-step order; later questions depend on earlier answers. |
| **Role-mapped** | Each field declares which matching role it feeds into (hard_constraint, strong_preference, etc.). |

### 1.2 Entity Relationship Map

```
QualificationMatrixDefinition
  ├── has N QualificationFieldDefinition
  │     └── each field declares QuestionRuleDefinition (priority, channel, step)
  │     └── each field declares MatchingSemanticDefinition (matching_role, weight)
  ├── has N QualificationRuleDefinition (pre-conditions, post-conditions)
  ├── has N ReadinessDefinition (what makes a dossier ready for this matrix)
  ├── belongs to MatrixVersion (version history)
  └── has N MatrixApplicability (when this matrix applies)
        └── references: request_family, transaction_type, property_type,
                        service_type, requester_typology, journey_stage
```

### 1.2 Qualification Data (Dossier-level, not schema-level)

Qualification answers are stored as a JSON document on the Project/Dossier entity — not as separate Prisma columns per field.

| Attribute | Type | Description |
|-----------|------|-------------|
| `project.qualification_matrix_id` | UUID? | Reference to active QualificationMatrixDefinition |
| `project.qualification_version` | String? | Matrix version snapshot at time of qualification |
| `project.qualification_data` | JSON | Key-value store of field_id → answer |
| `project.qualification_step` | Int (1-10) | Current step in progressive qualification |
| `project.qualification_completed_at` | DateTime? | When qualification was finalized |
| `project.readiness_score` | Float? | Computed readiness score (0-100) |

---

## 2. Entity: QualificationMatrixDefinition

Represents one of the 107 qualification matrices. This is the core entity — a named, versioned collection of fields and rules.

### 2.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `matrix_code` | String | Unique code (e.g., `RES-APT-BUY`, `LND-PLT-INV`) |
| `name` | String | Display name (e.g., "Recherche Appartement Achat") |
| `domain` | Enum | `residential \| land \| commercial \| investment \| financing \| professional \| service` |
| `family_code` | String | Domain grouping code (e.g., `RES`, `LND`, `COM`, `INV`, `FIN`, `PRO`, `SVC`) |
| `description` | Text | Business description of the matrix purpose |
| `version` | String | Current semantic version (e.g., `1.2.0`) |
| `status` | Enum | `draft \| active \| deprecated \| retired` |
| `is_default_for_family` | Boolean | Whether this is the default matrix when no specific match found |
| `field_count` | Int | Number of field definitions in this matrix (denormalized) |
| `applicable_steps` | Int[] | Which of the 10 progressive steps this matrix covers |
| `estimated_completion_minutes` | Int | Estimated time to complete (dashboard mode) |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last modification timestamp |
| `deprecated_at` | DateTime? | When this matrix was deprecated |
| `superseded_by_id` | UUID? | Newer matrix that replaces this one |

### 2.2 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| QualificationFieldDefinition | 1:N | Fields belonging to this matrix |
| QualificationRuleDefinition | 1:N | Rules for this matrix |
| ReadinessDefinition | 1:N | Readiness requirements |
| MatrixVersion | 1:N | Version history entries |
| MatrixApplicability | 1:N | Applicability rules |
| Project | 1:N | Projects qualified using this matrix |

---

## 3. Entity: QualificationFieldDefinition

A single field/question within a qualification matrix. Fields are the atomic unit of qualification.

### 3.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `matrix_id` | UUID | Parent matrix |
| `field_code` | String | Unique field code (e.g., `budget_min`, `surface_min`, `furnished`) |
| `label` | JSON | Multilingual label `{fr: "...", en: "..."}` |
| `description` | JSON | Multilingual help text |
| `field_type` | Enum | `text \| number \| decimal \| boolean \| enum \| multiselect \| date \| location \| range` |
| `enum_values` | JSON? | Allowed values for enum/multiselect types `[{value, label_fr, label_en}]` |
| `unit` | String? | Unit label (e.g., `m²`, `FCFA`, `rooms`) |
| `validation_rules` | JSON | Validation constraints `{min, max, required, pattern, depends_on}` |
| `placeholder` | JSON? | Multilingual placeholder text |
| `display_hint` | JSON? | Multilingual display hint |
| `sort_order` | Int | Display order within the matrix |
| `step_number` | Int (1-10) | Which progressive step this field belongs to |
| `priority` | Enum | `mandatory \| important \| optional` |
| `matching_role` | Enum | `hard_constraint \| strong_preference \| weak_preference \| nice_to_have \| deal_breaker \| tie_breaker \| exclusion \| boost \| transaction_blocker` |
| `matching_weight` | Float? | Weight factor for matching (0.0-1.0) |
| `is_visible_on_whatsapp` | Boolean | Whether this field is asked on WhatsApp |
| `is_visible_on_telegram` | Boolean | Whether this field is asked on Telegram |
| `is_visible_on_dashboard` | Boolean | Whether this field is shown on Dashboard (default true) |
| `whatsapp_question_limit` | Int | Max questions per WhatsApp interaction (default 1) |
| `telegram_question_limit` | Int | Max questions per Telegram interaction (default 2-3) |
| `dashboard_question_limit` | Int | Max questions per Dashboard step (default unlimited) |
| `group_name` | String? | Logical grouping (e.g., `location`, `budget`, `features`) |
| `depends_on_field_id` | UUID? | Conditional: only ask if parent field has specific value |
| `depends_on_value` | JSON? | Required value of parent field |
| `is_active` | Boolean | Whether this field is currently active |
| `created_at` | DateTime | Creation timestamp |

### 3.2 Relationships

| Entity | Cardinality | Description |
|--------|-------------|-------------|
| QualificationMatrixDefinition | N:1 | Parent matrix |
| QualificationFieldDefinition (self) | 0:1 | Conditional dependency on another field |

---

## 4. Entity: QualificationRuleDefinition

Business rules that govern the qualification flow — pre-conditions, post-conditions, skip logic, and escalation triggers.

### 4.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `matrix_id` | UUID | Parent matrix |
| `rule_code` | String | Unique rule code (e.g., `BUDGET_MIN_MAX`, `LOCATION_REQUIRED`) |
| `rule_type` | Enum | `pre_condition \| post_condition \| skip_logic \| validation \| escalation \| default_value` |
| `condition_expression` | JSON | Machine-readable condition (field, operator, value) |
| `action` | JSON | Action to take when condition is met |
| `error_message` | JSON? | Multilingual error message |
| `sort_order` | Int | Evaluation order |
| `is_active` | Boolean | Whether the rule is active |

### 4.2 Rule Examples

| Rule Code | Type | Condition | Action |
|-----------|------|-----------|--------|
| `BUDGET_MIN_MAX` | validation | `budget_min > budget_max` | Show error: "Budget minimum cannot exceed maximum" |
| `LOCATION_REQUIRED` | pre_condition | `city is empty` | Skip to step 3 (Ville) |
| `SURFACE_OPTIONAL_RENT` | skip_logic | `transaction_type = rent AND surface not provided` | Default surface = "Not specified" |
| `ESCALATE_INCOMPLETE` | escalation | `steps 1-9 complete AND confirmation = false` | Trigger escalation to agent |

---

## 5. Entity: ReadinessDefinition

Defines what makes a dossier/project ready to be qualified against a specific matrix. Used to determine which matrix to apply when multiple are eligible.

### 5.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `matrix_id` | UUID | Parent matrix |
| `readiness_criteria` | JSON | Conditions that must be met |
| `minimum_answers_required` | Int | Minimum answers before readiness is achieved |
| `required_fields` | String[] | Field codes that must be answered |
| `optional_fields` | String[] | Field codes that are helpful but not required |
| `readiness_score_formula` | String | Formula to compute readiness percentage |
| `is_active` | Boolean | Whether this readiness definition is active |

---

## 6. Entity: QuestionRuleDefinition

Controls how questions are rendered and sequenced per channel.

### 6.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `field_id` | UUID | Associated field definition |
| `channel` | Enum | `whatsapp \| telegram \| dashboard \| api` |
| `question_template` | JSON | Multilingual question text template |
| `response_type` | Enum | `free_text \| single_choice \| multiple_choice \| number \| yes_no \| location_picker \| date_picker` |
| `max_questions_per_interaction` | Int | Max questions to ask in a single interaction |
| `min_answers_before_proceed` | Int | Min answers needed before advancing step |
| `allow_skip` | Boolean | Whether the user can skip this question |
| `skip_label` | JSON? | Multilingual skip option label |
| `auto_advance` | Boolean | Whether to auto-advance after answer |
| `confirmation_required` | Boolean | Whether answer needs user confirmation |
| `retry_on_invalid` | Boolean | Whether to retry on invalid input |
| `max_retries` | Int | Maximum retry attempts |

---

## 7. Entity: MatchingSemanticDefinition

Maps each qualification field to its role in the matching engine. This is the bridge between qualification and matching.

### 7.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `field_id` | UUID | Associated field definition |
| `matching_role` | Enum | `hard_constraint \| strong_preference \| weak_preference \| nice_to_have \| deal_breaker \| tie_breaker \| exclusion \| boost \| transaction_blocker` |
| `weight` | Float (0.0-1.0) | Weight within its matching role category |
| `scoring_function` | Enum | `exact_match \| range_match \| fuzzy_match \| boolean_match \| enum_match \| geographic_distance` |
| `boost_value` | Int? | Boost value if role is `boost` |
| `penalty_value` | Int? | Penalty value if mismatch (negative) |
| `is_filter` | Boolean | Whether this field acts as a pre-filter before scoring |
| `filter_operator` | Enum? | `equals \| contains \| range \| any_of \| all_of \| not` |
| `exclusion_values` | JSON[]? | Values that cause exclusion |

### 7.2 Matching Role Mapping

| Matching Role | Qualification Use Case | Scoring Behavior |
|---------------|----------------------|------------------|
| `hard_constraint` | Budget range, location city | Binary pass/fail; mismatch = 0 score |
| `strong_preference` | Property type, bedrooms count | Heavily weighted (0.7-1.0 factor) |
| `weak_preference` | Floor level, parking | Lightly weighted (0.3-0.6 factor) |
| `nice_to_have` | Furnished, balcony | Bonus only (+5-15) if present |
| `deal_breaker` | Title deed status (land) | Any mismatch → match rejected entirely |
| `tie_breaker` | Response time, profile completeness | Only used when overall scores within 5% |
| `exclusion` | Property with known issues | Presence explicitly excludes match |
| `boost` | Urgent demandeur, complete dossier | Applied after base scoring (+10-20) |
| `transaction_blocker` | Legal document requirements | Blocks proceed if conditions not met |

---

## 8. Entity: MatrixVersion

Tracks the version history of every qualification matrix. Enables snapshot-based qualification to ensure consistency.

### 8.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `matrix_id` | UUID | Reference to QualificationMatrixDefinition |
| `version` | String | Semantic version (e.g., `1.0.0`, `1.1.0`, `2.0.0`) |
| `version_type` | Enum | `major \| minor \| patch` |
| `snapshot` | JSON | Complete matrix definition frozen at this version (fields, rules, applicability) |
| `change_log` | Text | Description of what changed in this version |
| `supersedes_version` | String? | Previous version this replaces |
| `is_active_snapshot` | Boolean | Whether this is the currently active version |
| `created_by` | UUID | Admin who created this version |
| `created_at` | DateTime | Version creation timestamp |
| `activated_at` | DateTime? | When this version became active |
| `deprecated_at` | DateTime? | When this version was deprecated |

### 8.2 Versioning Rules

| Change Type | Version Bump | Effect |
|-------------|-------------|--------|
| Add new optional field | Patch (1.0.0 → 1.0.1) | Existing dossiers unaffected |
| Add new mandatory field | Minor (1.0.0 → 1.1.0) | Existing dossiers grandfathered; new dossiers must answer |
| Remove field | Minor (1.0.0 → 1.1.0) | Existing answers preserved but field no longer asked |
| Change field priority | Patch (1.0.0 → 1.0.1) | Re-ordering only; no data impact |
| Change matching role/weight | Minor (1.0.0 → 1.1.0) | Matching recalculated for active dossiers |
| Restructure matrix entirely | Major (1.0.0 → 2.0.0) | New matrix version; old dossiers optionally re-qualified |
| Deprecate matrix | Version frozen | No new dossiers; existing continue with frozen snapshot |

---

## 9. Entity: MatrixApplicability

Defines when a specific qualification matrix applies based on cross-cutting dimensions.

### 9.1 Key Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Primary identifier |
| `matrix_id` | UUID | Reference to QualificationMatrixDefinition |
| `request_family` | Enum? | `property_search \| professional_find \| service_request \| financing_request \| investment_analysis` |
| `transaction_type` | Enum? | `buy \| rent \| sell \| invest \| lease \| short_stay \| commercial_lease \| business_transfer \| finance \| find \| service` |
| `property_type` | String? | Specific property type code (e.g., `apartment`, `house`, `land`, `commercial`) |
| `property_family` | Enum? | `residential \| commercial \| industrial \| land \| agricultural \| hotel \| project` |
| `service_type` | String? | Specific service code for service-request matrices |
| `requester_typology` | Enum? | `individual \| professional \| investor \| diaspora \| agency \| enterprise` |
| `journey_stage` | Enum? | `discovery \| qualification \| matching \| negotiation \| transaction` |
| `priority` | Int | When multiple matrices match, highest priority wins |
| `is_default` | Boolean | Whether this is the fallback default for its dimensions |

### 9.2 Applicability Dimensions

| Dimension | Values | Example |
|-----------|--------|---------|
| `request_family` | property_search, professional_find, service_request, financing_request, investment_analysis | `property_search` for residential buy |
| `transaction_type` | buy, rent, sell, invest, lease, short_stay, commercial_lease, business_transfer, finance, find, service | `buy` for apartment purchase |
| `property_type` | apartment, house, villa, studio, land, commercial, office, warehouse, hotel | `apartment` for RES-APT-BUY |
| `property_family` | residential, commercial, industrial, land, agricultural, hotel, project | `residential` for RES-* matrices |
| `service_type` | estimation, expertise, photography, legal, notary, etc. | `estimation` for SVC-EST-* |
| `requester_typology` | individual, professional, investor, diaspora, agency, enterprise | `individual` for standard search |
| `journey_stage` | discovery, qualification, matching, negotiation, transaction | `qualification` for initial data collection |

---

## 10. 107 Matrix Catalog by Domain

### 10.1 Residential (18 matrices)

| Code | Name | Transaction Types | Property Types |
|------|------|-------------------|----------------|
| RES-APT-BUY | Recherche Appartement Achat | buy | apartment |
| RES-APT-RENT | Recherche Appartement Location | rent | apartment |
| RES-HOU-BUY | Recherche Maison Achat | buy | house |
| RES-HOU-RENT | Recherche Maison Location | rent | house |
| RES-VIL-BUY | Recherche Villa Achat | buy | villa |
| RES-VIL-RENT | Recherche Villa Location | rent | villa |
| RES-STU-BUY | Recherche Studio Achat | buy | studio |
| RES-STU-RENT | Recherche Studio Location | rent | studio |
| RES-DUP-BUY | Recherche Duplex Achat | buy | duplex |
| RES-DUP-RENT | Recherche Duplex Location | rent | duplex |
| RES-PEN-BUY | Recherche Penthouse Achat | buy | penthouse |
| RES-PEN-RENT | Recherche Penthouse Location | rent | penthouse |
| RES-CHM-RENT | Recherche Chambre Location | rent | room |
| RES-RES-BUY | Recherche Résidence Achat | buy | residence |
| RES-RES-RENT | Recherche Résidence Location | rent | residence |
| RES-CONDO-BUY | Recherche Condominium Achat | buy | condominium |
| RES-CONDO-RENT | Recherche Condominium Location | rent | condominium |
| RES-OTH-RENT | Recherche Autre Logement Location | rent | other_residential |

### 10.2 Land (7 matrices)

| Code | Name | Transaction Types | Property Types |
|------|------|-------------------|----------------|
| LND-PLT-BUY | Recherche Terrain Achat | buy | plot |
| LND-PLT-INV | Recherche Terrain Investissement | invest | plot |
| LND-AGR-BUY | Recherche Terrain Agricole Achat | buy | agricultural_land |
| LND-AGR-INV | Recherche Terrain Agricole Investissement | invest | agricultural_land |
| LND-COM-BUY | Recherche Terrain Commercial Achat | buy | commercial_land |
| LND-COM-INV | Recherche Terrain Commercial Investissement | invest | commercial_land |
| LND-IND-BUY | Recherche Terrain Industriel Achat | buy | industrial_land |

### 10.3 Commercial (21 matrices)

| Code | Name | Transaction Types | Property Types |
|------|------|-------------------|----------------|
| COM-OFF-BUY | Recherche Bureau Achat | buy | office |
| COM-OFF-RENT | Recherche Bureau Location | rent | office |
| COM-SHP-BUY | Recherche Local Commercial Achat | buy | shop |
| COM-SHP-RENT | Recherche Local Commercial Location | rent | shop |
| COM-WRH-BUY | Recherche Entrepôt Achat | buy | warehouse |
| COM-WRH-RENT | Recherche Entrepôt Location | rent | warehouse |
| COM-RES-BUY | Recherche Résidence Commerciale Achat | buy | commercial_residence |
| COM-RES-RENT | Recherche Résidence Commerciale Location | rent | commercial_residence |
| COM-HOT-BUY | Recherche Hôtel Achat | buy | hotel |
| COM-HOT-RENT | Recherche Hôtel Location | rent | hotel |
| COM-GAR-BUY | Recherche Parking/Box Achat | buy | garage |
| COM-GAR-RENT | Recherche Parking/Box Location | rent | garage |
| COM-LAN-BUY | Recherche Hangar Achat | buy | hangar |
| COM-LAN-RENT | Recherche Hangar Location | rent | hangar |
| COM-LAB-BUY | Recherche Laboratoire Achat | buy | laboratory |
| COM-LAB-RENT | Recherche Laboratoire Location | rent | laboratory |
| COM-CLB-BUY | Recherche Club/Salle Achat | buy | club_hall |
| COM-CLB-RENT | Recherche Club/Salle Location | rent | club_hall |
| COM-COM-BUY | Recherche Local Commercial Multi Achat | buy | commercial_multi |
| COM-COM-RENT | Recherche Local Commercial Multi Location | rent | commercial_multi |
| COM-COM-LEASE | Recherche Bail Commercial | commercial_lease | commercial |

### 10.4 Investment (5 matrices)

| Code | Name | Transaction Types | Property Types |
|------|------|-------------------|----------------|
| INV-RES-BUY | Investissement Résidentiel | invest | residential |
| INV-COM-BUY | Investissement Commercial | invest | commercial |
| INV-LND-BUY | Investissement Terrain | invest | land |
| INV-PRO-BUY | Investissement Promotion Immobilière | invest | project_development |
| INV-SYN-BUY | Investissement Syndicat Copropriété | invest | condominium_syndicate |

### 10.5 Financing (10 matrices)

| Code | Name | Transaction Types | Property Types |
|------|------|-------------------|----------------|
| FIN-MTG-BUY | Crédit Immobilier Achat | finance | any |
| FIN-MTG-CON | Crédit Immobilier Construction | finance | any |
| FIN-MTG-REN | Crédit Immobilier Rénovation | finance | any |
| FIN-PER-BUY | Prêt Personnel Immobilier | finance | any |
| FIN-LEA-BUY | Crédit-Bail Immobilier | finance | any |
| FIN-INV-BUY | Financement Investissement | finance | investment |
| FIN-CON-BUY | Prêt Construction | finance | any |
| FIN-BRI-BUY | Prêt Pont (Bridge Loan) | finance | any |
| FIN-TOP-BUY | Prêt Relais (Top-Up) | finance | any |
| FIN-SOC-BUY | Financement Social (logement social) | finance | social_housing |

### 10.6 Professional (27 matrices)

| Code | Name | Service Type | Description |
|------|------|--------------|-------------|
| PRO-AGE-FND | Recherche Agent Immobilier | agent_immobilier | Find real estate agent |
| PRO-NOT-FND | Recherche Notaire | notaire | Find notary |
| PRO-GEO-FND | Recherche Géomètre | geometre | Find surveyor |
| PRO-ARC-FND | Recherche Architecte | architecte | Find architect |
| PRO-ENG-FND | Recherche Ingénieur/Génie Civil | ingenieur_civil | Find civil engineer |
| PRO-ELE-FND | Recherche Électricien | electricien | Find electrician |
| PRO-PLM-FND | Recherche Plombier | plombier | Find plumber |
| PRO-MAC-FND | Recherche Maçon | macon | Find mason |
| PRO-MEN-FND | Recherche Menuisier | menuisier | Find carpenter |
| PRO-PEI-FND | Recherche Peintre | peintre | Find painter |
| PRO-CAR-FND | Recherche Carreleur | carreleur | Find tiler |
| PRO-COU-FND | Recherche Couvreur | couvreur | Find roofer |
| PRO-EXP-FND | Recherche Expert Immobilier | expert_immobilier | Find real estate expert |
| PRO-EVA-FND | Recherche Évaluateur | evaluateur | Find appraiser |
| PRO-SYN-FND | Recherche Syndic | syndic | Find condo manager |
| PRO-VID-FND | Recherche Vidéaste Drone | videaste_drone | Find drone videographer |
| PRO-COU-FND2 | Recherche Courtier | courtier | Find broker |
| PRO-GAR-FND | Recherche Gardiennage | gardiennage | Find security service |
| PRO-ADM-FND | Recherche Prestataire Administratif | prestataire_administratif | Find admin service provider |
| PRO-AVOCAT | Recherche Avocat | avocat | Find lawyer |
| PRO-COMPTA | Recherche Comptable | comptable | Find accountant |
| PRO-ASSU-FND | Recherche Assurance | assurance | Find insurance agent |
| PRO-BANQ-FND | Recherche Banquier | banquier | Find banker |
| PRO-PROM-FND | Recherche Promoteur Immobilier | promoteur | Find property developer |
| PRO-DECO-FND | Recherche Décorateur | decorateur | Find decorator |
| PRO-JARD-FND | Recherche Jardinier | jardinier | Find gardener |
| PRO-PISC-FND | Recherche Pisciniste | pisciniste | Find pool builder |

### 10.7 Service (24 matrices)

| Code | Name | Service Type | Description |
|------|------|--------------|-------------|
| SVC-EST-BUY | Demande d'Estimation | estimation | Property valuation request |
| SVC-EXP-REQ | Demande d'Expertise | expertise | Property inspection request |
| SVC-VER-REQ | Vérification Documentaire | verification_documentaire | Document verification |
| SVC-VIS-REQ | Demande de Visite | visite_property | Visit scheduling |
| SVC-CVIS-REQ | Demande de Contre-Visite | contre_visite | Second visit request |
| SVC-GLOC-REQ | Demande Gestion Locative | gestion_locative | Rental management request |
| SVC-MLOC-REQ | Demande Mise en Location | mise_en_location | Rental listing service |
| SVC-MVENT-REQ | Demande Mise en Vente | mise_en_vente | Sales listing service |
| SVC-PUB-REQ | Demande Publication | publication_service | Publication service |
| SVC-PHOT-REQ | Demande Photographie | photographie | Photography request |
| SVC-VID-REQ | Demande Vidéo | video_service | Videography request |
| SVC-DRON-REQ | Demande Drone | drone_service | Drone photography |
| SVC-HOME-REQ | Demande Home Staging | home_staging | Home staging request |
| SVC-RENO-REQ | Demande Rénovation | renovation_service | Renovation request |
| SVC-CONS-REQ | Demande Construction | construction_service | Construction request |
| SVC-ENT-REQ | Demande Entretien | entretien | Maintenance request |
| SVC-NET-REQ | Demande Nettoyage | nettoyage | Cleaning request |
| SVC-SEC-REQ | Demande Sécurisation | securisation | Security service |
| SVC-DEM-REQ | Demande Déménagement | demenagement | Moving request |
| SVC-ASS-REQ | Demande Assurance | assurance_service | Insurance referral |
| SVC-JUR-REQ | Demande Conseil Juridique | conseil_juridique | Legal advice request |
| SVC-FIS-REQ | Demande Conseil Fiscal | conseil_fiscal | Tax advice request |
| SVC-CPROP-REQ | Demande Gestion Copropriété | gestion_copropriete | Condo management request |
| SVC-REC-REQ | Demande Recouvrement Locatif | recouvrement_locatif | Rent recovery request |

---

## 11. Field Dictionary with Matching Roles

### 11.1 Core Fields (shared across matrices)

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `intention` | Intention | enum | hard_constraint | 1.0 | mandatory |
| `property_type` | Type de bien | enum | hard_constraint | 1.0 | mandatory |
| `city` | Ville | location | hard_constraint | 1.0 | mandatory |
| `neighborhood` | Quartier | location | strong_preference | 0.8 | important |
| `budget_min` | Budget minimum | number | hard_constraint | 1.0 | mandatory |
| `budget_max` | Budget maximum | number | hard_constraint | 1.0 | mandatory |
| `timeline` | Délai souhaité | enum | strong_preference | 0.7 | important |
| `surface_min` | Surface minimale (m²) | number | strong_preference | 0.7 | important |
| `surface_max` | Surface maximale (m²) | number | weak_preference | 0.4 | optional |
| `bedrooms_min` | Nombre de chambres min | number | strong_preference | 0.8 | important |
| `bedrooms_max` | Nombre de chambres max | number | weak_preference | 0.4 | optional |
| `bathrooms_min` | Nombre de sdb min | number | weak_preference | 0.5 | optional |
| `furnished` | Meublé | boolean | nice_to_have | — | optional |
| `floor_level` | Niveau/Étage | number | weak_preference | 0.3 | optional |
| `parking` | Parking | boolean | nice_to_have | — | optional |
| `balcony` | Balcon | boolean | nice_to_have | — | optional |
| `garden` | Jardin | boolean | nice_to_have | — | optional |
| `elevator` | Ascenseur | boolean | weak_preference | 0.3 | optional |
| `condition` | État du bien | enum | strong_preference | 0.6 | important |
| `construction_year` | Année de construction | number | weak_preference | 0.3 | optional |

### 11.2 Residential-Specific Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `residence_type` | Type d'habitation | enum | strong_preference | 0.7 | important |
| `rooms_total` | Nombre de pièces | number | strong_preference | 0.7 | important |
| `living_room` | Séjour/Salon | boolean | weak_preference | 0.3 | optional |
| `dining_room` | Salle à manger | boolean | nice_to_have | — | optional |
| `guest_toilet` | WC invités | boolean | nice_to_have | — | optional |
| `maid_room` | Chambre de service | boolean | nice_to_have | — | optional |
| `terrace` | Terrasse | boolean | nice_to_have | — | optional |
| `pool` | Piscine | boolean | nice_to_have | — | optional |
| `heating` | Chauffage | enum | weak_preference | 0.3 | optional |
| `air_conditioning` | Climatisation | boolean | weak_preference | 0.4 | optional |

### 11.3 Land-Specific Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `title_status` | Statut du titre foncier | enum | deal_breaker | 1.0 | mandatory |
| `is_constructible` | Constructible | boolean | hard_constraint | 1.0 | mandatory |
| `land_area` | Superficie terrain (m²) | number | strong_preference | 0.8 | mandatory |
| `land_use` | Destination (usage) | enum | strong_preference | 0.7 | important |
| `road_access` | Accès routier | enum | strong_preference | 0.6 | important |
| `electricity_nearby` | Électricité à proximité | boolean | nice_to_have | — | optional |
| `water_nearby` | Eau à proximité | boolean | nice_to_have | — | optional |
| `flood_zone` | Zone inondable | boolean | deal_breaker | 1.0 | mandatory |
| `land_orientation` | Orientation | enum | weak_preference | 0.2 | optional |

### 11.4 Commercial-Specific Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `commercial_type` | Type commercial | enum | hard_constraint | 1.0 | mandatory |
| `front_window` | Vitrine/Façade | number | strong_preference | 0.7 | important |
| `ceiling_height` | Hauteur sous plafond | number | strong_preference | 0.6 | important |
| `floor_load` | Charge au sol (kg/m²) | number | weak_preference | 0.4 | optional |
| `loading_dock` | Quai de chargement | boolean | nice_to_have | — | optional |
| `parking_capacity` | Capacité parking | number | weak_preference | 0.4 | optional |
| `access_truck` | Accès camion | boolean | strong_preference | 0.6 | important |
| `visibility` | Visibilité (passage) | enum | strong_preference | 0.6 | important |
| `commercial_zone` | Zone commerciale | enum | strong_preference | 0.7 | important |
| `license_type` | Type de licence/droit | enum | deal_breaker | 1.0 | mandatory |

### 11.5 Investment-Specific Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `investment_type` | Type d'investissement | enum | hard_constraint | 1.0 | mandatory |
| `roi_target` | ROI visé (%) | number | strong_preference | 0.7 | important |
| `investment_horizon` | Horizon placement | enum | strong_preference | 0.7 | important |
| `monthly_rental_income` | Revenu locatif mensuel visé | number | strong_preference | 0.6 | important |
| `management_type` | Type de gestion | enum | strong_preference | 0.5 | important |
| `exit_strategy` | Stratégie de sortie | enum | weak_preference | 0.4 | optional |
| `co_investors` | Co-investisseurs | boolean | weak_preference | 0.3 | optional |

### 11.6 Financing-Specific Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `financing_type` | Type de financement | enum | hard_constraint | 1.0 | mandatory |
| `loan_amount` | Montant du prêt | number | hard_constraint | 1.0 | mandatory |
| `down_payment` | Apport personnel | number | hard_constraint | 1.0 | mandatory |
| `loan_duration` | Durée du prêt (mois) | number | strong_preference | 0.7 | important |
| `monthly_payment` | Mensualité souhaitée | number | strong_preference | 0.7 | important |
| `interest_rate` | Taux d'intérêt visé | number | weak_preference | 0.4 | optional |
| `employment_status` | Situation professionnelle | enum | strong_preference | 0.7 | important |
| `monthly_income` | Revenu mensuel | number | hard_constraint | 1.0 | mandatory |
| `existing_loans` | Crédits en cours | number | strong_preference | 0.6 | important |
| `guarantor_available` | Garant disponible | boolean | strong_preference | 0.5 | important |

### 11.7 Professional Search Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `professional_type` | Type de professionnel | enum | hard_constraint | 1.0 | mandatory |
| `service_required` | Service recherché | enum | strong_preference | 0.8 | mandatory |
| `city_pro` | Ville (professionnel) | location | hard_constraint | 1.0 | mandatory |
| `neighborhood_pro` | Quartier (professionnel) | location | weak_preference | 0.4 | optional |
| `language_pro` | Langue parlée | multiselect | weak_preference | 0.3 | optional |
| `years_experience` | Années d'expérience min | number | weak_preference | 0.4 | optional |
| `certification` | Certification requise | multiselect | strong_preference | 0.6 | important |
| `urgency_pro` | Urgence | enum | boost | +20 | optional |

### 11.8 Service Request Fields

| Field Code | Label (FR) | Field Type | Matching Role | Weight | Priority |
|------------|------------|------------|---------------|--------|----------|
| `service_type` | Type de service | enum | hard_constraint | 1.0 | mandatory |
| `property_to_service` | Bien concerné | uuid | strong_preference | 0.7 | important |
| `city_service` | Ville du service | location | hard_constraint | 1.0 | mandatory |
| `service_description` | Description du besoin | text | weak_preference | 0.3 | optional |
| `service_timeline` | Délai souhaité | enum | strong_preference | 0.6 | important |
| `service_budget` | Budget pour le service | number | strong_preference | 0.6 | important |

---

## 12. Question Priority System

Every qualification field is assigned a priority level that determines asking order, optionality, and channel behavior.

### 12.1 Priority Levels

| Priority | Weight | Behavior | Channel Adaptation |
|----------|--------|----------|-------------------|
| **mandatory** | Must answer | User cannot proceed without answering. Pre-filter before matching. Asked first in all channels. | WhatsApp: always asked (1/chunk). Telegram: asked first. Dashboard: required field (red asterisk). |
| **important** | Should answer | User can defer but is encouraged. Asked second in progressive order. | WhatsApp: aggregated into "we need a few more details". Telegram: asked after mandatory. Dashboard: marked "recommended". |
| **optional** | Nice to have | User can skip freely. Asked last, only if user engages further. | WhatsApp: not asked (captured via "optional details" prompt). Telegram: asked only on explicit "learn more". Dashboard: collapsed section, user expands voluntarily. |

### 12.2 Question Priority Distribution per Matrix

| Domain | Mandatory | Important | Optional | Total |
|--------|-----------|-----------|----------|-------|
| Residential | 4-6 | 5-8 | 6-12 | 15-26 |
| Land | 5-7 | 4-6 | 4-8 | 13-21 |
| Commercial | 5-7 | 6-10 | 6-14 | 17-31 |
| Investment | 4-5 | 5-7 | 3-6 | 12-18 |
| Financing | 5-7 | 5-8 | 3-6 | 13-21 |
| Professional | 3-4 | 3-5 | 4-8 | 10-17 |
| Service | 3-4 | 3-5 | 3-6 | 9-15 |

### 12.3 Priority-Based Asking Order

```
Step 1-3:   Only mandatory fields (intention, property_type, city)
Step 4-6:   Mandatory + Important fields
Step 7-9:   All fields (mandatory + important + optional)
Step 10:    Confirmation of all answers + escalation path
```

---

## 13. 10-Step Progressive Qualification Order

Strict progressive disclosure order that governs qualification across all channels.

### 13.1 Step Definitions

| Step | Name | Fields Asked | Channel Limit | Skip Behavior |
|------|------|-------------|---------------|---------------|
| 1 | **Intention** | intention | WhatsApp: 1, Telegram: 1, Dashboard: 1 | Cannot skip |
| 2 | **Type** | property_type, (subtype) | WhatsApp: 1, Telegram: 1, Dashboard: 1 | Cannot skip |
| 3 | **Ville** | city, neighborhood | WhatsApp: 1 (city only), Telegram: 2, Dashboard: 2 | Cannot skip city; neighborhood skippable |
| 4 | **Quartier** | neighborhood (if city known), zone | WhatsApp: 1, Telegram: 1-2, Dashboard: 2 | Skippable |
| 5 | **Budget** | budget_min, budget_max, negotiable | WhatsApp: 1 (range), Telegram: 2, Dashboard: 2-3 | Cannot skip |
| 6 | **Délai** | timeline, urgency | WhatsApp: 1, Telegram: 1-2, Dashboard: 2 | Skippable |
| 7 | **Critères** | surface, bedrooms, bathrooms, condition, construction_year | WhatsApp: 1 (aggregated), Telegram: 2-3, Dashboard: full | Important fields only |
| 8 | **Préférences** | furnished, parking, balcony, garden, elevator, pool, terrace | WhatsApp: 0 (not asked), Telegram: 1-2, Dashboard: full | All optional |
| 9 | **Confirmation** | Summary of all answers, confirmation boolean | All channels: confirmation prompt | Must confirm |
| 10 | **Escalade** | Escalate to agent if incomplete, optional notes | WhatsApp: agent handoff, Telegram: agent chat, Dashboard: submit to matching | Auto-escalate if incomplete |

### 13.2 State Machine

```
Step 1 (Intention)
  → Step 2 (Type)
    → Step 3 (Ville)
      → Step 4 (Quartier)
        → Step 5 (Budget)
          → Step 6 (Délai)
            → Step 7 (Critères)
              → Step 8 (Préférences)
                → Step 9 (Confirmation)
                  → [confirmed] → Qualification Complete → Matching
                  → [incomplete] → Step 10 (Escalade) → Agent Intervention
```

### 13.3 Step Transition Rules

| Transition | Condition |
|------------|-----------|
| Step N → Step N+1 | All mandatory fields in Step N are answered |
| Step N → Step N+2 | User explicitly says "I don't know" or skips all optional fields |
| Step 9 → Matching | Confirmation = true AND all mandatory fields across all steps are answered |
| Step 9 → Step 10 | Confirmation = false OR mandatory fields missing |
| Any Step → Step 10 | User requests agent assistance at any point |
| Any Step → Repeat | User provides invalid input (max 3 retries per field) |

---

## 14. Per-Channel Adaptation

The same qualification matrix produces different user experiences depending on the channel.

### 14.1 Channel Characteristics

| Aspect | WhatsApp | Telegram | Dashboard |
|--------|----------|----------|-----------|
| **Interaction style** | Conversational, single-thread | Conversational, multi-thread | Form-based, full view |
| **Questions per interaction** | 1 question per message | 2-3 questions per message | Full step rendered at once |
| **Response mechanism** | Free text / button reply | Inline keyboard / free text | Form inputs (dropdown, slider, text) |
| **Media support** | Images, documents | Images, documents | Full media, maps, calculators |
| **State persistence** | Session-based (24h timeout) | Session-based (48h timeout) | Persistent (until form submitted) |
| **Back navigation** | "Back" keyword | "Back" button | Previous step button |
| **Skip mechanism** | "Skip" reply | "Skip" inline button | "Skip this step" link |
| **Agent handoff** | "Talk to agent" keyword | /agent command | "Request agent assistance" button |

### 14.2 Question Limits per Channel

| Channel | Mandatory per Interaction | Important per Interaction | Optional per Interaction | Total per Step |
|---------|--------------------------|--------------------------|--------------------------|----------------|
| WhatsApp | 1 | 0 (aggregated summary) | 0 | 1 question max |
| Telegram | 2 | 1 | 0 (expandable) | 2-3 questions max |
| Dashboard | All mandatory | All important | All optional (collapsed) | Full step rendered |

### 14.3 Channel Adaptation Rules

| Rule | WhatsApp | Telegram | Dashboard |
|------|----------|----------|-----------|
| 1. Entry point | "What are you looking for?" → intention | /start → inline keyboard → intention | Landing page → matrix selection |
| 2. Question format | Single question per message with quick reply buttons | Grouped questions with inline keyboard | Form with validation, help tooltips, sliders |
| 3. Progress indication | "Step X of 10" in message footer | Progress bar in message | Step indicator at top of form |
| 4. Error handling | "I didn't understand. Please reply with a number." | "Invalid input. Choose from options below:" | Inline validation error |
| 5. Timeout handling | 24h inactivity → reminder → reopen | 48h inactivity → reminder → reopen | Session preserved indefinitely |
| 6. Confirmation | Summary card with "Confirm" button | Summary message with approve button | Review page with edit links |

---

## 15. Matrix Versioning Strategy

### 15.1 Versioning Principles

1. **All matrices are versioned.** Every change produces a new version entry.
2. **Dossiers are snapshotted.** When a dossier begins qualification, the matrix version is frozen and stored on the Project.
3. **Active dossiers are grandfathered.** Updating a matrix version does not requalify active dossiers.
4. **Admin can force requalification.** A manual override exists to requalify dossiers against a newer matrix version.
5. **Version history is immutable.** Once created, version snapshots are never modified.

### 15.2 Version Schema

```
MAJOR.MINOR.PATCH

MAJOR: Breaking change — field removed, field semantics changed, matching role changed
MINOR: Additive change — new field added, field priority changed, new rule added
PATCH: Cosmetic change — label updated, help text changed, sort order adjusted
```

### 15.3 Version Lifecycle

```
draft → beta → active → deprecated → retired

draft:      Being edited, not visible to users
beta:       Available for testing (admin + test users)
active:     Default for new dossiers
deprecated: No longer default, existing dossiers continue
retired:    No longer available, existing dossiers had version frozen
```

### 15.4 Snapshot Contents

Each MatrixVersion snapshot stores a complete frozen copy of:

```json
{
  "version": "1.2.0",
  "matrix_code": "RES-APT-BUY",
  "fields": [
    {"field_code": "budget_min", "priority": "mandatory", "matching_role": "hard_constraint", ...}
  ],
  "rules": [
    {"rule_code": "BUDGET_MIN_MAX", "rule_type": "validation", ...}
  ],
  "applicability": {
    "property_types": ["apartment"],
    "transaction_types": ["buy"]
  }
}
```

### 15.5 Version Compatibility Matrix

| Current Version | Target Version | Auto-migration | Requires Requalification |
|-----------------|----------------|----------------|---------------------------|
| 1.0.x | 1.0.y (patch) | Yes | No |
| 1.x.x | 1.y.x (minor) | Yes (new fields = null) | Optional |
| 1.x.x | 2.0.0 (major) | No | Required |

---

## 16. Matrix Applicability Rules

### 16.1 Applicability Resolution Order

When determining which matrix to apply for a given dossier, rules are evaluated in this order:

1. **Exact match** — All dimensions match exactly → highest priority
2. **Partial match** — Core dimensions match (request_family + transaction_type + property_type) → second priority
3. **Family fallback** — Only property_family matches → third priority
4. **Default matrix** — is_default = true for the request_family → lowest priority

### 16.2 Match Resolution Algorithm

```
function resolve_matrix(dossier):
    candidates = []
    for each MatrixApplicability:
        score = 0
        if matches(request_family): score += 1000
        if matches(transaction_type): score += 500
        if matches(property_type): score += 300
        if matches(requester_typology): score += 100
        if matches(journey_stage): score += 50
        if matches(service_type): score += 200
        if is_default: score += 10
        candidates.append({matrix, score})
    sort candidates by score descending
    return candidates[0].matrix  // highest score wins
```

### 16.3 Applicability by Dimension Combinations

| Request Family | Transaction Type | Property Family | Default Matrix |
|----------------|-----------------|-----------------|----------------|
| property_search | buy | residential | RES-APT-BUY |
| property_search | rent | residential | RES-APT-RENT |
| property_search | buy | land | LND-PLT-BUY |
| property_search | invest | land | LND-PLT-INV |
| property_search | buy | commercial | COM-OFF-BUY |
| property_search | rent | commercial | COM-OFF-RENT |
| property_search | commercial_lease | commercial | COM-COM-LEASE |
| investment_analysis | invest | any | INV-RES-BUY |
| financing_request | finance | any | FIN-MTG-BUY |
| professional_find | find | — | PRO-AGE-FND |
| service_request | service | — | SVC-EST-BUY |

### 16.4 Requester Typology Matrix Selection

| Requester Typology | Preferred Matrices | Behavior |
|--------------------|-------------------|----------|
| individual | Residential, Land, Service | Standard qualification flow |
| professional | Commercial, Professional | Simplified qualification, fewer mandatory fields |
| investor | Investment, Financing | Investment-specific fields activated |
| diaspora | All (with diaspora markers) | Diaspora boost applied, currency options shown |
| agency | Commercial, Professional | Agency-specific fields, multi-property context |
| enterprise | Commercial, Financing | Enterprise-specific fields, legal entity info |

### 16.5 Journey Stage Applicability

| Journey Stage | Applicable Matrices | Qualification Behavior |
|---------------|--------------------|----------------------|
| discovery | All (abridged) | Mandatory fields only, single interaction |
| qualification | All (full) | Full 10-step progressive order |
| matching | None (read-only) | Qualification data locked; read for scoring |
| negotiation | None | Re-qualification only if terms fundamentally change |
| transaction | None | Re-qualification only if property changes |

---

## 17. Complete Extension Mapping Table

| EXT ID | Source Concept | Proposed Entity | Priority | Phase |
|--------|---------------|-----------------|----------|-------|
| EXT-QUAL-001 | Residential Search (18 matrices) | QualificationMatrixDefinition | P1 | Phase 2 |
| EXT-QUAL-002 | Land Search (7 matrices) | QualificationMatrixDefinition | P1 | Phase 2 |
| EXT-QUAL-003 | Commercial Search (21 matrices) | QualificationMatrixDefinition | P2 | Phase 2 |
| EXT-QUAL-004 | Investment (5 matrices) | QualificationMatrixDefinition | P2 | Phase 2 |
| EXT-QUAL-005 | Financing Request (10 matrices) | QualificationMatrixDefinition | P2 | Phase 2 |
| EXT-QUAL-006 | Professional Search (27 matrices) | QualificationMatrixDefinition | P2 | Phase 2 |
| EXT-QUAL-007 | Real Estate Service (24 matrices) | QualificationMatrixDefinition | P2 | Phase 2 |
| EXT-QUAL-008 | Field dictionary with matching roles | QualificationFieldDefinition + MatchingSemanticDefinition | P2 | Phase 2 |
| EXT-QUAL-009 | Question priority system | QuestionRuleDefinition (priority field) | P2 | Phase 2 |
| EXT-QUAL-010 | Progressive qualification order (10 steps) | QualificationRuleDefinition + step_number field | P1 | Phase 2 |
| EXT-QUAL-011 | Per-channel adaptation | QuestionRuleDefinition (per-channel config) | P2 | Phase 2 |
