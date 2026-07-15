# QUESTION PRIORITY POLICY — Dynamic Question Ordering

**Document ID:** LAWIM-GOLD-QM-PRIORITY-V1
**Status:** CANONICAL — Policy for dynamic question ordering and priority calculation
**Date:** 2026-07-15

---

## Table of Contents

1. [Core Principles](#1-core-principles)
2. [The 7 Rules of Question Ordering](#2-the-7-rules-of-question-ordering)
3. [Priority Factors](#3-priority-factors)
4. [Priority Formula](#4-priority-formula)
5. [Implementation Guide](#5-implementation-guide)
6. [Examples](#6-examples)
7. [Channel-Specific Adaptations](#7-channel-specific-adaptations)
8. [Edge Cases](#8-edge-cases)
9. [Appendix: Priority Reference Tables](#9-appendix-priority-reference-tables)

---

## 1. Core Principles

The question priority system ensures that:
- Users are asked the most impactful questions first
- Confirmed facts are never re-asked
- The qualification process is efficient and natural
- Results are delivered as early as possible (MINIMUM_SEARCH_READY)
- Privacy-sensitive questions are deferred appropriately

### Design Goals

| Goal | Description |
|------|-------------|
| Efficiency | Minimum questions to reach search-ready |
| Natural flow | Questions feel logical, not robotic |
| Adaptivity | Priority adapts to context, channel, and user behavior |
| Privacy | Sensitive questions are asked later |
| Respect | Never re-ask, never waste user time |

---

## 2. The 7 Rules of Question Ordering

### Rule 1: Never Re-Ask Confirmed Facts

**Statement**: Once a field has been collected and confirmed, it MUST NEVER be asked again in the same qualification session.

**Implementation**:

```python
def next_question(context):
    # Filter out all fields that are already known
    known_fields = context.get_confirmed_fields()
    pending_fields = [f for f in all_fields if f.id not in known_fields]
    if not pending_fields:
        return None  # All fields collected
    return select_highest_priority(pending_fields)
```

**Exceptions**:
- User explicitly says "I changed my mind" about a previous answer
- User gives contradictory information → ask for clarification (not re-ask)
- Long time gap (>24h) since last session → soft reconfirmation

**Examples**:
- ✓ User said budget is 150k → never ask "what's your budget?" again
- ✗ "You mentioned Douala, is that correct?" → only if there's ambiguity
- ✓ User initially said RENT, now says BUY → correction overrides, but don't say "I thought you wanted to rent?"

---

### Rule 2: Extract Multiple Fields from Same Message

**Statement**: When a user provides information that contains multiple fields, extract ALL of them. Do not ask about something the user has already volunteered.

**Implementation**:

```python
def process_message(message, context):
    extracted = nlp_extract_fields(message)
    for field, value in extracted.items():
        context.set_field(field, value, source='extracted')
    # Only ask about fields NOT already extracted
    return next_question(context)
```

**Examples**:
- User: "I'm looking for a 2-bedroom furnished apartment in Bonapriso, Douala, max 150k"
  → Extract: PROPERTY_TYPE=appartement_meuble, CHAMBRES=2, MEUBLE=meuble, CITY=Douala, NEIGHBORHOOD=Bonapriso, BUDGET_MAX=150000
  → Next question: BUDGET_TYPE or timing

- User: "I need a plumber urgently in Yaounde, my pipe burst"
  → Extract: SERVICE=plombier, URGENCE=urgent_48h, CITY=Yaounde
  → Next question: description_besoin details

---

### Rule 3: One Main Question at a Time

**Statement**: On conversational channels (WhatsApp, Telegram), ask exactly ONE main question per message. On Telegram, you may include 2-3 fields in a structured format.

**Rationale**: Users are overwhelmed by multiple questions. Single-question turns lead to higher completion rates.

**Implementation**:

```python
def format_question(field, channel):
    if channel == 'whatsapp':
        return f"{field.question_template}"
    elif channel == 'telegram':
        # Could include a secondary related field
        return f"{field.question_template}\n\n{field.secondary_hint}"
    elif channel == 'dashboard':
        return render_full_form(pending_fields)
```

**What counts as "one question"**:
- ✓ "Quel quartier ou quelle zone ?" (single question, multiple acceptable answers)
- ✓ "Meublé ou non meublé ?" (binary choice)
- ✗ "Quel quartier, combien de chambres, et quel budget ?" (three separate questions)
- ✗ "Quel est votre budget et votre délai ?" (two questions)

---

### Rule 4: Prioritize Highest Filtering Power Missing Field

**Statement**: Among all missing fields, the one that most reduces the search space should be asked first.

**Ranking by filtering power**:

| Tier | Impact | Fields |
|------|--------|--------|
| 1 | Highest (80%+ reduction) | transaction, property_type, city |
| 2 | High (50-80% reduction) | budget_max, neighborhood |
| 3 | Medium (20-50% reduction) | chambres, douches, cuisine, meublé |
| 4 | Low (5-20% reduction) | surface, etage, parking, balcon |
| 5 | Lowest (<5% reduction) | jardin, piscine, gardiennage, dépendances |

**Note**: Filtering power varies by market and property type. These are generic estimates.

---

### Rule 5: Launch Search As Soon As Minimum Is Reached

**Statement**: When FLD-TRANSACTION, FLD-PROPERTY_TYPE, FLD-CITY, FLD-BUDGET_MAX, and FLD-NEIGHBORHOOD are all known, launch search immediately. DO NOT continue asking questions.

**Enforcement**:

```python
def should_launch_search(context):
    required = ['FLD-TRANSACTION', 'FLD-PROPERTY_TYPE', 'FLD-CITY',
                'FLD-BUDGET_MAX', 'FLD-NEIGHBORHOOD']
    return all(context.is_confirmed(f) for f in required)
```

**After search launch**, continue collecting:
1. Matching fields (for re-ranking)
2. Introduction fields (contact info)
3. Timing information

But only if the user engages with the results. If the user is satisfied, stop.

---

### Rule 6: Collect Secondary Preferences After

**Statement**: After the first search is launched and results are shown, collect secondary preferences for refinement. Never collect these before the first search.

**Secondary preferences include**:
- étage, ascenseur
- balcon, jardin, cour
- piscine, climatisation
- groupe électrogène, forage
- internet, sécurité, gardiennage
- dépendances, services inclus
- état du bien, standing

**Ordering after search**:
1. Ask "Would you like to refine the results?"
2. If yes → ask matching fields (chambres, douches, cuisine)
3. If user wants more refinement → ask amenity preferences
4. If user wants contact → move to INTRODUCTION_READY

---

### Rule 7: Ask Confirmation Only for Real Ambiguity

**Statement**: Only ask confirmation questions when there is genuine ambiguity. Never ask "is this correct?" for information the user explicitly provided.

**When to confirm**:
- NLP confidence is low (< 0.6)
- User gave ambiguous information (e.g., "around Bonapriso" vs exact neighborhood)
- User contradicts previous information
- Multiple values extracted for the same field

**When NOT to confirm**:
- User explicitly stated a value with high confidence
- Value was selected from a list by the user
- Value was confirmed in a previous turn

---

## 3. Priority Factors

### Factor Definitions

| Factor | Code | Range | Description |
|--------|------|-------|-------------|
| Known Information | known_information | binary | Whether this field is already confirmed |
| Previous Question | previous_question | binary | Whether this was the context of last question |
| Intent | intent | categorical | The detected user intention |
| Property Type | property_type | categorical | The chosen property type |
| Transaction | transaction | categorical | Buy/rent/sell/finance/find |
| Impact on Search | impact_filtering | 0.0-1.0 | How much this field filters results |
| Impact on Matching | impact_matching | 0.0-1.0 | How much this field affects matching score |
| Ambiguity | ambiguity | 0.0-1.0 | Whether the field needs clarification |
| Urgency | urgency | 0-3 | User's expressed urgency level |
| Sensitivity | sensitivity | 0-3 | Privacy sensitivity (0=public, 3=confidential) |
| Conversational Cost | conversational_cost | 1-5 | How hard/complex the question is to ask |

### Detailed Factor Specifications

#### known_information
- **Values**: confirmed (skip), deduced (can skip or confirm), extracted (use), unknown (ask)
- **Effect**: If confirmed, remove from consideration entirely
- **Detection**: From field registry, confirmed_fields list

#### previous_question
- **Values**: same_topic (keep context), new_topic (shift)
- **Effect**: If the previous answer suggests a related field, ask that first
- **Example**: If user says "Bonapriso", next question should ideally be about Bonapriso context, budget, or specific criteria — not about their name

#### intent
- **Values**: RENT_PROPERTY, BUY_PROPERTY, SELL_PROPERTY, INVESTOR_INTENT, FIND_PROFESSIONAL, GET_SERVICE
- **Effect**: Different intents prioritize different fields
- **Intents → Priority fields**:

| Intent | First Fields | Last Fields |
|--------|-------------|-------------|
| RENT_PROPERTY | city, budget (monthly), neighborhood, rooms | caution, charges, contact |
| BUY_PROPERTY | city, budget (total), neighborhood, usage | financing, notaire, documents |
| SELL_PROPERTY | city, property_type, price, condition | title, documents, photos |
| INVESTOR_INTENT | budget, type_investment, city, yield | experience, accompagnement |
| FIND_PROFESSIONAL | service_type, location, urgency, description | qualifications, references |
| GET_SERVICE | service_type, location, description, date | contract, payment |

#### property_type
- **Values**: All 18 residential, 7 land, 16 commercial, etc.
- **Effect**: Determines which fields are relevant and which are forbidden
- **Examples**:
  - chambre_simple → never ask chambres (always 1), never ask salon
  - studio → never ask chambres (0), derive meublé from sub-type
  - terrain → never ask chambres/douches/salon (irrelevant)
  - bureau → ask nombre_pieces, surface, etage; never ask chambres

#### transaction
- **Values**: RENT, BUY, SELL, FINANCE, FIND, SERVICE
- **Effect**: Determines budget semantics and required fields
- **Examples**:
  - RENT → budget is monthly, ask caution + charges
  - BUY → budget is total, ask financing + notaire
  - FINANCE → ask amount, duration, income, guarantees

#### impact_filtering
- **Values**: 0.0 to 1.0 (estimated fraction of results filtered)
- **Calculation**: Based on historical data per market
- **Reference table**:

| Field | Generic Impact | Rent Impact | Buy Impact |
|-------|---------------|-------------|------------|
| CITY | 0.9 | 0.9 | 0.9 |
| PROPERTY_TYPE | 0.8 | 0.8 | 0.8 |
| BUDGET_MAX | 0.7 | 0.7 | 0.7 |
| NEIGHBORHOOD | 0.6 | 0.6 | 0.6 |
| CHAMBRES | 0.4 | 0.4 | 0.4 |
| DOUCHES | 0.3 | 0.3 | 0.3 |
| CUISINE | 0.2 | 0.2 | 0.1 |
| MEUBLE | 0.3 | 0.3 | 0.1 |
| SURFACE | 0.3 | 0.2 | 0.4 |
| PARKING | 0.2 | 0.2 | 0.15 |
| CLIMATISATION | 0.15 | 0.15 | 0.1 |
| ETAGE | 0.1 | 0.1 | 0.1 |
| BALCON | 0.05 | 0.05 | 0.05 |

#### impact_matching
- **Values**: 0.0 to 1.0 (how much this field affects match score)
- **Reference**:

| Field | Matching Weight |
|-------|----------------|
| CITY | 0.30 |
| NEIGHBORHOOD | 0.25 |
| BUDGET | 0.25 |
| PROPERTY_TYPE | 0.15 |
| TITLE_STATUS | 0.05 |

#### ambiguity
- **Values**: 0.0 (crystal clear) to 1.0 (extremely ambiguous)
- **When high**: Defer the question or ask for confirmation
- **Examples**:
  - "budget around 150k" → ambiguity 0.3 (range vs. exact)
  - "somewhere in Douala" → ambiguity 0.5 (which area?)
  - "I need a good apartment" → ambiguity 0.7 (good = ?)

#### urgency
- **Values**: 0 (not urgent) to 3 (extremely urgent)
- **Effect**: Higher urgency = faster path to search, skip optional questions
- **Derivation**: From user language ("ASAP", "urgent", "need now") + selected delai

| User Signal | Urgency Score |
|-------------|---------------|
| "ASAP", "urgent", "now" | 3 |
| "this week", "soon" | 2 |
| "next month", "not in a hurry" | 1 |
| "no rush", "just looking" | 0 |

#### sensitivity
- **Values**: 0 (public) to 3 (confidential)
- **Effect**: Higher sensitivity = questions are asked later in the conversation
- **Reference**:

| Level | Value | Examples | Ask When |
|-------|-------|----------|----------|
| public | 0 | city, property_type, chambres | Always early |
| private | 1 | name, phone, email, budget | After trust established |
| sensitive | 2 | income, financing, title number | After introduction |
| confidential | 3 | identity docs, bank details | Only at transaction stage |

#### conversational_cost
- **Values**: 1 (easy) to 5 (complex)
- **Effect**: Higher cost = might break down into sub-questions
- **Reference**:

| Question Type | Cost | Example |
|---------------|------|---------|
| Binary (yes/no) | 1 | "Meublé ?" |
| Enum (few options) | 2 | "Quel quartier ?" |
| Number | 2 | "Budget maximum ?" |
| Enum (many options) | 3 | "Quel type de cuisine ?" |
| Free text | 4 | "Décrivez votre besoin" |
| Multi-part | 5 | "Quels documents avez-vous ?" |

---

## 4. Priority Formula

### Core Formula

```
priority = base_priority
         - (impact_filtering * 10)
         + (sensitivity * 5)
         - (ambiguity * 3)
```

Where:
- `base_priority` = the field's position in the qualification order (0-100)
- `impact_filtering` = 0.0-1.0 (higher = ask earlier → reduces priority number)
- `sensitivity` = 0-3 (higher = ask later → increases priority number)
- `ambiguity` = 0.0-1.0 (higher = ask later → reduces it further but with less weight)

**Lower priority number = asked earlier.**

### Enhanced Formula (with context awareness)

```python
def calculate_priority(field, context):
    # Base priority from matrix definition
    p = field.base_priority

    # Adjust for filtering impact (higher impact = earlier = lower p)
    p -= field.impact_filtering * 10

    # Adjust for sensitivity (higher sensitivity = later = higher p)
    p += field.sensitivity * 5

    # Adjust for ambiguity (ambiguous = defer slightly)
    p -= field.ambiguity * 3

    # Adjust for channel
    if context.channel == 'whatsapp':
        p += field.conversational_cost * 2  # Complex questions cost more on WhatsApp

    # Adjust for urgency
    if context.urgency >= 2:
        if field.impact_filtering < 0.3:
            p += 10  # Defer low-impact fields when urgent

    # Adjust for known information
    if context.is_deduced(field.id):
        p += 15  # Deduced fields are lower priority to ask (just confirm)
    if context.is_extracted_from_message(field.id):
        p += 20  # Already extracted, don't ask unless needed

    # Ensure minimum priority
    return max(1, p)
```

### Example Calculations

**Field: FLD-NEIGHBORHOOD**
```
base_priority = 40
impact_filtering = 0.6 → -6
sensitivity = 0 → +0
ambiguity = 0.1 → -0.3
priority = 40 - 6 + 0 - 0.3 = 33.7
```

**Field: FLD-BUDGET_MAX**
```
base_priority = 50
impact_filtering = 0.7 → -7
sensitivity = 1 → +5
ambiguity = 0.1 → -0.3
priority = 50 - 7 + 5 - 0.3 = 47.7
```

**Field: FLD-CLIMATISATION**
```
base_priority = 67
impact_filtering = 0.15 → -1.5
sensitivity = 0 → +0
ambiguity = 0.1 → -0.3
priority = 67 - 1.5 + 0 - 0.3 = 65.2
```

**Field: FLD-TELEPHONE**
```
base_priority = 85
impact_filtering = 0.0 → -0
sensitivity = 1 → +5
ambiguity = 0.0 → -0
priority = 85 - 0 + 5 - 0 = 90
```

---

## 5. Implementation Guide

### State Machine

```
[Start] → Ask Intent/Target → INTENT_IDENTIFIED
    → Ask City → Ask Budget
    → MINIMUM_INTAKE_READY
    → Ask Neighborhood
    → MINIMUM_SEARCH_READY
    → [LAUNCH SEARCH]
    → Ask Matching Criteria → MINIMUM_MATCHING_READY
    → Ask Contact → INTRODUCTION_READY
    → Ask Visit → VISIT_READY
    → Ask Transaction → TRANSACTION_READY
```

### Priority Queue Implementation

```python
class QuestionPriorityQueue:
    def __init__(self, matrix, context):
        self.matrix = matrix
        self.context = context
        self.queue = []

    def build(self):
        for field in self.matrix.all_fields():
            if field.id in self.context.confirmed_fields:
                continue
            priority = calculate_priority(field, self.context)
            heapq.heappush(self.queue, (priority, field))

    def next(self):
        while self.queue:
            priority, field = heapq.heappop(self.queue)
            if not field.is_applicable(self.context):
                continue
            if field.id in self.context.confirmed_fields:
                continue
            return field
        return None  # All fields collected
```

### Scheduler Rules

1. **Always check blocking conditions** before popping the next question
2. **Batch related fields** on Telegram (priority difference < 5)
3. **Skip fields** that are irrelevant for the current property type
4. **Re-check priority** after each user message (context may have changed)
5. **Maximum 3 attempts** per field before offering to escalate to human

---

## 6. Examples

### Example 1: WhatsApp Rental, User Volunteers Information

```
Bot: "Bonjour ! C'est pour louer, acheter, vendre ou investir ?"
User: "Je cherche un studio meublé à Douala Bonapriso, max 100k"
→ Extracted: TRANSACTION=RENT, PROPERTY_TYPE=studio_meuble,
  CITY=Douala, NEIGHBORHOOD=Bonapriso, BUDGET_MAX=100000
→ Confirmed: all 5 search-ready fields!
→ [SEARCH LAUNCHED]
→ Priority: next highest impact = CUISINE, MEUBLE... 
  but MEUBLE is already known from property type!
Bot: "Très bien ! Voici quelques studios meublés à Bonapriso..."
  (Shows results, then asks:) "Souhaitez-vous affiner les résultats ?"
```

### Example 2: Telegram Structured Questions

```
Bot: "Dans quelle ville cherchez-vous ? Et quel budget maximum ?"
User: "Yaoundé, max 200k"
→ Extracted: CITY=Yaounde, BUDGET_MAX=200000
Bot: "Quel quartier ? Et combien de chambres ?"
User: "Mvog-Mbi, 2 chambres"
→ SEARCH LAUNCHED (all 5 criteria met)
```

### Example 3: Land Search Priority

```
Bot: "C'est pour acheter ou investir ?"
User: "Acheter un terrain à Yaoundé"
→ TRANSACTION=BUY, PROPERTY_TYPE=terrain, CITY=Yaounde
Bot: "Quel quartier et quelle surface ?"
User: "Nkolbisson, 300m2"
→ NEIGHBORHOOD=Nkolbisson, SURFACE=300
Bot: "Quel budget maximum ?"
User: "5 millions"
→ BUDGET_MAX=5000000
→ SEARCH LAUNCHED for terrain in Nkolbisson, 300m2, ≤5M FCFA
```

### Example 4: High Urgency Skips Optional

```
User: "URGENT besoin d'un studio à Douala centre, je dois emménager cette semaine"
→ Extracted: URGENCE=3, TRANSACTION=RENT, PROPERTY_TYPE=studio,
  CITY=Douala, NEIGHBORHOOD=centre, DELAI=urgent
Bot: "Quel budget max ?"
User: "150k"
→ SEARCH LAUNCHED immediately
Bot: "Voici les studios disponibles. Vous voulez les détails ou organiser une visite ?"
→ Skips recommended fields, goes straight to visit logistics
```

### Example 5: Contradiction Handling

```
User Day 1: "Je cherche un appartement 3 chambres à Douala"
→ CHAMBRES=3 confirmed
User Day 2: "En fait finalement je cherche plutôt un studio"
→ PROPERTY_TYPE changes to studio
→ CHAMBRES becomes 0 (by definition, studio has no separate bedroom)
→ DOUCHE becomes INTERNE (by definition for studio_moderne)
→ System updates context, does NOT ask "But you said 3 bedrooms?"
  → Correction overrides previous value (per Rule 1)
```

---

## 7. Channel-Specific Adaptations

### WhatsApp

| Adaptation | Rule |
|------------|------|
| One question per message | Always |
| Max question length | 150 chars |
| Avoid lists | Present 2-3 options max |
| Prioritize binary/choice | Yes/no or pick-one questions preferred |
| Defer free text | Ask free text (description) only when essential |
| Use quick replies | Where WhatsApp API allows |

### Telegram

| Adaptation | Rule |
|------------|------|
| 2-3 fields per message | Batch closely-related fields |
| Can use formatting | Bold, lists, inline buttons |
| More detail per message | Can explain context |

### Dashboard

| Adaptation | Rule |
|------------|------|
| Full form on one page | Show all remaining fields |
| Group by category | Location, Budget, Property, Contact |
| Validation inline | Show errors per field |
| Save draft | Allow partial completion |

---

## 8. Edge Cases

### User Gives No Information

```
User: "Bonjour"
→ No fields extracted
Bot: "Bonjour ! C'est pour louer, acheter, vendre ou investir ?"
  (Start with highest-priority field: transaction)
```

### User Gives Maximum Information

```
User: "Je cherche un appartement non meublé 2 chambres 1 salon 1 douche
  cuisine équipée à Douala Bonapriso pas plus de 200k avec parking
  clim internet pour emménager le mois prochain je m'appelle Jean
  691234567"
→ Extract all possible fields
→ Confirm: "Récapitulatif : appartement non meublé, 2ch, 1 salon,
  1 douche, cuisine équipée, Douala Bonapriso, 200k max, parking,
  clim, internet. C'est bien ça ?"
→ LAUNCH SEARCH
```

### User Changes Intention Mid-Qualification

```
User initially: "Je cherche à louer"
→ TRANSACTION=RENT
Bot asks city, budget, neighborhood...
User now: "En fait je préfère acheter"
→ TRANSACTION changes to BUY
→ Reset BUDGET_TYPE (monthly → total), ask FLD-FINANCING, FLD-USAGE
→ Keep LOCATION fields (still valid)
→ Re-launch search with new criteria
```

### Incomplete Extraction

```
User: "Je cherche dans le centre"
→ Could be CENTRE_VILLE (zone) or neighbourhood named "Centre"
Bot: "Quand vous dites centre, c'est le quartier ou la zone centre-ville ?"
  (Ambiguity resolution)
```

### User Knows the System

```
User: "Studio meublé Douala Bonapriso 150k"
→ NLP extracts all 4+ fields
Bot: "Parfait ! Voici ce que j'ai trouvé..."
→ Skips all questions, goes straight to results
```

---

## 9. Appendix: Priority Reference Tables

### Default Priority by Readiness Level

| Readiness Level | Priority Range | Example Fields |
|-----------------|---------------|----------------|
| INTENT_IDENTIFIED | 10-30 | TRANSACTION (10), PROPERTY_TYPE (20), INTENT (15) |
| MINIMUM_INTAKE_READY | 30-50 | CITY (30), BUDGET_MAX (50) |
| MINIMUM_SEARCH_READY | 40-60 | NEIGHBORHOOD (40), BUDGET_TYPE (55) |
| MINIMUM_MATCHING_READY | 42-75 | CHAMBRES (42), DOUCHES (44), CUISINE (52) |
| INTRODUCTION_READY | 60-90 | DISPONIBILITE (60), NOM (80), TELEPHONE (85) |
| VISIT_READY | 62-74 | ETAGE (62), PARKING (63), CLIMATISATION (67) |
| TRANSACTION_READY | 71-73 | CAUTION (72), CHARGES (73), FINANCING (71) |

### Priority by Property Type (Residential)

| Property Type | Highest Priority Fields (besides core) | Deferred Fields |
|---------------|----------------------------------------|-----------------|
| chambre_simple | DOUCHES (interne/externe), CUISINE | CHAMBRES, SALONS, ETAGE, PARKING |
| chambre_moderne | CUISINE, DOUCHES (interne) | CHAMBRES, SALONS, PARKING |
| studio | CUISINE, MEUBLE, DOUCHES | CHAMBRES, SALONS |
| studio_moderne | CUISINE, MEUBLE, ETAGE | CHAMBRES, DOUCHES (always interne) |
| studio_meuble | CUISINE, ETAGE, PARKING | MEUBLE (always meuble), CHAMBRES |
| appartement_non_meuble | CHAMBRES, DOUCHES, SALONS, CUISINE | MEUBLE (always non-meuble) |
| appartement_meuble | CHAMBRES, DOUCHES, SALONS, CUISINE | MEUBLE (always meuble) |
| villa | CHAMBRES, DOUCHES, SALONS, SURFACE_TERRAIN, PARKING | ETAGE, ASCENSEUR |
| colocation | CHAMBRES, NOMBRE_COLOCATAIRES, ESPACES_PARTAGES | GENRE_PREFERENCE (deferred) |
| cite_universitaire | TYPE_CHAMBRE_UNIV, UNIVERSITE, RESTAURATION | BOURSE (sensitive, deferred) |

### Priority Modulation by Urgency

| Urgency Level | Behavioral Change |
|---------------|-------------------|
| 0 (NOT_URGENT) | Collect all fields normally; optional fields may be deferred to later |
| 1 (MODERATE) | Skip optional fields; collect recommended only |
| 2 (URGENT) | Launch search at minimum; skip most recommended fields |
| 3 (EXTREMELY URGENT) | Launch search at intake (city+budget); defer everything else |

---

**End of QUESTION_PRIORITY_POLICY.md**
