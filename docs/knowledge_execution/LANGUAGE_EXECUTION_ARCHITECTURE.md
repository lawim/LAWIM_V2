# LANGUAGE EXECUTION ARCHITECTURE — Language Engine LAWIM

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** LANGUAGE_MODEL.md, LANGUAGE_BUSINESS_KNOWLEDGE.md, RULE_INDEX.md (LANG-001 to LANG-014), NORMALIZATION_PIPELINE.md, ALIAS_RESOLUTION_CONTRACT.md, AMBIGUITY_HANDLING_POLICY.md

---

## 1. Language Engine Overview

The Language Engine consumes all LANG-001 to LANG-014 rules from Heritage Gold to provide multilingual detection, normalization, entity resolution, and response composition. It integrates with the Conversation Engine, Geography Engine, and Qualification Engine.

### 1.1 Rules Consumption Map

| Rule ID | Description | Engine Component | Status |
|---------|-------------|------------------|--------|
| LANG-001 | Default language: French | Language Detector | CANONICAL |
| LANG-002 | Detection hierarchy: DeepSeek → Gemini (commented) → Local rules | Language Detector | CANONICAL |
| LANG-003 | LANGUE command with persistence | Language Handler | CANONICAL |
| LANG-004 | 8 multilingual templates (FR/EN/PID) | Response Composer | CANONICAL |
| LANG-005 | 33 entity_linking entries with relation types | Entity Linker | CANONICAL |
| LANG-006 | 5 typo databases | Normalization Pipeline | CANONICAL |
| LANG-007 | 7 whatsapp_language files | WhatsApp Normalizer | CANONICAL |
| LANG-008 | 5 i18n documents (30-I18N-L10N-REFERENCE, 30A-30D) | I18N Manager | CANONICAL |
| LANG-009 | 38 country codes in phone_formatter | Phone Formatter | CANONICAL |
| LANG-010 | Cameroon format: 237 + 9 digits | Phone Formatter | CANONICAL |
| LANG-011 | WhatsApp link: https://wa.me/{normalized} | Phone Formatter | CANONICAL |
| LANG-012 | 14 Pidgin keywords for detection | Language Detector | PARTIAL |
| LANG-013 | 18 French keywords max | Language Detector | REFERENCE |
| LANG-014 | 18 English keywords max | Language Detector | REFERENCE |

---

## 2. Supported Languages

| Language | Code | Support Level | Default | Templates |
|----------|------|---------------|---------|-----------|
| French | FR | Full | Yes (LANG-001) | 8 templates complete |
| English | EN | Full | No | 8 templates complete |
| Pidgin Cameroon | PID | Partial | No | 8 templates (partial vocabulary) |
| Camfranglais | — | Expression-only | No | NOT a supported language |

### 2.1 Language Status Rules

1. **LANG-001** — Default language is French. Every new user without a stored preference receives French.
2. **LANG-002** — Detection hierarchy must be followed: DeepSeek AI first, then local keyword rules as fallback. Gemini is preserved as commented-out stub.
3. **LANG-003** — Language can be switched via `LANGUE` command. Switch is persisted per user across sessions. No conversation restart required.
4. **LANG-012** — Pidgin detection uses 14 keywords. Partial support — not all templates have full Pidgin vocabulary.
5. Camfranglais is explicitly NOT a supported language. It is only recognized at the expression level within the WhatsApp corpus (LANG-007).

---

## 3. Language Detection Hierarchy (LANG-002)

```
raw_message (string)
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. USER PREFERENCE CHECK       (LANG-001, LANG-003)              │
│    Check stored language for user_id                             │
│    Found → use language, confidence = 100                        │
│    Not found → proceed to detection                              │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. DEEPSEEK AI CLASSIFICATION  (LANG-002 — Priority 1)          │
│    Send message to DeepSeek for language classification          │
│    Returns: { language: "FR|EN|PID", confidence: 0.0–1.0 }      │
│    confidence ≥ 0.70 → accept, persist for user (LANG-003)      │
│    confidence < 0.70 → fall through                              │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. GEMINI AI CLASSIFICATION    (LANG-002 — Priority 2)          │
│    Commented out — NOT implemented                               │
│    Preserved as stub for future integration                      │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. LOCAL KEYWORD RULES         (LANG-002 — Priority 3, fallback) │
│    Keyword frequency analysis per language                       │
│    French keywords: 18 words (LANG-013)                          │
│    English keywords: 18 words (LANG-014)                         │
│    Pidgin keywords: 14 words (LANG-012)                          │
│    Highest frequency wins → primary language                     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. FALLBACK CHAIN                                               │
│    Known language for user → French (default) →                  │
│    Request explicit clarification                                │
└─────────────────────────────────────────────────────────────────┘
```

### 3.1 Detection Signals

Language can be deduced from up to 10 signals, evaluated in order:

1. User preference (stored per user_id)
2. Current session language
3. Device settings (where available)
4. `Accept-Language` header (API requests)
5. `Content-Language` header (API requests)
6. Input text content (keyword analysis)
7. Conversation history (persistence per LANG-003)
8. Channel configuration (WhatsApp account language, etc.)
9. Admin configuration (forced language for specific flows)
10. Fallback rule (French per LANG-001)

### 3.2 Detection Output

```json
{
  "language": "FR",
  "confidence": 0.95,
  "method": "deepseek|local_keywords|user_preference",
  "fallback_used": false,
  "detected_at": "2026-07-15T10:30:00Z"
}
```

### 3.3 Language Detection Algorithm (Local Keywords)

```
INPUT: message_text

1. Tokenize message into words (lowercase, strip punctuation)
2. Initialize scores: FR=0, EN=0, PID=0
3. For each token:
   a. If token in French_keywords[18]: FR += 1
   b. If token in English_keywords[18]: EN += 1
   c. If token in Pidgin_keywords[14]: PID += 1
4. Apply Pidgin multi-word check (e.g., "how far", "how i fit"):
   a. Check bigrams against Pidgin_phrases[] list
5. Normalize scores by keyword count per language:
   score_FR = FR / 18
   score_EN = EN / 18
   score_PID = PID / 14 (+ phrase bonuses)
6. If any score >= 0.30: primary_language = argmax(scores)
7. Else: return French (default, LANG-001)
8. Confidence = max(scores) * 100
OUTPUT: { language, confidence, method: "local_keywords" }
```

### 3.4 Ambiguity Handling (Language)

| Condition | Action |
|-----------|--------|
| Two languages tied within 5% | Use previous language if known; else French |
| No language detected above threshold | Use French (LANG-001) |
| Pidgin detected alongside FR/EN | Prefer FR/EN if scores are close; flag as mixed |
| Camfranglais detected | Treat as French with code-switching expressions |

---

## 4. Entity Linking (LANG-005)

### 4.1 33 Entry Entity Linking Structure

Source: `entity_linking.json` — 20 documented pairs (entity_linking) + property_type_aliases + search_aliases

**Relation Types:**

| Relation | Description | Example |
|----------|-------------|---------|
| `equivalent_to` | Direct equivalence | terrain ↔ parcelle |
| `synonym` | Cross-language or regional synonym | bureau ↔ office |
| `related_to` | Related concept (not exact) | parking ↔ stationnement |
| `typo_of` | Common misspelling mapping | appartemant → appartement |
| `abbreviation_of` | Abbreviation expansion | appt → appartement |

**Entity Linking Resolution:**

```
INPUT: source_term (string)

1. Normalize source_term (lowercase, trim, strip diacritics)
2. Check exact match in entity_linking[].source_entity
   → Found: return { target_entity, relation_type, confidence: 1.0 }
3. Check alias resolution (see ALIAS_RESOLUTION_CONTRACT.md)
4. Check typo database (LANG-006)
5. Check abbreviation expansion
6. Fallback: return source_term unchanged, confidence: 0.3

OUTPUT: { resolved_term, relation_type, confidence, domain }
```

**Entity Linking Examples (20 pairs from entity_linking.json):**

| Source | Target | Relation |
|--------|--------|----------|
| terrain | parcelle | equivalent_to |
| villa | maison de luxe | equivalent_to |
| appartement | appart | abbreviation_of |
| commerce | boutique | equivalent_to |
| bureau | office | synonym |
| immeuble | building | synonym |
| studio | one-room | equivalent_to |
| entrepôt | warehouse | synonym |
| climatisation | AC | abbreviation_of |
| parking | stationnement | related_to |
| piscine | swimming pool | synonym |
| gardien | security | synonym |
| meublé | furnished | synonym |
| non meublé | unfurnished | synonym |
| titre foncier | land title | synonym |
| notaire | lawyer | related_to |
| bail | lease | synonym |
| caution | deposit | synonym |
| agence | agency | synonym |
| commission | fee | synonym |

### 4.2 Search Alias Resolution (17 items, EN→FR)

| English | French Canonical |
|---------|------------------|
| apartment, flat | appartement |
| house, home | maison |
| land, plot, parcel | terrain |
| villa | villa |
| luxury | villa de luxe |
| office, workspace | bureau |
| warehouse | entrepôt |
| storage | dépôt |
| shop | boutique |
| store | commerce |
| building | immeuble |
| room | chambre |

### 4.3 Abbreviation Expansion

**Real Estate Abbreviations:**

| Abbrev | Expansion |
|--------|-----------|
| M | million (XAF) |
| k | thousand (XAF) |
| FCFA | Franc CFA (XAF) |
| T.F. / TF | Titre Foncier |
| SIC | Société Immobilière du Cameroun |
| CC | Centre Commercial |
| CBA | Caisse de Base d'Appui |
| CIP | Certificat d'Inscription au Propriétaire |
| PU | Permis d'Urbanisme |
| CU | Certificat d'Urbanisme |

**Social Abbreviations:**

| Abbrev | Expansion |
|--------|-----------|
| m2 / m² | mètre carré |
| ha | hectare |
| chbres | chambres |
| appt / appart | appartement |
| meubl | meublé |
| négoc | négociable |
| dispo | disponible |

**City Abbreviations (10 cities):**

| Abbrev | City |
|--------|------|
| YDE | Yaoundé |
| DLA | Douala |
| BDA | Bamenda |
| BFS | Bafoussam |
| BUE | Buea |
| KRI | Kribi |
| NKS | Nkongsamba |
| MRA | Maroua |
| LIM | Limbe |
| GAR | Garoua |

---

## 5. Typo Databases (LANG-006)

### 5.1 Database Inventory

| # | File | Domain | Coverage | Description |
|---|------|--------|----------|-------------|
| 1 | `cities_typo.json` | Cities | 10 cities, 4–9 variants each | City name misspellings |
| 2 | `neighborhoods_typo.json` | Neighborhoods | 11 neighborhoods with variants | Neighborhood name misspellings |
| 3 | `property_types_typo.json` | Property Types | 9 property types with variants | Property type misspellings |
| 4 | `whatsapp_typo.json` | WhatsApp | WhatsApp-specific typos | Social/mobile typos |
| 5 | `typo_database.json` | General (aggregated) | 49 entries, 3–6 variants each | Master typo database |

### 5.2 City Typo Variants

| Canonical | Variants |
|-----------|----------|
| Yaoundé | yaound, yaoundee, yaoundeee, yaounde1, yaonde, yaond, yaoundéé, yaounder, yyaounde, yaund, yaundee, yaounde_, yaounde3, yaound3, yand, yde3 |
| Douala | duala, dla, douala3, doualaa, doual, doulala, doual3, dual, douall, doula |
| Buea | buea3, bueaa, bueah, bue, buea town, bueatown, buea-town, buea_ |
| Bafoussam | bafousam, bafoussam3, bafoussan, bafousan, bafoussamm, bafoussama |
| Bamenda | bamenda3, bamend, bamendaa, bamenda_, bamend3, bamenda town |
| Limbe | limb, limbee |
| Kribi | kribi3, kribi_, krib, kribii |
| Garoua | garoua3, garouaa, garoua_ |
| Maroua | maroua3, marouaa, maroua_, marou |
| Nkongsamba | nkonsamba, nkongsmba, nkongsambaa |
| Ngaoundéré | ngaoundr, ngaounderee, ngaoundere3, ngaoundr3, ngaound, ngaound3 |

### 5.3 Neighborhood Typo Variants

| Canonical | Variants |
|-----------|----------|
| Odza | odza3, odzaa, odza_, odaz |
| Makepe | makepe3, makepea, makepe_, makep, makpe |
| Bonapriso | bonapriso3, bonaprisoo, bonapriso_, bonapreso |
| Akwa | akwa3, akwa_, akwaa, akw |
| Bastos | bastos3, bastosa, bastos_, basto |
| Mendong | mendong3, mendonga, mendong_, mendng |

### 5.4 Property Type Typo Variants

| Canonical | Variants |
|-----------|----------|
| appartement | appartement3, appart, appartment, apartement |
| villa | villa3, villaa, villa_, vlla, villla |
| terrain | terrain3, terrains, terraing, terrain_, terain, terraine |
| maison | maison3, maisons, maizo, maison_, maizone |
| duplex | duplex3, dup1ex, dupelx, duplx, dupex |
| bureau | bureau3, bureaux, burau, bureau_, breaux |
| commerce | commerce3, comerce, commerces, commerce_, commercia |
| studio | studio3, studios, studio_, studioo |
| immeuble | immeuble3, immeubles, imuble, immeuble_, immuble |

### 5.5 General Typo Variants

| Canonical | Variants |
|-----------|----------|
| meublé | meuble3, meubles, meuble_, meubl, meublee |
| négociable | negociable, negociable3, ngociable_, negociabl, negociablee |
| budget | budget3, budgets, budget_, budjet |
| urgent | urgent3, urgents, urgemt, urgent_ |
| climatisation | climatisation3, climatization, climatisation, climat |

---

## 6. WhatsApp Language Corpus (LANG-007)

### 6.1 File Inventory

| # | File | # Entries | Description |
|---|------|-----------|-------------|
| 1 | `whatsapp_language.json` | 697 lines | Full multilingual corpus FR/EN/PID/Camfranglais for all intents |
| 2 | `diaspora_language.json` | 9 items | Diaspora language patterns |
| 3 | `investor_language.json` | 8 items | Investor language patterns |
| 4 | `negotiation.json` | 8 items | Negotiation terms |
| 5 | `property_listing.json` | — | Property listing expressions |
| 6 | `property_search.json` | — | Property search expressions |
| 7 | `urgency_signals.json` | 8 items | Urgency signal expressions |

### 6.2 Intent → Expression Matrix

| Intent | FR | EN | PID | Camfranglais |
|--------|----|----|-----|--------------|
| Buy | je veux acheter un terrain | i want to buy land | i wan buy house | je need un terrain |
| Rent | je cherche appartement à louer | looking for apartment | i wan rent house | je cherche appartement |
| Sell | je vends une maison | house for sale | i di sell house | terrain à vendre prix ngociable |
| Invest | je veux investir dans l'immobilier | real estate investment | i wan invest | jai budget 10M pour land |
| Search | je cherche une maison | looking for property | i di find land | je cherche un land |
| Negotiate | dernier prix ? | best price? | price fine? | prix ngociable ? |

### 6.3 Diaspora Language Patterns (9 items)

| Pattern | Intent | Language |
|---------|--------|----------|
| je suis en france | INVESTOR_INTENT | FR |
| je suis au canada | INVESTOR_INTENT | FR |
| je suis en belgique | INVESTOR_INTENT | FR |
| i am in the usa | INVESTOR_INTENT | EN |
| i am in canada | INVESTOR_INTENT | EN |
| je veux acheter à distance | INVESTOR_INTENT | FR |
| buying remotely | INVESTOR_INTENT | EN |
| je veux construire au pays | INVESTOR_INTENT | FR |
| i want to build in cameroon | INVESTOR_INTENT | EN |

### 6.4 Investor Language Patterns (8 items)

| Pattern | Language | Priority |
|---------|----------|----------|
| je veux investir | FR | P0 |
| rendement locatif | FR | P0 |
| cashflow | FR/EN | P0 |
| retour sur investissement | FR | P0 |
| ROI | EN | P0 |
| yield | EN | P0 |
| rentabilité | FR | P0 |
| patrimoine | FR | P1 |

### 6.5 Negotiation Terms (8 items)

| Term | Language | Type |
|------|----------|------|
| dernier prix | FR | final_price |
| prix négociable | FR | negotiable |
| à débattre | FR | negotiable |
| prix ferme | FR | fixed |
| best price | EN | final_price |
| nego possible | FR/EN | negotiable |
| on peut s'entendre | FR | negotiable |
| combien dernier ? | FR | price_query |

### 6.6 Urgency Signals (8 items)

| Signal | Language | Action |
|--------|----------|--------|
| urgent | FR | Raise priority |
| très urgent | FR | Highest priority |
| asap | EN | Raise priority |
| immédiatement | FR | Highest priority |
| aujourd'hui | FR | Compress to today |
| avant fin semaine | FR | Compress to EOW |
| je déménage demain | FR | Emergency |
| need now | EN | Raise priority |

### 6.7 WhatsApp Expression Normalization

```
INPUT: raw_whatsapp_message

1. Normalize WhatsApp-specific patterns:
   "stp" → "s'il te plaît"
   "pk" → "pourquoi"
   "bjr" → "bonjour"
   "slm" → "salut"
   "merki" → "merci"
   (sourced from whatsapp_typo.json and common_abbreviations)
2. Expand short forms:
   "jai" → "j'ai"
   "cest" → "c'est"
   "jespere" → "j'espère"
3. Match against WhatsApp corpus patterns (LANG-007)
4. Tag matched intent, language, confidence

OUTPUT: { normalized_text, matched_intent, language, confidence }
```

---

## 7. Phone Formatting (LANG-009, LANG-010, LANG-011)

### 7.1 Phone Formatter Specifications

| Property | Value |
|----------|-------|
| Country codes supported | 38 (LANG-009) |
| Cameroon format | 237 + 9 digits (LANG-010) |
| WhatsApp link format | `https://wa.me/{normalized}` (LANG-011) |
| Normalization rule | Strip spaces, dashes, leading `+` or `00`, keep only digits |

### 7.2 Normalization Algorithm

```
INPUT: raw_phone (string)

1. Strip whitespace, dashes, parentheses
2. Remove leading "+" or "00"
3. Keep only digit characters
4. If length == 9 and no country code → prepend "237" (Cameroon, LANG-010)
5. If length == 13 and starts with "237" → keep as is
6. If length == 11 and starts with "237" → keep (valid Cameroon mobile)
7. Otherwise → treat as international, preserve country code
8. Generate WhatsApp URL: "https://wa.me/" + normalized_phone (LANG-011)

OUTPUT: { normalized_phone, country_code, is_cameroon, whatsapp_url }
```

### 7.3 Phone-Based Identity Resolution

| Match Criteria | Score |
|---------------|-------|
| Phone exact match | 100 (highest confidence) |
| Email match | 95 |
| Name + phone (combined) | ≥40 |
| Name only | Lower confidence |

### 7.4 Diaspora Detection via Phone

International dialing codes from 38 supported country codes are used as diaspora indicators alongside textual diaspora patterns (LANG-007).

---

## 8. Multilingual Response Templates (LANG-004)

### 8.1 Template Inventory (8 templates × 3 languages)

| Template | FR | EN | PID |
|----------|----|----|-----|
| welcome | Bienvenue sur LAWIM | Welcome to LAWIM | You welcome for LAWIM |
| help | Comment puis-je vous aider ? | How can I help you? | How I fit help you? |
| no_match | Désolé, aucun bien trouvé | Sorry, no property found | No property wey match |
| thanks | Merci de votre confiance | Thank you for your trust | Tank you for your trust |
| ask_name | Quel est votre nom ? | What is your name? | Wetin be your name? |
| ask_phone | Quel est votre numéro ? | What is your phone number? | Your number na wetin? |
| stats | Voici les statistiques | Here are the statistics | Stats dey here |
| language_changed | Langue changée en français | Language changed to English | We don change di language |

### 8.2 Response Composition

```
INPUT: template_key, language, context_data

1. Resolve language using detection hierarchy (LANG-002)
2. Select template by key + language from template store
3. Inject context data (name, count, property info, etc.)
4. Apply property display format (all languages):
   N. *description*\n📍 localisation\n💰 prix\n⭐ notes
5. Return composed string

OUTPUT: composed_response (string)
```

### 8.3 Response Hierarchy (LANG-004)

DeepSeek AI → Local Rules → Templates (fallback order)

---

## 9. Integration with Other Engines

### 9.1 Conversation Engine

- Language Engine provides `context.language` to Conversation Engine after detection
- Conversation Engine sends raw messages to Language Engine for normalization
- Response templates are served by Language Engine for Conversation Engine composition

### 9.2 Geography Engine

- Language Engine normalizes location strings before Geography Engine resolution
- City/neighborhood typo databases (LANG-006) shared with Geography Engine
- Entity linking (LANG-005) for geographic aliases consumed by Geography Engine

### 9.3 Qualification Engine

- Language Engine provides detected intent from WhatsApp corpus (LANG-007)
- Urgency signals (urgency_signals.json) influence lead scoring in Qualification Engine
- Diaspora patterns from Language Engine feed diaspora detection in Qualification Engine
- Phone formatting (LANG-009, LANG-010, LANG-011) used for identity resolution in Qualification Engine

---

## 10. I18N Management (LANG-008)

### 10.1 I18N Document Inventory

| # | Document | Content |
|---|----------|---------|
| 1 | 30-I18N-L10N-REFERENCE.md | Master internationalization & localization reference |
| 2 | 30A-BUSINESS-DICTIONARY-REFERENCE.md | Official business dictionary |
| 3 | 30B-TRANSLATION-REFERENCE.md | Translation key & version management |
| 4 | 30C-LANGUAGE-DETECTION-REFERENCE.md | Language detection architecture |
| 5 | 30D-MULTILINGUAL-SEARCH-REFERENCE.md | Multilingual tolerant search |

### 10.2 Core I18N Principles

1. Language is a native context data — Never hardcoded in business components
2. All layers display, interpret, and log information in multiple languages without changing business logic
3. 3 official languages: French (default), English, Pidgin
4. Adding a new language must be possible without modifying the business model
5. Fallback chain: User's known language → French (LANG-001)

### 10.3 Translation Key Management

- Every displayable text must be attached to a stable key (LANG-008)
- Each key must be: unique, versioned, traceable, reusable, independent of final rendering
- Each translation must preserve: source version, translated version, date, author, validation, history
- Sources: business reference, admin validator, LAWIM AI, human translator, controlled import/export
- LAWIM AI never publishes critical translations without human validation

---

## 11. Business Dictionary (30 Real Estate Terms)

| FR Term | EN Translation | Category |
|---------|---------------|----------|
| titre foncier | land title | Document |
| notaire | notary | Legal |
| propriétaire | owner | Role |
| acheteur | buyer | Role |
| vendeur | seller | Role |
| locataire | tenant | Role |
| caution | deposit | Financial |
| loyer | rent | Financial |
| commission | commission | Financial |
| bail | lease | Document |
| acte de vente | sale deed | Document |
| permis de construire | building permit | Document |
| certificat de propriété | certificate of ownership | Document |
| superficie | surface area | Property |
| pièce | room | Property |
| chambre | bedroom | Property |
| salle de bain | bathroom | Property |
| cuisine | kitchen | Property |
| salon | living room | Property |
| meublé | furnished | Property |
| non meublé | unfurnished | Property |
| climatisation | air conditioning | Amenity |
| parking | parking | Amenity |
| gardien | guard/security | Amenity |
| piscine | swimming pool | Amenity |
| groupe électrogène | generator | Amenity |
| forage | borehole | Amenity |
| viabilisé | serviced (utilities) | Land |
| constructible | buildable | Land |
| mitoyen | semi-detached | Property |

---

## 12. Pidgin Cameroon Support (LANG-012)

### 12.1 Detection Keywords (14)

| # | Keyword | # | Keyword |
|---|---------|---|---------|
| 1 | how far | 8 | small |
| 2 | wahala | 9 | plenty |
| 3 | chap | 10 | chop |
| 4 | gbedu | 11 | wetin |
| 5 | comot | 12 | na |
| 6 | dey | 13 | abeg |
| 7 | sabi | 14 | — |

### 12.2 Pidgin Expression Corpus

**Buy (5):** i wan buy house, i wan buy land, which land dey available, i di find land, i dey search land

**Rent (3):** i di find house, i wan rent house, house dey ?

**Sell (3):** i di sell house, i get land for sale, buyer dey ?

**Invest (3):** i wan invest, which project fine, i get money for build

### 12.3 Camfranglais Handling

Camfranglais is NOT a supported language. It is present only in the WhatsApp expression corpus (LANG-007). Expressions like "je need un terrain", "je cherche un land" enrich detection but do not constitute a 4th language.

---

## 13. Confidence Calculation

### 13.1 Language Detection Confidence

| Method | Base Confidence | Modifiers |
|--------|----------------|-----------|
| User preference stored | 100 | — |
| DeepSeek AI (≥0.70) | 70–99 | Score × 100 |
| Local keyword rules | 30–85 | Keyword density × language weight |
| Fallback (French) | 50 | Default language (LANG-001) |

### 13.2 Entity Resolution Confidence

| Resolution Method | Confidence |
|-------------------|------------|
| Exact match in entity_linking | 1.0 |
| Alias resolution (search_aliases) | 0.95 |
| Abbreviation expansion | 0.90 |
| Typo database match | 0.85 |
| Levenshtein ≤ 1 | 0.80 |
| Levenshtein ≤ 2 | 0.70 |
| Levenshtein ≤ 3 | 0.60 |
| No resolution | 0.30 |
