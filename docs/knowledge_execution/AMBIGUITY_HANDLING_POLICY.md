# AMBIGUITY HANDLING POLICY — Language Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** LANGUAGE_EXECUTION_ARCHITECTURE.md, NORMALIZATION_PIPELINE.md, ALIAS_RESOLUTION_CONTRACT.md, LANGUAGE_MODEL.md, LANGUAGE_BUSINESS_KNOWLEDGE.md, RULE_INDEX.md (LANG-001 to LANG-014)

---

## 1. Ambiguity Detection Overview

Ambiguity occurs when a token, phrase, or entity has multiple valid interpretations that cannot be resolved automatically with sufficient confidence. The Language Engine detects ambiguity at multiple stages of the NORMALIZATION_PIPELINE and applies a graduated resolution strategy.

### 1.1 Ambiguity Types

| Type | Definition | Example |
|------|------------|---------|
| **Location** | Multiple geographic entities share the same name | "Douala" as city vs. "Douala" as neighborhood reference |
| **Property Type** | Term maps to multiple property types | "studio" as STU vs. "studio" as CHB_MEUBLEE |
| **Language** | Word exists in multiple language keyword lists | "sale" in English (sell) vs. French (dirty) vs. shared |
| **Intent** | Expression matches multiple intents | "buy" vs. "invest" overlap |
| **Entity Boundary** | Unclear where entity starts/ends | "petite maison" as type or maison with modifier |
| **Co-reference** | Pronoun or implied reference to prior entity | "le" referring to terrain vs. appartement |
| **Price Ambiguity** | Price period unclear | "150k" monthly vs. yearly vs. global |

---

## 2. Ambiguity Detection Algorithm

### 2.1 Confidence Threshold-Based Detection

```
FUNCTION detect_ambiguity(entities, context):
    INPUT: entities[] (list of extracted entities with confidence scores)
           context (session context, history)
    OUTPUT: ambiguity_flags[]

    ambiguity_flags = []

    FOR EACH entity IN entities:
        IF entity.candidates.length > 1:
            # Multiple candidates exist
            top_two = entity.candidates.sorted_by_confidence[:2]
            delta = top_two[0].confidence - top_two[1].confidence

            IF delta < 0.20:
                # Insufficient separation between candidates

                IF delta < 0.05:
                    # Critical ambiguity — cannot distinguish
                    ambiguity_flags.append({
                        "type": entity.type,
                        "severity": "HIGH",
                        "token": entity.token,
                        "candidates": top_two,
                        "confidence_gap": delta,
                        "resolution_strategy": "ask_clarification"
                    })

                ELSE IF delta < 0.10:
                    # Significant ambiguity — context may resolve
                    ambiguity_flags.append({
                        "type": entity.type,
                        "severity": "MEDIUM",
                        "token": entity.token,
                        "candidates": top_two,
                        "confidence_gap": delta,
                        "resolution_strategy": "use_context"
                    })

                ELSE:
                    # Low ambiguity — context likely resolves
                    ambiguity_flags.append({
                        "type": entity.type,
                        "severity": "LOW",
                        "token": entity.token,
                        "candidates": top_two,
                        "confidence_gap": delta,
                        "resolution_strategy": "use_history"
                    })

    RETURN ambiguity_flags
```

### 2.2 Confidence Thresholds

| Severity | Confidence Gap | Resolution Strategy | Action |
|----------|---------------|---------------------|--------|
| HIGH | < 0.05 | ask_clarification | Must ask user to disambiguate |
| MEDIUM | 0.05 – 0.09 | use_context | Try context before asking |
| LOW | 0.10 – 0.19 | use_history | Check conversation history |
| NONE | ≥ 0.20 | auto_resolve | Pick top candidate automatically |

---

## 3. Ambiguity by Type — Detection & Resolution

### 3.1 Location Ambiguity

**Common Cases in Cameroon Context:**

| Ambiguous Token | Candidate A | Candidate B | Context |
|-----------------|-------------|-------------|---------|
| "Douala" | City: Douala (CM-DLA) | Neighborhood: Douala (in Yaoundé?) | Rare — Douala is distinctly a city |
| "Messa" | District: Messa (Douala) | District: Messa (Yaoundé) | Both exist — need city context |
| "Centre" | District: Centre (Douala) | Region: Centre | Need neighborhood vs. region context |
| "New-Bell" | District: New-Bell (Douala) | District: New-Bell Bandjoun | Need alias resolution to canonical |
| "Buea" | City: Buea (CM-BUE) | Town: Buea (generic) | City always wins — known city |
| "Small Soppo" | District: Small Soppo (Buea) | Village: Small Soppo | District is canonical |

**Detection:**

```json
{
  "type": "location",
  "severity": "MEDIUM",
  "token": "Messa",
  "candidates": [
    {"canonical": "Messa", "city": "Douala", "confidence": 0.50},
    {"canonical": "Messa", "city": "Yaoundé", "confidence": 0.45}
  ],
  "confidence_gap": 0.05,
  "context_available": true
}
```

**Resolution Strategy — High Severity:**
```
SYSTEM: "J'ai trouvé 'Messa' à Douala et à Yaoundé. De quel Messa parlez-vous ?"
USER:  "Messa à Douala"
→ Resolve: Messa, Douala, confidence restored to 0.95
```

**Resolution Strategy — Medium/Low:**
```
1. Check session context: if known_city exists, use it
2. Check previous user messages for city reference
3. If city is known (e.g., Douala), select Messa (Douala)
4. Promote with confidence = 0.80 + context_bonus(0.10)
```

### 3.2 Property Type Ambiguity

**Common Cases:**

| Ambiguous Token | Candidate A | Candidate B | Context |
|-----------------|-------------|-------------|---------|
| "studio" | STU (Studio) | CHB_MEUBLEE (Chambre Meublée) | Studio can mean both in Cameroon |
| "villa" | VIL (Villa) | MSN (Maison) | Villa is a type of house |
| "chambre" | CHB (Chambre) | CHB_MEUBLEE (Chambre Meublée) | Meublé vs. non-meublé distinction |
| "terrain" | TER (Terrain) | TER_CONST (Terrain Constructible) | Constructible vs. non-constructible |
| "duplex" | DUP (Duplex) | VIL (Villa duplex) | Duplex is standalone type vs. villa subtype |
| "commerce" | COM (Local Commercial) | BUR (Bureau) | Commerce vs. office ambiguity |

**Detection:**

```json
{
  "type": "property_type",
  "severity": "HIGH",
  "token": "studio",
  "candidates": [
    {"canonical_id": "STU", "label": "Studio", "confidence": 0.50},
    {"canonical_id": "CHB_MEUBLEE", "label": "Chambre Meublée", "confidence": 0.45}
  ],
  "confidence_gap": 0.05,
  "context_available": true
}
```

**Resolution Strategy:**
```
1. Check budget context: small budget → CHB_MEUBLEE, larger → STU
2. Check for modifiers: "studio meublé" → CHB_MEUBLEE, "studio tout équipé" → STU
3. Check for pricing pattern: monthly rent → CHB_MEUBLEE, purchase → STU
4. If context cannot resolve → ask:
   "Précisez : cherchez-vous un studio indépendant ou une chambre meublée ?"
```

### 3.3 Language Ambiguity

**Common Cases:**

| Ambiguous Token | FR Meaning | EN Meaning | PID Meaning |
|-----------------|------------|------------|-------------|
| "sale" | sale (dirty) | sale (vente) | — |
| "location" | location (rent) | location (emplacement) | — |
| "rent" | — | rent (louer) | — |
| "price" | — | price (prix) | — |
| "budget" | budget | budget | — |
| "urgent" | urgent | urgent | — |
| "na" | n/a (contraction) | — | na (is/are) |
| "small" | — | small (petit) | small (a little) |
| "plenty" | — | plenty (beaucoup) | plenty (beaucoup) |
| "dey" | — | — | dey (to be/exist) |

**Detection:**

```json
{
  "type": "language",
  "severity": "LOW",
  "token": "budget",
  "shared_across": ["FR", "EN"],
  "resolution_strategy": "use_detected_language"
}
```

**Resolution Strategy:**
```
1. Language ambiguity only matters when language detection is uncertain
2. If language is confidently detected, shared words take that language's meaning
3. If language is uncertain, ask for language clarification first
4. Example: user says "budget"
   - Language detected as FR → treat as French "budget"
   - Language uncertain → use French default (LANG-001)
```

### 3.4 Intent Ambiguity

**Common Cases:**

| Ambiguous Expression | Intent A | Intent B | Context |
|----------------------|----------|----------|---------|
| "je veux acheter un terrain pour investir" | BUY | INVESTOR | Both buy and invest |
| "je cherche une maison" | SEARCH | RENT | Search vs. Rent overlap |
| "dernier prix ?" | NEGOTIATE | BUY | Negotiation vs. Purchase intent |
| "i wan buy house for rent" | BUY | RENT | Buy-to-rent dual intent |
| "what's available" | SEARCH | — | Generic search, no specific intent |
| "je veux construire" | INVESTOR | BUY | Build-to-live vs. build-to-invest |

**Detection:**

```json
{
  "type": "intent",
  "severity": "MEDIUM",
  "expression": "je veux acheter un terrain pour investir",
  "candidates": [
    {"intent": "BUY", "score": 0.55, "matched_patterns": ["je veux acheter"]},
    {"intent": "INVESTOR", "score": 0.50, "matched_patterns": ["investir", "pour investir"]}
  ],
  "confidence_gap": 0.05,
  "multi_intent": true
}
```

**Resolution Strategy:**
```
1. Detect multi-intent messages:
   - If two intents score within 10%, mark as multi-intent (LANG-007)
   - Forward both intents to Qualification Engine for priority evaluation
2. Use conversation history:
   - Previous intent match → promote to primary
   - User behavior pattern (e.g., always invests) → promote INVESTOR
3. If no history and cannot resolve:
   - Ask clarifying question:
     "Cherchez-vous un terrain à acheter pour y habiter ou pour investir ?"
4. Cameroon-specific patterns:
   - "je veux construire au pays" → INVESTOR (diaspora pattern)
   - "je cherche un terrain à bâtir" → BUY (primary residence)
   - "rendement locatif" → INVESTOR
   - "maison pour la famille" → BUY
```

### 3.5 Price Ambiguity

**Common Cases:**

| Expression | Possibility A | Possibility B | Possibility C |
|------------|--------------|--------------|--------------|
| "150k" | 150,000 FCFA/month (rent) | 150,000 FCFA (global — too low for buy) | — |
| "5M" | 5,000,000 FCFA (buy) | 5,000,000 FCFA/month (rent — unlikely) | — |
| "budget 10M" | 10,000,000 FCFA (buy) | — | — |
| "prix 100k" | 100,000 FCFA (monthly rent) | 100,000 FCFA (service fee) | — |

**Detection:**

```json
{
  "type": "price_period",
  "severity": "LOW",
  "amount": 150000,
  "candidates": [
    {"period": "monthly", "intent_compat": "RENT", "confidence": 0.85},
    {"period": "global", "intent_compat": "BUY", "confidence": 0.15}
  ],
  "resolution_strategy": "use_detected_intent"
}
```

**Resolution Strategy:**
```
1. Use detected intent to infer period:
   - RENT intent → amount is likely monthly (unless explicitly "annual")
   - BUY intent → amount is likely global
   - LAND intent → amount could be global or per-square-meter
2. Check amount magnitude:
   - < 500,000 → typically monthly (rent)
   - > 1,000,000 → could be global (buy)
   - 500,000 – 1,000,000 → ambiguous, check context
3. Check for explicit period indicators:
   - "par mois", "/mois", "monthly", "chaque mois" → monthly
   - "total", "global", "price", "prix" → global
4. If still ambiguous → ask:
   "Le montant de 150 000 FCFA est-il par mois ou le prix total ?"
```

---

## 4. Resolution Strategies

### 4.1 Strategy: Ask Clarifying Question

Used for HIGH severity ambiguity where confidence gap < 0.05.

```
PROMPT TEMPLATES:

[location_ambiguity]
FR: "J'ai trouvé plusieurs [entity_type] qui correspondent à '[token]'. \
      Précisez : [option A], [option B], ou autre ?"
EN: "I found multiple [entity_type] matching '[token]'. \
      Please specify: [option A], [option B], or something else?"
PID: "I see plenty [entity_type] wey fit '[token]'. \
      Which one: [option A], [option B], or different one?"

[property_type_ambiguity]
FR: "Précisez le type de bien : [option A] ou [option B] ?"
EN: "Please specify the property type: [option A] or [option B]?"
PID: "Abeg tell me di property type: [option A] or [option B]?"

[intent_ambiguity]
FR: "Souhaitez-vous [option A] ou [option B] ?"
EN: "Do you want to [option A] or [option B]?"
PID: "You want [option A] or [option B]?"
```

**Example Flow — Location Ambiguity:**
```
USER: "je cherche terrain à messa"
SYSTEM: "J'ai trouvé 'Messa' à Douala et à Yaoundé. \
          De quel Messa parlez-vous ?"
USER: "Messa Douala"
SYSTEM: "Parfait ! Je cherche des terrains à Messa, Douala."
→ Ambiguity resolved. Entity locked to Messa (Douala).
```

### 4.2 Strategy: Use Context

Used for MEDIUM severity ambiguity (gap 0.05 – 0.09).

**Context Sources (in priority order):**

| Priority | Context Source | Example |
|----------|---------------|---------|
| 1 | Current session intent | User has been discussing RENT → prefer rental property types |
| 2 | Known city from current message | "Messa" + "Douala" in same message → Messa (Douala) |
| 3 | Previous user messages | Prior message mentioned "location" → RENT context |
| 4 | User profile / stored preferences | User always searches for apartments → prefer APT |
| 5 | Geographic proximity | Previous location was "Bonapriso" (Douala) → Messa (Douala) |
| 6 | Language context | French keywords → prefer French canonical forms |

```
FUNCTION resolve_with_context(ambiguity_flag, context):
    IF context.known_city AND ambiguity_flag.candidates[0].city IN [context.known_city, null]:
        RETURN ambiguity_flag.candidates[0]
    IF context.session_intent AND ambiguity_flag.candidates[0].intent_compat == context.session_intent:
        RETURN ambiguity_flag.candidates[0]
    IF context.previous_entity == ambiguity_flag.token:  # Repeated term
        RETURN context.previous_resolution

    # Apply context bonus
    FOR candidate IN ambiguity_flag.candidates:
        candidate.confidence += context_bonus(candidate, context)

    RETURN argmax(candidate.confidence FOR candidate IN candidates)
```

### 4.3 Strategy: Use History

Used for LOW severity ambiguity (gap 0.10 – 0.19) or when context is insufficient.

| History Source | Retention | Weight |
|---------------|-----------|--------|
| Current conversation | Session | 0.30 |
| Previous session (short-term) | 24 hours | 0.15 |
| User profile (long-term) | 365 days | 0.10 |
| Global user patterns | — | 0.05 |

```
FUNCTION resolve_with_history(ambiguity_flag, user_history):
    # Check conversation history for previous resolution of same token
    previous = user_history.find_resolution(ambiguity_flag.token)
    IF previous AND previous.confidence > 0.8:
        RETURN previous.resolution

    # Check if user corrected this ambiguity before
    correction = user_history.find_correction(ambiguity_flag.token)
    IF correction:
        RETURN correction.resolution

    # Fall back to statistical mode
    most_common = user_history.most_common_resolution(ambiguity_flag.token)
    IF most_common.frequency > 0.6:
        RETURN most_common.resolution

    # Cannot resolve with history alone
    RETURN null
```

### 4.4 Strategy: Fallback to Human

Used when all automated strategies fail.

**Escalation Conditions:**

| Condition | Description |
|-----------|-------------|
| `max_turns_exceeded` | 3 clarification turns without resolution |
| `confidence_too_low` | All candidates < 0.50 after resolution attempts |
| `user_confused` | User response indicates confusion or frustration |
| `irresolvable_ambiguity` | Entity maps to completely different domains |
| `critical_entity` | Entity is required for qualification and cannot be left ambiguous |

**Escalation Protocol:**
```
1. Log full ambiguity context (tokens, candidates, attempts)
2. Flag conversation for human operator review
3. Inform user that a human agent will follow up
4. Preserve conversation state for handover
5. Operator resolves ambiguity and updates knowledge base
```

---

## 5. Multi-Turn Ambiguity Resolution

### 5.1 Turn Tracking

```
TURN 1: USER → "je cherche studio à douala"
         SYSTEM → Detects: [studio: STU 0.50 / CHB_MEUBLEE 0.45] → AMBIGUITY MEDIUM
         SYSTEM → "Précisez : un studio indépendant ou une chambre meublée ?"

TURN 2: USER → "studio indépendant"
         SYSTEM → Resolves: [STU → confidence 0.95]
         SYSTEM → "Parfait ! Je cherche des studios indépendants à Douala."
```

**State Persistence:**

```json
{
  "ambiguity_state": {
    "active": true,
    "turn_count": 1,
    "max_turns": 3,
    "entity": "studio",
    "type": "property_type",
    "candidates": [
      {"id": "STU", "label": "Studio", "base_confidence": 0.50},
      {"id": "CHB_MEUBLEE", "label": "Chambre Meublée", "base_confidence": 0.45}
    ],
    "resolution_attempts": [
      {"turn": 1, "strategy": "use_context", "result": "insufficient"}
    ],
    "previous_language": "FR"
  }
}
```

### 5.2 Multi-Turn Rules

| Turn | Strategy | Action |
|------|----------|--------|
| 1 | Ask clarification | Direct question with options |
| 2 | Confirm resolution | Validate user's choice, persist |
| 3 | Escalate if failed | Route to human operator |

**If user response is still ambiguous after clarification:**
```
Turn 2: USER → "le petit"
        SYSTEM → Cannot resolve "le petit" as STU or CHB_MEUBLEE
        SYSTEM → "Désolé, je n'ai pas bien compris. \
                  Est-ce un studio (appartement d'une pièce) ou une chambre meublée ?"
        → Repeat clarification with more explicit options
```

### 5.3 Ambiguity Resolution Persistence

Once resolved, the resolution is cached to prevent re-asking:

| Cache Level | Duration | Scope |
|-------------|----------|-------|
| Session | Session lifetime | Current conversation |
| User | 365 days | Same user, all conversations |
| Global | Permanent (until override) | All users |

---

## 6. Cameroon-Specific Ambiguity Examples

### Example 1: Location — "Douala" ambiguous with "Douala neighborhood"

While rare, "Douala" could theoretically refer to:
- City: Douala (capital économique, Littoral) — canonical
- Neighborhood: Douala (in another city) — practically never used

**Resolution:** City Douala is assumed unless explicitly stated otherwise. No ambiguity raised.

### Example 2: Property Type — "Studio" in Cameroon context

In Cameroon real estate:
- "Studio" often means "chambre meublée" (CHB_MEUBLEE) — a furnished room
- "Studio" can also mean a true studio apartment (STU) — independent unit with kitchenette

**Resolution:** Check for modifiers:
- "studio meublé" → CHB_MEUBLEE
- "studio indépendant" or "studio tout équipé" → STU
- "studio avec salle de bain privée" → STU
- No modifier → ask clarification

### Example 3: Language — "Sale" in Cameroon context

```
USER: "terrain sale"
FR interpretation: "terrain sale" (dirty land — unlikely in real estate)
EN interpretation: "land sale" (terrain à vendre — likely real estate intent)
```

**Resolution:**
- If French keywords present (terrain, je cherche) → FR, "sale" is secondary modifier
- If English keywords present → EN, "sale" is primary intent
- If mixed → ask clarification: "Voulez-vous dire 'terrain à vendre' ?"

### Example 4: Intent — "Buy vs. Invest" overlap

```
USER: "je veux acheter un terrain pour investir au cameroun"
Candidates:
- BUY: score 0.55 (matched: "je veux acheter", "terrain")
- INVESTOR: score 0.50 (matched: "investir", "cameroun" — diaspora pattern)
```

**Resolution:**
1. Check diaspora indicators: "au cameroun" + possible international phone → INVESTOR boost
2. Check conversation history: previous buys vs. previous investments
3. Multi-intent flag: forward both BUY and INVESTOR to Qualification Engine
4. Qualification Engine will determine primary intent based on lead scoring rules

### Example 5: Location — "Bastos" vs. "Bastos neighborhood"

```
USER: "je cherche maison à bastos"
Candidates:
- Bastos (Yaoundé) — neighborhood: canonical, confidence 0.95
- Bastos (generic) — unknown, confidence 0.10
```

**Resolution:** No ambiguity — Bastos is definitively a Yaoundé neighborhood. Auto-resolve.

### Example 6: Price — "M" ambiguous

```
USER: "budget 1M"
Candidates:
- "1M" = 1,000,000 FCFA (million) — canonical, confidence 0.95
- "1M" = 1,000 FCFA (mille — non-standard) — confidence 0.10
```

**Resolution:** In Cameroon real estate, "M" always means "million". No ambiguity.

---

## 7. Ambiguity Resolution Flow

```
Ambiguity detected
    │
    ▼
┌─────────────────────────────────────────────┐
│ CLASSIFY SEVERITY                            │
│ HIGH   (gap < 0.05)                          │
│ MEDIUM (gap 0.05–0.09)                       │
│ LOW    (gap 0.10–0.19)                       │
│ NONE   (gap ≥ 0.20)                          │
└─────────────────────┬───────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌────────┐   ┌──────────┐   ┌──────────┐
   │ HIGH   │   │ MEDIUM   │   │ LOW      │
   └───┬────┘   └────┬─────┘   └────┬─────┘
       │             │              │
       ▼             ▼              ▼
   ┌─────────────────────────────────────┐
   │ USE CONTEXT                          │
   │ Check: session, intent, known_city,  │
   │        user_preferences, geo_prox    │
   └─────────────────┬───────────────────┘
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
   ┌──────────────┐    ┌────────────────┐
   │ RESOLVED     │    │ NOT RESOLVED   │
   └──────┬───────┘    └───────┬────────┘
          │                    │
          ▼                    ▼
   ┌──────────────┐    ┌────────────────┐
   │ Lock entity  │    │ USE HISTORY     │
   │ Update conf  │    │ Check: previous │
   │ Cache result │    │ corrections     │
   └──────────────┘    └───────┬────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐    ┌────────────────┐
             │ RESOLVED     │    │ NOT RESOLVED   │
             └──────┬───────┘    └───────┬────────┘
                    │                    │
                    ▼                    ▼
             ┌──────────────┐    ┌────────────────┐
             │ Lock entity  │    │ Turn ≤ 3?      │
             │ Update conf  │    │  YES → Ask     │
             │ Cache result │    │   Clarification │
             └──────────────┘    │  NO → Escalate │
                                 └────────────────┘
```

---

## 8. Fallback to Human Operator

### 8.1 Escalation Criteria

| Criteria | Threshold | Trigger |
|----------|-----------|---------|
| Max clarification turns | > 3 | consecutive HIGH ambiguities |
| Overall pipeline confidence | < 0.30 | after all resolution attempts |
| User explicit request | "parler à un agent" | "talk to a human", "agent" |
| Critical path blockage | Required field unresolved | city, property type, or budget |

### 8.2 Escalation Output

```json
{
  "escalation": {
    "reason": "max_turns_exceeded",
    "ambiguity_chain": [
      {"turn": 1, "entity": "studio", "strategy": "clarify", "outcome": "user_unclear"},
      {"turn": 2, "entity": "studio", "strategy": "clarify_explicit", "outcome": "user_still_unclear"},
      {"turn": 3, "entity": "studio", "strategy": "history", "outcome": "no_history"}
    ],
    "partial_entities": {
      "city": {"value": "Douala", "confidence": 0.90},
      "property_type": {"value": null, "ambiguity": true},
      "budget": {"value": null}
    },
    "conversation_snapshot": {
      "last_3_turns": [
        {"user": "je cherche studio"},
        {"bot": "Studio indépendant ou chambre meublée ?"},
        {"user": "le petit studio là"}
      ]
    },
    "handoff_priority": "NORMAL"
  }
}
```

### 8.3 Handoff Message

```
FR: "Je n'arrive pas à déterminer ce que vous cherchez précisément. \
      Un agent LAWIM va vous contacter pour vous aider."
EN: "I'm having trouble understanding exactly what you're looking for. \
      A LAWIM agent will contact you to help."
PID: "I no fit understand wetin you want exactly. \
      One LAWIM agent go contact you."
```

---

## 9. Ambiguity Prevention

### 9.1 Proactive Clarification

When the system detects that optional information would prevent future ambiguity:

```
USER: "je cherche terrain"
SYSTEM: "Dans quelle ville cherchez-vous ce terrain ?"
→ Prevents city ambiguity before it can occur

USER: "je cherche terrain à douala"
SYSTEM: "Quel type de terrain ? Résidentiel, commercial, ou constructible ?"
→ Prevents property type ambiguity
```

### 9.2 Ambiguity Learning

Each resolved ambiguity is stored to improve future resolution:

```json
{
  "learned_resolution": {
    "token": "studio",
    "context": {"city": "Douala", "budget_min": 50000, "budget_max": 150000},
    "resolved_as": "CHB_MEUBLEE",
    "user_id": "usr_<id>",
    "timestamp": "2026-07-15T10:30:00Z",
    "global_prevalence": 0.65
  }
}
```

---

## 10. Summary Table

| Ambiguity Type | Detection Method | Primary Strategy | Escalation Condition |
|----------------|-----------------|------------------|---------------------|
| Location | Multiple geo candidates | Use known city context | Unknown city, 3+ turns |
| Property Type | Multiple canonical IDs | Check modifiers + budget | Modifiers absent |
| Language | Shared keywords | Use detected language | Language uncertain |
| Intent | Overlapping WhatsApp patterns | Multi-intent forwarding | Irresolvable overlap |
| Price Period | Magnitude + intent analysis | Use detected intent | Conflicting signals |
| Entity Boundary | NLP segmentation | Pass to DeepSeek | Segmentation fails |
| Co-reference | Pronoun resolution | Use conversation memory | Multiple possible antecedents |
