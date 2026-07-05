# REFERENCE_DATA

## Curated Geo Bundle

LAWIM_V2 now carries a curated Cameroon location bundle at:

- `code/lawim_v2/data/cameroon_locations.json`

The bundle is built from:

- `LAWIM/ARCHIVES/GEO_REFERENCE_MODEL_CAMEROON_V4.md`
- `LAWIM/ARCHIVES/GEO_MODEL_ALIGNMENT_PLAN.md`
- `LAWIMA/02_KNOWLEDGE/cities/cameroon_cities.json`
- `LAWIMA/02_KNOWLEDGE/neighborhoods/douala.json`
- `LAWIMA/02_KNOWLEDGE/neighborhoods/yaounde.json`

## Data Shape

The file is split into:

- `cities`
- `neighborhoods`

Each entry can carry:

- `kind`
- `name`
- `city`
- `region`
- `department`
- `aliases`
- `typos`
- `landmarks`
- `informal_references`
- `related_zones`
- `target`
- `common_property_types`
- `sources`
- `confidence`
- optional `latitude` and `longitude`

## Safety Rules

- No secret, token, password, or API key is allowed in the curated bundle.
- The bundle must remain local-only and deterministic.
- If an entry cannot be validated, it must be rejected at load time.
- The reference data is allowed to enrich search and normalization, but it must not bypass runtime validation.

## Update Rule

When new entries are added:

1. normalize names and aliases;
2. document the source path;
3. keep coordinates optional;
4. keep confidence explicit;
5. add regression tests for any new alias or neighborhood behavior.

## Status

- The current curated Cameroon bundle is certified for runtime use after validation on 2026-07-05.
