# LANGUAGE BUSINESS KNOWLEDGE — LAWIM Heritage Gold (H0.4)

**Mission:** LAWIM Heritage Completion H0.4 — Language Historian Extraction  
**Date:** 15 July 2026  
**Status:** COMPLETE — All language/linguistic business knowledge extracted from heritage sources  

---

## Table of Contents

1. [Language Support (Languages, Status, Detection)](#1-language-support)
2. [Language Detection Rules and Hierarchy](#2-language-detection-rules-and-hierarchy)
3. [Multilingual Response Templates](#3-multilingual-response-templates)
4. [Entity Linking Rules (All Entries with Relation Types)](#4-entity-linking-rules)
5. [Typo Databases Coverage](#5-typo-databases-coverage)
6. [WhatsApp Language Corpus Categories](#6-whatsapp-language-corpus-categories)
7. [Phone Formatting Rules](#7-phone-formatting-rules)
8. [Search Aliases](#8-search-aliases)
9. [Internationalization Strategy](#9-internationalization-strategy)
10. [Business Dictionary](#10-business-dictionary)
11. [Translation Rules](#11-translation-rules)
12. [Camfranglais/Pidgin Handling](#12-camfranglaispidgin-handling)
13. [All Business Rules for Language](#13-all-business-rules-for-language)
14. [Source References](#14-source-references)

---

## 1. Language Support

### Supported Languages

| Language | Support Level | Code | Status |
|----------|--------------|------|--------|
| French | Full | FR | Default language |
| English | Full | EN | Full support |
| Pidgin Cameroon | Partial | PID | 14 keyword detection, partial templates |
| Camfranglais | Expression-only | — | NOT a supported language; present only in WhatsApp expression corpus |

### Languages NOT Supported
- Camfranglais is explicitly NOT a supported language — it is only recognized at the expression level within the WhatsApp language corpus.

### Language Persistence Rules
1. Language persistence is maintained per user (detected language is stored and reused across sessions).
2. Language can be manually switched via the `LANGUE` command.
3. Language switching does NOT require restarting the conversation.
4. Default language: French.
5. User preference must be memorized locally and reapplied after reconnection.

---

## 2. Language Detection Rules and Hierarchy

### Detection Pipeline (3 Levels)

| Priority | Method | Status |
|----------|--------|--------|
| 1st | DeepSeek AI classification | Implemented |
| 2nd | Gemini AI classification | **Not implemented (commented out)** |
| 3rd | Local keyword-based rules | Implemented (fallback) |

### Detection Signals
Language can be deduced from:
1. User preference (stored)
2. Current session
3. Device settings
4. `Accept-Language` header
5. `Content-Language` header
6. Input text content
7. Conversation history
8. Channel configuration
9. Admin configuration
10. Fallback rule

### French Detection Keywords (18 words)

| # | Word | # | Word |
|---|------|---|------|
| 1 | bonjour | 10 | budget |
| 2 | salut | 11 | urgent |
| 3 | appartement | 12 | merci |
| 4 | maison | 13 | je |
| 5 | terrain | 14 | tu |
| 6 | location | 15 | il |
| 7 | achat | 16 | elle |
| 8 | vente | 17 | nous |
| 9 | prix | 18 | vous |

### English Detection Keywords (18 words)

| # | Word | # | Word |
|---|------|---|------|
| 1 | hello | 10 | budget |
| 2 | hi | 11 | urgent |
| 3 | apartment | 12 | thanks |
| 4 | house | 13 | i |
| 5 | land | 14 | you |
| 6 | rent | 15 | he |
| 7 | buy | 16 | she |
| 8 | sale | 17 | we |
| 9 | price | 18 | they |

### Pidgin Cameroon Detection Keywords (14 keywords)

| # | Keyword | # | Keyword |
|---|---------|---|---------|
| 1 | how far | 8 | small |
| 2 | wahala | 9 | plenty |
| 3 | chap | 10 | chop |
| 4 | gbedu | 11 | wetin |
| 5 | comot | 12 | na |
| 6 | dey | 13 | abeg |
| 7 | sabi | 14 | — |

### Language Detection Rules (Directive 30C)
1. Must produce a primary language and a confidence level.
2. Must preserve the fallback language.
3. Must log the decision.
4. Must allow manual correction.
5. In case of ambiguity: stay in previous language if known; otherwise fall back to French; otherwise ask for explicit clarification.
6. Detection quality must be evaluated on: precision, recall, manual correction rate, fallback rate, response stability.

### Fallback Chain
1. Language known for user → use it
2. French (default)
3. No fallback → request explicit clarification

---

## 3. Multilingual Response Templates

### 8 Templates in FR/EN/PID

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

### Property Display Format
All languages: `N. *description*\n📍 localisation\n💰 prix\n⭐ notes`

### Response Hierarchy
DeepSeek → Local Rules → Templates

---

## 4. Entity Linking Rules

### Source: `entity_linking.json` (167 lines) — 20 linked entity pairs

| # | Source Entity | Linked Entity | Relation Type |
|---|---------------|---------------|---------------|
| 1 | terrain | parcelle | equivalent_to |
| 2 | villa | maison de luxe | equivalent_to |
| 3 | appartement | appart | abbreviation_of |
| 4 | commerce | boutique | equivalent_to |
| 5 | bureau | office | synonym |
| 6 | immeuble | building | synonym |
| 7 | studio | one-room | equivalent_to |
| 8 | entrepôt | warehouse | synonym |
| 9 | climatisation | AC | abbreviation_of |
| 10 | parking | stationnement | related_to |
| 11 | piscine | swimming pool | synonym |
| 12 | gardien | security | synonym |
| 13 | meublé | furnished | synonym |
| 14 | non meublé | unfurnished | synonym |
| 15 | titre foncier | land title | synonym |
| 16 | notaire | lawyer | related_to |
| 17 | bail | lease | synonym |
| 18 | caution | deposit | synonym |
| 19 | agence | agency | synonym |
| 20 | commission | fee | synonym |

### Relation Types Used
- `equivalent_to` — Direct equivalence
- `synonym` — Cross-language or regional synonym
- `related_to` — Related concept (not exact synonym)
- `typo_of` — Common misspelling mapping
- `abbreviation_of` — Abbreviation expansion

### Real Estate Abbreviation Mappings

| Abbreviation | Expansion |
|-------------|-----------|
| M | million (XAF) |
| k | thousand (XAF) |
| FCFA | Franc CFA (XAF) |
| T.F. / TF | Titre Foncier (land title) |
| SIC | Société Immobilière du Cameroun |
| CC | Centre Commercial |
| CBA | Caisse de Base d'Appui |
| CIP | Certificat d'Inscription au Propriétaire |
| PU | Permis d'Urbanisme |
| CU | Certificat d'Urbanisme |

### Social Abbreviations

| Abbreviation | Expansion |
|-------------|-----------|
| m2 / m² | mètre carré |
| ha | hectare |
| chbres | chambres |
| appt / appart | appartement |
| meubl | meublé |
| négoc | négociable |
| dispo | disponible |

### City Abbreviations

| Abbreviation | City |
|-------------|------|
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

## 5. Typo Databases Coverage

### 5 Typo Databases (Source: `typo_database/`)

| # | Database File | Domain | # Entries | Description |
|---|--------------|--------|-----------|-------------|
| 1 | cities_typo.json | Cities | 10 cities, 4–9 variants each | City name typos |
| 2 | neighborhoods_typo.json | Neighborhoods | 11 neighborhoods with variants | Neighborhood name typos |
| 3 | property_types_typo.json | Property Types | 9 property types with variants | Property type typos |
| 4 | typo_database.json | Aggregated | 49 entries, 3–6 variants each | Master typo database |
| 5 | whatsapp_typo.json | WhatsApp | WhatsApp-specific typos | Social/mobile typos |

### City Typo Variants

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

### Neighborhood Typo Variants

| Canonical | Variants |
|-----------|----------|
| Odza | odza3, odzaa, odza_, odaz |
| Makepe | makepe3, makepea, makepe_, makep, makpe |
| Bonapriso | bonapriso3, bonaprisoo, bonapriso_, bonapreso |
| Akwa | akwa3, akwa_, akwaa, akw |
| Bastos | bastos3, bastosa, bastos_, basto |
| Mendong | mendong3, mendonga, mendong_, mendng |

### Property Type Typo Variants

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

### General Typo Variants

| Canonical | Variants |
|-----------|----------|
| meublé | meuble3, meubles, meuble_, meubl, meublee |
| négociable | negociable, negociable3, ngociable_, negociabl, negociablee |
| budget | budget3, budgets, budget_, budjet |
| urgent | urgent3, urgents, urgemt, urgent_ |
| climatisation | climatisation3, climatization, climatisation, climat |

### Property Type Typo Mappings (Direct)

| Typo | Canonical |
|------|-----------|
| appartemant | appartement |
| appartementt | appartement |
| maisn | maison |
| maisoon | maison |
| terin | terrain |
| terrian | terrain |
| terain | terrain |
| teraine | terrain |
| vilaa | villa |
| vilage | maison |
| studeo | studio |
| studyo | studio |
| bereau | bureau |
| immuble | immeuble |

---

## 6. WhatsApp Language Corpus Categories

### 7 WhatsApp Language Files

| # | File | # Entries | Description |
|---|------|-----------|-------------|
| 1 | whatsapp_language.json | 697 lines | Full multilingual corpus FR/EN/PID/Camfranglais for all intents |
| 2 | diaspora_language.json | 9 items | Diaspora language patterns |
| 3 | investor_language.json | 8 items | Investor language patterns |
| 4 | negotiation.json | 8 items | Negotiation terms |
| 5 | property_listing.json | — | Property listing expressions |
| 6 | property_search.json | — | Property search expressions |
| 7 | urgency_signals.json | 8 items | Urgency signal expressions |

### Intent → Expression Matrix (FR/EN/PID/Camfranglais)

| Intent | FR Example | EN Example | PID Example | Camfranglais Example |
|--------|-----------|-----------|-------------|----------------------|
| Buy | je veux acheter un terrain | i want to buy land | i wan buy house | je need un terrain |
| Rent | je cherche appartement à louer | looking for apartment | i wan rent house | je cherche appartement |
| Sell | je vends une maison | house for sale | i di sell house | terrain à vendre |
| Invest | je veux investir dans l'immobilier | real estate investment | i wan invest | jai budget 10M pour land |
| Search | je cherche une maison | looking for property | i di find land | je cherche un land |
| Negotiate | dernier prix ? | best price? | price fine? | prix ngociable ? |

### Diaspora Language Patterns (9 items)

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

### Investor Language Patterns (8 items)

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

### Negotiation Terms (8 items)

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

### Property Listing/Search Expressions (17 items)

| Expression | Intent | Language |
|------------|--------|----------|
| maison à vendre | SELL | FR |
| terrain à vendre | SELL | FR |
| appartement à louer | RENT | FR |
| chambre à louer | RENT | FR |
| studio meublé | RENT | FR |
| house for sale | SELL | EN |
| land for sale | SELL | EN |
| apartment for rent | RENT | EN |
| rooms available | RENT | EN |
| house dey ? | RENT | PID |
| which land dey | SEARCH | PID |
| je cherche une maison | SEARCH | FR |
| je veux acheter | BUY | FR |
| looking to buy | BUY | EN |
| i wan buy | BUY | PID |
| urgent besoin | URGENT | FR |
| need now | URGENT | EN |

### Urgency Signals (8 items)

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

### French Expressions (Common Expressions)

**Buy (6):** je veux acheter, terrain à vendre, je cherche une maison à acheter, je veux devenir propriétaire, je cherche un immeuble

**Rent (5):** je veux louer, je cherche une maison, besoin d'un appartement, location urgente, qui a une maison disponible

**Sell (6):** je vends, maison à vendre, terrain à vendre, vente urgente, propriétaire direct, je cherche acheteur

**Invest (6):** je veux investir, je cherche un projet rentable, je veux construire, je suis en france, je veux acheter à distance, je cherche un immeuble locatif

**Negotiate (7):** dernier prix, prix ferme, prix négociable, à débattre, on peut s'entendre, nego possible, combien dernier ?

**Diaspora (5):** je suis en france, je suis au canada, je suis en belgique, je veux acheter à distance, je veux construire au pays

### English Expressions

**Buy (5):** i want to buy, looking to purchase, house for sale, land for sale, looking for land

**Rent (3):** looking for apartment, need house urgently, want to rent

**Sell (4):** house for sale, land for sale, selling property, looking for buyer

**Invest (4):** looking for investment, looking for ROI, real estate investment, buying remotely

### Pidgin Expressions

**Buy (5):** i wan buy house, i wan buy land, which land dey available, i di find land, i dey search land

**Rent (3):** i di find house, i wan rent house, house dey ?

**Sell (3):** i di sell house, i get land for sale, buyer dey ?

**Invest (3):** i wan invest, which project fine, i get money for build

### Camfranglais Expressions

**Buy (4):** je need un terrain, je cherche un land, je want acheter terrain, j'ai budget 10M pour land

**Sell (2):** je vends terrain, terrain à vendre prix ngociable

**Rent (1):** je cherche appartement à louer

---

## 7. Phone Formatting Rules

### Phone Formatter Specifications
1. **Source file:** `phone_formatter.py`
2. **Country codes supported:** 38 country codes
3. **Cameroon format:** `237` + 9 digits
4. **WhatsApp link format:** `https://wa.me/{normalized}`
5. **Normalization:** Strip spaces, dashes, leading `+` or `00`, keep only digits

### Phone-Based Identity Resolution
| Match Criteria | Score |
|---------------|-------|
| Phone exact match | 100 (highest confidence) |
| Email match | 95 |
| Name + phone (combined score) | ≥40 |
| Name only | Lower confidence |

### Diaspora Detection via Phone
- International dialing codes are used as diaspora indicators alongside textual patterns.

---

## 8. Search Aliases

### Property Type Normalisation Mappings (EN → FR) — 17 items

| English | French (Canonical) |
|---------|-------------------|
| apartment | appartement |
| flat | appartement |
| house | maison |
| home | maison |
| land | terrain |
| plot | terrain |
| parcel | terrain |
| villa | villa |
| luxury | villa de luxe |
| office | bureau |
| workspace | bureau |
| warehouse | entrepôt |
| storage | dépôt |
| shop | boutique |
| store | commerce |
| building | immeuble |
| room | chambre |

### Property Type Alias Mappings (Comprehensive — 11 Types)

| Canonical FR | Aliases (EN + FR + abbreviations + common variants) |
|-------------|------------------------------------------------------|
| appartement | appart, appt, apartment, flat, apart, apparte, appartement meublé, appartement non meublé |
| studio | flat, efficiency, chambre meublée, stud, studeo, studyo, studios |
| chambre | room, chb, cham, chambre meublée, chambre à louer, chambre seule, chambre simple, chambre à coucher, bedroom, single room, chamb |
| maison | house, home, msn, maisonnette, maison individuelle, maison basse, family house, mason, maison entière, villa |
| villa | luxury house, villa de luxe, luxury home, super villa, mini villa, villa haut standing, villa meublée, villa duplex |
| terrain | land, plot, parcel, lot, ground, ter, terrain nu, terrain constructible, terrain à bâtir, terrain viabilisé, terrain mitoyen, land for sale, building plot, piece of land, land property, terrain agricole, terrain à usage commercial |
| local commercial | boutique, shop, magasin, commerce, store, local, commercial space, retail space, boutique commerce, space commercial, local à usage commercial |
| bureau | office, buro, espace de travail, workspace, cabinet, bureaux, office space, desk, espace bureau, bureau professionnel, cabinet professionnel |
| immeuble | building, apartment building, immeuble de rapport, income property, immeuble locatif, immeuble résidentiel, building complex, immeuble commercial, résidence |
| dépôt/entrepôt | warehouse, storage, magasin général, hangar, dépôt de marchandises, entrepôt de stockage, warehouse space, go down, godown |
| terrain constructible | buildable land, building plot, terrain à bâtir, terrain viabilisé, constructible plot |

### Property Type Normalisation (EN Variant → French ID) — 12 items

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

### District Alias Mappings (33 entries)

| Source District | Canonical District |
|----------------|-------------------|
| Bependa Omnisport | Bepanda Omnisports |
| Bonamoussadi Cité | Bonamoussadi |
| Bonamouti-Akwa 2 | Bonamouti |
| Centre Ville / Centre-ville | Centre |
| Messa Administratif / Messa Doumassi / Messa Ekoazon / Messa Plateau / Messa-Carrière | Messa |
| Nkomkana I, II | Nkomkana |
| Nsimeyong I, II | Nsimeyong |
| Nouvelle zone d'Akwa Nord | Akwa Nord |
| Nouvelle zone de New-Deido | New Deido |
| Small Soppo-Wonganga / Small Soppo-Woteke / Small Soppo-Wovila | Small Soppo |
| Lower Bolifamba | Bolifamba |
| Upper Muea | Muea |
| Lower Bokova | Bokova |
| Federal Quarters / Old-Government Station / Clerk's Quarter | Government Residential Area |
| Bonakeke Akwa | Akwa |
| New-Bell Bandjoun | New-Bell |

---

## 9. Internationalization Strategy

### 5 I18N/L10N Documents

| # | Document | Content |
|---|----------|---------|
| 1 | 30-I18N-L10N-REFERENCE.md | Master internationalization & localization reference |
| 2 | 30A-BUSINESS-DICTIONARY-REFERENCE.md | Official business dictionary |
| 3 | 30B-TRANSLATION-REFERENCE.md | Translation key & version management |
| 4 | 30C-LANGUAGE-DETECTION-REFERENCE.md | Language detection architecture |
| 5 | 30D-MULTILINGUAL-SEARCH-REFERENCE.md | Multilingual tolerant search |

### Core I18N Principles (from 30-I18N-L10N-REFERENCE)

1. **Language is a native context data** — Must never be hardcoded in a business component.
2. **All layers** must display, interpret, and log the same information in multiple languages without changing business logic.
3. **3 official languages:** French (default), English, Pidgin English.
4. **Adding a new language** must remain possible without modifying the business model.
5. **Fallback chain:** User's known language → French.

### Regional Format Requirements
Must handle:
- Dates, times, numbers, currencies
- Time zones, decimal separators
- Phone number formats, address formats
- Must be consistent with language and country

### Coverage Scope
Web, Mobile, APIs, Dashboards, LAWIM AI, Matching, Conversation, Notifications, Emails, SMS, Campay, Reporting, Documentation, Tests.

### Absolute Rules
**Must:**
- Centralize translation keys
- Avoid hardcoded text
- Log the effective language
- Allow dynamic switching
- Keep functional content consistency
- Remain compatible with continuous learning

**Must NOT:**
- Mix translation with business rules
- Depend on hardcoded text for business decisions
- Lose user's preferred language
- Break interface compatibility

### Translation Key Management (from 30B-TRANSLATION-REFERENCE)
1. Every displayable text must be attached to a stable key.
2. Each key must be: unique, versioned, traceable, reusable, independent of final rendering.
3. Each translation must preserve: source version, translated version, date, author, validation, history.
4. Sources: business reference, admin validator, LAWIM AI, human translator, controlled import/export.
5. LAWIM AI never publishes a translation without human validation if the text is critical.

### UI Translation Coverage
Key labels for login/account creation:
- Identifiant, Email/téléphone/nom d'utilisateur, Mot de passe, Connexion, Mot de passe oublié
- Créer un compte, Nom complet, Nom d'utilisateur, Numéro WhatsApp
- Confirmation du mot de passe, Langue préférée, J'accepte les conditions
- Footer: lawim.app, contact@lawim.app, WhatsApp, Facebook @lawimofficial

### Multilingual Search Pipeline (from 30D-MULTILINGUAL-SEARCH-REFERENCE)

1. Language detection
2. Normalization
3. Orthographic correction
4. Synonym expansion
5. Functional translation (if needed)
6. Phonetic search
7. Ranking
8. Restitution

**Core principle:** "The language serves expression. Meaning serves matching." — Same business results regardless of input language.

**Search must NOT:**
- Depend on the exact input language
- Ignore local expressions
- Block a search due to a common typo
- Produce different results for the same business concept

### Business Dictionary Structure (from 30A-BUSINESS-DICTIONARY-REFERENCE)
Each concept must contain:
- ID, category, French, English, Pidgin
- Synonyms, variants, local expressions, frequent typos
- Real estate category, semantic weight, confidence level

**Covered domains:** immobilier, vente, location, bail, chambre, studio, appartement, duplex, immeuble, terrain, terrain agricole, plantation, hôtel, commerce, bureau, local commercial, usine, entrepôt, parking, garage, villa, résidence, logement, copropriété, syndic, notaire, titre foncier, certificat, agence, agent, propriétaire, détenteur, mandataire, visite, offre, contre-offre, paiement, Campay, Mobile Money, Orange Money, MTN MoMo, boost, premium, matching, géolocalisation, IA.

**Marketing vocabulary** (26 concepts in FR/EN/Pidgin): Campaign, Publication, Tracking, Attribution, Lead, Conversion, Funnel, Click, Unique Click, Redirection, Acteur, Canal, Source, Session, QR Code, UTM, Landing Page, ROI, CTR, CPC, CPL, CPA, Engagement, Portée, Impression, Campay Conversion, Service Revenue, Campaign Cost, Sponsored/Organic Publication.

---

## 10. Business Dictionary

### Real Estate Vocabulary (30 terms)

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

### Pricing Expressions

| Category | Examples | Range |
|----------|----------|-------|
| Thousands (50k–500k) | 150k, 300k/month, 100k par mois | 50,000–500,000 FCFA |
| Millions (1M–100M) | 5M, 10M, 20M, 50M, 100M, 200M | 1,000,000–200,000,000 FCFA |
| Full FCFA format | 8 000 000 FCFA, 12 millions FCFA | Variable |
| Range format | 10–15M, 20–30 millions | Variable ranges |

**Currency variants:** FCFA, Franc CFA, XAF (ISO code)
**Abbreviations:** M (million), k (thousand)

### Price Modifiers (Negotiation)

| Term | Meaning |
|------|---------|
| prix ferme | fixed price (non-negotiable) |
| prix négociable | negotiable |
| à débattre | negotiable |
| dernier prix | final price |
| on peut s'entendre | we can agree |
| combien dernier ? | what's the final price? |
| pas de commission | no commission |
| caution 1 mois | 1 month deposit |
| 2 mois caution | 2 months deposit |
| avance 6 mois | 6 months advance |

### Budget Types by Intent

| Intent | Budget Type |
|--------|------------|
| buy | global_price |
| rent | monthly_rent |
| land | global_price_or_per_sqm |
| commercial | monthly_rent_and_entry_fee |

### Cameroon-Specific Expressions

**Social validation phrases (5):**
- Mon grand frère doit voir
- Mon cousin va vérifier
- Mon oncle est sur place
- Ma femme doit valider
- Mon mari doit regarder

**Market-specific vocabulary:**
- **Title:** titre foncier, titre, papier, document, notaire, proprio direct, terrain titré
- **Measurement:** m², mètre carré, hectare, are
- **Construction:** parpaing, dur, semi-dur, en tôle, poto-poto
- **Negotiation:** dernier prix, prix négociable, à débattre, on peut s'entendre, combien dernier ?
- **Accessibility:** bordure de route, route goudronnée, piste, motopiste, véhicule
- **Services:** forage, groupe électrogène, climatisation, parking, gardien, caméra

---

## 11. Translation Rules

### Official Translation Policy (Directive 30B)

1. **Centralized keys:** Every displayable string must have a stable key.
2. **No hardcoded text:** All user-facing text must go through the translation system.
3. **Fallback:** Apply the fallback defined by the i18n/l10n reference (French → English → Pidgin).
4. **Versioning:** Each translation must be versioned with source, date, author, validation, history.
5. **Sources:** Business reference, admin validator, LAWIM AI, human translator, controlled import/export.
6. **Critical text:** LAWIM AI never publishes critical translations without human validation.
7. **UI consistency:** A correctly translated interface must NOT mix languages within the same screen (except for brand elements or validated official references).
8. **Language choice persistence:** Must be preserved across all interfaces after reconnection.

### Response Messages
8 templates are available in FR/EN/PID (see Section 3).

### Property Display Format (all languages)
`N. *description*\n📍 localisation\n💰 prix\n⭐ notes`

---

## 12. Camfranglais/Pidgin Handling

### Pidgin Cameroon
- **Support level:** Partial (14 keyword detection, limited templates)
- **Detection keywords:** how far, wahala, chap, gbedu, comot, dey, sabi, small, plenty, chop, wetin, na, abeg
- **Templates available:** 8 templates (welcome, help, no_match, thanks, ask_name, ask_phone, stats, language_changed)
- **Expression corpus:** 11+ expressions across buy/rent/sell/invest intents
- **NOT a replacement for English or French** — pidgin is supplementary

### Camfranglais
- **Status:** NOT a supported language — explicitly excluded from the 3-language model
- **Usage:** Present only in the WhatsApp expression corpus as Camfranglais example expressions
- **Expressions captured:** 7 expressions across buy/sell/rent intents
- **Examples:** "je need un terrain", "je cherche un land", "je want acheter terrain"
- **Rule:** Camfranglais expressions enrich the language corpus but do NOT constitute a 4th supported language

### Language Switch Rule
- Language switching does NOT require restarting the conversation.
- Switch available via `LANGUE` command.
- Persisted per user across sessions.

---

## 13. All Business Rules for Language

### From RULE_INDEX.md — Language Domain (Rules LANG-001 to LANG-014)

| Rule ID | Description | Source | Confidence |
|---------|-------------|--------|------------|
| LANG-001 | Default language: French | language_handler.py | VALIDATED |
| LANG-002 | Detection hierarchy: DeepSeek → Gemini (commented out) → Local rules | language_detector_ia.py | VALIDATED |
| LANG-003 | LANGUE command with persistence | language_handler.py | VALIDATED |
| LANG-004 | 8 multilingual templates (FR/EN/PID): welcome, help, no_match, thanks, ask_name, ask_phone, stats, language_changed | multilingual_responses.py | VALIDATED |
| LANG-005 | 33 entity_linking entries with relation types: equivalent_to, synonym, related_to, typo_of, abbreviation_of | entity_linking.json | VALIDATED |
| LANG-006 | 5 typo databases: cities, neighborhoods, property_types, whatsapp, general | typo_database/*.json | VALIDATED |
| LANG-007 | 7 whatsapp_language files: whatsapp, diaspora, investor, negotiation, listing, search, urgency | whatsapp_language/*.json | VALIDATED |
| LANG-008 | 5 i18n documents: 30-I18N-L10N-REFERENCE, 30A-30D | Directive/30*.md | VALIDATED |
| LANG-009 | 38 country codes in phone_formatter | phone_formatter.py | VALIDATED |
| LANG-010 | Cameroon format: 237 + 9 digits | phone_formatter.py | VALIDATED |
| LANG-011 | WhatsApp link: https://wa.me/{normalized} | phone_formatter.py | VALIDATED |
| LANG-012 | 12 pidgin words in language_detector.py, 14 in language_detector_ia.py | language_detector.py | PARTIAL |
| LANG-013 | 18 French keyword max (not 20) | language_detector_ia.py | NON_VALIDE |
| LANG-014 | 18 English keyword max (not 20) | language_detector_ia.py | NON_VALIDE |

### Business Rules from LANGUAGE_MODEL.md (Validated)

| # | Rule | Source |
|---|------|--------|
| 1 | 3 supported languages: FR (full), EN (full), PID (partial) | LANGUAGE_MODEL.md |
| 2 | Camfranglais is NOT a 4th language | LANGUAGE_MODEL.md |
| 3 | Language persistence per user across sessions | LANGUAGE_MODEL.md |
| 4 | Manual language switch via LANGUE command (no restart) | LANGUAGE_MODEL.md |
| 5 | 18 French keywords for detection | LANGUAGE_MODEL.md |
| 6 | 18 English keywords for detection | LANGUAGE_MODEL.md |
| 7 | 14 Pidgin keywords for detection | LANGUAGE_MODEL.md |
| 8 | 8 multilingual response templates | LANGUAGE_MODEL.md |
| 9 | 20 entity linked pairs (documented) | entity_linking.json |
| 10 | 17 search alias mappings (EN→FR) | search_aliases.json |
| 11 | 12 property type normalisation IDs | property_types.py |
| 12 | 5 typo databases with aggregated master | typo_database.json |
| 13 | 10 city typo mappings with variants | cities_typo.json |
| 14 | 6 neighborhood typo mappings | neighborhoods_typo.json |
| 15 | 9 property type typo mappings | property_types_typo.json |
| 16 | 30 real estate vocabulary terms | real_estate_vocabulary.json |
| 17 | 9 diaspora language patterns | diaspora_language.json |
| 18 | 8 investor language patterns | investor_language.json |
| 19 | 8 negotiation terms | negotiation.json |
| 20 | 17 property listing/search expressions | property_listing/search.json |
| 21 | 8 urgency signals | urgency_signals.json |
| 22 | Currency: FCFA, Franc CFA, XAF | LANGUAGE_MODEL.md |
| 23 | Pricing abbreviations: M (million), k (thousand) | LANGUAGE_MODEL.md |
| 24 | 10 negotiation terms (price modifiers) | LANGUAGE_MODEL.md |
| 25 | French default language | LANGUAGE_MODEL.md |
| 26 | 10 city abbreviations (YDE→Yaoundé, DLA→Douala, etc.) | abbreviations.json |
| 27 | 11 real estate abbreviations (M, k, FCFA, T.F., etc.) | abbreviations.json |
| 28 | 8 social abbreviations (m2, ha, chbres, appt, etc.) | abbreviations.json |
| 29 | 6 price amount patterns (5M, 10M, 20M, 50M, 100M, 200M) | amount_expressions.json |
| 30 | 4 budget types by intent | amount_expressions.json |
| 31 | 5 social validation phrases (Cameroon-specific) | cameroon_expressions.json |
| 32 | 6 market-specific vocabulary categories | cameroon_expressions.json |
| 33 | Language switch without conversation restart | cameroon_expressions.json |
| 34 | 5 intent indicators with primary/secondary keywords | intent_phrases.json |
| 35 | 6 pattern matching rules (search_buy, rent, sell, investor, diaspora) | intent_phrases.json |
| 36 | District hierarchy: Country → Region → Dept → District → Commune → City → District → Neighborhood | aliases.json |
| 37 | 33 district alias mappings | aliases.json |
| 38 | 11 property type alias groups (comprehensive) | property_type_aliases.json |
| 39 | 18 typo mappings for property types | property_type_aliases.json |

### Business Rules from RULE_INDEX.md — Additional Language Context

| Rule ID | Applied Domain | Rule Description |
|---------|---------------|------------------|
| CONV-003 | Conversation | 3 supported languages: FR, EN, PID (not 4) |
| CONV-019 | Conversation | 8 multilingual templates in FR/EN/PID |
| QUAL-016 | Qualification | 13 diaspora locations + 4 phone indicators |
| QUAL-001 | Qualification | Score boosts: diaspora_detected=+25 |
| NEGO-008 | Negotiation | Price expressions in negotiation.json |

---

## 14. Source References

### Primary Sources (Read in full)

| # | Source | Path | Read Status | Confidence |
|---|--------|------|------------|------------|
| 1 | LANGUAGE_MODEL.md | docs/lawim_heritage_gold/LANGUAGE_MODEL.md | Full (378 lines) | **HIGH** |
| 2 | RULE_INDEX.md (Language section) | docs/lawim_heritage_gold/RULE_INDEX.md | Full (lines 186–204) | **HIGH** |
| 3 | KNOWLEDGE_GLOSSARY.md | docs/lawim_heritage_gold/KNOWLEDGE_GLOSSARY.md | Full (271 lines) | **HIGH** |
| 4 | 30-I18N-L10N-REFERENCE.md | `git show backup:docs/Directive/30-I18N-L10N-REFERENCE.md` | Full (9 chapters) | **HIGH** |
| 5 | 30A-BUSINESS-DICTIONARY-REFERENCE.md | `git show backup:docs/Directive/30A-BUSINESS-DICTIONARY-REFERENCE.md` | Full (7 chapters + marketing vocabulary) | **HIGH** |
| 6 | 30B-TRANSLATION-REFERENCE.md | `git show backup:docs/Directive/30B-TRANSLATION-REFERENCE.md` | Full (8 chapters) | **HIGH** |
| 7 | 30C-LANGUAGE-DETECTION-REFERENCE.md | `git show backup:docs/Directive/30C-LANGUAGE-DETECTION-REFERENCE.md` | Full (6 chapters) | **HIGH** |
| 8 | 30D-MULTILINGUAL-SEARCH-REFERENCE.md | `git show backup:docs/Directive/30D-MULTILINGUAL-SEARCH-REFERENCE.md` | Full (6 chapters) | **HIGH** |

### Knowledge Unified Language Files (6 files)

| # | File | Path | Confidence |
|---|------|------|------------|
| 1 | abbreviations.json | knowledge_unified/language/abbreviations.json | **HIGH** |
| 2 | amount_expressions.json | knowledge_unified/language/amount_expressions.json | **HIGH** |
| 3 | cameroon_expressions.json | knowledge_unified/language/cameroon_expressions.json | **HIGH** |
| 4 | common_expressions.json | knowledge_unified/language/common_expressions.json | **HIGH** |
| 5 | intent_phrases.json | knowledge_unified/language/intent_phrases.json | **HIGH** |
| 6 | spelling_variants.json | knowledge_unified/language/spelling_variants.json | **HIGH** |

### Supporting Files

| # | File | Path | Confidence |
|---|------|------|------------|
| 1 | property_type_aliases.json | knowledge_unified/real_estate/property_type_aliases.json | **HIGH** |
| 2 | aliases.json (geography) | knowledge_unified/geography/aliases.json | **HIGH** |
| 3 | intentions.json (keywords) | knowledge_unified/qualification/intentions.json | **HIGH** |
| 4 | SOURCE_INVENTORY.md | knowledge_unified/sources/SOURCE_INVENTORY.md | **HIGH** |
| 5 | TRACEABILITY_MATRIX.md | knowledge_unified/sources/TRACEABILITY_MATRIX.md | **HIGH** |
| 6 | quality_report.md | knowledge_unified/validation/quality_report.md | **HIGH** |
| 7 | conflicts.md | knowledge_unified/validation/conflicts.md | **MEDIUM** |

### Heritage-Only Content (NO longer in repository — extracted from git history or heritage gold)

| # | Content | Preserved In | Original Legacy Path | Confidence |
|---|---------|-------------|---------------------|------------|
| 1 | entity_linking.json (20 pairs) | LANGUAGE_MODEL.md §5 | KNOWLEDGE/_archive/entity_linking_v1.json | **MEDIUM** |
| 2 | search_aliases.json (17 items) | LANGUAGE_MODEL.md §6 | KNOWLEDGE/search_aliases/search_aliases.json | **HIGH** |
| 3 | typo_database.json (49 entries) | LANGUAGE_MODEL.md §8 + spelling_variants.json | KNOWLEDGE/typo_database/typo_database.json | **HIGH** |
| 4 | cities_typo.json (10 cities) | spelling_variants.json | KNOWLEDGE/typo_database/cities_typo.json | **HIGH** |
| 5 | neighborhoods_typo.json (6 neighborhoods) | spelling_variants.json | KNOWLEDGE/typo_database/neighborhoods_typo.json | **HIGH** |
| 6 | property_types_typo.json (9 types) | spelling_variants.json | KNOWLEDGE/typo_database/property_types_typo.json | **HIGH** |
| 7 | whatsapp_typo.json | abbreviations.json (WhatsApp-specific) | KNOWLEDGE/typo_database/whatsapp_typo.json | **MEDIUM** |
| 8 | whatsapp_language.json (697 lines) | common_expressions.json | KNOWLEDGE/whatsapp_language/whatsapp_language.json | **HIGH** |
| 9 | diaspora_language.json (9 items) | common_expressions.json (diaspora) | KNOWLEDGE/whatsapp_language/diaspora_language.json | **HIGH** |
| 10 | investor_language.json (8 items) | common_expressions.json (invest) | KNOWLEDGE/whatsapp_language/investor_language.json | **HIGH** |
| 11 | negotiation.json (8 items) | common_expressions.json (negotiate) | KNOWLEDGE/whatsapp_language/negotiation.json | **HIGH** |
| 12 | property_listing.json | common_expressions.json | KNOWLEDGE/whatsapp_language/property_listing.json | **HIGH** |
| 13 | property_search.json | common_expressions.json + intent_phrases.json | KNOWLEDGE/whatsapp_language/property_search.json | **HIGH** |
| 14 | urgency_signals.json (8 items) | common_expressions.json (urgency_signals) | KNOWLEDGE/whatsapp_language/urgency_signals.json | **HIGH** |
| 15 | real_estate_vocabulary.json (30 terms) | LANGUAGE_MODEL.md §10 | KNOWLEDGE/vocabulary/real_estate_vocabulary.json | **HIGH** |
| 16 | phone_formatter.py | RULE_INDEX.md LANG-009/010/011 | code/ (current V2) | **HIGH** |
| 17 | property_types.py | LANGUAGE_MODEL.md §7 | code/ (current V2) | **MEDIUM** |

### Confidence Legend
- **HIGH:** Content confirmed from primary heritage gold document OR verified across multiple independent sources.
- **MEDIUM:** Content extracted from secondary source or backup only; not independently verified in current codebase.
- **LOW:** Content mentioned in one source only, or with noted conflicts/discrepancies.

---

*Document generated 15 July 2026 — Language Historian, LAWIM Heritage Completion Mission H0.4*
*Total extracted: 14 data categories, 34 JSON files referenced, 8 primary sources read, 6 knowledge_unified files analyzed, 14 heritage-only files documented.*
