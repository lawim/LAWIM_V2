# Geographic Scoring Methodology

## Source
LAWIM Matching Engine Module 4 documentation, location-segmentation-canonical.md

## Weight
Geographic compatibility = **20%** of total match score

## Scoring Levels

| Level | Condition | Score |
|-------|-----------|-------|
| 1 | Exact requested neighborhood | Maximal |
| 2 | Explicitly accepted alternative | High |
| 3 | Neighboring district (business-compatible) | Medium |
| 4 | Same city, distant zone | Low |
| 5 | Incompatible zone | Minimal |

## Key Rules

1. **User preference always wins**: Explicitly stated preferences override algorithmic assumptions
2. **Business logic over GPS**: Neighborhood affinity considers lifestyle, standing, and market reality - not just distance
3. **No cross-city substitution**: Never replace an uncovered city with a neighboring one
4. **Mobility radius**: Measured via `mobility_radius_m` and `mobility_mode` (STRICT/FLEXIBLE/VERY_FLEXIBLE)

## Neighborhood Affinity

Defined in `aliases.json` under `neighborhood_affinities`. Compatible pairs:
- Bastos Haut <-> Golf, Santa Barbara, Omnisports Haut Bastos
- Soa <-> Nkoabang, Mbankomo

## Non-Compatible Pairs
- Bastos Haut <-> Omnisports Popular, Mokolo Marché
- Golf <-> Omnisports Popular

## Request Lifecycle

1. User specifies primary neighborhood + optional alternatives
2. System matches against inventory
3. If no match: WAITLISTED with NO_ACTIVE_MATCH
4. Never auto-suggest different city
