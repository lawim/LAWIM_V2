# Knowledge Registry Operations

## Loading

1. `KnowledgeService(config).load_all()` reads all canonical source files.
2. Each loader parses its JSON source and registers items into the corresponding registry.
3. `SourceTraceRegistry` records provenance for every loaded concept.
4. `KnowledgeVersion` is computed deterministically from sorted source checksums + commit hash.
5. All registries are locked (immutable) after loading.

## Validation

- **StartupValidator**: Checks feature flags, registry emptiness, schema version.
- **SchemaValidator**: Validates JSON files exist, parse, and have expected structure.
- **ReferenceValidator**: Validates cross-references between registries (e.g., matrix fields exist in field registry).

## Health

`KnowledgeService.health()` returns:
- `status`: DISABLED | READY | FAILED
- `loaded_at`: ISO timestamp or null
- `version`: deterministic version dict or null
- `registries`: counts per registry
- `sources`: list of loaded source metadata
- `config`: feature flag state

## Version Computation

```
knowledge_version = sha256(
    sorted(source_checksums) +
    "commit:" + build_commit
)[:16]
```

The version is deterministic: same sources + same commit = same version hash.

## Error States

| Status | Meaning |
|--------|---------|
| DISABLED | Runtime feature flag is off |
| LOADING | Loading in progress |
| READY | All registries loaded and locked |
| DEGRADED | Partial load with warnings |
| FAILED | Loading threw exception |
