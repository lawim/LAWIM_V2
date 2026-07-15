# ALIAS RESOLUTION CONTRACT — Language Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** LANGUAGE_EXECUTION_ARCHITECTURE.md, NORMALIZATION_PIPELINE.md, AMBIGUITY_HANDLING_POLICY.md, LANGUAGE_MODEL.md, LANGUAGE_BUSINESS_KNOWLEDGE.md, RULE_INDEX.md (LANG-005, LANG-006)

---

## 1. Alias Resolution Overview

The Alias Resolution module normalizes variant forms of entities (property types, locations, abbreviations, misspellings) to their canonical representations. It is called during Stage 5 of the NORMALIZATION_PIPELINE and is a prerequisite for entity extraction (Stage 6).

---

## 2. Alias Resolution Priority

Resolution is applied in strict priority order. Once an alias is resolved, lower-priority methods are not attempted for that token.

```
INPUT: token (string)
    │
    ▼
┌──────────────────────────────────────────────────────────────┐
│ 1. EXACT MATCH      Priority: P0                             │
│    Match against canonical entity list                       │
│    If found → return canonical, confidence = 1.0             │
│    (No alias resolution needed)                              │
└────────────────────────────────┬─────────────────────────────┘
                                 │ not found
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. TYPO CORRECTION    Priority: P1 (LANG-006)                │
│    Match against 5 typo databases                            │
│    If found → return canonical, confidence = 0.85            │
└────────────────────────────────┬─────────────────────────────┘
                                 │ not found
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. SYNONYM RESOLUTION  Priority: P2                          │
│    Match against entity_linking.json synonym entries         │
│    If found → return canonical, confidence = 0.95            │
└────────────────────────────────┬─────────────────────────────┘
                                 │ not found
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. ABBREVIATION EXPANSION  Priority: P3                      │
│    Match against abbreviation lists                          │
│    If found → return expanded canonical, confidence = 0.90   │
└────────────────────────────────┬─────────────────────────────┘
                                 │ not found
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. ENTITY LINKING       Priority: P4 (LANG-005)              │
│    Cross-language and concept linking                        │
│    If found → return linked canonical, confidence = 0.80     │
└────────────────────────────────┬─────────────────────────────┘
                                 │ not found
                                 ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. LEVENSHTEIN FUZZY   Priority: P5                          │
│    Levenshtein distance ≤ 3 against all known terms          │
│    d≤1 → confidence = 0.80                                   │
│    d≤2 → confidence = 0.70                                   │
│    d≤3 → confidence = 0.60                                   │
└─────────────────────────────────────────────────────────────┘
```

### 2.1 Resolution Priority Table

| Priority | Method | Source | Confidence | Example |
|----------|--------|--------|------------|---------|
| P0 | Exact match | Canonical entity list | 1.0 | "appartement" → APT |
| P1 | Typo correction | 5 typo databases (LANG-006) | 0.85 | "appart" → appartement |
| P2 | Synonym resolution | entity_linking.json (LANG-005) | 0.95 | "office" → bureau |
| P3 | Abbreviation expansion | abbreviation lists | 0.90 | "YDE" → Yaoundé |
| P4 | Entity linking | entity_linking.json (LANG-005) | 0.80 | "parking" → stationnement |
| P5 | Levenshtein fuzzy | All known terms | 0.60–0.80 | "yaonde" → Yaoundé |

---

## 3. Alias Types

### 3.1 Relation Types

| Relation | Definition | Example | Source |
|----------|------------|---------|--------|
| `equivalent_to` | Direct equivalence between terms | terrain ↔ parcelle | entity_linking.json |
| `synonym` | Cross-language or regional synonym | bureau ↔ office | entity_linking.json |
| `related_to` | Related concept (not exact synonym) | parking ↔ stationnement | entity_linking.json |
| `typo_of` | Common misspelling → canonical | appartemant → appartement | typo_database.json |
| `abbreviation_of` | Abbreviation → full form | appt → appartement | abbreviations.json |

### 3.2 Relation Type Usage

| Domain | equivalent_to | synonym | related_to | typo_of | abbreviation_of |
|--------|---------------|---------|------------|---------|-----------------|
| Property Types | 5 | 7 | 0 | 9 | 2 |
| Cities | 0 | 0 | 0 | 10 | 10 |
| Neighborhoods | 0 | 0 | 0 | 6 | 0 |
| General Terms | 3 | 8 | 2 | 5 | 3 |

---

## 4. Entity Linking Structure (LANG-005)

### 4.1 Core Entity Linking (20 pairs from entity_linking.json)

```json
{
  "source_term": "terrain",
  "target_term": "parcelle",
  "relation_type": "equivalent_to",
  "confidence": 1.0,
  "domain": "property"
}
```

| Source | Target | Relation | Domain | Confidence |
|--------|--------|----------|--------|------------|
| terrain | parcelle | equivalent_to | property | 1.0 |
| villa | maison de luxe | equivalent_to | property | 1.0 |
| appartement | appart | abbreviation_of | property | 1.0 |
| commerce | boutique | equivalent_to | property | 1.0 |
| bureau | office | synonym | property | 1.0 |
| immeuble | building | synonym | property | 1.0 |
| studio | one-room | equivalent_to | property | 1.0 |
| entrepôt | warehouse | synonym | property | 1.0 |
| climatisation | AC | abbreviation_of | amenity | 1.0 |
| parking | stationnement | related_to | amenity | 1.0 |
| piscine | swimming pool | synonym | amenity | 1.0 |
| gardien | security | synonym | amenity | 1.0 |
| meublé | furnished | synonym | property | 1.0 |
| non meublé | unfurnished | synonym | property | 1.0 |
| titre foncier | land title | synonym | legal | 1.0 |
| notaire | lawyer | related_to | legal | 1.0 |
| bail | lease | synonym | legal | 1.0 |
| caution | deposit | synonym | financial | 1.0 |
| agence | agency | synonym | crm | 1.0 |
| commission | fee | synonym | financial | 1.0 |

### 4.2 Entity Linking Processing

```
FUNCTION resolve_entity(token, language):
    INPUT: token (string), language (FR|EN|PID)
    OUTPUT: { resolved_term, relation_type, confidence, domain }

    normalized = lowercase(strip_diacritics(trim(token)))

    # P0: Exact match in canonical entity list
    IF normalized IN canonical_entities:
        RETURN { resolved_term: normalized, relation_type: "exact", confidence: 1.0, domain: canonical_entities[normalized].domain }

    # P1: Typo database match (LANG-006)
    typo_result = check_typo_databases(normalized)
    IF typo_result.found:
        RETURN { resolved_term: typo_result.canonical, relation_type: "typo_of", confidence: 0.85, domain: typo_result.domain }

    # P2: Synonym match in entity_linking
    syn_result = check_synonyms(normalized)
    IF syn_result.found:
        RETURN { resolved_term: syn_result.canonical, relation_type: "synonym", confidence: 0.95, domain: syn_result.domain }

    # P3: Abbreviation expansion
    abbr_result = expand_abbreviation(normalized)
    IF abbr_result.found:
        RETURN { resolved_term: abbr_result.expansion, relation_type: "abbreviation_of", confidence: 0.90, domain: abbr_result.domain }

    # P4: Cross-language entity linking
    link_result = check_entity_linking(normalized)
    IF link_result.found:
        RETURN { resolved_term: link_result.target, relation_type: link_result.relation, confidence: 0.80, domain: link_result.domain }

    # P5: Levenshtein fuzzy match
    fuzzy_result = fuzzy_match(normalized, all_known_terms, max_distance=3)
    IF fuzzy_result.found:
        conf = [0.80, 0.70, 0.60][fuzzy_result.distance - 1]
        RETURN { resolved_term: fuzzy_result.term, relation_type: "typo_of", confidence: conf, domain: fuzzy_result.domain }

    # No resolution
    RETURN { resolved_term: token, relation_type: "unresolved", confidence: 0.30, domain: "unknown" }
```

---

## 5. Geographic Alias Resolution

### 5.1 City Alias Resolution

Resolves city name variants (typos, abbreviations, social variants) to canonical city IDs:

| Variant | Canonical | Method | Confidence |
|---------|-----------|--------|------------|
| yaound, yaoundee, yaonde | Yaoundé | typo_of | 0.85 |
| YDE | Yaoundé | abbreviation_of | 0.90 |
| doula, doualaa, duala | Douala | typo_of | 0.85 |
| DLA | Douala | abbreviation_of | 0.90 |
| bamnda, bameda | Bamenda | typo_of | 0.85 |
| BDA | Bamenda | abbreviation_of | 0.90 |
| bafousam, bafossam | Bafoussam | typo_of | 0.85 |
| BFS | Bafoussam | abbreviation_of | 0.90 |
| bueaa, bua, bueah | Buea | typo_of | 0.85 |
| BUE | Buea | abbreviation_of | 0.90 |

**City Canonical Forms (10 cities):**

| Canonical | Region | Canonical ID |
|-----------|--------|-------------|
| Yaoundé | Centre | CM-YAO |
| Douala | Littoral | CM-DLA |
| Bamenda | Nord-Ouest | CM-BDA |
| Bafoussam | Ouest | CM-BFS |
| Buea | Sud-Ouest | CM-BUE |
| Kribi | Sud | CM-KRI |
| Nkongsamba | Littoral | CM-NKS |
| Maroua | Extrême-Nord | CM-MRA |
| Limbe | Sud-Ouest | CM-LIM |
| Garoua | Nord | CM-GAR |

### 5.2 Neighborhood Alias Resolution

| Variant | Canonical | Method | Confidence |
|---------|-----------|--------|------------|
| odza3, odzaa, odaz | Odza | typo_of | 0.85 |
| makepe3, makep, makpe | Makepe | typo_of | 0.85 |
| bonapriso3, bonapreso | Bonapriso | typo_of | 0.85 |
| akwa3, akwaa, akw | Akwa | typo_of | 0.85 |
| bastos3, bastosa, basto | Bastos | typo_of | 0.85 |
| mendong3, mendng | Mendong | typo_of | 0.85 |

### 5.3 District Alias Resolution (33 entries from aliases.json)

| Source District | Canonical District | City |
|----------------|--------------------|------|
| Bependa Omnisport | Bepanda Omnisports | Douala |
| Bonamoussadi Cité | Bonamoussadi | Douala |
| Bonamouti-Akwa 2 | Bonamouti | Douala |
| Centre Ville | Centre | Douala |
| Messa Administratif | Messa | Douala |
| Messa Doumassi | Messa | Douala |
| Messa Ekoazon | Messa | Douala |
| Messa Plateau | Messa | Douala |
| Messa-Carrière | Messa | Douala |
| Nkomkana I, II | Nkomkana | Douala |
| Nsimeyong I, II | Nsimeyong | Yaoundé |
| Nouvelle zone d'Akwa Nord | Akwa Nord | Douala |
| Nouvelle zone de New-Deido | New Deido | Douala |
| Small Soppo-Wonganga | Small Soppo | Buea |
| Small Soppo-Woteke | Small Soppo | Buea |
| Small Soppo-Wovila | Small Soppo | Buea |
| Lower Bolifamba | Bolifamba | Buea |
| Upper Muea | Muea | Buea |
| Lower Bokova | Bokova | Buea |
| Federal Quarters | Government Residential Area | Buea |
| Old-Government Station | Government Residential Area | Buea |
| Clerk's Quarter | Government Residential Area | Buea |
| Bonakeke Akwa | Akwa | Douala |
| New-Bell Bandjoun | New-Bell | Douala |

---

## 6. Property Type Alias Resolution

### 6.1 Complete Alias Mappings (11 types)

| Canonical FR | Canonical ID | Aliases (EN + FR + abbreviations + variants) |
|-------------|-------------|------------------------------------------------------|
| appartement | APT | appart, appt, apartment, flat, apart, apparte, appartement3, appartment, apartement |
| studio | STU | flat, efficiency, chambre meublée, stud, studeo, studyo, studios, studio3, studio_ |
| chambre | CHB | room, chb, cham, chambre meublée, chambre à louer, chambre seule, bedroom, single room, chamb, chbres |
| maison | MSN | house, home, msn, maisonnette, villa, mason, maisn, maisoon, maizone |
| villa | VIL | luxury house, villa de luxe, luxury home, villa3, vlla, villla, villa_ |
| terrain | TER | land, plot, parcel, lot, ground, ter, terrain nu, terrains, terain, terraine |
| local commercial | COM | boutique, shop, magasin, commerce, store, local, commercial space |
| bureau | BUR | office, buro, workspace, cabinet, bureaux, breaux |
| immeuble | IMM | building, apartment building, immeuble3, imuble, immuble |
| dépôt/entrepôt | DEP | warehouse, storage, hangar, dépôt de marchandises |
| terrain constructible | TER_CONST | buildable land, building plot, terrain à bâtir, terrain viabilisé |

### 6.2 Property Type Normalisation (EN → FR Canonical ID)

| English Variant | Normalised French ID |
|-----------------|---------------------|
| apartment, flat | APT (Appartement) |
| studio, efficiency | STU (Studio) |
| room, single room | CHB (Chambre) |
| furnished room | CHB_MEUBLEE |
| house, home | MSN (Maison) |
| villa, luxury home | VIL (Villa) |
| land, plot, parcel, lot | TER (Terrain) |
| buildable land, building plot | TER_CONST (Terrain Constructible) |
| commercial space, shop | COM (Local Commercial) |
| office, workspace | BUR (Bureau) |
| warehouse, storage | DEP (Dépôt / Entrepôt) |
| building, apartment building | IMM (Immeuble) |

### 6.3 Property Type Typo Direct Mappings

| Typo | Canonical | Source |
|------|-----------|--------|
| appartemant | appartement | property_types_typo.json |
| appartementt | appartement | property_types_typo.json |
| maisn | maison | property_types_typo.json |
| maisoon | maison | property_types_typo.json |
| terin | terrain | property_types_typo.json |
| terrian | terrain | property_types_typo.json |
| terain | terrain | property_types_typo.json |
| teraine | terrain | property_types_typo.json |
| vilaa | villa | property_types_typo.json |
| vilage | maison | property_types_typo.json |
| studeo | studio | property_types_typo.json |
| studyo | studio | property_types_typo.json |
| bereau | bureau | property_types_typo.json |
| immuble | immeuble | property_types_typo.json |

---

## 7. Alias Resolution Examples (Cameroon Context)

### Example 1: Property Type Alias

**Input:** "je cherche un **appart** 3 pieces a DLA"

**Resolution Steps:**
```
1. Token: "appart"
   → P1 Typo correction: match in property_types_typo.json
   → Canonical: "appartement"
   → Canonical ID: APT
   → Confidence: 0.85

2. Token: "DLA"
   → P3 Abbreviation expansion: match in city_abbreviations
   → Canonical: "Douala"
   → Canonical ID: CM-DLA
   → Confidence: 0.90
```

**Output:**
```json
{
  "resolved_intent": "je cherche un appartement 3 pieces a douala",
  "entities": [
    {"original": "appart", "resolved": "appartement", "id": "APT", "relation": "typo_of", "confidence": 0.85},
    {"original": "DLA", "resolved": "Douala", "id": "CM-DLA", "relation": "abbreviation_of", "confidence": 0.90}
  ]
}
```

### Example 2: Cross-Language Synonym

**Input:** "i want to buy **land** in **buea**"

**Resolution Steps:**
```
1. Token: "land"
   → P4 Entity linking: match in search_aliases.json
   → Canonical: "terrain"
   → Canonical ID: TER
   → Relation: synonym
   → Confidence: 0.95

2. Token: "buea"
   → P0 Exact match: found in city list
   → Canonical: "Buea"
   → Canonical ID: CM-BUE
   → Confidence: 1.0
```

**Output:**
```json
{
  "resolved_intent": "i want to buy terrain in buea",
  "entities": [
    {"original": "land", "resolved": "terrain", "id": "TER", "relation": "synonym", "confidence": 0.95},
    {"original": "buea", "resolved": "Buea", "id": "CM-BUE", "relation": "exact", "confidence": 1.0}
  ]
}
```

### Example 3: Neighborhood Variant

**Input:** "je cherche chambre a **bastos3**"

**Resolution Steps:**
```
1. Token: "chambre"
   → P0 Exact match: canonical term
   → Canonical ID: CHB
   → Confidence: 1.0

2. Token: "bastos3"
   → P1 Typo correction: match in neighborhoods_typo.json
   → Canonical: "Bastos"
   → Relation: typo_of
   → Confidence: 0.85
```

**Output:**
```json
{
  "resolved_intent": "je cherche chambre a bastos",
  "entities": [
    {"original": "chambre", "resolved": "chambre", "id": "CHB", "relation": "exact", "confidence": 1.0},
    {"original": "bastos3", "resolved": "Bastos", "relation": "typo_of", "confidence": 0.85}
  ]
}
```

### Example 4: Abbreviation + Entity Linking

**Input:** "**bureau** **TF** a **YDE**"

**Resolution Steps:**
```
1. Token: "bureau"
   → P0 Exact match: canonical term
   → Canonical ID: BUR
   → Confidence: 1.0

2. Token: "TF"
   → P3 Abbreviation expansion: "titre foncier"
   → Confidence: 0.90

3. Token: "YDE"
   → P3 Abbreviation expansion: "Yaoundé"
   → Canonical ID: CM-YAO
   → Confidence: 0.90
```

**Output:**
```json
{
  "resolved_intent": "bureau titre foncier a yaoundé",
  "entities": [
    {"original": "bureau", "resolved": "bureau", "id": "BUR", "relation": "exact", "confidence": 1.0},
    {"original": "TF", "resolved": "titre foncier", "relation": "abbreviation_of", "confidence": 0.90},
    {"original": "YDE", "resolved": "Yaoundé", "id": "CM-YAO", "relation": "abbreviation_of", "confidence": 0.90}
  ]
}
```

### Example 5: Pidgin + Misspelling

**Input:** "i **wan** **buy** **terain** for **bamnda**"

**Resolution Steps:**
```
1. Token: "i wan"
   → P0 Exact match (bigram): Pidgin buy expression
   → Intent hint: BUY
   → Confidence: 1.0

2. Token: "buy"
   → P0 Exact match: English verb for BUY intent
   → Confidence: 1.0

3. Token: "terain"
   → P1 Typo correction: match in property_types_typo.json
   → Canonical: "terrain"
   → Canonical ID: TER
   → Confidence: 0.85

4. Token: "bamnda"
   → P5 Levenshtein fuzzy: distance 1 from "Bamenda"
   → Canonical: "Bamenda"
   → Canonical ID: CM-BDA
   → Confidence: 0.80
```

**Output:**
```json
{
  "resolved_intent": "i wan buy terrain for bamenda",
  "intent": "BUY",
  "entities": [
    {"original": "terain", "resolved": "terrain", "id": "TER", "relation": "typo_of", "confidence": 0.85},
    {"original": "bamnda", "resolved": "Bamenda", "id": "CM-BDA", "relation": "typo_of", "confidence": 0.80}
  ]
}
```

---

## 8. Confidence Calculation for Resolved Aliases

### 8.1 Base Confidence by Method

| Method | Base Confidence | Description |
|--------|----------------|-------------|
| Exact match | 1.0 | Token matches canonical entity directly |
| Typo database match | 0.85 | Token found in typo_database/*.json |
| Synonym resolution | 0.95 | Token found in search_aliases or entity_linking as synonym |
| Abbreviation expansion | 0.90 | Token found in abbreviation list |
| Entity linking (cross-language) | 0.80 | Token linked via relation_type |
| Levenshtein d=1 | 0.80 | Single character difference |
| Levenshtein d=2 | 0.70 | Two character difference |
| Levenshtein d=3 | 0.60 | Three character difference |
| No resolution | 0.30 | Token unrecognized |

### 8.2 Confidence Modifiers

| Condition | Modifier | Example |
|-----------|----------|---------|
| Multiple sources agree | +0.05 | Typo DB + Levenshtein agree |
| Source matched is low-quality | -0.10 | User-generated typo database |
| Token is very short (< 3 chars) | -0.10 | "M" could be million or maison |
| Token is numeric | -0.20 | Cannot reliably alias numbers |
| Ambiguous match (multiple candidates) | -0.15 | Token maps to 2+ canonical forms |
| Session context confirms alias | +0.05 | Previous turn used same alias |
| User correction applied earlier | +0.10 | User confirmed this alias previously |

### 8.3 Composite Confidence Formula

```
final_confidence = base_confidence + sum(modifiers)
final_confidence = clamp(final_confidence, 0.0, 1.0)
```

### 8.4 Confidence Tiers

| Tier | Range | Action |
|------|-------|--------|
| HIGH | ≥ 0.85 | Accept alias, proceed with full confidence |
| MEDIUM | 0.70 – 0.84 | Accept alias, flag for review if context uncertain |
| LOW | 0.50 – 0.69 | Accept provisionally, request confirmation in qualification |
| VERY LOW | < 0.50 | Keep original token, request clarification |

---

## 9. Domain-Specific Alias Resolution

### 9.1 Property Domain

| Domain | Canonical Sources | Alias Files |
|--------|------------------|-------------|
| Property Types | property_type_aliases.json | property_types_typo.json |
| Amenities | entity_linking.json | typo_database.json |
| Legal Terms | entity_linking.json | abbreviations.json |

### 9.2 Geographic Domain

| Domain | Canonical Sources | Alias Files |
|--------|------------------|-------------|
| Cities | cities.json | cities_typo.json, city_abbreviations |
| Neighborhoods | neighborhoods/*.json | neighborhoods_typo.json |
| Districts | aliases.json | aliases.json |

### 9.3 Financial Domain

| Domain | Canonical Sources | Alias Files |
|--------|------------------|-------------|
| Currency | FCFA, Franc CFA, XAF | abbreviations.json |
| Pricing | M, k, million, mille | amount_expressions.json |

### 9.4 Legal Domain

| Domain | Canonical Sources | Alias Files |
|--------|------------------|-------------|
| Documents | TF, titre foncier, PU, CU | abbreviations.json |
| Roles | notaire, propriétaire, agent | entity_linking.json |

---

## 10. Integration with Other Components

### 10.1 Input Contract

```json
{
  "token": "appart",
  "context": {
    "language": "FR",
    "domain": "property_type",
    "session_occurrences": 3,
    "previous_resolutions": ["appartement"]
  }
}
```

### 10.2 Output Contract

```json
{
  "resolved_term": "appartement",
  "canonical_id": "APT",
  "relation_type": "typo_of",
  "confidence": 0.85,
  "domain": "property",
  "resolution_method": "typo_database_match",
  "source_file": "property_types_typo.json"
}
```

### 10.3 Error States

| Error | Condition | Output |
|-------|-----------|--------|
| `unresolved_term` | No alias found | Return original token, confidence 0.30 |
| `ambiguous_match` | Multiple canonical matches | Return top candidate, set ambiguity flag |
| `low_confidence_all` | All candidates < 0.50 | Return original token with best-effort confidence |
| `cyclic_alias` | A → B → A resolution loop | Break at first resolution, log cycle |
