# Search Criteria Documentation

## Source: LAWIM KNOWLEDGE/search_aliases/search_aliases.json + KNOWLEDGE/minimum-fields-request.md

## Core Search Dimensions

| # | Dimension | Type | Required | Description |
|---|-----------|------|----------|-------------|
| 1 | Transaction Type | enum | Yes | buy, rent, sell, invest |
| 2 | Property Type | enum | Yes | apartment, house, land, commercial, etc. |
| 3 | City | string | Yes | Target city |
| 4 | Neighborhood | string | No | Specific neighborhood (optional if city-level) |
| 5 | Budget | number | Yes | Maximum budget or price range |
| 6 | Bedrooms | integer | No | Minimum number of bedrooms |
| 7 | Bathrooms | integer | No | Minimum number of bathrooms |
| 8 | Surface (m²) | number | No | Minimum surface area |
| 9 | Title Status | enum | No | titled, untitled, in_progress |
| 10 | Furnished | boolean | No | furnished or unfurnished |
| 11 | Condition | enum | No | new, good, needs_work |
| 12 | Amenities | string[] | No | Required amenities (ac, parking, etc.) |
| 13 | Timeline | string | No | Move-in date or deadline |
| 14 | Mobility Mode | enum | No | STRICT, FLEXIBLE, VERY_FLEXIBLE |

## Search Behavior Rules

### Intent → Default Criteria Mapping

| Intent | Default Required Criteria |
|--------|--------------------------|
| BUY | transaction_type=buy, property_type, city, budget |
| RENT | transaction_type=rent, property_type, city, budget (monthly) |
| SELL | transaction_type=sell, property_type, city, asking_price |
| INVEST | transaction_type=invest, budget, city, strategy |
| SEARCH | city, budget, property_type (inferred) |

### Budget Search Rules

| Condition | Behavior |
|-----------|----------|
| Budget is preference (not constraint) | Show properties slightly above/below with score penalty |
| Budget missing | Stop qualification - budget is mandatory before matching |
| Budget in EUR/USD/XAF | Accept all, normalize to XAF for matching |
| Budget expressed per m² | Calculate total based on surface hints |

### Location Search Rules

- If city is provided without neighborhood: search entire city
- If neighborhood is provided: score exact match highest, alternatives next
- If city is not covered: WAITLISTED with message
- Never auto-substitute a different city

### Keyword Search (Search Intent)

When intent is SEARCH_PROPERTY (unqualified), extract criteria from natural language:

| Expression | Extracted Criteria |
|------------|-------------------|
| "maison pas chère à Douala" | property_type=maison, city=Douala, budget=low |
| "terrain 500m² Yaoundé titré" | property_type=terrain, surface=500, city=Yaoundé, title_status=titled |
| "appartement 2 chambres meublé" | property_type=appartement, bedrooms=2, furnished=true |

### Search Alias Resolution

Common search aliases (from search_aliases.json):
- "pas cher", "abordable", "bon plan", "promo" → budget = low range
- "grand terrain", "vaste", "spacieux" → surface = large
- "bien situé", "centre", "accessible" → location_quality = high
- "calme", "tranquille", "résidentiel" → noise_level = low
- "sécurisé", "quartier sûr" → security = high

### Agent Search Behavior

When an agent searches for leads:
- Filter by zone (city/neighborhood specialization)
- Filter by property type specialty
- Sort by match score descending
- Max 5 leads per batch
- Boost: verified listings first

## Implementation Notes

- Search criteria are stored in Request model fields
- Each field maps to a matching dimension
- Missing required fields → MISSING_CORE_FIELDS status
- All fields collected → QUALIFIED → MATCH_READY
- Search criteria validation must happen before match execution
