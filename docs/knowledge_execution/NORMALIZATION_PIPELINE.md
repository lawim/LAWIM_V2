# NORMALIZATION PIPELINE — Language Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** LANGUAGE_EXECUTION_ARCHITECTURE.md, ALIAS_RESOLUTION_CONTRACT.md, AMBIGUITY_HANDLING_POLICY.md, LANGUAGE_MODEL.md, RULE_INDEX.md (LANG-001 to LANG-014)

---

## 1. Pipeline Overview

The normalization pipeline transforms a raw user message into a structured, normalized, confidence-scored fact set. It is the first processing stage for all incoming messages before intent detection, qualification, and matching.

```
raw_message (string from channel)
    │
    ▼
┌────────────────────────────────────────────────────────────────────┐
│ 1. RAW MESSAGE RECEPTION         Input: channel payload string     │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 2. LANGUAGE DETECTION           Input: normalized text             │
│    (LANG-001, LANG-002, LANG-012)                                  │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 3. CHANNEL NORMALIZATION        Input: raw message + channel meta  │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 4. SPELLING NORMALIZATION       Input: channel-normalized text     │
│    (LANG-006 — typo databases)                                     │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 5. ALIAS RESOLUTION             Input: spelling-normalized text    │
│    (LANG-005 — entity linking)                                     │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 6. ENTITY EXTRACTION            Input: alias-resolved text         │
│    (LANG-005, LANG-007)                                            │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 7. AMBIGUITY DETECTION          Input: extracted entities          │
│    (see AMBIGUITY_HANDLING_POLICY.md)                              │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 8. INTENT EXTRACTION            Input: resolved entities + context │
│    (LANG-007 — WhatsApp corpus)                                    │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 9. FACT EXTRACTION              Input: intent + entities           │
│    (pricing, location, property type, urgency)                     │
└────────────────────────────────┬───────────────────────────────────┘
                                 │
                                 ▼
┌────────────────────────────────────────────────────────────────────┐
│ 10. CONFIDENCE CALCULATION      Input: all prior results           │
│     Output: normalized_message object with confidence scores       │
└────────────────────────────────────────────────────────────────────┘
```

---

## 2. Stage Details

### Stage 1 — Raw Message Reception

**Input:** Raw string from channel (WhatsApp, Telegram, Dashboard, API)

**Processing:**
1. Receive payload from channel webhook
2. Extract message text
3. Attach channel metadata (channel type, sender_id, timestamp, session_id)
4. Log incoming message event

**Output:**
```json
{
  "raw_text": "je cherche appart 3 pieces a yaounde 150k budget urgent",
  "channel": "whatsapp",
  "sender_id": "237699999999",
  "session_id": "ses_abc123",
  "timestamp": "2026-07-15T10:30:00Z"
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `empty_message` | raw_text is null or empty | Log warning, return empty result |
| `unsupported_channel` | Channel not in allowed list | Reject with 400, log unsupported channel |
| `message_too_long` | Length > 4096 characters | Truncate, log truncation warning |

---

### Stage 2 — Language Detection

**Input:** `raw_text` from Stage 1

**Processing:**

```
DETECT_LANGUAGE(raw_text):

1. Check user stored preference (LANG-003):
   - If preference exists and confidence > 0.5 → return stored language

2. Apply DeepSeek AI classification (LANG-002 Priority 1):
   - Send text to DeepSeek classifier endpoint
   - Expect { language: "FR"|"EN"|"PID", confidence: 0.0-1.0 }
   - If confidence >= 0.70 → accept, persist, return

3. Apply Local Keyword Rules (LANG-002 Priority 3):
   - Tokenize text, strip punctuation, lowercase
   - Score against keyword lists:
     - French (LANG-013): 18 keywords
     - English (LANG-014): 18 keywords
     - Pidgin (LANG-012): 14 keywords
   - Calculate weighted scores:
     score_FR = matched_FR_keywords / 18
     score_EN = matched_EN_keywords / 18
     score_PID = matched_PID_keywords / 14
   - If max(score) >= 0.30 → language = argmax(score)
   - Else → French (default per LANG-001)

4. Apply Fallback Chain (LANG-001):
   - Known language for user → French → request explicit clarification

5. Persist detected language per user (LANG-003)
```

**Keyword Lists:**

| Language | Keywords |
|----------|----------|
| French (18) | bonjour, salut, appartement, maison, terrain, location, achat, vente, prix, budget, urgent, merci, je, tu, il, elle, nous, vous |
| English (18) | hello, hi, apartment, house, land, rent, buy, sale, price, budget, urgent, thanks, i, you, he, she, we, they |
| Pidgin (14) | how far, wahala, chap, gbedu, comot, dey, sabi, small, plenty, chop, wetin, na, abeg |

**Pidgin Multi-Word Detection:**
- Check for bigrams: "how far", "how i fit", "wey match", "wetin be"
- Each matched bigram adds +2 to Pidgin score

**Camfranglais Handling:**
- Camfranglais is NOT a supported language
- Detect code-switching patterns: "je need", "je want", "je cherche un land"
- When detected, classify as French with code-switching flag
- Do NOT create a 4th language classification

**Output:**
```json
{
  "language": "FR",
  "confidence": 0.92,
  "method": "deepseek|local_keywords|user_preference|fallback",
  "fallback_used": false,
  "code_switching_detected": false
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `detection_failed` | No method produces a result | Return French, confidence 0.3 |
| `low_confidence` | All scores below 0.30 | Return French, set lowest_confidence flag |
| `mixed_language_ambiguous` | Two languages tied within 5% | Use previous language if known, else French |

---

### Stage 3 — Channel Normalization

**Input:** `detected_language` + `raw_text` from Stage 1

**Processing:**

1. Normalize WhatsApp-specific patterns (LANG-007):
   - Expand common WhatsApp abbreviations:
     - "bjr" → "bonjour", "slm" → "salut", "stp" → "s'il te plaît"
     - "pk" → "pourquoi", "mrc" → "merci", "rdv" → "rendez-vous"
     - "tjrs" → "toujours", "qqn" → "quelqu'un", "qqch" → "quelque chose"
     - "cad" → "c'est-à-dire", "bcp" → "beaucoup", "vs" → "vous"
     - "jspr" → "j'espère", "g" → "j'ai", "t" → "tu as"
   - Expand English WhatsApp abbreviations:
     - "pls" → "please", "thx" → "thanks", "u" → "you"
     - "r" → "are", "ur" → "your", "ppl" → "people"
   - Normalize missing apostrophes: "jai" → "j'ai", "cest" → "c'est"
   - Normalize run-together words: "jespere" → "j'espère"
   - Normalize repeated characters (max 3): "urgenttt" → "urgent"

2. Normalize short-form expressions:
   - "t.f." → "titre foncier", "tf" → "titre foncier"
   - "M" (with space or alone) → context-dependent: "million" if numeric
   - "k" (with number) → "mille" (e.g., "150k" → "150000")

3. Strip extraneous whitespace, normalize unicode

**Output:**
```json
{
  "channel_normalized_text": "je cherche appartement 3 pieces a yaounde 150000 budget urgent",
  "expansions_applied": ["appart→appartement", "150k→150000"],
  "channel": "whatsapp"
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `normalization_failed` | Corrupted input after processing | Revert to raw_text, log error |
| `over_expansion` | Expansion context is ambiguous | Keep original, flag for review |

---

### Stage 4 — Spelling Normalization

**Input:** `channel_normalized_text` from Stage 3

**Processing:**

1. Lowercase the entire text
2. Strip diacritics for comparison (preserve originals for output)
3. Tokenize into words
4. For each token, check against typo databases in priority order (LANG-006):

   a. **Cities Typo DB** — Match against cities_typo.json
      - If city variant found → replace with canonical city name
   
   b. **Neighborhoods Typo DB** — Match against neighborhoods_typo.json
      - If neighborhood variant found → replace with canonical neighborhood name
   
   c. **Property Types Typo DB** — Match against property_types_typo.json
      - If property type variant found → replace with canonical property type
   
   d. **WhatsApp Typo DB** — Match against whatsapp_typo.json
      - If WhatsApp-specific typo found → replace with canonical form
   
   e. **General Typo DB** — Match against typo_database.json
      - If general typo found → replace with canonical form

5. Apply Levenshtein distance fallback for unknown tokens:
   - For each unknown token, compute Levenshtein distance against all known terms
   - If distance ≤ 1 → auto-correct, confidence = 0.80
   - If distance ≤ 2 → auto-correct, confidence = 0.70
   - If distance ≤ 3 → auto-correct, confidence = 0.60
   - If distance > 3 → leave unchanged, flag as potential error

6. Reconstruct normalized text from corrected tokens

**Output:**
```json
{
  "spelling_normalized_text": "je cherche appartement 3 pieces a yaounde 150000 budget urgent",
  "corrections_applied": [
    {"original": "appart", "corrected": "appartement", "source": "property_types_typo.json", "confidence": 0.85}
  ],
  "levenshtein_corrections": [],
  "unknown_tokens": []
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `correction_conflict` | Multiple typo DBs match same token | Apply highest confidence match |
| `over_correction` | Token matches known word but context suggests typo | Keep both, flag ambiguity |
| `too_many_unknowns` | > 50% of tokens unknown | Skip spelling correction, return raw |

---

### Stage 5 — Alias Resolution

**Input:** `spelling_normalized_text` from Stage 4

**Processing:**

1. For each recognizable entity in text, apply alias resolution (see ALIAS_RESOLUTION_CONTRACT.md):
   - Check entity_linking.json (LANG-005) — 20 pairs
   - Check search_aliases.json — 17 EN→FR mappings
   - Check property_type_aliases.json — 11 groups
   - Check district aliases (aliases.json) — 33 entries

2. Resolution priority (see ALIAS_RESOLUTION_CONTRACT.md §2):
   - Exact match → Typo correction → Synonym → Abbreviation → Entity linking

3. For geographic terms:
   - City abbreviations: YDE → Yaoundé, DLA → Douala, etc. (10 cities)
   - District aliases: Bonamoussadi Cité → Bonamoussadi, etc.

4. For property type terms:
   - English → French canonical: apartment → appartement, land → terrain
   - Abbreviations: appt → appartement

**Output:**
```json
{
  "alias_resolved_text": "je cherche appartement 3 pieces a yaounde 150000 budget urgent",
  "resolved_entities": [
    {"term": "appartement", "type": "property_type", "canonical_id": "APT", "confidence": 0.95},
    {"term": "yaounde", "type": "city", "canonical_id": "CM-YAO", "confidence": 1.0}
  ]
}
```

---

### Stage 6 — Entity Extraction

**Input:** `alias_resolved_text` + `resolved_entities` from Stage 5

**Processing:**

1. Extract structured entities using regex patterns and NLP:

   a. **Location (city/district/neighborhood):**
      - Pattern: `(?:à|a|dans|au|sur|vers|pour|chez)\s+([A-Za-zéèêëàâùûüôöîïç\-]+)` (FR)
      - Pattern: `(?:in|at|for|to|around)\s+([A-Za-z]+)` (EN)
      - Match against known city/neighborhood list (GEO-005)

   b. **Property type:**
      - Match against canonical property types: appartement, maison, terrain, villa, studio, chambre, bureau, commerce, immeuble, entrepôt, duplex
      - Resolve to canonical_id: APT, MSN, TER, VIL, STU, CHB, BUR, COM, IMM, DEP, DUP

   c. **Budget/Price:**
      - Pattern: `(\d+[\s]*(?:k|m|million|mille|cent|FCFA|franc|xaf)?)` (general)
      - Pattern: `(\d{1,3}(?:\s?\d{3})*\s*(?:FCFA|francs|xaf)?)` (full format)
      - Range: `(\d+)\s*(?:[–\-à])\s*(\d+)\s*(?:M|million)` (range format)
      - Extract: amount_min, amount_max, currency, period (month/year/global)
      - Normalize all to FCFA numeric value

   d. **Rooms/Bedrooms:**
      - Pattern: `(\d+)\s*(?:pièce|piece|pieces|pièces|chambre|chambres|room|rooms|chbre|chbres)`

   e. **Transaction type:**
      - location/rent → RENT
      - achat/vente/buy/sale → BUY/SELL
      - investir/invest → INVESTOR

   f. **Urgency:**
      - Match against urgency_signals.json (LANG-007) — 8 signals
      - Assign priority level: urgent → raise, très urgent → highest, etc.

2. Cross-reference entities with available knowledge base entries

**Output:**
```json
{
  "entities": {
    "location": {"city": "Yaoundé", "city_id": "CM-YAO", "neighborhood": null},
    "property_type": {"label": "appartement", "canonical_id": "APT", "confidence": 0.95},
    "budget": {"amount_min": 150000, "amount_max": 150000, "currency": "XAF", "period": "monthly"},
    "rooms": {"count": 3, "type": "pieces"},
    "transaction": {"intent": "RENT", "confidence": 0.85},
    "urgency": {"level": "normal", "signal": null}
  },
  "extraction_method": "regex|deepseek"
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `no_location` | No city/neighborhood found | Set location to null, flag for qualification |
| `no_property_type` | No property type found | Set type to null, flag for qualification |
| `no_budget` | No budget expression found | Set budget to null, flag for qualification |
| `partial_match` | Entity partially recognized | Include partial match with reduced confidence |

---

### Stage 7 — Ambiguity Detection

**Input:** Extracted entities from Stage 6

**Processing:**

1. Detect ambiguous entities (see AMBIGUITY_HANDLING_POLICY.md):
   - Location ambiguity: "Douala" could be city or neighborhood reference
   - Property type ambiguity: "studio" could be STU or CHB_MEUBLEE
   - Language ambiguity: word exists in multiple language keyword lists
   - Intent ambiguity: "buy" vs "invest" overlap

2. Apply detection algorithm:
   - For each entity with multiple possible resolutions
   - If confidence range between top candidates < 0.20 → mark ambiguous
   - Log ambiguity type and candidates

3. Classify ambiguity severity:
   - HIGH: No resolution possible without clarification
   - MEDIUM: Resolution possible with context
   - LOW: Resolution possible with high confidence

**Output:**
```json
{
  "ambiguous_entities": [],
  "ambiguity_flags": [],
  "resolution_strategy": "none_needed"
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `high_ambiguity` | Critical entity cannot be resolved | Request clarification from user |
| `irresolvable` | All resolution strategies exhausted | Escalate to human operator |

---

### Stage 8 — Intent Extraction

**Input:** Resolved entities + language from Stages 6 and 2

**Processing:**

1. Match message text against WhatsApp language corpus (LANG-007):
   - whatsapp_language.json — full corpus
   - diaspora_language.json — diaspora patterns
   - investor_language.json — investor patterns
   - negotiation.json — negotiation terms
   - property_listing.json — listing patterns
   - property_search.json — search patterns
   - urgency_signals.json — urgency patterns

2. Calculate intent scores for each intent type:
   - BUY, RENT, SELL, INVESTOR, SEARCH, VISIT, SIGNAL, COMMAND
   - Score = matched_pattern_count / total_patterns_for_intent

3. Select primary intent: argmax(intent_scores)
4. If score >= 0.70 → confident classification
5. If score < 0.70 → mark as multi-intent or ambiguous

6. Detect multi-intent messages:
   - If two intents score within 10% of each other
   - Mark as multi-intent, log both candidates
   - Example: "je veux acheter un terrain pour investir" → BUY + INVESTOR

**Output:**
```json
{
  "primary_intent": "RENT",
  "confidence": 0.85,
  "secondary_intent": null,
  "intent_scores": {"BUY": 0.1, "RENT": 0.85, "SELL": 0.0, "INVESTOR": 0.05, "SEARCH": 0.0},
  "matched_patterns": ["je cherche appartement à louer"]
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `no_intent` | No intent score above 0.20 | Set intent to SEARCH, confidence 0.3 |
| `multi_intent_ambiguous` | Two intents tied within 10% | Forward both, let Qualification Engine decide |
| `command_detected` | LANGUE, STATS, SIGNALER, etc. | Route to command handler directly |

---

### Stage 9 — Fact Extraction

**Input:** Intent + entities from Stages 8 and 6

**Processing:**

1. Build structured fact set combining all prior extractions:

   a. **Demographic facts:**
      - Language (from Stage 2)
      - Sender ID, channel (from Stage 1)
   
   b. **Property facts:**
      - Property type, canonical ID (from Stage 6)
      - Rooms, surface area (from Stage 6)
      - Furnished/unfurnished (from text matching)
   
   c. **Geographic facts:**
      - City, neighborhood, district (from Stage 6)
      - Canonical geography IDs
   
   d. **Financial facts:**
      - Budget min, max, currency, period (from Stage 6)
      - Negotiation terms (from Stage 8)
   
   e. **Temporal facts:**
      - Urgency level (from Stage 6)
      - Deadline (if mentioned)
   
   f. **Qualification facts:**
      - Diaspora indicators (from LANG-007 patterns)
      - Investor indicators (from investor_language.json)
      - Broker/spam indicators (from content analysis)

2. Normalize all values to canonical forms

3. Assign source traceability to each fact

**Output:**
```json
{
  "facts": {
    "language": "FR",
    "property": {"type": "appartement", "canonical_id": "APT", "rooms": 3, "furnished": null},
    "geography": {"city": "Yaoundé", "city_id": "CM-YAO", "neighborhood": null},
    "financial": {"budget_min": 150000, "budget_max": 150000, "currency": "XAF", "period": "monthly"},
    "urgency": {"level": "none"},
    "transaction_type": "RENT",
    "diaspora": false,
    "investor": false
  },
  "source_trace": {
    "intent_source": "whatsapp_language.json#property_search",
    "entity_source": "entity_linking.json#appartement",
    "geo_source": "cities.json#CM-YAO",
    "budget_source": "amount_expressions.json#k_format"
  }
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `incomplete_facts` | Required qualifying fields missing | Flag for qualification flow |
| `conflicting_facts` | Facts contradict each other | Flag for ambiguity resolution |
| `fact_validation_failed` | Fact cannot be validated against knowledge base | Reduce confidence on specific fact |

---

### Stage 10 — Confidence Calculation

**Input:** All outputs from Stages 1–9

**Processing:**

1. Compute overall pipeline confidence as weighted composite:

   | Component | Weight | Calculation |
   |-----------|--------|-------------|
   | Language detection confidence | 0.15 | From Stage 2 |
   | Spelling correction quality | 0.10 | 1.0 - (corrected_tokens / total_tokens) |
   | Alias resolution quality | 0.15 | Average confidence of resolved entities |
   | Entity extraction coverage | 0.20 | Ratio of extracted fields to expected fields |
   | Ambiguity penalty | 0.10 | 1.0 if no ambiguity, 0.5 if medium, 0.0 if high |
   | Intent confidence | 0.20 | From Stage 8 |
   | Fact validation | 0.10 | Ratio of validated facts |

2. Apply penalties:
   - Fallback chain used: -10%
   - Low confidence on critical fields: -15%
   - High ambiguity detected: -20%

3. Apply bonuses:
   - Multi-source confirmation: +10%
   - Exact match on all entities: +15%

**Output:**
```json
{
  "pipeline_confidence": 0.88,
  "component_scores": {
    "language_detection": 0.92,
    "spelling_correction": 0.95,
    "alias_resolution": 0.90,
    "entity_extraction": 0.85,
    "ambiguity": 1.0,
    "intent": 0.85,
    "fact_validation": 0.80
  },
  "penalties": [],
  "bonuses": ["multi_source_confirmation"]
}
```

**Error States:**

| Error | Condition | Action |
|-------|-----------|--------|
| `very_low_confidence` | Pipeline confidence < 0.30 | Flag for human review |
| `validation_failed` | Critical facts fail validation | Request re-entry from user |

---

## 3. Normalized Message Output

Final output of the normalization pipeline:

```json
{
  "message_id": "msg_<uuid>",
  "session_id": "ses_<uuid>",
  "timestamp": "2026-07-15T10:30:00Z",
  "channel": "whatsapp",
  "original_text": "je cherche appart 3 pieces a yaounde 150k budget urgent",
  "normalized_text": "je cherche appartement 3 pieces a yaounde 150000 budget urgent",
  "language": {
    "code": "FR",
    "confidence": 0.92,
    "method": "deepseek"
  },
  "entities": {
    "location": {"city": "Yaoundé", "city_id": "CM-YAO", "confidence": 1.0},
    "property_type": {"label": "appartement", "canonical_id": "APT", "confidence": 0.95},
    "budget": {"amount_min": 150000, "amount_max": 150000, "currency": "XAF", "period": "monthly"}
  },
  "intent": {
    "primary": "RENT",
    "confidence": 0.85,
    "secondary": null
  },
  "facts": {
    "language": "FR",
    "property": {"type": "appartement", "rooms": 3},
    "geography": {"city": "Yaoundé"},
    "financial": {"budget_min": 150000, "period": "monthly"},
    "urgency": "none",
    "transaction_type": "RENT"
  },
  "confidence": 0.88,
  "ambiguities": [],
  "pipeline_version": "1.0.0"
}
```

---

## 4. Language Detection Algorithm (Detailed)

```
FUNCTION detect_language(text):
    INPUT: text (string)
    OUTPUT: { language_code, confidence, method }

    # Step 1: Tokenization
    tokens = lowercase(text).split()
    bigrams = extract_bigrams(tokens)

    # Step 2: Score calculation
    fr_score = count_matches(tokens, FR_KEYWORDS) + count_bigram_matches(bigrams, FR_BIGRAMS)
    en_score = count_matches(tokens, EN_KEYWORDS) + count_bigram_matches(bigrams, EN_BIGRAMS)
    pid_score = count_matches(tokens, PID_KEYWORDS) + count_bigram_matches(bigrams, PID_BIGRAMS) * 2

    # Step 3: Normalize by lexicon size
    fr_norm = fr_score / len(FR_KEYWORDS)
    en_norm = en_score / len(EN_KEYWORDS)
    pid_norm = pid_score / len(PID_KEYWORDS)

    # Step 4: Determine language
    scores = { "FR": fr_norm, "EN": en_norm, "PID": pid_norm }
    max_lang = argmax(scores)
    max_score = scores[max_lang]

    IF max_score >= 0.30:
        # Check for ambiguity
        second_score = second_max(scores)
        IF max_score - second_score < 0.05:
            RETURN { language: previous_language_or_FR, confidence: max_score * 80, method: "ambiguous_fallback" }
        RETURN { language: max_lang, confidence: max_score * 100, method: "local_keywords" }
    ELSE:
        RETURN { language: "FR", confidence: 50, method: "fallback" }
```

---

## 5. Spelling Correction Algorithm

```
FUNCTION correct_spelling(tokens):
    INPUT: tokens (string[])
    OUTPUT: { corrected_tokens[], corrections[], unknown_tokens[] }

    corrected = empty list
    corrections = empty list
    unknown = empty list

    FOR token IN tokens:
        token_lower = lowercase(token)

        # Priority 1: Exact match in typo databases (LANG-006)
        IF token_lower IN cities_typo_db:
            canonical = cities_typo_db[token_lower]
            corrected.append(canonical)
            corrections.append({ original: token, corrected: canonical, source: "cities_typo", confidence: 0.85 })
            CONTINUE

        IF token_lower IN neighborhoods_typo_db:
            canonical = neighborhoods_typo_db[token_lower]
            corrected.append(canonical)
            corrections.append({ ... source: "neighborhoods_typo", confidence: 0.85 })
            CONTINUE

        IF token_lower IN property_types_typo_db:
            canonical = property_types_typo_db[token_lower]
            corrected.append(canonical)
            corrections.append({ ... source: "property_types_typo", confidence: 0.85 })
            CONTINUE

        IF token_lower IN whatsapp_typo_db:
            canonical = whatsapp_typo_db[token_lower]
            corrected.append(canonical)
            corrections.append({ ... source: "whatsapp_typo", confidence: 0.85 })
            CONTINUE

        IF token_lower IN general_typo_db:
            canonical = general_typo_db[token_lower]
            corrected.append(canonical)
            corrections.append({ ... source: "general_typo", confidence: 0.85 })
            CONTINUE

        # Priority 2: Levenshtein distance ≤ 3
        best_match = fuzzy_match(token_lower, all_known_terms) // Levenshtein
        IF best_match.distance <= 1:
            corrected.append(best_match.term)
            corrections.append({ ... source: "levenshtein_d1", confidence: 0.80 })
        ELSE IF best_match.distance <= 2:
            corrected.append(best_match.term)
            corrections.append({ ... source: "levenshtein_d2", confidence: 0.70 })
        ELSE IF best_match.distance <= 3:
            corrected.append(best_match.term)
            corrections.append({ ... source: "levenshtein_d3", confidence: 0.60 })
        ELSE:
            corrected.append(token)
            unknown.append(token)

    RETURN { corrected_tokens: corrected, corrections, unknown_tokens: unknown }
```

---

## 6. Pidgin Detection Algorithm

```
FUNCTION is_pidgin(tokens, bigrams):
    pidgin_keywords = {"how far", "wahala", "chap", "gbedu", "comot", "dey",
                       "sabi", "small", "plenty", "chop", "wetin", "na", "abeg"}
    pidgin_bigrams = {"how far", "how i fit", "wey match", "wetin be",
                      "your number", "don change", "i di", "i wan", "i dey",
                      "wey dey", "which land", "which project", "buyer dey",
                      "get money", "fine ?"}

    keyword_matches = count(tokens ∩ pidgin_keywords)
    bigram_matches = count(bigrams ∩ pidgin_bigrams)

    score = keyword_matches + (bigram_matches * 2)
    normalized_score = score / (len(pidgin_keywords) + len(pidgin_bigrams) * 2)

    RETURN normalized_score >= 0.15  // Lower threshold for pidgin due to smaller lexicon
```

---

## 7. WhatsApp Expression Normalization (Detailed)

```
FUNCTION normalize_whatsapp(text, language):
    # Common WhatsApp abbreviations — FR
    FR_ABBREVIATIONS = {
        "bjr": "bonjour", "slm": "salut", "stp": "s'il te plaît",
        "svp": "s'il vous plaît", "pk": "pourquoi", "mrc": "merci",
        "rdv": "rendez-vous", "tjrs": "toujours", "qqn": "quelqu'un",
        "qqch": "quelque chose", "cad": "c'est-à-dire", "bcp": "beaucoup",
        "jspr": "j'espère", "g": "j'ai", "t": "tu", "vs": "vous",
        "dsl": "désolé", "nv": "nouveau", "pb": "problème",
        "c": "c'est", "d": "de", "l": "le", "m": "me",
        "n": "nous", "s": "se", "tjs": "toujours",
        "jms": "jamais", "ac": "avec", "ap": "après",
        "appt": "appartement", "appart": "appartement",
        "meubl": "meublé", "négoc": "négociable",
        "dispo": "disponible", "chbres": "chambres"
    }

    # Common WhatsApp abbreviations — EN
    EN_ABBREVIATIONS = {
        "pls": "please", "thx": "thanks", "u": "you", "r": "are",
        "ur": "your", "ppl": "people", "btw": "by the way",
        "lol": "laughing", "omg": "oh my god", "idk": "i don't know",
        "tbh": "to be honest", "asap": "as soon as possible",
        "appt": "apartment", "apt": "apartment"
    }

    IF language == "FR":
        abbrev_map = FR_ABBREVIATIONS
    ELSE IF language == "EN":
        abbrev_map = EN_ABBREVIATIONS
    ELSE:
        abbrev_map = merge(FR_ABBREVIATIONS, EN_ABBREVIATIONS)

    # Apply replacements
    FOR abbr, expansion IN abbrev_map:
        text = replace_word(text, abbr, expansion)

    # Normalize missing apostrophes
    text = regex_replace(text, r'\b(jai|j\'ai)\b', "j'ai")
    text = regex_replace(text, r'\b(cest|c\'est)\b', "c'est")
    text = regex_replace(text, r'\b(jespere|j\'espere)\b', "j'espère")
    text = regex_replace(text, r'\b(tes|t\'es)\b', "t'es")
    text = regex_replace(text, r'\b(ilest|il\'est)\b', "il est")

    # Normalize repeated characters (max 3)
    text = regex_replace(text, r'(.)\1{3,}', r'\1\1\1')

    RETURN text
```

---

## 8. Short-Form Expansion (Abbreviations & Acronyms)

### 8.1 Real Estate Abbreviations

| Abbreviation | Expansion | Context |
|-------------|-----------|---------|
| M | million FCFA | After number: 5M = 5,000,000 |
| k | mille FCFA | After number: 150k = 150,000 |
| FCFA | Franc CFA | Currency indicator |
| T.F. / TF | Titre Foncier | Land title document |
| SIC | Société Immobilière du Cameroun | Public housing company |
| CC | Centre Commercial | Commercial center |
| CBA | Caisse de Base d'Appui | Financial institution |
| CIP | Certificat d'Inscription au Propriétaire | Ownership certificate |
| PU | Permis d'Urbanisme | Urban planning permit |
| CU | Certificat d'Urbanisme | Urban planning certificate |
| m2 / m² | mètre carré | Area measurement |
| ha | hectare | Land area (10,000 m²) |

### 8.2 Social Media Abbreviations

| Abbreviation | Expansion | Language |
|-------------|-----------|----------|
| bjr | bonjour | FR |
| slm | salut | FR |
| stp / svp | s'il te/vous plaît | FR |
| mrc | merci | FR |
| pk | pourquoi | FR |
| rdv | rendez-vous | FR |
| dsl | désolé | FR |
| bcp | beaucoup | FR |
| pls | please | EN |
| thx | thanks | EN |

### 8.3 Cameroon-Specific Short Forms

| Form | Expansion |
|------|-----------|
| appt / appart | appartement |
| meubl | meublé |
| négoc | négociable |
| dispo | disponible |
| chbres | chambres |
| chb | chambre |
| YDE | Yaoundé |
| DLA | Douala |
| BDA | Bamenda |
| BFS | Bafoussam |

### 8.4 Pricing Short-Form Expansion Algorithm

```
FUNCTION expand_pricing(text):
    # 150k → 150000
    text = regex_replace(text, r'(\d+)\s*k', lambda m: str(int(m[1]) * 1000))

    # 5M → 5000000
    text = regex_replace(text, r'(\d+)\s*M\b', lambda m: str(int(m[1]) * 1000000))

    # 10-15M → 10000000-15000000
    text = regex_replace(text, r'(\d+)\s*[–\-à]\s*(\d+)\s*M\b',
                         lambda m: f"{int(m[1]) * 1000000}-{int(m[2]) * 1000000}")

    RETURN text
```

---

## 9. Error Recovery Strategy

| Stage | Recoverable Error | Recovery Action |
|-------|-------------------|-----------------|
| 1 — Reception | empty_message | Return empty result, log |
| 2 — Language | detection_failed | Return FR (LANG-001), set low_confidence flag |
| 3 — Channel | normalization_failed | Use raw_text, log error |
| 4 — Spelling | too_many_unknowns | Skip spelling, use raw tokens |
| 5 — Alias | no_alias_match | Keep original term, reduced confidence |
| 6 — Extraction | no_location | Set null, flag for qualification |
| 7 — Ambiguity | high_ambiguity | Request clarification, do not proceed |
| 8 — Intent | no_intent | Default to SEARCH, low confidence |
| 9 — Facts | incomplete_facts | Flag for qualification flow |
| 10 — Confidence | very_low_confidence | Route for human review |

---

## 10. Pipeline Performance Characteristics

| Metric | Target | Threshold |
|--------|--------|-----------|
| Language detection accuracy | ≥ 95% | Minimum 85% |
| Spelling correction precision | ≥ 90% | Minimum 80% |
| Entity extraction recall | ≥ 85% | Minimum 70% |
| Intent classification accuracy | ≥ 90% | Minimum 80% |
| Pipeline end-to-end latency | ≤ 500ms | Maximum 2000ms |
| False positive typo correction | ≤ 2% | Maximum 5% |
