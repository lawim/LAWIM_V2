# LAWIM Legacy Knowledge Source Inventory

## Inventory Date: 2026-07-15
## Source Root: /media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/KNOWLEDGE/

## Directory Structure

### Top-Level Files (KNOWLEDGE/)
| File | Size | Type | Description |
|------|------|------|-------------|
| bootstrap-access.md | 2.9KB | Markdown | Bootstrap access rules |
| channel-tone-guidelines.md | 970B | Markdown | Channel-specific tone rules |
| city-affinity-matrix.md | 1.3KB | Markdown | City affinity relationships |
| conversation-humanization-rules.md | 7.6KB | Markdown | Humanization rules for Cameroon market |
| conversation-patterns.md | 9.0KB | Markdown | Core conversation patterns by intent |
| conversation-qualification-questions.md | 6.4KB | Markdown | Qualification question bank |
| conversation-style-guide.md | 2.0KB | Markdown | Conversation style guide |
| diaspora-behavior-model.md | 4.8KB | Markdown | Diaspora behavior patterns |
| facebook-page-profile.md | 5.5KB | Markdown | Facebook page profile |
| fraud-signals-and-verification.md | 6.0KB | Markdown | Fraud detection rules |
| immobilier_cameroun.json | 1.4KB | JSON | Cameroon real estate data |
| LAWIM_MASTER_DATASET.json | 250KB | JSON | Master dataset |
| location-segmentation-canonical.md | 5.1KB | Markdown | Location segmentation rules |
| location-segmentation-discovery.md | 7.8KB | Markdown | Location segmentation discovery |
| market-research-real-estate-cameroon.md | 8.8KB | Markdown | Cameroon market research |
| minimum-fields-property.md | 6.7KB | Markdown | Minimum fields for property |
| minimum-fields-request.md | 6.8KB | Markdown | Minimum fields for request |
| multilingual-conversation-guidelines.md | 1.5KB | Markdown | Multilingual conversation rules |
| negotiation-patterns.md | 4.8KB | Markdown | Negotiation behavior patterns |
| omnichannel-playbook.md | 7.1KB | Markdown | Omnichannel strategy |
| property-qualification-reference.md | 5.3KB | Markdown | Property qualification reference |
| qualification-implementation-backlog.md | 14.3KB | Markdown | Qualification implementation backlog |
| response-policy.md | 2.0KB | Markdown | Response policy rules |
| roles-matrix.md | 4.2KB | Markdown | Roles matrix and coverage |
| runtime-gap-remediation-plan.md | 9.5KB | Markdown | Runtime gap remediation |
| telegram-runtime.md | 2.2KB | Markdown | Telegram runtime rules |
| trust-and-objection-patterns.md | 7.5KB | Markdown | Trust and objection patterns |

### channels/
| File | Description |
|------|-------------|
| whatsapp-telegram-dashboard-qualification.md | Channel-specific qualification |

### cities/
| File | Description |
|------|-------------|
| cameroon_cities.json | Priority/secondary cities with aliases |
| cameroon_geography_before_mass_gps_20260610_084253.json | Historical GPS data (158KB) |

### geography/
| File | Description |
|------|-------------|
| cameroon_geography.json | Master geography v2.0 (162KB) |
| cameroon_geography_v2_backup.json | Geography v2 backup (98KB) |
| district_aliases.json | District alias mappings v1 |
| district_aliases_v2.json | District alias mappings v2 |
| district_aliases_v3.json | District alias mappings v3 |
| district_hierarchy.json | District parent-child relationships |
| gemini_recovered_gps.json | Gemini-recovered GPS data |
| neighborhood_gps.json | Neighborhood GPS coordinates |
| neighborhood_inventory.json | Raw neighborhood inventory |
| neighborhood_inventory_clean.json | Cleaned neighborhood inventory |
| neighborhood_inventory_final.json | Final neighborhood inventory |

### intents/
| File | Description |
|------|-------------|
| buy_property.json | Buy intent keywords and expressions |
| investor_intent.json | Investor intent with diaspora info |
| rent_property.json | Rent intent keywords |
| search_property.json | Search property intent |
| sell_property.json | Sell intent keywords and signals |

### neighborhoods/
| File | Description |
|------|-------------|
| all_neighborhoods.json | Aggregated neighborhoods |
| bafoussam.json | Bafoussam neighborhoods |
| bamenda.json | Bamenda neighborhoods |
| buea.json | Buea neighborhoods |
| douala.json | Douala neighborhoods |
| garoua.json | Garoua neighborhoods |
| kribi.json | Kribi neighborhoods |
| limbe.json | Limbe neighborhoods |
| maroua.json | Maroua neighborhoods |
| nkongsamba.json | Nkongsamba neighborhoods |
| yaounde.json | Yaounde neighborhoods |

### typo_database/
| File | Description |
|------|-------------|
| cities_typo.json | City typo mappings |
| neighborhoods_typo.json | Neighborhood typo mappings |
| property_types_typo.json | Property type typos |
| typo_database.json | Master typo database |
| whatsapp_typo.json | WhatsApp-specific typos |

### whatsapp_language/
| File | Description |
|------|-------------|
| diaspora_language.json | Diaspora language expressions |
| investor_language.json | Investor language expressions |
| negotiation.json | Negotiation expressions |
| property_listing.json | Property listing expressions |
| property_search.json | Property search expressions |
| urgency_signals.json | Urgency signal expressions |
| whatsapp_language.json | Multilingual WhatsApp examples |

### scoring/
| File | Description |
|------|-------------|
| lead_scoring_rules.json | Lead scoring weight rules |

### search_aliases/
| File | Description |
|------|-------------|
| search_aliases.json | Search alias mappings |

### pricing/
| File | Description |
|------|-------------|
| pricing.json | Pricing data |
| pricing_expressions.json | Price expression patterns |

### pricing_expressions/
| File | Description |
|------|-------------|
| pricing_expressions.json | Price expression patterns |

### property_types/
| File | Description |
|------|-------------|
| property_types.json | Property type taxonomy |

### real_estate/
| File | Description |
|------|-------------|
| property_taxonomy.json | Property taxonomy v1 |
| property_taxonomy_v2.json | Property taxonomy v2 with furnished criteria |

### vocabulary/
| File | Description |
|------|-------------|
| real_estate_vocabulary.json | Real estate vocabulary |

### master/ (Architecture docs)
| File | Description |
|------|-------------|
| 01_ARCHITECTURE_V1.md | Architecture overview |
| 02_CRM_V1.md | CRM design |
| 03_GEOGRAPHY_V1.md | Geography module |
| 04_MATCHING_V1.md | Matching engine |
| 05_SCORING_V1.md | Scoring system |
| 06_ACTORS_V1.md | Actors/roles |
| 07_TRACKING_V1.md | Tracking system |
| 08_SERVICES_V1.md | Services |
| 09_LEARNING_ENGINE_V1.md | Learning engine |
| 10_DATA_QUALITY_V1.md | Data quality |
| 11_STORAGE_ARCHITECTURE_V1.md | Storage |
| 12_DATA_DICTIONARY_V1.md | Data dictionary |
| 13_DATABASE_BLUEPRINT_V1.md | Database blueprint |
| 14_SCHEMA_PRISMA_V1.md | Prisma schema |
| 15_IMPLEMENTATION_MASTER_PLAN_V1.md | Implementation plan |

### REFERENCE/
| File | Description |
|------|-------------|
| 00-INDEX.md | Reference index |
| 01-FUNCTIONAL-SPECIFICATION.md | Functional spec |
| 02-CONVERSATION.md | Conversation reference |
| 03-PROPERTY-QUALIFICATION.md | Property qualification |
| 04-DASHBOARDS.md | Dashboard reference |
| 05-AUTHENTICATION.md | Authentication |
| 06-WORKFLOWS.md | Workflows |
| 07-BUSINESS-RULES.md | Business rules |
| 08-ARCHITECTURE.md | Architecture |
| 09-MIGRATION-GUIDE.md | Migration guide |
| Trnsmiission.md | Transmission content |

### _archive/ (Historical v1 snapshots)
Contains 27 JSON files including: cameroon_cities_v1.json, cities_typo_v1.json, crm_schema_v1.json, entity_linking_v1.json, investor_language_v1.json, investors_v1.json, lead_scoring_v1.json, negotiation_v1.json, neighborhoods_typo_v1.json, pricing_v1.json, property_types_v1.json, search_optimization_v1.json, title_status_v1.json, urgency_signals_v1.json, user_roles_v1.json, whatsapp_language_v1.json, etc.

### _repair_backup/ (Backup during repair)
Contains ~60 JSON files representing intermediate repair states.

### Additional Source Files (LAWIM Root)
| File | Description |
|------|-------------|
| 4-Matching Engine LAWIM.docx | Matching engine architecture (15.8KB) |
| 3-Request Engine - Module 3.docx | Request engine architecture (16KB) |
| 18_QUALIFICATION_MATRIX_IMPLEMENTATION.md | Qualification matrix |
| buea_lookup.txt | Buea neighborhood GPS lookup results |
| cameroon_geography_before_mass_gps_20260610_084253.json | Pre-mass-GPS geography |
| MATCHING_ENGINE_V1_SUMMARY.md | Matching engine summary |
| MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md | Matching engine scope |
| MATCHING_ENGINE_PHASE0_ARCHITECTURE.md | Phase 0 architecture |
| GEO_REFERENCE_MODEL_CAMEROON_V4.md | Geography reference model |

## Total Source Files Count
- KNOWLEDGE/ top-level: 26 files
- geography/: 11 files  
- cities/: 2 files
- intents/: 5 files
- neighborhoods/: 11 files
- whatsapp_language/: 7 files
- typo_database/: 5 files
- master/: 15 files
- REFERENCE/: 11 files
- _archive/: 27 files
- _repair_backup/: ~60 files
- Other directories: ~25 files
- LAWIM root sources: ~15 files
- **Total inventoried: ~220 files**
