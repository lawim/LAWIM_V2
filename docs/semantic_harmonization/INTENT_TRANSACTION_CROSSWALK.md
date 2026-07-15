# Intent & Transaction Crosswalk: Heritage Gold → LAWIM_V2

| Attribute | Value |
|-----------|-------|
| **Document ID** | LAWIM-HARM-INTENT-TRX-CROSSWALK-V1 |
| **Status** | DRAFT |
| **Date** | 2026-07-15 |
| **Sources** | `INTENT_MODEL.md`, `DOMAIN_MODEL.md`, `MATRIX_CATALOG.md`, `QUALIFICATION_MODEL.md`, `WORKFLOW_EXTRACTION_COMPLETE.md` (Gold); `project_domain.py`, `conversation_domain.py`, `schema.prisma` (V2) |

---

## Mapping Status Reference

| Status | Definition |
|--------|-----------|
| EXACT_MATCH | Identical semantics and representation |
| NORMALIZED_MATCH | Same concept, different representation (case, format, naming) |
| ONE_TO_MANY | One source entity maps to multiple target entities |
| MANY_TO_ONE | Multiple source entities map to one target entity |
| PARTIAL_MATCH | Partial semantic overlap; some aspects covered, others missing |
| EXTENSION_REQUIRED | Concept does not exist in target; requires new development |
| OBSOLETE | Concept no longer relevant or deliberately removed |
| CONFLICT | Semantics conflict between source and target |
| HUMAN_DECISION_REQUIRED | Mapping requires domain expert judgment |
| UNMAPPED | No equivalent concept identified |

---

## 1. Intent Model Comparison

### Heritage Gold (5 Primary Intents)

| Intent ID | Label FR | Label EN | Priority | Lead Score Weight | Detection |
|-----------|----------|----------|----------|-------------------|-----------|
| BUY_PROPERTY | Achat | Buy | VERY_HIGH | 50 | Keyword scoring ≥ 0.70 |
| RENT_PROPERTY | Location | Rent | HIGH | 30 | Keyword scoring ≥ 0.70 |
| SELL_PROPERTY | Vente | Sell | VERY_HIGH | 60 | Keyword scoring ≥ 0.70 |
| INVESTOR_INTENT | Investissement | Invest | P0 | 100 | Keyword scoring ≥ 0.70 |
| SEARCH_PROPERTY | Recherche | Search | NORMAL | 25 | Fallback < 0.70 |

### LAWIM_V2 Current (6 Project Types)

Defined in `project_domain.py:8`:

```python
PROJECT_TYPES = frozenset({"buy", "rent", "sell", "invest", "build", "other"})
```

No formal Intent model exists; intent is represented implicitly via `project_type`.

### Mapping Table

| Gold Intent ID | Current Equivalent | Mapping Status | Rationale |
|----------------|-------------------|----------------|-----------|
| BUY_PROPERTY | `project_type = "buy"` | NORMALIZED_MATCH | Same semantics; Gold uses INTENT model (UPPER_SNAKE_CASE with priority/weight), V2 uses lowercase string field |
| RENT_PROPERTY | `project_type = "rent"` | NORMALIZED_MATCH | Same semantics; tenant-side rental intent |
| SELL_PROPERTY | `project_type = "sell"` | NORMALIZED_MATCH | Same semantics; owner-side sales intent |
| INVESTOR_INTENT | `project_type = "invest"` | NORMALIZED_MATCH | Same semantics; priority label differs (P0 vs VERY_HIGH) |
| SEARCH_PROPERTY | `project_type = "other"` | PARTIAL_MATCH | Gold has explicit search fallback intent; V2 catch-all "other" lacks confidence semantics and fallback logic |
| — | `project_type = "build"` | EXTENSION_REQUIRED | Gold has no build intent; V2 extends with construction project lifecycle |

---

## 2. Transaction Type Comparison

### Heritage Gold Transaction Types

From `DOMAIN_MODEL.md` and `MATRIX_CATALOG.md`:

| Transaction | Description | Matrix Families |
|-------------|-------------|-----------------|
| rent | Location d'un bien immobilier | RESIDENTIAL_SEARCH |
| buy | Acquisition d'un bien immobilier | RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH |
| sell | Mise en vente d'un bien immobilier | — |
| short_stay | Séjour de courte durée | RESIDENTIAL_SEARCH (courte durée) |
| invest | Investissement immobilier | COMMERCIAL_SEARCH (Investment) |
| lease | Location longue durée (bail 3+ ans) | — |
| cession_bail | Cession de bail commercial | COMMERCIAL_SEARCH |
| bail_commercial | Bail commercial (3-9 ans) | COMMERCIAL_SEARCH |
| cession | Cession de fonds de commerce | COMMERCIAL_SEARCH |
| finance | Demande de financement immobilier | FINANCING_REQUEST (10 matrices) |
| find | Recherche de professionnel | PROFESSIONAL_SEARCH (27 matrices) |
| service | Prestation de service immobilier | REAL_ESTATE_SERVICES (24 matrices) |

### LAWIM_V2 Project Types

From `project_domain.py:8`:

```python
PROJECT_TYPES = frozenset({"buy", "rent", "sell", "invest", "build", "other"})
```

### Mapping Table

| Gold Transaction | Current Equivalent | Mapping Status | Rationale |
|------------------|-------------------|----------------|-----------|
| rent | `project_type = "rent"` | EXACT_MATCH | Identical semantics |
| buy | `project_type = "buy"` | EXACT_MATCH | Identical semantics |
| sell | `project_type = "sell"` | EXACT_MATCH | Identical semantics |
| invest | `project_type = "invest"` | EXACT_MATCH | Identical semantics |
| short_stay | `project_type = "rent"` + metadata | PARTIAL_MATCH | Sub-differentiated within rent; no dedicated short_stay type |
| lease | `project_type = "rent"` + `timeline_horizon` | PARTIAL_MATCH | timeline_horizon maxes at "2_years"; lease requires 3+ years |
| cession_bail | `project_type = "other"` | EXTENSION_REQUIRED | No equivalent; commercial lease transfer |
| bail_commercial | `project_type = "rent"` | PARTIAL_MATCH | Bail commercial (3-9 ans) has unique legal requirements not captured |
| cession | `project_type = "other"` | EXTENSION_REQUIRED | No equivalent; business asset transfer |
| finance | `project_type = "buy"/"invest"` (bundled) | EXTENSION_REQUIRED | No standalone financing request type; 10 matrices unmapped |
| find | `project_type = "other"` | EXTENSION_REQUIRED | No professional search type; 27 matrices unmapped |
| service | `project_type = "other"` | EXTENSION_REQUIRED | No service procurement type; 24 matrices unmapped |

### Key Discovery: 107 Qualification Matrices vs 6 Project Types

Heritage Gold defines **107 qualification matrices** across **7 families** (RESIDENTIAL_SEARCH, LAND_SEARCH, COMMERCIAL_SEARCH, FINANCING_REQUEST, PROFESSIONAL_SEARCH, REAL_ESTATE_SERVICES) mapped to **12 transaction types**. LAWIM_V2 has **6 project types** with no matrix-level granularity. This represents a significant granularity gap.

---

## 3. Intent-to-Role Mapping Comparison

### Heritage Gold

| Intent | Role | Role Type | Side |
|--------|------|-----------|------|
| BUY_PROPERTY | buyer | Demandeur | Demand |
| RENT_PROPERTY | tenant | Demandeur | Demand |
| SELL_PROPERTY | seller | Propriétaire | Supply |
| INVESTOR_INTENT | investor | Demandeur / Investisseur | Demand/Investment |
| SEARCH_PROPERTY | visitor | Demandeur (unqualified) | Demand (fallback) |

### LAWIM_V2 Current

**No formal role mapping exists.** The user's role is implicit in the `project_type` they select:
- `buy` → user is implicitly a buyer
- `rent` → user is implicitly a tenant
- `sell` → user is implicitly a seller
- `invest` → user is implicitly an investor

There is no Role model, no role type classification (Demandeur/Propriétaire/Investisseur), and no role-based access control tied to intent.

### Mapping Table

| Gold Intent | Gold Role | Gold Role Type | Current | Mapping Status |
|-------------|-----------|----------------|---------|----------------|
| BUY_PROPERTY | buyer | Demandeur | Implicit via project_type | EXTENSION_REQUIRED |
| RENT_PROPERTY | tenant | Demandeur | Implicit via project_type | EXTENSION_REQUIRED |
| SELL_PROPERTY | seller | Propriétaire | Implicit via project_type | EXTENSION_REQUIRED |
| INVESTOR_INTENT | investor | Demandeur / Investisseur | Implicit via project_type | EXTENSION_REQUIRED |
| SEARCH_PROPERTY | visitor | Demandeur (unqualified) | Not represented | EXTENSION_REQUIRED |

**All role mappings require formal extension.** The Heritage Gold role abstraction (especially the demand/supply distinction and the unqualified visitor role) is entirely absent.

---

## 4. Intent Detection Comparison

### Heritage Gold

| Feature | Detail |
|---------|--------|
| **Method** | Keyword scoring with confidence threshold |
| **Threshold** | 0.70 |
| **Languages** | FR, EN, PID (Pidgin) |
| **Algorithm** | Rule-based keyword scoring |
| **Multi-intent** | Supported — user can express multiple intents in one utterance |
| **Urgency** | Detected and scored |
| **Entity extraction** | Per intent (budget, location, property type, timeline) |
| **Fallback** | SEARCH_PROPERTY when confidence < 0.70 |
| **Score weights** | BUY=50, RENT=30, SELL=60, INVEST=100, SEARCH=25 |

### LAWIM_V2 Current

| Feature | Detail |
|---------|--------|
| **Method** | None — explicit `project_type` selection by user |
| **Threshold** | N/A |
| **Languages** | N/A |
| **Algorithm** | None |
| **Multi-intent** | Not supported |
| **Urgency** | Not detected |
| **Entity extraction** | Not implemented |
| **Fallback** | Not implemented |
| **Score weights** | Not implemented |

### Mapping Status: **EXTENSION_REQUIRED**

The entire intent detection pipeline is absent from LAWIM_V2 and requires new development. The current model relies on the user explicitly selecting a project type from a dropdown or form field.

### Recommendation

Implement an intent detection module with:
1. **Keyword-based intent classifier** with configurable confidence threshold (target 0.70)
2. **FR/EN/PID language support** using keyword dictionaries per language
3. **Multi-intent detection** allowing parallel project creation
4. **Urgency scoring** from temporal keywords
5. **Entity extraction** per intent (budget amounts, location names, property types, timeframes)
6. **Fallback to `other` (or new `search` intent)** when confidence < 0.70
7. **Lead score weight integration** for agent routing and prioritization

---

## 5. Journey / Workflow Stage Mapping

### Heritage Gold Journey Stages

From `WORKFLOW_EXTRACTION_COMPLETE.md`:

```
SEARCH → QUALIFICATION → MATCHING → VISIT → NEGOTIATION → TRANSACTION → CLOSURE → ARCHIVING
```

### Heritage Gold Qualification Order (10-Step)

From `QUALIFICATION_MODEL.md`:

```
1. Intention → 2. Type bien → 3. Ville → 4. Quartier → 5. Budget →
6. Délai → 7. Critères → 8. Préférences → 9. Confirmation → 10. Escalade
```

### LAWIM_V2 Journey Step Templates

| project_type | Steps |
|-------------|-------|
| buy | qualification → search → visit → negotiation → closing |
| rent | qualification → search → visit → negotiation → closing |
| sell | qualification → preparation → promotion → negotiation → closing |
| invest | qualification → analysis → search → due_diligence → closing |
| build | qualification → land → design → construction → closing |
| other | qualification → planning → execution → review → closing |

### Mapping Table

| Gold Stage | Current Equivalent | Applies To | Mapping Status | Rationale |
|------------|-------------------|------------|----------------|-----------|
| SEARCH | `search` step | buy, rent, invest | EXACT_MATCH | Direct step mapping |
| QUALIFICATION | `qualification` step | ALL types | EXACT_MATCH | Universal first step; Gold 10-step order is richer |
| MATCHING | `search` (buy/rent) / `promotion` (sell) | buy, rent, sell | PARTIAL_MATCH | Split across search (demand) and promotion (supply) |
| VISIT | `visit` step | buy, rent | EXACT_MATCH | Not present in sell/invest/build journeys |
| NEGOTIATION | `negotiation` step + `negotiationStage` | buy, rent, sell | PARTIAL_MATCH | V2 adds substages (inquiry→offer→counter→accepted/declined→closed) not in Gold |
| TRANSACTION | `due_diligence` (invest) / `closing` (partial) | invest, all | PARTIAL_MATCH | Distributed; Gold has distinct execution phase |
| CLOSURE | `closing` step | ALL types | EXACT_MATCH | Universal terminal step |
| ARCHIVING | `status = "archived"` | ALL types | EXACT_MATCH | Terminal project status |

### Negotiation Stage Sub-Mapping

Heritage Gold has no negotiation substages; LAWIM_V2 defines a rich substate model in `conversation_domain.py:3`:

```
inquiry → offer → counter → accepted / declined → closed
```

| Gold Stage | V2 Negotiation Stage | Mapping Status | Rationale |
|------------|---------------------|----------------|-----------|
| NEGOTIATION (entry) | inquiry | PARTIAL_MATCH | Gold treats negotiation as atomic; V2 splits into substages |
| NEGOTIATION (resolution) | accepted / declined / closed | PARTIAL_MATCH | Gold has no distinction between outcomes |

---

## 6. Gap Analysis

### Gap Summary

| # | Gap ID | Priority | Domain | Description |
|---|--------|----------|--------|-------------|
| 1 | GAP-001 | CRITICAL | Intent Detection | No intent detection system; relies on explicit project_type selection |
| 2 | GAP-002 | HIGH | Intent Model | No formal Intent model with priority, lead score weights, or status |
| 3 | GAP-003 | HIGH | Transaction Types | 7 of 12 Gold transaction types unmapped (short_stay, lease, cession_bail, bail_commercial, cession, finance, find, service) |
| 4 | GAP-004 | HIGH | Role Mapping | No intent-to-role mapping; roles are implicit and unstructured |
| 5 | GAP-005 | MEDIUM | Urgency Detection | No urgency scoring from user input |
| 6 | GAP-006 | MEDIUM | Entity Extraction | No per-intent entity extraction for qualification auto-population |
| 7 | GAP-007 | MEDIUM | Multi-Intent | Cannot handle users with multiple parallel intents |
| 8 | GAP-008 | MEDIUM | Qualification Order | Gold's 10-step progressive disclosure not implemented |
| 9 | GAP-009 | LOW | Search Fallback | No confidence-based fallback to search intent |
| 10 | GAP-010 | LOW | Lead Scoring | Lead score weights not integrated for routing/prioritization |

### Gap Distribution

```
CRITICAL  ██  1
HIGH      ██████  4
MEDIUM    █████  3
LOW       ███  2
Total:    10 gaps
```

### Quick Reference: What Maps Cleanly vs What Requires Extension

| Maps Cleanly (NORMALIZED_MATCH or better) | Requires Extension (PARTIAL_MATCH or worse) |
|---------------------------------------------|----------------------------------------------|
| BUY_PROPERTY → buy | SEARCH_PROPERTY → other |
| RENT_PROPERTY → rent | short_stay → no direct type |
| SELL_PROPERTY → sell | lease → no direct type |
| INVESTOR_INTENT → invest | cession_bail, bail_commercial, cession → no types |
| rent, buy, sell, invest (transaction types) | finance → no type |
| SEARCH, QUALIFICATION, VISIT, CLOSURE, ARCHIVING (stages) | find, service → no types |
| negotiation step (partial) | Intent detection → entire pipeline missing |
| | Intent-to-role mapping → entirely absent |
| | Multi-intent, urgency, entity extraction → missing |
| | 10-step qualification order → not implemented |

---

## 7. Recommendations (Priority Order)

1. **Implement intent detection module** (GAP-001) — critical path dependency for all downstream features
2. **Extend PROJECT_TYPES** (GAP-003) — add `lease`, `short_stay`, `finance`, `find`, `service`; handle cession variants via metadata
3. **Introduce Intent & Role models** (GAP-002, GAP-004) — formalize intents with priority/weight and role mapping
4. **Add entity extraction** (GAP-006) — per-intent extraction of budget, location, property type, timeline
5. **Build multi-intent support** (GAP-007) — parallel project creation from single user utterance
6. **Implement qualification wizard** (GAP-008) — 10-step progressive disclosure per Heritage Gold order
7. **Add urgency scoring** (GAP-005) — lightweight keyword-based urgency detection
8. **Integrate lead scoring** (GAP-010) — route and prioritize based on intent weights
9. **Implement confidence-based fallback** (GAP-009) — search/other routing below threshold

---

*End of INTENT_TRANSACTION_CROSSWALK.md — Cross-referenced with `intent_transaction_crosswalk.json` (same directory)*
