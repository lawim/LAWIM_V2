# DATASETS — LAWIM Heritage Gold

## 1. Geography Datasets

### Master Geography

| File | Size | Description |
|------|------|-------------|
| `cameroon_geography.json` | 6170 lines | Master geography — all cities, neighborhoods, GPS coordinates, hierarchies |
| `cameroon_geography_v2_backup.json` | ~2500 lines | v2 backup (pre-mass-GPS) |

### Neighborhood Inventory

| File | Size | Description |
|------|------|-------------|
| `neighborhood_inventory_final.json` | ~1200 lines | 382 neighborhoods across 10 cities (canonical) |
| `neighborhood_inventory.json` | raw | Raw neighborhood list |
| `neighborhood_inventory_clean.json` | cleaned | Cleaned version |

### Neighborhood Count by City

| City | Neighborhoods |
|------|-------------|
| Yaoundé | 111 |
| Douala | 104 |
| Buea | 51 |
| Limbe | 41 |
| Bafoussam | 33 |
| Maroua | 15 |
| Kribi | 12 |
| Bamenda | 10 |
| Garoua | 6 |
| Nkongsamba | 3 |
| **Total** | **382** |

### District Aliases & Hierarchy

| File | Entries | Description |
|------|---------|-------------|
| `district_aliases.json` | 14 entries | District alias mappings (v1+v2+v3 merged) |
| `district_hierarchy.json` | 4 entries | Parent-child district relationships (Buea only) |

### District Hierarchy (Buea)

| Parent District | Child Districts |
|-----------------|----------------|
| Muea | Lower Muea, Upper Muea |
| Great Soppo | Small Soppo-Wonganga, Small Soppo-Woteke, Small Soppo-Wovila |
| Government Residential Area | Federal Quarters, Clerk's Quarter, Old-Government Station |
| Bolifamba | Lower Bolifamba |

### GPS Datasets

| File | Description |
|------|-------------|
| `neighborhood_gps.json` | Neighborhood GPS coordinates |
| `gemini_recovered_gps.json` | GPS data recovered via Gemini AI |

### City-Specific Neighborhood Files (10 JSON files)

| File | City |
|------|------|
| `douala.json` | Douala |
| `yaounde.json` | Yaoundé |
| `bafoussam.json` | Bafoussam |
| `bamenda.json` | Bamenda |
| `buea.json` | Buea |
| `garoua.json` | Garoua |
| `kribi.json` | Kribi |
| `limbe.json` | Limbe |
| `maroua.json` | Maroua |
| `nkongsamba.json` | Nkongsamba |

### Aggregated Neighborhood File

| File | Description |
|------|-------------|
| `all_neighborhoods.json` | Single file aggregating all 10 city neighborhood lists |

### Secondary Cities (18)

Ebolowa, Mbalmayo, Ngaoundéré, Dschang, Foumban, Mbouda, Bertoua, Kumba, Edéa, Meiganga, Batouri, Ambam, Kousseri, Mora, Kaélé, Guider, Tiko, Mutengene

## 2. Intent Datasets (5 files)

Source directory: `KNOWLEDGE/intents/`

| File | Description | Key Content |
|------|-------------|-------------|
| `buy_property.json` | Buy intent keywords, expressions, qualification fields | Keywords FR/EN, budget_type: global_price |
| `rent_property.json` | Rent intent keywords, duration, budget patterns | Keywords FR/EN, budget_type: monthly_rent |
| `sell_property.json` | Sell intent, document requirements | Keywords FR/EN/PID, asking_price |
| `search_property.json` | General search intent, confidence threshold 0.7 | Generic search before full qualification |
| `investor_intent.json` | Investor intent with diaspora info, P0 priority | ROI, diaspora countries, investment types, capital signals |

All 5 intents merged into `qualification/intentions.json`.

## 3. Language Datasets

### WhatsApp Language Corpus

| File | Lines | Description |
|------|-------|-------------|
| `whatsapp_language.json` | 697 lines | Full multilingual corpus across FR/EN/PID/Camfranglais for all intents |

### Language Pattern Files (6 files)

| File | Description |
|------|-------------|
| `diaspora_language.json` | Diaspora-specific language patterns (9 items) |
| `investor_language.json` | Investor language patterns (8 items) |
| `negotiation.json` | Negotiation expressions and terms (8 items) |
| `property_listing.json` | Property listing language (17 items) |
| `property_search.json` | Property search language |
| `urgency_signals.json` | Urgency signal keywords and weights (8 items) |

## 4. Typo Datasets (5 files)

| File | Lines | Description |
|------|-------|-------------|
| `typo_database.json` | 346 lines | Master typo database (49 canonical entries, 3–6 variants each) |
| `cities_typo.json` | — | City-specific typo mappings (10 cities) |
| `neighborhoods_typo.json` | — | Neighborhood typo mappings (11 neighborhoods) |
| `property_types_typo.json` | — | Property type typo mappings (8 types) |
| `whatsapp_typo.json` | — | WhatsApp-specific spelling variants |

All typo sources merged into `language/spelling_variants.json`.

## 5. Search Datasets

| File | Lines | Description |
|------|-------|-------------|
| `search_aliases.json` | 99 lines | Search alias mappings (17 property type aliases EN→FR) |
| `search_optimization.json` | 37 lines | Search engine optimisation parameters |

## 6. CRM Datasets

| File | Description |
|------|-------------|
| `crm_schema.json` | CRM data schema (v1, archived) |
| `lead_scoring.json` | Lead scoring configuration |
| `lead_scoring_rules.json` | Lead scoring weight rules (from KNOWLEDGE/scoring/) |

### CRM Data Backups (CSV)

| File | Description |
|------|-------------|
| `agents.csv` | Agent records |
| `leads.csv` | Lead records |
| `properties.csv` | Property records |
| `persons.csv` | Person/contact records |
| `events.csv` | Event/tracking records |
| `users.csv` | User accounts |

## 7. Property Datasets

| File | Lines | Description |
|------|-------|-------------|
| `property_types.json` | 21 lines | Base property type taxonomy (12 types) |
| `property_taxonomy.json` | — | Property taxonomy v1 |
| `property_taxonomy_v2.json` | — | Property taxonomy v2 with furnished criteria |
| `title_status.json` | — | Title/document status options |

### Property Categories (from property_types.json)

| Category | Types |
|----------|-------|
| Residential | APT, STU, CHB, CHB_MEUBLEE, MSN, VIL |
| Land | TER, TER_CONST |
| Commercial | COM, BUR, IMM, DEP |

## 8. Pricing Datasets

| File | Lines | Description |
|------|-------|-------------|
| `pricing.json` | 45 lines | General pricing data |
| `pricing_expressions.json` | — | Price expression patterns (13 amount patterns + price modifiers + budget types) |

### Price Modifiers

| Expression | Meaning |
|------------|---------|
| prix ferme | fixed price |
| prix négociable | negotiable |
| à débattre | negotiable |
| dernier prix | final price |
| pas de commission | commission free |
| caution 1 mois | 1 month deposit |
| 2 mois caution | 2 months deposit |
| avance 6 mois | 6 months advance |

## 9. Role Datasets

| File | Lines | Description |
|------|-------|-------------|
| `user_roles.json` | 63 lines | Role definitions and permissions |
| `roles-matrix.md` | — | Roles matrix documentation with coverage |

### Roles (from user_roles.json)

| Role | Permissions |
|------|-------------|
| VISITOR | Browse, search |
| USER | Request creation, profile management |
| BUYER | Full buy flow |
| RENTER | Full rent flow |
| OWNER | Property listing, management |
| INTRODUCER | Lead introduction, commission |
| AGENT | Assignment, follow-up, performance |
| MANAGER | Queue management, triage, review |
| VICE_MANAGER | KPIs, exceptions, audit |
| ADMIN | Users, permissions, system health, roles |

## 10. Entity Linking

| File | Lines | Description |
|------|-------|-------------|
| `entity_linking.json` | 167 lines | 20 entity pairs linking real estate terms (terrain↔parcelle, villa↔maison de luxe, etc.) |

## 11. Investor Datasets

| File | Description |
|------|-------------|
| `investor_signals.json` | Investor signal patterns and weights |
| `investors.json` | Investor records and profiles |

### Investor Qualifiers

- **Required fields:** expected_return, budget, city, risk_tolerance
- **Optional fields:** strategy, timeline, diaspora_country, exit_strategy, property_type
- **Diaspora countries:** France, Canada, Belgique, USA, Allemagne, Italie, Royaume-Uni
- **Investment types:** land banking, rental property, commercial property, development project, student housing, airbnb
- **Capital signals:** 10M, 20M, 50M, 100M, 200M, 500M

## 12. Geography Scripts

| Script | Purpose |
|--------|---------|
| `generate_neighborhood_gps.js` | Generate GPS coordinates for neighborhoods |
| `generate_city_gps.js` | Generate GPS coordinates for cities |
| `build_cameroon_geography.js` | Build the master cameroon_geography.json from all sources |

## 13. AI Model Configs

| File | Description |
|------|-------------|
| `lead_classifier_v1.json` | Lead classification model (intent→role mapping) |
| `property_matching_v1.json` | Property matching algorithm configuration |
| `reasoning_rules_v1.json` | AI reasoning rules for conversation |
| `conversation_flows_v1.json` | Intent-based conversation flow definitions |
| `memory_rules_v1.json` | Memory persistence and context rules |

## 14. Rule Engines

| File | Description |
|------|-------------|
| `RULE_ENGINE_V2.json` | Rule engine v2 |
| `RULE_ENGINE_V3.json` | Rule engine v3 |
| `RULE_ENGINE_V4.json` | Rule engine v4 |
| `RULE_ENGINE_V5.json` | Rule engine v5 (latest) — includes multi-intent detection |
| `FEATURE_FLAGS.json` | Feature flag configuration |
| `USER_STATES.json` | User state machine definitions |
| `EVENT_TYPES.json` | Event type taxonomy for tracking |

## 15. Knowledge Files Comparison

### Source Files (KNOWLEDGE/)

| Category | Count |
|----------|-------|
| Top-level Markdown/JSON | 26 |
| geography/ | 11 |
| cities/ | 2 |
| intents/ | 5 |
| neighborhoods/ | 11 |
| whatsapp_language/ | 7 |
| typo_database/ | 5 |
| master/ (architecture docs) | 15 |
| REFERENCE/ | 11 |
| _archive/ (v1 snapshots) | 27 |
| _repair_backup/ | ~60 |
| Other directories | ~25 |
| LAWIM root sources | ~15 |
| **Total inventoried** | **~220 files** |

### Target Files (knowledge_unified/)

| Domain | Files |
|--------|-------|
| geography/ | 5 (cities.json, neighborhoods.json, aliases.json, proximity_rules.json, geographic_scoring.md) |
| matching/ | 6 (dimensions, scoring, exclusion, ranking, weights, explanations) |
| qualification/ | 8 (typologies, intentions, matrices ×5, rules) |
| language/ | 6 (expressions, cameroon, variants, abbreviations, amounts, phrases) |
| commercial/ | 5 (negotiation, objections, follow-up, closing, tone) |
| professionals/ | 4 (partner fields, categories, qualification, relationships) |
| legal_and_documents/ | 3 (disclaimer, document categories, legal index) |
| real_estate/ | 5 (amenities, constraints, property type aliases, property types, transaction types) |
| sources/ | 2 (inventory, traceability matrix) |
| validation/ | 4 (conflicts, quality, unresolved, validation report) |
| schemas/ | 0 (empty) |
| **Total** | **50 files** |

## 16. Validation Status

- **Status:** PASSED
- **Total files:** 50
- **Errors:** 0
- **Warnings:** 15 (code pattern 'type' occurrences in JSON/MD files)
- **Missing files:** 0
