# Turn Specification Details — LCIP A.2

## Fichier créé

`tests/gold_corpus/specification/schema/turn_spec.schema.json`

## Contenu

Spécification complète d'un tour de conversation :

| Propriété | Description |
|-----------|-------------|
| turn_number | Numéro du tour |
| user_input | Texte canonique + variants + langue |
| expected_intent | Intention attendue |
| expected_entities | Entités extraites |
| facts_extracted | Faits avec source |
| memory_changes | set/unset de mémoire |
| allowed_questions | Questions autorisées (max 1) |
| forbidden_questions | Questions interdites |
| expected_transition | from_phase → to_phase + action |
| assertions | Identifiants d'assertions |

## Validation

```bash
python -c "import json; json.load(open('tests/gold_corpus/specification/schema/turn_spec.schema.json'))"
```

## Contrôle

TURN-0001 : PASS
