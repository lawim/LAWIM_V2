# Structure Details — LCIP A.1

## Arborescence générée

```
tests/gold_corpus/
├── README.md
├── schema/
│   ├── conversation.schema.json
│   ├── expected_state.schema.json
│   ├── expected_business.schema.json
│   ├── expected_questions.schema.json
│   ├── expected_language.schema.json
│   ├── expected_runtime.schema.json
│   └── assertions.schema.json
├── categories/
│   ├── purchase/
│   ├── rental/
│   ├── seller/
│   ├── visit/
│   ├── investment/
│   ├── multilingual/
│   ├── correction/
│   ├── restart/
│   ├── idempotence/
│   ├── negotiation/
│   ├── qualification/
│   ├── marketplace/
│   ├── followup/
│   └── edge_cases/
├── conversations/           ← vide, prêt à recevoir des conversations
├── validators/
│   ├── __init__.py
│   ├── validate_schema.py
│   ├── validate_conversation.py
│   ├── validate_assertions.py
│   └── validate_business.py
├── benchmark/
│   ├── __init__.py
│   ├── run_gold_benchmark.py
│   ├── score.py
│   └── report.py
├── statistics/
│   ├── __init__.py
│   └── build_statistics.py
├── manifests/               ← prêt
├── reports/                 ← prêt
└── examples/
    └── B000001/
        ├── conversation.json
        ├── expected_state.json
        ├── expected_business.json
        ├── expected_questions.json
        ├── expected_language.json
        ├── expected_runtime.json
        ├── expected_assertions.json
        └── rationale.md
```

## Statistiques

- Dossiers : 25 (incluant sous-dossiers)
- Fichiers : 48
- Schémas : 7
- Scripts Python : 8
- Exemple conversation : 1 (8 fichiers)

## Contrôle

STRUCT-0001 : PASS
