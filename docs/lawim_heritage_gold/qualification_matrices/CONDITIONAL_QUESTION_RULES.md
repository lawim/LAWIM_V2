# CONDITIONAL QUESTION RULES — When and How to Ask

**Document ID:** LAWIM-GOLD-QM-CONDITIONAL-V1
**Status:** CANONICAL — Definitive reference for conditional question rules across all matrices
**Date:** 2026-07-15

---

## Table of Contents

1. [Categories of Questions](#1-categories-of-questions)
2. [Questions Always Needed](#2-questions-always-needed)
3. [Questions Needed Only in Certain Cases](#3-questions-needed-only-in-certain-cases)
4. [Questions to Deduce from Context](#4-questions-to-deduce-from-context)
5. [Questions to Defer](#5-questions-to-defer)
6. [Questions Never to Ask](#6-questions-never-to-ask)
7. [Domain-Specific Conditional Rules](#7-domain-specific-conditional-rules)
8. [Real Examples from Heritage](#8-real-examples-from-heritage)
9. [Implementation Guide](#9-implementation-guide)
10. [Complete Rule Reference Table](#10-complete-rule-reference-table)

---

## 1. Categories of Questions

Questions fall into five categories based on when and how they should be asked:

| Category | Definition | Marker |
|----------|------------|--------|
| **ALWAYS** | Must be asked for every qualification in the family | `mandatory_when: always` |
| **CONDITIONAL** | Asked only when specific conditions are met | `mandatory_when: {condition}` |
| **DEDUCED** | Never asked; derived from other fields | `(system-derived)` |
| **DEFERRED** | Delayed until after search or until context is right | `question_priority: high` |
| **FORBIDDEN** | Never asked; explicitly prohibited | Listed in forbidden_questions |

---

## 2. Questions Always Needed

### Universal Fields (All Requests)

These fields are mandatory regardless of property type, transaction, or channel:

| field_id | Question | Rationale |
|----------|----------|-----------|
| FLD-TRANSACTION | "C'est pour louer, acheter, vendre ou investir ?" | Foundation of all qualification |
| FLD-PROPERTY_TYPE | "Quel type de bien cherchez-vous ?" | Determines which matrix to use |
| FLD-CITY | "Dans quelle ville ?" | Geographic anchor for all searches |

### Residential Search (Always)

| field_id | Question | Rationale |
|----------|----------|-----------|
| FLD-BUDGET_MAX | "Quel budget maximum ?" | Budget is blocking per QUALIFICATION_MODEL.md §2.2 |
| FLD-NEIGHBORHOOD | "Quel quartier ou quelle zone ?" | Neighborhood is 25% of matching weight |
| FLD-BUDGET_TYPE | (Derived) | Determines monthly vs. total price |
| FLD-DISPONIBILITE | "À partir de quand ?" | Timing essential for matching |
| FLD-NOM | "Quel est votre nom ?" | Required for introduction |
| FLD-TELEPHONE | "Quel est votre numéro ?" | Required for contact |
| FLD-CANAL_PREFERE | "Quel canal préférez-vous ?" | Required for communication |

### Land Search (Always)

| field_id | Question | Rationale |
|----------|----------|-----------|
| ville | "Dans quelle ville ?" | Geographic anchor |
| quartier | "Quel quartier ?" | 25% of matching weight |
| surface | "Quelle surface (en m2) ?" | Critical for land |
| budget_total | "Quel budget maximum ?" | Budget is blocking |
| usage_prevu | "Quel usage prévu ?" | Hard constraint for matching |

### Commercial (Always)

| field_id | Question | Rationale |
|----------|----------|-----------|
| activité_prévue | "Quel type d'activité ?" | Hard constraint for commercial matching |
| surface_min | "Surface minimale ?" | Hard constraint |
| ville | "Dans quelle ville ?" | Geographic anchor |
| transaction | "Location/achat/cession ?" | Transaction type |
| budget | Budget for purchase or rent | Budget is blocking |

### Financing (Always)

| field_id | Question | Rationale |
|----------|----------|-----------|
| objet_financement | "Quel est l'objet de votre demande ?" | Core purpose |
| montant_recherche | "Quel montant ?" | Amount drives matching |
| apport_disponible | "Quel apport ?" | Key eligibility factor |
| ville_projet | "Dans quelle ville ?" | Geographic anchor |
| type_bien_projet | "De quel type de bien s'agit-il ?" | Property type reference |

### Professional Service (Always)

| field_id | Question | Rationale |
|----------|----------|-----------|
| type_prestation | "Quel type de service ?" | Service categorization |
| localisation | "Où avez-vous besoin de ce service ?" | Geographic |
| description_besoin | "Décrivez votre besoin." | Service specifics |
| urgence | "Quel niveau d'urgence ?" | Prioritization |
| date_souhaitee | "À partir de quand ?" | Timing |

---

## 3. Questions Needed Only in Certain Cases

### 3.1 Property-Type-Dependent

| field_id | Asked When | Condition |
|----------|------------|-----------|
| FLD-CHAMBRES | Multi-room property | Appartement, villa, maison, duplex, triplex. NOT for chambre, studio, terrain. |
| FLD-SALONS | Appartement, villa | 0 for studio/chambre (open plan) |
| FLD-DOUCHES | All residential | But number varies: 1 for chambre, 1+ for appartement |
| FLD-CUISINE | Residential with kitchen | Always for appartement/villa. Conditional for chambre_simple. |
| FLD-SURFACE_TERRAIN | Villa, land | Only properties with land component |
| FLD-ETAGE | Building with floors | Not for chambre simple, villa (ground floor houses) |
| FLD-ASCENSEUR | Etage > 2 | Irrelevant for ground-floor properties |
| FLD-COUR | Ground-floor, villa | Only for ground-level access |
| FLD-JARDIN | Villa, ground-floor apartment | Conditional on property type |
| FLD-PISCINE | High-end villa only | Luxury property segment |
| COM-COMMON-009 | Entrepot, hangar, atelier | Ceiling height only relevant for industrial/warehouse |
| COM-COMMON-010 | Entrepot, hangar, site_industriel | Vehicle access for industrial types |
| COM-COMMON-011 | Boutique, magasin | Road visibility for retail |
| COM-COMMON-021 | Restaurant, bar, hotel | Operating license for regulated activities |

### 3.2 Transaction-Dependent

| field_id | Asked When | Condition |
|----------|------------|-----------|
| FLD-FINANCING | BUY transaction | "Comptant ou crédit ?" |
| FLD-CAUTION | RENT transaction | "Dépôt de garantie ?" |
| FLD-CHARGES | RENT transaction | "Charges incluses ?" |
| FLD-USAGE | BUY transaction | "Résidence ou investissement ?" |
| COM-COMMON-024 | transaction=cession | "Fonds de commerce inclus ?" |
| FIN-CONS-001 | Construction financing | "Terrain disponible ?" |
| FIN-SAL-001 | profil_demandeur=salarie | Employee-specific fields |
| FIN-SE-001 | profil_demandeur=independant | Self-employed fields |

### 3.3 Channel-Dependent

| field_id | Asked When | Condition |
|----------|------------|-----------|
| FLD-PROXIMITY_PREFERENCES | Telegram/Dashboard | WhatsApp: defer or skip |
| FLD-MOBILITY | Multiple neighborhoods mentioned | Only relevant if user lists multiple zones |
| FLD-LANGUE | First message not in French | Auto-detect; only confirm if uncertain |

### 3.4 Context-Dependent

| field_id | Asked When | Condition |
|----------|------------|-----------|
| FLD-GROUPE_ELECTROGENE | City with frequent power cuts | Conditional on infrastructure data |
| FLD-FORAGE | Water-scarce area | Conditional on water infrastructure |
| FLD-CLIMATISATION | Hot city or user mentions heat | Conditional on climate + user signal |
| FLD-INTERNET | User mentions digital work, student | Conditional on user profile signal |
| FLD-MENAGE | Short-term rental > 1 week | Conditional on stay duration |
| FLD-LINGE | Short-term furnished rental | Conditional on property subtype |
| FIN-CONS-002 | terrain_disponible=true | Only if land is already available |
| FIN-CONS-007 | Construction financing | Permits and authorizations |
| PRO-COMMON-010 | Regulated profession | Qualifications needed for certain trades |

### 3.5 User-Behavior-Dependent

| field_id | Asked When | Condition |
|----------|------------|-----------|
| FLD-SURFACE | User mentions size or space | Only ask if user brings up size concerns |
| FLD-BUDGET_MIN | Range uncertainty | Only if user says "between X and Y" |
| FLD-ETAT_PROPRIETE | User asks about condition | Reactive, not proactive |
| FLD-DEPENDANCES | User mentions extra structures | Reactive |

---

## 4. Questions to Deduce from Context

### Fields That Are NEVER Asked

These fields are derived from property type, transaction, or context:

| field_id | Derivation Rule | Rationale |
|----------|-----------------|-----------|
| FLD-CHAMBRES | = 0 for studio, studio_moderne, studio_meuble | By definition, studios have no separate bedroom |
| FLD-CHAMBRES | = 1 for chambre_simple, chambre_moderne | A "chambre" is one room by definition |
| FLD-SALONS | = 0 for studio, chambre | Open-plan, no separate salon |
| FLD-MEUBLE | = MEUBLE for studio_meuble, appartement_meuble | Property type implies furnishing |
| FLD-MEUBLE | = NON_MEUBLE for appartement_non_meuble | Property type implies unfurnished |
| FLD-DOUCHES | = INTERNE for studio_moderne, appartement_moderne | By definition, modern = internal shower |
| FLD-SALONS | = 1 for appartement (minimum) | French Cameroonian standard |
| FLD-BUDGET_TYPE | = MONTHLY_RENT for RENT transaction | Budget semantics |
| FLD-BUDGET_TYPE | = TOTAL_PRICE for BUY transaction | Budget semantics |
| FLD-DERIVED-STANDING | Deduced from budget + quartier + property type | Never ask standing directly |
| FLD-DERIVED-PROFIL | Deduced from language + references + behavior | Never ask profile directly |
| FLD-DERIVED-URGENCE_REELLE | Deduced from delai + message language | Never ask "how urgent?" if deducible |
| FLD-TRANSACTION_TYPE | Derived from FLD-TRANSACTION | System mapping |
| FLD-REQUEST_FAMILY | Derived from intent + property type | System categorization |
| FLD-JOURNEY_STAGE | Progress tracking | System state |

### Never Ask Directly

These questions are explicitly forbidden in heritage because they should be deduced:

```
"Quel standing ?"
"Combien de pièces ?" (use chambres + salons instead)
"Quel est votre profil ?" (deduce from behavior)
"Quel type de résidence ?" (already covered by property type)
"Quelle surface ?" (for property types with standard sizes)
```

---

## 5. Questions to Defer

### Defer to Post-Search

These questions should only be asked after the first search results are shown:

| field_id | Why Deferred | Ask After Search When |
|----------|-------------|----------------------|
| FLD-BALCON | Low filtering impact | User wants to refine results |
| FLD-JARDIN | Low filtering impact | User wants to refine results |
| FLD-CLIMATISATION | Depends on property availability | User wants specific amenities |
| FLD-INTERNET | Conditionally important | User indicates need |
| FLD-PARKING | Medium impact | Ask before search only if high need |
| FLD-SECURITE | Usually desired; low differentiation | User wants to refine |
| FLD-GARDIENNAGE | Very low impact | Rarely asked; optional |
| FLD-GROUPE_ELECTROGENE | Infrastructure-dependent | Conditional on area knowledge |
| FLD-ETAGE | Preference, not constraint | After narrowing down properties |
| FLD-ASCENSEUR | Conditionally relevant | Only if building has floors |
| FLD-FORAGE | Very specific | Conditional on water issues |
| FLD-EAU | Most areas have water | Ask only if concern is raised |
| FLD-ELECTRICITE | Most areas have electricity | Ask only if concern is raised |

### Defer to Introduction Stage

These questions should wait until the user has seen results and wants to proceed:

| field_id | Why Deferred | Ask When |
|----------|-------------|----------|
| FLD-NOM | Not needed for search | User wants to be introduced |
| FLD-TELEPHONE | Privacy-sensitive | User wants to be contacted |
| FLD-EMAIL | Not needed for search | User prefers email contact |
| FLD-CANAL_PREFERE | Not needed for search | Before introduction |
| FLD-LANGUE | Auto-detect | Only confirm if uncertain |

### Defer to Transaction Stage

These questions should be asked only when a transaction is imminent:

| field_id | Why Deferred | Ask When |
|----------|-------------|----------|
| FLD-CAUTION | Rent-specific, at transaction | Before lease signing |
| FLD-CHARGES | Rent-specific | Before lease signing |
| FLD-FINANCING | Buy-specific | Before purchase agreement |
| FLD-NUM_TITRE | Legal-sensitive | Only during legal verification |
| FLD-SIGNATAIRES | Land-specific | Only during title transfer |
| FLD-LITIGES_CONNUS | Highly sensitive | Escalate to legal professional |
| FIN-SAL-001 | Employment details | Only for loan application |
| FIN-COMMON-019 | Personal documents | Only during formal application |

---

## 6. Questions Never to Ask

### Cross-Matrix Forbidden Questions

These questions are prohibited in ALL matrices:

| # | Forbidden Question | Reason | Source |
|---|-------------------|--------|--------|
| 1 | "Avez-vous un autre critère important à ajouter ?" | Empty question, wastes time | CONVERSATION_MODEL.md |
| 2 | "Comme le nombre de pièces ou le standing ?" | Suggestive, biases response | QUALIFICATION_MODEL.md |
| 3 | "Quel est votre standing souhaité ?" | Must be deduced from budget/neighborhood | QUALIFICATION_HERITAGE_EXTRACTION.md |
| 4 | "Combien de pièces ?" | Ambiguous in Cameroon; use chambres+salons | QUALIFICATION_MODEL.md |
| 5 | "Quelle est votre fourchette de prix exacte ?" | Budget maximum is sufficient | QUALIFICATION_MODEL.md |
| 6 | "Avez-vous des critères supplémentaires ?" | Too vague | QUALIFICATION_MODEL.md |
| 7 | "Quel type de résidence ?" | Already covered by property type | QUALIFICATION_MODEL.md |
| 8 | "Avez-vous une préférence pour le propriétaire ?" | Out of scope for qualification | DOMAIN_MODEL.md |
| 9 | "Quel est votre revenu mensuel ?" | Too intrusive for simple search | CONVERSATION_MODEL.md |
| 10 | "Pourquoi cherchez-vous un nouveau logement ?" | Out of scope | QUALIFICATION_MODEL.md |
| 11 | "Avez-vous déjà visité des biens ?" | Not relevant for qualification | QUALIFICATION_MODEL.md |
| 12 | "Quel est votre quartier actuel ?" | Not needed for search | QUALIFICATION_MODEL.md |
| 13 | "Quel âge avez-vous ?" | Age discrimination prohibited | Directive Art.14 |
| 14 | "Quelle est votre situation matrimoniale ?" | Marital status irrelevant | Directive Art.14 |
| 15 | "Quelle est votre ethnie ?" | Prohibited discrimination | Directive Art.14 |
| 16 | "Quelle est votre religion ?" | Prohibited discrimination | Directive Art.14 |
| 17 | "Quelle est votre orientation politique ?" | Prohibited discrimination | Directive Art.14 |
| 18 | "Avez-vous des enfants ?" | Personal data, irrelevant | Directive Art.14 |

### Property-Type-Specific Forbidden Questions

| Property Type | Forbidden Question | Reason |
|---------------|-------------------|--------|
| chambre_simple | "Combien de chambres ?" | Always 1 by definition |
| chambre_simple | "Combien de salons ?" | Not applicable |
| chambre_simple | "À quel étage ?" | Not pertinent |
| chambre_moderne | "Combien de chambres ?" | Always 1 by definition |
| studio | "Combien de chambres ?" | Studio = no separate bedroom |
| studio | "Combien de salons ?" | Open plan = 0 salons |
| studio_moderne | "Douche externe ou interne ?" | Always interne by definition |
| studio_meuble | "Meublé ou non meublé ?" | Always meublé by definition |
| appartement_non_meuble | "Meublé ou non meublé ?" | Always non_meuble by definition |
| appartement_meuble | "Meublé ou non meublé ?" | Always meublé by definition |
| ALL LAND | "Combien de chambres ?" | Irrelevant for land |
| ALL LAND | "Combien de douches ?" | Irrelevant for land |
| ALL LAND | "Combien de salons ?" | Irrelevant for land |
| ALL LAND | "Quel étage ?" | Irrelevant for land |
| ALL COMMERCIAL | "Chambres à coucher ?" | Residential criterion |
| ALL COMMERCIAL | "Salles de bain ?" | Residential criterion |
| ALL COMMERCIAL | "Usage résidentiel ?" | Not commercial |

---

## 7. Domain-Specific Conditional Rules

### 7.1 Residential Search Rules

| Rule | Description | Source |
|------|-------------|--------|
| RES-C01 | Never ask bedrooms for studio (always 0) | residential_search_matrices.md |
| RES-C02 | Never ask bedrooms for chambre (always 1) | residential_search_matrices.md |
| RES-C03 | Never ask meublé for studio_meuble (always meublé) | residential_search_matrices.md |
| RES-C04 | Never ask meublé for appartement_non_meuble (always non) | residential_search_matrices.md |
| RES-C05 | Ask climatisation only for hot cities | residential_search_matrices.md |
| RES-C06 | Ask groupe_électrogène only in high power-cut zones | residential_search_matrices.md |
| RES-C07 | Ask forage only in water-scarce areas | residential_search_matrices.md |
| RES-C08 | Ask étage only for building-type properties | residential_search_matrices.md |
| RES-C09 | Ask ascenseur only if étage > 2 | residential_search_matrices.md |
| RES-C10 | Ask jardin only for ground-floor or villa | residential_search_matrices.md |
| RES-C11 | Ask cour only for ground-floor access | residential_search_matrices.md |
| RES-C12 | Ask caution and charges for RENT only | residential_search_matrices.md |
| RES-C13 | Ask financing and usage for BUY only | residential_search_matrices.md |
| RES-C14 | Ask genre_préférence for colocation only, with sensitivity | residential_search_matrices.md |
| RES-C15 | Ask bourse for university context only, with sensitivity | residential_search_matrices.md |
| RES-C16 | Ask restaurant/ling for short-term context only | residential_search_matrices.md |
| RES-C17 | Ask université only for cite_universitaire | residential_search_matrices.md |

### 7.2 Land Search Rules

| Rule | Description | Source |
|------|-------------|--------|
| LAND-C01 | Always distinguish titre/non-titre | land_search_matrices.md |
| LAND-C02 | Surface is mandatory in m2 | land_search_matrices.md |
| LAND-C03 | Budget = global price or price/m2 (user chooses) | land_search_matrices.md |
| LAND-C04 | Location can be quartier OR axe+village+repere | land_search_matrices.md |
| LAND-C05 | Never conclude legal validity from user declarations | land_search_matrices.md |
| LAND-C06 | verification_required = true for all land transactions | land_search_matrices.md |
| LAND-C07 | professional_review = notaire or geometre required | land_search_matrices.md |
| LAND-C08 | usage_prevu is a hard constraint for matching | land_search_matrices.md |
| LAND-C09 | Ask titre only for terrain_titre or when user requires it | land_search_matrices.md |
| LAND-C10 | Ask documents only for terrain_non_titre | land_search_matrices.md |
| LAND-C11 | Ask signataires only for collective/individual title | land_search_matrices.md |
| LAND-C12 | Ask litiges only before transaction readiness | land_search_matrices.md |
| LAND-C13 | Ask procuration only when owner not present | land_search_matrices.md |
| LAND-C14 | Ask bornage only when limits are unclear | land_search_matrices.md |
| LAND-C15 | Ask pv_bornage only if bornage was done | land_search_matrices.md |

### 7.3 Commercial Rules

| Rule | Description | Source |
|------|-------------|--------|
| COM-C01 | Ask activité for all commercial types | commercial_property_matrices.md |
| COM-C02 | Ask hauteur only for entrepot/hangar/atelier | commercial_property_matrices.md |
| COM-C03 | Ask accès_véhicules for entrepot/hangar/industriel | commercial_property_matrices.md |
| COM-C04 | Ask visibilité for boutique/magasin | commercial_property_matrices.md |
| COM-C05 | Ask flux_passage for boutique/restaurant/bar | commercial_property_matrices.md |
| COM-C06 | Ask licence_exploitation for restaurant/bar/hotel | commercial_property_matrices.md |
| COM-C07 | Ask accès_pmr for hotel/restaurant/bureau | commercial_property_matrices.md |
| COM-C08 | Ask fonds_commerce only for cession transaction | commercial_property_matrices.md |
| COM-C09 | Ask chiffre_affaires only when fonds_commerce=true | commercial_property_matrices.md |
| COM-C10 | Deduce standing from visibility+flux+zone+état; never ask | commercial_property_matrices.md |

### 7.4 Financing Rules

| Rule | Description | Source |
|------|-------------|--------|
| FIN-C01 | Ask revenus only for salaried/self-employed profiles | financing_request_matrices.md |
| FIN-C02 | Ask employeur only for salaried profiles | financing_request_matrices.md |
| FIN-C03 | Ask activité only for self-employed/company profiles | financing_request_matrices.md |
| FIN-C04 | Ask terrain_disponible only for construction financing | financing_request_matrices.md |
| FIN-C05 | Ask statut_juridique_terrain only if terrain is available | financing_request_matrices.md |
| FIN-C06 | Ask plans_disponibles only for construction/renovation | financing_request_matrices.md |
| FIN-C07 | Ask permis_autorisations only for construction/renovation | financing_request_matrices.md |
| FIN-C08 | Ask statut_acquisition always (identifies next steps) | financing_request_matrices.md |
| FIN-C09 | NEVER promise loan approval (matching only) | financing_request_matrices.md |
| FIN-C10 | NEVER ask for bank codes or passwords | financing_request_matrices.md |

### 7.5 Professional Service Rules

| Rule | Description | Source |
|------|-------------|--------|
| PRO-C01 | Ask qualification for regulated professionals (notaire, geometre, architecte) | professional_service_matrices.md |
| PRO-C02 | Ask assurance_rc_pro for all professionals | professional_service_matrices.md |
| PRO-C03 | Ask portfolio/realisations for architect, photographe, home stager | professional_service_matrices.md |
| PRO-C04 | Ask references for all service providers | professional_service_matrices.md |
| PRO-C05 | Ask délai_moyen for services with delivery timelines | professional_service_matrices.md |
| PRO-C06 | Ask type_chantier for construction trades (macon, electricien, etc.) | professional_service_matrices.md |
| PRO-C07 | Ask équipement for specialized services (drone, photo, video) | professional_service_matrices.md |
| PRO-C08 | Ask certifications for diagnostiqueurs (amiante, DPE, etc.) | professional_service_matrices.md |

---

## 8. Real Examples from Heritage

These examples are directly from LAWIM heritage documents and validated conversations:

### Example 1: Studio Search — Don't Ask Bedrooms

```
Extract from residential_search_matrices.md MATRIX-RES-SEARCH-003:
Forbidden Questions:
1. "Combien de chambres ?" — Studio = pas de chambre séparée par définition
2. "Combien de salons ?" — Studio = espace unique (open plan)
```

**Implementation**: When PROPERTY_TYPE=studio, automatically set CHAMBRES=0, SALONS=0 and never ask.

### Example 2: Simple Rental — Don't Ask Land Title

```
Extract from land_search_matrices.md:
For LAND_SEARCH: titre foncier is relevant
For simple RENT: land title is NOT relevant
```

**Implementation**: Only ask about land title when TRANSACTION=BUY and PROPERTY_TYPE is in land categories.

### Example 3: Simple Housing Search — Don't Ask Detailed Income

```
From CONVERSATION_MODEL.md and QUALIFICATION_MODEL.md:
For simple residential RENT search, income is not asked.
Income is only collected for FINANCING_REQUEST.
```

**Implementation**: FLD-REVENUS only appears in financing_request_matrices.md. Never ask for income during residential search qualification.

### Example 4: Minimum Criteria Before Search

```
From READINESS_LEVELS.md — The Fundamental Rule:
"As soon as MINIMUM_SEARCH_READY is reached (city + budget + neighborhood + 
 property type + transaction known), LAWIM can launch a first search."
```

**Implementation**: Do not ask about all apartment features (parking, balcony, garden, security, etc.) before first search if minimum criteria are available.

### Example 5: "Anything Else to Add?" — Not a Qualification Mechanism

```
From residential_search_matrices.md Common Forbidden Questions:
#1: "Avez-vous un autre critère important à ajouter ?" — Question vide, inefficace
```

**Implementation**: Never use open-ended questions as the primary qualification mechanism. Ask specific questions about specific fields.

### Example 6: Deduce Standing, Never Ask

```
From all residential matrices:
"Quel standing ?" is in forbidden_questions.
Standing is deduced from budget + quartier + property type.
```

**Implementation**: Maintain a deduction engine that computes standing from available data. If budget+neighborhood+property type don't give enough signal, don't ask — it's not a matching-critical field.

### Example 7: Channel Adaptation

```
From CONVERSATION_MODEL.md §2:
WhatsApp: 1 question per message
Telegram: 2-3 fields per message
Dashboard: Full form
```

**Implementation**: Never send 3 questions on WhatsApp. On Telegram, batch related fields.

### Example 8: Urgency Modulates Questions

```
From user behavior analysis:
Urgent users should get minimal questions and fast results.
Non-urgent users can be asked more refinement questions.
```

**Implementation**: If urgency >= 2 (high), skip recommended fields, launch search on minimum criteria only.

---

## 9. Implementation Guide

### Decision Tree for Each Field

```
For each field in the matrix:
├── Is field in forbidden_questions?
│   └── YES → NEVER ask (skip entirely)
├── Is field deducible from context?
│   ├── YES → Derive value automatically, never ask
│   └── NO → continue
├── Is field's mandatory_when condition met?
│   ├── NO → Skip (field is optional for this context)
│   └── YES → continue
├── Has field already been confirmed?
│   ├── YES → Skip (never re-ask)
│   └── NO → continue
├── Is field deferred to later stage?
│   ├── YES → Queue for later stage
│   └── NO → continue
├── Is the field needed before search launch?
│   ├── YES → Add to pre-search question queue
│   └── NO → Add to post-search refinement queue
└── Add to appropriate queue with priority
```

### Conditional Evaluation Engine

```python
def is_applicable(field, context):
    # 1. Check forbidden list
    if field.id in context.matrix.forbidden_fields:
        return False
    
    # 2. Check deducibility
    if field.id in context.matrix.deductible_fields:
        context.set_deduced(field.id, derive(field, context))
        return False  # Never ask what we can deduce
    
    # 3. Check mandatory condition
    condition = field.mandatory_when
    if condition == 'always':
        return True
    return evaluate_condition(condition, context)

def evaluate_condition(condition, context):
    # Examples:
    # "transaction == BUY" → context.transaction == 'BUY'
    # "property_type in [villa, duplex]" → context.property_type in ['villa', 'duplex']
    # "city in hot_cities" → context.city in hot_cities_list
    # "etage > 2" → context.get('etage', 0) > 2
    return conditional_parser.parse(condition, context)
```

### Queue Management

```python
class QuestionQueue:
    def __init__(self, context):
        self.context = context
        self.pre_search = PriorityQueue()
        self.post_search = PriorityQueue()
        self.deferred_intro = PriorityQueue()
        self.deferred_transaction = PriorityQueue()
    
    def populate(self):
        for field in self.context.matrix.fields:
            if not is_applicable(field, self.context):
                continue
            if field.readiness_level == 'SEARCH':
                self.pre_search.put((field.priority, field))
            elif field.readiness_level == 'MATCHING':
                self.post_search.put((field.priority, field))
            elif field.readiness_level == 'INTRODUCTION':
                self.deferred_intro.put((field.priority, field))
            elif field.readiness_level == 'TRANSACTION':
                self.deferred_transaction.put((field.priority, field))
    
    def next_pre_search(self):
        # Check MINIMUM_SEARCH_READY before picking next field
        if self.context.is_search_ready():
            return None  # Launch search now
        return self.pre_search.get()[1] if not self.pre_search.empty() else None
```

---

## 10. Complete Rule Reference Table

### By Readiness Level

| Level | Always Ask | Conditional | Deduced | Deferred | Forbidden |
|-------|-----------|-------------|---------|----------|-----------|
| INTENT_IDENTIFIED | TRANSACTION, PROPERTY_TYPE | INTENT_CONFIDENCE | REQUEST_FAMILY | — | Standing, age, income |
| MINIMUM_INTAKE_READY | CITY, BUDGET_MAX | BUDGET_CURRENCY | BUDGET_TYPE | SURFACE_TERRAIN | Standing |
| MINIMUM_SEARCH_READY | NEIGHBORHOOD | BUDGET_MIN, MOBILITY | BUDGET_TYPE | Most amenities | "Anything else?" |
| MINIMUM_MATCHING_READY | Per matrix | CHAMBRES (conditional) | CHAMBRES (studio), SALONS (studio) | BALCON, JARDIN | Meublé (if known) |
| INTRODUCTION_READY | NOM, TELEPHONE, CANAL | EMAIL, LANGUE | — | CAUTION, CHARGES | Revenus, age |
| VISIT_READY | Per matrix | CLIMATISATION, SECURITE | — | FINANCING | Standing |
| TRANSACTION_READY | CAUTION/CHARGES/FINANCING | TITRE, DOCUMENTS | — | — | Bank codes, passwords |

### By Matrix Family

| Family | Always Mandatory | Conditional | Never |
|--------|-----------------|-------------|-------|
| RESIDENTIAL | TRANSACTION, PROPERTY_TYPE, CITY, BUDGET_MAX, NEIGHBORHOOD | CHAMBRES (not studio/chambre), DOUCHES, CUISINE, MEUBLE | Standing, "other criteria", ambiguous "pieces" |
| LAND | ville, quartier, surface, budget, usage_prevu | titre_requis, type_document, signataires, litiges | chambres, douches, salon, pieces, standing |
| COMMERCIAL | activité, surface_min, ville, transaction, budget | hauteur, accès_véhicules, visibilité, licence | chambres, douches, résidentiel, standing |
| FINANCING | objet, montant, apport, ville, type_bien | revenus, employeur, terrain, permis | "prêt approuvé", codes bancaires |
| PROFESSIONAL | type_prestation, localisation, description, urgence, date | qualification, assurance, portfolio | age, situation matrimoniale |
| SERVICES | service_type, localisation, description | specialisation, équipement, certification | residential criteria |

---

**End of CONDITIONAL_QUESTION_RULES.md**
