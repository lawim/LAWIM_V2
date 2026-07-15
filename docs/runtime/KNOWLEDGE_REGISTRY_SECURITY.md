# Knowledge Registry Security

## Access Control

- All v4 API endpoints are gated by the `LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API` feature flag.
- When disabled, `KnowledgeApiHandler` raises `ApiDisabledError`.
- Authentication required (via `_require_user()` in server.py handler).
- All endpoints are read-only; no mutation operations exist.

## Data Protection

- No sensitive data is exposed through the knowledge registries directly. The registry data is canonical knowledge (property types, field dictionaries, etc.), not user data.
- Source file validation prevents path traversal by checking file existence with `Path.is_file()`.
- Maximum JSON file size capped at 50 MiB (`MAX_JSON_FILE_SIZE_BYTES`).

## Feature Flag Defaults

Both `runtime_enabled` and `internal_api_enabled` default to `false`, ensuring knowledge runtime is inert by default.
