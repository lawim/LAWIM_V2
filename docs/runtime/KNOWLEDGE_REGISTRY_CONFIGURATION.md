# Knowledge Registry Configuration

## Feature Flags

| Variable | Default | Description |
|----------|---------|-------------|
| `LAWIM_KNOWLEDGE_RUNTIME_ENABLED` | `false` | Enable knowledge loading |
| `LAWIM_KNOWLEDGE_INTERNAL_API_ENABLED` | `false` | Enable v4 internal API |

Canonical constant names in `LAWIM_FEATURE_KNOWLEDGE_RUNTIME` and `LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API`.

## KnowledgeConfig

```python
@dataclass(frozen=True)
class KnowledgeConfig:
    property_taxonomy_path: Path  = docs/domain_extension/property_taxonomy_extensions.json
    service_taxonomy_path: Path   = docs/domain_extension/service_taxonomy_extensions.json
    roles_path: Path              = docs/domain_extension/identity_role_extensions.json
    intents_path: Path            = docs/domain_extension/intent_request_extensions.json
    transactions_path: Path       = docs/domain_extension/intent_request_extensions.json
    matrices_path: Path           = docs/.../qualification_matrices.json
    fields_path: Path             = docs/.../field_dictionary.json
    readiness_path: Path          = docs/.../readiness_rules.json
    question_rules_path: Path     = docs/.../question_rules.json
    matching_semantics_path: Path = docs/.../matching_semantics.json
    runtime_enabled: bool         = False
    internal_api_enabled: bool    = False
    project_root: Path            = .
```

All source paths are relative to `project_root`.
