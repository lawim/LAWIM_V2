# LAWIM_V2 MEGA WAVE 004 — Property Platform Report

- Date: 2026-06-29
- Scope: first business platform (Property, Media, Geo, Persistence)
- Reference branch: `develop`
- Target tag: `mega-wave-004-property-platform`

## 1. Executive Summary

MEGA WAVE 004 delivers the first cohesive business platform for LAWIM_V2 on top of the hardened executable baseline. The wave introduces schema v4, domain modules for property/media/geo, repository contracts, SQLite persistence adapter, prepared PostgreSQL adapter profile, paginated API contracts, optimistic locking, soft delete, local media storage, and a significantly expanded test suite (14 tests). SQLite remains the live runtime; PostgreSQL is prepared but not activated.

## 2. Architectural Decisions

- **Schema v4 over in-place migration**: existing SQLite databases are upgraded with additive `ALTER TABLE` steps instead of destructive rebuilds.
- **Domain modules over monolith growth**: property, media, and geo rules live in dedicated modules; `db.py` remains the SQLite repository implementation.
- **Repository contract via Protocols**: `repository_contract.py` documents the persistence surface without forcing premature abstraction splits.
- **Adapter factory**: `persistence_adapter.py` resolves SQLite (live) vs PostgreSQL (prepared) through `LAWIM_DB_DRIVER`.
- **DTO layer at service boundary**: API responses are normalized in `services.py` using `dto.py`, keeping HTTP handlers thin.
- **Optimistic locking**: property and media updates require matching `version`; conflicts return HTTP 409.
- **Soft delete by default**: properties with conversations and all media records are soft-deleted; hard delete remains available where safe.
- **Local media storage**: uploads are persisted under `LAWIM_MEDIA_STORAGE_PATH` and served from `/media/…`.

## 3. Components Developed

| Area | Files |
|------|-------|
| Persistence contracts | `code/lawim_v2/repository_contract.py`, `code/lawim_v2/persistence_adapter.py`, `code/lawim_v2/errors.py` |
| Property domain | `code/lawim_v2/property_domain.py` |
| Media domain | `code/lawim_v2/media_domain.py` |
| Geo domain | `code/lawim_v2/geo_domain.py` |
| API query/pagination | `code/lawim_v2/api_query.py`, `code/lawim_v2/dto.py` |
| Schema v4 + migrations | `code/lawim_v2/db.py`, `code/lawim_v2/persistence.py` |
| Service/API integration | `code/lawim_v2/services.py`, `code/lawim_v2/server.py`, `code/lawim_v2/config.py` |
| Tests | `tests/test_lawim_v2.py` (+5 platform tests) |

## 4. Components Reused

- `LawimRepository` SQLite implementation (extended, not replaced)
- `LawimServices` + `AccessPolicy` RBAC matrix
- `matching.py` geo-distance scoring
- Demo seed blueprint in `persistence.py`
- Docker compose contract (`compose/` and `docker/compose/`)
- Static browser console (`static/`)

## 5. API

| Method | Route | Notes |
|--------|-------|-------|
| GET | `/api/properties` | Pagination, filtering, sorting, search |
| GET | `/api/properties/{id}` | Property DTO + embedded media |
| POST | `/api/properties` | Extended property payload |
| PATCH/DELETE | `/api/properties/{id}` | Version-aware updates, soft delete |
| POST | `/api/properties/{id}/publish` | Publication workflow |
| GET | `/api/media` | Paginated media listing |
| GET | `/api/media/{id}` | Media DTO |
| POST | `/api/media` | URL-based media create |
| POST | `/api/media/upload` | Base64 upload to local storage |
| PATCH/DELETE | `/api/media/{id}` | Version-aware updates, soft delete |
| GET | `/api/geo/normalize` | Address/city/country normalization |
| GET | `/api/geo/search` | Location search preparation |
| GET | `/api/geo/contracts` | Thumbnail contract metadata |
| GET | `/media/{path}` | Served local media assets |

## 6. Persistence

- Schema version: **4**
- New property fields: `listing_code`, address/geo fields, `availability`, `metadata_json`, `version`, `published_at`, `deleted_at`, `search_key`
- New media fields: `storage_path`, `mime_type`, `size_bytes`, `thumbnail_url`, `metadata_json`, `position`, `version`, `deleted_at`
- SQLite adapter: `sqlite-repository` (live)
- PostgreSQL adapter: `postgresql-repository-prepared` (profile + factory guard)
- Audit events extended: `property_soft_deleted`, `media_soft_deleted`

## 7. Property Platform

- Listing codes generated automatically
- Lifecycle: draft → open → published → closed/archived
- Availability states: available, reserved, sold, rented, unavailable
- Publication rules enforced via `can_publish`
- Ownership remains organization-scoped with existing RBAC

## 8. Media Platform

- `MediaStorage` abstraction with `LocalMediaStorage`
- Upload contract: filename + base64 content
- Thumbnail contract: deterministic SVG placeholder (256px edge)
- Property relation preserved with cascade semantics

## 9. Geo Platform

- Normalization for city, country, region, postal code
- Coordinates validation (paired lat/lon)
- Search key generation for future indexing
- Location search aggregates distinct city/region/country groups from live properties

## 10. Tests

- 14 unittest integration tests (was 9)
- New coverage: pagination/DTO, geo normalize/search, media upload, publish, optimistic locking, PostgreSQL adapter profile
- All validations PASS:
  - `python3 -m compileall lawim_v2 code/lawim_v2 tests/test_lawim_v2.py`
  - `python3 -m unittest discover -s tests -v`
  - `python3 -m lawim_v2 --help`
  - `git diff --check`
  - Docker compose config (both overlay trees)

## 11. Docker

- No compose structural changes required
- New runtime env: `LAWIM_MEDIA_STORAGE_PATH` (optional, defaults to `data/runtime/media`)
- Optional future switch: `LAWIM_DB_DRIVER=postgresql` (prepared profile only)

## 12. Risks

- PostgreSQL adapter is prepared but not executable; switching driver without implementation will fail at startup by design.
- Soft-deleted properties remain in database; admin `include_deleted` listing is available but not exposed in UI.
- Media uploads are local-disk only; no CDN or virus scanning in this wave.

## 13. Limits

- No Prisma schema generation or migration runner yet
- No multipart HTTP upload (JSON base64 only)
- No geocoding external provider integration
- Browser console not updated for new platform fields

## 14. Preparation MEGA WAVE 005

Recommended focus for MEGA WAVE 005:

- Activate PostgreSQL adapter with Prisma schema generated from manifest fingerprint
- Conversation/negotiation platform deepening
- External geocoding provider integration
- Multipart media upload and CDN-ready storage backend
- UI alignment with property/media/geo DTO contracts

## 15. Final YAML

```yaml
wave: MEGA_WAVE_004
status: READY_FOR_DG_REVIEW
architecture: PASS
backend: PASS
api: PASS
property: PASS
media: PASS
geo: PASS
tests: PASS
compose: PASS
blocking_risk: false
next_wave: MEGA_WAVE_005
decision_required: true
```
