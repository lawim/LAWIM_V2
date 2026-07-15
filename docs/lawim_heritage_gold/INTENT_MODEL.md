# INTENT MODEL — LAWIM Heritage Gold

## 1. Primary Intents (5)

| Intent ID | Label FR | Label EN | Priority | Lead Score Weight |
|-----------|----------|----------|----------|-------------------|
| BUY_PROPERTY | Achat | Buy | VERY_HIGH | 50 |
| RENT_PROPERTY | Location | Rent | HIGH | 30 |
| SELL_PROPERTY | Vente | Sell | VERY_HIGH | 60 |
| INVESTOR_INTENT | Investissement | Invest | P0 | 100 |
| SEARCH_PROPERTY | Recherche | Search | NORMAL | 25 |

## 2. Intent Detection Method

Detection pipeline: `incoming_message` → `normalize` → `keyword scoring` → `highest score wins`

```
┌─────────────────┐     ┌──────────────┐     ┌────────────────┐     ┌──────────────────┐
│ incoming_message│────>│ normalize    │────>│ keyword scoring│────>│ highest score    │
│ (raw text)      │     │ (lowercase,  │     │ (FR/EN/PID     │     │ wins (>0.70      │
│                 │     │  strip,      │     │  keyword maps) │     │  threshold)      │
└─────────────────┘     └──────────────┘     └────────────────┘     └──────────────────┘
```

### Scoring Sources
- `intent_detector.py` — Core detection logic
- `intents/*.json` — Keyword definitions per intent
- `intent_phrases.json` — Phrase-level indicators
- `intentions.json` — Formalised intent spec

### Confidence Threshold
- **Minimum confidence:** 0.70 (70%)
- Below threshold → fallback to SEARCH_PROPERTY or clarification prompt

## 3. Intent Keywords

### BUY_PROPERTY

| Language | Keywords |
|----------|----------|
| FR | acheter, achat, propriétaire, terrain, villa, immeuble, investir, je cherche |
| EN | buy, purchase, looking for, I need, house for sale, land for sale |
| PID | i wan buy house, i wan buy land |

**Secondary signals:** titre foncier, notaire, proprio direct, terrain titré

### RENT_PROPERTY

| Language | Keywords |
|----------|----------|
| FR | louer, location, logement, appartement, maison, studio |
| EN | rent, apartment, house for rent, lease |
| PID | i di find house, i wan rent house |

**Secondary signals:** meublé, non meublé, caution, charges incluses

### SELL_PROPERTY

| Language | Keywords |
|----------|----------|
| FR | vendre, vente, céder, terrain, maison, villa |
| EN | sell, for sale, selling property |
| PID | i di sell house, i get land for sale |

**Secondary signals:** proprio, titre foncier, vente urgente, dernier prix

### INVESTOR_INTENT

| Language | Keywords |
|----------|----------|
| FR | investir, investissement, ROI, rentabilité, immeuble, projet, rendement, patrimoine, cashflow |
| EN | investment, ROI, yield, real estate investment |
| PID | i wan invest |

**Secondary signals:** diaspora (en france, au canada, à distance), immeuble locatif, cashflow

### SEARCH_PROPERTY

| Language | Keywords |
|----------|----------|
| FR | cherche, recherche, besoin, maison, appartement |
| EN | looking, need, find, searching |
| PID | i di find |

## 4. Intent-to-Role Mapping

Source: `lead_classifier_v1.json`

| Intent | Role | Role Type |
|--------|------|-----------|
| BUY_PROPERTY | buyer | Demandeur |
| RENT_PROPERTY | tenant | Demandeur |
| SELL_PROPERTY | seller | Propriétaire |
| INVESTOR_INTENT | investor | Demandeur / Investisseur |
| INVESTOR_INTENT + diaspora signals | diaspora_investor | Demandeur / Investisseur |
| SEARCH_PROPERTY | visitor | Demandeur (unqualified) |

### User Typologies (from user_typologies.json)

| Typology | Intent Mapping | Decision |
|----------|---------------|----------|
| DEMANDEUR | BUY, RENT, SEARCH | FUSIONNER |
| PROPRIETAIRE | SELL | FUSIONNER |
| AGENT_IMMOBILIER | Introducer role | ADAPTER |
| INVESTISSEUR | INVESTOR_INTENT | ADAPTER |
| OPERATEUR | Triage/Review | CONSERVER + ADAPTER |
| SUPERVISEUR | Oversight | FUSIONNER |
| ADMINISTRATEUR | Admin | CONSERVER |

## 5. Intent Detection Pipeline (Detailed)

### Step 1: Input Normalisation
- Lowercase conversion
- Strip punctuation and extra whitespace
- Expand common abbreviations (appt→appartement, M→million, etc.)
- Apply typo correction from typo database

### Step 2: Keyword Scoring
- Each intent has keyword lists in FR, EN, PID
- Each keyword match contributes a weighted score
- Secondary signals (contextual phrases) add bonus weight

### Step 3: Confidence Calculation
- Raw score normalised to 0.0–1.0 range
- `confidence = matched_keyword_count / total_keywords_for_intent`
- Modified by phrase-level matching from `intent_phrases.json`

### Step 4: Winner Selection
- Intent with highest confidence ≥ 0.70 is selected
- If no intent meets threshold → SEARCH_PROPERTY assigned
- Multi-intent detection: confidence ties → both intents flagged

## 6. Urgency Detection

Source: `urgency_signals.json`

| Signal | Weight | Priority Adjustment |
|--------|--------|---------------------|
| urgent | high | Raise to HIGH |
| très urgent | critical | Raise to CRITICAL |
| asap | high | Raise to HIGH |
| immédiatement | critical | Raise to CRITICAL |
| aujourd'hui | medium | Compress to today |
| avant fin semaine | medium | Compress to EOW |
| je déménage demain | critical | Emergency |
| need now | high | Raise to HIGH |

## 7. Multi-Intent Detection

Source: `RULE_ENGINE_V5.json`

The engine supports detecting multiple intents in a single message. When multiple intents score above 0.70:

| Scenario | Handling |
|----------|----------|
| BUY + SEARCH | Treat as BUY |
| RENT + SEARCH | Treat as RENT |
| INVESTOR + BUY | Dual-intent path |
| SELL + URGENT | SELL with priority boost |
| Any + URGENT | Intent + urgency flag |

## 8. Intent-Based Conversation Flows

Source: `conversation_flows_v1.json`

| Intent | Flow Steps |
|--------|-----------|
| BUY_PROPERTY | Identify → Qualify city → Qualify budget → Qualify property type → Match → Follow-up |
| RENT_PROPERTY | Identify → Qualify city/neighborhood → Qualify budget → Furnished? → Move-in date → Match |
| SELL_PROPERTY | Identify → Qualify property type → Documents → Availability → Price → Publish |
| INVESTOR_INTENT | Identify → Expected return → Budget → City → Risk tolerance → Strategy → Timeline |
| SEARCH_PROPERTY | Identify → Clarify intent → Route to specific intent |

## 9. Entity Extraction Per Intent

| Intent | Entities Extracted |
|--------|-------------------|
| BUY_PROPERTY | property_type, location (city/neighborhood), budget, price_pattern |
| RENT_PROPERTY | property_type, location, budget (monthly), furnished, move_in_date |
| SELL_PROPERTY | property_type, location, price (asking), documents, availability |
| INVESTOR_INTENT | budget, city, expected_return, risk_tolerance, strategy, diaspora_country |
| SEARCH_PROPERTY | property_type, location, budget (optional) |

### Property Types Extracted

| Entity ID | Label FR | Label EN |
|-----------|----------|----------|
| APT | Appartement | Apartment |
| STU | Studio | Studio |
| CHB | Chambre | Room |
| CHB_MEUBLEE | Chambre Meublée | Furnished Room |
| MSN | Maison | House |
| VIL | Villa | Villa |
| TER | Terrain | Land |
| TER_CONST | Terrain Constructible | Buildable Land |
| COM | Local Commercial | Commercial Space |
| BUR | Bureau | Office |
| IMM | Immeuble | Apartment Building |
| DEP | Dépôt / Entrepôt | Warehouse |

### Location Extraction
- City name extraction with typo tolerance (10 priority cities + 18 secondary)
- Neighborhood extraction (382 neighborhoods across 10 cities)
- District alias resolution (from `district_aliases.json`)

### Budget/Price Extraction
- Support for `k` (thousands) and `M` (millions) shorthand
- FCFA / Franc CFA / XAF currency recognition
- Range format detection (e.g., 10–15M, 20–30 millions)
- Per-month pattern for rent (`/month`, `par mois`, `/mois`)
