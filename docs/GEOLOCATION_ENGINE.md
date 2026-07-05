# GEOLOCATION_ENGINE

## Purpose

This document describes the selective geo integration added to LAWIM_V2 from the LAWIM and LAWIMA sources.

The goal is not to replace the existing runtime geo stack. The goal is to enrich it with a curated, local-only reference layer that improves:

- city normalization;
- neighborhood search;
- deterministic local geocoding;
- search results exposed by `/api/geo/search`;
- matching support when coordinates are available.

## Runtime Components

- `code/lawim_v2/geo_domain.py`
  - normalizes country, city, region, postal code, and coordinates;
  - now resolves city aliases through the curated reference catalog.
- `code/lawim_v2/geo_reference.py`
  - loads and validates the curated Cameroon location catalog;
  - resolves city aliases and neighborhood references;
  - ranks search results without any external service.
- `code/lawim_v2/geocoding_provider.py`
  - keeps the existing external provider optional;
  - the local provider now anchors itself on the curated catalog before applying a deterministic fallback.
- `code/lawim_v2/services.py`
  - merges property-backed locations and curated reference locations for `/api/geo/search`.
- `code/lawim_v2/matching.py`
  - continues to own distance calculation via Haversine.

## Behavioral Rules

- No internet call is required for the local geo path.
- No secret is loaded from LAWIMA.
- The curated catalog is treated as safe only after validation.
- If a neighborhood has no exact coordinates, the runtime falls back to the parent city anchor and then to a deterministic offset.

## Current Scope

The first curated bundle focuses on:

- Douala;
- Yaounde;
- Kribi;
- Bamenda;
- Bafoussam;
- Buea;
- Nkongsamba;
- Maroua;
- Limbe;
- Garoua;
- key neighborhoods from Douala and Yaounde.

This is intentionally selective. It is not a full territorial atlas yet.

## Status

- Geo Intelligence release closed and certified on 2026-07-05.
- The runtime remains offline, deterministic, and local-only.
