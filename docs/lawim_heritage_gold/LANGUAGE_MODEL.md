# LANGUAGE MODEL — LAWIM Heritage Gold

## 1. Supported Languages

| Language | Support Level | Code |
|----------|--------------|------|
| French | Full | FR |
| English | Full | EN |
| Pidgin Cameroon | Partial | PID |

## 2. Language Detection Pipeline

| Priority | Method | Status |
|----------|--------|--------|
| 1st | DeepSeek AI classification | Implemented |
| 2nd | Gemini AI classification | Not implemented |
| 3rd | Local keyword-based rules | Implemented (fallback) |

- Language persistence is maintained per user (detected language is stored and reused across sessions).
- Language can be manually switched via the `LANGUE` command.
- Language switching does not require restarting the conversation.

## 3. Language Detection Keywords

### French Detection (18 words)

| # | Word |
|---|------|
| 1 | bonjour |
| 2 | salut |
| 3 | appartement |
| 4 | maison |
| 5 | terrain |
| 6 | location |
| 7 | achat |
| 8 | vente |
| 9 | prix |
| 10 | budget |
| 11 | urgent |
| 12 | merci |
| 13 | je |
| 14 | tu |
| 15 | il |
| 16 | elle |
| 17 | nous |
| 18 | vous |

### English Detection (18 words)

| # | Word |
|---|------|
| 1 | hello |
| 2 | hi |
| 3 | apartment |
| 4 | house |
| 5 | land |
| 6 | rent |
| 7 | buy |
| 8 | sale |
| 9 | price |
| 10 | budget |
| 11 | urgent |
| 12 | thanks |
| 13 | i |
| 14 | you |
| 15 | he |
| 16 | she |
| 17 | we |
| 18 | they |

### Pidgin Cameroon Detection (14 keywords)

| # | Keyword |
|---|---------|
| 1 | how far |
| 2 | wahala |
| 3 | chap |
| 4 | gbedu |
| 5 | comot |
| 6 | dey |
| 7 | sabi |
| 8 | small |
| 9 | plenty |
| 10 | chop |
| 11 | wetin |
| 12 | na |
| 13 | abeg |

## 4. Multilingual Response Templates

Templates are defined in FR, EN, and PID for the following intents/contexts:

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

## 5. Entity Linking

Source: `entity_linking.json` (167 lines) — 20 linked entity pairs:

| Source Entity | Linked Entity |
|---------------|---------------|
| terrain | parcelle |
| villa | maison de luxe |
| appartement | appart |
| commerce | boutique |
| bureau | office |
| immeuble | building |
| studio | one-room |
| entrepôt | warehouse |
| climatisation | AC |
| parking | stationnement |
| piscine | swimming pool |
| gardien | security |
| meublé | furnished |
| non meublé | unfurnished |
| titre foncier | land title |
| notaire | lawyer |
| bail | lease |
| caution | deposit |
| agence | agency |
| commission | fee |

## 6. Search Aliases (17 items)

Source: `search_aliases.json` — Property type normalisation mappings EN→FR:

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

## 7. Property Type Normalisation (EN→FR)

Consolidated from `property_types.py` and `search_aliases.json`:

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

## 8. Typo Database

### Cities (10 cities, 4–7 variants each)

| City | Variants |
|------|----------|
| Yaoundé | yaound, yaoundee, yaoundeee, yaounde1, yaonde, yaond, yaoundéé, yaounder, yyaounde |
| Douala | doula, doualaa, doual, doulala, ddouala, doulla, doualaa237 |
| Bamenda | bamnda, bameda, bamendah, bamender |
| Bafoussam | bafousam, bafossam, bafoussamm, bafousan |
| Buea | bueaa, bua, bueah, bue |
| Kribi | kriby, kribbi, kribie, kiribi |
| Nkongsamba | nkonsamba, nkongsmba, nkongsambaa |
| Maroua | maroa, marouah, marouaa |
| Limbe | limbee, limbéé, limbeh, limbae |
| Garoua | garoa, garouah, garouaa |

### Neighborhoods (11 neighborhoods with variants)

| Neighborhood | Variants |
|-------------|----------|
| Odza | odza3, odzaa, odza_, odaz |
| Makepe | makepe3, makepea, makepe_, makep, makpe |
| Bonapriso | bonapriso3, bonaprisoo, bonapriso_, bonapreso |
| Akwa | akwa3, akwa_, akwaa, akw |
| Bastos | bastos3, bastosa, bastos_, basto |
| Mendong | mendong3, mendonga, mendong_, mendng |

### Property Types (8 types with variants)

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

### Aggregated Typo Database (49 entries, 3–6 variants each)

Source: `typo_database.json` (346 lines) — Aggregated from all typo sources including city, neighborhood, property type, and WhatsApp-specific typos. Each canonical form maps to 3–6 common misspellings.

## 9. Pricing Expressions

| Category | Examples | Range |
|----------|----------|-------|
| Thousands (50k–500k) | 150k, 300k/month, 100k par mois | 50,000–500,000 FCFA |
| Millions (1M–100M) | 5M, 10M, 20M, 50M, 100M, 200M | 1,000,000–200,000,000 FCFA |
| Full FCFA format | 8 000 000 FCFA, 12 millions FCFA | Variable |
| Range format | 10–15M, 20–30 millions | Variable ranges |

### Currency Variants
- FCFA, Franc CFA, XAF (ISO code)
- Abbreviations: M (million), k (thousand)

### Negotiation Terms
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

## 10. Real Estate Vocabulary (30 terms)

Source: `real_estate_vocabulary.json`

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

## 11. WhatsApp Language Corpus

Source: `whatsapp_language.json` (697 lines) — Full multilingual corpus across FR/EN/PID/Camfranglais for all intents:

| Intent | FR Example | EN Example | PID Example | Camfranglais Example |
|--------|-----------|-----------|-------------|----------------------|
| Buy | je veux acheter un terrain | i want to buy land | i wan buy house | je need un terrain |
| Rent | je cherche appartement à louer | looking for apartment | i wan rent house | je cherche appartement |
| Sell | je vends une maison | house for sale | i di sell house | terrain à vendre |
| Invest | je veux investir dans l'immobilier | real estate investment | i wan invest | jai budget 10M pour land |
| Search | je cherche une maison | looking for property | i di find land | je cherche un land |
| Negotiate | dernier prix ? | best price? | price fine? | prix ngociable ? |

## 12. Diaspora Language Patterns (9 items)

Source: `diaspora_language.json`

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

## 13. Investor Language Patterns (8 items)

Source: `investor_language.json`

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

## 14. Negotiation Terms (8 items)

Source: `negotiation.json`

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

## 15. Property Listing/Search Language (17 items)

Source: `property_listing.json`, `property_search.json`

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

## 16. Urgency Signals (8 items)

Source: `urgency_signals.json`

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
