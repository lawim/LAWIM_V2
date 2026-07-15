# Knowledge Registry Implementation

## Overview

The Knowledge Runtime (`code/lawim_v2/knowledge_runtime/`) provides in-memory loading, validation, and read-only access to canonical LAWIM knowledge sources. It is the bridge between the canonical documentation (Heritage Gold, Domain Extensions) and runtime engine consumption.

## Architecture

```
knowledge_runtime/
├── __init__.py          # Package entry, exports KnowledgeService
├── config.py            # KnowledgeConfig dataclass
├── constants.py         # Constants, statuses, default source paths, feature flag names
├── errors.py            # Structured error hierarchy
├── service.py           # KnowledgeService orchestration
├── models/
│   ├── __init__.py      # All model exports
│   ├── common.py        # Shared: KnowledgeIdentifier, KnowledgeSource, ValidationIssue, etc.
│   ├── version.py       # KnowledgeVersion with deterministic hash computation
│   ├── taxonomy.py      # PropertyType, ServiceType
│   ├── role.py          # Role with dimension classifier
│   ├── intent.py        # Intent
│   ├── transaction.py   # Transaction
│   ├── qualification.py # QualificationMatrix
│   ├── field.py         # FieldDefinition
│   ├── readiness.py     # ReadinessDefinition, ReadinessLevel enum
│   ├── question_rule.py # QuestionRule
│   ├── matching_semantic.py # MatchingSemantic
│   └── source_trace.py  # SourceTrace
├── registry/
│   ├── __init__.py      # All registry exports
│   ├── base.py          # BaseRegistry with immutability pattern
│   ├── errors.py        # Registry-specific errors
│   ├── property_registry.py    # PropertyTaxonomyRegistry
│   ├── service_registry.py     # ServiceTaxonomyRegistry
│   ├── role_registry.py        # RoleRegistry (8 dimensions)
│   ├── intent_registry.py      # IntentRegistry
│   ├── transaction_registry.py # TransactionRegistry
│   ├── matrix_registry.py      # MatrixRegistry (5 match types)
│   ├── field_registry.py       # FieldRegistry (rejects unknown types)
│   ├── readiness_registry.py   # ReadinessRegistry (7 levels)
│   ├── question_rule_registry.py # QuestionRuleRegistry
│   ├── matching_semantic_registry.py # MatchingSemanticRegistry (9 semantics)
│   ├── source_trace_registry.py     # SourceTraceRegistry
│   └── version_registry.py     # KnowledgeVersionRegistry
├── loaders/
│   ├── __init__.py
│   ├── base.py          # BaseLoader ABC
│   └── json_loader.py   # All JSON knowledge loaders + aggregate load_all_knowledge()
├── validation/
│   ├── __init__.py
│   ├── schema.py        # SchemaValidator (JSON validation)
│   ├── reference.py     # ReferenceValidator (cross-ref validation)
│   └── startup.py       # StartupValidator (feature flags, registry emptiness)
└── api/
    ├── __init__.py
    └── handler.py       # KnowledgeApiHandler (read-only protected endpoints)
```

## Registries Implemented

| Registry | Source File | Records | Key Features |
|----------|-------------|---------|-------------|
| PropertyTaxonomyRegistry | property_taxonomy_extensions.json | 7+ families | Hierarchy, alias, cycle detection |
| ServiceTaxonomyRegistry | service_taxonomy_extensions.json | 11+ families | Family-based lookup |
| RoleRegistry | identity_role_extensions.json | 23+ roles | 8 dimensions validated |
| IntentRegistry | intent_request_extensions.json | 6 intents | Extension-category filtered |
| TransactionRegistry | intent_request_extensions.json | 8 transactions | Type-based lookup |
| MatrixRegistry | qualification_matrices.json | 75+ matrices | 5 match modes |
| FieldRegistry | field_dictionary.json | 130+ fields | Type validation, 7 data types |
| ReadinessRegistry | readiness_rules.json | 7 levels | Sorted by order |
| QuestionRuleRegistry | question_rules.json | 50+ rules | 5 rule types, dedup validation |
| MatchingSemanticRegistry | matching_semantics.json | 9 semantics | All 9 required |
| SourceTraceRegistry | (derived) | n/a | Provenance tracking |
| KnowledgeVersionRegistry | (computed) | 1 | Deterministic hash |
