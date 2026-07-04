# AAC-B media registry compatibility

## Objectif

The AAC-B media registry work introduces a provider-oriented media abstraction while preserving the existing media API and runtime behavior.

## Compatibility guarantees

- Existing media rows continue to work without requiring a data migration.
- New media rows default to the local provider (`provider_name = local`) when no provider metadata is supplied.
- Legacy rows that predate the new media columns are interpreted with safe defaults:
  - `provider_name = local`
  - `provider_object_id = NULL`
  - `lifecycle_state = active`
  - `backup_state = available`
- Hard deletes use persisted provider metadata when available, and fall back to the legacy storage path parser for older rows.
- Google Drive URLs are rejected to keep unsupported external storage references out of the registry.

## Validation commands

```bash
python3 -m unittest tests.test_media_registry_aac_b -v
cd frontend && npm test
cd frontend && npm run build
```

## Notes

The implementation remains additive and backward-compatible: no existing business media APIs were changed, and DTO responses expose the new provider metadata in an extension-safe way.
